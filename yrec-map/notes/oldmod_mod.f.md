## Explanation

**Purpose.** `OLDMOD_MOD` holds the model at the start of the step (the "old" model): its structure, composition, effective temperature and number of shells, shared by 17 routines. It replaces `COMMON/OLDMOD/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]].

**What its variables hold, who sets them, who reads them.**
- `HPO`, `HTO`, `HRO`, `HLO`, `HDO` (`JSON` each): $\log P$, $\log T$, $\log r$, $L$ and $\log\rho$ of the old model. Saved by [[hpoint.f#HPOINT|`HPOINT`]] (when it remaps the model onto a new grid, interpolating them with [[osplin.f#OSPLIN|`OSPLIN`]]), by the [[main.f#(file level)|main program]] ("save old model for PTIME") and by [[starin.f#STARIN|`STARIN`]]. Read by [[ptime.f#PTIME|`PTIME`]] (the time step from the structure changes), [[midmod.f#MIDMOD|`MIDMOD`]] (interpolation within the step), [[entime.f#ENTIME|`ENTIME`]], [[lirate88.f#LIRATE88|`LIRATE88`]] (the old rates) and [[liburn.f#LIBURN|`LIBURN`]], [[liburn2.f#LIBURN2|`LIBURN2`]].
- `HCOMPP(15,JSON)`: the old composition, saved by the main program, HPOINT, [[getw.f#GETW|`GETW`]] and [[bursmix.f#BURSMIX|`BURSMIX`]]; read by the burning routines ([[kemcom.f#KEMCOM|`KEMCOM`]], [[eqburn.f#EQBURN|`EQBURN`]], [[dburn.f#DBURN|`DBURN`]], [[dburnm.f#DBURNM|`DBURNM`]], LIRATE88), MIDMOD, [[checkc.f#CHECKC|`CHECKC`]] and [[crrect.f#CRRECT|`CRRECT`]].
- `HSS(JSON)`: the old mass coordinates, against which HPOINT interpolates (and the new grid while HPOINT builds it).
- `LCO`, `LCZO` (`JSON` each): the old convective flags, saved by HPOINT; `LCO` is read by MIDMOD, `LCZO` nowhere.
- `TEFFLO`, `MO`: the old $\log T_\mathrm{eff}$ and number of shells ("JVS 04/14", "JVS 05/25"), saved by the main program, HPOINT and STARIN; read by `ENTIME`, which compares them with the new model.

**Design.** A blanket `USE OLDMOD_MOD`. HPOINT also uses `HPO`, `HTO` and `HDO` as scratch arrays ("note HDO is being used as a dummy array here"), so between HPOINT and the next save they do not hold the old model. At `rp_1`, [[mix.f#MIX|`MIX`]] and [[seculr.f#SECULR|`SECULR`]] also declared the block without using it; they no longer do.

**Changed since `rp_1`.** New file: `COMMON/OLDMOD/` as a module (two unused declarations dropped).

## Questions for the experts

1. **An unused copy.** `LCZO` is saved by HPOINT and read nowhere. Can it go?
