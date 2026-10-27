## Explanation

**Purpose.** `GET_IMP_DIFFCO` rebuilds the tridiagonal matrix of an implicit diffusion step for hydrogen, after correcting the diffusion coefficients for the change in $X$ found in the previous iteration.

**How it fits.**
- **Who calls it:** [[grsett.f#GRSETT|GRSETT]] (gravitational settling) and [[microdiff_run.f#MICRODIFF_RUN|MICRODIFF_RUN]] (the newer microscopic diffusion), inside their iterations.
- **Inputs:** `ALPHA` (the step's coefficients per point), `ECOD2_H` (diffusion coefficients at the half points), `EQCOD2X_H` (their derivatives with respect to $X$), `EX_H` (the change in $X$), `NPT`.
- **Outputs:** the matrix diagonals `A`, `B`, `C`, and `ECOD2_H` updated in place.
- **The change passed in** is that of the last iteration only: GRSETT sets `EX_H` from `EX - EX_P` and then `EX_P = EX`, and MICRODIFF_RUN does the same with `ED_H`. So the corrections to `ECOD2_H` add up correctly. MICRODIFF_RUN also sets `EQCOD2X_H` to zero before each call (its comment: only used by the old settling routine), so there the coefficients stay fixed and only the matrix is rebuilt.

**The method.** First $D_{i+1/2} \leftarrow D_{i+1/2} + (\partial D/\partial X)_{i+1/2}\,\Delta X_{i+1/2}$. Then, for the interior points,
$$a_i = -\alpha_i D_{i-1/2},\qquad b_i = 1 + \alpha_i(D_{i-1/2} + D_{i+1/2}),\qquad c_i = -\alpha_i D_{i+1/2},$$
with zero-flux ends: $a_1 = 0$, $b_1 = 1 + \alpha_1 D_{3/2}$, and $c_N = 0$, $b_N = 1 + \alpha_N D_{N-1/2}$. This is the backward-Euler matrix for $\partial X/\partial t = \partial_x(D\,\partial_x X)$ on the solver's grid, as far as can be told from the code alone.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`, and the array size `JSON` from `DIMENSIONS_MOD`.

## Questions for the experts

1. **Midpoint indices.** Here `ECOD2_H(I)` is the coefficient between points `I` and `I+1` (`B(1)` uses `ECOD2_H(1)`), the convention of [[model_to_equal.f#MODEL_TO_EQUAL|MODEL_TO_EQUAL]] and [[lax_wendrof1.f#LAX_WENDROF1|LAX_WENDROF1]] for `EX_H(1..NPT-1)` too. But GRSETT's loop sets `EX_H(I)`, for `I = 2..NPT`, from points `I-1` and `I`, the midpoint one lower, and leaves `EX_H(1)` as LAX_WENDROF1 set it. So `ECOD2_H(I)` is probably corrected with the change at the neighbouring midpoint. Is this an off-by-one error in GRSETT?

### GET_IMP_DIFFCO

Updates the diffusion coefficients for the last change in $X$ and rebuilds the implicit tridiagonal matrix (equations above).
