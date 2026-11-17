## Explanation

**Purpose.** This file solves a banded linear system $`A\,\mathbf{x} = \mathbf{b}`$ by Gaussian elimination without pivoting. It is the solver for the implicit angular-momentum transport in [DADCOEFT](dadcoeft.f.md#dadcoeft) (its comments speak of $`\Omega`$ and its radial derivatives).

**How it fits.**
- **Inputs:** the arguments `A(NMAX,10)` (the band), `NM` (the number of unknowns) and `B` (the right-hand side).
- **Who calls it:** only [DADCOEFT](dadcoeft.f.md#dadcoeft).
- **Output:** the solution, returned in `B`; `A` is overwritten.
- No COMMON blocks.

**Storage.** Row $`i`$ of the matrix is stored in `A(i,1:10)`, with the diagonal in column 5: `A(i,5+k)` is the coefficient of unknown $`x_{i+k}`$, for $`k = -4, \dots, 5`$. The band thus has 4 subdiagonals and 5 superdiagonals. `A` is declared `A(NMAX,10)` with `NMAX` = 8000 ([line 9](https://github.com/yreclab/yrec/blob/7be4133/src/bandw.f#L9); [line 12](https://github.com/yreclab/yrec/blob/7be4133/src/bandw.f#L12)), and DADCOEFT declares the same ([dadcoeft.f, line 39](https://github.com/yreclab/yrec/blob/7be4133/src/dadcoeft.f#L39); [dadcoeft.f, line 92](https://github.com/yreclab/yrec/blob/7be4133/src/dadcoeft.f#L92)); the two must agree, since the first dimension sets where each column starts. `KNOWN_ISSUES.md` (lines 1845–1848) keeps `NMAX` per routine on purpose.

**The method.**
1. **Forward elimination**, row by row: divide row $`i`$ and $`b_i`$ by the pivot $`a_{ii}`$, then remove $`x_i`$ from the next 4 rows,
   
   $$\displaystyle a\_{jk} \leftarrow a\_{jk} - a\_{ji}\\,a\_{ik}, \qquad b\_j \leftarrow b\_j - a\_{ji}\\,b\_i, \qquad j = i+1, \dots, i+4.$$
   
   The last 4 rows are handled separately, since their bands are cut off by the end of the matrix. A pivot smaller than $`10^{-20}`$ in absolute value stops the run (`STOP 999`), after printing the row (for the last row it stops without printing).
2. **Back substitution:** with unit diagonal, for $`i = N, \dots, 2`$,
   
   $$\displaystyle b\_{i-l} \leftarrow b\_{i-l} - b\_i\\,a\_{i-l,\\,i}, \qquad l = 1, \dots, \min(5, i-1).$$

**Design.** No pivoting: the method relies on the matrix being diagonally dominant enough.

> **Question** ([lines 29–32](https://github.com/yreclab/yrec/blob/7be4133/src/bandw.f#L29-L32); [lines 52–55](https://github.com/yreclab/yrec/blob/7be4133/src/bandw.f#L52-L55); [line 75](https://github.com/yreclab/yrec/blob/7be4133/src/bandw.f#L75)). **No pivoting.** Is the system from DADCOEFT always diagonally dominant? A small pivot stops the whole run rather than trying a pivoted solve.

About 100 lines of an earlier version (blocks of 4 rows per shell, "DIAGONALIZE OMEGA(II) TERM") remain as comments.

> **Question** ([lines 16–27](https://github.com/yreclab/yrec/blob/7be4133/src/bandw.f#L16-L27); [lines 81–152](https://github.com/yreclab/yrec/blob/7be4133/src/bandw.f#L81-L152)). **Dead code.** The commented-out block solver: can it go in the overhaul?

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`, and the unused `JSON` parameter removed, which settled half of a former question on the dimensions (the other half is now in Storage, above).

### BANDW

Gaussian elimination without pivoting for a band matrix with 4 subdiagonals and 5 superdiagonals (diagonal in column 5 of `A`); the solution replaces `B`.
