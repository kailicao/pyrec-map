## Explanation

**Purpose.** "Model to equal": interpolates the model's variables onto an equally spaced grid in radius, at the grid points and at the midpoints between them, for [[microdiff.f#MICRODIFF|MICRODIFF]].

**How it fits.**
- **Inputs:** from [[microdiff_setup.f#MICRODIFF_SETUP|MICRODIFF_SETUP]]: the radii `HRU` (units of $R_\odot$), `IBEGIN`, `IEND`, and the density `ODEN` and temperature `OTEM`; and the composition `HCOMP`, `HQPR`, `HS1` and $\nabla$ (`SDEL(2,·)` in `SCRTCH_MOD`).
- **Who calls it:** only `MICRODIFF`.
- **What it calls:** [[interp.f#INTERP|INTERP]], for the four-point Lagrange weights.
- **Outputs:** `NPT`, `DR`, and on the grid points (`E…`) and midpoints (`E…_H`): the mass $m$, $\rho$, $T$, $d\ln P/dr$, $\nabla$, $X$, $Y$, $Z$ and the light elements; these go to [[microdiff_run.f#MICRODIFF_RUN|MICRODIFF_RUN]]. The radius, mass and $d\ln P/dr$ are in the Bahcall–Loeb units of `MICRODIFF_SETUP`; $\rho$ and $T$ are in cgs units (g cm⁻³, K).
- **Modules:** `SCRTCH_MOD` (read: `SDEL`), `NMLPAR_MOD` (`LDIFLI`), `DIMENSIONS_MOD` (`JSON`).

**The method.**
1. **Spacing.** $\Delta r_\mathrm{min}$ is the smallest model spacing among the 20 points below `IEND` (the base of the surface convection zone). The number of points is
$$N = \left\lceil \frac{r_\mathrm{end} - r_\mathrm{begin}}{\Delta r_\mathrm{min}} \right\rceil,\quad N \ge 4,\quad N \le 5000\ (\mathrm{JSON}),\qquad \Delta r = \frac{r_\mathrm{end} - r_\mathrm{begin}}{N-1}.$$

    > **Question** ([[#L56-L60]]). **Where the spacing is measured.** $\Delta r_\mathrm{min}$ is measured only over the 20 points below the surface convection zone ("ID THE MINIMUM SPACING IN THE 20 LAYERS BELOW THE SURFACE CZ"). Deeper regions with finer model spacing are then under-resolved. Is this intended?

    > **Question** ([[#L61-L64]]; [[#L83]]). **The grid is coarser than the comment says.** The comment asks for "the minimum number of equally spaced grid points such that DR <= DRMIN", but `NPT` $=\lceil \Delta r_\mathrm{tot}/\Delta r_\mathrm{min}\rceil$ points make `NPT-1` intervals, so `DR` $= \Delta r_\mathrm{tot}/(N-1)$ is larger than $\Delta r_\mathrm{min}$ (up to 4/3 as large, when $N = 4$). Should `NPT` be one more?

2. **Midpoints.** $r_{i+1/2} = r_\mathrm{begin} + (i - \tfrac12)\Delta r$ for $i = 1,\dots,N-1$. The first is found by linear interpolation; the others by four-point Lagrange interpolation over the four model points around them, $f(r) = \sum_{k=1}^{4} w_k(r)\, f_{k_0+k-1}$. Two pieces of code here cannot run: the branch for `NPT = 2` ([[#L87-L88]]), since `NPT` is at least 4, and the debugging line `IF(I-1 .EQ. 0) PRINT*, 'mte line 47'` ([[#L91]]) inside `DO 10 I = 2,NPT-1` (unused?).
3. **Grid points.** $r_i = r_\mathrm{begin} + (i-1)\Delta r$. The first and last take the model's values at `IBEGIN` and `IEND`; the others use the same four-point interpolation.

    > **Question** ([[#L164-L177]]; [[#L256-L267]]). **Interpolated composition.** Four-point Lagrange interpolation of $X$, $Y$, $Z$ near steep gradients can overshoot (negative or above one). [[microdiff_cod.f#MICRODIFF_COD|MICRODIFF_COD]] floors the mass fractions at $10^{-24}$ for its coefficients ([[microdiff_cod.f#L83-L85]]), and [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] maps back only the changes, which limits the harm. Is an overshoot guarded anywhere else, or does it need to be?

**Changed since `rp_1`.** The cap on `NPT` is now `JSON` itself (the same 5000) rather than a repeated literal; the authors' comment says the name `HALFJSON` is presumably left from an earlier cap of `JSON/2`, which settles the former question 3; COMMON blocks to modules (the unused `/GRAVS3/` is gone), `IMPLICIT NONE`.

**Changed since `a8a5950`.** The grid has at least 4 points, not 2, since the 4-point Lagrange stencils here and in [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] read `ER(K0..K0+3)`, and a 2- or 3-point grid read points never set, or `ER(-1)` and `ER(0)`.

## Bugs, by priority

1. **(a)** **The first midpoint can be interpolated from the wrong model points.** ([[#L100-L113]]) The search for the model point above the first midpoint runs over `IU = 2..NPT`: model indices from 2, bounded by the number of *equal-grid* points, rather than `IBEGIN+1..IEND`. The model point needed lies above `IBEGIN`; when `NPT` is smaller than its index (a large `IBEGIN`, such as a convective core with many points, and a coarse equal grid), the loop ends, `IU` falls back to `NPT`, and the "interpolation" extrapolates from points `NPT-1` and `NPT`, far inside the core. What follows: wrong values at the first midpoint (`EM_H(1)`, `EDEN_H(1)`, `ETEM_H(1)`, `EHQPR_H(1)`, `EDELR_H(1)` and the abundances), which [[microdiff_run.f#MICRODIFF_RUN|MICRODIFF_RUN]] uses in its first cell ([[microdiff_run.f#L146]]). The older settling path has the same search ([[model_to_equal.f#b1]]). Only with `LNEWDIF` and `LDIFY`, `LDIFZ` or `LDIFLI` (all off by default; the test suite's settling decks set them), and only when `NPT` is that small; how often a run reaches it was not traced. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to search the model points from IBEGIN+1 to IEND, so
    C that the first midpoint lies between the two points used.
          DO 15 IU=IBEGIN+1,IEND
             IF(HRU(IU).GE.ER_H(1))GOTO 17
       15 CONTINUE
          IU=IEND
       17 CONTINUE
    ```
