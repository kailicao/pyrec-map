## Explanation

**Purpose.** `HSOLVE` performs the last stage of the Henyey solution of the stellar-structure equations: it applies the surface boundary condition and back-substitutes through the shells, turning the forward-eliminated matrix into the corrections to the variables at every point.

**How it fits.** Called only by [[crrect.f#CRRECT|`CRRECT`]], which builds the Henyey system; the forward elimination is done shell by shell by [[reduce.f#REDUCE|`REDUCE`]] (called from COEFFT), whose page works out what `HHA` and `HHB` hold. Arguments: `M` (number of points), `HHA(4,2,M)` and `HHB(4,M)` (the eliminated coefficients and right-hand sides, overwritten), `HSRF(6)` (the surface boundary conditions). No modules but `DIMENSIONS_MOD` (for `JSON`), no calls.

**The method.** *Inferred from the code;* the code has no comments. At the surface it solves a 2×2 system for the two corrections at point `M`, here written $\delta p$ and $\delta t$ (`QQQP`, `QQQT`; the corrections to $\log P$ and $\log T$ at point `M`, base 10, since CRRECT adds `HHB(1,i)` to `HP` and `HHB(2,i)` to `HT`):

$$\begin{pmatrix} s_1 - a_{31} & s_2 - a_{32}\\ s_4 - a_{41} & s_5 - a_{42}\end{pmatrix}\begin{pmatrix}\delta p\\ \delta t\end{pmatrix} = \begin{pmatrix} s_3 - b_3\\ s_6 - b_4\end{pmatrix},$$

with $s_k$ = `HSRF(k)` and $a_{ij}$, $b_i$ taken at point `M`. Then, from the surface inward ($i = M, M-1, \dots, 2$), the rows stored at point $i$ give

$$\delta p(i-1) = b_1(i) - a_{11}(i)\,\delta p(i) - a_{12}(i)\,\delta t(i),\qquad \delta t(i-1) = b_2(i) - a_{21}(i)\,\delta p(i) - a_{22}(i)\,\delta t(i),$$

$$y_k(i) = b_k(i) - a_{k1}(i)\,\delta p(i) - a_{k2}(i)\,\delta t(i)\quad (k = 3, 4),$$

and the centre point is finished the same way. On return `HHB(1..4, i)` holds the four corrections at each point, $\delta\log P$, $\delta\log T$, $\delta\log r$ and $\delta L$ ($L_\odot$), in the order of [[reduce.f#REDUCE|REDUCE]]'s rows. The six `HSRF` entries are the two surface conditions set by CRRECT: `HSRF(1..3)` the linearized $\log r$ relation of the envelope fit, `HSRF(4..6)` its $\log L$ relation, multiplied by $\ln 10\,L$ since $L$ is the unknown ([[crrect.f#CRRECT|CRRECT]], step 4).

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`, and the array size `JSON` from `DIMENSIONS_MOD`.

## Questions for the experts

1. **A comment on the variables.** `HHB(1..4)` holds the corrections to $\log P$, $\log T$, $\log r$ and $L$ (from CRRECT and REDUCE, above), but the code does not say so, nor which equations the six `HSRF` entries are. A comment would help readers of `CRRECT`.
2. **Singular surface system.** There is no check that $s_1 - a_{31}$ or the pivot is nonzero.

### HSOLVE

Surface 2×2 solve followed by back-substitution through the shells (above).
