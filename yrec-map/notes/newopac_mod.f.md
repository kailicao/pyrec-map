## Explanation

**Purpose.** `NEWOPAC_MOD` holds two switches of the opacity setup, shared by 4 routines. It replaces what is left of `COMMON/NEWOPAC/` (MHP via Claude, 10/14/26), into which `/MISCOPAC/` and `/NWLAOL/` had been merged on 9/24/26: the opacity choices and their $Z$ and temperature limits (`ZOPAL951`, `TMOLMIN`, `TMOLMAX`, `LALEX06`, `LOPAL95`) are namelist variables now in [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]], and the members of obsolete tables (`ZLAOL1`, `ZOPAL1`, `ZALEX1`, `ZKUR1`, `LLAOL89`, `LOPAL92`, `LKUR90`, `LALEX95` and their pairs) were removed with those options.

**What its variables hold, who sets them, who reads them.** Both are `LOGICAL*4`.
- `L2Z`: whether two opacity tables in $Z$ are needed, `LZRAMP .OR. LDIFZ`, set by [[setupopac.f#SETUPOPAC|`SETUPOPAC`]]; read by [[getopac.f#GETOPAC|`GETOPAC`]] in its test of whether the local $Z$ is covered by the tables (a $Z$ far from `ZENV` is accepted only with `L2Z` or `LOPAL95`).
- `LLAOL`: the switch of the obsolete LAOL opacities, initially `.FALSE.` (moved from PARMIN's `DATA` statement) and set nowhere, so [[starin.f#STARIN|`STARIN`]] always takes the element fractions from `VNEW` rather than from the LAOL tables (its comment: "to maintain backward compatibility").

**Design.** A blanket `USE NEWOPAC_MOD`; [[parmin.f#PARMIN|`PARMIN`]] still uses the module but reads neither member. The module header calls `LLAOL` a namelist variable, but it is in no namelist (so also at `rp_1`).

**Changed since `rp_1`.** New file: `L2Z` of `COMMON/NEWOPAC/` and `LLAOL` of `/NWLAOL/` as a module; the namelist members moved to `NMLPAR_MOD`, those of removed opacity tables deleted.

## Questions for the experts

1. **A switch that cannot be turned on.** `LLAOL` is set nowhere, and the LAOL tables it served were removed. Can it go, with STARIN's test?
