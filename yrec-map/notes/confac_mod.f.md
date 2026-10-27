## Explanation

**Purpose.** `CONFAC_MOD` holds the factors that convert radius, mass, temperature and time between the code's units and those of the diffusion routines (from Bahcall's): `CON_RAD`, `CON_MASS`, `CON_TEMP`, `CON_TIME`. It replaces `COMMON/CONFAC/` (MHP via Claude, 10/14/26).

**Who sets them, who reads them.** Set by [[microdiff_setup.f#MICRODIFF_SETUP|`MICRODIFF_SETUP`]] and [[setup_grsett.f#SETUP_GRSETT|`SETUP_GRSETT`]], with the same formulas ($1/R_\odot$, $10^{-2}$ `CON_RAD`³, $10^{-7}$, $2.7\times10^{13}$ yr in seconds); read by them and by [[equal_to_model.f#EQUAL_TO_MODEL|`EQUAL_TO_MODEL`]] and [[microdiff_etm.f#MICRODIFF_ETM|`MICRODIFF_ETM`]].

**Changed since `rp_1`.** New file: `COMMON/CONFAC/` as a module.
