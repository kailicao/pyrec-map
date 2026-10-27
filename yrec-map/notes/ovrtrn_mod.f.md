## Explanation

**Purpose.** `OVRTRN_MOD` holds the convective overturn time and the photospheric pressure at the start and end of a step, and the fraction of the step reached, which the wind laws and the rotational mixing use. Shared by 18 routines. It replaces `COMMON/OVRTRN/` (MHP via Claude, 10/14/26), less its two switches `LNEWTCZ` and `LCALCENV`, which are now in [[nmlpar_mod.f|`NMLPAR_MOD`]] (default `.TRUE.` each).

**What its variables hold, who sets them, who reads them.**
- `TAUCZ`: the convective overturn time of the surface convection zone (seconds; [[massloss.f#MASSLOSS|`MASSLOSS`]] prints `TAUCZ/CSECYR`). Computed by [[taucal.f#TAUCAL|`TAUCAL`]], [[tauint.f#TAUINT|`TAUINT`]] or [[tauintnew.f#TAUINTNEW|`TAUINTNEW`]], reached through [[gettau.f#GETTAU|`GETTAU`]] (which first sets it to 0) and [[envint.f#ENVINT|`ENVINT`]]; `MASSLOSS` and the [[main.f#(file level)|main program]] reset it to 0 when there is no convective envelope. Read by the wind laws ([[wind.f#WIND|`WIND`]], [[cowind.f#COWIND|`COWIND`]], [[mwind.f#MWIND|`MWIND`]], [[mcowind.f#MCOWIND|`MCOWIND`]]), [[amcalc.f#AMCALC|`AMCALC`]], [[dadcoeft.f#DADCOEFT|`DADCOEFT`]], [[deutrate.f#DEUTRATE|`DEUTRATE`]], [[engeb.f#ENGEB|`ENGEB`]] and [[wrtout.f#WRTOUT|`WRTOUT`]].
- `PPHOT`: the photospheric pressure, set by `ENVINT` (and to 0 first by `GETTAU`); read by `AMCALC` and `WRTOUT`.
- `TAUCZ0`, `PPHOT0`: `TAUCZ` and `PPHOT` at the start of the step, copied after `GETTAU` by [[starin.f#STARIN|`STARIN`]] (for the first model) and `WRTOUT` (for the next step); read by `AMCALC`, `MWIND`, `MCOWIND`.
- `FRACSTEP`: the fraction of the step at which the wind is evaluated, for $\tau = \tau_0 + f\,(\tau_1-\tau_0)$; set to 0.5 by `STARIN` and by [[getw.f#GETW|`GETW`]] (which also sets it to the fraction reached in its substeps); read by `AMCALC`, `MWIND`, `MCOWIND`.

**Design.** A blanket `USE OVRTRN_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/OVRTRN/` as a module, with `LNEWTCZ` and `LCALCENV` moved to `NMLPAR_MOD`.
