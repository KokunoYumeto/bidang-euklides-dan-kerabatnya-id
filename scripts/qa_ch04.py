#!/usr/bin/env python3
"""Fail-closed structural QA for O004 Chapter 4 and its exact hint slice."""

from __future__ import annotations

import hashlib
import json
import runpy
import sys
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
AUTHORITY = LANE / "source" / "upstream" / "birkhoff-0b0858e1e985f4c8dadbb6075ae9e095cd4a8981"
TARGET = LANE / "source" / "id-ID"
CH4_MARKER = b"%\\subsection*{Chapter~\\ref{chap:cong}}"
CH5_MARKER = b"%\\subsection*{Chapter~\\ref{chap:perp}}"
FROZEN_TARGET_PREFIX_SHA256 = "2ff27e2ca3f9c53f94dec954a4c07560787e9a61ed854d1a0720e0018152abe1"
FROZEN_TARGET_CHAPTER_SHA256 = "70cbc1809520da16814159a32021a66ebb48db56190b3a638af2205436282b43"
FROZEN_TARGET_SLICE_SHA256 = "85eb2f743180e984948a8fe094b5a7f645135e47a7a5f1e9d8cb8ac86fa69c5c"

_shared = runpy.run_path(str(Path(__file__).with_name("qa_ch03.py")))
active_text = _shared["active_text"]
ordered = _shared["ordered"]
ordered_raw = _shared["ordered_raw"]
require_same = _shared["require_same"]
math_surfaces = _shared["math_surfaces"]


def die(message: str) -> None:
    raise SystemExit(f"QA_FAIL: {message}")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def split_slice(data: bytes) -> tuple[bytes, bytes, bytes]:
    try:
        left = data.index(CH4_MARKER)
        right = data.index(CH5_MARKER, left + len(CH4_MARKER))
    except ValueError as error:
        die(f"hint boundary missing: {error}")
    return data[:left], data[left:right], data[right:]


def main() -> None:
    source_chapter_path = AUTHORITY / "cong.tex"
    target_chapter_path = TARGET / "cong.tex"
    source_hints_path = AUTHORITY / "hints.tex"
    target_hints_path = TARGET / "hints.tex"
    for path in (source_chapter_path, target_chapter_path, source_hints_path, target_hints_path):
        if not path.is_file():
            die(f"missing file {path}")

    source = source_chapter_path.read_text(encoding="utf-8")
    target = target_chapter_path.read_text(encoding="utf-8")
    if digest(target_chapter_path.read_bytes()) != FROZEN_TARGET_CHAPTER_SHA256:
        die("admitted translated Chapter 4 body changed")
    source_environments = ordered(r"\\(begin|end)\{([^}]+)\}", source)
    target_environments = ordered(r"\\(begin|end)\{([^}]+)\}", target)
    semantic_source_environments = [pair for pair in source_environments if pair[1] not in {"wrapfigure", "center"}]
    semantic_target_environments = [pair for pair in target_environments if pair[1] not in {"wrapfigure", "center"}]
    if semantic_source_environments != semantic_target_environments:
        die("ordered semantic environments changed")
    layout_reflow = {
        "authority_wrapfigures": sum(pair == ("begin", "wrapfigure") for pair in source_environments),
        "target_wrapfigures": sum(pair == ("begin", "wrapfigure") for pair in target_environments),
        "authority_centers": sum(pair == ("begin", "center") for pair in source_environments),
        "target_centers": sum(pair == ("begin", "center") for pair in target_environments),
    }
    if layout_reflow != {
        "authority_wrapfigures": 6,
        "target_wrapfigures": 5,
        "authority_centers": 0,
        "target_centers": 1,
    }:
        die(f"unexpected construction-panel reflow: {layout_reflow!r}")

    topology = {
        "environments": len(source_environments),
        "labels": require_same("ordered labels", r"\\label\{([^}]+)\}", source, target),
        "equation_labels": require_same("ordered equation labels", r"\\eqlbl\{([^}]+)\}", source, target),
        "references": require_same("ordered references", r"\\(?:ref|pageref|eqref)\{([^}]+)\}", source, target),
        "citations": require_same("ordered citations", r"\\cite\{([^}]+)\}", source, target),
        "graphics": require_same("ordered graphics", r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", source, target),
        "theorem_options": require_same("ordered theorem options", r"\\begin\{thm\}(?:\[([^\]]*)\])?", source, target),
        "qeds": require_same("ordered proof closures", r"\\qedsf?", source, target),
    }
    expected = {
        "environments": 42,
        "labels": 10,
        "equation_labels": 3,
        "references": 24,
        "citations": 0,
        "graphics": 10,
        "theorem_options": 10,
        "qeds": 5,
    }
    if topology != expected or len(target_environments) != expected["environments"]:
        die(f"unexpected authority topology: {topology!r}")

    scalar_counts = {
        "sections": len(ordered(r"\\section\{", source)),
        "index_entries": len(ordered(r"\\index\{", source)),
        "absolute_markers": len(ordered(r"\\begin\{thm\}\[\\abs\]", source)),
        "used_later_markers": len(ordered(r"\\begin\{thm\}\[!\]", source)),
    }
    expected_scalars = {
        "sections": 6,
        "index_entries": 7,
        "absolute_markers": 4,
        "used_later_markers": 1,
    }
    if scalar_counts != expected_scalars:
        die(f"unexpected authority scalar counts: {scalar_counts!r}")
    if len(ordered(r"\\section\{", target)) != 6 or len(ordered(r"\\index\{", target)) != 7:
        die("translated section or index-entry count changed")

    raw_topology = {
        "authority_commands": len(ordered_raw(r"\\[A-Za-z@]+", source)),
        "target_commands": len(ordered_raw(r"\\[A-Za-z@]+", target)),
        "labels": require_same("ordered raw labels", r"\\label\{([^}]+)\}", source, target, raw=True),
        "references": require_same("ordered raw references", r"\\(?:ref|pageref|eqref)\{([^}]+)\}", source, target, raw=True),
        "graphics": require_same("ordered raw graphics", r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", source, target, raw=True),
        "authority_comments": len(ordered_raw(r"(?m)^%[^\r\n]*$", source)),
        "comments": len(ordered_raw(r"(?m)^%[^\r\n]*$", target)),
    }
    expected_raw = {
        "authority_commands": 336,
        "target_commands": 340,
        "labels": 11,
        "references": 24,
        "graphics": 11,
        "authority_comments": 11,
        "comments": 11,
    }
    if raw_topology != expected_raw:
        die(f"unexpected raw chapter topology: {raw_topology!r}")

    source_math = math_surfaces(source)
    target_math = math_surfaces(target)
    if source_math != target_math:
        for index, pair in enumerate(zip(source_math, target_math), start=1):
            if pair[0] != pair[1]:
                die(f"protected active chapter math surface {index} changed")
        die("protected active chapter math-surface count changed")
    source_raw_math = math_surfaces(source, include_comments=True)
    target_raw_math = math_surfaces(target, include_comments=True)
    if source_raw_math != target_raw_math:
        die("protected raw chapter math surfaces changed")
    if len(source_math) != 166 or len(source_raw_math) != 180:
        die("unexpected authority chapter math-surface count")

    source_hint_bytes = source_hints_path.read_bytes()
    target_hint_bytes = target_hints_path.read_bytes()
    _, source_slice, source_suffix = split_slice(source_hint_bytes)
    target_prefix, target_slice, target_suffix = split_slice(target_hint_bytes)
    if digest(target_prefix) != FROZEN_TARGET_PREFIX_SHA256:
        die("frozen translated Chapter 1-3 hint prefix changed")
    if digest(target_slice) != FROZEN_TARGET_SLICE_SHA256:
        die("admitted translated Chapter 4 hint slice changed")

    # Later chapters are owned by their own source-order QA. Record whether the
    # current suffix is still authority-identical, but do not freeze its hash;
    # an admitted Chapter 5+ translation must not invalidate Chapter 4.
    later_suffix_matches_authority = target_suffix == source_suffix

    source_hint = source_slice.decode("utf-8")
    target_hint = target_slice.decode("utf-8")
    hint_topology = {
        "commands_raw": require_same("ordered raw hint commands", r"\\[A-Za-z@]+", source_hint, target_hint, raw=True),
        "references_raw": require_same("ordered raw hint references", r"\\(?:ref|pageref|eqref)\{([^}]+)\}", source_hint, target_hint, raw=True),
        "comments": len(ordered_raw(r"(?m)^%[^\r\n]*$", target_hint)),
    }
    source_hint_math = math_surfaces(source_hint, include_comments=True)
    target_hint_math = math_surfaces(target_hint, include_comments=True)
    if source_hint_math != target_hint_math:
        die("protected raw Chapter 4 hint math surfaces changed")
    if hint_topology != {"commands_raw": 58, "references_raw": 8, "comments": 2}:
        die(f"unexpected hint topology: {hint_topology!r}")
    if len(source_hint_math) != 35:
        die(f"unexpected hint math-surface count: {len(source_hint_math)}")

    report = {
        "schema": "o004-ch04-qa-v0",
        "status": "pass",
        "authority": {
            "chapter_bytes": source_chapter_path.stat().st_size,
            "chapter_sha256": digest(source_chapter_path.read_bytes()),
            "hint_slice_bytes": len(source_slice),
            "hint_slice_sha256": digest(source_slice),
            "later_suffix_bytes": len(source_suffix),
            "later_suffix_sha256": digest(source_suffix),
        },
        "target": {
            "chapter_bytes": target_chapter_path.stat().st_size,
            "chapter_sha256": digest(target_chapter_path.read_bytes()),
            "hint_slice_bytes": len(target_slice),
            "hint_slice_sha256": digest(target_slice),
            "whole_hints_sha256": digest(target_hint_bytes),
            "frozen_prefix_bytes": len(target_prefix),
            "frozen_prefix_sha256": digest(target_prefix),
            "current_later_suffix_bytes": len(target_suffix),
            "current_later_suffix_sha256": digest(target_suffix),
            "current_later_suffix_matches_authority": later_suffix_matches_authority,
        },
        "chapter_topology": topology,
        "layout_reflow": layout_reflow,
        "chapter_raw_topology": raw_topology,
        "scalar_counts": scalar_counts,
        "chapter_math_surfaces": len(source_math),
        "chapter_math_surfaces_raw": len(source_raw_math),
        "hint_topology": hint_topology,
        "hint_math_surfaces_raw": len(source_hint_math),
    }
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
