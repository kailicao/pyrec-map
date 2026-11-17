## Explanation

**Purpose.** `KSPLINE` computes the second derivatives of a natural cubic spline through exactly 4 points (the size `NM` = 4 is fixed), as in *Numerical Recipes*' `SPLINE`. [`KSPLINT`](ksplint.f.md#ksplint) evaluates the spline.

**How it fits.** Called by the surface-pressure routines [`KCSURFP`](kcsurfp.f.md#kcsurfp) and [`SURFP`](surfp.f.md#surfp), the SCV equation of state [`EQSCVE`](eqscve.f.md#eqscve), and [`TAUINTNEW`](tauintnew.f.md#tauintnew). No COMMON blocks, no calls.

**The method.** The tridiagonal system for the second derivatives $`y''_i`$ of a natural spline ($`y''_1 = y''_4 = 0`$), solved by forward elimination and back-substitution.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE` with explicit declarations.

### KSPLINE

Natural cubic spline on 4 points: returns $`y''`$ in `Y2`.
