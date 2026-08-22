# O004 additive backend

`catalog-v0.json` is the canonical deterministic UTF-8 view for the current
production boundaries.  It does not replace LaTeX labels or alter the reader.
Locale-neutral IDs map the source topology, exercises, hints, figures, rights,
and build evidence so a later curriculum backend can import this lane without
reconstructing identity from translated titles or page numbers.

Status values distinguish admitted reader/translation records from additive
concept and axiom mappings that still await backend-specific review. Chapter 2
reader records were admitted after structural, render, and visual QA; a pending
mapping remains evidence of preserved identity, not an admission claim.

Per-chapter concept tables preserve reader terminology and the printed/source
identity of axioms.  In Chapter 2, the source's printed Axioms I--V retain their
Roman numbering while `def:birkhoff-axioms:0` through `:4` remain the exact
LaTeX source labels; neither identity is normalized into the other.

Chapter 3 adds explicit `absolute_geometry` flags for every result, preserves
all nine exercise IDs and eight authored hint links, and records the intentional
absence of a source hint for `ex:angle-measures`. Its concept table carries the
prerequisite graph from oriented-angle signs through half-planes, Pasch's
theorem, triangle existence, and the circle-intersection criterion.

Chapter 4 adds six ordered sections, four neutral-geometry results, five
exercise-hint pairs, one synthetic ID for the unlabeled worked construction
problem, ten described figures, and fifteen concept/dependency rows. The
catalog records the deliberate layout-only reflow of `pic-445` through
`pic-449`: all five panels and their order are preserved, but the overflowing
side wrap is replaced by a visually verified two-row sequence.

Chapter 5 adds seven ordered sections, eight result records, eighteen exercise
rows, and seventeen authored hint records. Exercises 17 and 18 intentionally
share the final hint record because the source presents their guidance in one
combined block. The exercise kind `advanced-classroom-exercise` preserves both
the source's advanced flag and classroom designation for `ex:3-reflections`.
Twenty-six concept/dependency rows cover perpendicularity, reflections and
orientation, point-line distance, triangle types, and circle tangency. Fourteen
figure descriptions cover nine body figures and five hint figures; all are
visually admitted. The catalog also preserves the two misspelled exercise IDs
and the stray distance label, records four bounded prose clarifications, and
records the admitted layout-only short running title. Chapter 5 reader,
exercise, hint, result, figure, build-artifact, and QA records are admitted;
concept mappings remain `mapped-pending-qa` as an additive backend review
state. The admitted Chapter 5 boundary has 201 unique records and 122
relations with no dangling endpoints.

Chapter 6 adds four ordered sections, four result records, eight
exercise-hint pairs, four body-figure descriptions, and twenty-two
concept/dependency rows. The unlabeled reformulation of Axiom V receives a
synthetic locale-neutral result ID; the three source-labeled results retain
their LaTeX IDs. Reader, exercise, hint, result, and figure records are admitted
after structural, build, and visual QA, while all twenty-two concept mappings
remain `mapped-pending-qa`. The catalog preserves the legacy chapter label
`chap:parallel`, records the `k=1` distinctness conflict in `ex:k*triangle`, and
retains `thm:signs-of-triug` as a legacy identifier. The commented-out
`ex:footpoints` body and its inactive hint containing `\triange` remain inactive
source surfaces and are excluded from the active exercise-hint closure. The
admitted localized Ptolemy-proof clarification states explicitly which angle
is added to each side of an equality and changes no mathematics. The
full-context PDF remains private, mixed-context, untagged QA evidence rather
than a public reader. The admitted Chapter 6 boundary brings the catalog to 240
unique records and 139 relations with no dangling endpoints.

Chapter 7 adds six ordered sections, eight result records, and twenty-four
active exercise labels. The latter comprise twenty-one top-level exercises and
three labeled subparts; they map in source order to twenty-one top-level hint
blocks, so the two `ex:perp-perp` subparts share their parent hint and
`ex:line-coord:parameter` shares the `ex:line-coord` hint. Subpart rows inherit
their parent exercise's advanced and used-later flags rather than claiming
separate source markers. Thirteen body figures and two hint figures are
described, while inactive `pic-92` and `pic-334` remain
excluded with their commented-out exercise. Twenty-nine concept/dependency rows
cover parallelism, transversals, angle sums, parallelograms, coordinate methods,
and Apollonius circles. Stable source identities preserve `chap:angle-sum`,
`ex:smililar+parallel`, and the two `ex:apolonnius` spellings. The catalog
discloses and admits the point-reflection proof incidence correction, both
rhombus-hint corrections, added Apollonius-construction hypotheses,
nondegenerate-quadrangle index keys, the layout-only forced-page-break removal,
and bounded fluency normalization. Chapter 7 reader, exercise, hint, result,
figure, applied-correction, build-artifact, and QA-event records are admitted
after structural, byte-reproducible build, and visual QA; source-note records
remain `upstream-editorial-note-preserved` and all twenty-nine concept mappings
remain `mapped-pending-qa`. The full-context PDF is private, mixed-context,
untagged QA evidence rather than a public reader. This admitted boundary brings
the catalog to 309 unique records and 179 relations with no dangling endpoints.

Serialization rules: UTF-8 without BOM, LF, two-space indentation, object keys
in the checked-in order, arrays in source order, one terminal newline.  A
canonical SHA-256 is recorded after each admitted boundary.  The schema is
`schema-v0.json`.
