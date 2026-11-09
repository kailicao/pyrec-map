## Explanation

**Purpose.** This file does the extrapolation step of [[bursmix.f#BURSMIX|BURSMIX]]: burning and rotational mixing are done in turn over $n$ substeps of one time step, for increasing $n$, and this routine extrapolates the resulting abundances to zero substep size (the Bulirsch–Stoer idea, "MHP 6/00"). It also decides when the extrapolation has converged.

**How it fits.**
- **Inputs:** the arguments `DELTS` (the time step), `HCOMP` (the abundances after the latest sequence), `IEST` (which sequence: 1, 2, …), `M` (number of shells), `JBEG`, `NSPEC` (the range of species), `NSEQ` (the numbers of substeps).
- **Who calls it:** only [[bursmix.f#BURSMIX|BURSMIX]], once per sequence; at 7be4133 BURSMIX itself is never called, since GETW's `LBURS` is always false ([[getw.f#L140]]): unused?
- **Outputs:** `LCONV`; when converged, the extrapolated abundances in `HCOMP`. The tableau (`HCOMPI`, `HCOMPA`, `HCOMPE`) is a local array kept between calls by `SAVE` (it was the COMMON block `/BSBURN/`, used by no other routine); the maximum number of shells `JSON` comes from [[dimensions_mod.f|DIMENSIONS_MOD]].

**The method.**
1. **First call (`IEST = 1`):** find which species are present anywhere (abundance $> 10^{-14}$), and at which shells $^3$He and the four CNO species are present ($> 10^{-24}$).
2. **Variables extrapolated.** Most species directly; $^3$He as $\ln X_3$; and, where C, N, O are all present, the CNO species replaced by
$$v_5 = \frac{X_{13}}{X_{12}}, \quad v_6 = \frac{X_{14}}{X_{12}}, \quad v_7 = \frac{X_{16}}{X_{14}}, \quad v_9 = \frac{X_{12}}{12} + \frac{X_{13}}{13} + \frac{X_{14}}{14} + \frac{X_{16}}{16},$$
which the comment calls the "alternate method": ratios and the total number of CNO nuclei per gram (in units of the atomic mass unit).
3. **Polynomial extrapolation** in $h^2$, with $h_k = \Delta t / n_k$: the results $A(h_k^2)$ are extrapolated to $h^2 = 0$ by Neville's scheme, as in Numerical Recipes' `PZEXTR`. At each new sequence $k$, with $x_k = h_k^2$, for $j = 1, \dots, k-1$:
$$\delta = \frac{d - c_j}{x_{k-j} - x_k}, \qquad e \leftarrow x_k\,\delta, \qquad d \leftarrow x_{k-j}\,\delta, \qquad A \leftarrow A + e,$$
where $c_j$ are the stored differences (`HCOMPI`) and $e$ the last correction (`HCOMPE`, the error vector that the comment calls `DCOMPA`, [[#L79-L80]]). Before each update, $c_j$ is replaced by the previous correction (`HCOMPI(K1) = HCOMPE`), as in Neville's scheme ([[#L184-L199]]).
4. **Convergence:** the largest relative correction $|e/A|$ over all variables with $A > 10^{-12}$; converged if it is below $10^{-3}$ ([[#L207-L226]]). Each call prints the error and where it is. Since $\ln X_3 < 0$, $^3$He never enters this test (suspected bug 1).

    > **Question** ([[#L226]]). **The tolerance.** The relative tolerance $10^{-3}$ is hard-coded, while [[bsstep.f#BSSTEP|BSSTEP]] gets its own as the argument `EPS`, which ENVINT takes from `STOLR0` in [[intpar_mod.f|INTPAR_MOD]]. Should BSROTMIX's be an input too?

5. **Back-transform:** $X_3 = e^{A_4}$, and
$$X_{12} = \frac{v_9}{\frac{1}{12} + \frac{v_5}{13} + \frac{v_6}{14} + \frac{v_6 v_7}{16}}, \quad X_{13} = v_5 X_{12}, \quad X_{14} = v_6 X_{12}, \quad X_{16} = v_7 X_{14};$$
abundances below $10^{-24}$ are set to 0.

**Design.** The routine prints a line to the screen at every call after the first. The bookkeeping in step 1 is done only at `IEST = 1` and kept with `SAVE`.

**Changed since `rp_1`.** Declarations only: `/BSBURN/` to local saved arrays, `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Bugs, by priority

1. **(c)** **$^3$He is left out of the convergence test.** ([[#L88-L96]]; [[#L213-L220]]) $^3$He is extrapolated as $\ln X_3$ wherever $X_3 > 10^{-24}$, and $\ln X_3$ is negative, so the test `HCOMPA(J,I).GT.1.0D-12` skips it at every such shell; elsewhere $X_3 \le 10^{-24}$ fails the test too. The extrapolation can then be declared converged while $^3$He has not converged. Not reached at 7be4133, since BURSMIX is never called ([[getw.f#L140]]). Read from the code, not run. **A possible fix** (the correction of $\ln X_3$ is itself the relative correction of $X_3$):

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to test HE3 by its correction in LN(X3), the relative
    C correction of X3; LN(X3) is negative and never passed the test.
                   IF(J.EQ.4 .AND. LHE3(I))THEN
                      Q = HCOMPE(J,I)
                   ELSE IF(HCOMPA(J,I).GT.1.0D-12)THEN
                      Q = HCOMPE(J,I)/HCOMPA(J,I)
                   ELSE
                      Q = 0.0D0
                   ENDIF
                   IF(ABS(Q).GT.ERRMAX)THEN
                      IMAX = I
                      JMAX = J
                      ERRMAX=ABS(Q)
                   ENDIF
    ```

2. **(b)** **`STOP999` when no species is present.** ([[#L76-L77]]) If no species from `JBEG` to `NSPEC` exceeds $10^{-14}$ anywhere, the run stops, with no message. Such a composition (no $^3$He and no metals) is unusual but not invalid, and with nothing to extrapolate the routine could go on: With `NMAX` = 0, the next call finds `ERRMAX` = $10^{-30}$ and reports convergence. Not reached at 7be4133, since BURSMIX is never called. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to go on with nothing to extrapolate (NMAX = 0); the
    C next call then reports convergence at once.  It stopped the run.
    C        IF(NMAX.LT.1)STOP999
    ```

### BSROTMIX

Polynomial (Richardson) extrapolation to zero substep of the abundances from successive burn–mix sequences, with $^3$He in logarithm and CNO as ratios plus a total; sets `LCONV` when the relative correction is below $10^{-3}$.
