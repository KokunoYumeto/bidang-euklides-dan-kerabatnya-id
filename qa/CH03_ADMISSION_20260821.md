# Chapter 3 admission receipt

- Date: 2026-08-21
- Unit: `o004.petrunin.ch03`
- Source: `half-planes.tex` plus the exact Chapter 3 hint slice
- Status: admitted for the private id-ID production lane

## Translation and structural result

The complete five-section Chapter 3, all 12 result blocks, all nine exercises,
all 13 figures and all eight available author-hint records are translated.
Exercise `ex:angle-measures` has no source hint and remains explicitly recorded
as such; no hint was invented. The independent language/fidelity audit found no
mathematical, completeness or substantive Indonesian issue and no active
English residue.

Fail-closed structural QA passes. The target preserves 82 ordered environment
boundaries, 25 labels, one equation label, 38 references, 13 graphics, 21
theorem blocks, 10 proof closures, 326 protected chapter math surfaces, 65
hint math surfaces, four `[!]` markers and nine `[\abs]` markers. The already
translated hint prefix is frozen and the entire Chapter 4+ suffix remains
byte-identical to authority. Exact evidence is in
`qa/CH03_STRUCTURAL_QA_20260821.json`.

## Deterministic build

Two separate fresh builds used `SOURCE_DATE_EPOCH=1766112130`,
`FORCE_SOURCE_DATE=1`, MetaPost seed `2718`, `mpost -tex=latex`, and
deterministic normalization of both EPS-derived PDFs. Results:

- PDF: 204 pages; 2,961,804 bytes; SHA-256
  `94057485cd2f16d55b1adff8d0e53583584c8330e2b51a08d906ef1e83dc6117`;
- all 224 generated `.mps` files: zero cross-build mismatches;
- normalized `by-sa` PDF: 5,002 bytes; SHA-256
  `7167e45adcc360f116b77210a2e452308e2b8fffd84106f1ea69045cb5be9928`;
- normalized H2checkers PDF: 194,716 bytes; SHA-256
  `61a45915d8630a8df63bd9b9ecb095ab9fe6d6671b3360f814bea97ce9a8d885`.

The converged log has zero undefined references/citations, zero fatal errors,
33 overfull and 20 underfull boxes, and the one inherited
`end occurred inside a group` warning. Within Chapter 3 itself there is one
3.65144-point overfull box on the unchanged `pic-32` graphic wrapper and two
underfull text boxes; none appears as clipping or overlap. The Chapter 3 hint
slice introduces no box warning.

## Visual result

Full-context pages 26-33 and hint pages 183-184 were rendered at 150 dpi and
inspected. All 13 figures, directed-angle arcs, the two-figure wrap, late
`pic-838`, dense `pic-34`, circle criterion and translated hint column are
present and legible. There is no clipping, overlap, lost formula, broken wrap,
missing figure or header collision. Page 33 is a legitimate short final page.
English Chapter 4 begins on page 34 and in the facing hint column on page 183;
therefore this full-context PDF is QA evidence only, not a release artifact.
After terminology normalization, final pages 31 and 183 were rerendered and
reinspected with no reflow or legibility regression.

The PDF is untagged. Accessibility is not claimed for it; the required semantic
HTML/EPUB layer remains separate work.

## Backend result

JSON Schema validation passes for 103 unique records and 65 unique relations;
all relation endpoints resolve. Chapter 3 adds five section rows, 12 result
records, nine exercise rows, eight author-hint links, 13 Indonesian figure
descriptions and 16 concept/dependency rows. All four CSVs parse as UTF-8
without BOM, LF-only, and with a terminal newline. Key hashes:

- `catalog-v0.json`: `3df2f1ea21cbd2ca96712fe5f7ad68f9c57f3cddd2670b4f8f1771637cdd5c82`;
- `unit-order-v0.csv`: `3450e6107632787424958b5f21830de23915150c424cddab0bdf2c071780b55f`;
- `exercise-hints-v0.csv`: `9baca1696d35549b24f28da6065aadd4dbc823c4285b96625fa3e3c32d7bccf8`;
- `figure-descriptions-id-v0.csv`: `13705f53f6021f3a3f466f134e6f7c3539c4781f202f4a9a74e1774cbab71d9c`;
- `concepts-ch03-id-v0.csv`: `54b2aba0a2da38d7df8251d0bd784f11b512e327881bedc82a5208e1cb5ce25b`.

## Preserved upstream observations

Potential upstream defects remain recorded separately and were not silently
changed: the `X,Y` versus `P,Q` inconsistency in the opposite-side definition,
`s(\beta,r)` in `pic-32` versus textual `s(r,\beta)`, historic misspelled stable
labels, and the misplaced `\centering` declaration after `pic-22`. No upstream
message was sent.
