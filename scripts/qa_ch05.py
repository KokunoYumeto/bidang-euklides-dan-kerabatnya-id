#!/usr/bin/env python3
"""Fail-closed structural QA for O004 Chapter 5 and its exact hint slice."""

from __future__ import annotations

import difflib
import hashlib
import json
import re
import runpy
import sys
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
AUTHORITY = LANE / "source" / "upstream" / "birkhoff-0b0858e1e985f4c8dadbb6075ae9e095cd4a8981"
TARGET = LANE / "source" / "id-ID"
CH5_MARKER = b"%\\subsection*{Chapter~\\ref{chap:perp}}"
CH6_MARKER = b"%\\subsection*{Chapter~\\ref{chap:parallel}}"
FROZEN_TARGET_PREFIX_SHA256 = "c6d71d57ad3753572e380e673c6d60f55cb10540dc3c5918f0c66a4f58f64245"
FROZEN_TARGET_CHAPTER_SHA256 = "650ffbc55d59c238dc7c884bc3d0765ecae6e2fdab953d5390fb27ceb09446ed"
FROZEN_TARGET_HINT_SLICE_SHA256 = "d2788d7d1095d838d733533750e3bc6fe4d6de00bad2669be21f67f8988894de"

_shared = runpy.run_path(str(Path(__file__).with_name("qa_ch03.py")))
active_text = _shared["active_text"]
ordered = _shared["ordered"]
ordered_raw = _shared["ordered_raw"]
require_same = _shared["require_same"]
math_surfaces = _shared["math_surfaces"]

ENGLISH_RESIDUE_WORDS = frozenset(
    """
    across all and another any apply arbitrary are argument assume at axiom
    bisector by called center chapter choose circle classroom composition
    conclude construct construction corollary direct distance draw each exercise
    finally fixed follows for from given has have identity if image in indirect
    inequality intersection is lemma let lies line mapping means motion note
    obtuse of on only opposite otherwise perpendicular picture point proof
    proposition reflection repeat respectively result right same secant see
    segment show side straight suppose tangent that the theorem then therefore
    this to triangle use using we with
    """.split()
)
ALLOWED_SHARED_SOURCE_WORDS = frozenset({"birkhoff", "data", "diameter", "sas", "sss"})


def die(message: str) -> None:
    raise SystemExit(f"QA_FAIL: {message}")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def split_slice(data: bytes) -> tuple[bytes, bytes, bytes]:
    if data.count(CH5_MARKER) != 1 or data.count(CH6_MARKER) != 1:
        die("Chapter 5 or Chapter 6 hint marker is not unique")
    left = data.index(CH5_MARKER)
    right = data.index(CH6_MARKER, left + len(CH5_MARKER))
    return data[:left], data[left:right], data[right:]


def require_utf8_lf(name: str, data: bytes) -> str:
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
    if trailing:
        die(f"{name} has trailing whitespace on lines {trailing}")
    return text


def strip_balanced_command_arguments(text: str, commands: tuple[str, ...]) -> str:
    command_pattern = re.compile(
        r"\\(?:" + "|".join(re.escape(command) for command in commands) + r")"
        r"(?:\[[^\]]*\])?\{"
    )
    cursor = 0
    while True:
        match = command_pattern.search(text, cursor)
        if match is None:
            return text
        brace = match.end() - 1
        depth = 1
        index = brace + 1
        while index < len(text) and depth:
            if text[index] == "{" and text[index - 1] != "\\":
                depth += 1
            elif text[index] == "}" and text[index - 1] != "\\":
                depth -= 1
            index += 1
        if depth:
            die(f"unbalanced argument for {match.group(0)!r}")
        text = text[: match.start()] + " " + text[index:]
        cursor = match.start() + 1


def prose_tokens(text: str) -> list[str]:
    checked = active_text(text)
    checked = strip_balanced_command_arguments(
        checked,
        (
            "begin",
            "end",
            "label",
            "ref",
            "pageref",
            "eqref",
            "eqlbl",
            "cite",
            "includegraphics",
            "index",
            "refstepcounter",
            "setcounter",
        ),
    )
    math_patterns = (
        r"\\begin\{(?:align\*?|alignat\*?|gather\*?|multline\*?)\}.*?"
        r"\\end\{(?:align\*?|alignat\*?|gather\*?|multline\*?)\}",
        r"\$\$.*?\$\$",
        r"\\\[.*?\\\]",
        r"(?<!\\)(?<!\$)\$(?!\$).*?(?<!\\)\$(?!\$)",
    )
    for pattern in math_patterns:
        checked = re.sub(pattern, " ", checked, flags=re.DOTALL)
    checked = re.sub(r"\\[A-Za-z@]+\*?", " ", checked)
    checked = checked.translate(str.maketrans({"{": " ", "}": " ", "[": " ", "]": " "}))
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", checked)


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


def require_named_math_exception(
    source: list[str], target: list[str], *, raw: bool
) -> dict[str, object]:
    differences = [
        (tag, source_left, source_right, target_left, target_right)
        for tag, source_left, source_right, target_left, target_right in difflib.SequenceMatcher(
            a=source, b=target, autojunk=False
        ).get_opcodes()
        if tag != "equal"
    ]
    expected_index = 177 if raw else 175
    expected = [("delete", expected_index, expected_index + 1, expected_index, expected_index)]
    if differences != expected or source[expected_index : expected_index + 1] != ["f"]:
        die(f"protected {'raw ' if raw else ''}chapter math surfaces changed outside the named $f$ correction")
    return {
        "authority_count": len(source),
        "target_count": len(target),
        "omitted_authority_surface": "$f$",
        "authority_surface_ordinal": expected_index + 1,
    }


def main() -> None:
    source_chapter_path = AUTHORITY / "perp.tex"
    target_chapter_path = TARGET / "perp.tex"
    source_hints_path = AUTHORITY / "hints.tex"
    target_hints_path = TARGET / "hints.tex"
    for path in (source_chapter_path, target_chapter_path, source_hints_path, target_hints_path):
        if not path.is_file():
            die(f"missing file {path}")

    source_chapter_bytes = source_chapter_path.read_bytes()
    target_chapter_bytes = target_chapter_path.read_bytes()
    source = source_chapter_bytes.decode("utf-8", errors="strict")
    target = require_utf8_lf("target perp.tex", target_chapter_bytes)
    if digest(target_chapter_bytes) != FROZEN_TARGET_CHAPTER_SHA256:
        die("admitted translated Chapter 5 body changed")

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
    expected_topology = {
        "environments": 80,
        "labels": 34,
        "equation_labels": 4,
        "references": 22,
        "citations": 0,
        "graphics": 9,
        "theorem_options": 26,
        "qeds": 7,
    }
    if topology != expected_topology:
        die(f"unexpected authority topology: {topology!r}")

    raw_topology = {
        "authority_commands": len(ordered_raw(r"\\[A-Za-z@]+", source)),
        "target_commands": len(ordered_raw(r"\\[A-Za-z@]+", target)),
        "environments": require_same("ordered raw environments", r"\\(begin|end)\{([^}]+)\}", source, target, raw=True),
        "labels": require_same("ordered raw labels", r"\\label\{([^}]+)\}", source, target, raw=True),
        "equation_labels": require_same("ordered raw equation labels", r"\\eqlbl\{([^}]+)\}", source, target, raw=True),
        "references": require_same("ordered raw references", r"\\(?:ref|pageref|eqref)\{([^}]+)\}", source, target, raw=True),
        "citations": require_same("ordered raw citations", r"\\cite\{([^}]+)\}", source, target, raw=True),
        "graphics": require_same("ordered raw graphics", r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", source, target, raw=True),
        "theorem_options": require_same("ordered raw theorem options", r"\\begin\{thm\}(?:\[([^\]]*)\])?", source, target, raw=True),
        "qeds": require_same("ordered raw proof closures", r"\\qedsf?", source, target, raw=True),
        "authority_comments": len(ordered_raw(r"(?m)^%[^\r\n]*$", source)),
        "target_comments": len(ordered_raw(r"(?m)^%[^\r\n]*$", target)),
    }
    expected_raw_topology = {
        "authority_commands": 509,
        "target_commands": 509,
        "environments": 80,
        "labels": 34,
        "equation_labels": 4,
        "references": 22,
        "citations": 0,
        "graphics": 9,
        "theorem_options": 26,
        "qeds": 7,
        "authority_comments": 1,
        "target_comments": 1,
    }
    if raw_topology != expected_raw_topology:
        die(f"unexpected raw chapter topology: {raw_topology!r}")

    section_pattern = r"\\section(?:\[[^\]]*\])?\{"
    scalar_counts = {
        "sections": len(ordered(section_pattern, source)),
        "index_entries": len(ordered(r"\\index\{", source)),
        "absolute_markers": len(ordered(r"\\begin\{thm\}\[\\abs\]", source)),
        "used_later_markers": len(ordered(r"\\begin\{thm\}\[!\]", source)),
    }
    expected_scalars = {
        "sections": 7,
        "index_entries": 25,
        "absolute_markers": 7,
        "used_later_markers": 7,
    }
    if scalar_counts != expected_scalars:
        die(f"unexpected authority scalar counts: {scalar_counts!r}")
    if len(ordered(section_pattern, target)) != 7 or len(ordered(r"\\index\{", target)) != 25:
        die("translated section or index-entry count changed")

    source_section = r"\section{Direct and indirect motions}"
    target_section = (
        r"\section[Isometri langsung dan tak langsung]"
        r"{Transformasi isometrik langsung dan tak langsung}"
    )
    if source.count(source_section) != 1 or target.count(target_section) != 1:
        die("named direct/indirect-isometry running-title correction is missing or duplicated")
    if len(ordered_raw(r"\\section\[[^\]]+\]\{", source)) != 0:
        die("authority unexpectedly has an optional Chapter 5 section title")
    if len(ordered_raw(r"\\section\[[^\]]+\]\{", target)) != 1:
        die("target must have exactly one optional Chapter 5 section title")

    source_math = math_surfaces(source)
    target_math = math_surfaces(target)
    active_math_exception = require_named_math_exception(source_math, target_math, raw=False)
    source_raw_math = math_surfaces(source, include_comments=True)
    target_raw_math = math_surfaces(target, include_comments=True)
    raw_math_exception = require_named_math_exception(source_raw_math, target_raw_math, raw=True)
    source_correction_text = "then the motion $f$ is called \\index{indirect motion}\\emph{indirect}."
    target_correction_text = (
        "maka transformasi isometrik tersebut disebut "
        "\\index{transformasi isometrik tak langsung}\\emph{tak langsung}."
    )
    if source.count(source_correction_text) != 1 or target.count(target_correction_text) != 1:
        die("named undefined-$f$ prose correction is missing or duplicated")

    source_hint_bytes = source_hints_path.read_bytes()
    target_hint_bytes = target_hints_path.read_bytes()
    _, source_slice, source_suffix = split_slice(source_hint_bytes)
    target_prefix, target_slice, target_suffix = split_slice(target_hint_bytes)
    target_hint = require_utf8_lf("target Chapter 5 hint slice", target_slice)
    source_hint = source_slice.decode("utf-8", errors="strict")
    if digest(target_prefix) != FROZEN_TARGET_PREFIX_SHA256:
        die("frozen translated Chapter 1-4 hint prefix changed")
    if digest(target_slice) != FROZEN_TARGET_HINT_SLICE_SHA256:
        die("admitted translated Chapter 5 hint slice changed")

    hint_topology = {
        "environments": require_same("ordered hint environments", r"\\(begin|end)\{([^}]+)\}", source_hint, target_hint),
        "labels": require_same("ordered hint labels", r"\\label\{([^}]+)\}", source_hint, target_hint),
        "equation_labels": require_same("ordered hint equation labels", r"\\eqlbl\{([^}]+)\}", source_hint, target_hint),
        "references": require_same("ordered hint references", r"\\(?:ref|pageref|eqref)\{([^}]+)\}", source_hint, target_hint),
        "citations": require_same("ordered hint citations", r"\\cite\{([^}]+)\}", source_hint, target_hint),
        "graphics": require_same("ordered hint graphics", r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", source_hint, target_hint),
        "theorem_options": require_same("ordered hint theorem options", r"\\begin\{thm\}(?:\[([^\]]*)\])?", source_hint, target_hint),
        "qeds": require_same("ordered hint proof closures", r"\\qedsf?", source_hint, target_hint),
    }
    expected_hint_topology = {
        "environments": 16,
        "labels": 0,
        "equation_labels": 0,
        "references": 44,
        "citations": 0,
        "graphics": 5,
        "theorem_options": 0,
        "qeds": 0,
    }
    if hint_topology != expected_hint_topology:
        die(f"unexpected hint topology: {hint_topology!r}")

    hint_raw_topology = {
        "commands": require_same("ordered raw hint commands", r"\\[A-Za-z@]+", source_hint, target_hint, raw=True),
        "environments": require_same("ordered raw hint environments", r"\\(begin|end)\{([^}]+)\}", source_hint, target_hint, raw=True),
        "labels": require_same("ordered raw hint labels", r"\\label\{([^}]+)\}", source_hint, target_hint, raw=True),
        "equation_labels": require_same("ordered raw hint equation labels", r"\\eqlbl\{([^}]+)\}", source_hint, target_hint, raw=True),
        "references": require_same("ordered raw hint references", r"\\(?:ref|pageref|eqref)\{([^}]+)\}", source_hint, target_hint, raw=True),
        "citations": require_same("ordered raw hint citations", r"\\cite\{([^}]+)\}", source_hint, target_hint, raw=True),
        "graphics": require_same("ordered raw hint graphics", r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", source_hint, target_hint, raw=True),
        "theorem_options": require_same("ordered raw hint theorem options", r"\\begin\{thm\}(?:\[([^\]]*)\])?", source_hint, target_hint, raw=True),
        "qeds": require_same("ordered raw hint proof closures", r"\\qedsf?", source_hint, target_hint, raw=True),
        "comments": require_same("ordered raw hint comments", r"(?m)^%[^\r\n]*$", source_hint, target_hint, raw=True),
    }
    expected_hint_raw_topology = {
        "commands": 189,
        "environments": 16,
        "labels": 0,
        "equation_labels": 0,
        "references": 45,
        "citations": 0,
        "graphics": 5,
        "theorem_options": 0,
        "qeds": 0,
        "comments": 1,
    }
    if hint_raw_topology != expected_hint_raw_topology:
        die(f"unexpected raw hint topology: {hint_raw_topology!r}")

    source_hint_math = math_surfaces(source_hint)
    target_hint_math = math_surfaces(target_hint)
    if source_hint_math != target_hint_math or len(source_hint_math) != 82:
        die("protected active Chapter 5 hint math surfaces changed")
    source_hint_raw_math = math_surfaces(source_hint, include_comments=True)
    target_hint_raw_math = math_surfaces(target_hint, include_comments=True)
    if source_hint_raw_math != target_hint_raw_math or len(source_hint_raw_math) != 82:
        die("protected raw Chapter 5 hint math surfaces changed")

    exercise_pattern = r"\\begin\{thm\}(?:\[[^\]]*\])?\{[^}]+\}\\label\{(ex:[^}]+)\}"
    source_exercises = ordered(exercise_pattern, source)
    target_exercises = ordered(exercise_pattern, target)
    hint_header_pattern = r"\\parbf\{\\ref\{([^}]+)\}(?:\+\\ref\{([^}]+)\})?"
    source_hint_headers = ordered(hint_header_pattern, source_hint)
    target_hint_headers = ordered(hint_header_pattern, target_hint)
    flattened_hint_ids = [item for pair in target_hint_headers for item in pair if item]
    if source_exercises != target_exercises or source_hint_headers != target_hint_headers:
        die("ordered Chapter 5 exercise or hint-header identity changed")
    if len(target_exercises) != 18 or len(target_hint_headers) != 17:
        die("unexpected Chapter 5 exercise or hint-block count")
    if flattened_hint_ids != target_exercises:
        die("Chapter 5 exercise-to-hint closure is incomplete or out of order")
    shared_hint_headers = [list(pair) for pair in target_hint_headers if pair[1]]
    if shared_hint_headers != [["ex:tangent", "ex:tangent-circle"]]:
        die("the exact shared tangent-construction hint closure changed")

    body_english_hits = require_no_active_english("target perp.tex", target)
    hint_english_hits = require_no_active_english("target Chapter 5 hints", target_hint)
    body_source_overlap = require_no_untranslated_source_overlap(
        "target perp.tex", source, target
    )
    hint_source_overlap = require_no_untranslated_source_overlap(
        "target Chapter 5 hints", source_hint, target_hint
    )

    # Later chapters are owned by their own source-order QA. Record whether the
    # current suffix is still authority-identical, but do not freeze its hash;
    # a subsequently admitted Chapter 6 translation must not invalidate Ch5.
    later_suffix_matches_authority = target_suffix == source_suffix

    report = {
        "schema": "o004-ch05-qa-v0",
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
            "current_later_suffix_matches_authority": later_suffix_matches_authority,
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
        "chapter_topology": topology,
        "chapter_raw_topology": raw_topology,
        "scalar_counts": scalar_counts,
        "chapter_math_surfaces": {
            "active": active_math_exception,
            "raw": raw_math_exception,
        },
        "named_editorial_correction": {
            "id": "o004.petrunin.correction.ch05.undefined-f",
            "authority_line": 297,
            "authority_token_omitted": "$f$",
            "reason": "The authority calls the motion f without defining f; the target says 'the transformation' instead.",
            "mathematics_changed": False,
            "only_permitted_math_surface_difference": True,
        },
        "named_layout_correction": {
            "id": "o004.petrunin.correction.ch05.direct-motion-running-head",
            "authority_line": 284,
            "target_line": 284,
            "target_running_title": "Isometri langsung dan tak langsung",
            "target_visible_title": "Transformasi isometrik langsung dan tak langsung",
            "reason": "The shorter optional running title prevents a running-head/page-number collision while preserving the full visible section title.",
            "mathematics_changed": False,
            "identifiers_changed": False,
            "section_order_changed": False,
        },
        "exercise_hint_closure": {
            "exercise_count": len(target_exercises),
            "hint_block_count": len(target_hint_headers),
            "covered_exercise_count": len(flattened_hint_ids),
            "ordered_exercise_ids": target_exercises,
            "shared_hint_headers": shared_hint_headers,
            "complete": True,
        },
        "hint_topology": hint_topology,
        "hint_raw_topology": hint_raw_topology,
        "hint_math_surfaces": {
            "active": len(source_hint_math),
            "raw": len(source_hint_raw_math),
        },
    }
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
