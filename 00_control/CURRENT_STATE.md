# O004 / C100 — current state

Updated: 2026-08-21

Status: active Bahasa Indonesia reader production. The front matter, Chapters
1-3, and their exact available hint slices are complete, structurally verified,
and visually admitted. The GitHub repository and Unit 001 release are private.
Zenodo record `22044358`, DOI
`10.5281/zenodo.22044358`, retains all five files with restricted access. The
whole book is not complete; the cursor is immediately before Chapter 4.

The admitted core is Anton Petrunin, *Euclidean Plane and Its Relatives: A
Minimalist Introduction*. The labeled publication witness is arXiv
`1302.1630v25` (third edition, tenth printing, revised 2025-07-07). Production
uses the later official author-repository snapshot
`0b0858e1e985f4c8dadbb6075ae9e095cd4a8981` intentionally, with v25 retained as
the immutable rendered-edition witness. The later commit is not described as a
new printing or edition.

The body-only derivative is admitted. The separate `cover/` directory and its
two proprietary P22 fonts are excluded. This release boundary may include the
translated overlay, backend, controls, scripts, and generated reader. It must
not redistribute the unresolved MetaPost generator closure. Reproduction can
fetch the pinned official archive, remove `cover/`, and apply the overlay.

## Admitted reader boundaries

Unit `o004.petrunin.front-ch01` contains:

- localized title and CC BY-SA 4.0 attribution/change/non-endorsement notice;
- complete Prakata (`intro.tex`);
- complete Bab 1, Pendahuluan (`metric.tex`);
- all 16 Chapter 1 exercises and all 16 current-master hint blocks;
- the inline dependency graph and figures `pic-2`, `pic-4`, and `pic-6`;
- additive Indonesian structural labels and the deterministic modular backend.

The deterministic full-context build is 203 pages, 2,955,024 bytes, SHA-256
`b8b0d838d9eff855fbb85aadc2039660fdbad0f2fdc9e7c6eff5b35d84f915d3`.
It exists only to prove references, figures, and layout; later chapters remain
English and are not a release artifact.

The honest partial reader selects only admitted pages and a separately resolved
two-page Chapter 1 hint booklet. It is 19 pages, 881,787 bytes, SHA-256
`1a6909ab8c315fe2529d9267c3d539def1e1f68667bc432d8bf40059dd91a452`.
Two independent compositions produced identical bytes. `/Lang` is `id-ID`,
metadata and outlines are present, internal links to omitted pages are removed,
and only URI annotations remain. The PDF is untagged; the structured source,
backend descriptions, and a future accessible HTML/EPUB surface are explicit
accessibility work, not falsely claimed as complete here.

All 19 pages were rendered and inspected. No clipping, overlap, missing figure,
blank required page, English Chapter 2 spill, or reader-visible structural-label
residue was found. Structural QA preserves environments, labels, references,
citations, graphics, formulas, and the untouched Chapter 2+ hint suffix.

Unit `o004.petrunin.ch02` adds the complete Bab 2, Aksioma: six sections,
eight absolute-geometry results, seven exercises, all seven matching hints, and
figures `pic-8`, `pic-10`, `pic-12`, `pic-915`, and `pic-76`. Its target source
hashes are `e44a5934711c4871289ec82a1c8e4e2acb98b66c18e1e5a3bca378ecabaa3a6d`
for `axioms.tex` and
`cb449316a820b09ef386feefa61d3b57b05b46d90929ea3e87a4c78e7913c066`
for the Chapter 2 hint slice.

The final full-context Chapter 2 admission build is 203 pages, 2,966,179
bytes, SHA-256
`3fec5c24f0e5b73a597dcd5660774c35fb2dd3c8815e89d5ae3568c1309d8501`.
It is reproducible and has no undefined references/citations or
translation-induced Chapter 2 box warnings. Pages 20–25 and hint page 181 were
rendered and inspected; all five wrapfigures are correct. See
`qa/CH02_ADMISSION_20260821.md`. The full-context PDF still contains English
Chapter 3+ material and is not a release artifact.

Unit `o004.petrunin.ch03` adds complete Bab 3, Setengah bidang: five sections,
12 result blocks, nine exercises, eight matching author hints, and 13 figures.
Exercise `ex:angle-measures` has no source hint; no hint was invented. Target
hashes are
`e7b3b3e4858302e4c361fe47056c9285d4881c5a2c8ec4cd2332629504f698d8`
for `half-planes.tex` and
`d5f75149bd2fdbc993d00c0a8d4c8c659846374c9da60d459be0871bbe6f40d4`
for its hint slice.

Two fresh Chapter 3 builds are byte-identical: 204 pages, 2,961,804 bytes,
SHA-256
`94057485cd2f16d55b1adff8d0e53583584c8330e2b51a08d906ef1e83dc6117`.
All 224 generated MetaPost figures match across builds. Pages 26-33 and hint
pages 183-184 were inspected; all 13 figures and the translated hint column are
legible, with no clipping, overlap or missing content. This full-context PDF
contains English Chapter 4+ material and is not a release artifact. See
`qa/CH03_ADMISSION_20260821.md`.

The backend now has 103 records and 65 relations with no dangling endpoints.
Chapter 3 contributes five section rows, 12 result records, nine exercise rows,
eight hint links, 13 descriptions and 16 concept/dependency rows. JSON Schema
and deterministic UTF-8/LF CSV validation pass.

The exact publication/access receipt is
`00_control/PUBLICATION_RECEIPT_UNIT001.json`. GitHub is private at
`KokunoYumeto/bidang-euklides-dan-kerabatnya-id`, tag
`v2026.08.21-unit001`, target commit
`6ccd1c6add2bf4fb5f3c18314c8358e08b47bb08`. The Zenodo record was edited
in place without a new version: anonymous record readback reports restricted
access and exposes zero files, and anonymous requests for all five exact file
URLs return HTTP 403.

The three-layer architecture is frozen in
`00_control/CURRICULUM_ARCHITECTURE.md`; the complete finite workflow is
`00_control/00_CURRENT_GOAL_AND_WORKFLOW.md`.

Next action: translate Chapter 4 (`cong.tex`) and its matching contiguous hint
slice in source order, extend the backend, and apply the same bounded gate. Do
not reopen the admitted Chapters 1-3 boundary.
