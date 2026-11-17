## Explanation

**Purpose.** `CONFAC_MOD` holds the factors that convert radius, mass, temperature and time between the code's units and those of the diffusion routines (from Bahcall's): `CON_RAD`, `CON_MASS`, `CON_TEMP`, `CON_TIME`. It replaces `COMMON/CONFAC/` (MHP via Claude, 10/14/26).

**Who sets them, who reads them.** Set by [`MICRODIFF_SETUP`](microdiff_setup.f.md#microdiff_setup) and [`SETUP_GRSETT`](setup_grsett.f.md#setup_grsett), with the same formulas ($`1/R_\odot`$, $`10^{-2}`$ `CON_RAD`$`^3`$, $`10^{-7}`$, $`2.7\times10^{13}\,\mathrm{yr}`$ in seconds: the units of Bahcall and Loeb ([1989](https://ui.adsabs.harvard.edu/abs/1990ApJ...360..267B), the code's year; published 1990, ApJ 360, 267), a length unit $`R_\odot`$, a mass unit $`100\,\mathrm{g\,cm^{-3}}\times R_\odot^3`$, a temperature unit $`10^7\,\mathrm{K}`$, and a time unit that "includes factor of 2.2 from ln Lambda," the Coulomb logarithm; see [`MICRODIFF_SETUP`](microdiff_setup.f.md#microdiff_setup)); read by them and by [`EQUAL_TO_MODEL`](equal_to_model.f.md#equal_to_model) and [`MICRODIFF_ETM`](microdiff_etm.f.md#microdiff_etm).

**Changed since `rp_1`.** New file: `COMMON/CONFAC/` as a module.
