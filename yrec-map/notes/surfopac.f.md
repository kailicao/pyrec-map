## Explanation

**Purpose.** `SURFOPAC` sets up the opacity tables for the surface hydrogen abundance $`X`$ (`XENV`): if the OPAL 1995 tables are switched on (`LOPAL95`), it calls the routine that interpolates them in $`X`$. Its comment says the tables must already have been read. The low-temperature tables of Ferguson et al. ([2005](https://ui.adsabs.harvard.edu/abs/2005ApJ...623..585F)) (`LALEX06`), now the only molecular tables, need no set-up here: [GETALEX06](getalex06.f.md#getalex06) rebuilds their table itself, through [ALEX06TAB](alex06tab.f.md#alex06tab), whenever the $`X`$ or $`Z`$ of a point differs from that of the current table by more than $`10^{-8}`$ (settled from the code, Nov 9, 2026: [getalex06.f, lines 26–33](https://github.com/yreclab/yrec/blob/7be4133/src/getalex06.f#L26-L33)).

**How it fits.**
- **Who calls it:** [STARIN](starin.f.md#starin), when the starting model is ready, and [HPOINT](hpoint.f.md#hpoint), when the surface $`X`$ (`HCOMP(1,M)`) has changed by more than $`10^{-8}`$.
- **What it calls:** [OP95XTAB](op95xtab.f.md#op95xtab) (OPAL95, if `LOPAL95`).
- **Modules:** [NMLPAR_MOD](nmlpar_mod.f.md), for the namelist switch `LOPAL95`, read by [PARMIN](parmin.f.md#parmin).

**Changed since `rp_1`.** The OPAL 1992 and Alexander 1995 (the code's name for the tables of Alexander & Ferguson [1994](https://ui.adsabs.harvard.edu/abs/1994ApJ...437..879A)) tables were removed from the code, and with them the calls to `LL4TH` and `ALX8TH`; COMMON `NEWOPAC` gave way to `NMLPAR_MOD`; `IMPLICIT NONE`. Question 1 of `rp_1` (why the Alexander 2006 (the code's name for the tables of Ferguson et al. [2005](https://ui.adsabs.harvard.edu/abs/2005ApJ...623..585F)), LAOL 1989 and Kurucz 1990 (the code's name; probably the opacities of Kurucz [1991](https://ui.adsabs.harvard.edu/abs/1991ASIC..341..441K), “New Opacity Calculations”) tables need no surface-$`X`$ set-up) is settled in part: LAOL 1989 and Kurucz 1990 are gone, so only Alexander 2006 remains, and the question is narrowed to it.

### SURFOPAC

Interpolates the OPAL 1995 tables to the surface $`X`$, if they are switched on.
