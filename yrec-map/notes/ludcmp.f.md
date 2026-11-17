## Explanation

**Purpose.** `LUDCMP` replaces a square matrix by its LU decomposition with partial pivoting (Crout's method with implicit scaling), as *Numerical Recipes*' `LUDCMP`. [`LUBKSB`](lubksb.f.md#lubksb) then solves systems with it.

**How it fits.** Called only by [`THDIFF`](thdiff.f.md#thdiff) (the diffusion coefficients of Thoul et al., by its name). No COMMON blocks, no calls. Arguments: `A(NP,NP)` (overwritten by L and U), `N`, `NP`, the row permutation `INDX`, and `D` = $`\pm 1`$ (the parity of the row swaps).

**The method.** It first stores each row's scale, $`1/\max_k |a_{ik}|`$, and stops with `STOP 'Singular matrix.'` if a row is all zero. Then, for each column $`j`$ it computes the $`U`$ entries above the diagonal and the candidates below, picks the pivot with the largest scaled magnitude $`|a_{ij}|/\max_k |a_{ik}|`$, swaps rows, and divides the sub-diagonal entries by the pivot. A zero pivot is replaced by `TINY` = $`10^{-20}`$.

The scale vector `VV` has the fixed size `NMAX` = 100 ([line 13](https://github.com/yreclab/yrec/blob/7be4133/src/ludcmp.f#L13); [line 28](https://github.com/yreclab/yrec/blob/7be4133/src/ludcmp.f#L28)), and `N` is not checked against it. THDIFF passes `N` = $`2M + 2`$ with its own arrays sized 42 ([thdiff.f, lines 48–54](https://github.com/yreclab/yrec/blob/7be4133/src/thdiff.f#L48-L54); [thdiff.f, line 72](https://github.com/yreclab/yrec/blob/7be4133/src/thdiff.f#L72); [thdiff.f, line 264](https://github.com/yreclab/yrec/blob/7be4133/src/thdiff.f#L264)), so `N` $`\le 42`$; `KNOWN_ISSUES.md` (lines 1845–1848) keeps `NMAX` per routine on purpose (settled from the code, Nov 9, 2026).

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE` with explicit declarations.

### LUDCMP

LU decomposition with partial pivoting (*Numerical Recipes*).
