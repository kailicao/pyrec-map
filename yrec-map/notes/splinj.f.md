## Explanation

**Purpose.** `SPLINJ` computes the second derivatives of a natural cubic spline through $(x_i, y_i)$, $i = 1, \dots, N$ ($y''_1 = y''_N = 0$), for interpolation with [[splint.f#SPLINT|SPLINT]]. The algorithm, with its equations, is that of [[splinc.f|splinc.f]]; only the arrays differ: here they are sized `N` (adjustable arrays), not 5000, and the routine has no `SAVE`. The work array `U(N)` ([[#L10]]) is a local with an adjustable size, an automatic array: not allowed in Fortran 77, standard in Fortran 90, which YREC is (its modules, `IMPLICIT NONE` and the F90 spellings already in use: `docs/archive/F90_CONVERSION_PLAN.md`, line 38) (settled from the code, Nov 9, 2026).

**How it fits.**
- **Who calls it:** [[boole.f#BOOLE|BOOLE]] and [[calcad.f#CALCAD|CALCAD]], which then call [[splint.f#SPLINT|SPLINT]].
- **COMMON blocks:** none.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

### SPLINJ

Natural cubic spline's second derivatives, with arrays sized `N`; the same algorithm as [[splinc.f#SPLINC|SPLINC]].
