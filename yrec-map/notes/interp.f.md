## Explanation

**Purpose.** `INTERP` returns the weights of 4-point Lagrange interpolation, and of its first derivative, at a point $x$.

**How it fits.** Called by [[eqscve.f#EQSCVE|`EQSCVE`]] and [[eqscvg.f#EQSCVG|`EQSCVG`]] (the SCV equation of state), [[getalex06.f#GETALEX06|`GETALEX06`]] and [[getopal95.f#GETOPAL95|`GETOPAL95`]] (opacity tables; `YALO3D` is removed since `rp_1`), and [[microdiff_mte.f#MICRODIFF_MTE|`MICRODIFF_MTE`]] and [[model_to_equal.f#MODEL_TO_EQUAL|`MODEL_TO_EQUAL`]] (regridding for diffusion). No modules, no calls. The version without derivatives is [[intrp2.f#INTRP2|`INTRP2`]]; the 3-point one is [[inter3.f#INTER3|`INTER3`]].

> **Question** ([[#L16-L18]]). **Stale comment.** The comment calls it "the interpolation routine for the VandenBerg opacity tables (CAPPA)"; it now serves the EOS, several opacity tables, and the diffusion grids. A comment to update?

**The method.** For nodes $a_1,\dots,a_4$,

$$B_i(x) = \prod_{j\ne i}\frac{x-a_j}{a_i-a_j},\qquad C_i(x) = \frac{dB_i}{dx},$$

returned in `B` and `C`; then $f(x)\approx\sum_i B_i f(a_i)$ and $f'(x)\approx\sum_i C_i f(a_i)$. Used in a table, the interpolant is piecewise: it is continuous where the four-point stencil shifts from one cell to the next, but its derivative, and so the derivative weights `C` the equation of state and opacities use, jump there.

> **Question** ([[#L37-L40]]). **Derivative jumps.** Piecewise four-point Lagrange interpolation gives derivatives (such as $\partial\ln\kappa/\partial\ln T$) that jump where the stencil shifts. Do these jumps affect the convergence of the Henyey iteration, which uses them, and would a smoother interpolation (such as the splines some other tables use) be preferable?

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`. One caller, `YALO3D`, is removed with the obsolete opacity options.

### INTERP

4-point Lagrange weights and derivative weights (above).
