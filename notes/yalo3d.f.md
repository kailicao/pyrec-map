## Explanation

**Purpose.** `YALO3D` gives the low-temperature opacity from the Alexander tables (its comment: "MHP 4/98, subroutine for calculating Alexander low T opacities"): $\kappa$ and its logarithmic derivatives at a given $\log\rho$, $\log T$, $X$ and $Z$, by interpolation in $\log T$, $\log R$ (with $R = \rho/T_6^3$) and $X$.

**How it fits.**
- **Inputs:** $\log\rho$ (`DL`), $\log T$ (`TL`), $X$, $Z$; the tables in COMMON `ALOT` (`CAPALEX`, $\log\kappa$ on the grid, with the table's $X$ and $Z$, `XE` and `ZE`, and the last indices `IX`, `IT`, `ID`) and their grids in `GALOT` (`TGR`, `XXG`, `R0GR`, `ZZG`), filled by [[alxtbl.f#ALXTBL|ALXTBL]], [[alxztab.f#ALXZTAB|ALXZTAB]] and [[alx8th.f#ALX8TH|ALX8TH]].
- **Who calls it:** [[getopac.f#GETOPAC|GETOPAC]], when the Alexander 1995 tables are on (`LALEX95`).
- **What it calls:** [[alxztab.f#ALXZTAB|ALXZTAB]] and [[alx8th.f#ALX8TH|ALX8TH]], to rebuild the tables when $Z$ differs from the tables' by more than $10^{-8}$; [[interp.f#INTERP|INTERP]] (4-point weights and their derivatives) and [[intrp2.f#INTRP2|INTRP2]] (4-point weights).
- **Outputs:** `O` = $\kappa$, `OL` = $\log\kappa$, `QOD` = $\partial\log\kappa/\partial\log\rho$ and `QOT` = $\partial\log\kappa/\partial\log T$ at fixed $\rho$.

**The method.**
1. $\log R = \log\rho - 3(\log T - 6)$.
2. Find four grid temperatures and four grid values of $\log R$ around the point, starting from the indices of the previous call, and their 4-point interpolation weights (with derivatives).
3. If $X$ equals the table's surface $X$ (`XE`), use the eighth table (the surface composition, built by `ALX8TH`); beyond the largest $\log R$ there, extrapolate linearly in $\log R$. Otherwise interpolate in $\log R$ and $\log T$ in four of the seven $X$ tables, then in $X$.
4. Convert the derivative from fixed $R$ to fixed $\rho$:
   $$\left.\frac{\partial\log\kappa}{\partial\log T}\right|_\rho = \left.\frac{\partial\log\kappa}{\partial\log T}\right|_R - 3\,\frac{\partial\log\kappa}{\partial\log R}.$$

## Questions for the experts

1. **`ID` is not checked.** The temperature index `IT` is clamped to the table on entry ("llp 8/19/08"), the density index `ID` is not, though it is used as `R0GR(ID+2)` before the search. Is `ID` always valid on the first call?
2. **Extrapolation.** Beyond the grids, the 4-point interpolation extrapolates without a warning; only the surface-$X$ table, at large $\log R$, switches to linear extrapolation. Is the asymmetry intended?
3. **The surface test.** The surface table is used when $|X - X_E| < 10^{-8}$; a slightly different $X$ (after diffusion, for example) switches to the interpolation in $X$, with a possible jump in $\kappa$.

### YALO3D

Alexander low-temperature opacity and its derivatives, by 4-point interpolation in $\log T$, $\log R$ and $X$ (or the surface-composition table).
