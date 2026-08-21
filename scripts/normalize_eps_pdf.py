#!/usr/bin/env python3
"""Remove live conversion metadata from one EPS-derived PDF deterministically."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, ByteStringObject, NameObject


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-eps", required=True, type=Path)
    parser.add_argument("--input-pdf", required=True, type=Path)
    parser.add_argument("--output-pdf", required=True, type=Path)
    args = parser.parse_args()

    for path in (args.source_eps, args.input_pdf):
        if not path.is_file():
            raise SystemExit(f"missing input: {path}")
    if args.output_pdf.exists():
        raise SystemExit(f"output already exists: {args.output_pdf}")

    reader = PdfReader(args.input_pdf)
    if len(reader.pages) != 1:
        raise SystemExit(f"expected one EPS-derived page, found {len(reader.pages)}")

    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer.root_object.pop(NameObject("/Metadata"), None)
    writer.metadata = None

    # Remove the now-unreachable live XMP/Info objects before serialization.
    writer.compress_identical_objects(remove_duplicates=False, remove_unreferenced=True)

    # Derive a stable PDF file identifier from the immutable EPS source bytes.
    source_sha256 = hashlib.sha256(args.source_eps.read_bytes()).digest()
    stable_id = ByteStringObject(source_sha256[:16])
    writer._ID = ArrayObject((stable_id, stable_id))

    args.output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with args.output_pdf.open("wb") as stream:
        writer.write(stream)

    check = PdfReader(args.output_pdf)
    if len(check.pages) != 1:
        raise SystemExit("normalized PDF failed page-count readback")
    if check.trailer.get("/Info") is not None:
        raise SystemExit("normalized PDF retains an Info dictionary")
    if check.root_object.get("/Metadata") is not None:
        raise SystemExit("normalized PDF retains an XMP metadata stream")


if __name__ == "__main__":
    main()
