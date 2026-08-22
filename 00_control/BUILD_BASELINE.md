# Deterministic upstream build baseline

Authority: current commit `0b0858e1e985f4c8dadbb6075ae9e095cd4a8981`.

Environment observed 2026-08-21:

- MetaPost 3.00 (MiKTeX 26.5)
- pdfTeX 1.40.29 (MiKTeX 26.5)
- Biber 2.21
- MakeIndex 2.18

The repository README's bare `mpost pic.mp` and `mpost pic-hints.mp` commands do
not work in this MiKTeX environment: MetaPost invokes plain TeX and fails on the
LaTeX preamble.  The source-preserving correction is explicit `-tex=latex`:

```text
cd mppics
mpost -interaction=nonstopmode -tex=latex pic.mp
mpost -interaction=nonstopmode -tex=latex pic-hints.mp
cd ..
pdflatex -interaction=nonstopmode -halt-on-error all-lectures.tex
makeindex all-lectures
pdflatex -interaction=nonstopmode -halt-on-error all-lectures.tex
biber all-lectures
makeindex all-lectures
pdflatex -interaction=nonstopmode -halt-on-error all-lectures.tex
pdflatex -interaction=nonstopmode -halt-on-error all-lectures.tex
```

The first LaTeX pass predictably stops because `all-lectures.tex` inputs the
not-yet-created `.ind`; MakeIndex creates it and the sequence then converges.

For byte-reproducible final passes:

```text
SOURCE_DATE_EPOCH=1766112130
FORCE_SOURCE_DATE=1
```

Two consecutive final passes produced identical bytes:

- PDF: 2,959,996 bytes
- SHA-256: `6a296d2a6e046520575b4987fb6f4e519014f3ff64d1f154d59e2bede15bd50d`
- pages: 199
- page size: 432 × 648 pt
- unencrypted; no JavaScript; no forms; untagged
- resolved references/citations: zero undefined
- log: 24 overfull boxes, 20 underfull boxes, one inherited
  `end occurred inside a group` warning, no LaTeX error or fatal error

Seven representative pages (title, Preface, Chapter 1 opening/body/end,
Chapter 2 boundary, bibliography) were rendered and visually inspected.  No
missing figure, blank page, clipping, or font substitution was observed at
those witnesses.  This is the upstream baseline, not yet the final Indonesian
visual audit.

## Indonesian Unit 001 boundary

After localization and translation of the title, Prakata, Chapter 1, and its
hints, the full-context build converged reproducibly:

- 203 pages; 2,955,024 bytes;
- SHA-256 `b8b0d838d9eff855fbb85aadc2039660fdbad0f2fdc9e7c6eff5b35d84f915d3`;
- zero undefined references/citations and no LaTeX error;
- the remaining later chapters are English and this full PDF is not public.

The Chapter 1 hint-only build is 2 pages, 206,812 bytes, SHA-256
`7ed39f4da2f791da1e2e27547507593b9ca82f8d9338bc07bbe264d1fd26ff67`.

The deterministic publication reader combines a scope page, full-context pages
1–2 and 6–19, and the two hint pages. Two separate runs were byte-identical:

- 19 pages; 881,787 bytes;
- SHA-256 `1a6909ab8c315fe2529d9267c3d539def1e1f68667bc432d8bf40059dd91a452`;
- `/Lang=id-ID`; unencrypted; no JavaScript/forms; URI-only annotations;
- untagged PDF, stated as an accessibility caveat.

All 19 pages were rendered at 120 dpi and inspected through four contact sheets
plus high-resolution scope, figure, chapter-end, and both hint-page witnesses.
No clipping, overlap, missing figure, English Chapter 2 spill, or blank required
content was observed.

## Chapter 3 deterministic admission boundary

The build harness now seeds disposable MetaPost driver copies with `2718`, uses
`mpost -tex=latex`, and normalizes conversion-time metadata in both EPS-derived
PDFs. Default source-root resolution is performed after parameter binding so it
does not evaluate an empty `$PSScriptRoot`; the admitted builds were executed
under PowerShell 7.

Two fresh, separate output directories produced the same result:

- PDF: 204 pages; 2,961,804 bytes;
- SHA-256: `94057485cd2f16d55b1adff8d0e53583584c8330e2b51a08d906ef1e83dc6117`;
- 224 generated `.mps` files; zero cross-build hash mismatches;
- normalized CC badge PDF SHA-256
  `7167e45adcc360f116b77210a2e452308e2b8fffd84106f1ea69045cb5be9928`;
- normalized H2checkers PDF SHA-256
  `61a45915d8630a8df63bd9b9ecb095ab9fe6d6671b3360f814bea97ce9a8d885`.

The converged full-context log has zero undefined references/citations and no
fatal error. It reports 33 overfull and 20 underfull boxes plus the inherited
group warning. Chapter 3 itself contributes one 3.65144-point overfull graphic
wrapper and two underfull text boxes, with no visible clipping or overlap; its
hint slice contributes none. Pages 26-33 and hint pages 183-184 were rendered
at 150 dpi and inspected. See `qa/CH03_ADMISSION_20260821.md`.

The full-context PDF still contains English Chapter 4+ material. It is build/QA
evidence and is not a release artifact.

## Chapter 4 deterministic admission boundary

The first translated Chapter 4 build was rejected visually because the five
construction panels in the inherited side wrap overlapped Indonesian prose and
ran off the page. The admitted source reflows `pic-445` through `pic-449` into
a centered two-row sequence without changing their order or any mathematical
surface, identifier, reference, exercise, or construction step.

The fixed closure `build/ch04-source-snapshot-20260822` contains the exact
admitted Chapter 4 and hint bytes, with authority Chapter 5 onward. Two fresh
output directories, `build/ch04-final-i-20260822` and
`build/ch04-final-j-20260822`, built independently from that closure, produced
identical results. Their PDF bytes are also identical to the visually
inspected pre-cleanup builds; intervening source changes removed only trailing
whitespace from Chapter 4 and its hint comments:

- PDF: 205 pages; 2,962,911 bytes;
- SHA-256: `1ff91aa4ff95880980237060624fe95022d6664b8cc68180859d266a9e5cc92e`;
- 224 generated `.mps` files; zero cross-build hash mismatches;
- normalized CC badge SHA-256
  `7167e45adcc360f116b77210a2e452308e2b8fffd84106f1ea69045cb5be9928`;
- normalized H2checkers SHA-256
  `61a45915d8630a8df63bd9b9ecb095ab9fe6d6671b3360f814bea97ce9a8d885`.

The converged log has zero undefined references/citations and no fatal error.
It reports 40 overfull and 22 underfull boxes plus the inherited group warning.
Chapter 4 contributes seven overfull and two underfull diagnostics; none causes
visible clipping. Pages 34-40 and hint page 184 were rendered at 150 dpi and
inspected. All ten figures, including every construction panel, are visible and
legible with no overlap or cutoff. See `qa/CH04_ADMISSION_20260822.md`.

The full-context PDF still contains English Chapter 5+ material. It is private
build/QA evidence and is not a release artifact.

## Chapter 5 deterministic admission boundary

Two fresh output directories, `build/ch05-final-c-20260822` and
`build/ch05-final-d-20260822`, built from the exact final Chapter 5 body and
hint bytes, produced identical results:

- PDF: 207 pages; 2,965,782 bytes;
- SHA-256: `6ca6402e66b5ab0a048697bf0478a00548e1c5a64096d605fbd95947c21994ee`;
- 224 generated `.mps` files; zero cross-build hash mismatches;
- normalized CC badge SHA-256
  `7167e45adcc360f116b77210a2e452308e2b8fffd84106f1ea69045cb5be9928`;
- normalized H2checkers SHA-256
  `61a45915d8630a8df63bd9b9ecb095ab9fe6d6671b3360f814bea97ce9a8d885`.

The converged log has zero undefined references/citations and no fatal error.
It reports 44 overfull and 31 underfull boxes plus the inherited group warning.
Chapter 5 contributes four overfull and one underfull diagnostic; rendered
inspection confirms that none clips or hides reader content.

Pages 41-48 and hint pages 185-187 were rendered at 150 dpi and inspected.
All nine body figures and five hint figures are present and legible. The first
build exposed a collision between the long Indonesian Section E running head
and page number 45. An optional short running/contents title, `Isometri
langsung dan tak langsung`, removes the collision while retaining the complete
visible section title. Pixel comparison proves pages 41-44, 46-48, and 185-187
are unchanged by the repair; the repaired page 45 was inspected separately.

The full-context PDF still contains English Chapter 6+ material. It is private
build/QA evidence and is not a release artifact.

## Chapter 6 deterministic admission boundary

Two fresh output directories, `build/ch06-final-a-20260822` and
`build/ch06-final-b-20260822`, built from the exact final Chapter 6 body and
hint bytes, produced identical results:

- PDF: 208 pages; 2,967,413 bytes;
- SHA-256: `4c4e1b9a27b17d274834c4b828bc764519d018c73a0449842098b1e2d937146a`;
- 224 generated `.mps` files; zero cross-build hash mismatches;
- normalized CC badge SHA-256
  `7167e45adcc360f116b77210a2e452308e2b8fffd84106f1ea69045cb5be9928`;
- normalized H2checkers SHA-256
  `61a45915d8630a8df63bd9b9ecb095ab9fe6d6671b3360f814bea97ce9a8d885`.

The converged log has zero undefined references/citations and no fatal error.
It reports 51 overfull and 32 underfull boxes plus the inherited group warning.
Chapter 6 contributes six overfull and one underfull diagnostic; rendered
inspection confirms that none clips, collides, or obscures reader content.

Pages 49–54 and hint page 188 were rendered at 150 dpi and inspected. All four
Chapter 6 figures are present, sharp, and correctly wrapped. Page 54's open
space is the genuine end of the short chapter, and the mixed-language boundary
on hint page 188 cleanly separates the admitted Chapter 6 hints from English
Chapter 7 QA context.

The full-context PDF still contains English Chapter 7+ material. It is private
build/QA evidence and is not a release artifact.

## Chapter 7 deterministic admission boundary

Two fresh output directories, `build/ch07-final-e-20260822` and
`build/ch07-final-f-20260822`, built from the exact final Chapter 7 body and
hint bytes, produced identical results:

- PDF: 208 pages; 2,968,464 bytes;
- SHA-256: `7fa21a42a1cdf4d78db3b1b1ae9d8db3e58ae50c3091264f4402f4b54aa0b448`;
- 224 generated `.mps` files; zero cross-build hash mismatches;
- normalized CC badge SHA-256
  `7167e45adcc360f116b77210a2e452308e2b8fffd84106f1ea69045cb5be9928`;
- normalized H2checkers SHA-256
  `61a45915d8630a8df63bd9b9ecb095ab9fe6d6671b3360f814bea97ce9a8d885`.

The converged log has zero undefined references/citations and no fatal error.
It reports 55 overfull and 39 underfull boxes plus the inherited group warning.
Chapter 7 contributes six overfull and three underfull diagnostics; rendered
inspection confirms that none clips, collides, or obscures reader content.

Body pages 55–65 and hint pages 189–190 were rendered at 150 dpi and
independently inspected. All thirteen body figures and both hint figures are
present and legible. The corrected incidence point is visible on page 58; the
reflowed `Sifat transversal` heading is clean; the added Apollonius hypotheses
are readable on page 64; and the transition to untranslated Chapter 8 context
on page 65 is explicit. See `qa/CH07_ADMISSION_20260822.md`.

The full-context PDF still contains English Chapter 8+ material. It is private
build/QA evidence and is not a release artifact.

## Chapter 8 deterministic admission boundary

The first two clean builds exposed a reader-visible English-label defect in
`pic-108` and were rejected. The two `bisector` strings were localized to
`garis bagi` and the `external` string to `luar`, so the paired labels read
`garis bagi luar`. Two fresh corrected output directories,
`build/ch08-final-c-20260822` and `build/ch08-final-d-20260822`, produced
identical results:

- PDF: 209 pages; 2,677,012 bytes;
- SHA-256: `ca38d7112aa685020094760b3d91c8511cc926eaff73c8fe1db27446400cfdfc`;
- 224 generated `.mps` files; zero cross-build hash mismatches;
- localized `pic-108.mps`: 22,274 bytes; SHA-256
  `7801282b8ef71e335f8da9ee426d69a1d255adbb9cabcdbcf7819179d8c72532`;
- normalized CC badge SHA-256
  `7167e45adcc360f116b77210a2e452308e2b8fffd84106f1ea69045cb5be9928`;
- normalized H2checkers SHA-256
  `61a45915d8630a8df63bd9b9ecb095ab9fe6d6671b3360f814bea97ce9a8d885`.

The converged log has zero undefined references/citations and no fatal error.
It reports 63 overfull and 41 underfull boxes plus the inherited group warning.
Chapter 8 contributes eight overfull and two underfull diagnostics; rendered
inspection confirms that none clips, collides, or obscures reader content.

Physical PDF pages 65–73 and hint pages 191–193 were rendered at 150 dpi and
inspected. All nine body figures are present and legible. The corrected page 68
shows `garis bagi` and `garis bagi luar` cleanly; the B/C/A correspondence and
same-proposition wording are visible; Chapter 9 begins as explicit English QA
context. See `qa/CH08_ADMISSION_20260822.md`.

The tracked, idempotent `scripts/apply_figure_localizations.ps1` applies or
verifies the exact `pic-108` overlay by hash. A fresh proof build through the
updated harness reproduced the admitted PDF hash exactly. The full-context PDF
is private build/QA evidence and is not a release artifact.
