# Chapter 5 admission — 2026-08-22

## Boundary

Complete Bab 5, *Garis tegak lurus dan transformasi isometrik*, and its exact
authored hint slice are admitted. The unit contains seven sections, eight
results, eighteen exercises, nine body figures, and seventeen author hint
blocks with five hint figures. The final source hint deliberately covers both
`ex:tangent` and `ex:tangent-circle`; all eighteen exercises therefore have
source-hint coverage. The next source-order cursor is Chapter 6, `similar.tex`.

Authority `perp.tex` is 16,499 bytes, SHA-256
`c5be147e0249d3c7ffe5f2432cdd11b5e686e808927661de57614c55bfc28f91`.
The admitted target is 17,849 bytes, SHA-256
`650ffbc55d59c238dc7c884bc3d0765ecae6e2fdab953d5390fb27ceb09446ed`.
The authority hint slice is 5,290 bytes, SHA-256
`80f7d0508c31e8a2dbdf3826814658b98ba551ac427f1d6a3955311f4502044e`;
the target slice is 5,770 bytes, SHA-256
`d2788d7d1095d838d733533750e3bc6fe4d6de00bad2669be21f67f8988894de`.
The complete target `hints.tex` is 92,831 bytes, SHA-256
`0d0f48fcc22abd8ed8e2a067b2b30d27c15003ba2cad549fd0cc0135e9c6dc8c`.
The frozen Chapter 1–4 prefix is 14,089 bytes, SHA-256
`c6d71d57ad3753572e380e673c6d60f55cb10540dc3c5918f0c66a4f58f64245`;
the Chapter 6+ suffix remains byte-identical to authority at 72,972 bytes,
SHA-256
`0d0735b595811fea0fb1bb90103e8a99521e0b2d44170bae9b2d89862c743114`.

## Structural and language gate

`scripts/qa_ch05.py` passes and writes
`qa/CH05_STRUCTURAL_QA_20260822.json`. Their SHA-256 values are
`bf038766990caafb9ee079135ca11d17efe18a0fda78759bb2a670c61ee038b5`
and
`e7136be9817e68ecfa871f10330eccf9912a4804999408f0f3d3d649736617e7`.
Ordered environment boundaries, labels, equation labels, references,
citations, graphics, theorem options, proof closures, exercise markings, and
comment topology agree with authority. The active body census is 80
environment boundaries, 34 labels, four equation labels, 22 references, zero
citations, nine graphics, 26 theorem options, seven proof closures, seven
sections, 25 index entries, seven `abs` markers, and seven later-use markers.
The hint census is 16 environment boundaries, 44 active references (45 raw),
five graphics, and 82 active math surfaces.

The authority has 334 active math surfaces and the target 333. The sole
deliberate omission is authority surface 176, an undefined `$f$`: the paragraph
introduces `X\mapsto X'` and then unexpectedly refers to `f`. The Indonesian
text says `transformasi isometrik tersebut`, preserving the evident referent
without inventing a symbol. Three further bounded wording clarifications make
the construction extend a perpendicular segment rather than an infinite line,
pair `m` and `n` respectively with the perpendicular bisectors of `AB` and
`BC`, and attach “through the given point” to the requested tangent lines.
None changes a mathematical claim, formula, label, reference, or exercise.
All Chapter 1–5 QA scripts pass together.

## Running-head repair

The first translated render exposed a collision between the long Indonesian
Section E running head and page number 45. The optional short title `Isometri
langsung dan tak langsung` now serves only the running head; the complete
visible title `Transformasi isometrik langsung dan tak langsung` is retained.
Pixel comparisons show that body pages 41–44 and 46–48 and hint pages 185–187
are unchanged by the repair. Only page 45 changed, and its final render was
inspected separately.

## Deterministic build and visual gate

Fresh directories `build/ch05-final-c-20260822` and
`build/ch05-final-d-20260822` produced identical 207-page PDFs:

- 2,965,782 bytes;
- SHA-256
  `6ca6402e66b5ab0a048697bf0478a00548e1c5a64096d605fbd95947c21994ee`;
- 224 generated MetaPost files with zero cross-build hash mismatches;
- normalized CC badge SHA-256
  `7167e45adcc360f116b77210a2e452308e2b8fffd84106f1ea69045cb5be9928`;
- normalized H2checkers SHA-256
  `61a45915d8630a8df63bd9b9ecb095ab9fe6d6671b3360f814bea97ce9a8d885`.

The converged log has zero undefined references, zero undefined citations, and
no fatal error. It has 44 overfull and 31 underfull boxes globally plus the
inherited group warning. Chapter 5 contributes four overfull and one underfull
diagnostic; visual inspection confirms that none clips or hides content. PDF
pages 41–48 and hint pages 185–187 were rendered at 150 dpi and inspected. All
nine body figures and five hint figures are legible, with no cutoff, overlap,
or missing content.

The full-context PDF contains English Chapter 6+ material and is private QA
evidence, not a release artifact. It is untagged; the required semantic
HTML/EPUB reader remains a later additive accessibility surface.

## Backend gate

The additive backend has 201 unique records and 122 unique relations with zero
dangling endpoints; JSON Schema validation passes. Chapter 5 contributes eight
unit-order rows, eighteen exercise rows, seventeen authored hint records,
twenty-six concept/dependency rows, fourteen admitted figure descriptions,
eight result records, one private full-context build artifact, one QA event,
and five admitted bounded-correction records. The concept rows deliberately
remain `mapped-pending-qa`: this backend-review state does not weaken the
reader, exercise, hint, result, figure, or build admission.

CSV imports verify UTF-8 without BOM, LF endings, terminal newlines, exact
headers, expected row/column counts, and unique primary IDs. Canonical hashes
are:

- `catalog-v0.json`: `ac5ff5b60b45bf7315324effa6784a3b92dda2a0657b406ae45d491324f8f7c2`;
- `unit-order-v0.csv`: `ce0e983eb7cdae10f9e0eecd5b37f29b9e49b243aa0eb0389f89e804fd47e5c3`;
- `exercise-hints-v0.csv`: `32a128ca552dd25c3724d5fbe94fc1d2cc7027a9b8cc88ced36ccfdaff6d4004`;
- `figure-descriptions-id-v0.csv`: `33c1be1f19256c4b35d7fe9d5b81c8f0a8577b88fe2d5ea8d0099a6b55ff6baa`;
- `concepts-ch05-id-v0.csv`: `2738921b0c969bb2ed7d230c294c148dfffbe064b0aaf0877ddd4b5f0b9f7f4e`.

Admission decision: pass. Advance to Chapter 6 without reopening Chapters
1–5. Keep GitHub private and Zenodo files restricted; make no Zenodo version at
this boundary.
