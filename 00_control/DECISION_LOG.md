# Decision log

## D001 — authority split

Use arXiv v25 as the labeled third-edition/tenth-printing witness and current
official repository commit `0b0858e…` as the intentional post-printing working
source.  Never describe the latter as an eleventh printing or new edition.

## D002 — candidate admission

Admit Petrunin after a bounded comparison with Hitchman and Martin.  Petrunin
alone satisfies the exact role breadth, editable-source, assessment, and lawful
adaptation requirements together.

## D003 — cover and fonts

Exclude the entire `cover/` directory.  Do not redistribute or embed either P22
font.  Use the body title page and independently licensed/default TeX fonts.

## D004 — component rights

Do not flatten `fiziko.mp`, `macros.mp`, public-domain and CC badge assets into
one blanket CC claim.  Generated body output is admitted; public generator
source packaging remains gated.

## D005 — initial production unit

Translate the localized title, complete Preface, complete Chapter 1, and all
Chapter 1 hints as the first contiguous reader unit.  Preserve full-context
buildability; do not claim the later English chapters are translated.

## D006 — backend

Stable identifiers are locale-neutral and additive.  Existing LaTeX labels are
preserved as source-local IDs; backend IDs never replace them in the TeX source.

## D007 — honest partial-reader publication

At a substantial verified boundary, publish only the completed Indonesian unit,
not the mixed-language full-context build. Unit 001 contains a scope notice,
title/license, complete Prakata, complete Chapter 1, and its exact hint slice.
Label it as partial on every GitHub and Zenodo surface.

## D008 — source-overlay distribution

The Indonesian overlay, backend, controls, and generated reader may be public.
Do not mirror the unresolved MetaPost generator source. Reproducible builds may
download the exact official commit, verify its archive hash, remove `cover/`,
then apply the public translation overlay locally.

## D009 — structural locale hook

Because Babel reapplies English captions at document start, Indonesian
structural labels are registered through `\captionsenglish` in addition to the
direct commands. This changes only generated labels such as `Bab` and
`Daftar Isi`; source numbering and identifiers remain unchanged.
