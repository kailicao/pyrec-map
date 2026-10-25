## Explanation

**Purpose.** `INTRP2` returns the weights of 4-point Lagrange interpolation at a point $x$, without the derivative weights: the same as [[interp.f#INTERP|`INTERP`]] minus its `C` output.

**How it fits.** Called by the opacity-table routines [[alex06tab.f#ALEX06TAB|`ALEX06TAB`]], [[alx8th.f#ALX8TH|`ALX8TH`]], [[alxztab.f#ALXZTAB|`ALXZTAB`]], [[getopal95.f#GETOPAL95|`GETOPAL95`]], [[op95xtab.f#OP95XTAB|`OP95XTAB`]], [[op95ztab.f#OP95ZTAB|`OP95ZTAB`]] and [[yalo3d.f#YALO3D|`YALO3D`]], by the diffusion regridding [[equal_to_model.f#EQUAL_TO_MODEL|`EQUAL_TO_MODEL`]] and [[microdiff_etm.f#MICRODIFF_ETM|`MICRODIFF_ETM`]], and by [[physic.f#PHYSIC|`PHYSIC`]]. No COMMON blocks, no calls.

**The method.** $B_i(x) = \prod_{j\ne i}(x-a_j)/(a_i-a_j)$ for $i = 1..4$.

## Questions for the experts

1. **Header typo and stale comment.** The banner says "INTEP2", and the comment still speaks of the VandenBerg opacity tables only.

### INTRP2

4-point Lagrange weights only.
