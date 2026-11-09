## Explanation

**Purpose.** The first step of [[microdiff.f#MICRODIFF|MICRODIFF]]: it decides which part of the star takes part in settling, and converts the model's variables to the units of Bahcall and Loeb (1989), as its comments call them.

**How it fits.**
- **Inputs:** the arguments of `MICRODIFF` (see there); `XMIN` and `YMIN` from `NMLPAR_MOD` (namelist variables read by [[parmin.f#PARMIN|PARMIN]]); the solar constants in `CONSTANTS_MOD` (not used: the routine has its own constants).
- **Who calls it:** only [[microdiff.f#MICRODIFF|MICRODIFF]].
- **Outputs:** `IBEGIN`, `IEND`, `LALLCZ`; the unlogged radius `HRU` and temperature `HTU` in the new units; the unlogged density `ODEN` and temperature `OTEM` in cgs units; and, **in place**, `HS1`, `HQPR`, `DT` and `STOT`, converted to the new units. [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] converts them back at the end.
- **Modules:** it writes the conversion factors to `CONFAC_MOD`, which `MICRODIFF_ETM` reads (as do [[setup_grsett.f#SETUP_GRSETT|SETUP_GRSETT]] and [[equal_to_model.f#EQUAL_TO_MODEL|EQUAL_TO_MODEL]] in the older settling path). It reads `NMLPAR_MOD` (`XMIN`, `YMIN`), `CONSTANTS_MOD` (`CLN`) and `IOUNITS_MOD` (`ISHORT`, for the messages), and takes `JSON` from `DIMENSIONS_MOD`. The unused COMMON blocks of `rp_1` (`/GRAVST/`, `/GRAVS3/`, `/SCRTCH/`, `/GSCOF/`, `/CMIXING/`) are no longer declared.

**The method.**
1. **The diffusion region.** If the centre is convective (`LC(1)`), `IBEGIN` is the last point of the convective core; if every point is convective, settling is skipped (`LALLCZ = .TRUE.`). `IBEGIN` then moves out to the first point with $X >$ `XMIN`. If the surface is convective, `IEND` is the innermost point of the surface convection zone, otherwise the last point `M`; it then moves inward to the outermost point with $Y >$ `YMIN`. A model with $X \le$ `XMIN` or $Y \le$ `YMIN` everywhere is skipped.

    > **Question** ([[#L101]]; [[#L123]]). **Overshoot.** Two comments say "COMPUTE OVERSHOOT (TO BE ADDED)", so settling ignores overshoot at the convective boundaries: `IBEGIN` and `IEND` are the convective boundaries themselves. Is this still planned?

    > **Question** ([[#L110]]; [[#L133-L137]]). **A copied comment.** The second exit (no helium above `YMIN`) is commented "HYDROGEN-FREE MODEL", copied from the first; its message says "Y BELOW". Should the comment read "HELIUM-FREE MODEL"?

2. **Units.** With $R_\odot = 6.9598\times10^{10}$ cm (`CRSUN_BAH`) and the year $3.1558\times10^{7}$ s (`CSECYR_BAH`):
$$r' = \frac{r}{R_\odot},\quad T' = \frac{T}{10^7\ \mathrm{K}},\quad m' = \frac{10^{-2}\,m}{R_\odot^{3}},\quad \left(\frac{d\ln P}{dr}\right)' = R_\odot\,\frac{d\ln P}{dr},\quad \Delta t' = \frac{\Delta t}{2.7\times10^{13}\ \mathrm{yr}}.$$
That is, the mass unit is $100\ \mathrm{g\,cm^{-3}}\times R_\odot^3$. The comment says the time unit "includes factor of 2.2 from ln Lambda", the Coulomb logarithm that [[microdiff_cod.f#MICRODIFF_COD|MICRODIFF_COD]] divides by.

    > **Question** ([[#L86-L87]]; [[#L144-L148]]). **Constants of its own.** The routine uses its own $R_\odot$ and year (`CRSUN_BAH`, `CSECYR_BAH`) rather than `CRSUN` and `CSECYR` from `CONSTANTS_MOD`, which it uses (for `CLN`). Is this intended, to keep Bahcall and Loeb's values?

**Design.** `HS1`, `HQPR`, `DT` and `STOT` are converted in place, and `MICRODIFF_ETM` converts them back; since [[microdiff.f#MICRODIFF|MICRODIFF]] passes copies of them ([[microdiff.f#L112-L117]]), the caller's own values are not touched. When settling is skipped, the routine returns before converting, so the two stay consistent.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (the unused ones dropped), `IMPLICIT NONE`.

## Bugs, by priority

1. **(b)** **No check that `IEND > IBEGIN`.** ([[#L107-L116]]; [[#L130-L139]]) After the two searches, nothing checks that the region from `IBEGIN` to `IEND` is not empty. The search for $X >$ `XMIN` runs outward to `M`, past `IEND`, so when the hydrogen-exhausted centre reaches the base of the convective envelope, `IBEGIN` ends inside the envelope, beyond `IEND`. What follows in [[microdiff_mte.f#MICRODIFF_MTE|MICRODIFF_MTE]]: the total width `DRTOT` is zero or negative and is divided by the minimum spacing, which is the same number ([[microdiff_mte.f#L54-L63]]); with `IEND = IBEGIN` this is 0/0 and `DR` = 0, and [[microdiff_run.f#MICRODIFF_RUN|MICRODIFF_RUN]] divides by `DR` ([[microdiff_run.f#L145]]); with `IEND < IBEGIN` the grid runs inward, and [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] applies both the central and the envelope change to the shells between them. Only with `LNEWDIF` and `LDIFY`, `LDIFZ` or `LDIFLI` (all off by default; the test suite's settling decks set them); whether a run reaches such a model was not traced. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to skip settling when the region between IBEGIN and
    C IEND is empty, as for a fully convective model.
       47 CONTINUE
          IEND = I
          IF(IEND.LE.IBEGIN)THEN
             WRITE(ISHORT,18)
       18    FORMAT(1X,' NO RADIATIVE REGION LEFT - NO SETTLING')
             LALLCZ = .TRUE.
             GOTO 9999
          ENDIF
    ```
