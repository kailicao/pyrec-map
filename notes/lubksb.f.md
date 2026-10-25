## Explanation

**Purpose.** `LUBKSB` solves $A\,x = b$ given the LU decomposition of $A$ from [[ludcmp.f#LUDCMP|`LUDCMP`]] (*Numerical Recipes*' `LUBKSB`). The solution overwrites `B`.

**How it fits.** Called only by [[thdiff.f#THDIFF|`THDIFF`]]. No COMMON blocks, no calls.

**The method.** Forward substitution with $L$ (unpacking the permutation `INDX`, and skipping leading zeros of $b$), then back-substitution with $U$:

$$y_i = b_{p(i)} - \sum_{j<i} L_{ij}\,y_j,\qquad x_i = \frac{1}{U_{ii}}\Big(y_i - \sum_{j>i} U_{ij}\,x_j\Big).$$

### LUBKSB

Forward and back substitution (above).
