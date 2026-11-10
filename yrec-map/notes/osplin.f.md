## Explanation

**Purpose.** Interpolation by a shape-preserving osculatory quadratic spline, from ACM Algorithm 574 (D. F. McAllister and J. A. Roulier, ACM Transactions on Mathematical Software, September 1981), as the header says. It interpolates the table `(XTAB, YTAB)` of `N` points to the `K` abscissas `XVAL`, and returns the values in `YVAL`.

**How it fits.**
- **Who calls it:** the routines that move quantities between the model grid and an equally spaced grid: [[mixcom.f#MIXCOM|MIXCOM]], [[mixgrid.f#MIXGRID|MIXGRID]], [[rotgrid.f#ROTGRID|ROTGRID]], [[getgrid.f#GETGRID|GETGRID]], [[eq2mod.f#EQ2MOD|EQ2MOD]] and [[hpoint.f#HPOINT|HPOINT]].
- **What it calls:** [[slopes.f#SLOPES|SLOPES]] (the derivatives $m_i$ at the data points) and [[meval.f#MEVAL|MEVAL]] (the evaluation; `EPS` $=10^{-4}$ is a relative error tolerance passed on to MEVAL's internal routine `CHOOSE`).

**The method.** The spline is made of quadratic pieces, with one or two knots added between data points where needed (`CASES`, `CHOOSE`), matches the values and the slopes $m_i$ at the data, and preserves the data's monotonicity and convexity wherever the data allow (hence "shape-preserving"); the details are in `SLOPES` and `MEVAL`. That is why it is used to move the diffusion coefficients, $\Omega$ and the abundances between grids: it does not overshoot, so regridding creates no new extrema, negative coefficients or negative abundances. The arrays are dimensioned `JSON` (from `DIMENSIONS_MOD`), the model's maximum number of shells.

**Changed since `rp_1`.** Declarations only: `JSON` from `DIMENSIONS_MOD` instead of a local `PARAMETER`, `IMPLICIT NONE`.

## Bugs, by priority

1. **(never occurred)** **MEVAL's error code is ignored.** ([[#L47]]; [[meval.f#L93-L98]]) `MEVAL` returns `ERR` = 2 when `XVAL` is not nondecreasing, and then returns without setting `YVAL`; `ERR` = 1 marks extrapolation, which is expected. `OSPLIN` does not check `ERR`, so with points of evaluation out of order the caller gets whatever `YVAL` held, without a message. Correct while every caller passes ordered points (the new mass grid, the equally spaced grids), which was not traced for each of the six callers.

    **A possible fix:**

    ```diff
    --- a/src/osplin.f
    +++ b/src/osplin.f
    @@ -14,6 +14,10 @@
     C code changed to take JSON from DIMENSIONS_MOD instead of declaring
     C PARAMETER(JSON=5000) here.
           USE DIMENSIONS_MOD
    +C 11/09/26 KC via Claude
    +C code changed to stop the run when MEVAL finds the points of
    +C evaluation out of order, since YVAL is then left unset.
    +      USE IOUNITS_MOD
     C 10/20/26 MHP via Claude
     C code changed to replace implicit typing with IMPLICIT NONE.
           IMPLICIT NONE
    @@ -45,6 +49,13 @@
           EPS=1.D-04
     C CALL MEVAL TO EVALUATE THE SPLINE AT THE RUN OF POINTS XVAL.
           CALL MEVAL(XVAL,YVAL,XTAB,YTAB,M,N,K,EPS,ERR)
    +      IF (ERR .EQ. 2) THEN
    +         WRITE(*,900) K
    +         WRITE(ISHORT,900) K
    + 900     FORMAT(' OSPLIN: POINTS OF EVALUATION NOT IN ORDER, K',I6/
    +     *          ' RUN STOPPED')
    +         STOP 1
    +      ENDIF
     
           RETURN
           END
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): OSPLIN ran in 33 of 34 runs (26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones; one of these, with `FCORE` = 1.0, stopped in its first second), from 400 to 342,520 times each, with from 9 to 3455 points; MEVAL never returned `ERR` = 2. Points out of order would reach it; no caller gave them. No fix was run, since the page's fix is a stop. Intent: none found.
