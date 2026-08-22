#!/usr/bin/env python3
"""Fail-closed structural QA for O004 Chapter 6 and its exact hint slice."""

from __future__ import annotations

import hashlib
import json
import re
import runpy
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
CH6_MARKER = b"%\\subsection*{Chapter~\\ref{chap:parallel}}"
CH7_MARKER = b"%\\subsection*{Chapter~\\ref{chap:angle-sum}}"
FROZEN_TARGET_PREFIX_SHA256 = (
    "f2d9f4153457a500482d1f480c07a18d62d2ac2440138f9cf927f93ae1c522b0"
)
FROZEN_TARGET_CHAPTER_SHA256 = (
    "23c609c66ae26e627425bfd196454b4cdc7a7b11d8398265786c9234ddcdd201"
)
FROZEN_TARGET_HINT_SLICE_SHA256 = (
    "38cdafe5f4fcbb7440d4ac9cfdb1bb6c1b0925d37de24dc0996da61de0e82273"
)

_shared = runpy.run_path(str(Path(__file__).with_name("qa_ch05.py")))
active_text = _shared["active_text"]
ordered = _shared["ordered"]
ordered_raw = _shared["ordered_raw"]
require_same = _shared["require_same"]
math_surfaces = _shared["math_surfaces"]
require_utf8_lf = _shared["require_utf8_lf"]
prose_tokens = _shared["prose_tokens"]

ALLOWED_SHARED_SOURCE_WORDS = frozenset(
    {"birkhoff", "data", "diameter", "elements", "lemma", "sas", "sss"}
)
ENGLISH_RESIDUE_WORDS = _shared["ENGLISH_RESIDUE_WORDS"] - {"lemma"}


def die(message: str) -> None:
    raise SystemExit(f"QA_FAIL: {message}")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def split_slice(data: bytes) -> tuple[bytes, bytes, bytes]:
    if data.count(CH6_MARKER) != 1 or data.count(CH7_MARKER) != 1:
        die("Chapter 6 or Chapter 7 hint marker is not unique")
    left = data.index(CH6_MARKER)
    right = data.index(CH7_MARKER, left + len(CH6_MARKER))
    return data[:left], data[left:right], data[right:]


def require_no_active_english(name: str, text: str) -> list[str]:
    hits = sorted(
        {
            token.lower()
            for token in prose_tokens(text)
            if token.lower() in ENGLISH_RESIDUE_WORDS
        }
    )
    if hits:
        die(f"active English prose detected in {name}: {hits}")
    return hits


def require_no_untranslated_source_overlap(
    name: str, source: str, target: str
) -> list[str]:
    source_words = {token.lower() for token in prose_tokens(source) if len(token) >= 4}
    target_words = {token.lower() for token in prose_tokens(target) if len(token) >= 4}
    hits = sorted((source_words & target_words) - ALLOWED_SHARED_SOURCE_WORDS)
    if hits:
        die(f"untranslated source-language overlap detected in {name}: {hits}")
    return hits


def topology(source: str, target: str, *, raw: bool = False) -> dict[str, int]:
    suffix = "raw " if raw else ""
    return {
        "environments": require_same(
            f"ordered {suffix}environments",
            r"\\(begin|end)\{([^}]+)\}",
            source,
            target,
            raw=raw,
        ),
        "labels": require_same(
            f"ordered {suffix}labels",
            r"\\label\{([^}]+)\}",
            source,
            target,
            raw=raw,
        ),
        "equation_labels": require_same(
            f"ordered {suffix}equation labels",
            r"\\eqlbl\{([^}]+)\}",
            source,
            target,
            raw=raw,
        ),
        "references": require_same(
            f"ordered {suffix}references",
            r"\\(?:ref|pageref|eqref)\{([^}]+)\}",
            source,
            target,
            raw=raw,
        ),
        "citations": require_same(
            f"ordered {suffix}citations",
            r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}",
            source,
            target,
            raw=raw,
        ),
        "graphics": require_same(
            f"ordered {suffix}graphics",
            r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}",
            source,
            target,
            raw=raw,
        ),
        "theorem_options": require_same(
            f"ordered {suffix}theorem options",
            r"\\begin\{thm\}(?:\[([^\]]*)\])?",
            source,
            target,
            raw=raw,
        ),
        "qeds": require_same(
            f"ordered {suffix}proof closures",
            r"\\qedsf?",
            source,
            target,
            raw=raw,
        ),
    }


def main() -> None:
    source_chapter_path = AUTHORITY / "similar.tex"
    target_chapter_path = TARGET / "similar.tex"
    source_hints_path = AUTHORITY / "hints.tex"
    target_hints_path = TARGET / "hints.tex"
    for path in (
        source_chapter_path,
        target_chapter_path,
        source_hints_path,
        target_hints_path,
    ):
        if not path.is_file():
            die(f"missing file {path}")

    source_chapter_bytes = source_chapter_path.read_bytes()
    target_chapter_bytes = target_chapter_path.read_bytes()
    source = source_chapter_bytes.decode("utf-8", errors="strict")
    target = require_utf8_lf("target similar.tex", target_chapter_bytes)
    if digest(target_chapter_bytes) != FROZEN_TARGET_CHAPTER_SHA256:
        die("translated Chapter 6 body changed")

    chapter_topology = topology(source, target)
    expected_topology = {
        "environments": 44,
        "labels": 12,
        "equation_labels": 4,
        "references": 17,
        "citations": 2,
        "graphics": 4,
        "theorem_options": 12,
        "qeds": 3,
    }
    if chapter_topology != expected_topology:
        die(f"unexpected authority topology: {chapter_topology!r}")

    chapter_raw_topology = topology(source, target, raw=True)
    chapter_raw_topology.update(
        {
            "authority_commands": len(ordered_raw(r"\\[A-Za-z@]+", source)),
            "target_commands": len(ordered_raw(r"\\[A-Za-z@]+", target)),
            "authority_comments": len(ordered_raw(r"(?m)^%[^\r\n]*$", source)),
            "target_comments": len(ordered_raw(r"(?m)^%[^\r\n]*$", target)),
        }
    )
    expected_raw_topology = {
        **expected_topology,
        "environments": 46,
        "labels": 13,
        "theorem_options": 13,
        "authority_commands": 348,
        "target_commands": 348,
        "authority_comments": 5,
        "target_comments": 5,
    }
    if chapter_raw_topology != expected_raw_topology:
        die(f"unexpected raw chapter topology: {chapter_raw_topology!r}")

    scalar_counts = {
        "sections": len(ordered(r"\\section(?:\[[^\]]*\])?\{", source)),
        "index_entries": len(ordered(r"\\index\{", source)),
        "absolute_markers": len(ordered(r"\\begin\{thm\}\[\\abs\]", source)),
        "used_later_markers": len(ordered(r"\\begin\{thm\}\[!\]", source)),
    }
    expected_scalars = {
        "sections": 4,
        "index_entries": 20,
        "absolute_markers": 0,
        "used_later_markers": 0,
    }
    if scalar_counts != expected_scalars:
        die(f"unexpected authority scalar counts: {scalar_counts!r}")
    if len(ordered(r"\\section(?:\[[^\]]*\])?\{", target)) != 4:
        die("translated section count changed")
    if len(ordered(r"\\index\{", target)) != 20:
        die("translated index-entry count changed")

    source_math = math_surfaces(source)
    target_math = math_surfaces(target)
    if source_math != target_math or len(source_math) != 143:
        die("protected active Chapter 6 math surfaces changed")
    source_raw_math = math_surfaces(source, include_comments=True)
    target_raw_math = math_surfaces(target, include_comments=True)
    if source_raw_math != target_raw_math or len(source_raw_math) != 156:
        die("protected raw Chapter 6 math surfaces changed")

    source_chapter_identity = (
        r"\chapter[Similar triangles]{Similar triangles}\label{chap:parallel}"
    )
    target_chapter_identity = (
        r"\chapter[Segitiga sebangun]{Segitiga sebangun}\label{chap:parallel}"
    )
    if source.count(source_chapter_identity) != 1 or target.count(target_chapter_identity) != 1:
        die("legacy chap:parallel identity is missing or duplicated")
    if source.count(r"\label{ex:k*triangle}") != 1 or target.count(
        r"\label{ex:k*triangle}"
    ) != 1:
        die("ex:k*triangle identity changed")

    source_clarification = (
        "since adding $\\measuredangle BAX$ or $\\measuredangle CAD$ "
        "to the corresponding sides"
    )
    target_clarification = (
        "jika $\\measuredangle BAX$ ditambahkan pada ruas kiri dan "
        "$\\measuredangle CAD$ pada ruas kanan"
    )
    if source.count(source_clarification) != 1 or target.count(target_clarification) != 1:
        die("named Ptolemy-side wording clarification is missing or duplicated")

    source_hint_bytes = source_hints_path.read_bytes()
    target_hint_bytes = target_hints_path.read_bytes()
    _, source_slice, source_suffix = split_slice(source_hint_bytes)
    target_prefix, target_slice, target_suffix = split_slice(target_hint_bytes)
    source_hint = source_slice.decode("utf-8", errors="strict")
    target_hint = require_utf8_lf("target Chapter 6 hint slice", target_slice)
    if digest(target_prefix) != FROZEN_TARGET_PREFIX_SHA256:
        die("frozen translated Chapter 1-5 hint prefix changed")
    if digest(target_slice) != FROZEN_TARGET_HINT_SLICE_SHA256:
        die("translated Chapter 6 hint slice changed")

    hint_topology = topology(source_hint, target_hint)
    expected_hint_topology = {
        "environments": 0,
        "labels": 0,
        "equation_labels": 0,
        "references": 10,
        "citations": 0,
        "graphics": 0,
        "theorem_options": 0,
        "qeds": 0,
    }
    if hint_topology != expected_hint_topology:
        die(f"unexpected hint topology: {hint_topology!r}")

    hint_raw_topology = topology(source_hint, target_hint, raw=True)
    hint_raw_topology.update(
        {
            "commands": require_same(
                "ordered raw hint commands",
                r"\\[A-Za-z@]+",
                source_hint,
                target_hint,
                raw=True,
            ),
            "comments": require_same(
                "ordered raw hint comments",
                r"(?m)^%[^\r\n]*$",
                source_hint,
                target_hint,
                raw=True,
            ),
        }
    )
    expected_hint_raw_topology = {
        **expected_hint_topology,
        "references": 12,
        "commands": 88,
        "comments": 2,
    }
    if hint_raw_topology != expected_hint_raw_topology:
        die(f"unexpected raw hint topology: {hint_raw_topology!r}")

    source_hint_math = math_surfaces(source_hint)
    target_hint_math = math_surfaces(target_hint)
    if source_hint_math != target_hint_math or len(source_hint_math) != 22:
        die("protected active Chapter 6 hint math surfaces changed")
    source_hint_raw_math = math_surfaces(source_hint, include_comments=True)
    target_hint_raw_math = math_surfaces(target_hint, include_comments=True)
    if source_hint_raw_math != target_hint_raw_math or len(source_hint_raw_math) != 23:
        die("protected raw Chapter 6 hint math surfaces changed")

    exercise_pattern = (
        r"\\begin\{thm\}(?:\[[^\]]*\])?\{[^}]+\}"
        r"\\label\{(ex:[^}]+)\}"
    )
    source_exercises = ordered(exercise_pattern, source)
    target_exercises = ordered(exercise_pattern, target)
    hint_header_pattern = r"\\parbf\{\\ref\{([^}]+)\}(?:\+\\ref\{([^}]+)\})?"
    source_hint_headers = ordered(hint_header_pattern, source_hint)
    target_hint_headers = ordered(hint_header_pattern, target_hint)
    flattened_hint_ids = [item for pair in target_hint_headers for item in pair if item]
    if source_exercises != target_exercises or source_hint_headers != target_hint_headers:
        die("ordered Chapter 6 exercise or hint-header identity changed")
    if len(target_exercises) != 8 or len(target_hint_headers) != 8:
        die("unexpected Chapter 6 exercise or hint-block count")
    if flattened_hint_ids != target_exercises:
        die("Chapter 6 exercise-to-hint closure is incomplete or out of order")

    body_english_hits = require_no_active_english("target similar.tex", target)
    hint_english_hits = require_no_active_english("target Chapter 6 hints", target_hint)
    body_source_overlap = require_no_untranslated_source_overlap(
        "target similar.tex", source, target
    )
    hint_source_overlap = require_no_untranslated_source_overlap(
        "target Chapter 6 hints", source_hint, target_hint
    )

    report = {
        "schema": "o004-ch06-qa-v0",
        "status": "pass",
        "authority": {
            "chapter_bytes": len(source_chapter_bytes),
            "chapter_sha256": digest(source_chapter_bytes),
            "hint_slice_bytes": len(source_slice),
            "hint_slice_sha256": digest(source_slice),
            "later_suffix_bytes": len(source_suffix),
            "later_suffix_sha256": digest(source_suffix),
        },
        "target": {
            "chapter_bytes": len(target_chapter_bytes),
            "chapter_sha256": digest(target_chapter_bytes),
            "hint_slice_bytes": len(target_slice),
            "hint_slice_sha256": digest(target_slice),
            "whole_hints_sha256": digest(target_hint_bytes),
            "frozen_prefix_bytes": len(target_prefix),
            "frozen_prefix_sha256": digest(target_prefix),
            "current_later_suffix_bytes": len(target_suffix),
            "current_later_suffix_sha256": digest(target_suffix),
            "current_later_suffix_matches_authority": target_suffix == source_suffix,
            "utf8_lf_no_bom_terminal_lf": True,
            "trailing_whitespace_lines": [],
            "active_english_prose_hits": {
                "chapter": body_english_hits,
                "hints": hint_english_hits,
            },
            "untranslated_source_language_overlap": {
                "chapter": body_source_overlap,
                "hints": hint_source_overlap,
            },
        },
        "chapter_topology": chapter_topology,
        "chapter_raw_topology": chapter_raw_topology,
        "scalar_counts": scalar_counts,
        "chapter_math_surfaces": {
            "active": len(source_math),
            "raw": len(source_raw_math),
        },
        "exercise_hint_closure": {
            "exercise_count": len(target_exercises),
            "hint_block_count": len(target_hint_headers),
            "covered_exercise_count": len(flattened_hint_ids),
            "ordered_exercise_ids": target_exercises,
            "complete": True,
        },
        "hint_topology": hint_topology,
        "hint_raw_topology": hint_raw_topology,
        "hint_math_surfaces": {
            "active": len(source_hint_math),
            "raw": len(source_hint_raw_math),
        },
        "named_source_notes": [
            {
                "id": "o004.petrunin.correction.ch06.legacy-chapter-label",
                "description": "The Similar triangles chapter retains the legacy label chap:parallel.",
                "source_changed": False,
            },
            {
                "id": "o004.petrunin.correction.ch06.k-one-distinctness",
                "description": "Exercise ex:k*triangle requires distinct points but permits k=1, which forces each primed point to equal its unprimed counterpart.",
                "source_changed": False,
            },
            {
                "id": "o004.petrunin.correction.ch06.inactive-triange-typos",
                "description": "The commented-out footpoint exercise and hint retain inherited triange typos and English prose as inactive source surfaces.",
                "source_changed": False,
            },
        ],
        "named_localization_clarification": {
            "id": "o004.petrunin.correction.ch06.ptolemy-corresponding-sides",
            "description": "The Indonesian proof explicitly names the left and right sides to which the equal angles are added.",
            "mathematics_changed": False,
        },
    }
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
