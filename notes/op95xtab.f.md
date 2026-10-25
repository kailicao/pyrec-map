## Explanation

**Purpose.** Builds the OPAL95 opacity table at one fixed hydrogen abundance (the surface $X$), from the table at the model's $Z$ (MHP 7/98). The result is what [[op952d.f#OP952D|OP952D]] interpolates, for the outer layers, where $X$ and $Z$ are those of the surface.

**How it fits.**
- **Inputs:** the desired $X$ (the envelope's, `XENV`); the table at the model's $Z$, `CAPPA` in `/LLOT95/` (from [[op95ztab.f#OP95ZTAB|OP95ZTAB]]); the $X$ grid `XXG` in `/LLOT95A/`.
- **Who calls it:** [[setupopac.f#SETUPOPAC|SETUPOPAC]] (at start-up) and [[surfopac.f#SURFOPAC|SURFOPAC]] (which rebuilds the surface tables for a new envelope $X$, `XENV`).
- **What it calls:** [[intrp2.f#INTRP2|INTRP2]], four-point Lagrange weights.
- **Output:** `CAPPAE(70,19)` and `XTAB` in `/LLOT95E/`, read by `OP952D` and [[getopal95.f#GETOPAL95|GETOPAL95]].

**The method.** It picks four $X$ tables around the desired $X$ and interpolates every $(T, R)$ entry with Lagrange weights $b_k$:
$$\log\kappa_\mathrm{E}(T, R) = \sum_{k=1}^4 b_k\,\log\kappa(X_k, T, R).$$
For $X \le 0.8$, or $Z \le 0.04$ (where all ten $X$ tables exist), the four nearest tables. For $0.04 < Z < 0.1$, tables 6, 7, 8 and 10 (table 9, $X = 0.95$, is missing). For $Z \ge 0.1$, tables 6–9.

## Questions for the experts

1. **Table 9 at $Z = 0.04$.** This routine treats exactly $Z = 0.04$ as "low Z" (`ZTAB.LE.0.04`, all ten tables), while [[op95ztab.f#OP95ZTAB|OP95ZTAB]] skips table 9 for `Z.GE.0.04`, so for a surface $X > 0.8$ the interpolation may use a table 9 that holds old values (zeros at first). Should the test here be `ZTAB.LT.0.04`?
2. **The branch for $Z \ge 0.1$.** It uses tables 6–9, but table 9 is never filled at that $Z$. The branch cannot be reached now, since `OP95ZTAB` stops the run for any $Z > 0.08$; if that limit is raised, should it use tables 5–8?
3. **A wrong comment.** "Find interpolation factors in Z" precedes the interpolation in $X$.
4. **The sentinel `IDX = 11`.** The value marks the "6, 7, 8, 10" case for the index selection below; a named flag would be clearer.
