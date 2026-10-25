## Explanation

**Purpose.** `ZSULAOL` ("spline pure Z LAOL89") prepares the pure-metal LAOL89 opacity table (DBG 12/95) for interpolation in density, as [[sulaol.f|sulaol.f]] does for the main tables: for each temperature, a natural cubic spline of $\log\kappa$ against $\log\rho$, through the nonzero entries, if there are at least four.

**How it fits.**
- **Inputs:** COMMON `ZLAOL` (`ZOLAOL`, the grids `ZOT`, `ZORHO`, sizes `NUMRHOZ`, `NUMTZ`), filled by [[rdzlaol.f#RDZLAOL|RDZLAOL]].
- **Who calls it:** [[setupopac.f#SETUPOPAC|SETUPOPAC]].
- **What it calls:** [[cspline.f#CSPLINE|CSPLINE]] (end slopes $10^{30}$, a natural spline).
- **Outputs:** COMMON `ZSLAOL` ($\log\kappa$, $\log\rho$, second derivatives, points per temperature), read by [[gtpurz.f#GTPURZ|GTPURZ]]; a temperature with fewer than four nonzero entries gets `NUMRSZ` = 0, and `GTPURZ` skips it. `ZOT` is converted to $\log_{10} T$ in place; this is safe because the routine runs once per job (main program → `SETUPS` → `SETUPOPAC`).

## Questions for the experts

1. **Logarithm in place.** As in `SULAOL`, `ZOT` becomes $\log_{10}T$ in place, so a second call would take the logarithm twice. It is called once per job today; should the new code keep $T$ and $\log T$ apart?

### ZSULAOL

Natural cubic splines of $\log\kappa$ against $\log\rho$ for each temperature of the pure-Z LAOL89 table.
