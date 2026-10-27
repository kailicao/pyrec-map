## Explanation

**Purpose.** `INTER3` returns the weights of 3-point Lagrange interpolation, and of its first derivative, at a point $x$.

**How it fits.** Called by [[setscv.f#SETSCV|`SETSCV`]] (interpolation in the SCV equation-of-state tables), [[surfp.f#SURFP|`SURFP`]] and [[kcsurfp.f#KCSURFP|`KCSURFP`]] (interpolation in gravity in the surface-pressure tables). No modules, no calls. The 4-point version is [[interp.f#INTERP|`INTERP`]].

**The method.** For nodes $a_1, a_2, a_3$ (`A`), the weights `B` and derivative weights `C` are

$$B_i(x) = \prod_{j\ne i}\frac{x-a_j}{a_i-a_j},\qquad C_i(x) = \frac{dB_i}{dx} = \frac{\sum_{j\ne i}\prod_{k\ne i,j}(x-a_k)}{\prod_{j\ne i}(a_i-a_j)},$$

so that $f(x) \approx \sum_i B_i f(a_i)$ and $f'(x) \approx \sum_i C_i f(a_i)$.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

## Questions for the experts

1. **Stale comment.** The comment says `INTER3` is "the interpolation routine for density in the Livermore opacity tables", but its callers are the SCV EOS set-up and the surface-pressure routines. Is the comment from an older use?

### INTER3

3-point Lagrange weights and derivative weights (above).
