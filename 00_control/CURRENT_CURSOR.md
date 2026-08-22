# Translation cursor

Updated: 2026-08-22

Current admitted unit IDs: `o004.petrunin.front-ch01`, `o004.petrunin.ch02`,
`o004.petrunin.ch03`, `o004.petrunin.ch04`

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
13. `cong.tex` — complete Bab 4, six sections, four neutral-geometry results,
    five labeled exercises, one unlabeled worked construction problem, and ten
    active figures; 13,622 bytes, SHA-256
    `70cbc1809520da16814159a32021a66ebb48db56190b3a638af2205436282b43`.
14. `hints.tex` — complete Chapter 4 slice, target lines 360-395, five
    matching hints; 1,601 bytes, SHA-256
    `85eb2f743180e984948a8fe094b5a7f645135e47a7a5f1e9d8cb8ac86fa69c5c`.
15. Chapter 4 backend: seven unit rows, four result records, five exercises
    and hints, one synthetic ID for the unlabeled problem, ten figure
    descriptions, and 15 concept/dependency rows. The catalog has 140 records
    and 87 relations with zero dangling endpoints.
16. The construction sequence `pic-445` through `pic-449` is deliberately
    reflowed from one overflowing side wrap into a visually admitted two-row
    sequence. Figures, order, text, formulas, labels and references are
    unchanged.

Current production boundary: immediately before Chapter 5 (`perp.tex`) and at
the Chapter 5 hint marker on target line 396. The translated hint prefix before
that marker is 14,089 bytes, SHA-256
`c6d71d57ad3753572e380e673c6d60f55cb10540dc3c5918f0c66a4f58f64245`.
Everything from the marker onward remains byte-identical to authority: 78,262
bytes, SHA-256
`c9d2a983be56f8d1c78b6ad06ce6ac6e468b4b74df161d8fac79c8e056eecce4`.

Chapter 5 authority and current target `perp.tex` are identical: 16,499 bytes,
SHA-256
`c5be147e0249d3c7ffe5f2432cdd11b5e686e808927661de57614c55bfc28f91`.
Its exact authority hint slice is source lines 396-561, 5,290 bytes, SHA-256
`80f7d0508c31e8a2dbdf3826814658b98ba551ac427f1d6a3955311f4502044e`.

Artifact boundary: the locally admitted 19-page partial reader has SHA-256
`1a6909ab8c315fe2529d9267c3d539def1e1f68667bc432d8bf40059dd91a452`.

Publication state: the GitHub repository and release remain private. Zenodo
record `22044358`, DOI `10.5281/zenodo.22044358`, is the same published record
with its five files restricted; see
`00_control/PUBLICATION_RECEIPT_UNIT001.json`.

Chapter 3 admission evidence is `qa/CH03_ADMISSION_20260821.md`; its two fresh
full-context builds have SHA-256
`94057485cd2f16d55b1adff8d0e53583584c8330e2b51a08d906ef1e83dc6117`.

Chapter 4 admission evidence is `qa/CH04_ADMISSION_20260822.md`; its two fresh
full-context builds are 205 pages, 2,962,911 bytes, SHA-256
`1ff91aa4ff95880980237060624fe95022d6664b8cc68180859d266a9e5cc92e`.

Immediate cursor action: translate Chapter 5 (`perp.tex`) and its matching
contiguous hints, then extend the backend and perform one bounded gate.
Translation remains dominant; do not reopen the admitted Chapters 1-4
boundary.
