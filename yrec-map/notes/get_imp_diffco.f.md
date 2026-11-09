## Explanation

**Purpose.** `GET_IMP_DIFFCO` rebuilds the tridiagonal matrix of an implicit diffusion step for hydrogen, after correcting the diffusion coefficients for the change in $X$ found in the previous iteration.

**How it fits.**
- **Who calls it:** [[grsett.f#GRSETT|GRSETT]] (gravitational settling) and [[microdiff_run.f#MICRODIFF_RUN|MICRODIFF_RUN]] (the newer microscopic diffusion), inside their iterations.
- **Inputs:** `ALPHA` (the step's coefficients per point), `ECOD2_H` (diffusion coefficients at the half points), `EQCOD2X_H` (their derivatives with respect to $X$), `EX_H` (the change in $X$), `NPT`.
- **Outputs:** the matrix diagonals `A`, `B`, `C`, and `ECOD2_H` updated in place.
- **The change passed in** is that of the last iteration only: GRSETT sets `EX_H` from `EX - EX_P` and then `EX_P = EX`, and MICRODIFF_RUN does the same with `ED_H`. So the corrections to `ECOD2_H` add up, but GRSETT stores each change one midpoint off from the coefficient it corrects, and never sets `EX_H(1)` ([[grsett.f#b1]]). MICRODIFF_RUN also sets `EQCOD2X_H` to zero before each call (its comment: only used by the old settling routine), so there the coefficients stay fixed and only the matrix is rebuilt.

**The method.** First $D_{i+1/2} \leftarrow D_{i+1/2} + (\partial D/\partial X)_{i+1/2}\,\Delta X_{i+1/2}$. Then, for the interior points,
$$a_i = -\alpha_i D_{i-1/2},\qquad b_i = 1 + \alpha_i(D_{i-1/2} + D_{i+1/2}),\qquad c_i = -\alpha_i D_{i+1/2},$$
with zero-flux ends: $a_1 = 0$, $b_1 = 1 + \alpha_1 D_{3/2}$, and $c_N = 0$, $b_N = 1 + \alpha_N D_{N-1/2}$. This is the backward-Euler matrix for $\partial X/\partial t = \partial_x(D\,\partial_x X)$ on the solver's grid, as far as can be told from the code alone.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`, and the array size `JSON` from `DIMENSIONS_MOD`.

### GET_IMP_DIFFCO

Updates the diffusion coefficients for the last change in $X$ and rebuilds the implicit tridiagonal matrix (equations above).
