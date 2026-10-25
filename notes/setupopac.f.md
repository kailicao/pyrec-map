## Explanation

**Purpose.** Reads the opacity tables chosen for the run and sets up their interpolation. Its comment: "THIS SUBROUTINE READS IN SPECIFIED OPACITY TABLES AND SET UP SPLINES FOR THE TABLES. WHEN LZRAMP=T OR LDIFZ=T THEN READ IN SECOND SET OF OPACITY TABLES AT DIFFERENT Z."

**How it fits.**
- **Who calls it:** [[setups.f#SETUPS|`SETUPS`]], once per run; the file names are passed through (MHP 8/25).
- **What it calls,** by the switches in `/NEWOPAC/`:
  - interior tables: OPAL95, [[ll95tbl.f#LL95TBL|`LL95TBL`]] then [[op95xtab.f#OP95XTAB|`OP95XTAB`]] (`LOPAL95`); OPAL92, [[setllo.f#SETLLO|`SETLLO`]] then [[ll4th.f#LL4TH|`LL4TH`]] (`LOPAL92`); LAOL89, [[rdlaol.f#RDLAOL|`RDLAOL`]] then [[sulaol.f#SULAOL|`SULAOL`]] (`LLAOL89`); the pure-Z LAOL table, [[rdzlaol.f#RDZLAOL|`RDZLAOL`]] then [[zsulaol.f#ZSULAOL|`ZSULAOL`]] (`LPUREZ`, in `/NWLAOL/`);
  - low-temperature tables, one of: Ferguson et al. 2005, [[readalex06.f#READALEX06|`READALEX06`]] (`LALEX06`); Alexander 1995, [[alxtbl.f#ALXTBL|`ALXTBL`]] then [[alx8th.f#ALX8TH|`ALX8TH`]] (`LALEX95`); Kurucz, [[setkrz.f#SETKRZ|`SETKRZ`]] (`LKUR90`).
- **Inputs:** `XENV` (the envelope's $X$, for the tables built at fixed composition) and the file names. Sets `L2Z` = `LZRAMP` or `LDIFZ` (`/ZRAMP/`, `/GRAVS3/`) in `/NEWOPAC/`, which the readers use to decide whether to read a second table.
- **Output:** the argument `V` (the LAOL mix, from `RDLAOL`), and the tables in the COMMON blocks of the routines called. They are used at run time by [[getopac.f#GETOPAC|`GETOPAC`]].

## Questions for the experts

1. **Several interior tables at once.** The interior switches are independent `IF`s, so more than one table can be read (for example OPAL95 and LAOL89). Is that intended, with `GETOPAC` choosing among them, or should they exclude each other like the low-temperature ones?
