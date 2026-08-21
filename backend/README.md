# O004 additive backend

`catalog-v0.json` is the canonical deterministic UTF-8 view for the first
production boundary.  It does not replace LaTeX labels or alter the reader.
Locale-neutral IDs map the source topology, exercises, hints, figures, rights,
and build evidence so a later curriculum backend can import this lane without
reconstructing identity from translated titles or page numbers.

Serialization rules: UTF-8 without BOM, LF, two-space indentation, object keys
in the checked-in order, arrays in source order, one terminal newline.  A
canonical SHA-256 is recorded after each admitted boundary.  The schema is
`schema-v0.json`.

