## Explanation

**Purpose.** Computes the settling coefficients of one species at each point of the equally spaced grid, "in the method of the Thoul routine," for [MICRODIFF_RUN](microdiff_run.f.md#microdiff_run). Its header (G. Somers, 5/15) says it was written for light-element diffusion; it now serves hydrogen and metals too.

**How it fits.**
- **Inputs:** `NPT` points with radius `ER` (units of $`R_\odot`$), density `EDEN` ($`\mathrm{g\,cm^{-3}}`$), temperature `ETEM` ($`\mathrm{K}`$), $`d\ln P/dr`$ (`EHQPR`), $`\nabla`$ (`EDELR`), the three abundances `ESPEC(3,·)`, and the species' weight `THEA`, charge `THEZ` and column `J`.
- **Who calls it:** only `MICRODIFF_RUN`, once on the grid points and once on the midpoints.
- **What it calls:** [THDIFF](thdiff.f.md#thdiff), which solves for the diffusion coefficients of the four-species mixture (H, He, the species, electrons).
- **Outputs:** `ECOD1` and `ECOD2`, and the hydrogen concentration gradient `EDXDR`, written on the hydrogen call ($`J = 1`$) and read on later calls.
- **Modules:** `CONSTANTS_MOD` (`CC13` $`=1/3`$), `NMLPAR_MOD` (the namelist factors `FGRY` and `FGRZ`, set by [PARMIN](https://github.com/yreclab/yrec/blob/7be4133/src/parmin.f#L16-L1489)) and `DIMENSIONS_MOD` (`JSON`).

**The method.** At each point, with mass fractions $`X_k`$ (floored at $`10^{-24}`$), weights $`A_k`$ (1.008, 4.004, `THEA`, $`5.486\times10^{-4}`$) and charges $`Z_k`$ (1, 2, `THEZ`, −1):
1. **Concentrations** relative to electrons: $`c_k = \dfrac{X_k/A_k}{\sum_l Z_l X_l/A_l}`$ for the three ions, $`c_e = 1`$.
2. **Electron and ion densities:** $`n_e = \rho / (m_p \sum_k A_k c_k)`$ with $`m_p = 1.6726\times10^{-24}`$ g, $`n_i = \sum_\mathrm{ions} c_k\, n_e`$.
3. **Lengths:** the inter-ionic distance $`a_0 = (3/(4\pi n_i))^{1/3}`$ (`0.23873` $`= 3/4\pi`$), the Debye length $`\lambda_D = 6.9010\,\sqrt{T/(n_e \sum_k c_k Z_k^2)}`$ cm, and $`\lambda = \max(\lambda_D, a_0)`$.
4. **Coulomb logarithms** for each pair:
   
   $$\displaystyle x\_{kl} = \frac{2.3939\times10^{3}\\, T\\, \lambda}{\|Z\_k Z\_l\|},\qquad \ln\Lambda\_{kl} = 0.81245\\,\ln\\!\left(1 + 0.18769\\, x\_{kl}^{1.2}\right).$$
5. **`THDIFF`** returns the coefficients $`A_P`$ (`TAP`), $`A_T`$ (`TAT`) and $`A_{kl}`$ (`TAC`).
6. **The coefficients.** With $`f = F\, r'^2\, T'^{5/2} / 2.2`$ ($`r'`$ in $`R_\odot`$, $`T'`$ in $`10^7\,\mathrm{K}`$, 2.2 the fixed `LN_LAMBDA`; $`F`$ is `FGRY` on the hydrogen call, $`J = 1`$, `FGRZ` on the third column, $`J = 3`$, and 1 otherwise, the same factors as in [SETUP_GRSETT](https://github.com/yreclab/yrec/blob/7be4133/src/setup_grsett.f#L2-L330); `ER` is already in $`R_\odot`$, so the local `CON_RAD`, [line 75](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_cod.f#L75), is set and never read: unused?):
   
   $$\displaystyle C\_1 = -f\left\[(A\_P + A\_T\nabla)\\,\frac{d\ln P}{dr} + A\_{j1}\\,\frac{d\ln c\_H}{dr}\right\] X\_j ,\qquad C\_2 = -f\\,A\_{jj}.$$
   
   The comment writes the velocity as $`A_P\, d\ln P/dr + A_T\, d\ln T/dr + A_X\, d\ln X/dr + A_D\, d\ln D/dr`$; here $`d\ln T/dr = \nabla\, d\ln P/dr`$. The hydrogen term is dropped on the hydrogen call (it is the same as the last term) and is zero at the first and last points; $`d\ln c_H/dr`$ is a centred difference.

    **The two Coulomb logarithms cancel.** Pairwise Coulomb logarithms go into `THDIFF`, but the coefficient is also divided by a fixed $`\ln\Lambda`$ = `LN_LAMBDA` = 2.2 ([line 74](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_cod.f#L74); [lines 148–154](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_cod.f#L148-L154)), and the time unit in [MICRODIFF_SETUP](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_setup.f#L4-L169), `CON_TIME` = $`2.7 \times 10^{13}`$ yr, "INCLUDES FACTOR OF 2.2 FROM LN LAMBDA" ([microdiff_setup.f, lines 147–148](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_setup.f#L147-L148)), so the two factors of 2.2 cancel exactly, and the net unit, $`5.94 \times 10^{13}`$ yr, is within 1% of Thoul et al.'s $`6 \times 10^{13}`$ yr; whether that unit itself assumes $`\ln\Lambda = 2.2`$ the code does not show. ([`THDIFF`'s page](thdiff.f.md#thdiff) raises the same point from its side.)

    > **Question** ([lines 152–154](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_cod.f#L152-L154); [microdiff.f, lines 187–188](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff.f#L187-L188); [microdiff.f, lines 213–215](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff.f#L213-L215)). **`FGRZ` for light elements.** `FGRZ` scales every call with $`J = 3`$, which [MICRODIFF](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff.f#L4-L245) uses both for the metals (`LDIFZ`) and for each light element (`LDIFLI`), so a factor named for metals also scales lithium, beryllium, and boron settling; in [SETUP_GRSETT](https://github.com/yreclab/yrec/blob/7be4133/src/setup_grsett.f#L2-L330) it scales the metals only. Is this intended? The documentation's "metal-settling" (`docs/source/namelist_physics.md`, line 32) does not settle it, since in astronomical usage the metals include lithium and beryllium, and SETUP_GRSETT diffuses no light elements to compare with; the intent of the change that added `FGRY` and `FGRZ` (JvS 01/26, [lines 145–146](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_cod.f#L145-L146)) would settle it, and with the default `FGRZ` = 1 ([nmlpar_mod.f, line 80](https://github.com/yreclab/yrec/blob/7be4133/src/nmlpar_mod.f#L80)) no run is affected.

**Changed since `rp_1`.** The settling coefficients are now scaled by `FGRY` (hydrogen) and `FGRZ` (the third column), as in the older settling routines (JvS, 01/26); `LN_LAMBDA` is now the double-precision `2.2D0`; COMMON blocks to modules, `IMPLICIT NONE`; the unused `/SCRTCH/` and `/THEAGE/` are gone and `/GRAVS3/`'s factors are now used, which settles the former question 4 (declared but unused blocks).

## Bugs, by priority

1. **(cannot be reached)** **Without hydrogen settling, the hydrogen gradient is never computed.** ([line 96](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_cod.f#L96); [lines 191–212](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_cod.f#L191-L212)) The gradient $`d\ln c_H/dr`$ (`EDXDR`, and `EDXDR_H` on the midpoint call) is computed and stored only on the hydrogen call ($`J = 1`$); later calls read it back. When `LDIFY` is false, [MICRODIFF](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff.f#L4-L245) makes no hydrogen call ([microdiff.f, line 157](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff.f#L157)), so its `SAVE`d arrays `EDXDR` and `EDXDR_H` are never set (zero in practice, though the standard does not promise it), and the term $`A_{j1}\,d\ln c_H/dr`$ silently drops out of the settling of metals and light elements. What follows: where $`X`$ varies (the burned core, the base of the convective envelope), metals and light elements settle without the hydrogen-gradient term of Thoul et al. ([1994](https://ui.adsabs.harvard.edu/abs/1994ApJ...421..828T)). Only with `LNEWDIF` and `LDIFZ` or `LDIFLI` but not `LDIFY` (all off by default; the test suite's settling decks set all three, so they do not take this path).

    **A possible fix:**

    ```diff
    --- a/src/microdiff_cod.f
    +++ b/src/microdiff_cod.f
    @@ -93,7 +93,10 @@
              ENDDO
              CONCEN(NSPEC)=1.D0
     c        save the hydrogen concentration when X is diffused.
    -         IF(J.EQ.1) HYDCON(I) = CONCEN(1)
    +C 11/09/26 KC via Claude
    +C code changed to compute the hydrogen gradient on every call when
    +C hydrogen does not settle, so that EDXDR is always set.
    +         IF(J.EQ.1.OR..NOT.LDIFY) HYDCON(I) = CONCEN(1)
     c        now check whether the Thoul routine must be run. if not,
     c        write COD1 = COD2 = 0. If its the first shell in the depleted
     C        zone, permit the calculations so that AD is correct.
    @@ -188,7 +191,7 @@
     C        only calculate the gradient on the hydrogen call.
     C        set the gradient at first and last points to 0.
     c
    -         IF(J.EQ.1)THEN
    +         IF(J.EQ.1.OR..NOT.LDIFY)THEN
                 DLNCDR = 1.0
                 IF (I.EQ.1) THEN
                    DLNCDR = 0.0
    @@ -205,7 +208,7 @@
                 ENDIF
                 EDXDR(I) = DLNCDR
     c           zero out gradient for hydrogen abundance, as stated above.
    -            DLNCDR = 0.0
    +            IF(J.EQ.1) DLNCDR = 0.0
              ELSE
     c           if not the hydrogen call, retrieve the gradient
                 DLNCDR = EDXDR(I)
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The lines that read the stored gradient on a later call ran in all seven runs with settling (`testsuite/Test_solarGS98_dif`, `testsuite/Test_solarAAG21_dif`, `testsuite/Test_solarM22M_difkur`, `testsuite/Test_solarGS98_difrotmixper18p4d1p0`, `testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`, `testsuite/Test_m1p4feh+0p0GS98_dif_TAMS`, and `testsuite/Test_solarAAG21_dif` with a custom mixture), 5,520 to 29,624 times per run, and `LDIFY` was true every time, so the hydrogen call had always run first. It cannot be reached at 7be4133: `LDIFZ` and `LDIFLI` both force `LDIFY` on ([parmin.f, lines 1239–1250](https://github.com/yreclab/yrec/blob/7be4133/src/parmin.f#L1239-L1250)), and `MIX` and `ROTMIX` call `MICRODIFF` only while `LDIFY` is true, switching settling off for the rest of the run once central $`X`$ falls below `XMIN` ([mix.f, lines 412–416](https://github.com/yreclab/yrec/blob/7be4133/src/mix.f#L412-L416); [rotmix.f, lines 151–155](https://github.com/yreclab/yrec/blob/7be4133/src/rotmix.f#L151-L155)). What remains is fragile code, which relies on the order of the calls in `MICRODIFF`. Intent: "only calculate the gradient on the hydrogen call." ([line 188](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_cod.f#L188)), which assumes that call is always made.

2. **(harmless in the runs)** **Skipped points keep old terms.** ([lines 100–105](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_cod.f#L100-L105); [lines 163–174](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_cod.f#L163-L174)) Where the species' abundance is exactly zero at a point and the next, only `ADS(I)` is set to zero; `FACS`, `APS`, `ATS` and `AHS` keep values from an earlier point or call (`SAVE`). Correct today: $`X_j = 0`$ makes $`C_1`$ zero, and `ADS(I)` = 0 makes $`C_2`$ zero; but a stale value that is not finite would give $`0\times\infty`$, and any change that reads these terms elsewhere would read stale values.

    **A possible fix:**

    ```diff
    --- a/src/microdiff_cod.f
    +++ b/src/microdiff_cod.f
    @@ -98,7 +98,14 @@
     c        write COD1 = COD2 = 0. If its the first shell in the depleted
     C        zone, permit the calculations so that AD is correct.
              IF(ESPEC(J,I).EQ.0.0.AND.I.NE.NPT)THEN
    +C 11/09/26 KC via Claude
    +C code changed to zero all the stored terms of a skipped point, not
    +C only ADS.
                 IF(ESPEC(J,I+1).EQ.0.0)THEN
    +               FACS(I) = 0.0D0
    +               APS(I) = 0.0D0
    +               ATS(I) = 0.0D0
    +               AHS(I) = 0.0D0
                    ADS(I) = 0.0
                    GOTO 5
                 ENDIF
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Points were skipped in all seven runs with settling (six of the test suite's and a made-up one with a custom mixture, listed in [suspected bug 1](#b1)), up to 21.9 million times per run (`testsuite/Test_solarM22M_difkur`), always on a call for a metal or light element; the stored terms were finite every time, so the zero abundance made them harmless, as above. The fix was not run. Intent: The comment says the coefficients are to be zero there ("if not, write COD1 = COD2 = 0," [lines 97–98](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_cod.f#L97-L98)); only `ADS` is zeroed.
