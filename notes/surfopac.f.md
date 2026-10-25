## Explanation

**Purpose.** `SURFOPAC` sets up the opacity tables for the surface hydrogen abundance $X$ (`XENV`): it calls the routine that interpolates each table family in $X$, for the families switched on in COMMON `NEWOPAC`. Its comment says the tables must already have been read.

**How it fits.**
- **Who calls it:** [[starin.f#STARIN|STARIN]], when the starting model is ready, and [[hpoint.f#HPOINT|HPOINT]], when the surface $X$ (`HCOMP(1,M)`) has changed by more than $10^{-8}$.
- **What it calls:** [[op95xtab.f#OP95XTAB|OP95XTAB]] (OPAL95, if `LOPAL95`), [[ll4th.f#LL4TH|LL4TH]] (OPAL92 at `ZOPAL1` and `ZOPAL2`, if `LOPAL92`) and [[alx8th.f#ALX8TH|ALX8TH]] (the Alexander 1995 low-temperature tables, if `LALEX95`).
- **COMMON blocks:** `NEWOPAC`, the opacity switches set by [[parmin.f#PARMIN|PARMIN]] and [[setupopac.f#SETUPOPAC|SETUPOPAC]].

## Questions for the experts

1. **The other table families.** Only OPAL92, OPAL95 and Alexander 1995 are set up here; the switches `LALEX06`, `LLAOL89` and `LKUR90` are in the same COMMON block. Do those tables need no surface-$X$ set-up?

### SURFOPAC

Interpolates the switched-on opacity tables (OPAL95, OPAL92, Alexander 1995) to the surface $X$.
