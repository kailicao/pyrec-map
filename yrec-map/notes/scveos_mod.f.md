## Explanation

**Purpose.** `SCVEOS_MOD` holds the tables of the SCV equation of state ("MHP 5/97"): those of pure hydrogen, pure helium and the metals as read, the table built from them for the envelope's mixture, and the search indices of the last interpolation. Shared by 4 routines. It replaces `COMMON/SCVEOS/` (MHP via Claude, 10/14/26), less its switch `LSCV`, now in [[nmlpar_mod.f|`NMLPAR_MOD`]], and with `IDT` renamed `IDTSCV` (10/9/26), since PARMIN and STARIN had an unrelated `IDT` of `COMMON/OPTAB/` and called this one `IDTT`. The dimensions `NTS` = 63 (temperatures) and `NPS` = 76 (pressures per temperature) are `PRIVATE`, because the importing files declare their own.

**What its variables hold, who sets them, who reads them.**
- `TLOGX(NTS)`, `NPTSX(NTS)`: the tables' $\log T$ values and the number of pressure points at each; read by [[setups.f#SETUPS|`SETUPS`]] from the hydrogen table.
- `TABLEX(NTS,NPS,12)`, `TABLEY(NTS,NPS,12)`: the hydrogen and helium tables (11 columns as read by `SETUPS`, the first $\log P$); [[setscv.f#SETSCV|`SETSCV`]] adds column 12, $\mathrm{d}U/\mathrm{d}T$. `TABLEZ(NTS,NPS,13)`: the metals' table, read by `SETUPS`.
- `SMIX(NTS,NPS)`: the entropy of mixing of hydrogen and helium, computed by `SETSCV`; read by `SETSCV` and [[eqscvg.f#EQSCVG|`EQSCVG`]].
- `TABLENV(NTS,NPS,12)`: the table for the envelope's mixture ($\log P$, $\log\rho$, the derivatives, $c_P$, $\mathrm{d}U/\mathrm{d}T$, …), built by `SETSCV`; read by `SETSCV`, [[eqscve.f#EQSCVE|`EQSCVE`]] and `EQSCVG`.
- `IDTSCV`, `IDP`: the first indices of the four-point stencil in temperature and in pressure, kept between calls as the starting point of the next search; set and read by `EQSCVE`, `EQSCVG` and `SETSCV`.

**Design.** A blanket `USE SCVEOS_MOD` in each routine. `EQSCVE` and `EQSCVG` share `IDTSCV` and `IDP`, so a call of one starts its search where the other left off.

**Changed since `rp_1`.** New file: `COMMON/SCVEOS/` as a module, with `LSCV` moved to `NMLPAR_MOD` and `IDT` renamed `IDTSCV`.
