## Explanation

**Purpose.** `INTER3` returns the weights of 3-point Lagrange interpolation, and of its first derivative, at a point $`x`$.

**How it fits.** Called by [`SETSCV`](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L4-L255) (interpolation in the SCV equation-of-state tables), [`SURFP`](surfp.f.md#surfp) and [`KCSURFP`](kcsurfp.f.md#kcsurfp) (interpolation in gravity in the surface-pressure tables). No modules, no calls. The 4-point version is [`INTERP`](interp.f.md#interp).

**The header's "Livermore opacity tables" is from an older use.** The comment says `INTER3` is "the interpolation routine for density in the Livermore opacity tables" ([lines 18–19](https://github.com/yreclab/yrec/blob/7be4133/src/inter3.f#L18-L19)), but its only callers are the SCV EOS set-up ([setscv.f, line 114](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L114); [setscv.f, line 193](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L193); [setscv.f, line 208](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L208); [setscv.f, line 242](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L242)) and the surface-pressure routines ([surfp.f, line 81](https://github.com/yreclab/yrec/blob/7be4133/src/surfp.f#L81); [kcsurfp.f, line 90](https://github.com/yreclab/yrec/blob/7be4133/src/kcsurfp.f#L90)), none an opacity routine.

**The method.** For nodes $`a_1, a_2, a_3`$ (`A`), the weights `B` and derivative weights `C` are

```math
B_i(x) = \prod_{j\ne i}\frac{x-a_j}{a_i-a_j},\qquad C_i(x) = \frac{dB_i}{dx} = \frac{\sum_{j\ne i}\prod_{k\ne i,j}(x-a_k)}{\prod_{j\ne i}(a_i-a_j)},
```

so that $`f(x) \approx \sum_i B_i f(a_i)`$ and $`f'(x) \approx \sum_i C_i f(a_i)`$.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

### INTER3

3-point Lagrange weights and derivative weights (above).
