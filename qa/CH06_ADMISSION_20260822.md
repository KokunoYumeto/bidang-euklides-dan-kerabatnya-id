# Chapter 6 admission — 2026-08-22

## Boundary

Complete Bab 6, *Segitiga sebangun*, and its exact authored hint slice are
admitted. The unit contains four sections, four result blocks, eight exercises,
four body figures, and eight matching author hint blocks. The next source-order
cursor is Chapter 7, `parallel.tex`.

Authority `similar.tex` is 10,655 bytes, SHA-256
`75dd3b1b3eca732b2744a7d61f37356c6078cf57f59f8bd5413f6de8205b8d1a`.
The admitted target is 11,244 bytes, SHA-256
`23c609c66ae26e627425bfd196454b4cdc7a7b11d8398265786c9234ddcdd201`.
The authority hint slice is 2,092 bytes, SHA-256
`ccda006b21c6fac93216f50518fc938a0c1825ae70b66182afdac63793eb4808`;
the target slice is 2,353 bytes, SHA-256
`38cdafe5f4fcbb7440d4ac9cfdb1bb6c1b0925d37de24dc0996da61de0e82273`.
The complete target `hints.tex` is 93,092 bytes, SHA-256
`db4f4b097ed2f39b1c5340a93037b4f3dd781a9a9d34610a51e2fdf77e5bbd69`.
The frozen Chapter 1–5 prefix is 19,859 bytes, SHA-256
`f2d9f4153457a500482d1f480c07a18d62d2ac2440138f9cf927f93ae1c522b0`;
the Chapter 7+ suffix remains byte-identical to authority at 70,880 bytes,
SHA-256
`5cb477a32870e20435d7cb6978a361b33ddead279f26dbec5814f57b4100d474`.

## Structural and language gate

`scripts/qa_ch06.py` passes and writes
`qa/CH06_STRUCTURAL_QA_20260822.json`. Their SHA-256 values are
`5e27d7ba91cacef2d36e8293829b8bec61d95c6c94168f3b19c45502ed9f3024`
and
`bd765af10abc67d52b869ac3a080618fbfaddc34f30f8dcd2e398bb9202b77c2`.
Ordered active topology agrees with authority: 44 environment boundaries, 12
labels, four equation labels, 17 references, two citations, four graphics, 12
theorem options, and three proof closures. Raw topology also agrees exactly:
46 environment boundaries, 13 labels, four equation labels, 17 references,
two citations, four graphics, 13 theorem options, three proof closures, 348
commands, and five comments. All 143 active and 156 raw body math surfaces are
preserved. The hint slice retains 10 active references, 12 raw references, 88
commands, two comments, and 22 active/23 raw math surfaces. All eight ordered
exercise IDs have exactly one authored hint block. Active Indonesian prose has
no untranslated-source overlap or English residue.

The source's legacy chapter label `chap:parallel`, theorem-label spelling
`thm:signs-of-triug`, `ex:k*triangle` distinctness inconsistency at `k=1`, and
inactive commented `\triange` spellings remain unchanged and are documented.
The Ptolemy proof explicitly names the left and right sides to which its equal
angles are added. This bounded wording clarification changes no formula,
claim, identifier, reference, or proof dependency.

## Deterministic build and visual gate

Fresh directories `build/ch06-final-a-20260822` and
`build/ch06-final-b-20260822` produced identical 208-page PDFs:

- 2,967,413 bytes;
- SHA-256
  `4c4e1b9a27b17d274834c4b828bc764519d018c73a0449842098b1e2d937146a`;
- page size 432 × 648 points, PDF 1.5, unencrypted and untagged;
- 224 generated MetaPost files with zero cross-build hash mismatches;
- normalized CC badge SHA-256
  `7167e45adcc360f116b77210a2e452308e2b8fffd84106f1ea69045cb5be9928`;
- normalized H2checkers SHA-256
  `61a45915d8630a8df63bd9b9ecb095ab9fe6d6671b3360f814bea97ce9a8d885`.

The converged log has zero undefined references, zero undefined citations, and
no fatal or undefined-control error. It has 51 overfull and 32 underfull boxes
globally plus the inherited group warning. Chapter 6 contributes six overfull
and one underfull diagnostic. PDF pages 49–54 and hint page 188 were rendered
at 150 dpi and inspected independently and by the production owner. All four
figures are clear and correctly wrapped; there is no clipping, overlap,
off-page content, header/page-number collision, broken glyph, or unreadable
line. The diagnostics are visually harmless. Page 54's open remainder is the
genuine chapter ending. Hint page 188 cleanly separates admitted Indonesian
Chapter 6 hints from the English Chapter 7 full-context QA boundary.

The full-context PDF contains English Chapter 7+ material and is private QA
evidence, not a reader release. It remains untagged; semantic HTML/EPUB is a
required later accessibility layer.

## Backend gate

The additive backend has 240 unique records and 139 unique relations with zero
dangling endpoints; JSON Schema validation passes. Chapter 6 contributes five
unit-order rows, four result records, eight exercise–hint mappings, four
admitted figure descriptions, 22 concept/dependency rows, four correction or
source-note records, one private full-context build artifact, and one QA event.
The 22 concept rows deliberately remain `mapped-pending-qa`; reader, result,
exercise, hint, figure, and build admission is complete.

CSV imports verify UTF-8 without BOM, LF endings, terminal newlines, exact
headers, expected row/column counts, and unique primary IDs. Canonical hashes
are:

- `catalog-v0.json`: `a47a99d8d3df589c17c11335a2231398dbd9043553d950479a8390201e9156c9`;
- `unit-order-v0.csv`: `2e9cfbb9cdbf2c9de7b3ce4d3dd4471d76222b86f14203a447388a0b33c4a92d`;
- `exercise-hints-v0.csv`: `3287800bc32796b372ff5a28030e459b59f4b1102ec6e2339bcd0bd3fa5037eb`;
- `figure-descriptions-id-v0.csv`: `dfd5069eeba2e9cddfd7a826a226ddbc2b65dc7b473a0c467b95ee631ae46fa8`;
- `concepts-ch06-id-v0.csv`: `8ff5b6abb4499c332c3c90bfd3913ea7a25f3709578e49262e7adab69ad240f7`.

Admission decision: pass. Advance to Chapter 7 without reopening Chapters
1–6. Keep GitHub private and Zenodo files restricted; make no Zenodo version at
this boundary.
