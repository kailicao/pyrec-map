## Explanation

**Purpose.** `OLDMOD_MOD` holds the model at the start of the step (the "old" model): its structure, composition, effective temperature, and surface luminosity, shared by 17 routines. It replaces `COMMON/OLDMOD/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/dimensions_mod.f#L38-L44).

**What its variables hold, who sets them, who reads them.**
- `HPO`, `HTO`, `HRO`, `HLO`, `HDO` (`JSON` each): $`\log P`$, $`\log T`$, $`\log r`$, $`L`$, and $`\log\rho`$ of the old model. Saved by [`HPOINT`](hpoint.f.md#hpoint) (when it remaps the model onto a new grid, interpolating them with [`OSPLIN`](https://github.com/yreclab/yrec/blob/7be4133/src/osplin.f#L12-L50)), by the [main program](main.f.md#file-level) ("save old model for PTIME"), and by [`STARIN`](starin.f.md#starin) (all but `HDO`). Read by [`PTIME`](https://github.com/yreclab/yrec/blob/7be4133/src/ptime.f#L6-L138) (the time step from the structure changes), [`MIDMOD`](https://github.com/yreclab/yrec/blob/7be4133/src/midmod.f#L2-L523) (interpolation within the step), [`LIRATE88`](lirate88.f.md#lirate88) (the old rates), [`LIBURN`](liburn.f.md#liburn), and [`LIBURN2`](liburn2.f.md#liburn2).
- `HCOMPP(15,JSON)`: the old composition, saved by the main program, HPOINT, [`GETW`](getw.f.md#getw), and [`BURSMIX`](bursmix.f.md#bursmix); read by the burning routines ([`KEMCOM`](kemcom.f.md#kemcom), [`EQBURN`](eqburn.f.md#eqburn), [`DBURN`](dburn.f.md#dburn), [`DBURNM`](dburnm.f.md#dburnm), LIRATE88), MIDMOD, [`CHECKC`](checkc.f.md#checkc), and [`CRRECT`](crrect.f.md#crrect).
- `HSS(JSON)`: the old mass coordinates, against which HPOINT interpolates (and the new grid while HPOINT builds it).
- `LCO`, `LCZO` (`JSON` each): the old convective flags, saved by HPOINT (`LCZO` also by STARIN); `LCO` is read by MIDMOD, `LCZO` by [`CRRECT`](crrect.f.md#crrect), which passes it to [`GETROT`](getrot.f.md#getrot).
- `TEFFLO`, `HLSURO`: the old $`\log T_\mathrm{eff}`$ ("JVS 04/14") and surface luminosity, saved by the main program, HPOINT (before it remaps the model) and STARIN; read by [`ENTIME`](entime.f.md#entime), which compares them with the new model.

**Design.** A blanket `USE OLDMOD_MOD`. HPOINT also uses `HPO`, `HTO`, and `HDO` as scratch arrays ("note HDO is being used as a dummy array here"), so between HPOINT and the next save they do not hold the old model. At `rp_1`, [`MIX`](https://github.com/yreclab/yrec/blob/7be4133/src/mix.f#L26-L507) and [`SECULR`](https://github.com/yreclab/yrec/blob/7be4133/src/seculr.f#L6-L532) also declared the block without using it; they no longer do.

**Changed since `rp_1`.** New file: `COMMON/OLDMOD/` as a module (two unused declarations dropped).

**Changed since `a8a5950`.** The point count `MO` is replaced by `HLSURO`, the old model's surface luminosity, which is what ENTIME needs: `HLO(MO)` was not the surface once HPOINT had changed the number of points. Since CRRECT passes `LCZO` to GETROT (crrect.f changed, not this file), `LCZO` is read, which settles former question 1.
