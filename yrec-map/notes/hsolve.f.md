## Explanation

**Purpose.** `HSOLVE` performs the last stage of the Henyey solution of the stellar-structure equations: it applies the surface boundary condition and back-substitutes through the shells, turning the forward-eliminated matrix into the corrections to the variables at every point.

**How it fits.** Called only by [[crrect.f#CRRECT|`CRRECT`]], which builds and eliminates the Henyey system. Arguments: `M` (number of points), `HHA(4,2,M)` and `HHB(4,M)` (the eliminated coefficients and right-hand sides, overwritten), `HSRF(6)` (the surface boundary conditions). No modules but `DIMENSIONS_MOD` (for `JSON`), no calls.

**The method.** *Inferred from the code;* the code has no comments. At the surface it solves a 2×2 system for the two corrections at point `M`, here written $\delta p$ and $\delta t$ (`QQQP`, `QQQT`; probably the corrections to $\ln P$ and $\ln T$):

$$\begin{pmatrix} s_1 - a_{31} & s_2 - a_{32}\\ s_4 - a_{41} & s_5 - a_{42}\end{pmatrix}\begin{pmatrix}\delta p\\ \delta t\end{pmatrix} = \begin{pmatrix} s_3 - b_3\\ s_6 - b_4\end{pmatrix},$$

with $s_k$ = `HSRF(k)` and $a_{ij}$, $b_i$ taken at point `M`. Then, from the surface inward ($i = M, M-1, \dots, 2$), the rows stored at point $i$ give

$$\delta p(i-1) = b_1(i) - a_{11}(i)\,\delta p(i) - a_{12}(i)\,\delta t(i),\qquad \delta t(i-1) = b_2(i) - a_{21}(i)\,\delta p(i) - a_{22}(i)\,\delta t(i),$$

$$y_k(i) = b_k(i) - a_{k1}(i)\,\delta p(i) - a_{k2}(i)\,\delta t(i)\quad (k = 3, 4),$$

and the centre point is finished the same way. On return `HHB(1..4, i)` holds the four corrections at each point.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`, and the array size `JSON` from `DIMENSIONS_MOD`.

## Questions for the experts

1. **Which variables.** Which four variables are `HHB(1..4)` at return (presumably $\ln P$, $\ln T$, $\ln r$, $L$ in some order), and which equations are the six `HSRF` entries? A comment would help readers of `CRRECT`.
2. **Singular surface system.** There is no check that $s_1 - a_{31}$ or the pivot is nonzero.

### HSOLVE

Surface 2×2 solve followed by back-substitution through the shells (above).
