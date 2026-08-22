#!/usr/bin/env python3
"""Fail-closed structural QA for O004 Chapter 7 and its exact hint slice."""

from __future__ import annotations

import hashlib
import difflib
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
CH7_MARKER = b"%\\subsection*{Chapter~\\ref{chap:angle-sum}}"
CH8_MARKER = b"%\\subsection*{Chapter~\\ref{chap:triangle}}"
FROZEN_AUTHORITY_CHAPTER_SHA256 = (
    "4b9d48e62644119e03f8c8875850fb9a08cad85236766b8fdaae08c8084321b3"
)
FROZEN_AUTHORITY_HINT_SLICE_SHA256 = (
    "60a99490a841b318c0d03be10fbdc7590fc70e1913f339cdcd94c1950642afbf"
)
FROZEN_AUTHORITY_SUFFIX_SHA256 = (
    "4f3df5cb98e16c929468bcb8624e9851d4442440a03e87624d27113190238de1"
)
FROZEN_TARGET_PREFIX_SHA256 = (
    "29fc07469fbb866904cf168bc758a794eaa22baad34e9fd8cf947f0a55fedabb"
)
FROZEN_TARGET_CHAPTER_SHA256 = (
    "3459de730c56922fe4a9e30781d3a12ce1671c735423f5eaed12175d9d5d5385"
)
FROZEN_TARGET_HINT_SLICE_SHA256 = (
    "1a914474041c1a1fb05a3b7f2cd46c8da279431de7d08e39ed9f72e770532280"
)
FROZEN_TARGET_WHOLE_HINTS_SHA256 = (
    "345caa2579bb9c9781d5c9f5426ddf25e710f4b5cfe6eff71440b6a6ca811cde"
)
EXPECTED_HINT_TRAILING_WHITESPACE_LINES = (73, 80)

_shared = runpy.run_path(str(Path(__file__).with_name("qa_ch05.py")))
ordered = _shared["ordered"]
ordered_raw = _shared["ordered_raw"]
require_same = _shared["require_same"]
math_surfaces = _shared["math_surfaces"]
prose_tokens = _shared["prose_tokens"]
ENGLISH_RESIDUE_WORDS = _shared["ENGLISH_RESIDUE_WORDS"]

ALLOWED_SHARED_SOURCE_WORDS = frozenset(
    {
        "apollonius",
        "birkhoff",
        "data",
        "diameter",
        "elements",
        "enumi",
        "model",
        "pasch",
        "pythagoras",
        "real",
        "sas",
        "sss",
        "transversal",
        "universal",
    }
)


def die(message: str) -> None:
    raise SystemExit(f"QA_FAIL: {message}")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def split_slice(data: bytes, *, name: str) -> tuple[bytes, bytes, bytes]:
    if data.count(CH7_MARKER) != 1 or data.count(CH8_MARKER) != 1:
        die(f"{name}: Chapter 7 or Chapter 8 hint marker is not unique")
    left = data.index(CH7_MARKER)
    right = data.index(CH8_MARKER, left + len(CH7_MARKER))
    first_line = data[:left].count(b"\n") + 1
    next_marker_line = data[:right].count(b"\n") + 1
    if (first_line, next_marker_line) != (608, 793):
        die(
            f"{name}: Chapter 7 hint slice moved from lines 608-792 "
            f"to {first_line}-{next_marker_line - 1}"
        )
    return data[:left], data[left:right], data[right:]


def require_utf8_lf(
    name: str,
    data: bytes,
    *,
    expected_trailing_lines: tuple[int, ...] = (),
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
    if tuple(trailing) != expected_trailing_lines:
        die(
            f"{name} trailing-whitespace lines changed: "
            f"expected {list(expected_trailing_lines)}, found {trailing}"
        )
    for line_number in trailing:
        if not text.splitlines()[line_number - 1].lstrip().startswith("%"):
            die(f"{name} has active trailing whitespace on line {line_number}")
    return text, trailing


def require_comments_preserved(source: str, target: str, *, name: str) -> int:
    pattern = r"(?m)^%[^\r\n]*$"
    source_comments = ordered_raw(pattern, source)
    target_comments = ordered_raw(pattern, target)
    normalized_source = [comment.rstrip(" \t") for comment in source_comments]
    normalized_target = [comment.rstrip(" \t") for comment in target_comments]
    if normalized_source != normalized_target:
        die(f"{name} inactive comment surfaces changed")
    return len(source_comments)


def require_body_comments_with_reflow_note(
    source: str, target: str
) -> dict[str, int]:
    pattern = r"(?m)^%[^\r\n]*$"
    source_comments = ordered_raw(pattern, source)
    target_comments = ordered_raw(pattern, target)
    normalized_source = [comment.rstrip(" \t") for comment in source_comments]
    normalized_target = [comment.rstrip(" \t") for comment in target_comments]
    reflow_note = (
        "% Reflow id-ID: the inherited forced page break is omitted; "
        "content and order are unchanged."
    )
    if normalized_target != [reflow_note, *normalized_source]:
        die("Chapter 7 body inactive comments changed beyond the named reflow note")
    return {
        "authority_comments": len(source_comments),
        "target_comments": len(target_comments),
    }


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


def topology(
    source: str,
    target: str,
    *,
    raw: bool = False,
    require_identical_commands: bool = True,
) -> dict[str, int]:
    suffix = "raw " if raw else "active "
    result = {
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
    if require_identical_commands:
        result = {
            "commands": require_same(
            f"ordered {suffix}commands",
            r"\\[A-Za-z@]+",
            source,
            target,
            raw=raw,
        ),
            **result,
        }
    return result


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


def require_once(text: str, needle: str, *, name: str) -> None:
    if text.count(needle) != 1:
        die(f"{name} is missing or duplicated")


def main() -> None:
    source_chapter_path = AUTHORITY / "parallel.tex"
    target_chapter_path = TARGET / "parallel.tex"
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
    target, chapter_trailing = require_utf8_lf(
        "target parallel.tex", target_chapter_bytes
    )
    if digest(source_chapter_bytes) != FROZEN_AUTHORITY_CHAPTER_SHA256:
        die("pinned authority Chapter 7 body changed")
    if digest(target_chapter_bytes) != FROZEN_TARGET_CHAPTER_SHA256:
        die("translated Chapter 7 body changed")

    source_commands = ordered(r"\\[A-Za-z@]+", source)
    target_commands = ordered(r"\\[A-Za-z@]+", target)
    chapter_command_deviations = require_named_sequence_differences(
        "active Chapter 7 command topology",
        source_commands,
        target_commands,
        [
            ("delete", 223, 224, 223, 223, [r"\pagebreak"], []),
            ("insert", 225, 225, 224, 225, [], [r"\hspace"]),
            (
                "insert",
                616,
                616,
                616,
                619,
                [],
                [r"\ne", r"\notin", r"\ne"],
            ),
        ],
    )
    chapter_topology = topology(
        source, target, require_identical_commands=False
    )
    chapter_topology = {
        "authority_commands": len(source_commands),
        "target_commands": len(target_commands),
        **chapter_topology,
    }
    chapter_topology["comments"] = 0
    expected_chapter_topology = {
        "authority_commands": 617,
        "target_commands": 620,
        "environments": 96,
        "labels": 35,
        "equation_labels": 5,
        "references": 44,
        "citations": 0,
        "graphics": 13,
        "theorem_options": 29,
        "qeds": 9,
        "comments": 0,
    }
    if chapter_topology != expected_chapter_topology:
        die(f"unexpected active chapter topology: {chapter_topology!r}")

    source_raw_commands = ordered_raw(r"\\[A-Za-z@]+", source)
    target_raw_commands = ordered_raw(r"\\[A-Za-z@]+", target)
    chapter_raw_command_deviations = require_named_sequence_differences(
        "raw Chapter 7 command topology",
        source_raw_commands,
        target_raw_commands,
        [
            ("delete", 223, 224, 223, 223, [r"\pagebreak"], []),
            ("insert", 225, 225, 224, 225, [], [r"\hspace"]),
            (
                "insert",
                627,
                627,
                627,
                630,
                [],
                [r"\ne", r"\notin", r"\ne"],
            ),
        ],
    )
    chapter_raw_topology = topology(
        source, target, raw=True, require_identical_commands=False
    )
    chapter_raw_topology = {
        "authority_commands": len(source_raw_commands),
        "target_commands": len(target_raw_commands),
        **chapter_raw_topology,
        **require_body_comments_with_reflow_note(source, target),
    }
    expected_chapter_raw_topology = {
        "authority_commands": 628,
        "target_commands": 631,
        "environments": 98,
        "labels": 36,
        "equation_labels": 5,
        "references": 44,
        "citations": 0,
        "graphics": 14,
        "theorem_options": 30,
        "qeds": 9,
        "authority_comments": 7,
        "target_comments": 8,
    }
    if chapter_raw_topology != expected_chapter_raw_topology:
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
        "used_later_markers": 5,
    }
    if scalar_counts != expected_scalars:
        die(f"unexpected authority scalar counts: {scalar_counts!r}")
    target_scalars = {
        "sections": len(ordered(r"\\section(?:\[[^\]]*\])?\{", target)),
        "index_entries": len(ordered(r"\\index\{", target)),
        "absolute_markers": len(
            ordered(r"\\begin\{thm\}\[\\abs\]", target)
        ),
        "used_later_markers": len(ordered(r"\\begin\{thm\}\[!\]", target)),
    }
    if target_scalars != expected_scalars:
        die(f"translated scalar counts changed: {target_scalars!r}")

    source_math = math_surfaces(source)
    target_math = math_surfaces(target)
    chapter_math_deviations = require_named_sequence_differences(
        "active Chapter 7 math topology",
        source_math,
        target_math,
        [
            ("insert", 41, 41, 41, 42, [], ["m"]),
            ("delete", 42, 43, 43, 43, ["m"], []),
            ("replace", 148, 149, 148, 149, ["P"], ["Q"]),
            (
                "insert",
                410,
                410,
                410,
                413,
                [],
                [r"A\neB", r"M\notin\{A,B\}", r"AM\neBM"],
            ),
        ],
    )
    if (len(source_math), len(target_math)) != (413, 416):
        die("unexpected active Chapter 7 math-surface counts")
    source_raw_math = math_surfaces(source, include_comments=True)
    target_raw_math = math_surfaces(target, include_comments=True)
    chapter_raw_math_deviations = require_named_sequence_differences(
        "raw Chapter 7 math topology",
        source_raw_math,
        target_raw_math,
        [
            ("insert", 41, 41, 41, 42, [], ["m"]),
            ("delete", 42, 43, 43, 43, ["m"], []),
            ("replace", 148, 149, 148, 149, ["P"], ["Q"]),
            (
                "insert",
                417,
                417,
                417,
                420,
                [],
                [r"A\neB", r"M\notin\{A,B\}", r"AM\neBM"],
            ),
        ],
    )
    if (len(source_raw_math), len(target_raw_math)) != (420, 423):
        die("unexpected raw Chapter 7 math-surface counts")

    source_hint_bytes = source_hints_path.read_bytes()
    target_hint_bytes = target_hints_path.read_bytes()
    _, source_slice, source_suffix = split_slice(
        source_hint_bytes, name="authority hints"
    )
    target_prefix, target_slice, target_suffix = split_slice(
        target_hint_bytes, name="target hints"
    )
    source_hint = source_slice.decode("utf-8", errors="strict")
    target_hint, hint_trailing = require_utf8_lf(
        "target Chapter 7 hint slice",
        target_slice,
        expected_trailing_lines=EXPECTED_HINT_TRAILING_WHITESPACE_LINES,
    )
    if digest(source_slice) != FROZEN_AUTHORITY_HINT_SLICE_SHA256:
        die("pinned authority Chapter 7 hint slice changed")
    if digest(source_suffix) != FROZEN_AUTHORITY_SUFFIX_SHA256:
        die("pinned authority Chapter 8+ hint suffix changed")
    if digest(target_prefix) != FROZEN_TARGET_PREFIX_SHA256:
        die("frozen translated Chapter 1-6 hint prefix changed")
    if digest(target_slice) != FROZEN_TARGET_HINT_SLICE_SHA256:
        die("translated Chapter 7 hint slice changed")
    if digest(target_hint_bytes) != FROZEN_TARGET_WHOLE_HINTS_SHA256:
        die("translated complete hints file changed")
    if target_suffix != source_suffix:
        die("untouched Chapter 8+ hint suffix differs from authority")

    hint_topology = topology(source_hint, target_hint)
    hint_topology["comments"] = 0
    expected_hint_topology = {
        "commands": 199,
        "environments": 6,
        "labels": 0,
        "equation_labels": 2,
        "references": 56,
        "citations": 0,
        "graphics": 2,
        "theorem_options": 0,
        "qeds": 0,
        "comments": 0,
    }
    if hint_topology != expected_hint_topology:
        die(f"unexpected active hint topology: {hint_topology!r}")

    hint_raw_topology = topology(source_hint, target_hint, raw=True)
    hint_raw_topology["comments"] = require_comments_preserved(
        source_hint, target_hint, name="Chapter 7 hints"
    )
    expected_hint_raw_topology = {
        "commands": 222,
        "environments": 8,
        "labels": 0,
        "equation_labels": 2,
        "references": 60,
        "citations": 0,
        "graphics": 3,
        "theorem_options": 0,
        "qeds": 0,
        "comments": 12,
    }
    if hint_raw_topology != expected_hint_raw_topology:
        die(f"unexpected raw hint topology: {hint_raw_topology!r}")

    source_hint_math = math_surfaces(source_hint)
    target_hint_math = math_surfaces(target_hint)
    hint_math_deviations = require_named_sequence_differences(
        "active Chapter 7 hint math topology",
        source_hint_math,
        target_hint_math,
        [
            ("replace", 54, 55, 54, 55, [r"D\neC"], [r"D\neB"]),
            (
                "replace",
                67,
                68,
                67,
                68,
                [
                    r"AB=CD\\iff\\triangleAMB\cong\triangleAMD"
                    r"\\z\iff\\measuredangleAMB=\pm\tfrac\pi2"
                ],
                [
                    r"AB=AD\\iff\\triangleAMB\cong\triangleAMD"
                    r"\\z\iff\\measuredangleAMB=\pm\tfrac\pi2"
                ],
            ),
        ],
    )
    if len(source_hint_math) != 91 or len(target_hint_math) != 91:
        die("unexpected active Chapter 7 hint math-surface counts")
    source_hint_raw_math = math_surfaces(source_hint, include_comments=True)
    target_hint_raw_math = math_surfaces(target_hint, include_comments=True)
    hint_raw_math_deviations = require_named_sequence_differences(
        "raw Chapter 7 hint math topology",
        source_hint_raw_math,
        target_hint_raw_math,
        [
            ("replace", 60, 61, 60, 61, [r"D\neC"], [r"D\neB"]),
            (
                "replace",
                73,
                74,
                73,
                74,
                [
                    r"AB=CD\\iff\\triangleAMB\cong\triangleAMD"
                    r"\\z\iff\\measuredangleAMB=\pm\tfrac\pi2"
                ],
                [
                    r"AB=AD\\iff\\triangleAMB\cong\triangleAMD"
                    r"\\z\iff\\measuredangleAMB=\pm\tfrac\pi2"
                ],
            ),
        ],
    )
    if len(source_hint_raw_math) != 97 or len(target_hint_raw_math) != 97:
        die("unexpected raw Chapter 7 hint math-surface counts")

    top_level_pattern = (
        r"\\begin\{thm\}(?:\[[^\]]*\])?\{[^}]+\}"
        r"\\label\{(ex:[^}]+)\}"
    )
    expected_top_level_exercises = [
        "ex:perp-perp",
        "ex:construction-parallel",
        "ex:reflections",
        "ex:parallel-angles",
        "ex:smililar+parallel",
        "ex:trisection",
        "ex:|3sum|",
        "ex:pent",
        "ex:right-isos",
        "ex:quadrangle",
        "ex:4parallels",
        "ex:romb",
        "ex:rectangle",
        "ex:romb2",
        "ex:inscribed-rhombus",
        "ex:coordinates",
        "ex:abc",
        "ex:line-coord",
        "ex:circle-coord",
        "ex:apolonnius",
        "ex:apolonnius-construction",
    ]
    expected_all_exercise_ids = [
        "ex:perp-perp",
        "ex:perp-perp:a",
        "ex:perp-perp:b",
        "ex:construction-parallel",
        "ex:reflections",
        "ex:parallel-angles",
        "ex:smililar+parallel",
        "ex:trisection",
        "ex:|3sum|",
        "ex:pent",
        "ex:right-isos",
        "ex:quadrangle",
        "ex:4parallels",
        "ex:romb",
        "ex:rectangle",
        "ex:romb2",
        "ex:inscribed-rhombus",
        "ex:coordinates",
        "ex:abc",
        "ex:line-coord",
        "ex:line-coord:parameter",
        "ex:circle-coord",
        "ex:apolonnius",
        "ex:apolonnius-construction",
    ]
    source_top_level = ordered(top_level_pattern, source)
    target_top_level = ordered(top_level_pattern, target)
    source_all_exercises = ordered(r"\\label\{(ex:[^}]+)\}", source)
    target_all_exercises = ordered(r"\\label\{(ex:[^}]+)\}", target)
    hint_headers = ordered(r"\\parbf\{\\ref\{(ex:[^}]+)\}", target_hint)
    source_hint_headers = ordered(
        r"\\parbf\{\\ref\{(ex:[^}]+)\}", source_hint
    )
    if source_top_level != expected_top_level_exercises or target_top_level != expected_top_level_exercises:
        die("ordered Chapter 7 top-level exercise identities changed")
    if source_all_exercises != expected_all_exercise_ids or target_all_exercises != expected_all_exercise_ids:
        die("ordered Chapter 7 exercise/subpart identities changed")
    if source_hint_headers != expected_top_level_exercises or hint_headers != expected_top_level_exercises:
        die("top-level Chapter 7 exercise-to-hint closure changed")

    source_hint_exercise_refs = ordered(r"\\ref\{(ex:[^}]+)\}", source_hint)
    target_hint_exercise_refs = ordered(r"\\ref\{(ex:[^}]+)\}", target_hint)
    if source_hint_exercise_refs != target_hint_exercise_refs:
        die("ordered Chapter 7 exercise references in hints changed")
    subpart_ids = [
        exercise_id
        for exercise_id in expected_all_exercise_ids
        if exercise_id not in expected_top_level_exercises
    ]
    referenced_subparts = [
        exercise_id
        for exercise_id in subpart_ids
        if exercise_id in target_hint_exercise_refs
    ]
    unreferenced_subparts = [
        exercise_id
        for exercise_id in subpart_ids
        if exercise_id not in target_hint_exercise_refs
    ]
    if referenced_subparts != ["ex:perp-perp:a", "ex:perp-perp:b"]:
        die("expected perpendicular-line exercise subpart hint references changed")
    if unreferenced_subparts != ["ex:line-coord:parameter"]:
        die("expected unreferenced line-coordinate subpart identity changed")

    body_english_hits = require_no_active_english("target parallel.tex", target)
    hint_english_hits = require_no_active_english(
        "target Chapter 7 hints", target_hint
    )
    body_source_overlap = require_no_untranslated_source_overlap(
        "target parallel.tex", source, target
    )
    hint_source_overlap = require_no_untranslated_source_overlap(
        "target Chapter 7 hints", source_hint, target_hint
    )

    require_once(
        source,
        r"\chapter{Parallel lines}\label{chap:angle-sum}",
        name="legacy Chapter 7 label in authority",
    )
    require_once(
        target,
        r"\chapter{Garis sejajar}\label{chap:angle-sum}",
        name="legacy Chapter 7 label in target",
    )
    require_once(
        source,
        "Both lines $\\ell'$ and $m$ pass thru $P$.",
        name="possible P/Q incidence error in authority",
    )
    require_once(
        target,
        "Kedua garis $\\ell'$ dan $m$ melalui $Q$.",
        name="corrected P/Q incidence surface in target",
    )
    require_once(
        source,
        r"\index{quadrangle!degenerate quadrangle}\index{degenerate!quadrangle}\emph{nondegenerate}",
        name="nondegenerate-definition index mismatch in authority",
    )
    require_once(
        target,
        r"\index{segiempat!segiempat tak degenerat}\index{tak degenerat!segiempat}\emph{tak degenerat}",
        name="corrected nondegenerate-definition index keys in target",
    )
    require_once(
        source_hint,
        "Since $D\\ne C$, we get ``$-$'' in the last formula.",
        name="rhombus sign-choice condition in authority hint",
    )
    require_once(
        target_hint,
        "Karena $D\\ne B$, tanda dalam rumus terakhir harus ``$-$''.",
        name="corrected rhombus sign-choice condition in target hint",
    )
    require_once(
        source_hint,
        r"$AB=CD\ \iff\ \triangle AMB",
        name="rhombus adjacent-side condition in authority hint",
    )
    require_once(
        target_hint,
        r"$AB=AD\ \iff\ \triangle AMB",
        name="corrected rhombus adjacent-side condition in target hint",
    )
    for identifier in (
        "ex:smililar+parallel",
        "ex:apolonnius",
        "ex:apolonnius-construction",
    ):
        require_once(source, rf"\label{{{identifier}}}", name=f"authority ID {identifier}")
        require_once(target, rf"\label{{{identifier}}}", name=f"target ID {identifier}")
    inactive_body_claim = (
        r"%Show that $\measuredangle CAX\z=\pm\tfrac\pi4$."
    )
    inactive_hint_acute = r"%Show that $\angle CAX$ is acute."
    inactive_hint_claim = (
        r"%Conclude that $\measuredangle CAX\z=\pm\tfrac\pi4$."
    )
    for text, surface_name in (
        (source, "authority inactive pi/4 exercise"),
        (target, "target inactive pi/4 exercise"),
    ):
        require_once(text, inactive_body_claim, name=surface_name)
    for text, surface_name in (
        (source_hint, "authority inactive pi/4 hint"),
        (target_hint, "target inactive pi/4 hint"),
    ):
        require_once(text, inactive_hint_acute, name=f"{surface_name} acute step")
        require_once(text, inactive_hint_claim, name=f"{surface_name} conclusion")
    target_apollonius_hypotheses = (
        r"Andaikan $A\ne B$, $M\notin\{A,B\}$, dan $AM\ne BM$."
    )
    if target_apollonius_hypotheses in source:
        die("Apollonius construction hypotheses unexpectedly exist in authority")
    require_once(
        target,
        target_apollonius_hypotheses,
        name="bounded Apollonius construction hypotheses in target",
    )
    require_once(
        target,
        r"Pilih titik $Q\in s$ yang terletak pada sisi $m$ yang sama dengan~$\ell$.",
        name="same-side fluency reordering in target",
    )
    require_once(source, r"\pagebreak%???", name="authority pagebreak comment")
    if r"\pagebreak%???" in target:
        die("target retains the intentionally removed inherited pagebreak")
    require_once(
        target,
        "% Reflow id-ID: the inherited forced page break is omitted; content and order are unchanged.",
        name="target layout-only reflow note",
    )
    require_once(
        target,
        r"\section[Sifat transversal]{\hspace{1em}Sifat transversal}",
        name="target visible section-heading gap reflow",
    )

    named_source_notes = [
        {
            "id": "o004.petrunin.correction.ch07.legacy-chapter-label",
            "surface": "body",
            "authority_line": 1,
            "description": "Parallel lines retains the legacy chapter label chap:angle-sum.",
            "proposed_correction": "Rename only with a complete reference migration if upstream chooses to normalize semantic labels.",
            "target_action": "preserved",
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.correction.ch07.parallel-reflection-incidence-p-or-q",
            "surface": "body",
            "authority_line": 187,
            "description": "The only-if proof says the reflected line and m both pass through P, although the theorem says m passes through Q and reflection across the midpoint sends P to Q.",
            "proposed_correction": "Replace P with Q.",
            "confidence": "high",
            "target_action": "corrected P to Q in the proof sentence",
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.correction.ch07.nondegenerate-index-keys",
            "surface": "body",
            "authority_line": 408,
            "description": "The nondegenerate-quadrangle definition is indexed under degenerate quadrangle and degenerate!quadrangle.",
            "proposed_correction": "Change both index keys from degenerate to nondegenerate.",
            "target_action": "corrected both index keys; displayed definition unchanged",
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.correction.ch07.rhombus-sign-distinctness",
            "surface": "hints",
            "authority_line": 711,
            "description": "The ex:romb hint invokes D != C to select the negative angle sign; the relevant distinctness appears to be D != B, or equivalently that B and D lie on opposite sides of AC.",
            "proposed_correction": "Replace D != C with D != B.",
            "confidence": "high",
            "target_action": "corrected D != C to D != B",
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.correction.ch07.rhombus-adjacent-side-condition",
            "surface": "hints",
            "authority_line": 735,
            "description": "The ex:romb2 hint starts AB=CD iff triangle AMB is congruent to triangle AMD, but AB=CD already holds for every parallelogram and the SSS comparison requires the adjacent-side condition AB=AD.",
            "proposed_correction": "Replace AB=CD with AB=AD.",
            "confidence": "high",
            "target_action": "corrected AB=CD to AB=AD",
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.correction.ch07.similar-parallel-label-spelling",
            "surface": "identifier",
            "authority_line": 299,
            "description": "The immutable exercise ID ex:smililar+parallel contains the spelling smililar.",
            "proposed_correction": "Normalize to ex:similar+parallel only with all references migrated.",
            "target_action": "preserved immutable identifier",
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.correction.ch07.apollonius-exercise-label-spelling",
            "surface": "identifier",
            "authority_line": 569,
            "description": "The immutable exercise ID ex:apolonnius contains the spelling apolonnius.",
            "proposed_correction": "Normalize to ex:apollonius only with all references migrated.",
            "target_action": "preserved immutable identifier",
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.correction.ch07.apollonius-construction-label-spelling",
            "surface": "identifier",
            "authority_line": 586,
            "description": "The immutable exercise ID ex:apolonnius-construction contains the spelling apolonnius.",
            "proposed_correction": "Normalize to ex:apollonius-construction only with all references migrated.",
            "target_action": "preserved immutable identifier",
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.correction.ch07.inactive-pi4-exercise-hint-sign",
            "surface": "inactive-body-and-hint",
            "authority_line": 386,
            "authority_hint_lines": "692-693",
            "description": "The inactive exercise asks for measured angle CAX = +/- pi/4; its inactive hint first asks the reader to show the angle is acute and then repeats the signed conclusion, for which +pi/4 appears intended.",
            "proposed_correction": "If this exercise is reactivated, reconcile the acute-angle step and conclusion, most likely by stating +pi/4 after verifying the orientation convention.",
            "confidence": "medium",
            "target_action": "preserved inactive source and hint surfaces verbatim",
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.correction.ch07.apollonius-construction-domain",
            "surface": "body",
            "authority_line": 586,
            "target_line": 587,
            "description": "The straightedge-and-compass construction task needs A != B, M distinct from A and B, and AM != BM for the stated Apollonius circle to be nondegenerate and determined by the given data.",
            "proposed_correction": "State A != B, M not in {A,B}, and AM != BM.",
            "confidence": "high",
            "target_action": "added the three bounded well-posedness hypotheses",
            "source_changed": False,
        },
        {
            "id": "o004.petrunin.correction.ch07.forced-pagebreak-reflow",
            "surface": "layout",
            "authority_line": 191,
            "description": "The authority forces a page break with the unexplained inline marker %???.",
            "proposed_correction": "Remove the forced page break when it produces a sparse page and let the reader reflow naturally.",
            "target_action": "removed the layout-only pagebreak, inserted an explicit id-ID reflow comment, and added a one-em visible heading inset while preserving the short title, source mathematics, and order",
            "source_changed": False,
        },
    ]

    localization_clarifications = [
        {
            "id": "o004.petrunin.localization.ch07.consolidated-fluency-normalization",
            "description": "Reader-facing Indonesian syntax, terminology, punctuation, and referent order were normalized throughout without changing source order or mathematical meaning; one same-side sentence moves the math token m before ell, which accounts for the named delete/insert math-sequence pair.",
            "mathematics_changed": False,
        }
    ]

    report = {
        "schema": "o004-ch07-qa-v0",
        "status": "pass",
        "authority": {
            "chapter_bytes": len(source_chapter_bytes),
            "chapter_sha256": digest(source_chapter_bytes),
            "hint_slice_lines": "608-792",
            "hint_slice_bytes": len(source_slice),
            "hint_slice_sha256": digest(source_slice),
            "later_suffix_bytes": len(source_suffix),
            "later_suffix_sha256": digest(source_suffix),
        },
        "target": {
            "chapter_bytes": len(target_chapter_bytes),
            "chapter_sha256": digest(target_chapter_bytes),
            "hint_slice_lines": "608-792",
            "hint_slice_bytes": len(target_slice),
            "hint_slice_sha256": digest(target_slice),
            "whole_hints_bytes": len(target_hint_bytes),
            "whole_hints_sha256": digest(target_hint_bytes),
            "frozen_chapters_1_6_prefix_bytes": len(target_prefix),
            "frozen_chapters_1_6_prefix_sha256": digest(target_prefix),
            "current_chapter_8_plus_suffix_bytes": len(target_suffix),
            "current_chapter_8_plus_suffix_sha256": digest(target_suffix),
            "chapter_8_plus_suffix_matches_authority": target_suffix == source_suffix,
            "utf8_lf_no_bom_terminal_lf": True,
            "trailing_whitespace_lines": {
                "chapter": chapter_trailing,
                "hints": hint_trailing,
            },
            "inherited_inactive_hint_comment_whitespace_only": True,
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
        "intentional_command_topology_deviations": {
            "active": chapter_command_deviations,
            "raw": chapter_raw_command_deviations,
            "named_ids": [
                "o004.petrunin.correction.ch07.forced-pagebreak-reflow",
                "o004.petrunin.correction.ch07.apollonius-construction-domain",
            ],
        },
        "scalar_counts": scalar_counts,
        "chapter_math_surfaces": {
            "authority_active": len(source_math),
            "target_active": len(target_math),
            "authority_raw": len(source_raw_math),
            "target_raw": len(target_raw_math),
            "named_deviations_active": chapter_math_deviations,
            "named_deviations_raw": chapter_raw_math_deviations,
            "named_ids": [
                "o004.petrunin.localization.ch07.consolidated-fluency-normalization",
                "o004.petrunin.correction.ch07.parallel-reflection-incidence-p-or-q",
                "o004.petrunin.correction.ch07.apollonius-construction-domain",
            ],
        },
        "exercise_hint_closure": {
            "top_level_exercise_count": len(expected_top_level_exercises),
            "hint_header_count": len(hint_headers),
            "ordered_top_level_exercise_ids": expected_top_level_exercises,
            "ordered_exercise_and_subpart_ids": expected_all_exercise_ids,
            "directly_referenced_subpart_ids": referenced_subparts,
            "subpart_without_direct_hint_ref": "ex:line-coord:parameter",
            "subpart_without_direct_hint_ref_note": "The Chapter 7 hint addresses ex:line-coord as a whole and does not directly reference its labeled parameterization subpart.",
            "top_level_complete": True,
        },
        "hint_topology": hint_topology,
        "hint_raw_topology": hint_raw_topology,
        "hint_math_surfaces": {
            "authority_active": len(source_hint_math),
            "target_active": len(target_hint_math),
            "authority_raw": len(source_hint_raw_math),
            "target_raw": len(target_hint_raw_math),
            "named_deviations_active": hint_math_deviations,
            "named_deviations_raw": hint_raw_math_deviations,
            "named_ids": [
                "o004.petrunin.correction.ch07.rhombus-sign-distinctness",
                "o004.petrunin.correction.ch07.rhombus-adjacent-side-condition",
            ],
        },
        "inactive_surfaces": {
            "body_authority_comments_preserved_excluding_trailing_whitespace": True,
            "body_target_added_reflow_comment_only": True,
            "hint_comments_preserved": True,
            "body_authority_comment_count": chapter_raw_topology[
                "authority_comments"
            ],
            "body_target_comment_count": chapter_raw_topology["target_comments"],
            "hint_comment_count": hint_raw_topology["comments"],
        },
        "named_source_notes": named_source_notes,
        "localization_clarifications": localization_clarifications,
    }
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
