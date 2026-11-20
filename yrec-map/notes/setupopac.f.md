## Explanation

**Purpose.** Reads the opacity tables chosen for the run and sets up their interpolation. Its comment: "THIS SUBROUTINE READS IN SPECIFIED OPACITY TABLES AND SET UP SPLINES FOR THE TABLES. WHEN LZRAMP=T OR LDIFZ=T THEN READ IN SECOND SET OF OPACITY TABLES AT DIFFERENT Z."

**How it fits.**
- **Who calls it:** [`SETUPS`](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L16-L396), once per run; the file names are passed through (MHP 8/25).
- **What it calls,** by the namelist switches in `NMLPAR_MOD`:
  - interior tables: OPAL95, [`LL95TBL`](ll95tbl.f.md#ll95tbl) then [`OP95XTAB`](https://github.com/yreclab/yrec/blob/7be4133/src/op95xtab.f#L6-L104) (`LOPAL95`); the pure-Z table, [`RDZLAOL`](https://github.com/yreclab/yrec/blob/7be4133/src/rdzlaol.f#L6-L74) then [`ZSULAOL`](zsulaol.f.md#zsulaol) (`LPUREZ`);
  - low-temperature tables: Ferguson et al. [2005](https://ui.adsabs.harvard.edu/abs/2005ApJ...623..585F), [`READALEX06`](https://github.com/yreclab/yrec/blob/7be4133/src/readalex06.f#L18-L141) (`LALEX06`).
- **Inputs:** `XENV` (the envelope's $`X`$, for the tables built at fixed composition) and the file names `FALEX06`, `FLIV95`, `FPUREZ`. Sets `L2Z` = `LZRAMP` or `LDIFZ` (both namelist parameters) in `NEWOPAC_MOD` ([line 64](https://github.com/yreclab/yrec/blob/7be4133/src/setupopac.f#L64)); despite the header's comment, no reader reads it, and only [`GETOPAC`](getopac.f.md#getopac) does, in its single-table test ([getopac.f, lines 140–141](https://github.com/yreclab/yrec/blob/7be4133/src/getopac.f#L140-L141); settled from the code, Nov 9, 2026).
- **Output:** the tables, in the modules of the routines called. They are used at run time by [`GETOPAC`](getopac.f.md#getopac).

**From YREC's documentation.** [Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html) (Input files): `FALEX06` is the molecular opacity table (Ferguson et al. 2005, with `LALEX06`, recommended), `FLIV95` the atomic one (OP/OPAL format, with `LOPAL95`, recommended), and `FPUREZ` the pure Y/Z table (with `LPUREZ`).

**Changed since `rp_1`.** The OPAL92 (`SETLLO`, `LL4TH`), LAOL89 (`RDLAOL`, `SULAOL`), Alexander 1995 (`ALXTBL`, `ALX8TH`; the code's name for the tables of Alexander & Ferguson [1994](https://ui.adsabs.harvard.edu/abs/1994ApJ...437..879A)) and Kurucz 1990 (`SETKRZ`; the code's name, probably the opacities of Kurucz [1991](https://ui.adsabs.harvard.edu/abs/1991ASIC..341..441K), “New Opacity Calculations”) tables are removed (all removed since `rp_1`), with their file-name arguments and the argument `V`; this settles former question 1 (several interior tables at once), since OPAL95 is now the only interior table; COMMON blocks to modules, `IMPLICIT NONE`.
