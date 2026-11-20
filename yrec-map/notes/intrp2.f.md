## Explanation

**Purpose.** `INTRP2` returns the weights of 4-point Lagrange interpolation at a point $`x`$, without the derivative weights: the same as [`INTERP`](interp.f.md#interp) minus its `C` output.

**How it fits.** Called by the opacity-table routines [`ALEX06TAB`](alex06tab.f.md#alex06tab), [`GETOPAL95`](getopal95.f.md#getopal95), [`OP95XTAB`](https://github.com/yreclab/yrec/blob/7be4133/src/op95xtab.f#L6-L104) and [`OP95ZTAB`](https://github.com/yreclab/yrec/blob/7be4133/src/op95ztab.f#L6-L126) (`ALX8TH`, `ALXZTAB` and `YALO3D` also called it; removed since `rp_1`), by the diffusion regridding [`EQUAL_TO_MODEL`](equal_to_model.f.md#equal_to_model) and [`MICRODIFF_ETM`](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_etm.f#L2-L174), and by [`PHYSIC`](https://github.com/yreclab/yrec/blob/7be4133/src/physic.f#L3-L191). No COMMON blocks, no calls.

**The header has a typo and a copied comment.** The banner says "INTEP2" ([line 4](https://github.com/yreclab/yrec/blob/7be4133/src/intrp2.f#L4)), and the comment, copied from [INTERP](interp.f.md#interp), still speaks of the VandenBerg opacity tables only ([lines 15–17](https://github.com/yreclab/yrec/blob/7be4133/src/intrp2.f#L15-L17)).

**The method.** $`B_i(x) = \prod_{j\ne i}(x-a_j)/(a_i-a_j)`$ for $`i = 1..4`$.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE` with explicit declarations. Three of its callers (`ALX8TH`, `ALXZTAB`, `YALO3D`) are removed since `rp_1`.

### INTRP2

4-point Lagrange weights only.
