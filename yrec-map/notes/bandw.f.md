## Explanation

**Purpose.** This file solves a banded linear system $A\,\mathbf{x} = \mathbf{b}$ by Gaussian elimination without pivoting. It is the solver for the implicit angular-momentum transport in [[dadcoeft.f#DADCOEFT|DADCOEFT]] (its comments speak of $\Omega$ and its radial derivatives).

**How it fits.**
- **Inputs:** the arguments `A(NMAX,10)` (the band), `NM` (the number of unknowns) and `B` (the right-hand side).
- **Who calls it:** only [[dadcoeft.f#DADCOEFT|DADCOEFT]].
- **Output:** the solution, returned in `B`; `A` is overwritten.
- No COMMON blocks.

**Storage.** Row $i$ of the matrix is stored in `A(i,1:10)`, with the diagonal in column 5: `A(i,5+k)` is the coefficient of unknown $x_{i+k}$, for $k = -4, \dots, 5$. The band thus has 4 subdiagonals and 5 superdiagonals.

**The method.**
1. **Forward elimination**, row by row: divide row $i$ and $b_i$ by the pivot $a_{ii}$, then remove $x_i$ from the next 4 rows,
$$a_{jk} \leftarrow a_{jk} - a_{ji}\,a_{ik}, \qquad b_j \leftarrow b_j - a_{ji}\,b_i, \qquad j = i+1, \dots, i+4.$$
The last 4 rows are handled separately, since their bands are cut off by the end of the matrix. A pivot smaller than $10^{-20}$ in absolute value stops the run (`STOP 999`), after printing the row (for the last row it stops without printing).
2. **Back substitution:** with unit diagonal, for $i = N, \dots, 2$,
$$b_{i-l} \leftarrow b_{i-l} - b_i\,a_{i-l,\,i}, \qquad l = 1, \dots, \min(5, i-1).$$

**Design.** No pivoting: the method relies on the matrix being diagonally dominant enough. About 100 lines of an earlier version (blocks of 4 rows per shell, "DIAGONALIZE OMEGA(II) TERM") remain as comments.

**KC's changes.** 2025-05-31: the unused arguments `M1`, `M2` removed from the argument list (the old header kept as a comment).

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`, and the unused `JSON` parameter removed, which settles half of question 2.

## Questions for the experts

1. **No pivoting.** Is the system from DADCOEFT always diagonally dominant? A small pivot stops the whole run rather than trying a pivoted solve.
2. **A dimension to keep in step.** `NMAX = 8000` must match the first dimension of `A` in DADCOEFT, which declares the same value.
3. **Dead code.** The commented-out block solver: can it go in the overhaul?

### BANDW

Gaussian elimination without pivoting for a band matrix with 4 subdiagonals and 5 superdiagonals (diagonal in column 5 of `A`); the solution replaces `B`.
