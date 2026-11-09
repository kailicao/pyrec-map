## Explanation

**Purpose.** Interpolation by a shape-preserving osculatory quadratic spline, from ACM Algorithm 574 (D. F. McAllister and J. A. Roulier, ACM Transactions on Mathematical Software, September 1981), as the header says. It interpolates the table `(XTAB, YTAB)` of `N` points to the `K` abscissas `XVAL`, and returns the values in `YVAL`.

**How it fits.**
- **Who calls it:** the routines that move quantities between the model grid and an equally spaced grid: [[mixcom.f#MIXCOM|MIXCOM]], [[mixgrid.f#MIXGRID|MIXGRID]], [[rotgrid.f#ROTGRID|ROTGRID]], [[getgrid.f#GETGRID|GETGRID]], [[eq2mod.f#EQ2MOD|EQ2MOD]] and [[hpoint.f#HPOINT|HPOINT]].
- **What it calls:** [[slopes.f#SLOPES|SLOPES]] (the derivatives $m_i$ at the data points) and [[meval.f#MEVAL|MEVAL]] (the evaluation; `EPS` $=10^{-4}$ is a relative error tolerance passed on to MEVAL's internal routine `CHOOSE`).

**The method.** The spline is made of quadratic pieces, with one or two knots added between data points where needed (`CASES`, `CHOOSE`), matches the values and the slopes $m_i$ at the data, and preserves the data's monotonicity and convexity wherever the data allow (hence "shape-preserving"); the details are in `SLOPES` and `MEVAL`. That is why it is used to move the diffusion coefficients, $\Omega$ and the abundances between grids: it does not overshoot, so regridding creates no new extrema, negative coefficients or negative abundances. The arrays are dimensioned `JSON` (from `DIMENSIONS_MOD`), the model's maximum number of shells.

**Changed since `rp_1`.** Declarations only: `JSON` from `DIMENSIONS_MOD` instead of a local `PARAMETER`, `IMPLICIT NONE`.

## Bugs, by priority

1. **(d)** **MEVAL's error code is ignored.** ([[#L47]]; [[meval.f#L93-L98]]) `MEVAL` returns `ERR` = 2 when `XVAL` is not nondecreasing, and then returns without setting `YVAL`; `ERR` = 1 marks extrapolation, which is expected. `OSPLIN` does not check `ERR`, so with points of evaluation out of order the caller gets whatever `YVAL` held, without a message. Correct while every caller passes ordered points (the new mass grid, the equally spaced grids), which was not traced for each of the six callers. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to stop the run when MEVAL finds the points of
    C evaluation out of order, since YVAL is then left unset.
          USE IOUNITS_MOD
    ...
          CALL MEVAL(XVAL,YVAL,XTAB,YTAB,M,N,K,EPS,ERR)
          IF (ERR .EQ. 2) THEN
             WRITE(*,900) K
             WRITE(ISHORT,900) K
     900     FORMAT(' OSPLIN: POINTS OF EVALUATION NOT IN ORDER, K',I6/
         *          ' RUN STOPPED')
             STOP 1
          ENDIF
    ```
