## Explanation

**Purpose.** `INTERP` returns the weights of 4-point Lagrange interpolation, and of its first derivative, at a point $x$.

**How it fits.** Called by [[eqscve.f#EQSCVE|`EQSCVE`]] and [[eqscvg.f#EQSCVG|`EQSCVG`]] (the SCV equation of state), [[getalex06.f#GETALEX06|`GETALEX06`]], [[getopal95.f#GETOPAL95|`GETOPAL95`]] and [[yalo3d.f#YALO3D|`YALO3D`]] (opacity tables), and [[microdiff_mte.f#MICRODIFF_MTE|`MICRODIFF_MTE`]] and [[model_to_equal.f#MODEL_TO_EQUAL|`MODEL_TO_EQUAL`]] (regridding for diffusion). No COMMON blocks, no calls. The version without derivatives is [[intrp2.f#INTRP2|`INTRP2`]]; the 3-point one is [[inter3.f#INTER3|`INTER3`]].

**The method.** For nodes $a_1,\dots,a_4$,

$$B_i(x) = \prod_{j\ne i}\frac{x-a_j}{a_i-a_j},\qquad C_i(x) = \frac{dB_i}{dx},$$

returned in `B` and `C`; then $f(x)\approx\sum_i B_i f(a_i)$ and $f'(x)\approx\sum_i C_i f(a_i)$.

## Questions for the experts

1. **Stale comment.** The comment calls it "the interpolation routine for the VandenBerg opacity tables (CAPPA)"; it now serves the EOS, several opacity tables and the diffusion grids.

### INTERP

4-point Lagrange weights and derivative weights (above).
