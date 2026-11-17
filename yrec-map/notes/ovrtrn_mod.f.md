## Explanation

**Purpose.** `OVRTRN_MOD` holds the convective overturn time and the photospheric pressure at the start and end of a step, and the fraction of the step reached, which the wind laws and the rotational mixing use. Shared by 18 routines. It replaces `COMMON/OVRTRN/` (MHP via Claude, 10/14/26), less its two switches `LNEWTCZ` and `LCALCENV`, which are now in [`NMLPAR_MOD`](nmlpar_mod.f.md) (default `.TRUE.` each).

**What its variables hold, who sets them, who reads them.**
- `TAUCZ`: the convective overturn time of the surface convection zone (seconds; [`MASSLOSS`](massloss.f.md#massloss) prints `TAUCZ/CSECYR`). Computed by [`TAUCAL`](taucal.f.md#taucal), [`TAUINT`](tauint.f.md#tauint) or [`TAUINTNEW`](tauintnew.f.md#tauintnew), reached through [`GETTAU`](gettau.f.md#gettau) (which first sets it to 0) and [`ENVINT`](envint.f.md#envint); `MASSLOSS` and the [main program](main.f.md#file-level) reset it to 0 when there is no convective envelope. Read by the wind laws ([`WIND`](wind.f.md#wind), [`COWIND`](cowind.f.md#cowind), [`MWIND`](mwind.f.md#mwind), [`MCOWIND`](mcowind.f.md#mcowind)), [`AMCALC`](amcalc.f.md#amcalc), [`DADCOEFT`](dadcoeft.f.md#dadcoeft), [`DEUTRATE`](deutrate.f.md#deutrate), [`ENGEB`](engeb.f.md#engeb) and [`WRTOUT`](wrtout.f.md#wrtout).
- `PPHOT`: the photospheric pressure, set by `ENVINT` (and to 0 first by `GETTAU`); read by `AMCALC` and `WRTOUT`.
- `TAUCZ0`, `PPHOT0`: `TAUCZ` and `PPHOT` at the start of the step, copied after `GETTAU` by [`STARIN`](starin.f.md#starin) (for the first model) and `WRTOUT` (for the next step); read by `AMCALC`, `MWIND`, `MCOWIND`.
- `FRACSTEP`: the fraction of the step at which the wind is evaluated, for $`\tau = \tau_0 + f\,(\tau_1-\tau_0)`$; set to 0.5 by `STARIN` and by [`GETW`](getw.f.md#getw) (which also sets it to the fraction reached in its substeps); read by `AMCALC`, `MWIND`, `MCOWIND`.

**Design.** A blanket `USE OVRTRN_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/OVRTRN/` as a module, with `LNEWTCZ` and `LCALCENV` moved to `NMLPAR_MOD`.
