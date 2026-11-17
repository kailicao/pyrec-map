## Explanation

**Purpose.** `NEWOPAC_MOD` holds two switches of the opacity setup, shared by 4 routines. It replaces what is left of `COMMON/NEWOPAC/` (MHP via Claude, 10/14/26), into which `/MISCOPAC/` and `/NWLAOL/` had been merged on 9/24/26: the opacity choices and their $`Z`$ and temperature limits (`ZOPAL951`, `TMOLMIN`, `TMOLMAX`, `LALEX06`, `LOPAL95`) are namelist variables now in [`NMLPAR_MOD`](nmlpar_mod.f.md#nmlpar_mod), and the members of obsolete tables (`ZLAOL1`, `ZOPAL1`, `ZALEX1`, `ZKUR1`, `LLAOL89`, `LOPAL92`, `LKUR90`, `LALEX95` and their pairs) were removed with those options.

**What its variables hold, who sets them, who reads them.** Both are `LOGICAL*4`.
- `L2Z`: whether two opacity tables in $`Z`$ are needed, `LZRAMP .OR. LDIFZ`, set by [`SETUPOPAC`](setupopac.f.md#setupopac); read by [`GETOPAC`](getopac.f.md#getopac) in its test of whether the local $`Z`$ is covered by the tables (a $`Z`$ far from `ZENV` is accepted only with `L2Z` or `LOPAL95`).
- `LLAOL`: the switch of the obsolete LAOL opacities, initially `.FALSE.` (moved from PARMIN's `DATA` statement) and set nowhere, so [`STARIN`](starin.f.md#starin) always takes the element fractions from `VNEW` rather than from the LAOL tables (its comment: "to maintain backward compatibility," [starin.f, lines 910–916](https://github.com/yreclab/yrec/blob/7be4133/src/starin.f#L910-L916)); unused? (a switch that cannot be turned on, for tables that were removed).

**Design.** A blanket `USE NEWOPAC_MOD`; [`PARMIN`](parmin.f.md#parmin) still uses the module but reads neither member. The module header calls `LLAOL` a namelist variable, but it is in no namelist (so also at `rp_1`).

**Changed since `rp_1`.** New file: `L2Z` of `COMMON/NEWOPAC/` and `LLAOL` of `/NWLAOL/` as a module; the namelist members moved to `NMLPAR_MOD`, those of removed opacity tables deleted.
