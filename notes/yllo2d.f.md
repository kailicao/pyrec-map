## Explanation

**Purpose.** `YLLO2D` interpolates the OPAL (Livermore) opacity tables (the comment of [[yllo3d.f|yllo3d.f]]: "the interpolation facility for the Livermore opacity tables using cubic spline interpolation") in two dimensions, at one composition table: in density with the stored splines, then in temperature. It returns $\log\kappa$, $\kappa$ and the derivatives with respect to $\log R$ and $\log T_6$.

**How it fits.**
- **Inputs:** $\log T_6$ (`T`), $\log R$ (`D`), and the grid indices of composition (`M1`; 4 means the surface table) and temperature (`M2`); the spline coefficients `CFORD` (COMMON `LINTPL`, from [[ylloc.f#YLLOC|YLLOC]]) or, for the surface table, `CFORD4` (`LLOT4`, from [[ll4th.f#LL4TH|LL4TH]]), whose density range (`NDS`, `NDD`) is taken from composition `KIPM1`, which `LL4TH` sets; the grids in `GLLOT`.
- **Who calls it:** [[yllo3d.f#YLLO3D|YLLO3D]] and [[ll4th.f#LL4TH|LL4TH]].
- **What it calls:** [[findex.f#FINDEX|FINDEX]] (the density interval) and [[intpol.f#INTPOL|INTPOL]] (piecewise interpolation in $T$ with its derivative).
- **Outputs:** `O`, `OL` ($\log_{10}\kappa$), `QODF` = $\partial\log\kappa/\partial\log R$, `QOTF` = $\partial\log\kappa/\partial\log T$ at fixed $R$; and `M3`, the density index.

**The method.** For up to six temperatures around `M2` (from `M2-2` to `M2+3`), the spline in density gives
$$\log\kappa = c_1 + c_2\,\delta + c_3\,\delta^2 + c_4\,\delta^3,\qquad \frac{\partial\log\kappa}{\partial\log R} = c_2 + 2c_3\,\delta + 3c_4\,\delta^2,$$
with $\delta$ the distance from the knot; outside the table's densities (`FINDEX` then returns a negative index), the linear part only ($c_1 + c_2\delta$), from the first or last knot. Then `INTPOL` interpolates both in $\log T$ and gives $\partial\log\kappa/\partial\log T$. The run stops if $T$ lies outside the temperatures used ("EXTRAPOLATION FAILS").

[[yllo2d2.f|yllo2d2.f]] is the same routine for the second table at another $Z$.

## Questions for the experts

1. **The error message.** The check `NDSS .NE. 1` stops with "OPAL95 2D CHECK NDSS", but these are the OPAL92 tables of `LL4TH` and `SETLLO` (OPAL95 has its own routines). A message to correct?
2. **Unused values.** `LMORE`, `QODTI` and COMMON `LLOT`'s `OPACITY` are not used.

### YLLO2D

Two-dimensional interpolation in one OPAL92 composition table: splines in $\log R$ at up to six temperatures, then piecewise interpolation in $\log T$; with linear extrapolation in density.
