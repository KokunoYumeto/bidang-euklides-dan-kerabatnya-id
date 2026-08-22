# Translation cursor

Updated: 2026-08-22

Current admitted unit IDs: `o004.petrunin.front-ch01`, `o004.petrunin.ch02`,
`o004.petrunin.ch03`, `o004.petrunin.ch04`, `o004.petrunin.ch05`,
`o004.petrunin.ch06`, `o004.petrunin.ch07`

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
21. `similar.tex` — complete Bab 6, four sections, four results, eight
    exercises, and four figures; 11,244 bytes, SHA-256
    `23c609c66ae26e627425bfd196454b4cdc7a7b11d8398265786c9234ddcdd201`.
22. `hints.tex` — complete Chapter 6 slice, target lines 562–607, eight
    matching authored hints; 2,353 bytes, SHA-256
    `38cdafe5f4fcbb7440d4ac9cfdb1bb6c1b0925d37de24dc0996da61de0e82273`.
23. Chapter 6 backend: five unit-order rows, four result records, eight
    exercise–hint mappings, four admitted figure descriptions, 22
    concept/dependency rows, four correction/source-note records, one build
    artifact, and one QA event. The catalog has 240 records and 139 relations
    with zero dangling endpoints; concept mappings remain pending their
    separate backend review.
24. The inherited `chap:parallel`, `thm:signs-of-triug`, `k=1`
    distinctness inconsistency, and inactive `\triange` spellings are recorded
    without source repair. The Ptolemy proof's explicit left/right-side wording
    is admitted as a nonmathematical localization clarification.
25. `parallel.tex` — complete Bab 7, six sections, eight results, twenty-one
    top-level exercises with three labeled subparts, and thirteen body figures;
    22,352 bytes, SHA-256
    `3459de730c56922fe4a9e30781d3a12ce1671c735423f5eaed12175d9d5d5385`.
26. `hints.tex` — complete Chapter 7 slice, target lines 608–792,
    twenty-one authored hint blocks and two hint figures; 6,855 bytes,
    SHA-256
    `1a914474041c1a1fb05a3b7f2cd46c8da279431de7d08e39ed9f72e770532280`.
    The labeled subpart `ex:line-coord:parameter` is covered by its parent
    `ex:line-coord` hint.
27. Chapter 7 backend: seven unit-order rows, eight result records,
    twenty-four exercise/subpart rows, twenty-one top-level hint mappings,
    fifteen admitted figure descriptions, twenty-nine concept/dependency rows,
    twelve correction/source/localization records, one build artifact, and one
    QA event. The catalog has 309 records and 179 relations with zero dangling
    endpoints; concept mappings remain `mapped-pending-qa`.
28. Four high-confidence mathematical repairs, one index correction, one
    layout-only reflow, and bounded Indonesian fluency normalization are
    admitted and disclosed in `qa/CH07_ADMISSION_20260822.md`. Legacy and
    misspelled source IDs and the inactive signed-`pi/4` material remain
    preserved.

Current production boundary: immediately before Chapter 8 (`triangle.tex`) and
at its hint marker on target line 793. The translated hint prefix through
Chapter 7 is 29,067 bytes, SHA-256
`46c00e637aa948158b9e3ac7a5b38379bb367ec9c90f2c560d010f151c3b814c`.

Chapter 8 authority and current target `triangle.tex` are byte-identical:
14,691 bytes, SHA-256
`95e4d8050e38af8da76ed24c48277550bfe7cdf8c1a7274887d6f853e4429948`.
Its exact authority hint slice is target lines 793–871, 3,032 bytes, SHA-256
`9094d0267cd658585f398bf029934f4a3af9eec2069ecfd18451fa5a3fc2ad8d`.
The translated prose action begins after the preserved marker/counter lines,
at line 797, and ends at line 870. The Chapter 9+ suffix begins at line 872 and
is byte-identical to authority: 61,744 bytes, SHA-256
`2ea9859cf7143c6f56069ad802df4c1e295839f8729408a0f72ee8884e205afd`.
Chapter 8 contains thirteen exercises, thirteen directly matching authored
hint blocks, nine body figures, and no hint figures. Preserve the immutable
`ex:midle` and `ex:ext-disect` spellings and record the source's
proposition/lemma and external/exterior-bisector terminology inconsistencies.

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

Chapter 6 admission evidence is `qa/CH06_ADMISSION_20260822.md`; its two fresh
full-context builds are 208 pages, 2,967,413 bytes, SHA-256
`4c4e1b9a27b17d274834c4b828bc764519d018c73a0449842098b1e2d937146a`.

Chapter 7 admission evidence is `qa/CH07_ADMISSION_20260822.md`; its two fresh
full-context builds are 208 pages, 2,968,464 bytes, SHA-256
`7fa21a42a1cdf4d78db3b1b1ae9d8db3e58ae50c3091264f4402f4b54aa0b448`.

Immediate cursor action: translate Chapter 8 (`triangle.tex`) and its matching
contiguous hints, then extend the backend and perform one bounded gate.
Translation remains dominant; do not reopen the admitted Chapters 1-7
boundary.
