## Explanation

**Purpose.** This file builds the low-temperature opacity table of Alexander (the 2006 tables, as the names `ALEX06`/`ALOT06` say) for one composition $(X, Z)$, by interpolating between the stored tables of the grid in $X$ and $Z$. The result is a single table of opacity against $\log T$ and $\log R$ that [[getalex06.f#GETALEX06|GETALEX06]] then interpolates in.

**How it fits.**
- **Inputs:** the full set of tables, `CAPTALEX06` in `ALOT06ALL_MOD`, read once by [[readalex06.f#READALEX06|READALEX06]], and the grid values `XXG06`, `ZZG06` in `GALOT06_MOD` (initialized there); the requested composition `XE`, `ZE` in `ALOT06_MOD`.
- **Who calls it:** only [[getalex06.f#GETALEX06|GETALEX06]], whenever the $X$ or $Z$ of the point differs from the composition of the current table by more than $10^{-8}$. GETALEX06 sets `XE`, `ZE` before the call.
- **What it calls:** [[intrp2.f#INTRP2|INTRP2]], 4-point Lagrange weights.
- **Output:** `CAPALEX06(NUMT,NUMD)` in `ALOT06_MOD`, read by GETALEX06. It also sets the index `IX` in `ALOT06_MOD`.
- **Modules:** `GALOT06_MOD` and `ALOT06_MOD` (with GETALEX06 and READALEX06), `ALOT06ALL_MOD` (with READALEX06); the formerly shared COMMON blocks `/GALOT06/`, `/ALOT06/` and `/ALOT06ALL/`.

**The grid.** READALEX06 stores the tables as `CAPTALEX06(JJ, T, R)` with $JJ = (i_X - 1)\,N_Z + i_Z$, for $N_X = 9$ values of $X$ (eight from 0 to 0.9, then a ninth set at $X = 1 - Z$, which `XXG06(9) = 1.0` stands for) and $N_Z = 16$ values of $Z$ (0 to 0.10): 143 tables in all, since there is no extra table at $X = 1 - Z$ for $Z = 0.10$ (the $X = 0.9$ table doubles for it). Each table has 85 temperatures and 19 values of $\log R$.

**The method.**
1. Check the composition: $0 \le X \le 1 - Z$, and $0 \le Z \le Z_{16} + (Z_{16} - Z_{15}) = 0.12$, an extrapolation by one grid step in $Z$. Otherwise the run stops.
2. Choose 4 neighboring grid values in $Z$ (starting index `IZ`) and in $X$ (`IX`). Above $X = 0.8$ the start is `NUMX-3`, or `NUMX-4` if $Z \ge 0.1$.
3. Interpolate in $Z$ for each of the 4 values of $X$, with the 4-point Lagrange weights $w_k(Z)$:
$$\kappa_m(T,R) = \sum_{k=1}^{4} w_k(Z)\,\kappa(X_m, Z_{k}; T, R), \qquad w_k(Z) = \prod_{l \ne k} \frac{Z - Z_l}{Z_k - Z_l}.$$
The 4th value of $X$ needs its own indexing near the corner of the grid ($X = 1 - Z$, $Z = 0.1$).
4. Interpolate in $X$ the same way over the 4 results (`CAPTEMP`), giving `CAPALEX06`. When `IZ = NUMZ-3`, the 4th node in $X$ is placed at $1 - Z$.

The tabulated quantity is probably $\log \kappa$ (READALEX06 reads it with format `F7.3`); the interpolation is linear in whatever is stored.

**Design.** All state is in modules; the routine has no arguments. It stops the run on a bad composition, with a message that names "ALEX06".

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE` (the unused `NUMXZ` parameter is now in `ALOT06ALL_MOD`).

## Questions for the experts

1. **The 4th node in $X$.** `QR(4) = 1-ZE` whenever `IZ = NUMZ-3` (that is, for $Z > 0.06$), whatever `IX` is. But the 4th table is at $X = 1 - Z$ only when `IX = NUMX-3`; for smaller $X$ it is `XXG06(IX+3)` (for example 0.35 when `IX = 1`). Should the test be on `IX` as well? As written, the $X$ interpolation for $Z > 0.06$ and $X \lesssim 0.7$ uses a wrong abscissa.
2. **The last row at small $Z$.** When `IX = NUMX-3` and `IZ < NUMZ-3`, the 4th node is `XXG06(9) = 1.0`, although the table stored there is at $X = 1 - Z$. Is the difference (up to 0.06) accepted on purpose?
3. **Extrapolation to $Z = 0.12$.** Between $Z = 0.10$ and 0.12 the code extrapolates; for $X$ near $1-Z$ the corner table is the $X = 0.9$ one at $Z = 0.10$. Is this range meant to be used?

### ALEX06TAB

Interpolates the stored Alexander tables to the composition (`XE`, `ZE`) in `ALOT06_MOD`: first in $Z$, then in $X$, each with 4-point Lagrange weights from [[intrp2.f#INTRP2|INTRP2]]. Writes `CAPALEX06`.
