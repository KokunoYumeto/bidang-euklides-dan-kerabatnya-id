# Source authority and bounded selection

## Official identity

- Author: Anton Petrunin.
- Official work page: <https://anton-petrunin.github.io/birkhoff/>
- Official repository: <https://github.com/anton-petrunin/birkhoff>
- Labeled publication: <https://arxiv.org/abs/1302.1630v25>
- arXiv v25: third edition, tenth printing, revised 2025-07-07,
  ISBN 978-1650229676.
- GitHub edition-anchor commit: `f5c74ca043be7bca9d59c55e17b98d272d6161f4`,
  whose message identifies the tenth printing with arXiv v25.
- Current working commit: `0b0858e1e985f4c8dadbb6075ae9e095cd4a8981`.
- Current working tree: `4c931765feb8e83b77b079e618b994a74efa5cf3`.
- Current commit time: 2025-12-19T02:42:10Z; message `bookmark`.

The current repository snapshot is later than v25 and is not labeled as a new
printing or edition.  It is used as an intentional post-printing working
revision because this lane was instructed to freeze the exact current revision.
The v25 source and PDF remain the edition-fidelity witnesses.

## Frozen bytes

| Object | Bytes | SHA-256 |
|---|---:|---|
| immutable current-commit ZIP | 532177 | `ef6142598854078fe3d9777005b5aff49ee0d5c70b17acebce876398c8b71081` |
| arXiv v25 PDF | 3003618 | `8797bcfa4ec4457aa7a7561d6b246c0e61deea02cb377b8828cee0b1da28f282` |
| downloaded arXiv v25 source response | 3306215 | `0dd8863fc75aebaa13f9b817fc5ec5a10ac6220bef7b8b789d4959989f62886f` |
| uncompressed arXiv v25 source tar | 9154560 | `fc3f127f5a1a4b15c95c74f960ca7dff6ea55e31bc0635d748140c095214c5d6` |

The immutable current-commit archive contains 41 regular files.  The active
body driver is `all-lectures.tex`; it never inputs `cover/cover.tex`.  The arXiv
source contains 242 regular files, including generated MetaPost figures, and no
P22 fonts or external cover.

## Bounded comparison

The selection comparison stopped after three genuinely relevant candidates:

1. Petrunin: official editable LaTeX/MetaPost source, CC BY-SA 4.0 body,
   semester-scale foundations course, 20 chapters spanning Euclidean,
   inversive, neutral/hyperbolic, affine, projective, spherical, construction,
   and area topics, with a large exercise/hint apparatus.  It passes when the
   separate font-bearing cover is excluded and component rights are preserved.
2. Michael P. Hitchman, *Geometry with an Introduction to Cosmic Topology*:
   official PreTeXt reader and CC BY-SA 4.0, with more than 200 exercises and
   strong Euclidean/hyperbolic/elliptic coverage, but its cosmological/Möbius
   route does not supply the same affine/projective/foundational spine.
3. George E. Martin, *The Foundations of Geometry and the Non-Euclidean Plane*:
   strong 512-page curricular coverage, but the official Springer record is
   subscription/copyright publication and supplies neither public editable
   authoring source nor derivative permission for this lane.

Petrunin therefore remains the strongest lawful core.  Missing semantic-reader
and mastery surfaces are additions around this core, not a reason to replace it.

