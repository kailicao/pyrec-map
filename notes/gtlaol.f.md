## Explanation

**Purpose.** `GTLAOL` returns the opacity from the Livermore (LAOL) opacity tables at a given density, temperature and hydrogen abundance, with its logarithmic derivatives in density and temperature.

**How it fits.**
- **Who calls it:** only [[getopac.f#GETOPAC|`GETOPAC`]], the opacity driver, when the run uses the LAOL tables (`LLAOL89`): directly, and as the X-dependent table when interpolating to a pure-metal table (with [[gtpurz.f#GTPURZ|`GTPURZ`]]). With two metallicities (`L2Z`), `GETOPAC` also calls [[gtlaol2.f#GTLAOL2|`GTLAOL2`]] and interpolates linearly in $Z$.
- **Inputs:** `DL` = $\log\rho$, `TL` = $\log T$, `X`; the tables in COMMON: `NWLAOL` (the grids `OXA` in $X$ and `OT` in $\log T$, their sizes, and the tolerance `TOLLAOL`), filled by [[rdlaol.f#RDLAOL|`RDLAOL`]], and `SLAOL` (for each $X$ and $T$ the run of $\log\kappa$ against $\log\rho$, `SLAOLL`, `SRHOL`, with its spline second derivatives `SDORL` and the number of points `NUMRS`), prepared by [[sulaol.f#SULAOL|`SULAOL`]].
- **Outputs:** `O` = $\kappa$, `OL` = $\log\kappa$, `QOD` $\approx \partial\log\kappa/\partial\log\rho$, `QOT` $\approx \partial\log\kappa/\partial\log T$.
- **Calls:** [[locate.f#LOCATE|`LOCATE`]] (bisection in a grid), [[xrng4.f#XRNG4|`XRNG4`]] (the four grid points around an index), and the spline pair [[cspline.f#CSPLINE|`CSPLINE`]] / [[splint.f#SPLINT|`SPLINT`]].
- **COMMON blocks:** `LUOUT` (the output units), `NWLAOL` (shared with 16 units: the readers, `GETOPAC`, `ENVINT`, `PARMIN`, `PUTSTORE`, …), `SLAOL` (with `GTLAOL2`, `GTPURZ`, `SULAOL`).

**The method.** As its comment says: (1) cubic spline in density, (2) cubic spline in temperature, (3) linear in composition.
1. For the two tabulated $X$ values bracketing `X` (index clamped to the grid) and for the four temperatures around $\log T$, it evaluates the density spline at $\log\rho$. Just outside a row's density range, within a margin $\delta$, it extrapolates linearly from the two end points; the slope of the bracketing interval is kept as $\partial\log\kappa/\partial\log\rho$.
2. Through the (at least four) values at the different temperatures, it fits a natural cubic spline and evaluates it at $\log T$. The temperature derivative is the chord slope of the bracketing interval, and the density derivative is interpolated linearly in $T$.
3. It interpolates $\log\kappa$ and both derivatives linearly in $X$:
$$\log\kappa = \log\kappa_1 + \frac{\log\kappa_2-\log\kappa_1}{X_2-X_1}\,(X-X_1).$$
4. It caps $\log\kappa$ at 35.

The margin is $\delta = \ln(\texttt{TOLLAOL})$, the natural log, applied in $\log_{10}\rho$. `TOLLAOL` is read in `PARMIN`'s namelist; no file in `src/` gives it a value, so it must be set there (with `TOLLAOL` = 10, for example, $\delta \approx 2.30$).

**Design.** It stops the run (`STOP`) when a temperature row has fewer than 4 density points, or fewer than 4 temperatures are usable, or fewer than 2 compositions. Points outside the margin are dropped silently, which can lead to the "outside the table" stop.

## Questions for the experts

1. **The extrapolation margin.** `TOLL = LOG(TOLLAOL)` is a natural log but is compared with $\log_{10}\rho$ (a value of 10 gives 2.3 dex, not 1). Was $\log_{10}$ meant? And `TOLLAOL` has no default in the code: if the namelist leaves it at zero, `LOG(0)` fails or gives $-\infty$. Should it get a default?
2. **Derivatives are chord slopes.** `QOD` and `QOT` are slopes of the bracketing intervals, not the spline derivatives, so they are discontinuous at grid points and not consistent with $\kappa$. Is this accurate enough for the Henyey iteration?
3. **Extrapolation in X.** When `X` lies outside the composition grid the index is clamped and the linear formula extrapolates without a warning.

### GTLAOL

Spline in $\rho$, spline in $T$, linear in $X$ (above); returns $\kappa$, $\log\kappa$ and approximate derivatives.
