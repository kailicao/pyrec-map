## Explanation

**Purpose.** Builds the OPAL95 opacity table at one fixed hydrogen abundance (the surface $X$), from the table at the model's $Z$ (MHP 7/98). The result is what [[op952d.f#OP952D|OP952D]] interpolates, for the outer layers, where $X$ and $Z$ are those of the surface.

**How it fits.**
- **Inputs:** the desired $X$ (the envelope's, `XENV`); the table at the model's $Z$, `CAPPA` and `ZTAB` in `LLOT95_MOD` (from [[op95ztab.f#OP95ZTAB|OP95ZTAB]]); the $X$ grid `XXG` in `LLOT95A_MOD`.
- **Who calls it:** [[setupopac.f#SETUPOPAC|SETUPOPAC]] (at start-up) and [[surfopac.f#SURFOPAC|SURFOPAC]] (which rebuilds the surface tables for a new envelope $X$, `XENV`).
- **What it calls:** [[intrp2.f#INTRP2|INTRP2]], four-point Lagrange weights.
- **Output:** `CAPPAE(70,19)` and `XOP95` (the table's $X$, formerly `XTAB`) in `LLOT95E_MOD`, read by `OP952D` and [[getopal95.f#GETOPAL95|GETOPAL95]] (which uses this table when the point's $X$ is within $10^{-4}$ of `XOP95`).

**The method.** It picks four $X$ tables around the desired $X$ and interpolates every $(T, R)$ entry with Lagrange weights $b_k$:
$$\log\kappa_\mathrm{E}(T, R) = \sum_{k=1}^4 b_k\,\log\kappa(X_k, T, R).$$
For $X \le 0.8$, or $Z \le 0.04$ (where all ten $X$ tables exist), the four nearest tables. For $0.04 < Z < 0.1$, tables 6, 7, 8 and 10 (table 9, $X = 0.95$, is missing). For $Z \ge 0.1$, tables 6–9: This branch is unused? since [[op95ztab.f#OP95ZTAB|OP95ZTAB]] stops the run for any $Z > 0.08$; if it were reached, it would read table 9, which `OP95ZTAB` does not fill at that $Z$, where [[getopal95.f#GETOPAL95|GETOPAL95]] uses tables 5–8 (settled from the code, Nov 9, 2026: [[#L66-L71]]; [[op95ztab.f#L41-L46]], [[op95ztab.f#L68-L70]]; [[getopal95.f#L292-L296]]).

> **Question** ([[#L75]], [[#L85-L95]]). **The sentinel `IDX = 11`.** The value marks the "6, 7, 8, 10" case for the index selection below; a named flag would be clearer.

> **Question** ([[#L82-L83]]). **A wrong comment.** "Find interpolation factors in Z" precedes the interpolation in $X$.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`; the table's $X$ is renamed `XOP95` (formerly `XTAB` in `/LLOT95E/`). No question is settled.

## Bugs, by priority

1. **(d)** **Table 9 at $Z = 0.04$.** ([[#L53-L65]]; [[op95ztab.f#L68-L70]]) This routine treats exactly $Z = 0.04$ as "low Z" (`ZTAB.LE.0.04D0`, all ten tables), while [[op95ztab.f#OP95ZTAB|OP95ZTAB]] skips table 9 ($X = 0.95$) for `Z.GE.0.04D0`, and [[getopal95.f#GETOPAL95|GETOPAL95]] avoids it for `ZTAB.GE.0.04D0` ([[getopal95.f#L283-L290]]). So with `ZOPAL951` = 0.04 exactly and a surface $X$ above 0.8, the interpolation here uses a table 9 that holds zeros (or the values of an earlier `OP95ZTAB` call at a lower $Z$). Only for that exact $Z$ and an unusual surface $X$. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to treat Z = 0.04 as OP95ZTAB and GETOPAL95 do, without
    C table 9 (X=0.95).
          ELSE IF(ZTAB.LT.0.04D0)THEN
    ```

2. **(d)** **The last $X$ node taken as 1 instead of $1 - Z$.** ([[#L63-L65]], [[#L76-L79]]) The tenth table is at $X = 1 - Z$ ([[ll95tbl.f#L118-L122]]), and [[getopal95.f#GETOPAL95|GETOPAL95]] sets its node so (`A(4) = 1.0D0 - ZTAB`, [[getopal95.f#L315-L317]]), but here the node is `XXG(10)` = 1.0, so the Lagrange weights are those for a table at $X = 1$. This touches only a surface $X$ above 0.9 (or above 0.8 when $0.04 < Z < 0.1$), where table 10 is in the stencil; correct for every usual surface. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to put the last X node at 1-Z, the X of table 10, as
    C GETOPAL95 does (IDX = 7 and 11 are the cases that use table 10).
          IF(IDX.EQ.7 .OR. IDX.EQ.11) A(4) = 1.0D0 - ZTAB
    C
    C  FIND INTERPOLATION FACTORS IN Z.
          CALL INTRP2(A,B,X)
    ```
