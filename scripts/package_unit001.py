#!/usr/bin/env python3
"""Create the deterministic public translation-overlay bundle for Unit 001."""

from __future__ import annotations

import hashlib
import json
import stat
import zipfile
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
OUTPUT = LANE / "output" / "TRANSLATION_OVERLAY_AND_BACKEND_ID_UNIT_001.zip"
PUBLIC_FILES = (
    "README.md",
    "README_RELEASE.md",
    "CITATION.cff",
    "LICENSE.md",
    "00_control/BUILD_BASELINE.md",
    "00_control/COVERAGE_AND_ASSESSMENT.md",
    "00_control/CURRENT_CURSOR.md",
    "00_control/CURRENT_STATE.md",
    "00_control/DECISION_LOG.md",
    "00_control/RIGHTS_AND_COMPONENTS.md",
    "00_control/SOURCE_AUTHORITY.md",
    "00_control/TERMINOLOGY.csv",
    "backend/README.md",
    "backend/catalog-v0.json",
    "backend/concepts-ch01-id-v0.csv",
    "backend/exercise-hints-v0.csv",
    "backend/figure-descriptions-id-v0.csv",
    "backend/schema-v0.json",
    "backend/unit-order-v0.csv",
    "scripts/build_reader_id.ps1",
    "scripts/build_unit001_hints.ps1",
    "scripts/fetch_and_build_unit001.ps1",
    "scripts/make_unit001_reader.py",
    "scripts/package_unit001.py",
    "scripts/qa_first_unit.py",
    "source/id-ID/all-lectures.tex",
    "source/id-ID/locale-id.tex",
    "source/id-ID/title.tex",
    "source/id-ID/intro.tex",
    "source/id-ID/metric.tex",
    "source/id-ID/hints.tex",
    "qa/UNIT001_ADMISSION_20260821.md",
    "output/UNIT001_READER_RECEIPT.json",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def info(name: str) -> zipfile.ZipInfo:
    value = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    value.compress_type = zipfile.ZIP_DEFLATED
    value.create_system = 3
    value.external_attr = (stat.S_IFREG | 0o644) << 16
    return value


def main() -> None:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite {OUTPUT}")
    rows: list[dict[str, object]] = []
    payload: list[tuple[str, bytes]] = []
    for relative in PUBLIC_FILES:
        path = LANE / Path(relative)
        if not path.is_file():
            raise SystemExit(f"missing public file: {relative}")
        data = path.read_bytes()
        if b"P22-Underground-Reg.ttf" in data or b"P22UndergroundCYBookSC.ttf" in data:
            # Documentary rights ledgers name excluded files; only actual binary
            # payloads are forbidden. Font signatures would start with sfnt/OTTO,
            # while these selected public files are text/JSON/PDF-receipt only.
            if path.suffix.lower() not in {".md", ".json", ".py", ".ps1", ".tex", ".csv", ".cff"}:
                raise SystemExit(f"excluded font payload suspected: {relative}")
        rows.append({"path": relative, "bytes": len(data), "sha256": digest(data)})
        payload.append((relative, data))

    manifest = {
        "schema": "o004-unit001-overlay-manifest-v0",
        "scope": "translation-overlay-and-backend; no-complete-upstream-generator-closure",
        "files": rows,
    }
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    payload.append(("FILE_MANIFEST.json", manifest_bytes))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative, data in payload:
            archive.writestr(info(relative), data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    with zipfile.ZipFile(OUTPUT) as archive:
        if archive.testzip() is not None:
            raise SystemExit("ZIP CRC verification failed")
        names = archive.namelist()
        expected = [name for name, _ in payload]
        if names != expected:
            raise SystemExit("ZIP entry order/set mismatch")
        for name, data in payload:
            if archive.read(name) != data:
                raise SystemExit(f"ZIP byte mismatch: {name}")

    print(
        json.dumps(
            {
                "path": str(OUTPUT),
                "entries": len(payload),
                "bytes": OUTPUT.stat().st_size,
                "sha256": digest(OUTPUT.read_bytes()),
                "manifest_sha256": digest(manifest_bytes),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
