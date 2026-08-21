# Translation cursor

Updated: 2026-08-21

Current admitted unit ID: `o004.petrunin.front-ch01`

Completed and frozen:

1. `title.tex` — localized title, subtitle, license/change notice, attribution,
   and non-endorsement.
2. `intro.tex` — complete Prakata.
3. `metric.tex` — complete Bab 1, `chap:metr`, including all 16 exercises.
4. `hints.tex` — exact contiguous Chapter 1 block beginning with
   `ex:dist-square` and ending with `ex:ncong` (target lines 13–231).
5. `locale-id.tex` and the narrow `all-lectures.tex` locale hooks.
6. Backend records for the unit, 10 sections, 16 exercise–hint pairs, 18 core
   concepts, and four figure descriptions.

Stop boundary: immediately before Chapter 2 (`axioms.tex`) and immediately
before the Chapter 2 `\refstepcounter{chapter}` transition in `hints.tex`.
The Chapter 2+ hint suffix is byte-identical to authority: 84,364 bytes,
SHA-256 `49406336c41b960c0a0e3686491a97b0602f9e198c4378a161dcfb56b05d3380`.

Artifact boundary: the locally admitted 19-page partial reader has SHA-256
`1a6909ab8c315fe2529d9267c3d539def1e1f68667bc432d8bf40059dd91a452`.

Immediate cursor action: publish/verify Unit 001 on the edition GitHub and
Zenodo, then translate Chapter 2 (`axioms.tex`) followed by its seven matching
hint blocks. Translation remains dominant; do not reopen settled authority or
repeat the Unit 001 QA loop.
