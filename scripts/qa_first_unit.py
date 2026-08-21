#!/usr/bin/env python3
"""Fail-closed structural QA for the first O004 id-ID production unit."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parents[1]
AUTHORITY = LANE / "source" / "upstream" / "birkhoff-0b0858e1e985f4c8dadbb6075ae9e095cd4a8981"
TARGET = LANE / "source" / "id-ID"
FILES = ("title.tex", "intro.tex", "metric.tex", "hints.tex")


def die(message: str) -> None:
    raise SystemExit(f"QA_FAIL: {message}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def active_text(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        out: list[str] = []
        i = 0
        while i < len(line):
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                break
            out.append(line[i])
            i += 1
        lines.append("".join(out))
    return "\n".join(lines)


def ordered(pattern: str, text: str) -> list[str]:
    return re.findall(pattern, active_text(text), flags=re.DOTALL)


def mask_text_commands(value: str) -> str:
    commands = ("text", "textit", "textrm", "textbf", "intertext", "shortintertext")
    for command in commands:
        marker = "\\" + command + "{"
        while marker in value:
            start = value.index(marker)
            depth = 1
            i = start + len(marker)
            while i < len(value) and depth:
                if value[i] == "{" and (i == 0 or value[i - 1] != "\\"):
                    depth += 1
                elif value[i] == "}" and value[i - 1] != "\\":
                    depth -= 1
                i += 1
            if depth:
                die(f"unbalanced {marker} inside math")
            # Use a marker that cannot be rediscovered by this loop.
            value = value[:start] + "\\maskedtext{#}" + value[i:]
    return re.sub(r"\s+", "", value)


def math_surfaces(text: str) -> list[str]:
    text = active_text(text)
    spans: list[tuple[int, int, str]] = []
    patterns = (
        r"\$\$(.+?)\$\$",
        r"(?<!\\)(?<!\$)\$(?!\$)(.+?)(?<!\\)\$(?!\$)",
        r"\\\[(.+?)\\\]",
        r"\\begin\{(?:align\*?|alignat\*?|gather\*?|multline\*?)\}(.+?)\\end\{(?:align\*?|alignat\*?|gather\*?|multline\*?)\}",
    )
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.DOTALL):
            spans.append((match.start(), match.end(), mask_text_commands(match.group(1))))
    spans.sort()
    return [value for _, _, value in spans]


def compare_file(name: str) -> dict[str, object]:
    source_path = AUTHORITY / name
    target_path = TARGET / name
    source = source_path.read_text(encoding="utf-8")
    target = target_path.read_text(encoding="utf-8")

    # The queued Chapter 2+ suffix is compared byte-for-byte below.  Restrict
    # regex work to the translated prefix so this check stays bounded and does
    # not repeatedly parse the remaining 90 KB backmatter.
    checked_source = source
    checked_target = target
    if name == "hints.tex":
        boundary = "%\\subsection*{Chapter~\\ref{chap:axioms}}"
        if boundary not in source or boundary not in target:
            die("hints.tex: Chapter 2 boundary missing")
        source_boundary = source.index(boundary)
        target_boundary = target.index(boundary)
        if source[source_boundary:] != target[target_boundary:]:
            die("hints.tex: queued Chapter 2+ suffix changed")
        checked_source = source[:source_boundary]
        checked_target = target[:target_boundary]

    checks = {
        "environments": r"\\(begin|end)\{([^}]+)\}",
        "labels": r"\\label\{([^}]+)\}",
        "refs": r"\\(?:ref|pageref|eqref)\{([^}]+)\}",
        "citations": r"\\cite\{([^}]+)\}",
        "graphics": r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}",
    }
    for label, pattern in checks.items():
        before = ordered(pattern, checked_source)
        after = ordered(pattern, checked_target)
        if before != after:
            die(f"{name}: ordered {label} changed")

    before_math = math_surfaces(checked_source)
    after_math = math_surfaces(checked_target)
    if before_math != after_math:
        for index, (left, right) in enumerate(zip(before_math, after_math), start=1):
            if left != right:
                die(f"{name}: protected math surface {index} changed")
        die(f"{name}: protected math surface count changed")

    return {
        "path": name,
        "source_bytes": source_path.stat().st_size,
        "source_sha256": sha256(source_path),
        "target_bytes": target_path.stat().st_size,
        "target_sha256": sha256(target_path),
        "environments": len(ordered(checks["environments"], checked_source)),
        "labels": len(ordered(checks["labels"], checked_source)),
        "refs": len(ordered(checks["refs"], checked_source)),
        "citations": len(ordered(checks["citations"], checked_source)),
        "graphics": len(ordered(checks["graphics"], checked_source)),
        "math_surfaces": len(before_math),
    }


def main() -> None:
    for path in (AUTHORITY, TARGET):
        if not path.is_dir():
            die(f"missing directory {path}")
    if (TARGET / "cover").exists():
        die("excluded cover directory present in target")
    public_bytes = b"\n".join(path.read_bytes() for path in TARGET.rglob("*") if path.is_file())
    for forbidden in (b"P22-Underground-Reg.ttf", b"P22UndergroundCYBookSC.ttf"):
        if forbidden in public_bytes:
            die(f"excluded font name present: {forbidden.decode()}")

    report = {
        "schema": "o004-first-unit-qa-v0",
        "status": "pass",
        "files": [compare_file(name) for name in FILES],
    }
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
