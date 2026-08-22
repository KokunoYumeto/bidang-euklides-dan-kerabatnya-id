# Chapter 4 admission — 2026-08-22

## Boundary

Complete Bab 4, *Segitiga kongruen*, and its exact authored hint slice are
admitted. The unit contains six sections, four neutral-geometry results, five
labeled exercises, one unlabeled worked construction problem, five matching
author hints, ten active figures, and the inactive `ex:3-isos`/`pic-43` block
preserved as comments. The next source-order cursor is Chapter 5, `perp.tex`.

Authority `cong.tex` is 12,527 bytes, SHA-256
`7ad021c768316aafec871003fdcb7f5daff4a16d42c378366dfe8dc913df4f4f`.
The admitted target is 13,622 bytes, SHA-256
`70cbc1809520da16814159a32021a66ebb48db56190b3a638af2205436282b43`.
The authority hint slice is 1,451 bytes, SHA-256
`35999a3ca0db65e8c1bdf1e9e9a298b90a1c7cf0fc8044203ffaa8b0202b8716`;
the target slice is 1,601 bytes, SHA-256
`85eb2f743180e984948a8fe094b5a7f645135e47a7a5f1e9d8cb8ac86fa69c5c`.
The complete target `hints.tex` is 92,351 bytes, SHA-256
`84a8289a0d5a7939bd13d16831efcd155d017ec0d7099584aa451a38d299d3f0`.
The Chapter 1-3 prefix and Chapter 5+ suffix remain frozen at
`2ff27e2ca3f9c53f94dec954a4c07560787e9a61ed854d1a0720e0018152abe1`
and
`c9d2a983be56f8d1c78b6ad06ce6ac6e468b4b74df161d8fac79c8e056eecce4`.

## Structural and language gate

`scripts/qa_ch04.py` passes and records the machine-readable receipt in
`qa/CH04_STRUCTURAL_QA_20260822.json`. Ordered labels, equation labels,
references, citations, graphics, theorem options, proof closures, active and
commented math surfaces, exercise markings, and comment topology agree with
authority. The verified active census is 42 environment boundaries, ten
labels, three equation labels, 24 references, zero citations, ten graphics,
ten theorem blocks, five proof closures, six sections, seven index entries,
166 math surfaces, four `abs` markers, and one later-use marker. The hint slice
preserves 58 raw commands, eight raw references, two comment lines, and 35 raw
math surfaces. Earlier Chapter 1-3 QA scripts also pass after being made
source-order aware: each freezes its own admitted slice rather than rejecting
legitimate later translation.

An independent full read compared every translated paragraph with authority.
No mathematical change or active English residue was found. Terminology is
normalized around `kekongruenan`, SAS/ASA/SSS/SSA/SAA/AAA, `segitiga sama
kaki`, `alas`, `tak degenerat`, `transformasi isometrik`, and `konstruksi
penggaris dan jangka`. The source label
`eq:A'B'C'simA'B'C''` is preserved even though its mnemonic says `sim` and the
display uses congruence.

## Deliberate reader reflow

The first translated build exposed a real layout defect: the longer Indonesian
prose caused the five-panel construction wrap (`pic-445` through `pic-449`) to
begin too low, overlap text, and run off the page. The final target replaces
only that layout wrapper with a centered two-row sequence. All five figures,
their order, the construction steps, formulas, labels, and references are
unchanged. Fail-closed QA records the exact one-for-one layout exception: six
authority wrapfigures versus five target wrapfigures and one target centered
panel sequence.

## Deterministic build and visual gate

The fixed closure `build/ch04-source-snapshot-20260822` contains the exact
admitted Chapter 4 and hint bytes, with authority Chapter 5 onward. Fresh
directories `build/ch04-final-i-20260822` and
`build/ch04-final-j-20260822`, built independently from that closure, produced
identical 205-page PDFs. Their PDF bytes are also identical to the visually
inspected pre-cleanup builds; intervening source changes removed only trailing
whitespace from Chapter 4 and its hint comments:

- 2,962,911 bytes;
- SHA-256
  `1ff91aa4ff95880980237060624fe95022d6664b8cc68180859d266a9e5cc92e`;
- 224 generated MetaPost files with zero cross-build hash mismatches;
- normalized CC badge SHA-256
  `7167e45adcc360f116b77210a2e452308e2b8fffd84106f1ea69045cb5be9928`;
- normalized H2checkers SHA-256
  `61a45915d8630a8df63bd9b9ecb095ab9fe6d6671b3360f814bea97ce9a8d885`.

The converged log has zero undefined references, zero undefined citations, and
no fatal error. It has 40 overfull and 22 underfull boxes globally plus the
inherited group warning. Chapter 4 contributes seven overfull and two
underfull diagnostics; rendered inspection confirms that none clips or hides
reader content. PDF pages 34-40 and hint page 184 were rendered at 150 dpi and
inspected. Every figure, equation, theorem box, exercise marking, construction
step, and hint is legible; the reflow has no overlap, cutoff, or missing panel.

The full-context PDF still contains English Chapter 5+ material and is private
QA evidence, not a release artifact. It is untagged; the required semantic
HTML/EPUB reader remains a later additive accessibility surface.

## Backend gate

The additive backend now has 140 unique records and 87 relations with zero
dangling endpoints; JSON Schema validation passes. Chapter 4 adds seven unit
order rows, five exercise-hint rows, fifteen concept/dependency rows, ten
figure descriptions, four result records, the synthetic unlabeled-problem ID,
one build artifact, one QA event, and two correction records. Artifact-tool CSV
imports verify UTF-8 without BOM, LF endings, terminal newlines, exact headers,
expected row/column counts, and unique primary IDs. Canonical hashes are:

- `catalog-v0.json`: `ee62b6e19359c25f089ca06a914c1a15f5f9f45a08566aedd254e7287244e796`;
- `unit-order-v0.csv`: `a4de5d2e2f570e07fd241b1f314363e4c27ec1f6259815e0fa26d7fefd7e7665`;
- `exercise-hints-v0.csv`: `8f5721d427144f7102964e930b78ea9c266ead54d4c2ad9fbb0891a2f5c0a8f1`;
- `figure-descriptions-id-v0.csv`: `bb9e145dc089f1cc1d885308621f1662a7a20b4e83992a2f8732977c346e346f`;
- `concepts-ch04-id-v0.csv`: `cb90bc6f410c7cf72e2ac088502118c7a9c4a08acb41ce5731de10ec32b4584c`.

Admission decision: pass. Advance to Chapter 5 without reopening Chapters
1-4. Keep GitHub private and Zenodo files restricted; make no Zenodo version at
this boundary.
