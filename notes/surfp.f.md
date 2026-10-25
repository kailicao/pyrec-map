## Explanation

**Purpose.** `SURFP` gives the pressure at $T = T_\mathrm{eff}$ in a model atmosphere, by interpolating a table of $\log P$ in $\log T_\mathrm{eff}$ and $\log g$. It is the outer boundary of the envelope integration with Kurucz atmospheres (`KTTAU = 3`).

**How it fits.**
- **Inputs:** $\log T_\mathrm{eff}$ (`TEFFL`) and $\log g$ (`GL`); the table in COMMON `ATMOS2` (`ATMPL(57,11)`, the grids `ATMTL`, `ATMGL`), read by [[setups.f#SETUPS|SETUPS]]; and in COMMON `FAC`, the lowest and highest valid gravity index for each temperature (`IMIN`, `IMINMAX`), also set by `SETUPS`.
- **Who calls it:** [[envint.f#ENVINT|ENVINT]], for `KTTAU = 3`. Its siblings are [[kcsurfp.f#KCSURFP|KCSURFP]] (Kurucz–Castelli tables, `KTTAU = 5`) and [[alsurfp.f#ALSURFP|ALSURFP]] (Allard tables, `KTTAU = 4`).
- **What it calls:** [[inter3.f#INTER3|INTER3]] (3-point Lagrange weights), [[kspline.f#KSPLINE|KSPLINE]] and [[ksplint.f#KSPLINT|KSPLINT]] (a natural cubic spline through four points).
- **Outputs:** in COMMON `ATMPRT`, `AP` = $\log P$ and `AT` = $\log T_\mathrm{eff}$, read by `ENVINT` (and [[qatm.f#QATM|QATM]], [[massloss.f#MASSLOSS|MASSLOSS]]); `JP` and `KP` in `FAC`, the table cell used. With `LPRT`, a line on `ISHORT` and `ISTOR`.

**The method.**
1. Stop the run if $\log T_\mathrm{eff} < 3.5$ or $\log g < -0.5$.
2. Find four table temperatures around $T_\mathrm{eff}$.
3. At each of them, interpolate $\log P$ in $\log g$: for $\log T > 4.55$ linearly between the two highest gravities; for $4.5 < \log T \le 4.55$ with the 3-point Lagrange formula on the three highest gravities; otherwise with a natural cubic spline through the four valid gravities nearest $\log g$ (the top four, a bracketing four, or the bottom four).
4. Interpolate the four values in $\log T_\mathrm{eff}$ with a natural cubic spline through four points.

The four-point spline, for points $x_1 < \dots < x_4$, is the cubic-spline formula of [[splint.f|splint.f]] with natural ends.

## Questions for the experts

1. **The comment describes another method.** The header says it interpolates "using a 4-point Lagrangian interpolator" and "will quit if the desired data point has Teff or log g more than one table point from the data". The code uses 4-point splines (the Lagrange calls `INTRP2` are commented out), and checks only the lower limits of $T_\mathrm{eff}$ and $g$. Extrapolation above the table's top is silent.
2. **Hot temperatures.** For $\log T > 4.5$ only the two or three highest gravities are used, whatever $\log g$ is: probably because the table has no low-gravity values there. Is linear extrapolation to low gravity acceptable?
3. **Hard-coded limits.** 3.5, $-0.5$, 4.5 and 4.55 are written in the code and tie it to one table; a different table would need them changed.
4. **Missing gravities outside the general case.** G. Somers limited the general case's search to `IMINMAX(J)` "to prevent using -999", but the top-four branch (`GL ≥ ATMGL(NG-1)`) and the hot branches use the gravities `NG-3` … `NG` without checking `IMINMAX(J)`. Can those branches still read the table's missing values (-999)?

### SURFP

$\log P$ at $T = T_\mathrm{eff}$ from the Kurucz atmosphere table, by interpolation in $\log g$ then $\log T_\mathrm{eff}$.
