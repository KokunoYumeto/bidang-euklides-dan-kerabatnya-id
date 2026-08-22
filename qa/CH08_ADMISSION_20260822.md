# Chapter 8 admission — 2026-08-22

## Boundary

Admitted unit: `o004.petrunin.ch08`, complete Bab 8, *Geometri segitiga*,
plus its complete contiguous author-hint slice. The unit contains six sections,
six labeled results, thirteen exercises, thirteen directly matching authored
hint blocks, nine body figures, and no hint figures or exercise subparts. The
two `\abs` results retain their absolute-geometry marker.

## Exact source identity

- `source/id-ID/triangle.tex`: 15,865 bytes; SHA-256
  `b599ee9baded53dc0c81fe6e0bb6539e5e43e5173d1ba525df5e8885a024f8b6`.
- complete `source/id-ID/hints.tex`: 94,133 bytes; SHA-256
  `fab63adad2acc5dacd44b51724afd9297ffa3a64a9753ad9e5bd22732d899483`.
- Chapter 8 hint slice, target lines 793–871: 3,322 bytes; SHA-256
  `8cba27ea4b834ce686c95e6601044a4f792daae4400094da3e6bcec1fd289187`.
- admitted Chapter 1–7 hint prefix before the Chapter 8 marker: 29,067 bytes;
  SHA-256
  `46c00e637aa948158b9e3ac7a5b38379bb367ec9c90f2c560d010f151c3b814c`.
- untouched Chapter 9+ hint suffix: 61,744 bytes; SHA-256
  `2ea9859cf7143c6f56069ad802df4c1e295839f8729408a0f72ee8884e205afd`;
  byte-identical to authority.
- authority `mppics/pic.mp`: 123,186 bytes; SHA-256
  `616b73cc36d9d7517ae54b8948a982469829988280d5cf22dfb634f3081129f3`.
- localized `source/id-ID/mppics/pic.mp`: 123,186 bytes; SHA-256
  `567a0e33c5addabb995ce0d283984cba768606b0819a92a3ead5b83dc596cef1`;
  the only differences are the three reader-visible labels in figure 108.

## Structural and editorial gate

`scripts/qa_ch08.py` is 27,549 bytes, SHA-256
`e23817fde9160e2a03f9714d59e45e8639ac5585580dfba76a03637e8ae6bf7f`.
Its normalized fresh output is byte-identical to
`qa/CH08_STRUCTURAL_QA_20260822.json`: 9,468 bytes, SHA-256
`7d2f9f8ef2ef6d63a676327d3240ff6705b5c4a1cf8acba9df2d78e6e0950ffd`.
The receipt passes frozen authority/target hashes, ordered command,
environment, label, reference, graphic, theorem, proof, index, marker, and
formula topology; all thirteen exercise–hint pairs; encoding/whitespace;
external-reference closure; active-language checks; and the frozen prefix and
suffix.

The following decisions are disclosed and indexed in the backend:

1. Immutable misspelled source IDs `ex:midle` and `ex:ext-disect` remain
   unchanged.
2. The source lists `\angle ABC`, `\angle BCA`, and `\angle CAB` but assigns
   them respectively to vertices A, B, and C. The reader corrects the prose to
   vertices B, C, and A while preserving the displayed angle order.
3. The incenter proof's reference to “the same lemma” is rendered as “the same
   proposition,” matching `prop:angle-bisect-dist`.
4. The source's external/exterior-bisector variation is consistently rendered
   as `garis bagi luar`.
5. The dual source sense of *altitude* is preserved explicitly as the line
   `garis tinggi` and the distance `tinggi`.
6. The Euler-line hint's bare “Read about homothety” is preserved and recorded
   as a self-study dependency for the solutions/mastery layer.
7. External reference `ex:abs-bisect=median` is preserved and resolves in the
   complete source closure.
8. Hint-only term *excenter* is localized and indexed as `eksenter`.
9. Figure `pic-108` originally retained visible English labels. Its two
   `bisector` strings are localized to `garis bagi`, and its `external` string
   to `luar`, so the paired labels read `garis bagi luar`; geometry,
   coordinates, marks, and figure order are unchanged.

The tracked overlay `scripts/apply_figure_localizations.ps1` is 1,603 bytes,
SHA-256
`83abf9446c6fea42dbe3a43885bad2983e2b5062a2ea5e5de4c8e83e0317b6f4`.
It is idempotent and hash-gated: it patches an exact fetched authority copy or
verifies the already-localized live closure, without redistributing the
unresolved MetaPost dependencies.

No high-confidence mathematical error beyond the vertex-correspondence prose
error was found in the bounded chapter and hint slice.

## Deterministic build and visual gate

Fresh builds `build/ch08-final-c-20260822` and
`build/ch08-final-d-20260822` are byte-identical:

- 209 pages; 2,677,012 bytes; SHA-256
  `ca38d7112aa685020094760b3d91c8511cc926eaff73c8fe1db27446400cfdfc`;
- 224 MetaPost outputs per build and zero cross-build mismatches;
- localized `pic-108.mps`: 22,274 bytes; SHA-256
  `7801282b8ef71e335f8da9ee426d69a1d255adbb9cabcdbcf7819179d8c72532`;
- normalized CC badge SHA-256
  `7167e45adcc360f116b77210a2e452308e2b8fffd84106f1ea69045cb5be9928`;
- normalized H2checkers SHA-256
  `61a45915d8630a8df63bd9b9ecb095ab9fe6d6671b3360f814bea97ce9a8d885`;
- zero undefined references, undefined citations, or fatal errors;
- 63 global overfull and 41 global underfull boxes plus the one inherited
  group warning; Chapter 8 contributes eight overfull and two underfull boxes.

Physical PDF pages 65–73 and 191–193 were rendered at 150 dpi and inspected.
All nine body figures, headings, running heads, page numbers, equations,
wrapping, glyphs, and hint columns are legible, with no clipping, overlap,
collision, or off-page content. The initial visual pass rejected the English
labels in `pic-108`; the rebuilt page 68 independently passed after localization.
The Chapter 9 body and hint boundaries remain intentionally English QA context.
The full-context PDF is untagged and mixed-language after Chapter 8; it is
private QA evidence, not a public or accessible final reader.

A fresh proof build through the updated figure-localization harness reproduced
the admitted PDF hash exactly; its disposable output directory was then
removed.

## Backend and continuation

The admitted backend has 360 unique records and 209 relations, with no
duplicate IDs or dangling endpoints. Final hashes:

- `backend/catalog-v0.json`: 174,380 bytes; SHA-256
  `238a0bd84e574aa56d568db98951d24635bb981ec778aff39837b9b67d9786aa`;
- `backend/unit-order-v0.csv`: 3,669 bytes; SHA-256
  `7c3bb6754450c90289b6949b5b7082af8105dbdbe380bc96ded48f8a62b55a32`;
- `backend/exercise-hints-v0.csv`: 12,521 bytes; SHA-256
  `d31aecadd965aba1197ff432479ee17effa49d487472bec174aaabe0cf43cdba`;
- `backend/figure-descriptions-id-v0.csv`: 23,363 bytes; SHA-256
  `3aad60a5b0b286acc2e519bd0144ffc7fc31fd23385dcef222c5d2272982b247`;
- `backend/concepts-ch08-id-v0.csv`: 3,304 bytes; SHA-256
  `8618062b7610f7c8eaf55ea68b2ebc829dcb05a2502ecd9a90d2afbfb5854caa`.

All backend CSVs are UTF-8 without BOM, LF-terminated, rectangular, and have
unique first-column keys within each file. Exact artifact and receipt existence/byte/hash
checks pass. Chapter 8's twenty-one concept mappings remain
`mapped-pending-qa` by design; reader, result, exercise, hint, figure, applied
correction, artifact, and QA records are admitted, while five source,
dependency, and accessibility notes remain explicitly preserved.

The next exact cursor is Chapter 9, `inscribed-angle.tex`, and its contiguous
hint slice. GitHub remains private and Zenodo record `22044358` remains
file-restricted; this admission changes neither visibility state.
