## Explanation

**Purpose.** One step of the elimination in the Henyey method: for the pair of shells $(i-1, i)$, it forms the residuals of the four difference equations of stellar structure and eliminates the unknowns of shell $i-1$, leaving relations for the corrections at shell $i$. Its name and the comments ("REDUCE MATRIX FOR PAIR OF POINTS (IM-1,IM)", in the caller) say this; that it is the forward sweep of a Henyey solver, with [[hsolve.f#HSOLVE|`HSOLVE`]] the backward one, is our reading of the algebra.

**How it fits.**
- **Who calls it:** [[coefft.f#COEFFT|`COEFFT`]], once for each shell `IM` > 1, right after computing that shell's right-hand sides and their derivatives. For the first shell, `COEFFT` sets the central boundary conditions in the same arrays instead.
- **Inputs:** the shell index `I`; the model's variables `HP`, `HT`, `HR`, `HL` (pressure, temperature, radius and luminosity, in the code's variables) and the mass variable `HS`; and for each equation $y \in \{P, T, R, L\}$ its right-hand side $f_y$ at shells $i-1$ (`QP0`, `QT0`, `QR0`, `QL0`) and $i$ (`QP`, …), with its partial derivatives (`QPR` is $\partial f_P/\partial R$, `QTL` is $\partial f_T/\partial L$, and so on; a `0` marks shell $i-1$).
- **Outputs:** the arrays `HHA(4,2,JSON)` and `HHB(4,JSON)` at shell `I` (the reduced coefficients and right-hand sides), and `HMAX(4)`, the largest residual of each equation so far. `COEFFT` returns them to [[crrect.f#CRRECT|`CRRECT`]], which passes them to [[hsolve.f#HSOLVE|`HSOLVE`]], the back-substitution that gives the corrections.
- **Modules:** `CONSTANTS_MOD`, for `CLN` $= \ln 10$; `DIMENSIONS_MOD`, for `JSON`.

**The method.** Each structure equation is differenced with the trapezoidal rule. With $\Delta s = s_i - s_{i-1}$ (`HS`), the residual of equation $y$ is

$$b_y = \frac{\Delta s}{2}\,\bigl(f_{y,i-1} + f_{y,i}\bigr) - \bigl(y_i - y_{i-1}\bigr),$$

stored in `HHB(k,I)`, with $|b_y|$ tracked in `HMAX(k)`. The linearized (Newton) equations for the corrections $\delta y$ are, for each equation $y$,

$$\sum_{k}\Bigl[\Bigl(-\epsilon_{yk} - \tfrac{\Delta s}{2}\ln 10\,\frac{\partial f_{y,i-1}}{\partial y_k}\Bigr)\delta y_{k,i-1} + \Bigl(\epsilon_{yk} - \tfrac{\Delta s}{2}\ln 10\,\frac{\partial f_{y,i}}{\partial y_k}\Bigr)\delta y_{k,i}\Bigr] = b_y ,$$

with $k$ over $P, T, R, L$ ($\epsilon_{yk}$ is 1 when $k = y$, else 0; the factor `CLN` $= \ln 10$ probably because the variables are base-10 logarithms). Read from the algebra, the comments' columns are: 1–2 $\delta R_{i-1}$, $\delta L_{i-1}$; 3–4 $\delta P_{i-1}$, $\delta T_{i-1}$; 5–6 $\delta R_i$, $\delta L_i$; and $\delta P_i$, $\delta T_i$ remain. The work matrix `Q(k,1:2)` holds the coefficients of $\delta P_{i-1}$, $\delta T_{i-1}$, and `HHA(k,1:2,I)` those of $\delta P_i$, $\delta T_i$.

1. **Columns 1 and 2.** The previous call left $\delta R_{i-1} = $ `HHB(3,I-1)` $- \sum_m$ `HHA(3,m,I-1)` $u_m$, and the same for $\delta L_{i-1}$ with row 4, where $u = (\delta P_{i-1}, \delta T_{i-1})$. Substituting them removes $\delta R_{i-1}$, $\delta L_{i-1}$. In the $L$ row the coefficient of $\delta L_{i-1}$ is $-1$ (no $\partial f_L/\partial L$ term), so its terms enter with a plus sign.
2. **Columns 6, 5, 4, 3,** in turn ("PIVOT ON ROW-4 AND COLUMN-6", then row 3 and column 5, row 2 and column 4, row 1 and column 3): Gauss–Jordan steps that eliminate $\delta L_i$, $\delta R_i$, $\delta T_{i-1}$ and $\delta P_{i-1}$.

At the end, each of the four unknowns $x_k = (\delta P_{i-1}, \delta T_{i-1}, \delta R_i, \delta L_i)$ is given in terms of the two unknowns of shell $i$:

$$x_k = \texttt{HHB}(k,i) - \texttt{HHA}(k,1,i)\,\delta P_i - \texttt{HHA}(k,2,i)\,\delta T_i .$$

Rows 3 and 4 are what the next call (shell $i+1$) uses in step 1; [[hsolve.f#HSOLVE|`HSOLVE`]] fixes $\delta P$, $\delta T$ at the last shell from the surface conditions (`HSRF`), then applies this relation from the surface inward.

**Design.** No pivoting by size: the divisions by `Q(2,2)`, `Q(1,1)` and $1 - \tfrac{\Delta s}{2}\ln 10\,\partial f_R/\partial R$ assume these are not zero. The routine has 39 arguments, the equations' derivatives one by one.

**Changed since `rp_1`.** Declarations only: `/CONST1/` to `CONSTANTS_MOD`, `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Questions for the experts

1. **The meaning of the columns.** The comments name the pivots by row and column of a matrix that is written nowhere; the column map above is read from the algebra. Can it be confirmed, and documented in the code?
2. **No safeguard against a zero pivot.** `DIV = 1.0D0/Q(2,2)` and `1.0D0/Q(1,1)` are taken without a check. Has a breakdown ever been seen, for instance in very thin shells?
