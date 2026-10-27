## Explanation

**Purpose.** `CENT_MOD` holds the central conditions and the base of the surface convection zone of the last model written. It replaces `COMMON/CENT/` (MHP via Claude, 10/14/26).

**What its variables hold, who sets them, who reads them.** All are set by [[wrtout.f#WRTOUT|`WRTOUT`]]: `TCENTER`, `PCENTER`, `DCENTER`, the central $\log T$, $\log P$, $\log\rho$; `CZsurf_M`, the mass of the surface convection zone ($M_\odot$; the star's mass when it is fully convective, 0 without one); `CZsurf_R`, the radius of its base ($R_\odot$). The [[main.f#(file level)|main program]] reads them for the neutrino-flux output.

**Changed since `rp_1`.** New file: `COMMON/CENT/` as a module.
