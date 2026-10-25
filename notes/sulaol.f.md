## Explanation

**Purpose.** `SULAOL` ("SPLINE LAOL89") prepares the LAOL89 opacity tables for interpolation in density: for each composition and temperature of the table, it fits a cubic spline to $\log\kappa$ as a function of $\log\rho$ and stores the spline's second derivatives. With two metallicities (`L2Z`, the "ZRAMP" option, DBG 4/94) it does the same for the second table.

**How it fits.**
- **Inputs:** the tables read by [[rdlaol.f#RDLAOL|RDLAOL]] into COMMON `NWLAOL` (`OLAOL`, the grids `OT`, `ORHO`, sizes `NUMOFXYZ`, `NUMT`, `NUMRHO`) and `NWLAOL2` (the second table).
- **Who calls it:** [[setupopac.f#SETUPOPAC|SETUPOPAC]], right after `RDLAOL`, when `LLAOL89` is set.
- **What it calls:** [[cspline.f#CSPLINE|CSPLINE]], with end slopes $10^{30}$, that is natural splines.
- **Outputs:** COMMON `SLAOL` (`SLAOLL` = $\log\kappa$, `SRHOL` = $\log\rho$, `SDORL` = second derivatives, `NUMRS` = points per spline) and `SLAOL2`, read by [[gtlaol.f#GTLAOL|GTLAOL]], [[gtlaol2.f#GTLAOL2|GTLAOL2]] and [[gtpurz.f#GTPURZ|GTPURZ]]. It also converts the temperature grid `OT` (and `OT2`) to $\log_{10}$ in place.
- **COMMON blocks:** `NWLAOL`, `NWLAOL2`, `SLAOL`, `SLAOL2`, `NEWOPAC` (for `L2Z`), and `ZRAMP`, which it declares but does not use.

**The method.** For each composition $X$ and temperature $T$, the nonzero entries $\kappa(\rho_k)$ give points $(\log\rho_k, \log\kappa_k)$; zeros mark missing entries and are skipped. A spline is fitted only if at least four points remain; otherwise `NUMRS = 0`.

## Questions for the experts

1. **The second table's temperature loop.** For the second table, `OT2` is converted with `DO IT=1, NUMT`, the first table's size, while the rest of that block uses `NT2`. Should it be `NT2`?
2. **Logarithm in place.** `OT` and `OT2` become $\log_{10} T$ in place, so a second call to `SULAOL` would take the logarithm twice. Is it called only once per job?
3. **Unused COMMON.** `ZRAMP` is declared but not used here.

### SULAOL

Natural cubic splines of $\log\kappa$ against $\log\rho$ for each composition and temperature of the LAOL89 table (and of the second table with `L2Z`).
