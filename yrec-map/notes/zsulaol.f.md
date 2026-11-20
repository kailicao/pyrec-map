## Explanation

**Purpose.** `ZSULAOL` ("spline pure Z LAOL89") prepares the pure-metal LAOL89 opacity table (DBG 12/95) for interpolation in density, as `SULAOL` did for the main LAOL89 tables (sulaol.f, removed since `rp_1` with those tables): for each temperature, a natural cubic spline of $`\log\kappa`$ against $`\log\rho`$, through the nonzero entries, if there are at least four.

**How it fits.**
- **Inputs:** `ZLAOL_MOD` (formerly `COMMON/ZLAOL/`: `ZOLAOL`, the grids `ZOT`, `ZORHO`, sizes `NUMRHOZ`, `NUMTZ`), filled by [RDZLAOL](https://github.com/yreclab/yrec/blob/7be4133/src/rdzlaol.f#L6-L74) when `LPUREZ` is set.
- **Who calls it:** [SETUPOPAC](https://github.com/yreclab/yrec/blob/7be4133/src/setupopac.f#L14-L95).
- **What it calls:** [CSPLINE](cspline.f.md#cspline) (end slopes $`10^{30}`$, a natural spline).
- **Outputs:** `ZSLAOL_MOD` (formerly `COMMON/ZSLAOL/`: $`\log\kappa`$, $`\log\rho`$, second derivatives, points per temperature), read by [GTPURZ](gtpurz.f.md#gtpurz); a temperature with fewer than four nonzero entries gets `NUMRSZ` = 0, and `GTPURZ` stops the run if it needs that temperature ([gtpurz.f, line 75](https://github.com/yreclab/yrec/blob/7be4133/src/gtpurz.f#L75), [gtpurz.f, lines 106–111](https://github.com/yreclab/yrec/blob/7be4133/src/gtpurz.f#L106-L111)); the table of the test suite, `PURECO.DBGLAOL`, has at least 23 at every temperature. `ZOT` is converted to $`\log_{10} T`$ in place ([lines 23–25](https://github.com/yreclab/yrec/blob/7be4133/src/zsulaol.f#L23-L25)); this is safe because the routine runs once per job (main program → `SETUPS` → `SETUPOPAC`), and its only call follows a fresh read of the table by `RDZLAOL`, so even a second call would not take the logarithm twice (settled from the code, Nov 9, 2026: [setupopac.f, lines 79–81](https://github.com/yreclab/yrec/blob/7be4133/src/setupopac.f#L79-L81)).

**Changed since `rp_1`.** Declarations only: `COMMON/ZLAOL/` and `/ZSLAOL/` to `ZLAOL_MOD` and `ZSLAOL_MOD`, `IMPLICIT NONE`; the main LAOL89 tables (`SULAOL`) are removed, the pure-Z one kept.

### ZSULAOL

Natural cubic splines of $`\log\kappa`$ against $`\log\rho`$ for each temperature of the pure-Z LAOL89 table.
