## Explanation

**Purpose.** `MICRODIFF` is the driver of YREC's newer treatment of gravitational settling (microscopic diffusion) of helium, metals and light elements. Its header (Garrett Somers, 05/2015) says it is adapted from [[grsett.f#GRSETT|GRSETT]], "which is retained for backwards compatability", and "follows the formulism of Bahcall and Loeb 1989". It moves the model onto an equally spaced grid in radius, diffuses each species there, and maps the changes back onto the model's mass grid.

**How it fits.**
- **Inputs (arguments):** the time step `DT` (s), the composition `HCOMP(15,M)`, $d\ln P/dr$ (`HQPR`), $\log r$ (`HR`, cm), $\log\rho$ (`HD`), the unlogged mass `HS1` (g), $\log T$ (`HT`), the convection flags `LC`, the number of points `M` and the total mass `STOT`. `STOT` is in grams; [[microdiff_setup.f#MICRODIFF_SETUP|MICRODIFF_SETUP]] converts copies of `DT`, `STOT`, `HS1`, and `HQPR` (`DTU`, `STOTU`, `HS1U`, and `HQPRU`, which `MICRODIFF` hands to all four parts of the method) in place to Bahcall and Loeb's units (radius in $R_\odot$ = 6.9598×10¹⁰ cm, temperature in $10^7$ K, mass in $100\ \mathrm{g\,cm^{-3}}\times R_\odot^3$, time in $2.7\times10^{13}$ yr, a unit that "includes factor of 2.2 from ln lambda"; the same as [[setup_grsett.f#SETUP_GRSETT|SETUP_GRSETT]]), and [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] converts them back; the caller's values are not changed. The temperature gradient $\nabla = d\ln T/d\ln P$ (`SDEL(2,·)` in `SCRTCH_MOD`), named in the header, is read not here but by `MICRODIFF_MTE`.
- **Who calls it:** [[mix.f#MIX|MIX]] (when the settling flags are on and `LNEWDIF` selects the new routine) and [[rotmix.f#ROTMIX|ROTMIX]] (the same inside the rotational-mixing step).
- **What it calls:** the four parts of the method, in order: [[microdiff_setup.f#MICRODIFF_SETUP|MICRODIFF_SETUP]] (units and boundaries), [[microdiff_mte.f#MICRODIFF_MTE|MICRODIFF_MTE]] (model to equal grid), [[microdiff_run.f#MICRODIFF_RUN|MICRODIFF_RUN]] (once per diffused species) and [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] (equal grid back to model).
- **Output:** the updated `HCOMP`, in place.
- **Modules:** `NMLPAR_MOD`, for the namelist switches `LDIFY`, `LDIFZ` and `LDIFLI` (read by [[parmin.f#PARMIN|PARMIN]] and shared with GRSETT, MIX, ROTMIX and the other MICRODIFF routines), and `DIMENSIONS_MOD` for `JSON`. The other members of `rp_1`'s `/GRAVST/`, `/GRAVS3/` and `/GRAVS4/` (`GRTOL`, `NITER_GS`, `FGRY`, `FGRZ`, `LTHOUL`, `LNEWDIF`) are in `NMLPAR_MOD` too, but not used here.

**The method.** After the set-up (which returns at once for a fully convective model, or one with no hydrogen or helium left), up to three kinds of species are diffused, each by a call to `MICRODIFF_RUN` that returns the *change* in abundance on the equal grid:
1. **Hydrogen** if `LDIFY`: column $j=1$ of the three-species vector `ESPEC` (X, Y, and a third species), with the metals as the third species, taken as iron ($A = 55.86$, $Z = 26$). Helium then follows from $Y = 1 - X - Z - X_4$ in `MICRODIFF_ETM`. `LDIFY` is always on when `MICRODIFF` runs: [[mix.f#MIX|MIX]] and [[rotmix.f#ROTMIX|ROTMIX]] call it only under `IF(LDIFY)`, and [[parmin.f#PARMIN|PARMIN]] turns `LDIFY` on with `LDIFZ` or `LDIFLI`; so `EDELX` is always set before `MICRODIFF_ETM` applies it (settled from the code, Nov 9, 2026: [[mix.f#L412]], [[rotmix.f#L151]], [[parmin.f#L1239-L1252]]; [[#L157-L182]]).
2. **Metals** if `LDIFZ`: column $j=3$, again as iron.

    > **Question** ([[#L186-L190]]). **Iron for the metals.** All metals are diffused as one species with iron's weight and charge. Is this a deliberate choice (the heaviest abundant element) rather than a mean metal?

    > **Question** ([[#L159-L160]]; [[#L189-L190]]). **Full ionization of iron.** The metals' charge is $Z = 26$ everywhere. At the base of the solar convection zone ($T \approx 2\times10^6$ K) iron is far from fully ionized (a charge of roughly 16–20), and the settling velocity depends strongly on the charge. Is the fully ionized approximation known to bias the surface $Z$ in solar calibrations, and has a mean charge been considered?

3. **Light elements** if `LDIFLI`: `NLIGHT = 3` species in `HCOMP` rows `CSLIGHT = 13, 14, 15`, with atomic weights 6.015, 7.016, 9.012 and charges 3, 3, 4 (⁶Li, ⁷Li and ⁹Be: [[starin.f#STARIN|STARIN]] fills these rows from `XLI6_INI`, `XLI7_INI` and `XBE9_INI`), each in turn as the third species. The last point is set as `ESPEC(3,I) = ELI(II,NPT)` with `I` = `NPT`, the value the loop variable has after `DO I=1,NPT-1` completes (the Fortran standard), so it is correct as written ([[#L220-L224]]).

    > **Question** ([[#L213-L234]]). **Three-species runs.** Each light element is diffused as the third species of an H–He–trace mixture, one call each, so the metals' collisions are left out of those calls (and the metals' call leaves out the light elements). Is the error from omitting the metals small enough for Li and Be?

The changes `EDELX`, `EDELZ` and `EDELLI` are passed to `MICRODIFF_ETM`, which interpolates them back and applies them.

**The physics included.** Gravitational settling, thermal diffusion (the $A_T\nabla$ term) and concentration diffusion, from Thoul et al.'s solution of Burgers' equations ([[thdiff.f#THDIFF|THDIFF]], called by [[microdiff_cod.f#MICRODIFF_COD|MICRODIFF_COD]]), with every species fully ionized (fixed charges) and no radiative accelerations (levitation). The results are therefore least trustworthy where radiative accelerations or partial ionization matter, as in the thin envelopes of F and hotter stars.

**Grids.** Variables prefixed `E` are on the equally spaced grid in radius; those also suffixed `_H` are at the midpoints between its points. Both are needed by the two-step Lax–Wendroff scheme.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (the unused `/CONST1/` and `/LUOUT/` dropped), `IMPLICIT NONE`.

**Changed since `a8a5950`.** The settling routines get copies of `DT`, `STOT`, `HS1`, and `HQPR`, so that the unit conversion and its inverse (which need not restore a value to the last bit) no longer change the structure's mass coordinate or [[mix.f#MIX|MIX]]'s sub-step.
