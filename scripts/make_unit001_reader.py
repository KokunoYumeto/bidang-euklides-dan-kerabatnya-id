#!/usr/bin/env python3
"""Create the honest partial O004 Unit 001 reader from admitted PDF pages."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, NameObject, TextStringObject
from reportlab.pdfgen import canvas


PAGE_SIZE = (432, 648)
FULL_PAGE_INDICES = (0, 1, *range(5, 19))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def draw_wrapped(
    pdf: canvas.Canvas,
    text: str,
    *,
    x: float,
    y: float,
    width: float,
    font: str = "Helvetica",
    size: float = 10,
    leading: float = 14,
) -> float:
    words = text.split()
    line = ""
    lines: list[str] = []
    for word in words:
        candidate = f"{line} {word}".strip()
        if pdf.stringWidth(candidate, font, size) <= width or not line:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    pdf.setFont(font, size)
    for value in lines:
        pdf.drawString(x, y, value)
        y -= leading
    return y


def scope_page() -> bytes:
    buffer = io.BytesIO()
    pdf = canvas.Canvas(
        buffer,
        pagesize=PAGE_SIZE,
        invariant=1,
        pageCompression=1,
        bottomup=1,
    )
    pdf.setTitle("Bidang Euklides dan Kerabatnya — Unit Produksi 001")
    pdf.setAuthor("Anton Petrunin")
    pdf.setSubject("Terjemahan bahasa Indonesia parsial: Prakata dan Bab 1")

    left = 48
    width = PAGE_SIZE[0] - 96
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(PAGE_SIZE[0] / 2, 568, "Bidang Euklides dan Kerabatnya")
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_SIZE[0] / 2, 538, "Unit Produksi 001 — Prakata dan Bab 1")
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(PAGE_SIZE[0] / 2, 516, "Bahasa Indonesia — status: edisi parsial")

    y = 474
    y = draw_wrapped(
        pdf,
        "Cakupan unit ini terbatas pada halaman judul dan pemberitahuan lisensi, "
        "Prakata lengkap, Bab 1 (Pendahuluan) lengkap beserta 16 latihan, serta "
        "petunjuk untuk keenam belas latihan tersebut.",
        x=left,
        y=y,
        width=width,
    )
    y -= 10
    y = draw_wrapped(
        pdf,
        "Bab 2–20 belum termasuk dalam unit ini. Dokumen ini bukan terjemahan lengkap "
        "dan tidak boleh dikutip sebagai edisi Indonesia lengkap dari buku tersebut.",
        x=left,
        y=y,
        width=width,
        font="Helvetica-Bold",
    )
    y -= 10
    y = draw_wrapped(
        pdf,
        "Karya asli oleh Anton Petrunin. Terjemahan dan adaptasi teknis ini tidak "
        "didukung atau disahkan oleh penulis asli. Dilisensikan dengan Creative "
        "Commons Atribusi-BerbagiSerupa 4.0 Internasional (CC BY-SA 4.0).",
        x=left,
        y=y,
        width=width,
    )
    y -= 14
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(left, y, "Sumber resmi:")
    y -= 14
    source_url = "https://github.com/anton-petrunin/birkhoff"
    pdf.setFont("Helvetica", 8.5)
    pdf.drawString(left, y, source_url)
    pdf.linkURL(source_url, (left, y - 2, left + pdf.stringWidth(source_url, "Helvetica", 8.5), y + 9))
    y -= 18
    witness_url = "https://arxiv.org/abs/1302.1630v25"
    pdf.drawString(left, y, witness_url)
    pdf.linkURL(witness_url, (left, y - 2, left + pdf.stringWidth(witness_url, "Helvetica", 8.5), y + 9))
    y -= 18
    license_url = "https://creativecommons.org/licenses/by-sa/4.0/"
    pdf.drawString(left, y, license_url)
    pdf.linkURL(license_url, (left, y - 2, left + pdf.stringWidth(license_url, "Helvetica", 8.5), y + 9))

    pdf.setFont("Helvetica-Oblique", 8)
    pdf.drawString(left, 52, "PDF ini belum bertag; sumber terstruktur dan permukaan aksesibel masih dalam produksi.")
    pdf.showPage()
    pdf.save()
    return buffer.getvalue()


def keep_only_uri_annotations(page: object) -> None:
    annotations = page.get("/Annots")
    if not annotations:
        return
    kept = ArrayObject()
    for reference in annotations:
        annotation = reference.get_object()
        action = annotation.get("/A")
        if action and action.get("/S") == "/URI":
            kept.append(reference)
    if kept:
        page[NameObject("/Annots")] = kept
    else:
        page.pop(NameObject("/Annots"), None)


def build(full_pdf: Path, hints_pdf: Path, output: Path) -> dict[str, object]:
    full = PdfReader(str(full_pdf))
    hints = PdfReader(str(hints_pdf))
    if len(full.pages) != 203:
        raise SystemExit(f"expected 203-page full-context build, found {len(full.pages)}")
    if len(hints.pages) != 2:
        raise SystemExit(f"expected 2-page Chapter 1 hint booklet, found {len(hints.pages)}")

    writer = PdfWriter()
    writer.add_page(PdfReader(io.BytesIO(scope_page())).pages[0])
    for index in FULL_PAGE_INDICES:
        writer.add_page(full.pages[index])
    for page in hints.pages:
        writer.add_page(page)

    for page in writer.pages:
        keep_only_uri_annotations(page)

    writer.add_metadata(
        {
            "/Title": "Bidang Euklides dan Kerabatnya — Unit Produksi 001",
            "/Author": "Anton Petrunin",
            "/Subject": "Terjemahan bahasa Indonesia parsial: Prakata dan Bab 1",
            "/Creator": "Pipeline edisi bahasa Indonesia O004/C100",
        }
    )
    writer._root_object[NameObject("/Lang")] = TextStringObject("id-ID")
    writer.add_outline_item("Cakupan Unit Produksi 001", 0)
    writer.add_outline_item("Judul dan lisensi", 1)
    writer.add_outline_item("Prakata", 3)
    writer.add_outline_item("Bab 1 — Pendahuluan", 7)
    writer.add_outline_item("Petunjuk Bab 1", 17)

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as handle:
        writer.write(handle)

    result = {
        "schema": "o004-unit001-reader-v0",
        "status": "partial",
        "locale": "id-ID",
        "full_source_pdf_sha256": sha256(full_pdf),
        "hints_source_pdf_sha256": sha256(hints_pdf),
        "selected_full_pdf_pages_1_based": [index + 1 for index in FULL_PAGE_INDICES],
        "hint_pages": 2,
        "output_pages": len(PdfReader(str(output)).pages),
        "output_bytes": output.stat().st_size,
        "output_sha256": sha256(output),
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-pdf", required=True, type=Path)
    parser.add_argument("--hints-pdf", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args()

    result = build(args.full_pdf.resolve(), args.hints_pdf.resolve(), args.output.resolve())
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
