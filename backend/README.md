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
state. The current catalog has 201 unique records and 122 relations with no
dangling endpoints.

Serialization rules: UTF-8 without BOM, LF, two-space indentation, object keys
in the checked-in order, arrays in source order, one terminal newline.  A
canonical SHA-256 is recorded after each admitted boundary.  The schema is
`schema-v0.json`.
