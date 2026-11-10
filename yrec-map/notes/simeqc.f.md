## Explanation

**Purpose.** Solves a small linear system by Gaussian elimination with partial pivoting, in place.

**How it fits.** Its only caller is [[kemcom.f#KEMCOM|`KEMCOM`]], which calls `SIMEQC(A,8,7)`: 7 equations, with the matrix and one right-hand side stored together by columns in `A(56)` (7 × 8). The solution overwrites the last column. No COMMON blocks.

**The method.** For each column $j$, the row with the largest $|a_{ij}|$ ($i \ge j$) becomes the pivot row; it is swapped in and divided by the pivot, and the column is eliminated below. Back substitution then gives the solution in the right-hand-side column. A zero pivot (a singular matrix) stops the run with "STOPPED AT 1010" and the code 29 ([[#L29-L33]]; the message goes to unit 5: [[simeqc.f#b1]]). In general, `N` is the number of equations and `M` − `N` the number of right-hand sides; the array size 56 fixes `M`·`N` ≤ 56.

> **Question** ([[#L25-L29]]). **Exact zero only.** The pivot test is `DABS(BIGA).EQ.0.0D0`, so a nearly singular system passes and may give a meaningless solution. Has this been an issue in `KEMCOM`?

**Design.** The index arithmetic on a one-dimensional array, without comments, follows the style of old library routines (it resembles IBM's SSP `SIMQ`; our inference).

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

## Bugs, by priority

1. **(never occurred)** **The error message goes to unit 5.** ([[#L31-L33]]) `WRITE (5,1011)` writes to unit 5, which YREC never opens: it is the preconnected standard input. What follows: On a singular matrix the message "STOPPED AT 1010" does not reach the terminal or the `.short` file (with gfortran the `WRITE` to the input unit may itself end the run with an I/O error before `STOP 29`; not run). Only when KEMCOM's 7 × 7 system is singular.

    **A possible fix,** in the style of the other error stops (`KNOWN_ISSUES.md`, issue 38):

    ```diff
    --- a/src/simeqc.f
    +++ b/src/simeqc.f
    @@ -4,6 +4,10 @@
     C SIMEQC
     C$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
           SUBROUTINE SIMEQC(A,M,N)
    +C 11/09/26 KC via Claude
    +C code changed to write the message to the terminal and the .short
    +C file instead of unit 5, standard input.
    +      USE IOUNITS_MOD
     C 10/20/26 MHP via Claude
     C code changed to replace implicit typing with IMPLICIT NONE and
     C explicit declarations.
    @@ -28,9 +32,10 @@
        30 CONTINUE
           IF(DABS(BIGA).EQ.0.0D0) GOTO 1010
           GOTO 1012
    - 1010 WRITE (5,1011)
    - 1011 FORMAT (1X,'STOPPED AT 1010')
    -      STOP29
    + 1010 WRITE (*,1011)
    +      WRITE (ISHORT,1011)
    + 1011 FORMAT (1X,'SIMEQC: SINGULAR MATRIX, STOPPED AT 1010')
    +      STOP 29
      1012 IA=J+N*(J-2)
           IT=IMAX-J
           DO 50 K=J,M
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The pivot test ran in 30 of 34 runs (26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones; one of these, with `FCORE` = 1.0, stopped in its first second), from 1,288 to about 94 million times each, and the largest pivot was never below 0.229, so the matrix was never singular and the message never written. A singular system would reach it; none was run. No fix was run, since the page's fix only moves a message. Intent: none found.
