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

    The spacing is then larger than $\Delta r_\mathrm{min}$, against the comment ([[#b2]]).

2. **Midpoints.** $r_{i+1/2} = r_\mathrm{begin} + (i - \tfrac12)\Delta r$ for $i = 1,\dots,N-1$. The first is found by linear interpolation; the others by four-point Lagrange interpolation over the four model points around them, $f(r) = \sum_{k=1}^{4} w_k(r)\, f_{k_0+k-1}$. Two pieces of code here cannot run: the branch for `NPT = 2` ([[#L87-L88]]), since `NPT` is at least 4, and the debugging line `IF(I-1 .EQ. 0) PRINT*, 'mte line 47'` ([[#L91]]) inside `DO 10 I = 2,NPT-1` (unused?).
3. **Grid points.** $r_i = r_\mathrm{begin} + (i-1)\Delta r$. The first and last take the model's values at `IBEGIN` and `IEND`; the others use the same four-point interpolation.

    > **Question** ([[#L164-L177]]; [[#L256-L267]]). **Interpolated composition.** Four-point Lagrange interpolation of $X$, $Y$, $Z$ near steep gradients can overshoot (negative or above one). [[microdiff_cod.f#MICRODIFF_COD|MICRODIFF_COD]] floors the mass fractions at $10^{-24}$ for its coefficients ([[microdiff_cod.f#L83-L85]]), and [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] maps back only the changes, which limits the harm. Is an overshoot guarded anywhere else, or does it need to be?

**Changed since `rp_1`.** The cap on `NPT` is now `JSON` itself (the same 5000) rather than a repeated literal; the authors' comment says the name `HALFJSON` is presumably left from an earlier cap of `JSON/2`, which settles the former question 3; COMMON blocks to modules (the unused `/GRAVS3/` is gone), `IMPLICIT NONE`.

**Changed since `a8a5950`.** The grid has at least 4 points, not 2, since the 4-point Lagrange stencils here and in [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] read `ER(K0..K0+3)`, and a 2- or 3-point grid read points never set, or `ER(-1)` and `ER(0)`.

## Bugs, by priority

1. **(never occurred)** **The first midpoint can be interpolated from the wrong model points.** ([[#L100-L113]]) The search for the model point above the first midpoint runs over `IU = 2..NPT`: model indices from 2, bounded by the number of *equal-grid* points, rather than `IBEGIN+1..IEND`. The model point needed lies above `IBEGIN`; when `NPT` is smaller than its index (a large `IBEGIN`, such as a convective core with many points, and a coarse equal grid), the loop ends, `IU` falls back to `NPT`, and the "interpolation" extrapolates from points `NPT-1` and `NPT`, far inside the core. What follows: wrong values at the first midpoint (`EM_H(1)`, `EDEN_H(1)`, `ETEM_H(1)`, `EHQPR_H(1)`, `EDELR_H(1)` and the abundances), which [[microdiff_run.f#MICRODIFF_RUN|MICRODIFF_RUN]] uses in its first cell ([[microdiff_run.f#L146]]). The older settling path has the same search ([[model_to_equal.f#b1]]). Only with `LNEWDIF` and `LDIFY`, `LDIFZ` or `LDIFLI` (all off by default; the test suite's settling decks set them), and only when `NPT` is that small.

    **A possible fix:**

    ```diff
    --- a/src/microdiff_mte.f
    +++ b/src/microdiff_mte.f
    @@ -97,10 +97,13 @@
     C  AT EQUALLY SPACED ZONE MIDPOINTS.
     C
     C  FIRST POINT : LINEAR INTERPOLATION BETWEEN STARTING POINT AND 2ND PT.
    -      DO 15 IU=2,NPT
    +C 11/09/26 KC via Claude
    +C code changed to search the model points from IBEGIN+1 to IEND, so
    +C that the first midpoint lies between the two points used.
    +      DO 15 IU=IBEGIN+1,IEND
              IF(HRU(IU).GE.ER_H(1))GOTO 17
        15 CONTINUE
    -      IU=NPT
    +      IU=IEND
        17 CONTINUE
           FX=(ER_H(1)-HRU(IU-1))/(HRU(IU)-HRU(IU-1))
           EM_H(1) = HS1(IU-1)+FX*(HS1(IU)-HS1(IU-1))
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The search ran at every settling call in all seven runs with settling (`testsuite/Test_solarGS98_dif`, `testsuite/Test_solarAAG21_dif`, `testsuite/Test_solarM22M_difkur`, `testsuite/Test_solarGS98_difrotmixper18p4d1p0`, `testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`, `testsuite/Test_m1p4feh+0p0GS98_dif_TAMS`, and `testsuite/Test_solarAAG21_dif` with a custom mixture), 690 to 3,703 times per run, with `IBEGIN` up to 536 and `NPT` from 4 to 5,000, and it never failed: The model point above the first midpoint was always found. Not reached: It needs a first point of the settling range beyond `NPT`, a large convective core under few equally spaced points. The fix was not run. Intent: The comment "FIRST POINT : LINEAR INTERPOLATION BETWEEN STARTING POINT AND 2ND PT." ([[#L99]]) names the point above `IBEGIN`, which the search is meant to find.

2. **(harmless in the runs)** **The grid is coarser than the comment says.** ([[#L61-L64]]; [[#L83]]) The comment asks for "the minimum number of equally spaced grid points such that DR <= DRMIN," but `NPT` $=\lceil \Delta r_\mathrm{tot}/\Delta r_\mathrm{min}\rceil$ points make `NPT-1` intervals, so `DR` $= \Delta r_\mathrm{tot}/(N-1)$ is larger than $\Delta r_\mathrm{min}$, by up to the factor $N/(N-1)$ (4/3 when $N = 4$). What follows: The settling is computed on a grid slightly coarser than intended. Only with `LNEWDIF` and `LDIFY`, `LDIFZ`, or `LDIFLI` (all off by default; the test suite's settling decks set them).

    **A possible fix:**

    ```diff
    --- a/src/microdiff_mte.f
    +++ b/src/microdiff_mte.f
    @@ -62,6 +62,10 @@
     C  DR <= DRMIN.
           NPT=INT(DRTOT/DRMIN)
           IF(MOD(DRTOT,DRMIN).NE.0.0D0)NPT=NPT+1
    +C 11/10/26 KC via Claude
    +C code changed to add one point, so that the NPT-1 intervals are no
    +C wider than DRMIN, as the comment above asks.
    +      NPT=NPT+1
     C JVS add additional trap to deal with models with NPT=1
     C 10/30/26 MHP via Claude
     C code changed to require at least 4 points, not 2.  The 4-point
    ```

    **Checked by running YREC** (Nov 10, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): In `testsuite/Test_solarGS98_difrotmixper18p4d1p0` (a rotating solar model with settling, to 4.568 Gyr), the grid was set up 3,702 times, with `NPT` from 35 to 2,061 (never the cap of 5,000), and `DR` exceeded $\Delta r_\mathrm{min}$ every time, by a factor of 1.000 to 1.020. With the fix, `NPT` is 36 to 2,067 and `DR` is 0.975 to 1.000 times $\Delta r_\mathrm{min}$, and the effect stays within the noise: $\log L$ moves by up to 0.00021 dex, against 0.00029 for a null change (nearly every opacity, all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$, times $1 + 10^{-10}$, on the same case); the surface $Y$ by 0.0000061 against 0.0000067, the surface $\log$ Li by 0.00026 dex against 0.00061, and central $Y$ by 0.0000085 against 0.000061; the track has 1,203 models in both. Intent: The comment ([[#L61-L62]]) asks for `DR` no larger than `DRMIN`.
