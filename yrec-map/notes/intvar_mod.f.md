## Explanation

**Purpose.** `INTVAR_MOD` holds the structure variables at the interfaces between shells (the midpoints in radius), for the rotation routines, shared by [[setupv.f#SETUPV|`SETUPV`]], [[vcirc.f#VCIRC|`VCIRC`]], [[getfc.f#GETFC|`GETFC`]] and [[seculr.f#SECULR|`SECULR`]]. It replaces `COMMON/INTVAR/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]]. All members are arrays of `JSON`.

**What its variables hold, who sets them, who reads them.** All are set by `SETUPV`:
- `RM`: the radius of the interface between shells `I-1` and `I`, the mean of the two shells' radii.
- At each interface, by four-point Lagrangian interpolation in radius (the first and last interfaces from the first and last four points): `PM`, `TM`, `DM` ($P$, $T$, $\rho$, unlogged), `ALM` ($L$, cgs), `HS3` (the mass), `HGM` (gravity), `DELMI`, `DELAMI` (the radiative and adiabatic gradients), `QDTMI` (a thermodynamic derivative), `EPSILM` (the energy generation rate).
- `SETUPV` uses them to build the circulation coefficients; `VCIRC` reads `RM`, `HGM`, `ALM`; `GETFC` reads `RM`, `DM`; `SECULR` reads `RM`.

**Design.** A blanket `USE INTVAR_MOD`. At `rp_1`, [[codiff.f#CODIFF|`CODIFF`]] also declared the block without using it.

**Changed since `rp_1`.** New file: `COMMON/INTVAR/` as a module (CODIFF's unused declaration dropped).
