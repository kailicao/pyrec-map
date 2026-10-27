## Explanation

**Purpose.** `LUDCMP` replaces a square matrix by its LU decomposition with partial pivoting (Crout's method with implicit scaling), as *Numerical Recipes*' `LUDCMP`. [[lubksb.f#LUBKSB|`LUBKSB`]] then solves systems with it.

**How it fits.** Called only by [[thdiff.f#THDIFF|`THDIFF`]] (the diffusion coefficients of Thoul et al., by its name). No COMMON blocks, no calls. Arguments: `A(NP,NP)` (overwritten by L and U), `N`, `NP`, the row permutation `INDX`, and `D` = ±1 (the parity of the row swaps).

**The method.** It first stores each row's scale, $1/\max_k |a_{ik}|$, and stops with `STOP 'Singular matrix.'` if a row is all zero. Then, for each column $j$ it computes the $U$ entries above the diagonal and the candidates below, picks the pivot with the largest scaled magnitude $|a_{ij}|/\max_k |a_{ik}|$, swaps rows, and divides the sub-diagonal entries by the pivot. A zero pivot is replaced by `TINY` = $10^{-20}$.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE` with explicit declarations.

## Questions for the experts

1. **Fixed work size.** The scaling vector `VV` has `NMAX` = 100 entries and `N` is not checked against it.

### LUDCMP

LU decomposition with partial pivoting (*Numerical Recipes*).
