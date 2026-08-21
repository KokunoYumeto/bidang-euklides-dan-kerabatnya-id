# Rights and component disposition

## Admitted body

The author repository, `LICENSE.md`, README, and in-book notice state Creative
Commons Attribution-ShareAlike 4.0 International.  The Indonesian adaptation
must credit Anton Petrunin and the work, link the official source and license,
identify translation/layout changes, keep the adaptation under CC BY-SA 4.0 (or
a permitted compatible license), and add no effective technological or legal
restriction.

## Component matrix

| Component | Status | Public disposition |
|---|---|---|
| authored TeX, style, bibliography, ordinary figures | CC BY-SA 4.0 body | admitted with attribution, change notice, and ShareAlike |
| `pics/H2checkers_334.eps` | public-domain source image by Tamfang | retain PD attribution/provenance |
| `pics/by-sa.eps` | official Creative Commons license badge/trademark | use unmodified only to identify the actual CC BY-SA 4.0 license, or replace with text notice |
| `mppics/fiziko.mp` | Sergey Slyusarev, GPL-3.0-or-later | preserve notice and provide GPL text/source if publicly redistributed |
| `mppics/macros.mp` | credits several third-party macro bases; no license stated | source-redistribution blocker until provenance/license is resolved |
| `pic.mp`, `pic-hints.mp` | local generator using `fiziko`, `macros`, `hatching`, `mparrows` | build locally; do not flatten component rights into the book CC notice |
| generated `.mps` figures and body PDF | generated output; no P22 content | admitted for body-only reader, subject to the book/figure provenance recorded here |
| `cover/P22-Underground-Reg.ttf` | proprietary P22 font, all rights reserved | excluded; never redistribute, embed, subset, or derive outlines |
| `cover/P22UndergroundCYBookSC.ttf` | proprietary P22 font, all rights reserved | excluded; never redistribute, embed, subset, or derive outlines |
| `cover/cover.tex` | invokes the excluded P22 fonts | excluded from this derivative |

The root Creative Commons notice cannot grant third-party font or generator
rights that the author does not control.  The official arXiv v25 source and PDF
demonstrate a complete 199-page body path without the external cover or P22
fonts.  This lane follows that safe boundary.

Redistribution of the complete upstream generator closure remains blocked until
`mppics/macros.mp` is resolved and the GPL component is packaged correctly.
This does not block the Indonesian translation overlay, backend, controls, or a
generated body PDF without P22 assets. A public reproduction script may fetch
the exact official archive for local use, verify it, exclude `cover/`, and apply
the separately distributed overlay without republishing the generator files.

## Deterministic generated-asset handling

The build closure converts `pics/by-sa.eps` and
`pics/H2checkers_334.eps` locally, removes conversion-time Info/XMP metadata,
and assigns a stable PDF file identifier derived from each immutable source
EPS. This does not change the assets' rights or provenance. The normalized
outputs are deterministic:

- CC badge: 5,002 bytes, SHA-256
  `7167e45adcc360f116b77210a2e452308e2b8fffd84106f1ea69045cb5be9928`;
- H2checkers: 194,716 bytes, SHA-256
  `61a45915d8630a8df63bd9b9ecb095ab9fe6d6671b3360f814bea97ce9a8d885`.

The CC badge is used only to identify the actual CC BY-SA 4.0 license;
H2checkers retains its public-domain provenance. This deterministic conversion
does not authorize redistribution of `mppics/macros.mp` or either excluded
font.
