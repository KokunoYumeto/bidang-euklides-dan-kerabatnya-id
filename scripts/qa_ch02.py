#!/usr/bin/env python3
"""Fail-closed structural QA for O004 Chapter 2 and its hint slice."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
AUTHORITY = (
    LANE
    / "source"
    / "upstream"
    / "birkhoff-0b0858e1e985f4c8dadbb6075ae9e095cd4a8981"
)
TARGET = LANE / "source" / "id-ID"
CH2_HINT_MARKER = "%\\subsection*{Chapter~\\ref{chap:axioms}}"
CH3_HINT_MARKER = "%\\subsection*{Chapter~\\ref{chap:half-planes}}"
CH4_HINT_MARKER = "%\\subsection*{Chapter~\\ref{chap:cong}}"
FROZEN_TARGET_PREFIX_SHA256 = (
    "659167c454ee2ee734a6222fa065b860ed53348eb3a74744a567fba802a1d486"
)
FROZEN_TARGET_CH3_SHA256 = (
    "d5f75149bd2fdbc993d00c0a8d4c8c659846374c9da60d459be0871bbe6f40d4"
)


def die(message: str) -> None:
    raise SystemExit(f"QA_FAIL: {message}")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def active_text(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        out: list[str] = []
        for index, char in enumerate(line):
            if char == "%" and (index == 0 or line[index - 1] != "\\"):
                break
            out.append(char)
        lines.append("".join(out))
    return "\n".join(lines)


def ordered(pattern: str, text: str) -> list[object]:
    return re.findall(pattern, active_text(text), flags=re.DOTALL)


def ordered_raw(pattern: str, text: str) -> list[object]:
    return re.findall(pattern, text, flags=re.DOTALL)


def mask_translatable_math_text(value: str) -> str:
    commands = ("text", "textit", "textrm", "textbf", "intertext", "shortintertext")
    for command in commands:
        marker = "\\" + command + "{"
        while marker in value:
            start = value.index(marker)
            depth = 1
            index = start + len(marker)
            while index < len(value) and depth:
                if value[index] == "{" and (index == 0 or value[index - 1] != "\\"):
                    depth += 1
                elif value[index] == "}" and value[index - 1] != "\\":
                    depth -= 1
                index += 1
            if depth:
                die(f"unbalanced {marker} inside math")
            value = value[:start] + "\\maskedtext{#}" + value[index:]
    return re.sub(r"\s+", "", value)


def math_surfaces(text: str, *, include_comments: bool = False) -> list[str]:
    checked = text if include_comments else active_text(text)
    spans: list[tuple[int, int, str]] = []
    patterns = (
        r"\$\$(.+?)\$\$",
        r"(?<!\\)(?<!\$)\$(?!\$)(.+?)(?<!\\)\$(?!\$)",
        r"\\\[(.+?)\\\]",
        r"\\begin\{(?:align\*?|alignat\*?|gather\*?|multline\*?)\}"
        r"(.+?)\\end\{(?:align\*?|alignat\*?|gather\*?|multline\*?)\}",
    )
    for pattern in patterns:
        for match in re.finditer(pattern, checked, flags=re.DOTALL):
            spans.append(
                (match.start(), match.end(), mask_translatable_math_text(match.group(1)))
            )
    spans.sort()
    return [value for _, _, value in spans]


def require_same(name: str, pattern: str, source: str, target: str) -> int:
    before = ordered(pattern, source)
    after = ordered(pattern, target)
    if before != after:
        die(f"{name} changed")
    return len(before)


def require_same_raw(name: str, pattern: str, source: str, target: str) -> int:
    before = ordered_raw(pattern, source)
    after = ordered_raw(pattern, target)
    if before != after:
        die(f"{name} changed")
    return len(before)


def slice_between(data: bytes, start: bytes, end: bytes) -> tuple[bytes, bytes, bytes]:
    try:
        left = data.index(start)
        right = data.index(end, left + len(start))
    except ValueError as error:
        die(f"hint boundary missing: {error}")
    return data[:left], data[left:right], data[right:]


def main() -> None:
    source_axioms_path = AUTHORITY / "axioms.tex"
    target_axioms_path = TARGET / "axioms.tex"
    source_hints_path = AUTHORITY / "hints.tex"
    target_hints_path = TARGET / "hints.tex"
    for path in (source_axioms_path, target_axioms_path, source_hints_path, target_hints_path):
        if not path.is_file():
            die(f"missing file {path}")

    source_axioms = source_axioms_path.read_text(encoding="utf-8")
    target_axioms = target_axioms_path.read_text(encoding="utf-8")
    topology = {
        "environments": require_same(
            "ordered environments", r"\\(begin|end)\{([^}]+)\}", source_axioms, target_axioms
        ),
        "labels": require_same(
            "ordered labels", r"\\label\{([^}]+)\}", source_axioms, target_axioms
        ),
        "references": require_same(
            "ordered references",
            r"\\(?:ref|pageref|eqref)\{([^}]+)\}",
            source_axioms,
            target_axioms,
        ),
        "citations": require_same(
            "ordered citations", r"\\cite\{([^}]+)\}", source_axioms, target_axioms
        ),
        "graphics": require_same(
            "ordered graphics",
            r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}",
            source_axioms,
            target_axioms,
        ),
        "theorem_options": require_same(
            "ordered theorem optional arguments",
            r"\\begin\{thm\}(?:\[([^\]]*)\])?",
            source_axioms,
            target_axioms,
        ),
        "parit": require_same("ordered parit commands", r"\\parit", source_axioms, target_axioms),
        "qeds": require_same("ordered qeds commands", r"\\qeds", source_axioms, target_axioms),
    }
    expected = {
        "environments": 56,
        "labels": 25,
        "references": 27,
        "citations": 4,
        "graphics": 5,
        "theorem_options": 15,
        "parit": 9,
        "qeds": 7,
    }
    if topology != expected:
        die(f"unexpected authority topology: {topology!r}")

    source_math = math_surfaces(source_axioms)
    target_math = math_surfaces(target_axioms)
    if source_math != target_math:
        for index, (before, after) in enumerate(zip(source_math, target_math), start=1):
            if before != after:
                die(f"protected axioms.tex math surface {index} changed")
        die("protected axioms.tex math surface count changed")

    source_hint_bytes = source_hints_path.read_bytes()
    target_hint_bytes = target_hints_path.read_bytes()
    source_prefix, source_ch2, source_suffix = slice_between(
        source_hint_bytes, CH2_HINT_MARKER.encode(), CH3_HINT_MARKER.encode()
    )
    target_prefix, target_ch2, target_suffix = slice_between(
        target_hint_bytes, CH2_HINT_MARKER.encode(), CH3_HINT_MARKER.encode()
    )
    if digest(target_prefix) != FROZEN_TARGET_PREFIX_SHA256:
        die("frozen translated Chapter 1 hint prefix changed")
    _, source_ch3, source_ch4plus = slice_between(
        source_hint_bytes, CH3_HINT_MARKER.encode(), CH4_HINT_MARKER.encode()
    )
    _, target_ch3, target_ch4plus = slice_between(
        target_hint_bytes, CH3_HINT_MARKER.encode(), CH4_HINT_MARKER.encode()
    )
    if digest(target_ch3) != FROZEN_TARGET_CH3_SHA256:
        die("admitted translated Chapter 3 hint slice changed")
    # Later chapter slices are admitted by their own fail-closed QA scripts.
    # Chapter 2 must not reject legitimate source-order progress after Chapter 3.

    source_ch2_text = source_ch2.decode("utf-8")
    target_ch2_text = target_ch2.decode("utf-8")
    hint_topology = {
        "commands_raw": require_same_raw(
            "ordered raw Chapter 2 hint commands",
            r"\\[A-Za-z@]+",
            source_ch2_text,
            target_ch2_text,
        ),
        "references_raw": require_same_raw(
            "ordered raw Chapter 2 hint references",
            r"\\(?:ref|pageref|eqref)\{([^}]+)\}",
            source_ch2_text,
            target_ch2_text,
        ),
        "commands_active": require_same(
            "ordered active Chapter 2 hint commands",
            r"\\[A-Za-z@]+",
            source_ch2_text,
            target_ch2_text,
        ),
        "references_active": require_same(
            "ordered active Chapter 2 hint references",
            r"\\(?:ref|pageref|eqref)\{([^}]+)\}",
            source_ch2_text,
            target_ch2_text,
        ),
    }
    source_hint_math = math_surfaces(source_ch2_text)
    target_hint_math = math_surfaces(target_ch2_text)
    if source_hint_math != target_hint_math:
        die("protected Chapter 2 hint math surfaces changed")
    source_hint_math_raw = math_surfaces(source_ch2_text, include_comments=True)
    target_hint_math_raw = math_surfaces(target_ch2_text, include_comments=True)
    if source_hint_math_raw != target_hint_math_raw:
        die("protected raw Chapter 2 hint math surfaces changed")
    if hint_topology != {
        "commands_raw": 69,
        "references_raw": 30,
        "commands_active": 60,
        "references_active": 26,
    }:
        die(f"unexpected Chapter 2 hint topology: {hint_topology!r}")
    if len(source_hint_math) != 15:
        die(f"unexpected Chapter 2 hint math count: {len(source_hint_math)}")
    if len(source_hint_math_raw) != 16:
        die(f"unexpected raw Chapter 2 hint math count: {len(source_hint_math_raw)}")

    report = {
        "schema": "o004-ch02-qa-v0",
        "status": "pass",
        "authority": {
            "axioms_bytes": source_axioms_path.stat().st_size,
            "axioms_sha256": digest(source_axioms_path.read_bytes()),
            "hint_slice_bytes": len(source_ch2),
            "hint_slice_sha256": digest(source_ch2),
        },
        "target": {
            "axioms_bytes": target_axioms_path.stat().st_size,
            "axioms_sha256": digest(target_axioms_path.read_bytes()),
            "hint_slice_bytes": len(target_ch2),
            "hint_slice_sha256": digest(target_ch2),
            "whole_hints_sha256": digest(target_hint_bytes),
            "frozen_prefix_sha256": digest(target_prefix),
            "admitted_ch3_sha256": digest(target_ch3),
            "current_ch4plus_sha256": digest(target_ch4plus),
        },
        "axioms_topology": topology,
        "axioms_math_surfaces": len(source_math),
        "hint_topology": hint_topology,
        "hint_math_surfaces_active": len(source_hint_math),
        "hint_math_surfaces_raw": len(source_hint_math_raw),
    }
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
