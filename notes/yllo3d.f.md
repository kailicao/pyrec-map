## Explanation

**Purpose.** `YLLO3D` gives the OPAL92 (Livermore) opacity at $\log\rho$, $\log T$ and $X$: it chooses the composition tables, calls [[yllo2d.f#YLLO2D|YLLO2D]] for each, and interpolates linearly in $X$. Its header lists the family: `YLLO3D` and `SETLLO` are "the routines to be called"; `YLLO2D`, `YLLOC` and `LL4TH` work for them; `YLLO3D2` and `YLLO2D2` are the second-$Z$ versions.

**How it fits.**
- **Who calls it:** [[getopac.f#GETOPAC|GETOPAC]].
- **What it calls:** [[findex.f#FINDEX|FINDEX]] and [[yllo2d.f#YLLO2D|YLLO2D]].
- **Inputs:** the tables' grids (`GLLOT`: `GRIDT`, three values of $X$ in `GRIDX`), the surface table's $X$ (`XENV4`, `LLOT4`); the last indices in COMMON `KIPMLL`, used by no other routine.
- **Outputs:** `OF` = $\kappa$, `OLF` = $\log\kappa$, `QODF` = $\partial\log\kappa/\partial\log\rho$, `QOTF` = $\partial\log\kappa/\partial\log T$ at fixed $\rho$.

**The method.**
1. $\log T_6 = \log T - 6$ and $\log R = \log\rho - 3\log T_6$ (the comments write "LN" and "T/10E6", but the code uses $\log_{10}$ and $T/10^6$).
2. If $X$ is the surface table's (within $10^{-5}$) or one of the three grid values, one table is used. Otherwise the interval in $X$ is found: tables 2–3 are used for $X$ above the second grid value, and also below it when $\log R > -1$; tables 1–2 only for $X$ below the second grid value at $\log R \le -1$. Then
   $$\log\kappa = \log\kappa_{m} + (\log\kappa_{m+1} - \log\kappa_m)\,\frac{X - X_m}{X_{m+1} - X_m},$$
   which extrapolates linearly when $X$ is outside $[X_m, X_{m+1}]$ (the comment: "linear extrapolation in X"). The derivatives are interpolated the same way.
3. $\partial\log\kappa/\partial\log T|_\rho = \partial\log\kappa/\partial\log T|_R - 3\,\partial\log\kappa/\partial\log R$.
4. The run stops if $T$ is outside the table ("T OUT OF TABLE").

## Questions for the experts

1. **The choice of $X$ tables.** For $X$ between the first two grid values, tables 1–2 are used only at $\log R \le -1$; at higher $\log R$ the code extrapolates from tables 2–3. Probably because table 1 lacks high-density entries; can the experts confirm?
2. **`DATA` for a COMMON block.** `DATA M1,M2,M3/1,1,1/` initialises COMMON `KIPMLL` in a subroutine, which standard Fortran allows only in BLOCK DATA. `YLLO3D2` has no such `DATA`.
3. **Comments on units.** The comments write "LN(T/10E6)" for what the code computes as $\log_{10}(T/10^6)$.

### YLLO3D

OPAL92 opacity at $(\rho, T, X)$: one composition table, or linear interpolation (or extrapolation) in $X$ between two, each from `YLLO2D`.
