## Explanation

**Purpose.** `SURFOPAC` sets up the opacity tables for the surface hydrogen abundance $X$ (`XENV`): if the OPAL 1995 tables are switched on (`LOPAL95`), it calls the routine that interpolates them in $X$. Its comment says the tables must already have been read.

**How it fits.**
- **Who calls it:** [[starin.f#STARIN|STARIN]], when the starting model is ready, and [[hpoint.f#HPOINT|HPOINT]], when the surface $X$ (`HCOMP(1,M)`) has changed by more than $10^{-8}$.
- **What it calls:** [[op95xtab.f#OP95XTAB|OP95XTAB]] (OPAL95, if `LOPAL95`).
- **Modules:** [[nmlpar_mod.f|NMLPAR_MOD]], for the namelist switch `LOPAL95`, read by [[parmin.f#PARMIN|PARMIN]].

**Changed since `rp_1`.** The OPAL 1992 and Alexander 1995 tables were removed from the code, and with them the calls to `LL4TH` and `ALX8TH`; COMMON `NEWOPAC` gave way to `NMLPAR_MOD`; `IMPLICIT NONE`. Question 1 of `rp_1` (why the Alexander 2006, LAOL 1989 and Kurucz 1990 tables need no surface-$X$ set-up) is settled in part: LAOL 1989 and Kurucz 1990 are gone, so only Alexander 2006 remains, and the question is narrowed to it.

## Questions for the experts

1. **Alexander 2006.** Only OPAL 1995 is set up here; the low-temperature tables of Ferguson–Alexander 2006 (`LALEX06`), now the only molecular tables, are not. Do they need no surface-$X$ set-up (that is, does [[getalex06.f#GETALEX06|GETALEX06]] interpolate in $X$ itself)?

### SURFOPAC

Interpolates the OPAL 1995 tables to the surface $X$, if they are switched on.
