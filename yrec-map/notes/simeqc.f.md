## Explanation

**Purpose.** Solves a small linear system by Gaussian elimination with partial pivoting, in place.

**How it fits.** Its only caller is [[kemcom.f#KEMCOM|`KEMCOM`]], which calls `SIMEQC(A,8,7)`: 7 equations, with the matrix and one right-hand side stored together by columns in `A(56)` (7 × 8). The solution overwrites the last column. No COMMON blocks.

**The method.** For each column $j$, the row with the largest $|a_{ij}|$ ($i \ge j$) becomes the pivot row; it is swapped in and divided by the pivot, and the column is eliminated below. Back substitution then gives the solution in the right-hand-side column. A zero pivot (a singular matrix) stops the run with "STOPPED AT 1010" and the code 29. In general, `N` is the number of equations and `M` − `N` the number of right-hand sides; the array size 56 fixes `M`·`N` ≤ 56.

**Design.** The index arithmetic on a one-dimensional array, without comments, follows the style of old library routines (it resembles IBM's SSP `SIMQ`; our inference).

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

## Questions for the experts

1. **The error message goes to unit 5.** `WRITE (5,1011)` writes to unit 5, normally standard input. Should it be `ISHORT` or `*`?
2. **Exact zero only.** The pivot test is `DABS(BIGA).EQ.0.0D0`, so a nearly singular system passes and may give a meaningless solution. Has this been an issue in `KEMCOM`?
