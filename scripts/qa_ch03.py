#!/usr/bin/env python3
"""Fail-closed structural QA for O004 Chapter 3 and its exact hint slice."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
AUTHORITY = LANE / "source" / "upstream" / "birkhoff-0b0858e1e985f4c8dadbb6075ae9e095cd4a8981"
TARGET = LANE / "source" / "id-ID"
CH3_MARKER = b"%\\subsection*{Chapter~\\ref{chap:half-planes}}"
CH4_MARKER = b"%\\subsection*{Chapter~\\ref{chap:cong}}"
FROZEN_TARGET_PREFIX_SHA256 = "07d7b54f88389a171e2487c77184b6b0755a136dd4902fa41fa6aa0e031876fb"
FROZEN_TARGET_SLICE_SHA256 = "d5f75149bd2fdbc993d00c0a8d4c8c659846374c9da60d459be0871bbe6f40d4"


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


def require_same(name: str, pattern: str, source: str, target: str, *, raw: bool = False) -> int:
    finder = ordered_raw if raw else ordered
    before = finder(pattern, source)
    after = finder(pattern, target)
    if before != after:
        die(f"{name} changed")
    return len(before)


def mask_math_text(value: str) -> str:
    for command in ("text", "textit", "textrm", "textbf", "intertext", "shortintertext"):
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
        r"\\begin\{(?:align\*?|alignat\*?|gather\*?|multline\*?)\}(.+?)\\end\{(?:align\*?|alignat\*?|gather\*?|multline\*?)\}",
    )
    for pattern in patterns:
        for match in re.finditer(pattern, checked, flags=re.DOTALL):
            spans.append((match.start(), match.end(), mask_math_text(match.group(1))))
    spans.sort()
    return [value for _, _, value in spans]


def split_slice(data: bytes) -> tuple[bytes, bytes, bytes]:
    try:
        left = data.index(CH3_MARKER)
        right = data.index(CH4_MARKER, left + len(CH3_MARKER))
    except ValueError as error:
        die(f"hint boundary missing: {error}")
    return data[:left], data[left:right], data[right:]


def main() -> None:
    source_chapter_path = AUTHORITY / "half-planes.tex"
    target_chapter_path = TARGET / "half-planes.tex"
    source_hints_path = AUTHORITY / "hints.tex"
    target_hints_path = TARGET / "hints.tex"
    for path in (source_chapter_path, target_chapter_path, source_hints_path, target_hints_path):
        if not path.is_file():
            die(f"missing file {path}")

    source = source_chapter_path.read_text(encoding="utf-8")
    target = target_chapter_path.read_text(encoding="utf-8")
    topology = {
        "environments": require_same("ordered environments", r"\\(begin|end)\{([^}]+)\}", source, target),
        "labels": require_same("ordered labels", r"\\label\{([^}]+)\}", source, target),
        "equation_labels": require_same("ordered equation labels", r"\\eqlbl\{([^}]+)\}", source, target),
        "references": require_same("ordered references", r"\\(?:ref|pageref|eqref)\{([^}]+)\}", source, target),
        "citations": require_same("ordered citations", r"\\cite\{([^}]+)\}", source, target),
        "graphics": require_same("ordered graphics", r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", source, target),
        "theorem_options": require_same("ordered theorem options", r"\\begin\{thm\}(?:\[([^\]]*)\])?", source, target),
        "qeds": require_same("ordered proof closures", r"\\qedsf?", source, target),
    }
    expected = {
        "environments": 82,
        "labels": 25,
        "equation_labels": 1,
        "references": 38,
        "citations": 0,
        "graphics": 13,
        "theorem_options": 21,
        "qeds": 10,
    }
    if topology != expected:
        die(f"unexpected authority topology: {topology!r}")

    scalar_counts = {
        "sections": len(ordered(r"\\section\{", source)),
        "index_entries": len(ordered(r"\\index\{", source)),
        "absolute_markers": len(ordered(r"\\begin\{thm\}\[\\abs\]", source)),
        "used_later_markers": len(ordered(r"\\begin\{thm\}\[!\]", source)),
    }
    if scalar_counts != {"sections": 5, "index_entries": 7, "absolute_markers": 9, "used_later_markers": 4}:
        die(f"unexpected authority scalar counts: {scalar_counts!r}")
    if len(ordered(r"\\section\{", target)) != 5 or len(ordered(r"\\index\{", target)) != 7:
        die("translated section or index-entry count changed")

    source_math = math_surfaces(source)
    target_math = math_surfaces(target)
    if source_math != target_math:
        for index, pair in enumerate(zip(source_math, target_math), start=1):
            if pair[0] != pair[1]:
                die(f"protected chapter math surface {index} changed")
        die("protected chapter math-surface count changed")

    source_hint_bytes = source_hints_path.read_bytes()
    target_hint_bytes = target_hints_path.read_bytes()
    _, source_slice, _ = split_slice(source_hint_bytes)
    target_prefix, target_slice, target_suffix = split_slice(target_hint_bytes)
    if digest(target_prefix) != FROZEN_TARGET_PREFIX_SHA256:
        die("frozen translated Chapter 1-2 hint prefix changed")
    if digest(target_slice) != FROZEN_TARGET_SLICE_SHA256:
        die("admitted translated Chapter 3 hint slice changed")

    source_hint = source_slice.decode("utf-8")
    target_hint = target_slice.decode("utf-8")
    hint_topology = {
        "commands_raw": require_same("ordered raw hint commands", r"\\[A-Za-z@]+", source_hint, target_hint, raw=True),
        "references_raw": require_same("ordered raw hint references", r"\\(?:ref|pageref|eqref)\{([^}]+)\}", source_hint, target_hint, raw=True),
        "comments": require_same("ordered hint comments", r"(?m)^%[^\r\n]*$", source_hint, target_hint, raw=True),
    }
    source_hint_math = math_surfaces(source_hint, include_comments=True)
    target_hint_math = math_surfaces(target_hint, include_comments=True)
    if source_hint_math != target_hint_math:
        die("protected raw Chapter 3 hint math surfaces changed")
    if hint_topology != {"commands_raw": 102, "references_raw": 21, "comments": 1}:
        die(f"unexpected hint topology: {hint_topology!r}")
    if len(source_hint_math) != 65:
        die(f"unexpected hint math-surface count: {len(source_hint_math)}")

    report = {
        "schema": "o004-ch03-qa-v0",
        "status": "pass",
        "authority": {
            "chapter_bytes": source_chapter_path.stat().st_size,
            "chapter_sha256": digest(source_chapter_path.read_bytes()),
            "hint_slice_bytes": len(source_slice),
            "hint_slice_sha256": digest(source_slice),
        },
        "target": {
            "chapter_bytes": target_chapter_path.stat().st_size,
            "chapter_sha256": digest(target_chapter_path.read_bytes()),
            "hint_slice_bytes": len(target_slice),
            "hint_slice_sha256": digest(target_slice),
            "whole_hints_sha256": digest(target_hint_bytes),
            "frozen_prefix_sha256": digest(target_prefix),
            "current_later_suffix_sha256": digest(target_suffix),
        },
        "chapter_topology": topology,
        "scalar_counts": scalar_counts,
        "chapter_math_surfaces": len(source_math),
        "hint_topology": hint_topology,
        "hint_math_surfaces_raw": len(source_hint_math),
    }
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
