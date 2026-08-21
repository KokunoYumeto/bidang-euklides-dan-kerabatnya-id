# O004 / C100 — current state

Updated: 2026-08-21

Status: active Bahasa Indonesia reader production. Unit Produksi 001 is complete,
built, structurally verified, and visually admitted locally; GitHub and Zenodo
publication are the next boundary. The whole book is not complete.

The admitted core is Anton Petrunin, *Euclidean Plane and Its Relatives: A
Minimalist Introduction*. The labeled publication witness is arXiv
`1302.1630v25` (third edition, tenth printing, revised 2025-07-07). Production
uses the later official author-repository snapshot
`0b0858e1e985f4c8dadbb6075ae9e095cd4a8981` intentionally, with v25 retained as
the immutable rendered-edition witness. The later commit is not described as a
new printing or edition.

The body-only derivative is admitted. The separate `cover/` directory and its
two proprietary P22 fonts are excluded. This public boundary may include the
translated overlay, backend, controls, scripts, and generated reader. It must
not redistribute the unresolved MetaPost generator closure. Reproduction can
fetch the pinned official archive, remove `cover/`, and apply the overlay.

## Admitted reader boundary

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

Next action: publish this explicitly partial unit to its dedicated GitHub and
Zenodo record/DOI, anonymously verify both, bind URLs/remote bytes in controls,
then translate Chapter 2 (`axioms.tex`) and its seven hints in source order.
