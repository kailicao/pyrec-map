## Explanation

**Purpose.** `MICRODIFF` is the driver of YREC's newer treatment of gravitational settling (microscopic diffusion) of helium, metals and light elements. Its header (Garrett Somers, 05/2015) says it is adapted from [[grsett.f#GRSETT|GRSETT]], "which is retained for backwards compatability", and "follows the formulism of Bahcall and Loeb 1989". It moves the model onto an equally spaced grid in radius, diffuses each species there, and maps the changes back onto the model's mass grid.

**How it fits.**
- **Inputs (arguments):** the time step `DT` (s), the composition `HCOMP(15,M)`, $d\ln P/dr$ (`HQPR`), $\log r$ (`HR`, cm), $\log\rho$ (`HD`), the unlogged mass `HS1` (g), $\log T$ (`HT`), the convection flags `LC`, the number of points `M` and the total mass `STOT`. `STOT` is in grams; [[microdiff_setup.f#MICRODIFF_SETUP|MICRODIFF_SETUP]] converts `DT`, `STOT`, `HS1` and `HQPR` in place and [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] converts them back. The temperature gradient $\nabla = d\ln T/d\ln P$ (`SDEL(2,·)` in `/SCRTCH/`), named in the header, is read not here but by `MICRODIFF_MTE`.
- **Who calls it:** [[mix.f#MIX|MIX]] (when the settling flags are on and `LNEWDIF` selects the new routine) and [[rotmix.f#ROTMIX|ROTMIX]] (the same inside the rotational-mixing step).
- **What it calls:** the four parts of the method, in order: [[microdiff_setup.f#MICRODIFF_SETUP|MICRODIFF_SETUP]] (units and boundaries), [[microdiff_mte.f#MICRODIFF_MTE|MICRODIFF_MTE]] (model to equal grid), [[microdiff_run.f#MICRODIFF_RUN|MICRODIFF_RUN]] (once per diffused species) and [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] (equal grid back to model).
- **Output:** the updated `HCOMP`, in place.
- **COMMON blocks:** `/GRAVST/` (`LDIFY`, the tolerance `GRTOL`, the iteration limit `NITER_GS`; set by [[parmin.f#PARMIN|PARMIN]] and shared with GRSETT, MIX, ROTMIX, the other MICRODIFF routines and the output routines), `/GRAVS3/` (`LDIFZ`, `FGRY`, `FGRZ`, `LTHOUL`), `/GRAVS4/` (`LNEWDIF`, `LDIFLI`), and `/CONST1/` and `/LUOUT/`.

**The method.** After the set-up (which returns at once for a fully convective model, or one with no hydrogen or helium left), up to three kinds of species are diffused, each by a call to `MICRODIFF_RUN` that returns the *change* in abundance on the equal grid:
1. **Hydrogen** if `LDIFY`: column $j=1$ of the three-species vector `ESPEC` (X, Y, and a third species), with the metals as the third species, taken as iron ($A = 55.86$, $Z = 26$). Helium then follows from $Y = 1 - X - Z - X_4$ in `MICRODIFF_ETM`.
2. **Metals** if `LDIFZ`: column $j=3$, again as iron.
3. **Light elements** if `LDIFLI`: `NLIGHT = 3` species in `HCOMP` rows `CSLIGHT = 13, 14, 15`, with atomic weights 6.015, 7.016, 9.012 and charges 3, 3, 4 (⁶Li, ⁷Li and ⁹Be: [[starin.f#STARIN|STARIN]] fills these rows from `XLI6_INI`, `XLI7_INI` and `XBE9_INI`), each in turn as the third species.

The changes `EDELX`, `EDELZ` and `EDELLI` are passed to `MICRODIFF_ETM`, which interpolates them back and applies them.

**Grids.** Variables prefixed `E` are on the equally spaced grid in radius; those also suffixed `_H` are at the midpoints between its points. Both are needed by the two-step Lax–Wendroff scheme.

**KC's changes.** 2025-05-30: `CSLIGHT` declared `INTEGER` (fixing `-Wconversion`); 2025-05-31: unused arguments dropped from the calls to `MICRODIFF_MTE` (`HTU`, `LC`) and `MICRODIFF_RUN` (`NLIGHT`, `CSLIGHT`).

## Questions for the experts

1. **Stale changes when a species is not diffused.** `MICRODIFF_ETM` always applies `EDELX` (and `EDELZ` when `LDIFZ`). If `LDIFY` is false but `LDIFZ` or `LDIFLI` is true, `EDELX` is never set in this call; as a `SAVE`d local array it holds zeros only if the compiler zero-initializes static storage, or the values of an earlier call. Should `EDELX` be zeroed when `LDIFY` is false?
2. **The last light-element point.** In the light-element loop, `ESPEC(3,I) = ELI(II,NPT)` relies on `I` equalling `NPT` after the preceding `DO I=1,NPT-1` loop. It works in practice, but `ESPEC(3,NPT)` is clearer. Intended?
3. **Iron for the metals.** All metals are diffused as one species with iron's weight and charge. Is this a deliberate choice (the heaviest abundant element) rather than a mean metal?
