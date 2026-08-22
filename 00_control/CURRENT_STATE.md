# O004 / C100 — current state

Updated: 2026-08-22

Status: active Bahasa Indonesia reader production. The front matter, Chapters
1-8, and their exact available hint slices are complete, structurally verified,
and visually admitted. The GitHub repository and Unit 001 release are private.
Zenodo record `22044358`, DOI
`10.5281/zenodo.22044358`, retains all five files with restricted access. The
whole book is not complete; the cursor is immediately before Chapter 9.

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

At the Chapter 3 boundary, the backend had 103 records and 65 relations.
Chapter 3 contributes five section rows, 12 result records, nine exercise rows,
eight hint links, 13 descriptions and 16 concept/dependency rows. JSON Schema
and deterministic UTF-8/LF CSV validation pass.

Unit `o004.petrunin.ch04` adds complete Bab 4, Segitiga kongruen: six
sections, four neutral-geometry results, five labeled exercises, one unlabeled
worked construction problem, five matching hints, and ten active figures.
Target hashes are
`70cbc1809520da16814159a32021a66ebb48db56190b3a638af2205436282b43`
for `cong.tex` and
`85eb2f743180e984948a8fe094b5a7f645135e47a7a5f1e9d8cb8ac86fa69c5c`
for its hint slice.

Two fresh Chapter 4 builds are byte-identical: 205 pages, 2,962,911 bytes,
SHA-256
`1ff91aa4ff95880980237060624fe95022d6664b8cc68180859d266a9e5cc92e`.
All 224 generated MetaPost figures match across builds. PDF pages 34-40 and
hint page 184 were inspected. The initial build exposed overlapping and
off-page construction panels; the admitted source replaces that single side
wrap with a centered two-row sequence retaining `pic-445` through `pic-449` in
order. The final pages have no clipping, overlap, or missing panels. See
`qa/CH04_ADMISSION_20260822.md`.

Unit `o004.petrunin.ch05` adds complete Bab 5, Garis tegak lurus dan
transformasi isometrik: seven sections, eight results, eighteen exercises,
seventeen authored hint blocks covering all eighteen exercises, nine body
figures, and five hint figures. The final source hint is intentionally shared
by `ex:tangent` and `ex:tangent-circle`. Target hashes are
`650ffbc55d59c238dc7c884bc3d0765ecae6e2fdab953d5390fb27ceb09446ed`
for `perp.tex` and
`d2788d7d1095d838d733533750e3bc6fe4d6de00bad2669be21f67f8988894de`
for its hint slice.

Two fresh Chapter 5 builds are byte-identical: 207 pages, 2,965,782 bytes,
SHA-256
`6ca6402e66b5ab0a048697bf0478a00548e1c5a64096d605fbd95947c21994ee`.
All 224 generated MetaPost figures match across builds. PDF pages 41-48 and
hint pages 185-187 were inspected. All fourteen figures are legible, with no
clipping, overlap, or missing content. The initial build exposed a collision
between the long Section E running head and page number 45; an optional short
running title fixes only that header while preserving the complete visible
section title. See `qa/CH05_ADMISSION_20260822.md`.

The Chapter 5 translation records one referent correction for an undefined
source symbol `$f$`, three bounded Indonesian attachment/wording
clarifications, and the layout-only short running title. None changes a
mathematical claim, formula, identifier, exercise, figure, or source order.

Unit `o004.petrunin.ch06` adds complete Bab 6, Segitiga sebangun: four
sections, four results, eight exercises, eight matching author hints, and four
figures. Target hashes are
`23c609c66ae26e627425bfd196454b4cdc7a7b11d8398265786c9234ddcdd201`
for `similar.tex` and
`38cdafe5f4fcbb7440d4ac9cfdb1bb6c1b0925d37de24dc0996da61de0e82273`
for its hint slice.

Two fresh Chapter 6 builds are byte-identical: 208 pages, 2,967,413 bytes,
SHA-256
`4c4e1b9a27b17d274834c4b828bc764519d018c73a0449842098b1e2d937146a`.
All 224 generated MetaPost figures match across builds. PDF pages 49–54 and
hint page 188 were inspected. All four figures and their wraps are legible,
with no clipping, overlap, collision, or missing content. The six Chapter 6
overfull and one underfull diagnostics are visually harmless. See
`qa/CH06_ADMISSION_20260822.md`.

Chapter 6 preserves the legacy chapter label `chap:parallel`, the legacy
theorem-label spelling `thm:signs-of-triug`, the incompatibility between `k=1`
and seven distinct points in `ex:k*triangle`, and inactive commented
`\triange` spellings. The backend tracks the chapter-label note, distinctness
inconsistency, inactive typos, and a localized Ptolemy clarification. That
proof explicitly names the corresponding left and right sides when adding
equal angles; this changes no mathematical claim, formula, identifier, or
source order.

The backend now has 240 unique records and 139 relations with no dangling
endpoints. Chapter 6 contributes five unit-order rows, four result records,
eight exercise–hint mappings, four admitted figure descriptions, 22
concept/dependency rows, four correction/source-note records, one build
artifact, and one QA event. JSON Schema and UTF-8/LF CSV verification pass;
concept mappings remain separately pending backend review.

Unit `o004.petrunin.ch07` adds complete Bab 7, Garis sejajar: six sections,
eight results, twenty-one top-level exercises with three labeled subparts,
twenty-one authored hint blocks, thirteen body figures, and two hint figures.
The parent hint for `ex:line-coord` covers its labeled parameterization
subpart. Target hashes are
`3459de730c56922fe4a9e30781d3a12ce1671c735423f5eaed12175d9d5d5385`
for `parallel.tex` and
`1a914474041c1a1fb05a3b7f2cd46c8da279431de7d08e39ed9f72e770532280`
for its hint slice.

Two fresh Chapter 7 builds are byte-identical: 208 pages, 2,968,464 bytes,
SHA-256
`7fa21a42a1cdf4d78db3b1b1ae9d8db3e58ae50c3091264f4402f4b54aa0b448`.
All 224 generated MetaPost figures match across builds. Body pages 55–65 and
hint pages 189–190 were independently inspected; all fifteen Chapter 7 figures
and the corrected/reflowed reader surfaces are legible, with no clipping,
overlap, collision, off-page content, or missing material. The six Chapter 7
overfull and three underfull diagnostics are visually harmless. See
`qa/CH07_ADMISSION_20260822.md`.

Chapter 7 preserves the legacy `chap:angle-sum`, `ex:smililar+parallel`, and
both `ex:apolonnius` spellings. It discloses four high-confidence mathematical
repairs, the nondegenerate-quadrangle index correction, the forced-pagebreak
reflow, and bounded Indonesian fluency normalization. The inactive signed
`pi/4` exercise and hint remain preserved as an upstream editorial note.

The backend now has 309 unique records and 179 relations with no dangling
catalog endpoints. Chapter 7 contributes seven unit-order rows, eight result
records, twenty-four exercise/subpart rows, twenty-one top-level hint mappings,
fifteen admitted figure descriptions, twenty-nine concept/dependency rows,
twelve correction/source/localization records, one build artifact, and one QA
event. JSON Schema and UTF-8/LF CSV verification pass; Chapter 7 concept
mappings remain `mapped-pending-qa`.

Unit `o004.petrunin.ch08` adds complete Bab 8, Geometri segitiga: six
sections, six labeled results (including two absolute-geometry results),
thirteen exercises, thirteen directly matching author hints, and nine body
figures. Target hashes are
`b599ee9baded53dc0c81fe6e0bb6539e5e43e5173d1ba525df5e8885a024f8b6`
for `triangle.tex` and
`8cba27ea4b834ce686c95e6601044a4f792daae4400094da3e6bcec1fd289187`
for its hint slice.

Two fresh Chapter 8 builds are byte-identical: 209 pages, 2,677,012 bytes,
SHA-256
`ca38d7112aa685020094760b3d91c8511cc926eaff73c8fe1db27446400cfdfc`.
All 224 generated MetaPost figures match across builds. Body pages 65-73 and
hint pages 191-193 were inspected. All nine body figures, equations, wraps,
headings and hint columns are legible, with no clipping, overlap, collision,
off-page content, or missing material. The first visual pass rejected English
labels in `pic-108`; the admitted hash-gated overlay localizes both `bisector`
strings to `garis bagi` and `external` to `luar`, so the paired labels read
`garis bagi luar`. A fresh build through the
updated harness reproduced the admitted PDF hash. See
`qa/CH08_ADMISSION_20260822.md`.

Chapter 8 preserves the immutable source IDs `ex:midle` and
`ex:ext-disect`, the external `ex:abs-bisect=median` reference, the homothety
self-study dependency, and the distinct line/distance senses of altitude. It
corrects the source's angle/vertex prose correspondence to B/C/A and calls
`prop:angle-bisect-dist` a proposition rather than a lemma, without altering
any formula or identifier. The hint-only term *excenter* is localized as
`eksenter`.

The backend now has 360 unique records and 209 relations with no duplicates or
dangling endpoints. Chapter 8 contributes seven admitted ordered-unit rows,
six admitted result records, thirteen exercise-hint mappings, nine admitted
figure descriptions, twenty-one concept/dependency rows, five applied
correction/localization records, five preserved source/dependency/accessibility
notes, one build artifact and one QA event. JSON Schema, deterministic UTF-8/LF
CSV, and registered-artifact hash checks pass; Chapter 8 concept mappings
remain `mapped-pending-qa`.

The exact publication/access receipt is
`00_control/PUBLICATION_RECEIPT_UNIT001.json`. GitHub is private at
`KokunoYumeto/bidang-euklides-dan-kerabatnya-id`, tag
`v2026.08.21-unit001`, target commit
`6ccd1c6add2bf4fb5f3c18314c8358e08b47bb08`. The Zenodo record was edited
in place without a new version: anonymous record readback reports restricted
access and exposes zero files, and anonymous requests for all five exact file
URLs currently return HTTP 302 to the Zenodo login page rather than file bytes.
The record and DOI were not changed and no new version was created; see
`00_control/GITHUB_CHECKPOINT_CH05.json`. The earlier timestamped Chapter 4
access receipt records the then-observed 404 response without overriding this
newer readback.

The Chapter 3 content checkpoint is private Git commit
`4b2a2a683354c4785aaebb777343049ec5697f6e`. GitHub branch readback matched
that commit, repository visibility remained `PRIVATE`, and six representative
source/backend/control blob IDs matched local Git exactly. The receipt is
`00_control/GITHUB_CHECKPOINT_CH03.json`. No Zenodo mutation or new version was
made at this boundary.

The Chapter 5 content checkpoint is private Git commit
`79eee83fbb1c0153146325b48c08ea6bf0bf5874`. GitHub branch readback matched
that commit, repository visibility remained `PRIVATE`, and five representative
source/backend/control blob IDs and byte counts matched local Git exactly. The
receipt is `00_control/GITHUB_CHECKPOINT_CH05.json`. Zenodo remained
file-restricted and was not mutated or versioned.

The combined Chapter 6–7 content checkpoint is private Git commit
`6086305e6ffba0101cf2a96fb1b105f655e00d54`. GitHub branch readback matched
that commit, repository visibility remained `PRIVATE`, and six representative
source/backend/QA/control files matched local bytes, SHA-256 hashes, and Git
blob IDs exactly. The receipt is `00_control/GITHUB_CHECKPOINT_CH07.json`.
Zenodo remained file-restricted, exposed zero files anonymously, redirected all
five known file requests to authentication, and was not mutated or versioned.

The Chapter 8 content checkpoint is private Git commit
`6ff15b6090337a602b993fbb43e55cbe85a65402`. GitHub branch readback matched
that commit, repository visibility remained `PRIVATE`, and six representative
source/backend/QA/control files matched local bytes, SHA-256 hashes, and Git
blob IDs exactly. The receipt is `00_control/GITHUB_CHECKPOINT_CH08.json`.
Zenodo remained file-restricted, exposed zero files anonymously, redirected all
five known file requests to authentication, and was not mutated or versioned.

The three-layer architecture is frozen in
`00_control/CURRICULUM_ARCHITECTURE.md`; the complete finite workflow is
`00_control/00_CURRENT_GOAL_AND_WORKFLOW.md`.

Next action: translate Chapter 9 (`inscribed-angle.tex`) and its matching
contiguous hint slice in source order, extend the backend, and apply the same
bounded gate. Do not reopen the admitted Chapters 1-8 boundary.
