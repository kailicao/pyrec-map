## Explanation

**Purpose.** "Equal to model": the last step of [[microdiff.f#MICRODIFF|MICRODIFF]]. It interpolates the changes in abundance from the equally spaced grid back to the model points, applies them to `HCOMP`, recomputes helium, and converts the variables changed by [[microdiff_setup.f#MICRODIFF_SETUP|MICRODIFF_SETUP]] back to cgs units.

**How it fits.**
- **Inputs:** the equal grid radii `ER`, the changes `EDELX`, `EDELZ`, `EDELLI` from [[microdiff_run.f#MICRODIFF_RUN|MICRODIFF_RUN]], `IBEGIN`, `IEND`, `NPT`, and the conversion factors in `CONFAC_MOD` (written by `MICRODIFF_SETUP`).
- **Who calls it:** only `MICRODIFF`.
- **What it calls:** [[intrp2.f#INTRP2|INTRP2]], for four-point Lagrange weights.
- **Outputs:** `HCOMP` updated in place; `HRU`, `HTU`, `HS1`, `HQPR`, `DT` and `STOT` converted back ([[#L165-L172]]), though [[microdiff.f#MICRODIFF|MICRODIFF]] passes its local `HRU` and `HTU` and copies of the other four, and returns right after the call ([[microdiff.f#L112-L117]]; [[microdiff.f#L242-L244]]): unused?
- **Modules:** `CONFAC_MOD`, `NMLPAR_MOD` (`LDIFZ`, `LDIFLI`), `DIMENSIONS_MOD` (`JSON`).

**The method.**
1. **Central region** (points `1..IBEGIN`, the convective core or the hydrogen-exhausted centre): the change at the first grid point is added to each point: $X \to \max(X + \Delta X_1, 0)$, the light elements likewise floored at zero, and $Z \to \min(Z + \Delta Z_1,\ 1 - X - X_3)$.
2. **Radiative interior** (points `IBEGIN+1..IEND-1`): the change is interpolated with four-point Lagrange weights $w_k$ over the grid points around the model radius, $\Delta X(r) = \sum_k w_k\,\Delta X_{k_0+k-1}$, and $X \to \min(X + \Delta X, 1 - Z - X_3)$.
3. **Envelope** (points `IEND..M`): the change at the last grid point is added, with $X$ capped as above and $Z$ floored at zero.

    > **Question** ([[#L47-L48]]; [[#L104-L111]]; [[#L135-L142]]). **The guard comment.** The comment says the failsafes guard "against negative X and Z>1 respectively," and so they do in the centre ($X \ge 0$, $Z \le 1 - X - X_3$); but in the interior $X$ and $Z$ are both capped from above, and in the envelope $X$ is capped from above and $Z$ floored at zero. Which guards are intended where?

4. **Metals** are scaled as a whole: with $Z' = Z + \Delta Z$ (capped at $1 - X - X_3$ in the centre and the interior), the individual metal rows 5–11 of `HCOMP` (¹²C, ¹³C, ¹⁴N, ¹⁵N, ¹⁶O, ¹⁷O, ¹⁸O, as STARIN names them) are multiplied by $Z'/Z$.
5. **Helium** follows from closure: $Y = 1 - X - Z - X_3$, where $X_3$ is ³He, `HCOMP(4,·)` ([[starin.f#STARIN|STARIN]] fills it from `XHE3_INI`).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

**Changed since `a8a5950`.** The file is unchanged, but [[microdiff_mte.f#MICRODIFF_MTE|`MICRODIFF_MTE`]] now gives the grid at least 4 points, so `K0` stays within the grid; this settles former question 5.

## Bugs, by priority

1. **(harmless in the runs)** **Light elements in the interior and the envelope are not floored at zero.** ([[#L66-L74]]; [[#L122-L131]]; [[#L156-L163]]) The light elements (`HCOMP(13..15,·)`) are floored at zero only in the centre (`MAX(…,XMINIM)`); in the interior (`HCOMP(II,I) + DXMOD`, with `DXMOD` from four-point Lagrange interpolation, which can overshoot) and in the envelope the change is added with no floor. What follows: where an element is nearly depleted, its abundance can become negative until `MIX` and `ROTMIX` floor every species at zero after the settling substeps ([[mix.f#L470]]; [[rotmix.f#L244]]), so only the later substeps of the same call see it. Only with `LNEWDIF` and `LDIFLI` (both off by default; the test suite's settling decks set them).

    **A possible fix:**

    ```diff
    --- a/src/microdiff_etm.f
    +++ b/src/microdiff_etm.f
    @@ -126,7 +126,10 @@
          *                 FACINTERP(2)*EDELLI(KK,K0+1)+
          *                 FACINTERP(3)*EDELLI(KK,K0+2)+
          *                 FACINTERP(4)*EDELLI(KK,K0+3)
    -               HCOMP(II,I) = HCOMP(II,I) + DXMOD
    +C 11/09/26 KC via Claude
    +C code changed to floor the light elements at zero in the interior
    +C and the envelope too, as in the centre.
    +               HCOMP(II,I) = MAX(HCOMP(II,I) + DXMOD,0.0D0)
                 ENDDO
              ENDIF
        20 CONTINUE
    @@ -157,7 +160,7 @@
              DO KK = 1,NLIGHT
                 DO 65 I = IEND,M
                    II = CSLIGHT(KK)
    -               HCOMP(II,I)=HCOMP(II,I) + EDELLI(KK,NPT)
    +               HCOMP(II,I)=MAX(HCOMP(II,I) + EDELLI(KK,NPT),0.0D0)
        65       CONTINUE
              ENDDO
           ENDIF
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): taken in all seven runs with settling (`testsuite/Test_solarGS98_dif`, `testsuite/Test_solarAAG21_dif`, `testsuite/Test_solarM22M_difkur`, `testsuite/Test_solarGS98_difrotmixper18p4d1p0`, `testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`, `testsuite/Test_m1p4feh+0p0GS98_dif_TAMS`, and `testsuite/Test_solarAAG21_dif` with a custom mixture), up to 13.2 million times per run (`testsuite/Test_solarM22M_difkur`). A light element became negative 7,781 to 92,130 times per run, by at most $3.8\times10^{-13}$. With the fix, `testsuite/Test_m1p4feh+0p0GS98_dif_TAMS` and `testsuite/Test_solarM22M_difkur` give identical tracks and stored models, with the same numbers of models and ages, since `MIX` floors the values at zero anyway (above). The negative values never reach the model, and the code relies on that later floor. Intent: The comment guards X and Z only ("GUARDING AGAINST NEGATIVE X AND Z>1," [[#L46-L48]]), and the light elements have a floor only in the centre ([[#L68-L71]]).

2. **(never occurred)** **Division by zero where $Z = 0$.** ([[#L53]]; [[#L112]]; [[#L143]]) `ZZ2 = ZZ/HCOMP(3,I)` divides by zero at a point with $Z = 0$; with IEEE arithmetic it gives an infinity or NaN rather than a stop, and the metal rows 5–11 (zero there) become NaN. Only with `LNEWDIF` and `LDIFZ` and a model with $Z = 0$ somewhere (a metal-free model).

    **A possible fix** (the same at the three places; where $Z = 0$ the rows 5–11 stay zero):

    ```diff
    --- a/src/microdiff_etm.f
    +++ b/src/microdiff_etm.f
    @@ -50,7 +50,13 @@
              DO I = IBEGIN,1,-1
                 ZMAX = 1.0D0 - HCOMP(1,I) - HCOMP(4,I)
                 ZZ=MIN(HCOMP(3,I)+EDELZ(1),ZMAX)
    -            ZZ2 = ZZ/HCOMP(3,I)
    +C 11/09/26 KC via Claude
    +C code changed to avoid a division by zero where Z = 0.
    +            IF(HCOMP(3,I).GT.0.0D0)THEN
    +               ZZ2 = ZZ/HCOMP(3,I)
    +            ELSE
    +               ZZ2 = 1.0D0
    +            ENDIF
                 HCOMP(3,I) = ZZ
                 DO J = 5,11
                    HCOMP(J,I) = ZZ2*HCOMP(J,I)
    @@ -109,7 +115,13 @@
                 DZMOD = FACINTERP(1)*EDELZ(K0)+FACINTERP(2)*EDELZ(K0+1)+
          *             FACINTERP(3)*EDELZ(K0+2)+FACINTERP(4)*EDELZ(K0+3)
                 ZZ = MIN(HCOMP(3,I)+DZMOD,ZMAX)
    -            ZZ2 = ZZ/HCOMP(3,I)
    +C 11/09/26 KC via Claude
    +C code changed to avoid a division by zero where Z = 0.
    +            IF(HCOMP(3,I).GT.0.0D0)THEN
    +               ZZ2 = ZZ/HCOMP(3,I)
    +            ELSE
    +               ZZ2 = 1.0D0
    +            ENDIF
                 HCOMP(3,I)=ZZ
                 DO J = 5,11
                    HCOMP(J,I) = ZZ2*HCOMP(J,I)
    @@ -140,7 +152,13 @@
              ZMIN = 0.0D0
              DO I = IEND,M
                 ZZ = MAX(HCOMP(3,I)+EDELZ(NPT),ZMIN)
    -            ZZ2 = ZZ/HCOMP(3,I)
    +C 11/09/26 KC via Claude
    +C code changed to avoid a division by zero where Z = 0.
    +            IF(HCOMP(3,I).GT.0.0D0)THEN
    +               ZZ2 = ZZ/HCOMP(3,I)
    +            ELSE
    +               ZZ2 = 1.0D0
    +            ENDIF
                 HCOMP(3,I) = ZZ
                 DO J = 5,11
                    HCOMP(J,I) = ZZ2*HCOMP(J,I)
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): taken in all seven runs with settling (six of the test suite's and a made-up one with a custom mixture, listed in [[#b1]]), up to 4.7 million times per run; $Z$ was never zero (at least 0.0020). Not reached: It needs `LDIFZ` and a model with $Z = 0$ somewhere, and no case has a metal-free model. The fix was not run. Intent: none found.
