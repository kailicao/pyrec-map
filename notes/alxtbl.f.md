## Explanation

**Purpose.** This file reads the older Alexander low-temperature opacity tables (its comment cites Alexander and Ferguson, ApJ 437, 879, 1994): 7 files, one per hydrogen abundance $X$ = 0, 0.1, 0.2, 0.35, 0.5, 0.7 and 0.8, each holding 15 tables in $Z$ from 0 to 0.10. Each table covers $\log T$ = 3.00 to 4.10 (23 values) and $\log R$ = −7.0 to 1.0 (17 values), with $R = \rho / T_6^3$.

**How it fits.**
- **Input:** the 7 files named in `OPECALEX`, opened on unit `IALXO` (`/ALEXO/`, set to 39 in [[parmin.f#PARMIN|PARMIN]]).
- **Who calls it:** [[setupopac.f#SETUPOPAC|SETUPOPAC]], at start-up.
- **What it calls:** [[alxztab.f#ALXZTAB|ALXZTAB]], with `ZALEX1` from `/NEWOPAC/` (the metallicity at which the Alexander tables are used).
- **Output:** all 105 tables in `CAPTALEX` (`/ALOTALL/`, shared with ALXZTAB); the grid `TGR`, `XXG`, `R0GR`, `ZZG` in `/GALOT/` (shared with [[alx8th.f#ALX8TH|ALX8TH]], ALXZTAB and [[yalo3d.f#YALO3D|YALO3D]]), set here by DATA statements; through ALXZTAB, the 7 fixed-$Z$ tables in `/ALOT/`.
- **COMMON blocks:** also `/NEWOPAC/`, the opacity options shared with 17 routines, and `/LUOUT/`.

**The method.** For each file (fixed $X$), read the 15 tables in descending $Z$ and, within each, the 23 rows in descending $T$. Each table is stored at index $i = i_X + 7\,(i_Z - 1)$, so that the 7 values of $X$ at one $Z$ are adjacent. Each header's $X$, $Z$ and each row's $\log T$, number of densities and first $\log R$ are checked against the grid; a mismatch stops the run. Then [[alxztab.f#ALXZTAB|ALXZTAB]] interpolates to $Z$ = `ZALEX1`. The comment says a surface-$X$ table is then built "if model has no diffusion"; that step is in the caller, which calls [[alx8th.f#ALX8TH|ALX8TH]].

**Design.** The grid is fixed by DATA statements; tables of another size need a code change. The DATA statement also initializes the search indices `XE`, `ZE`, `IX`, `IT`, `ID` of `/ALOT/`.

## Questions for the experts

1. **`IT` overwritten.** The read `READ(IALXO,30) IT,ND,T,R0,…` stores the row's first integer in `IT`, which is the search index that [[yalo3d.f#YALO3D|YALO3D]] keeps in `/ALOT/` (initialized to 12 by DATA). After reading, `IT` holds the last value from the file. YALO3D clips `IT` into range, so this is probably harmless, but was a local variable meant?
2. **One or two values of $Z$.** The header says the routine generates entries "at either one or two fixed values of Z", but it builds one, at `ZALEX1`; `ZALEX2` is still in `/NEWOPAC/` (PARMIN) but appears elsewhere only in comments. Is the second value meant to return, or should the header be updated?

### ALXTBL

Reads the 7 files of Alexander opacities (105 tables) into `/ALOTALL/`, checks the grid, and calls [[alxztab.f#ALXZTAB|ALXZTAB]] for $Z$ = `ZALEX1`.
