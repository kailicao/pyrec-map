## Explanation

**Purpose.** `INTERP` returns the weights of 4-point Lagrange interpolation, and of its first derivative, at a point $`x`$.

**How it fits.** Called by [`EQSCVE`](eqscve.f.md#eqscve) and [`EQSCVG`](eqscvg.f.md#eqscvg) (the SCV equation of state), [`GETALEX06`](getalex06.f.md#getalex06) and [`GETOPAL95`](getopal95.f.md#getopal95) (opacity tables; `YALO3D` is removed since `rp_1`), and [`MICRODIFF_MTE`](microdiff_mte.f.md#microdiff_mte) and [`MODEL_TO_EQUAL`](model_to_equal.f.md#model_to_equal) (regridding for diffusion). No modules, no calls. The version without derivatives is [`INTRP2`](intrp2.f.md#intrp2); the 3-point one is [`INTER3`](inter3.f.md#inter3).

**The header's "VandenBerg opacity tables" is from an older use.** The comment calls it "THE INTERPOLATION ROUTINE FOR THE VANDENBERG OPACITY TABLES(CAPPA)" ([lines 16–18](https://github.com/yreclab/yrec/blob/7be4133/src/interp.f#L16-L18)); it now serves the SCV EOS ([EQSCVE](eqscve.f.md#eqscve), [EQSCVG](eqscvg.f.md#eqscvg)), the opacity tables of [GETOPAL95](getopal95.f.md#getopal95) and [GETALEX06](getalex06.f.md#getalex06), and the diffusion grids ([MICRODIFF_MTE](microdiff_mte.f.md#microdiff_mte), [MODEL_TO_EQUAL](model_to_equal.f.md#model_to_equal)), so the comment could describe a general four-point Lagrange interpolation.

**The method.** For nodes $`a_1,\dots,a_4`$,

```math
B_i(x) = \prod_{j\ne i}\frac{x-a_j}{a_i-a_j},\qquad C_i(x) = \frac{dB_i}{dx},
```

returned in `B` and `C`; then $`f(x)\approx\sum_i B_i f(a_i)`$ and $`f'(x)\approx\sum_i C_i f(a_i)`$. Used in a table, the interpolant is piecewise: it is continuous where the four-point stencil shifts from one cell to the next, but its derivative, and so the derivative weights `C` the equation of state and opacities use, jump there.

> **Question** ([lines 37–40](https://github.com/yreclab/yrec/blob/7be4133/src/interp.f#L37-L40)). **Derivative jumps.** Piecewise four-point Lagrange interpolation gives derivatives (such as $`\partial\ln\kappa/\partial\ln T`$) that jump where the stencil shifts. Do these jumps affect the convergence of the Henyey iteration, which uses them, and would a smoother interpolation (such as the splines some other tables use) be preferable?

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`. One caller, `YALO3D`, is removed with the obsolete opacity options.

### INTERP

4-point Lagrange weights and derivative weights (above).
