## Explanation

**Purpose.** `MHDST` reads the MHD equation-of-state tables into memory at set-up: up to three "ZAMS" tables (different $X$, units `IR1`–`IR3`) and up to five "centre" tables (units `IR4`–`IR8`), and sets the temperature limits that decide which tables are used.

**How it fits.** Called only by [[mhdtbl.f#MHDTBL|`MHDTBL`]] (from [[setups.f#SETUPS|`SETUPS`]]), with the units of the opened table files; a unit ≤ 0 would skip that table, but `MHDTBL` always opens all eight files (`STATUS='OLD'`), and [[mhdpx1.f#MHDPX1|`MHDPX1`]] in turn always uses all three ZAMS tables and, above `TLIM2`, all five centre tables. It calls [[mhdst1.f#MHDST1|`MHDST1`]] once per table. It fills the COMMON blocks `TAB1A`…`TAB2C`, `TABX1`…`TABX5`, `CHEA`…`CHEC`, `CHE1`…`CHE5` (read by [[mhdpx2.f#MHDPX2|`MHDPX2`]]) and `TTTT` (read by [[mhdpx1.f#MHDPX1|`MHDPX1`]]).

**The method.** Read each table with `MHDST1` (`IDX` = 0 for ZAMS tables, 1 for centre tables). Then set
`TMINI` = first temperature of the ZAMS lower part, `TLIM1` = its last; `TLIM2` = the last temperature of the ZAMS upper part if there are no centre tables (`IR4` ≤ 0; then `TMAXI` = `TLIM2`), else the first temperature of the centre tables (and `TMAXI` = their last). So with centre tables, the ZAMS upper part is used only up to the centre tables' first temperature.

**Design.** A comment explains the dummy variables `NCHEM`, `DRDUM`, `NTDUM`, `NRDUM`: they give storage to arguments that would otherwise appear only as formal parameters ("Fortran is not a recursive language").

## Questions for the experts

1. **Shared grids.** The three ZAMS tables are read into separate arrays but the same grid variables (`NT1`, `NR1`, `NT2`, `NR2`, `TLOG1`, `TLOG2`, `DRH1`, `DRH2`), so each read overwrites the previous one's grid without a check that they agree.
2. **Dead code.** `IF(IR4.LE.0) GOTO 500` jumps to the next line; the output formats are commented out.

### MHDST

Reads up to eight MHD tables and sets the temperature limits (above).
