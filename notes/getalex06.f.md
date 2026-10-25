## Explanation

**Purpose.** `GETALEX06` returns the low-temperature (molecular) opacity from the Ferguson–Alexander 2006 tables ("Alexander low T opacities", per its header, MHP 3/09) for a given $\rho$, $T$, $X$, $Z$, with its logarithmic derivatives.

**How it fits.**
- **Who calls it:** only [[getopac.f#GETOPAC|GETOPAC]], when $\log T \le$ `TMOLMAX` and `LALEX06` is set.
- **Inputs:** `DL`, `TL` ($\log\rho$, $\log T$), `X`, `Z`.
- **What it calls:** [[alex06tab.f#ALEX06TAB|ALEX06TAB]], which builds a table for the current $X$, $Z$ from the full set, and [[interp.f#INTERP|INTERP]] (four-point Lagrange weights and derivative weights).
- **Outputs:** `O` ($\kappa$, cm$^2$ g$^{-1}$), `OL` ($\log\kappa$), `QOD` $=\partial\log\kappa/\partial\log\rho|_T$, `QOT` $=\partial\log\kappa/\partial\log T|_\rho$.
- **COMMON blocks:** `/GALOT06/` (the grids `TGR06`, `R0GR06`, `XXG06`, `ZZG06`) and `/ALOT06/` (the table `CAPALEX06` at the composition `XE`, `ZE`, and the last indices `IT`, `ID`), shared with `ALEX06TAB` and [[readalex06.f#READALEX06|READALEX06]].

**The method.**
1. If $X$ or $Z$ differs from the stored `XE`, `ZE` by more than $10^{-8}$, rebuild the table with `ALEX06TAB`.
2. The table is in $\log T$ and $\log R$, with $\log R = \log\rho - 3(\log T - 6)$ (that is, $R = \rho/T_6^3$).
3. Find the 4×4 stencil from the last indices, get Lagrange weights in $\log T$ and $\log R$, and interpolate $\log\kappa$ and $\partial\log\kappa/\partial\log R$.
4. Above the largest $\log R$ of the table, extrapolate $\log\kappa$ linearly from the last two columns.
5. Convert the temperature derivative from fixed $R$ to fixed $\rho$:
$$\left.\frac{\partial\log\kappa}{\partial\log T}\right|_\rho = \left.\frac{\partial\log\kappa}{\partial\log T}\right|_R - 3\left.\frac{\partial\log\kappa}{\partial\log R}\right|_T.$$

## Questions for the experts

1. **Table rebuilt per composition.** Every change of $X$ or $Z$ beyond $10^{-8}$ rebuilds the table. In a model with a composition gradient in the cool envelope, or with settling, this happens at almost every call. Is that cost acceptable, or should the routine interpolate in $X$ and $Z$ directly?
2. **Extrapolation and derivatives.** Above the largest $\log R$, the value is extrapolated but `QOD` is not: it stays the derivative at the table edge. Consistent, or should it be the slope of the extrapolation?
3. **No lower-edge handling.** Below the smallest $\log R$ or outside the $\log T$ range, the Lagrange weights extrapolate silently. Should there be a check?

### GETALEX06

Ferguson–Alexander 2006 molecular opacity: four-point Lagrange interpolation in $\log T$ and $\log R$, with the derivative converted to fixed $\rho$ (method above).
