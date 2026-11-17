## Explanation

**Purpose.** `SPLINJ` computes the second derivatives of a natural cubic spline through $`(x_i, y_i)`$, $`i = 1, \dots, N`$ ($`y''_1 = y''_N = 0`$), for interpolation with [SPLINT](splint.f.md#splint). The algorithm, with its equations, is that of [splinc.f](splinc.f.md); only the arrays differ: here they are sized `N` (adjustable arrays), not 5000, and the routine has no `SAVE`. The work array `U(N)` ([line 10](https://github.com/yreclab/yrec/blob/7be4133/src/splinj.f#L10)) is a local with an adjustable size, an automatic array: not allowed in Fortran 77, standard in Fortran 90, which YREC is (its modules, `IMPLICIT NONE` and the F90 spellings already in use: `docs/archive/F90_CONVERSION_PLAN.md`, line 38) (settled from the code, Nov 9, 2026).

**How it fits.**
- **Who calls it:** [BOOLE](boole.f.md#boole) and [CALCAD](calcad.f.md#calcad), which then call [SPLINT](splint.f.md#splint).
- **COMMON blocks:** none.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

### SPLINJ

Natural cubic spline's second derivatives, with arrays sized `N`; the same algorithm as [SPLINC](splinc.f.md#splinc).
