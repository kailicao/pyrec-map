## Explanation

**Purpose.** This file does the extrapolation step of [[bursmix.f#BURSMIX|BURSMIX]]: burning and rotational mixing are done in turn over $n$ substeps of one time step, for increasing $n$, and this routine extrapolates the resulting abundances to zero substep size (the Bulirsch–Stoer idea, "MHP 6/00"). It also decides when the extrapolation has converged.

**How it fits.**
- **Inputs:** the arguments `DELTS` (the time step), `HCOMP` (the abundances after the latest sequence), `IEST` (which sequence: 1, 2, …), `M` (number of shells), `JBEG`, `NSPEC` (the range of species), `NSEQ` (the numbers of substeps).
- **Who calls it:** only [[bursmix.f#BURSMIX|BURSMIX]], once per sequence.
- **Outputs:** `LCONV`; when converged, the extrapolated abundances in `HCOMP`. The tableau (`HCOMPI`, `HCOMPA`, `HCOMPE`) is a local array kept between calls by `SAVE` (it was the COMMON block `/BSBURN/`, used by no other routine); the maximum number of shells `JSON` comes from [[dimensions_mod.f|DIMENSIONS_MOD]].

**The method.**
1. **First call (`IEST = 1`):** find which species are present anywhere (abundance $> 10^{-14}$), and at which shells $^3$He and the four CNO species are present ($> 10^{-24}$).
2. **Variables extrapolated.** Most species directly; $^3$He as $\ln X_3$; and, where C, N, O are all present, the CNO species replaced by
$$v_5 = \frac{X_{13}}{X_{12}}, \quad v_6 = \frac{X_{14}}{X_{12}}, \quad v_7 = \frac{X_{16}}{X_{14}}, \quad v_9 = \frac{X_{12}}{12} + \frac{X_{13}}{13} + \frac{X_{14}}{14} + \frac{X_{16}}{16},$$
which the comment calls the "alternate method": ratios and the total number of CNO nuclei per gram (in units of the atomic mass unit).
3. **Polynomial extrapolation** in $h^2$, with $h_k = \Delta t / n_k$: the results $A(h_k^2)$ are extrapolated to $h^2 = 0$ by Neville's scheme, as in Numerical Recipes' `PZEXTR`. At each new sequence $k$, with $x_k = h_k^2$, for $j = 1, \dots, k-1$:
$$\delta = \frac{d - c_j}{x_{k-j} - x_k}, \qquad e \leftarrow x_k\,\delta, \qquad d \leftarrow x_{k-j}\,\delta, \qquad A \leftarrow A + e,$$
where $c_j$ are the stored differences (`HCOMPI`) and $e$ the last correction (`HCOMPE`). Before each update, $c_j$ is replaced by the previous correction (`HCOMPI(K1) = HCOMPE`), as in Neville's scheme.
4. **Convergence:** the largest relative correction $|e/A|$ over all variables with $A > 10^{-12}$; converged if it is below $10^{-3}$. Each call prints the error and where it is.
5. **Back-transform:** $X_3 = e^{A_4}$, and
$$X_{12} = \frac{v_9}{\frac{1}{12} + \frac{v_5}{13} + \frac{v_6}{14} + \frac{v_6 v_7}{16}}, \quad X_{13} = v_5 X_{12}, \quad X_{14} = v_6 X_{12}, \quad X_{16} = v_7 X_{14};$$
abundances below $10^{-24}$ are set to 0.

**Design.** The routine prints a line to the screen at every call after the first. The bookkeeping in step 1 is done only at `IEST = 1` and kept with `SAVE`.

**Changed since `rp_1`.** Declarations only: `/BSBURN/` to local saved arrays, `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Questions for the experts

1. **$^3$He left out of the test.** $\ln X_3$ is negative, so the test `HCOMPA(J,I).GT.1.0D-12` excludes $^3$He from the convergence check. Likewise, the ratio variables are tested on their own size. Is that intended?
2. **The tolerance.** The relative tolerance $10^{-3}$ is hard-coded, while [[bsstep.f#BSSTEP|BSSTEP]] gets its own as the argument `EPS`, which ENVINT takes from `STOLR0` in [[intpar_mod.f|INTPAR_MOD]]. Should BSROTMIX's be an input too?
3. **Comment.** The comment above the first loop speaks of an error vector `DCOMPA`; the code uses `HCOMPE`.
4. **`STOP999` on no species.** If no species from `JBEG` to `NSPEC` is present, the run stops without a message.

### BSROTMIX

Polynomial (Richardson) extrapolation to zero substep of the abundances from successive burn–mix sequences, with $^3$He in logarithm and CNO as ratios plus a total; sets `LCONV` when the relative correction is below $10^{-3}$.
