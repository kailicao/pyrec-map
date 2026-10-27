## Explanation

**Purpose.** The first step of [[microdiff.f#MICRODIFF|MICRODIFF]]: it decides which part of the star takes part in settling, and converts the model's variables to the units of Bahcall and Loeb (1989), as its comments call them.

**How it fits.**
- **Inputs:** the arguments of `MICRODIFF` (see there); `XMIN` and `YMIN` from `NMLPAR_MOD` (namelist variables read by [[parmin.f#PARMIN|PARMIN]]); the solar constants in `CONSTANTS_MOD` (not used: the routine has its own constants).
- **Who calls it:** only [[microdiff.f#MICRODIFF|MICRODIFF]].
- **Outputs:** `IBEGIN`, `IEND`, `LALLCZ`; the unlogged radius `HRU` and temperature `HTU` in the new units; the unlogged density `ODEN` and temperature `OTEM` in cgs units; and, **in place**, `HS1`, `HQPR`, `DT` and `STOT`, converted to the new units. [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] converts them back at the end.
- **Modules:** it writes the conversion factors to `CONFAC_MOD`, which `MICRODIFF_ETM` reads (as do [[setup_grsett.f#SETUP_GRSETT|SETUP_GRSETT]] and [[equal_to_model.f#EQUAL_TO_MODEL|EQUAL_TO_MODEL]] in the older settling path). It reads `NMLPAR_MOD` (`XMIN`, `YMIN`), `CONSTANTS_MOD` (`CLN`) and `IOUNITS_MOD` (`ISHORT`, for the messages), and takes `JSON` from `DIMENSIONS_MOD`. The unused COMMON blocks of `rp_1` (`/GRAVST/`, `/GRAVS3/`, `/SCRTCH/`, `/GSCOF/`, `/CMIXING/`) are no longer declared.

**The method.**
1. **The diffusion region.** If the centre is convective (`LC(1)`), `IBEGIN` is the last point of the convective core; if every point is convective, settling is skipped (`LALLCZ = .TRUE.`). `IBEGIN` then moves out to the first point with $X >$ `XMIN`. If the surface is convective, `IEND` is the innermost point of the surface convection zone, otherwise the last point `M`; it then moves inward to the outermost point with $Y >$ `YMIN`. A model with $X \le$ `XMIN` or $Y \le$ `YMIN` everywhere is skipped.
2. **Units.** With $R_\odot = 6.9598\times10^{10}$ cm (`CRSUN_BAH`) and the year $3.1558\times10^{7}$ s (`CSECYR_BAH`):
$$r' = \frac{r}{R_\odot},\quad T' = \frac{T}{10^7\ \mathrm{K}},\quad m' = \frac{10^{-2}\,m}{R_\odot^{3}},\quad \left(\frac{d\ln P}{dr}\right)' = R_\odot\,\frac{d\ln P}{dr},\quad \Delta t' = \frac{\Delta t}{2.7\times10^{13}\ \mathrm{yr}}.$$
That is, the mass unit is $100\ \mathrm{g\,cm^{-3}}\times R_\odot^3$. The comment says the time unit "includes factor of 2.2 from ln Lambda", the Coulomb logarithm that [[microdiff_cod.f#MICRODIFF_COD|MICRODIFF_COD]] divides by.

**Design.** `HS1`, `HQPR`, `DT` and `STOT` belong to the caller and are converted in place; `MICRODIFF_ETM` converts them back. When settling is skipped, the routine returns before converting, so the two stay consistent.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (the unused ones dropped), `IMPLICIT NONE`.

## Questions for the experts

1. **A copied comment.** The second exit (no helium above `YMIN`) is commented "HYDROGEN-FREE MODEL", copied from the first.
2. **Overshoot.** Two comments say "COMPUTE OVERSHOOT (TO BE ADDED)". Settling ignores overshoot at the convective boundaries. Is this still planned?
3. **Constants of its own.** The routine uses its own $R_\odot$ and year rather than `CRSUN` and `CSECYR` from `CONSTANTS_MOD`, which it uses. Intended, to keep Bahcall and Loeb's values?
4. **No check that `IEND > IBEGIN`.** After the two searches, nothing checks that the region between `IBEGIN` and `IEND` is not empty. If it is, [[microdiff_mte.f#MICRODIFF_MTE|MICRODIFF_MTE]] divides the total width (zero or negative) by the minimum spacing, which is the same number, and builds a grid with $\Delta r \le 0$ (or 0/0 when the width is zero). Should settling be skipped then, as for a fully convective model?
