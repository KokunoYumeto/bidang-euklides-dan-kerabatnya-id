# Translation cursor

Updated: 2026-08-22

Current admitted unit IDs: `o004.petrunin.front-ch01`, `o004.petrunin.ch02`,
`o004.petrunin.ch03`, `o004.petrunin.ch04`, `o004.petrunin.ch05`

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
17. `perp.tex` — complete Bab 5, seven sections, eight results, eighteen
    exercises, and nine body figures; 17,849 bytes, SHA-256
    `650ffbc55d59c238dc7c884bc3d0765ecae6e2fdab953d5390fb27ceb09446ed`.
18. `hints.tex` — complete Chapter 5 slice, target lines 396-561, seventeen
    author hint blocks covering eighteen exercises and five hint figures;
    5,770 bytes, SHA-256
    `d2788d7d1095d838d733533750e3bc6fe4d6de00bad2669be21f67f8988894de`.
    The final block is shared by `ex:tangent` and `ex:tangent-circle`.
19. Chapter 5 backend: eight unit rows, eight result records, eighteen
    exercises, seventeen hint records, fourteen admitted figure descriptions,
    26 concept/dependency rows, one build artifact, one QA event, and five
    admitted bounded-correction records. The catalog has 201 records and 122
    relations with zero dangling endpoints.
20. The Section E running head uses the optional short title `Isometri
    langsung dan tak langsung` to avoid a page-number collision while the full
    visible title is unchanged. One undefined source `$f$` is rendered as the
    already-introduced isometric transformation; three further wording
    clarifications change no mathematics or identifiers.

Current production boundary: immediately before Chapter 6 (`similar.tex`) and
at the Chapter 6 hint marker on target line 562. The translated hint prefix
before that marker is 19,859 bytes, SHA-256
`f2d9f4153457a500482d1f480c07a18d62d2ac2440138f9cf927f93ae1c522b0`.
Chapter 6+ remains byte-identical to authority.

Chapter 6 authority and current target `similar.tex` are identical: 10,655
bytes, SHA-256
`75dd3b1b3eca732b2744a7d61f37356c6078cf57f59f8bd5413f6de8205b8d1a`.
Its exact authority hint slice is source lines 562-607, 2,092 bytes, SHA-256
`ccda006b21c6fac93216f50518fc938a0c1825ae70b66182afdac63793eb4808`.
The Chapter 7+ suffix is 70,880 bytes, SHA-256
`5cb477a32870e20435d7cb6978a361b33ddead279f26dbec5814f57b4100d474`.

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

Chapter 5 admission evidence is `qa/CH05_ADMISSION_20260822.md`; its two fresh
full-context builds are 207 pages, 2,965,782 bytes, SHA-256
`6ca6402e66b5ab0a048697bf0478a00548e1c5a64096d605fbd95947c21994ee`.

Immediate cursor action: translate Chapter 6 (`similar.tex`) and its matching
contiguous hints, then extend the backend and perform one bounded gate.
Translation remains dominant; do not reopen the admitted Chapters 1-5
boundary.
