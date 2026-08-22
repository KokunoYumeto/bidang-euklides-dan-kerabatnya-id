#!/usr/bin/env python3
"""Fail-closed structural QA for O004 Chapter 8 and its exact hint slice."""

from __future__ import annotations

import difflib
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
CH8_MARKER = b"%\\subsection*{Chapter~\\ref{chap:triangle}}"
CH9_MARKER = b"%\\subsection*{Chapter~\\ref{chap:inscribed-angle}}"
FROZEN_AUTHORITY_CHAPTER_SHA256 = (
    "95e4d8050e38af8da76ed24c48277550bfe7cdf8c1a7274887d6f853e4429948"
)
FROZEN_AUTHORITY_HINT_SLICE_SHA256 = (
    "9094d0267cd658585f398bf029934f4a3af9eec2069ecfd18451fa5a3fc2ad8d"
)
FROZEN_AUTHORITY_SUFFIX_SHA256 = (
    "2ea9859cf7143c6f56069ad802df4c1e295839f8729408a0f72ee8884e205afd"
)
FROZEN_TARGET_PREFIX_SHA256 = (
    "46c00e637aa948158b9e3ac7a5b38379bb367ec9c90f2c560d010f151c3b814c"
)
FROZEN_TARGET_CHAPTER_SHA256 = (
    "b599ee9baded53dc0c81fe6e0bb6539e5e43e5173d1ba525df5e8885a024f8b6"
)
FROZEN_TARGET_HINT_SLICE_SHA256 = (
    "8cba27ea4b834ce686c95e6601044a4f792daae4400094da3e6bcec1fd289187"
)
FROZEN_TARGET_WHOLE_HINTS_SHA256 = (
    "fab63adad2acc5dacd44b51724afd9297ffa3a64a9753ad9e5bd22732d899483"
)

_shared = runpy.run_path(str(Path(__file__).with_name("qa_ch05.py")))
ordered = _shared["ordered"]
ordered_raw = _shared["ordered_raw"]
require_same = _shared["require_same"]
math_surfaces = _shared["math_surfaces"]
prose_tokens = _shared["prose_tokens"]
ENGLISH_RESIDUE_WORDS = _shared["ENGLISH_RESIDUE_WORDS"]

ALLOWED_SHARED_SOURCE_WORDS = frozenset({"analog", "medial", "transversal"})


def die(message: str) -> None:
    raise SystemExit(f"QA_FAIL: {message}")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def split_hint_slice(
    data: bytes, *, name: str
) -> tuple[bytes, bytes, bytes]:
    if data.count(CH8_MARKER) != 1 or data.count(CH9_MARKER) != 1:
        die(f"{name}: Chapter 8 or Chapter 9 hint marker is not unique")
    left = data.index(CH8_MARKER)
    right = data.index(CH9_MARKER, left + len(CH8_MARKER))
    first_line = data[:left].count(b"\n") + 1
    next_marker_line = data[:right].count(b"\n") + 1
    if (first_line, next_marker_line) != (793, 872):
        die(
            f"{name}: Chapter 8 hint slice moved from lines 793-871 "
            f"to {first_line}-{next_marker_line - 1}"
        )
    return data[:left], data[left:right], data[right:]


def decode_utf8_lf(
    name: str, data: bytes, *, require_no_trailing: bool
) -> tuple[str, list[int]]:
    if data.startswith(b"\xef\xbb\xbf"):
        die(f"{name} has a UTF-8 BOM")
    if b"\r" in data:
        die(f"{name} is not LF-only")
    if not data.endswith(b"\n"):
        die(f"{name} lacks a terminal LF")
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        die(f"{name} is not valid UTF-8: {error}")
    trailing = [
        line_number
        for line_number, line in enumerate(text.splitlines(), start=1)
        if line.endswith((" ", "\t"))
    ]
    if require_no_trailing and trailing:
        die(f"{name} has trailing whitespace on lines {trailing}")
    return text, trailing


def require_comments_preserved(source: str, target: str, *, name: str) -> int:
    pattern = r"(?m)^%[^\r\n]*$"
    source_comments = ordered_raw(pattern, source)
    target_comments = ordered_raw(pattern, target)
    if source_comments != target_comments:
        die(f"{name} inactive comments changed")
    return len(source_comments)


def require_named_sequence_differences(
    name: str,
    source: list[str],
    target: list[str],
    expected: list[tuple[object, ...]],
) -> list[dict[str, object]]:
    matcher = difflib.SequenceMatcher(a=source, b=target, autojunk=False)
    actual = [
        (tag, i1, i2, j1, j2, source[i1:i2], target[j1:j2])
        for tag, i1, i2, j1, j2 in matcher.get_opcodes()
        if tag != "equal"
    ]
    if actual != expected:
        die(f"{name} changed beyond the named deviations: {actual!r}")
    return [
        {
            "operation": tag,
            "authority_range": [i1, i2],
            "target_range": [j1, j2],
            "authority_values": old,
            "target_values": new,
        }
        for tag, i1, i2, j1, j2, old, new in actual
    ]


def topology(source: str, target: str, *, raw: bool = False) -> dict[str, int]:
    suffix = "raw " if raw else "active "
    return {
        "commands": require_same(
            f"ordered {suffix}commands",
            r"\\[A-Za-z@]+",
            source,
            target,
            raw=raw,
        ),
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
    source_words = {
        token.lower() for token in prose_tokens(source) if len(token) >= 4
    }
    target_words = {
        token.lower() for token in prose_tokens(target) if len(token) >= 4
    }
    hits = sorted((source_words & target_words) - ALLOWED_SHARED_SOURCE_WORDS)
    if hits:
        die(f"untranslated source-language overlap detected in {name}: {hits}")
    return hits


def require_once(text: str, needle: str, *, name: str) -> None:
    if text.count(needle) != 1:
        die(f"{name} is missing or duplicated")


def main() -> None:
    source_chapter_path = AUTHORITY / "triangle.tex"
    target_chapter_path = TARGET / "triangle.tex"
    source_hints_path = AUTHORITY / "hints.tex"
    target_hints_path = TARGET / "hints.tex"
    external_exercise_path = AUTHORITY / "absolute.tex"
    for path in (
        source_chapter_path,
        target_chapter_path,
        source_hints_path,
        target_hints_path,
        external_exercise_path,
    ):
        if not path.is_file():
            die(f"missing file {path}")

    source_chapter_bytes = source_chapter_path.read_bytes()
    target_chapter_bytes = target_chapter_path.read_bytes()
    source = source_chapter_bytes.decode("utf-8", errors="strict")
    target, chapter_trailing = decode_utf8_lf(
        "target triangle.tex",
        target_chapter_bytes,
        require_no_trailing=True,
    )
    if digest(source_chapter_bytes) != FROZEN_AUTHORITY_CHAPTER_SHA256:
        die("pinned authority Chapter 8 body changed")
    if digest(target_chapter_bytes) != FROZEN_TARGET_CHAPTER_SHA256:
        die("translated Chapter 8 body changed")

    chapter_topology = topology(source, target)
    chapter_topology["comments"] = 0
    expected_chapter_topology = {
        "commands": 360,
        "environments": 62,
        "labels": 20,
        "equation_labels": 5,
        "references": 28,
        "citations": 0,
        "graphics": 9,
        "theorem_options": 19,
        "qeds": 6,
        "comments": 0,
    }
    if chapter_topology != expected_chapter_topology:
        die(f"unexpected active chapter topology: {chapter_topology!r}")

    chapter_raw_topology = topology(source, target, raw=True)
    chapter_raw_topology["comments"] = require_comments_preserved(
        source, target, name="Chapter 8 body"
    )
    if chapter_raw_topology != expected_chapter_topology:
        die(f"unexpected raw chapter topology: {chapter_raw_topology!r}")

    scalar_counts = {
        "sections": len(ordered(r"\\section(?:\[[^\]]*\])?\{", source)),
        "index_entries": len(ordered(r"\\index\{", source)),
        "absolute_markers": len(
            ordered(r"\\begin\{thm\}\[\\abs\]", source)
        ),
        "used_later_markers": len(ordered(r"\\begin\{thm\}\[!\]", source)),
    }
    expected_scalars = {
        "sections": 6,
        "index_entries": 15,
        "absolute_markers": 2,
        "used_later_markers": 1,
    }
    target_scalars = {
        "sections": len(ordered(r"\\section(?:\[[^\]]*\])?\{", target)),
        "index_entries": len(ordered(r"\\index\{", target)),
        "absolute_markers": len(
            ordered(r"\\begin\{thm\}\[\\abs\]", target)
        ),
        "used_later_markers": len(ordered(r"\\begin\{thm\}\[!\]", target)),
    }
    if scalar_counts != expected_scalars or target_scalars != expected_scalars:
        die(
            "Chapter 8 scalar counts changed: "
            f"authority={scalar_counts!r}, target={target_scalars!r}"
        )

    expected_math_deviations = [
        ("delete", 137, 138, 137, 137, ["A"], []),
        ("insert", 140, 140, 139, 140, [], ["A"]),
    ]
    source_math = math_surfaces(source)
    target_math = math_surfaces(target)
    chapter_math_deviations = require_named_sequence_differences(
        "active Chapter 8 math topology",
        source_math,
        target_math,
        expected_math_deviations,
    )
    source_raw_math = math_surfaces(source, include_comments=True)
    target_raw_math = math_surfaces(target, include_comments=True)
    chapter_raw_math_deviations = require_named_sequence_differences(
        "raw Chapter 8 math topology",
        source_raw_math,
        target_raw_math,
        expected_math_deviations,
    )
    if (
        len(source_math),
        len(target_math),
        len(source_raw_math),
        len(target_raw_math),
    ) != (282, 282, 282, 282):
        die("unexpected Chapter 8 math-surface counts")

    source_hint_bytes = source_hints_path.read_bytes()
    target_hint_bytes = target_hints_path.read_bytes()
    _, source_slice, source_suffix = split_hint_slice(
        source_hint_bytes, name="authority hints"
    )
    target_prefix, target_slice, target_suffix = split_hint_slice(
        target_hint_bytes, name="target hints"
    )
    source_hint = source_slice.decode("utf-8", errors="strict")
    target_hint, hint_trailing = decode_utf8_lf(
        "target Chapter 8 hint slice",
        target_slice,
        require_no_trailing=True,
    )
    _, whole_hints_trailing = decode_utf8_lf(
        "target complete hints file",
        target_hint_bytes,
        require_no_trailing=False,
    )
    if digest(source_slice) != FROZEN_AUTHORITY_HINT_SLICE_SHA256:
        die("pinned authority Chapter 8 hint slice changed")
    if digest(source_suffix) != FROZEN_AUTHORITY_SUFFIX_SHA256:
        die("pinned authority Chapter 9+ hint suffix changed")
    if digest(target_prefix) != FROZEN_TARGET_PREFIX_SHA256:
        die("frozen translated pre-Chapter-8 hint prefix changed")
    if digest(target_slice) != FROZEN_TARGET_HINT_SLICE_SHA256:
        die("translated Chapter 8 hint slice changed")
    if digest(target_hint_bytes) != FROZEN_TARGET_WHOLE_HINTS_SHA256:
        die("translated complete hints file changed")
    if digest(target_suffix) != FROZEN_AUTHORITY_SUFFIX_SHA256:
        die("target Chapter 9+ hint suffix changed")
    if target_suffix != source_suffix:
        die("untouched Chapter 9+ hint suffix differs from authority")

    hint_topology = topology(source_hint, target_hint)
    hint_topology["comments"] = 0
    expected_hint_topology = {
        "commands": 111,
        "environments": 2,
        "labels": 0,
        "equation_labels": 0,
        "references": 27,
        "citations": 0,
        "graphics": 0,
        "theorem_options": 0,
        "qeds": 0,
        "comments": 0,
    }
    if hint_topology != expected_hint_topology:
        die(f"unexpected active hint topology: {hint_topology!r}")

    hint_raw_topology = topology(source_hint, target_hint, raw=True)
    hint_raw_topology["comments"] = require_comments_preserved(
        source_hint, target_hint, name="Chapter 8 hints"
    )
    expected_hint_raw_topology = {
        "commands": 113,
        "environments": 2,
        "labels": 0,
        "equation_labels": 0,
        "references": 28,
        "citations": 0,
        "graphics": 0,
        "theorem_options": 0,
        "qeds": 0,
        "comments": 1,
    }
    if hint_raw_topology != expected_hint_raw_topology:
        die(f"unexpected raw hint topology: {hint_raw_topology!r}")

    source_hint_math = math_surfaces(source_hint)
    target_hint_math = math_surfaces(target_hint)
    source_hint_raw_math = math_surfaces(source_hint, include_comments=True)
    target_hint_raw_math = math_surfaces(target_hint, include_comments=True)
    if source_hint_math != target_hint_math:
        die("active Chapter 8 hint math surfaces changed")
    if source_hint_raw_math != target_hint_raw_math:
        die("raw Chapter 8 hint math surfaces changed")
    if (
        len(source_hint_math),
        len(target_hint_math),
        len(source_hint_raw_math),
        len(target_hint_raw_math),
    ) != (39, 39, 39, 39):
        die("unexpected Chapter 8 hint math-surface counts")

    exercise_pattern = (
        r"\\begin\{thm\}(?:\[[^\]]*\])?\{[^}]+\}"
        r"\s*\\label\{(ex:[^}]+)\}"
    )
    hint_header_pattern = r"\\parbf\{\\ref\{(ex:[^}]+)\}\.\}"
    exercise_ids = ordered(exercise_pattern, source)
    target_exercise_ids = ordered(exercise_pattern, target)
    hint_ids = ordered(hint_header_pattern, target_hint)
    expected_exercise_ids = [
        "ex:unique-cline",
        "ex:orthic-4",
        "ex:orthic-sim",
        "ex:midle",
        "ex:euler-line",
        "ex:perp-bisectors",
        "ex:bisect=altitude",
        "ex:ext-disect",
        "ex:bisect=median",
        "ex:bisector-parallel",
        "ex:2x=b+c-a",
        "ex:orthic-triangle",
        "ex:bisector-incenter",
    ]
    if (
        exercise_ids != expected_exercise_ids
        or target_exercise_ids != expected_exercise_ids
        or hint_ids != expected_exercise_ids
    ):
        die(
            "Chapter 8 exercise-hint closure changed: "
            f"authority={exercise_ids!r}, target={target_exercise_ids!r}, "
            f"hints={hint_ids!r}"
        )
    if len(set(hint_ids)) != len(hint_ids):
        die("Chapter 8 hint headers are not unique")

    all_hint_exercise_refs = ordered(r"\\ref\{(ex:[^}]+)\}", target_hint)
    external_hint_refs = sorted(
        set(all_hint_exercise_refs) - set(expected_exercise_ids)
    )
    if external_hint_refs != ["ex:abs-bisect=median"]:
        die(f"unexpected external Chapter 8 hint references: {external_hint_refs!r}")
    if all_hint_exercise_refs.count("ex:abs-bisect=median") != 1:
        die("external ex:abs-bisect=median hint reference changed")
    external_exercise = external_exercise_path.read_text(encoding="utf-8")
    require_once(
        external_exercise,
        r"\label{ex:abs-bisect=median}",
        name="authority external exercise ex:abs-bisect=median",
    )

    chapter_english = require_no_active_english("Chapter 8 body", target)
    hint_english = require_no_active_english("Chapter 8 hints", target_hint)
    chapter_overlap = require_no_untranslated_source_overlap(
        "Chapter 8 body", source, target
    )
    hint_overlap = require_no_untranslated_source_overlap(
        "Chapter 8 hints", source_hint, target_hint
    )

    require_once(source, r"\label{ex:midle}", name="authority ex:midle label")
    require_once(target, r"\label{ex:midle}", name="target ex:midle label")
    require_once(
        source,
        r"\label{ex:ext-disect}",
        name="authority ex:ext-disect label",
    )
    require_once(
        target,
        r"\label{ex:ext-disect}",
        name="target ex:ext-disect label",
    )
    require_once(
        source,
        "at vertices $A$, $B$, and $C$ respectively.",
        name="authority angle-bisector vertex correspondence",
    )
    require_once(
        target,
        "masing-masing di titik sudut $B$, $C$, dan $A$.",
        name="corrected angle-bisector vertex correspondence",
    )
    require_once(
        source,
        "From the same lemma,",
        name="authority same-lemma wording",
    )
    require_once(
        target,
        "Dari proposisi yang sama,",
        name="corrected same-proposition wording",
    )
    if source.count("external bisector") != 7 or source.count(
        "exterior bisector"
    ) != 2:
        die("authority external/exterior bisector terminology changed")
    if target.count("garis bagi luar") != 9:
        die("target external/exterior bisector normalization changed")
    require_once(
        target,
        r"\index{garis tinggi}\emph{garis tinggi}",
        name="line-valued altitude term",
    )
    require_once(
        target,
        r"\index{garis tinggi}\emph{tinggi}",
        name="distance-valued altitude term",
    )
    require_once(
        target_hint,
        "Pelajari homoteti.",
        name="homothety self-study dependency",
    )
    if target_hint.count("homoteti") != 3:
        die("Chapter 8 homothety hint surface changed")
    require_once(
        source_hint,
        r"\index{excenter}\emph{excenters}",
        name="authority hint-only excenter surface",
    )
    require_once(
        target_hint,
        r"\index{eksenter}\emph{eksenter}",
        name="translated hint-only excenter surface",
    )

    named_source_notes = [
        {
            "id": "o004.petrunin.correction.ch08.midle-label-spelling",
            "surface": "identifier",
            "authority_line": 163,
            "authority_hint_line": 810,
            "description": "The immutable exercise ID ex:midle retains the source spelling midle.",
            "proposed_correction": "Normalize only with a complete migration of the body label, hint header, backend ID links, and every cross-reference.",
            "target_action": "preserved immutable identifier",
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.correction.ch08.ext-disect-label-spelling",
            "surface": "identifier",
            "authority_line": 252,
            "authority_hint_line": 840,
            "description": "The immutable exercise ID ex:ext-disect retains the source spelling disect.",
            "proposed_correction": "Normalize only with a complete migration of the body label, hint header, backend ID links, and every cross-reference.",
            "target_action": "preserved immutable identifier",
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.correction.ch08.angle-bisector-vertex-correspondence",
            "surface": "body",
            "authority_lines": "201-202",
            "description": "The listed angles ABC, BCA, and CAB have vertices B, C, and A respectively, while the authority sentence assigns them to A, B, and C.",
            "proposed_correction": "Replace the vertex sequence A, B, C with B, C, A.",
            "confidence": "high",
            "target_action": "corrected the displayed correspondence to B, C, A",
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.correction.ch08.same-lemma-reference-kind",
            "surface": "body",
            "authority_lines": "392-394",
            "description": "The proof explicitly applies Proposition prop:angle-bisect-dist and then calls it the same lemma.",
            "proposed_correction": "Replace same lemma with same proposition.",
            "confidence": "high",
            "target_action": "translated as proposisi yang sama",
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.localization.ch08.external-exterior-bisector-normalization",
            "surface": "body-and-hints",
            "authority_body_lines": "183-400",
            "description": "The authority alternates external bisector and exterior bisector for the same concept.",
            "target_action": "normalized both terms consistently to garis bagi luar",
            "mathematics_changed": False,
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.localization.ch08.altitude-line-distance-distinction",
            "surface": "body",
            "authority_lines": "51-52",
            "description": "The source deliberately uses altitude both for a line and for the scalar distance from a vertex to its footpoint.",
            "target_action": "rendered the line as garis tinggi and the distance as tinggi while retaining one shared index concept",
            "mathematics_changed": False,
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.dependency.ch08.homothety-self-study",
            "surface": "hints",
            "authority_lines": "815-822",
            "description": "The Euler-line hint requires homothety and tells the learner to read about it, but Chapter 8 supplies no definition or internal prerequisite link.",
            "target_action": "preserved and translated the explicit self-study dependency without inventing a replacement hint",
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.dependency.ch08.external-absolute-bisect-median-reference",
            "surface": "hints",
            "authority_line": 848,
            "description": "The ex:bisect=median hint points outside Chapter 8 to ex:abs-bisect=median, defined later in absolute.tex line 77.",
            "target_action": "preserved the external stable label and verified that it resolves within the complete authority corpus",
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.dependency.ch08.hint-only-excenter",
            "surface": "hints",
            "authority_lines": "864-866",
            "description": "The orthic-triangle hint introduces excenters even though Chapter 8 body prose does not define the term.",
            "target_action": "translated and indexed the term as eksenter and retained the source's explanatory intersection description",
            "source_changed": False,
        },
    ]

    report = {
        "schema": "o004-ch08-qa-v0",
        "status": "pass",
        "authority": {
            "chapter_bytes": len(source_chapter_bytes),
            "chapter_sha256": digest(source_chapter_bytes),
            "hint_slice_lines": "793-871",
            "hint_slice_bytes": len(source_slice),
            "hint_slice_sha256": digest(source_slice),
            "later_suffix_bytes": len(source_suffix),
            "later_suffix_sha256": digest(source_suffix),
        },
        "target": {
            "chapter_bytes": len(target_chapter_bytes),
            "chapter_sha256": digest(target_chapter_bytes),
            "hint_slice_lines": "793-871",
            "hint_slice_bytes": len(target_slice),
            "hint_slice_sha256": digest(target_slice),
            "whole_hints_bytes": len(target_hint_bytes),
            "whole_hints_sha256": digest(target_hint_bytes),
            "frozen_pre_chapter_8_prefix_bytes": len(target_prefix),
            "frozen_pre_chapter_8_prefix_sha256": digest(target_prefix),
            "chapter_9_plus_suffix_bytes": len(target_suffix),
            "chapter_9_plus_suffix_sha256": digest(target_suffix),
            "chapter_9_plus_suffix_matches_authority": target_suffix
            == source_suffix,
            "utf8_lf_no_bom_terminal_lf": True,
            "edited_surface_trailing_whitespace_lines": {
                "chapter": chapter_trailing,
                "hints": hint_trailing,
            },
            "whole_hints_inherited_trailing_whitespace_outside_chapter_8_count": len(
                whole_hints_trailing
            ),
            "active_english_prose_hits": {
                "chapter": chapter_english,
                "hints": hint_english,
            },
            "untranslated_source_language_overlap": {
                "chapter": chapter_overlap,
                "hints": hint_overlap,
            },
        },
        "chapter_topology": chapter_topology,
        "chapter_raw_topology": chapter_raw_topology,
        "scalar_counts": scalar_counts,
        "chapter_math_surfaces": {
            "authority_active": len(source_math),
            "target_active": len(target_math),
            "authority_raw": len(source_raw_math),
            "target_raw": len(target_raw_math),
            "named_deviations_active": chapter_math_deviations,
            "named_deviations_raw": chapter_raw_math_deviations,
            "named_id": "o004.petrunin.correction.ch08.angle-bisector-vertex-correspondence",
        },
        "exercise_hint_closure": {
            "exercise_count": len(exercise_ids),
            "hint_header_count": len(hint_ids),
            "ordered_exercise_ids": expected_exercise_ids,
            "direct_complete": True,
            "external_hint_references": [
                {
                    "id": "ex:abs-bisect=median",
                    "authority_path": "source/upstream/birkhoff-0b0858e1e985f4c8dadbb6075ae9e095cd4a8981/absolute.tex",
                    "authority_line": 77,
                    "resolved_in_complete_authority_corpus": True,
                }
            ],
        },
        "hint_topology": hint_topology,
        "hint_raw_topology": hint_raw_topology,
        "hint_math_surfaces": {
            "authority_active": len(source_hint_math),
            "target_active": len(target_hint_math),
            "authority_raw": len(source_hint_raw_math),
            "target_raw": len(target_hint_raw_math),
            "exact_order": True,
        },
        "inactive_surfaces": {
            "body_comments_preserved": True,
            "body_comment_count": chapter_raw_topology["comments"],
            "hint_comments_preserved": True,
            "hint_comment_count": hint_raw_topology["comments"],
        },
        "named_source_notes": named_source_notes,
    }
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
