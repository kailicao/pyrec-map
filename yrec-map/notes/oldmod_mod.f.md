## Explanation

**Purpose.** `OLDMOD_MOD` holds the model at the start of the step (the "old" model): its structure, composition, effective temperature, and surface luminosity, shared by 17 routines. It replaces `COMMON/OLDMOD/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]].

**What its variables hold, who sets them, who reads them.**
- `HPO`, `HTO`, `HRO`, `HLO`, `HDO` (`JSON` each): $\log P$, $\log T$, $\log r$, $L$ and $\log\rho$ of the old model. Saved by [[hpoint.f#HPOINT|`HPOINT`]] (when it remaps the model onto a new grid, interpolating them with [[osplin.f#OSPLIN|`OSPLIN`]]), by the [[main.f#(file level)|main program]] ("save old model for PTIME") and by [[starin.f#STARIN|`STARIN`]]. Read by [[ptime.f#PTIME|`PTIME`]] (the time step from the structure changes), [[midmod.f#MIDMOD|`MIDMOD`]] (interpolation within the step), [[lirate88.f#LIRATE88|`LIRATE88`]] (the old rates) and [[liburn.f#LIBURN|`LIBURN`]], [[liburn2.f#LIBURN2|`LIBURN2`]].
- `HCOMPP(15,JSON)`: the old composition, saved by the main program, HPOINT, [[getw.f#GETW|`GETW`]] and [[bursmix.f#BURSMIX|`BURSMIX`]]; read by the burning routines ([[kemcom.f#KEMCOM|`KEMCOM`]], [[eqburn.f#EQBURN|`EQBURN`]], [[dburn.f#DBURN|`DBURN`]], [[dburnm.f#DBURNM|`DBURNM`]], LIRATE88), MIDMOD, [[checkc.f#CHECKC|`CHECKC`]] and [[crrect.f#CRRECT|`CRRECT`]].
- `HSS(JSON)`: the old mass coordinates, against which HPOINT interpolates (and the new grid while HPOINT builds it).
- `LCO`, `LCZO` (`JSON` each): the old convective flags, saved by HPOINT (`LCZO` also by STARIN); `LCO` is read by MIDMOD, `LCZO` by [[crrect.f#CRRECT|`CRRECT`]], which passes it to [[getrot.f#GETROT|`GETROT`]].
- `TEFFLO`, `HLSURO`: the old $\log T_\mathrm{eff}$ ("JVS 04/14") and surface luminosity, saved by the main program, HPOINT (before it remaps the model) and STARIN; read by [[entime.f#ENTIME|`ENTIME`]], which compares them with the new model.

**Design.** A blanket `USE OLDMOD_MOD`. HPOINT also uses `HPO`, `HTO` and `HDO` as scratch arrays ("note HDO is being used as a dummy array here"), so between HPOINT and the next save they do not hold the old model. At `rp_1`, [[mix.f#MIX|`MIX`]] and [[seculr.f#SECULR|`SECULR`]] also declared the block without using it; they no longer do.

**Changed since `rp_1`.** New file: `COMMON/OLDMOD/` as a module (two unused declarations dropped).

**Changed since `a8a5950`.** The point count `MO` is replaced by `HLSURO`, the old model's surface luminosity, which is what ENTIME needs: `HLO(MO)` was not the surface once HPOINT had changed the number of points. Since CRRECT passes `LCZO` to GETROT (crrect.f changed, not this file), `LCZO` is read, which settles former question 1.
