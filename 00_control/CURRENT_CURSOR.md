# Translation cursor

Updated: 2026-08-21

Current admitted unit IDs: `o004.petrunin.front-ch01`, `o004.petrunin.ch02`,
`o004.petrunin.ch03`

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
7. `axioms.tex` — complete Bab 2, six sections, eight results, seven exercises,
   and five figures; 13,472 bytes, SHA-256
   `e44a5934711c4871289ec82a1c8e4e2acb98b66c18e1e5a3bca378ecabaa3a6d`.
8. `hints.tex` — complete Chapter 2 slice, target lines 234–288, seven matching
   hints; 2,249 bytes, SHA-256
   `cb449316a820b09ef386feefa61d3b57b05b46d90929ea3e87a4c78e7913c066`.
9. Chapter 2 backend records and visual descriptions for all five figures.
10. `half-planes.tex` — complete Bab 3, five sections, 12 results, nine
    exercises and 13 figures; 16,419 bytes, SHA-256
    `e7b3b3e4858302e4c361fe47056c9285d4881c5a2c8ec4cd2332629504f698d8`.
11. `hints.tex` — complete Chapter 3 slice, target lines 289-359, eight author
    hints; 3,053 bytes, SHA-256
    `d5f75149bd2fdbc993d00c0a8d4c8c659846374c9da60d459be0871bbe6f40d4`.
    Exercise `ex:angle-measures` has no source hint.
12. Chapter 3 backend: five section rows, 12 result records, nine exercises,
    eight hint links, 13 figure descriptions and 16 concept/dependency rows.

Current production boundary: immediately before Chapter 4 (`cong.tex`) and at
the Chapter 4 hint marker on target line 360. The translated hint prefix before
that marker is 12,488 bytes, SHA-256
`2ff27e2ca3f9c53f94dec954a4c07560787e9a61ed854d1a0720e0018152abe1`.
Everything from the marker onward remains byte-identical to authority: 79,713
bytes, SHA-256
`d5cd7c02bde78f749f657812b4c48a6d652c1d5820cc2cbe7fe937f0d0711aa5`.

Chapter 4 authority and current target `cong.tex` are identical: 12,527 bytes,
SHA-256
`7ad021c768316aafec871003fdcb7f5daff4a16d42c378366dfe8dc913df4f4f`.

Artifact boundary: the locally admitted 19-page partial reader has SHA-256
`1a6909ab8c315fe2529d9267c3d539def1e1f68667bc432d8bf40059dd91a452`.

Publication state: the GitHub repository and release remain private. Zenodo
record `22044358`, DOI `10.5281/zenodo.22044358`, is the same published record
with its five files restricted; see
`00_control/PUBLICATION_RECEIPT_UNIT001.json`.

Chapter 3 admission evidence is `qa/CH03_ADMISSION_20260821.md`; its two fresh
full-context builds have SHA-256
`94057485cd2f16d55b1adff8d0e53583584c8330e2b51a08d906ef1e83dc6117`.

Immediate cursor action: translate Chapter 4 (`cong.tex`) and its matching
contiguous hints, then extend the backend and perform one bounded gate.
Translation remains dominant; do not reopen the admitted Chapters 1-3
boundary.
