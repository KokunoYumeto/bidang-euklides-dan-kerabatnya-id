# Chapter 7 admission — 2026-08-22

## Boundary

Admitted unit: `o004.petrunin.ch07`, complete Bab 7, *Garis sejajar*, plus its
complete contiguous author-hint slice. The unit contains six sections, eight
result blocks, twenty-one top-level exercises, three labeled exercise
subparts, twenty-one authored hint blocks, thirteen body figures, and two hint
figures. The `ex:line-coord:parameter` subpart is covered by its parent
`ex:line-coord` hint; no hint was invented. Inactive `pic-92`, `pic-334`, and
their commented exercise/hint remain inactive.

## Exact source identity

- `source/id-ID/parallel.tex`: 22,352 bytes; SHA-256
  `3459de730c56922fe4a9e30781d3a12ce1671c735423f5eaed12175d9d5d5385`.
- complete `source/id-ID/hints.tex`: 93,843 bytes; SHA-256
  `345caa2579bb9c9781d5c9f5426ddf25e710f4b5cfe6eff71440b6a6ca811cde`.
- Chapter 7 hint slice, target lines 608–792: 6,855 bytes; SHA-256
  `1a914474041c1a1fb05a3b7f2cd46c8da279431de7d08e39ed9f72e770532280`.
- admitted Chapter 1–6 hint prefix: 22,212 bytes; SHA-256
  `29fc07469fbb866904cf168bc758a794eaa22baad34e9fd8cf947f0a55fedabb`.
- untouched Chapter 8+ hint suffix: 64,776 bytes; SHA-256
  `4f3df5cb98e16c929468bcb8624e9851d4442440a03e87624d27113190238de1`;
  byte-identical to authority.

## Structural and editorial gate

`scripts/qa_ch07.py` is 39,549 bytes, SHA-256
`876c532557f34f0b03e02b649c53fbdf0985ad12677e770c8f7d4237b927d1d9`.
Its normalized fresh output is byte-identical to
`qa/CH07_STRUCTURAL_QA_20260822.json`: 17,596 bytes, SHA-256
`77e43446acb920dfb54855e417c98df8deb56ef9332eac537eefb7780e435de1`.
The receipt passes source/target topology, labels, references, graphics,
exercise–hint closure, formulas, inactive surfaces, translated-language
checks, and the frozen prefix/suffix checks.

The following deliberate changes are disclosed and indexed in the backend:

1. The point-reflection only-if proof says the reflected line and `m` pass
   through `Q`, correcting the authority's inconsistent `P`.
2. The `ex:romb` hint uses `D\ne B`, correcting `D\ne C` in the angle-sign
   argument.
3. The `ex:romb2` hint begins with the adjacent-side condition `AB=AD`,
   correcting the automatically true parallelogram equality `AB=CD`.
4. The Apollonius construction adds `A\ne B`, `M\notin\{A,B\}`, and
   `AM\ne BM`, the hypotheses needed for the requested nondegenerate circle.
5. Both index keys attached to the nondegenerate-quadrangle definition use
   *nondegenerate* rather than *degenerate*; displayed mathematics is unchanged.
6. The unexplained inherited `\pagebreak%???` is omitted and the following
   visible heading receives a one-em inset. This is a layout-only reflow.
7. Reader-facing Indonesian fluency, punctuation, and referent order are
   normalized without changing mathematical meaning or source order.

The legacy `chap:angle-sum`, `ex:smililar+parallel`, and both
`ex:apolonnius` identifiers remain unchanged. The inactive signed-`pi/4`
exercise and hint remain preserved and are recorded as a source note.

## Deterministic build and visual gate

Fresh builds `build/ch07-final-e-20260822` and
`build/ch07-final-f-20260822` are byte-identical:

- 208 pages; 2,968,464 bytes; SHA-256
  `7fa21a42a1cdf4d78db3b1b1ae9d8db3e58ae50c3091264f4402f4b54aa0b448`;
- 224 MetaPost outputs per build and zero cross-build mismatches;
- zero undefined references, undefined citations, or fatal errors;
- 55 global overfull and 39 global underfull boxes plus the one inherited
  group warning; Chapter 7 contributes six overfull and three underfull boxes.

Body pages 55–65 and hint pages 189–190 were rendered at 150 dpi and inspected
independently. All figures, equations, headings, margins, headers, wraps, and
glyphs are legible, with no clipping, overlap, off-page content, or collision.
The full-context PDF is untagged and contains untranslated Chapter 8+ material;
it is private QA evidence, not a public or accessible final reader.

## Backend and continuation

The admitted backend has 309 unique records and 179 relations, with no
duplicate IDs or dangling catalog endpoints. Final hashes:

- `backend/catalog-v0.json`: 147,134 bytes; SHA-256
  `6f95311d71e024afeba3fcec49f0234a7c1bac2334b6adc0f44466ec3321a04a`;
- `backend/unit-order-v0.csv`: 3,184 bytes; SHA-256
  `158c9cb259d6f1e95c3585c52c8305b0920da13a95474910c403e6bba988cb1a`;
- `backend/exercise-hints-v0.csv`: 10,801 bytes; SHA-256
  `3671353367bdfb5910c7627f49af7168a22b38f4bda3164c8e98b7d4556559f5`;
- `backend/figure-descriptions-id-v0.csv`: 20,656 bytes; SHA-256
  `ff65ab8a47cad26b29f1ae172a474d630f2679359601d643dadc85ca969bc620`;
- `backend/concepts-ch07-id-v0.csv`: 5,674 bytes; SHA-256
  `be769025e24b8c35693602ab315c0038f4725dcc5b058ed86494f0ba260a2f98`.

All ten backend CSVs are UTF-8 without BOM, LF-terminated, rectangular, and
unique in their first-column IDs. Chapter 7 prerequisite IDs close across the
per-chapter CSV universe; Chapter 7's twenty-nine concept mappings remain
`mapped-pending-qa` by design. Artifact-tool import, inspection, rendering, and
visual review passed for all Chapter 7-facing CSV ranges.

The next exact cursor is Chapter 8, `triangle.tex`, and its contiguous hint
slice. GitHub remains private and Zenodo record `22044358` remains
file-restricted; this admission changes neither visibility state.
