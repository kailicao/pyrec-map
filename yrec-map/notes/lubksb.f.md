## Explanation

**Purpose.** `LUBKSB` solves $`A\,x = b`$ given the LU decomposition of $`A`$ from [`LUDCMP`](ludcmp.f.md#ludcmp) (*Numerical Recipes*' `LUBKSB`). The solution overwrites `B`.

**How it fits.** Called only by [`THDIFF`](thdiff.f.md#thdiff). No COMMON blocks, no calls.

**The method.** Forward substitution with $`L`$ (unpacking the permutation `INDX`, and skipping leading zeros of $`b`$), then back-substitution with $`U`$:

```math
y_i = b_{p(i)} - \sum_{j<i} L_{ij}\,y_j,\qquad x_i = \frac{1}{U_{ii}}\Big(y_i - \sum_{j>i} U_{ij}\,x_j\Big).
```

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE` with explicit declarations.

### LUBKSB

Forward and back substitution (above).
