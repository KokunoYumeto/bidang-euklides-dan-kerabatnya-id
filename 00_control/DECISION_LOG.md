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

## D010 — private access state

Keep `KokunoYumeto/bidang-euklides-dan-kerabatnya-id` private. Keep Zenodo
record `22044358`, DOI `10.5281/zenodo.22044358`, but restrict its files in
place. Do not create a new version or change either surface to public without a
new direct instruction.

## D011 — localized Chapter 2 reflow

The longer Indonesian chapter introduction made the inherited `\vfill` spill
two lines onto an almost empty page and collide with the running header. Remove
that stretch, move the opener up three baselines, and add three baselines after
the preserved page break. This retains normal type size, fills the opener,
keeps the framed axioms together, and introduces no mathematical or identifier
change.

## D012 — three-layer O004 course architecture

Use the complete Petrunin book as the sole external instructional spine, then
separately author the CC BY-SA 4.0 companion *Transformations, Invariants, and
Model Surfaces* and the separately attributed CC BY-SA 4.0 solutions/mastery
volume. No second external whole book or excerpt is required course reading.
The backend and accessible HTML/EPUB are release layers. Translation completion
does not itself decide curricular selection, but the independently selected
architecture retains the existing edition.

## D013 — deterministic MetaPost and EPS repair

Set MetaPost random seed `2718` only in disposable build copies of both drivers.
Convert each EPS and then remove live Info/XMP metadata and derive a stable PDF
ID from the source-EPS hash. This preserves source bytes while eliminating the
only observed cross-build differences. Two fresh Chapter 3 builds now agree in
the final PDF and all 224 generated MetaPost figures.

## D014 — Chapter 3 admission

Admit complete Chapter 3 and its eight available author hints after structural,
independent language, deterministic-build and visual checks. Do not invent a
hint for `ex:angle-measures`. The full-context PDF contains English Chapter 4+
material and is QA evidence only. Advance the source-order cursor to Chapter 4,
`cong.tex`.

## D015 — Chapter 4 admission and construction-panel reflow

Admit complete Chapter 4 and all five authored hints after structural,
language, deterministic-build and visual checks. Preserve all ten active
figures and the inactive `ex:3-isos`/`pic-43` block. The longer Indonesian text
made the inherited five-panel side wrap overlap prose and run off the page;
replace only that wrapper with a centered two-row sequence for `pic-445`
through `pic-449`. Record the environment substitution as an explicit
layout-only correction, with formulas, labels, references, figure order and
mathematics unchanged. The full-context PDF contains English Chapter 5+
material and remains private QA evidence. Advance the cursor to Chapter 5,
`perp.tex`.
