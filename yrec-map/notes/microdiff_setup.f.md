## Explanation

**Purpose.** The first step of [[microdiff.f#MICRODIFF|MICRODIFF]]: it decides which part of the star takes part in settling, and converts the model's variables to the units of Bahcall and Loeb (1989), as its comments call them.

**How it fits.**
- **Inputs:** the arguments of `MICRODIFF` (see there); `XMIN` and `YMIN` from `NMLPAR_MOD` (namelist variables read by [[parmin.f#PARMIN|PARMIN]]); the solar constants in `CONSTANTS_MOD` (not used: the routine has its own constants).
- **Who calls it:** only [[microdiff.f#MICRODIFF|MICRODIFF]].
- **Outputs:** `IBEGIN`, `IEND`, `LALLCZ`; the unlogged radius `HRU` and temperature `HTU` in the new units; the unlogged density `ODEN` and temperature `OTEM` in cgs units; and, **in place**, `HS1`, `HQPR`, `DT` and `STOT`, converted to the new units. [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] converts them back at the end.
- **Modules:** it writes the conversion factors to `CONFAC_MOD`, which `MICRODIFF_ETM` reads (as do [[setup_grsett.f#SETUP_GRSETT|SETUP_GRSETT]] and [[equal_to_model.f#EQUAL_TO_MODEL|EQUAL_TO_MODEL]] in the older settling path). It reads `NMLPAR_MOD` (`XMIN`, `YMIN`), `CONSTANTS_MOD` (`CLN`) and `IOUNITS_MOD` (`ISHORT`, for the messages), and takes `JSON` from `DIMENSIONS_MOD`. The unused COMMON blocks of `rp_1` (`/GRAVST/`, `/GRAVS3/`, `/SCRTCH/`, `/GSCOF/`, `/CMIXING/`) are no longer declared.

**The method.**
1. **The diffusion region.** If the centre is convective (`LC(1)`), `IBEGIN` is the last point of the convective core; if every point is convective, settling is skipped (`LALLCZ = .TRUE.`). `IBEGIN` then moves out to the first point with $X >$ `XMIN`. If the surface is convective, `IEND` is the innermost point of the surface convection zone, otherwise the last point `M`; it then moves inward to the outermost point with $Y >$ `YMIN`. A model with $X \le$ `XMIN` or $Y \le$ `YMIN` everywhere is skipped.

    > **Question** ([[#L101]]; [[#L123]]). **Overshoot.** Two comments say "COMPUTE OVERSHOOT (TO BE ADDED)," so settling ignores overshoot at the convective boundaries: `IBEGIN` and `IEND` are the convective boundaries themselves. Is this still planned?

    **The second exit's comment is copied from the first.** The exit taken when no helium is above `YMIN` ([[#L133-L137]]) is commented "HYDROGEN-FREE MODEL," as the hydrogen exit is ([[#L110]]); its message says "Y BELOW," so the comment should read "HELIUM-FREE MODEL."

2. **Units.** With $R_\odot = 6.9598\times10^{10}$ cm (`CRSUN_BAH`) and the year $3.1558\times10^{7}$ s (`CSECYR_BAH`):
$$r' = \frac{r}{R_\odot},\quad T' = \frac{T}{10^7\ \mathrm{K}},\quad m' = \frac{10^{-2}\,m}{R_\odot^{3}},\quad \left(\frac{d\ln P}{dr}\right)' = R_\odot\,\frac{d\ln P}{dr},\quad \Delta t' = \frac{\Delta t}{2.7\times10^{13}\ \mathrm{yr}}.$$
That is, the mass unit is $100\ \mathrm{g\,cm^{-3}}\times R_\odot^3$. The comment says the time unit "includes factor of 2.2 from ln Lambda," the Coulomb logarithm that [[microdiff_cod.f#MICRODIFF_COD|MICRODIFF_COD]] divides by.

    > **Question** ([[#L86-L87]]; [[#L144-L148]]). **Constants of its own.** The routine uses its own $R_\odot$ and year (`CRSUN_BAH`, `CSECYR_BAH`) rather than `CRSUN` and `CSECYR` from `CONSTANTS_MOD`, which it uses (for `CLN`). Is this intended, to keep Bahcall and Loeb's values?

**Design.** `HS1`, `HQPR`, `DT` and `STOT` are converted in place, and `MICRODIFF_ETM` converts them back; since [[microdiff.f#MICRODIFF|MICRODIFF]] passes copies of them ([[microdiff.f#L112-L117]]), the caller's own values are not touched. When settling is skipped, the routine returns before converting, so the two stay consistent.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (the unused ones dropped), `IMPLICIT NONE`.

## Bugs, by priority

1. **(cannot be reached)** **No check that `IEND > IBEGIN`.** ([[#L107-L116]]; [[#L130-L139]]) After the two searches, nothing checks that the region from `IBEGIN` to `IEND` is not empty. The search for $X >$ `XMIN` runs outward to `M`, past `IEND`, so if the hydrogen-exhausted centre reached the base of the convective envelope, `IBEGIN` would end inside the envelope, beyond `IEND` (but settling stops before the centre is exhausted: below). What follows in [[microdiff_mte.f#MICRODIFF_MTE|MICRODIFF_MTE]]: the total width `DRTOT` is zero or negative and is divided by the minimum spacing, which is the same number ([[microdiff_mte.f#L54-L63]]); with `IEND = IBEGIN` this is 0/0 and `DR` = 0, and [[microdiff_run.f#MICRODIFF_RUN|MICRODIFF_RUN]] divides by `DR` ([[microdiff_run.f#L145]]); with `IEND < IBEGIN` the grid runs inward, and [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] applies both the central and the envelope change to the shells between them. Only with `LNEWDIF` and `LDIFY`, `LDIFZ` or `LDIFLI` (all off by default; the test suite's settling decks set them).

    **A possible fix:**

    ```diff
    --- a/src/microdiff_setup.f
    +++ b/src/microdiff_setup.f
    @@ -135,8 +135,17 @@
        17 FORMAT(1X,'Y BELOW ',F9.6,' IN WHOLE MODEL-NO SETTLING')
           LALLCZ = .TRUE.
           GOTO 9999
    +C 11/09/26 KC via Claude
    +C code changed to skip settling when the region between IBEGIN and
    +C IEND is empty, as for a fully convective model.
        47 CONTINUE
           IEND = I
    +      IF(IEND.LE.IBEGIN)THEN
    +         WRITE(ISHORT,18)
    +   18    FORMAT(1X,' NO RADIATIVE REGION LEFT - NO SETTLING')
    +         LALLCZ = .TRUE.
    +         GOTO 9999
    +      ENDIF
     C     CON_MASS=CONVERSION FACTOR FOR MASS.
     C     CON_RADIUS=CONVERSION FACTOR FOR RADIUS.
     C     CON_TEMP=CONVERSION FACOTR FOR TEMPERATURE.
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The check point was passed at every settling call in all seven runs with settling (`testsuite/Test_solarGS98_dif`, `testsuite/Test_solarAAG21_dif`, `testsuite/Test_solarM22M_difkur`, `testsuite/Test_solarGS98_difrotmixper18p4d1p0`, `testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`, `testsuite/Test_m1p4feh+0p0GS98_dif_TAMS`, and `testsuite/Test_solarAAG21_dif` with a custom mixture), 690 to 3,703 times per run, with `IBEGIN` from 1 to 536 and `IEND` from 3 to 972, and `IEND` was above `IBEGIN` every time. It cannot be reached as described at 7be4133: `MIX` and `ROTMIX` switch settling off for the rest of the run once central $X$ falls below `XMIN` ([[mix.f#L412-L416]]; [[rotmix.f#L151-L155]]), so `IBEGIN` stays at 1 or at the edge of a mixed core, and the searches give `IEND` ≥ `IBEGIN` + 2 ([[#L91-L127]]); only the helium check ([[#L130-L139]]) could move `IEND` lower, with $Y$ below `YMIN` outside the core. It is fragile code. The fix was not run. Intent: none found.
