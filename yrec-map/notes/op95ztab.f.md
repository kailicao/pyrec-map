## Explanation

**Purpose.** Builds the OPAL95 opacity tables at the model's fixed $Z$ (one table for each of the ten $X$ values) from the full set of tables (MHP 7/98). The result is what [[op953d.f#OP953D|OP953D]] interpolates, and what [[op95xtab.f#OP95XTAB|OP95XTAB]] reduces further to the surface $X$.

**How it fits.**
- **Inputs:** the desired $Z$; the full set in `LLOT95A_MOD` (`ZZG`, `NZ`, `CAPPA2`).
- **Who calls it:** [[ll95tbl.f#LL95TBL|LL95TBL]], after reading the tables.
- **What it calls:** [[intrp2.f#INTRP2|INTRP2]].
- **Output:** `CAPPA(10,70,19)` and `ZTAB` in `LLOT95_MOD`, read by `OP953D`, `OP95XTAB`, [[getopal95.f#GETOPAL95|GETOPAL95]] and [[calcad.f#CALCAD|CALCAD]].

**The method.** It finds the four $Z$ values around the desired $Z$ and interpolates each $(T, R)$ entry with Lagrange weights $b_k$, $\log\kappa(X_j, T, R) = \sum_k b_k\,\log\kappa(Z_k, X_j, T, R)$:
- tables 1–8 (present at every $Z$): directly;
- table 9 ($X = 0.95$): only if $Z < 0.04$, from four $Z$ values no larger than 0.04 (shifted to 0.01–0.04 if needed);
- table 10 ($X = 1 - Z$): only if $Z < 0.1$, from four $Z$ values below 0.1 (shifted to 0.03–0.08 if needed).

The search for the four $Z$ values only accepts a fourth value up to the twelfth, $Z = 0.08$ (the loop runs to `NUMZ-1`), so any $Z > 0.08$ stops the run ("DESIRED Z … OUTSIDE OP95 TABLE RANGE"), although the comment says "Z > 0.1". The top table, $Z = 0.1$, still enters as the fourth of the four values.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/LLOT95/` to `LLOT95_MOD`, `/LLOT95A/` to `LLOT95A_MOD`), `IMPLICIT NONE` (the unused parameters `NUMX` and `NUMXZ` dropped).

## Questions for the experts

1. **The upper limit on $Z$.** Any $Z$ between 0.08 and 0.1 stops the run, though the tables reach 0.1 and the comment says only $Z > 0.1$ stops. Is 0.08 the intended limit? If the loop ran to `NUMZ`, $Z$ up to 0.1 would be accepted.
2. **Label 30 in the wrong place.** For $Z \ge 0.1$, `GOTO 30` is meant to skip table 10 ("omit table 10 if desired Z >= 0.1"), but label 30 stands *before* the loop that fills table 10, so it would be filled anyway, with `IDZ2` and `BB` left from an earlier step. Since $Z > 0.08$ stops the run first (question 1), this path is never reached now; it matters only if the limit is raised.
3. **Table 9 for $Z \ge 0.04$.** Table 9 is not rebuilt, so `CAPPA(9,…)` keeps old values (zeros at first). [[op95xtab.f#OP95XTAB|OP95XTAB]] avoids it for $0.04 < Z < 0.1$, but uses it at exactly $Z = 0.04$ (its test is `ZTAB.LE.0.04`) when the surface $X > 0.8$.
4. **Fixed positions in the $Z$ grid.** The shifts for tables 9 and 10 use `NUMZ - 6` and `NUMZ - 4`, which assume where 0.04 and 0.1 sit in the 13-value $Z$ grid. Worth a comment, or a search.
