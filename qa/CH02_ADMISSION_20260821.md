# Chapter 2 admission — 2026-08-21

Status: admitted for contiguous Bahasa Indonesia production. This is a source,
backend, and full-context build boundary; it is not a new public release.

## Frozen source

- authority `axioms.tex`: 12,593 bytes, SHA-256
  `f82198417341fe2ae9bb713bddda2f8620b6d45bf1b948bf94f7fa93efcf85a5`;
- target `axioms.tex`: 13,472 bytes, SHA-256
  `e44a5934711c4871289ec82a1c8e4e2acb98b66c18e1e5a3bca378ecabaa3a6d`;
- authority Chapter 2 hint slice: 1,962 bytes, SHA-256
  `d0ddde798dd4f09dadc8ece08e8fae377226dc851b9a0534935bc3fbc7916511`;
- target Chapter 2 hint slice: 2,249 bytes, SHA-256
  `cb449316a820b09ef386feefa61d3b57b05b46d90929ea3e87a4c78e7913c066`;
- whole target `hints.tex`: SHA-256
  `cb075a2c45658d5f0a82391024097a2cffdcd99201fe3d075cef7d74a0bbbaca`;
- frozen Chapter 1 hint prefix: SHA-256
  `659167c454ee2ee734a6222fa065b860ed53348eb3a74744a567fba802a1d486`;
- frozen Chapter 3+ hint suffix: SHA-256
  `3a4e2fface82d19a9488b95352d58fbeedabe388c6e3b0967c3f1ffbe4e87761`.

The admitted scope is the complete chapter, all six sections, eight marked
absolute-geometry results, all seven exercises and their seven current-source
hints, five figures, and the source-order backend records. Stable source labels,
including `ex:refelection-of-line`, remain unchanged.

## Structural and language QA

`scripts/qa_ch02.py` passes. It preserves 56 ordered environment boundaries,
25 labels, 27 references, four citations, five graphics, 15 theorem-like
blocks, nine `\parit` commands, seven `\qeds`, and 199 protected mathematics
surfaces. The hint gate preserves 69 raw commands, 30 raw references, 15 active
and 16 raw mathematics surfaces, the translated Chapter 1 prefix, and the
byte-identical Chapter 3+ suffix.

Independent language audit found no P1 or P2 issue and one P3 calque, which was
corrected. A second layout pass shortened several faithful Indonesian sentences
to remove every translation-induced overfull/underfull box without changing a
formula, identifier, claim, or exercise part.

The inherited chapter-opening stretch produced an almost empty spill page in
Indonesian. The localized source removes that `\vfill`, pulls the longer opener
up by three baselines, and restores three baselines above the following section.
The normal font size is retained. This eliminates the spill and running-header
collisions while retaining the intended section page break.

## Build and visual QA

The clean deterministic full-context build is:

- `build/ch02-admitted-final-20260821/all-lectures.pdf`;
- 203 pages, 2,966,179 bytes;
- SHA-256
  `3fec5c24f0e5b73a597dcd5660774c35fb2dd3c8815e89d5ae3568c1309d8501`;
- two final `pdflatex` passes produced identical bytes;
- no undefined reference or citation and no Chapter 2 overfull/underfull box;
- the only Chapter 2 diagnostic is the duplicate `Hfootnote.1` destination
  already present in the upstream build.

Rendered pages 20–25 and hint page 181 were inspected at 144 dpi. The chapter
opener, framed axioms, all text and formulas, and figures `pic-8`, `pic-10`,
`pic-12`, `pic-915`, and `pic-76` are present without clipping, collision,
misplacement, or blank required pages. The seven Chapter 2 hints are readable in
the right column of page 181. Untranslated Chapter 3 hints begin below them;
therefore this mixed-context PDF remains QA evidence, not a release artifact.

## Preserved upstream observations

Potential upstream cleanup remains deferred and deduplicated until completion:
the stable typo in `ex:refelection-of-line`, the mismatch between label
`ex:infinite-number-of-lines` and its actual triangle prompt, the missing
`\angle` in the prose of `thm:straight-angle`, and the index spacing in
`degenerate! triangle`. No upstream contact was made.
