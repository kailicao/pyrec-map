## Explanation

**Purpose.** `LL4TH` builds the "4th table" of the Livermore (LL) opacity tables: a table at the surface composition, interpolated once in $X$ from the stored tables, so that the many opacity calls in the envelope and atmosphere need not interpolate in $X$ each time (its comment). It stores, for each temperature, the spline coefficients of $\log\kappa$ against the density variable.

**How it fits.**
- **Who calls it:** [[setupopac.f#SETUPOPAC|`SETUPOPAC`]] at set-up, and [[surfopac.f#SURFOPAC|`SURFOPAC`]] (when `LOPAL92` is set), which [[starin.f#STARIN|`STARIN`]] calls for the starting model and [[hpoint.f#HPOINT|`HPOINT`]] when the surface $X$ changes.
- **Input:** `X`, the surface hydrogen abundance. The tables: grids in COMMON `GLLOT` (`GRIDT`, `GRIDX`, `GRHOT3`; the density variable is $\rho/T_6^3$ by its name) and the per-composition spline coefficients in `LINTPL` (`CFORD`, `NDS`, `NDD`), with second-$Z$ copies `GLLOT2`, `LINTPL2`; filled by [[setllo.f#SETLLO|`SETLLO`]] and [[yllo3d.f|`yllo3d.f`]].
- **Output:** COMMON `LLOT4` (`XENV4`, `ZENV4`, the coefficients `CFORD4`, the $X$ index `KIPM1`) and, with two metallicities (`L2Z`), `LLOT42`; read by [[yllo2d.f#YLLO2D|`YLLO2D`]], [[yllo3d.f|`YLLO3D`]] and their `2` versions.
- **Calls:** [[findex.f#FINDEX|`FINDEX`]], [[yllo2d.f#YLLO2D|`YLLO2D`]] and [[yllo2d2.f#YLLO2D2|`YLLO2D2`]] (values at a grid node of one composition), [[ysplin.f#YSPLIN|`YSPLIN`]] (spline coefficients).
- **COMMON blocks:** `LLOT4`, `LLOT42`, `GLLOT`, `GLLOT2`, `LLOT`, `LLOT2`, `LINTPL`, `LINTPL2`, and `NEWOPAC` (the opacity switches and table metallicities, shared with 17 other units).

**The method.** Find the $X$ interval $[X_1, X_2]$ (index clamped to 1 or 2 of the three $X$ values). For each temperature row and each density node, interpolate linearly in $X$:

$$\log\kappa = \log\kappa(X_1) + \frac{X - X_1}{X_2 - X_1}\,\big(\log\kappa(X_2) - \log\kappa(X_1)\big),$$

then fit a spline in the density variable along the row (`YSPLIN`) and store its coefficients. Repeat for the second-$Z$ tables when `L2Z` is set. `ZENV4` is set to the table metallicity `ZOPAL1`, not to the surface $Z$.

## Questions for the experts

1. **Leftovers.** `OF`, the derivatives `QOD0`, `QOT0`, `QOD1`, `QOT1`, and the comment "conversion from the derivative with constant RHOT3 to constant RHO" have no code behind them. Was a derivative step dropped?
2. **Strict shape check.** It stops (`STOP ' LL4TH NDSS '`) unless every row starts at the first density node. Is that guaranteed for all LL tables?
3. **Extrapolation in X.** With only three $X$ values, an $X$ outside the grid is extrapolated linearly without a warning.

### LL4TH

The surface-composition opacity table: linear in $X$, then splines in density along each temperature row (above).
