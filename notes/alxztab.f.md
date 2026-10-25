## Explanation

**Purpose.** This file interpolates the older Alexander low-temperature opacity tables to one metallicity $Z$, giving 7 tables, one per grid value of $X$.

**How it fits.**
- **Input:** the argument `Z`; the 105 tables in `CAPTALEX` (`/ALOTALL/`) and the grid `ZZG` (`/GALOT/`), from [[alxtbl.f#ALXTBL|ALXTBL]].
- **Who calls it:** [[alxtbl.f#ALXTBL|ALXTBL]] (at start-up, with `ZALEX1`) and [[yalo3d.f#YALO3D|YALO3D]] (whenever the envelope's $Z$ changes by more than $10^{-8}$).
- **What it calls:** [[intrp2.f#INTRP2|INTRP2]].
- **Output:** `CAPALEX(1:7,T,R)` and `ZE` in `/ALOT/`. [[alx8th.f#ALX8TH|ALX8TH]] then interpolates these in $X$.

**The method.** Choose 4 consecutive grid values of $Z$ around `Z` (start index from 1 to 12; above $Z = 0.06$ the last four, 0.04 to 0.10, extrapolating beyond 0.10), and for each $X$:
$$\kappa_{i_X}(T,R) = \sum_{k=1}^{4} w_k(Z)\,\kappa(X_{i_X}, Z_{k}; T,R), \qquad w_k(Z) = \prod_{l \ne k}\frac{Z - Z_l}{Z_k - Z_l}.$$

## Questions for the experts

1. **Search bounds.** The search loops `I = 3, NUMZ-1` with a strict `Z.LT.ZZG(I)`, so the stencil is chosen differently from [[alex06tab.f#ALEX06TAB|ALEX06TAB]] (which uses `.LE.` and `NUMZ-2`). Is the difference intended? Neither checks that $Z$ is inside the grid.

### ALXZTAB

4-point Lagrange interpolation of the Alexander tables in $Z$ at each of the 7 values of $X$; sets `ZE`.
