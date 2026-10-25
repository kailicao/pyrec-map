## Explanation

**Purpose.** This file builds, for the older Alexander low-temperature opacities (Alexander and Ferguson 1994, per [[alxtbl.f|alxtbl.f]]), the table at the envelope's hydrogen abundance $X$. It interpolates in $X$ between the 7 tables that [[alxztab.f#ALXZTAB|ALXZTAB]] has already brought to the envelope's $Z$, and stores the result as an 8th table.

**How it fits.**
- **Input:** the argument `X`; the 7 fixed-$Z$ tables `CAPALEX(1:7,…)` and the grid `XXG` in `/ALOT/` and `/GALOT/`, from [[alxtbl.f#ALXTBL|ALXTBL]] and [[alxztab.f#ALXZTAB|ALXZTAB]].
- **Who calls it:** [[setupopac.f#SETUPOPAC|SETUPOPAC]] at start-up (with the envelope's `XENV`), [[surfopac.f#SURFOPAC|SURFOPAC]], and [[yalo3d.f#YALO3D|YALO3D]] when $Z$ changes.
- **What it calls:** [[intrp2.f#INTRP2|INTRP2]].
- **Output:** `CAPALEX(8,T,R)` and `XE` in `/ALOT/`, read by [[yalo3d.f#YALO3D|YALO3D]], the opacity lookup, which uses table 8 only when its $X$ equals `XE` (within $10^{-8}$).

**The method.** Choose 4 consecutive grid values of $X$ (0, 0.1, 0.2, 0.35, 0.5, 0.7, 0.8) around `X`, with start index $i_X = 1$ to 4, and form
$$\kappa_8(T,R) = \sum_{k=1}^{4} w_k(X)\,\kappa_{i_X+k-1}(T,R), \qquad w_k(X) = \prod_{l \ne k}\frac{X - X_l}{X_k - X_l}.$$
Above $X = 0.8$ this extrapolates.

## Questions for the experts

1. **The index `IX`.** `IX` is in `/ALOT/`, where [[yalo3d.f#YALO3D|YALO3D]] also keeps `IT` and `ID`, its last grid positions; here it holds the start of the $X$ stencil. No routine reads the value left here: YALO3D sets `IX` itself before each use, and ALXTBL only gives it a DATA value. Could `IX` be a local variable in both routines?

### ALX8TH

Interpolates the 7 fixed-$Z$ Alexander tables to the envelope's $X$ (4-point Lagrange) and stores the result in slot 8 of `CAPALEX`.
