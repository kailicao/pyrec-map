## Explanation

**Purpose.** This file builds the table of the low-temperature opacities of Ferguson et al. (2005), called ALEX06 in the code (read by [[readalex06.f#READALEX06|READALEX06]]), for one composition $(X, Z)$, by interpolating between the stored tables of the grid in $X$ and $Z$. The result is a single table of opacity against $\log T$ and $\log R$ that [[getalex06.f#GETALEX06|GETALEX06]] then interpolates in.

**How it fits.**
- **Inputs:** the full set of tables, `CAPTALEX06` in `ALOT06ALL_MOD`, read once by [[readalex06.f#READALEX06|READALEX06]], and the grid values `XXG06`, `ZZG06` in `GALOT06_MOD` (initialized there); the requested composition `XE`, `ZE` in `ALOT06_MOD`.
- **Who calls it:** only [[getalex06.f#GETALEX06|GETALEX06]], whenever the $X$ or $Z$ of the point differs from the composition of the current table by more than $10^{-8}$. GETALEX06 sets `XE`, `ZE` before the call.
- **What it calls:** [[intrp2.f#INTRP2|INTRP2]], 4-point Lagrange weights.
- **Output:** `CAPALEX06(NUMT,NUMD)` in `ALOT06_MOD`, read by GETALEX06. It also sets the index `IX` in `ALOT06_MOD`.
- **Modules:** `GALOT06_MOD` and `ALOT06_MOD` (with GETALEX06 and READALEX06), `ALOT06ALL_MOD` (with READALEX06); the formerly shared COMMON blocks `/GALOT06/`, `/ALOT06/` and `/ALOT06ALL/`.

**The grid.** READALEX06 stores the tables as `CAPTALEX06(JJ, T, R)` with $JJ = (i_X - 1)\,N_Z + i_Z$, for $N_X = 9$ values of $X$ (eight from 0 to 0.9, then a ninth set at $X = 1 - Z$, which `XXG06(9) = 1.0` stands for) and $N_Z = 16$ values of $Z$ (0 to 0.10): 143 tables in all, since there is no extra table at $X = 1 - Z$ for $Z = 0.10$ (the $X = 0.9$ table doubles for it). Each table has 85 temperatures and 19 values of $\log R$.

**The method.**
1. Check the composition: $0 \le X \le 1 - Z$, and $0 \le Z \le Z_{16} + (Z_{16} - Z_{15}) = 0.12$, an extrapolation by one grid step in $Z$ ([[#L28-L45]]; the comment: "PERMIT EXTRAPOLATION IN Z BY UP TO 1 TABLE ELEMENT"). Otherwise the run stops.

    > **Question** ([[#L38-L45]]; [[#L62-L67]]; [[#L91-L104]]). **Extrapolation to $Z = 0.12$.** Between $Z = 0.10$ and 0.12 the code extrapolates from the tables at $Z$ = 0.05, 0.06, 0.08 and 0.10; for $X$ above 0.8 the top table in $X$ is then the $X = 0.9$ one, which stands for $X = 1 - Z$ only at $Z = 0.10$. Is this range meant to be used in runs, or only to absorb small overshoots of $Z$ during the iterations?

2. Choose 4 neighboring grid values in $Z$ (starting index `IZ`) and in $X$ (`IX`). Above $X = 0.8$ the start is `NUMX-3`, or `NUMX-4` if $Z \ge 0.1$.
3. Interpolate in $Z$ for each of the 4 values of $X$, with the 4-point Lagrange weights $w_k(Z)$:
$$\kappa_m(T,R) = \sum_{k=1}^{4} w_k(Z)\,\kappa(X_m, Z_{k}; T, R), \qquad w_k(Z) = \prod_{l \ne k} \frac{Z - Z_l}{Z_k - Z_l}.$$
The 4th value of $X$ needs its own indexing near the corner of the grid ($X = 1 - Z$, $Z = 0.1$).
4. Interpolate in $X$ the same way over the 4 results (`CAPTEMP`), giving `CAPALEX06`. When `IZ = NUMZ-3` ($Z > 0.06$), the 4th node in $X$ is placed at $1 - Z$, whatever `IX` is; otherwise at `XXG06(IX+3)`, which is 1.0 for `IX = NUMX-3` ([[#L112-L121]]; bug 1).

The tabulated quantity is $\log \kappa$, as GETALEX06 uses it (READALEX06 reads it with format `F7.3`); the interpolation is linear in $\log\kappa$.

**Design.** All state is in modules; the routine has no arguments. It stops the run on a bad composition (`STOP 1`), with a message that names "ALEX06", written to the terminal and the `.short` file (`ISHORT`, from `IOUNITS_MOD`).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE` (the unused `NUMXZ` parameter is now in `ALOT06ALL_MOD`).

**Changed since `a8a5950`.** The two stops on a bad composition now write their message to the `.short` file as well as the terminal (the routine now uses `IOUNITS_MOD`), and exit with status 1, the code for run-time errors, instead of a bare `STOP` (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(a)** **The 4th node in $X$ is tested on `IZ`, not on `IX`.** ([[#L56-L68]]; [[#L91-L104]]; [[#L117-L121]]) The 4th table in $X$ is at $X = 1 - Z$ only when `IX = NUMX-3` (lines 93–104 read it from the ninth set, or from $X = 0.9$ at $Z = 0.10$); otherwise it is the table at `XXG06(IX+3)`. But its abscissa `QR(4)` is $1 - $ `ZE` whenever `IZ = NUMZ-3`, that is, for $Z > 0.06$, and `XXG06(IX+3)` otherwise. Two cases follow. (i) For $Z > 0.06$ and $X \le 0.8$ (`IX` ≤ `NUMX-4`), the 4th node is placed at $1 - Z$, between 0.88 and 0.94, instead of at its table's $X$ (for example 0.8 for $0.5 < X \le 0.7$, 0.9 for $0.7 < X \le 0.8$), so the Lagrange weights in $X$ are those of a wrong grid; this holds for any $X$ up to 0.8 (and, with an error of at most 0.02, for $X > 0.8$ at $Z \ge 0.10$, where `IX = NUMX-4` and the table is at 0.9). (ii) For $Z \le 0.06$ and $X > 0.8$ (`IX = NUMX-3`), the 4th node is placed at `XXG06(9)` = 1.0, while its table is at $X = 1 - Z$, up to 0.06 lower. Only with `LALEX06` (off by default in the code; recommended by YREC's User Guide), at $\log T \le$ `TMOLMAX`; case (i) only for $Z > 0.06$, case (ii) only for $X > 0.8$. Read from the code, not run; the size of the error in $\kappa$ was not computed. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to place the 4th node in X at 1-Z when the 4th table
    C is the X = 1-Z one (IX = NUMX-3), and at XXG06(IX+3) otherwise.
          IF(IX.EQ.NUMX-3)THEN
             QR(4) = 1.0D0-ZE
          ELSE
             QR(4) = XXG06(IX+3)
          ENDIF
    ```

### ALEX06TAB

Interpolates the stored ALEX06 tables to the composition (`XE`, `ZE`) in `ALOT06_MOD`: first in $Z$, then in $X$, each with 4-point Lagrange weights from [[intrp2.f#INTRP2|INTRP2]]. Writes `CAPALEX06`.
