## Explanation

**Purpose.** `SPLINJ` computes the second derivatives of a natural cubic spline through $(x_i, y_i)$, $i = 1, \dots, N$ ($y''_1 = y''_N = 0$), for interpolation with [[splint.f#SPLINT|SPLINT]]. The algorithm, with its equations, is that of [[splinc.f|splinc.f]]; only the arrays differ: here they are sized `N` (adjustable arrays), not 5000, and the routine has no `SAVE`.

**How it fits.**
- **Who calls it:** [[boole.f#BOOLE|BOOLE]] and [[calcad.f#CALCAD|CALCAD]], which then call [[splint.f#SPLINT|SPLINT]].
- **COMMON blocks:** none.

## Questions for the experts

1. **The work array `U`.** `U(N)` is a local array with an adjustable size, which standard Fortran 77 does not allow (only dummy arguments may have adjustable bounds). It compiles as an automatic array under modern compilers. Is that the intended reliance on an extension?

### SPLINJ

Natural cubic spline's second derivatives, with arrays sized `N`; the same algorithm as [[splinc.f#SPLINC|SPLINC]].
