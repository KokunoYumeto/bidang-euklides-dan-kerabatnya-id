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
- log: 24 overfull boxes, 18 underfull boxes, one inherited
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
