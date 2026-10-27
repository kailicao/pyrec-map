## Explanation

**Purpose.** `FLUXES_MOD` holds the solar neutrino fluxes: per gram at the current shell, summed over the star, and the capture rates for the chlorine and gallium experiments, shared by 4 routines. It replaces `COMMON/FLUXES/` (MHP via Claude, 10/14/26). All members are `REAL*8`.

**What its variables hold, who sets them, who reads them.**
- `FLUX(10)`: the neutrino fluxes of the ten reactions produced per gram at one shell, scaled to the Earth's distance (divided by $4\pi\,\mathrm{AU}^2$), set by [[engeb.f#ENGEB|`ENGEB`]].
- `FLUXTOT(10)`: their sums over the shells, weighted by the shell masses: built by [[coefft.f#COEFFT|`COEFFT`]] with `LSNU`, and by the [[main.f#(file level)|main program]] in its neutrino-table block; written out by [[wrtout.f#WRTOUT|`WRTOUT`]] (which then zeroes them) and by the main program.
- `CLSNU`, `GASNU`: the capture rates (SNU) for Cl37 and Ga71, $\sum_i f_i\,\Phi_i$ over the first eight fluxes with the factors `CLSNUF`, `GASNUF`, set by `WRTOUT` ("MHP 8/96"); written by `WRTOUT` and the main program.

**Design.** A blanket `USE FLUXES_MOD`.

**Changed since `rp_1`.** New file: `COMMON/FLUXES/` as a module.
