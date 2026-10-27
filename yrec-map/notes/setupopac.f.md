## Explanation

**Purpose.** Reads the opacity tables chosen for the run and sets up their interpolation. Its comment: "THIS SUBROUTINE READS IN SPECIFIED OPACITY TABLES AND SET UP SPLINES FOR THE TABLES. WHEN LZRAMP=T OR LDIFZ=T THEN READ IN SECOND SET OF OPACITY TABLES AT DIFFERENT Z."

**How it fits.**
- **Who calls it:** [[setups.f#SETUPS|`SETUPS`]], once per run; the file names are passed through (MHP 8/25).
- **What it calls,** by the namelist switches in `NMLPAR_MOD`:
  - interior tables: OPAL95, [[ll95tbl.f#LL95TBL|`LL95TBL`]] then [[op95xtab.f#OP95XTAB|`OP95XTAB`]] (`LOPAL95`); the pure-Z table, [[rdzlaol.f#RDZLAOL|`RDZLAOL`]] then [[zsulaol.f#ZSULAOL|`ZSULAOL`]] (`LPUREZ`);
  - low-temperature tables: Ferguson et al. 2005, [[readalex06.f#READALEX06|`READALEX06`]] (`LALEX06`).
- **Inputs:** `XENV` (the envelope's $X$, for the tables built at fixed composition) and the file names `FALEX06`, `FLIV95`, `FPUREZ`. Sets `L2Z` = `LZRAMP` or `LDIFZ` (both namelist parameters) in `NEWOPAC_MOD`, which the readers use to decide whether to read a second table.
- **Output:** the tables, in the modules of the routines called. They are used at run time by [[getopac.f#GETOPAC|`GETOPAC`]].

**Changed since `rp_1`.** The OPAL92 (`SETLLO`, `LL4TH`), LAOL89 (`RDLAOL`, `SULAOL`), Alexander 1995 (`ALXTBL`, `ALX8TH`) and Kurucz 1990 (`SETKRZ`) tables are removed (all removed since `rp_1`), with their file-name arguments and the argument `V`; this settles former question 1 (several interior tables at once), since OPAL95 is now the only interior table; COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

None.
