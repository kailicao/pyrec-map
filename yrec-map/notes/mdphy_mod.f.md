## Explanation

**Purpose.** `MDPHY_MOD` holds physical quantities at each shell at an intermediate time of the model step, for the rotational-mixing and angular-momentum transport loop, shared by 10 routines. It replaces `COMMON/MDPHY/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](dimensions_mod.f.md#dimensions_mod). All members are arrays of `JSON`.

**What its variables hold, who sets them, who reads them.** [`MIDMOD`](midmod.f.md#midmod) sets them by linear interpolation, with weight `FX`, between the old model (`…O`) and the new one:
- `DELRM`, `DELAM`, `DELM`: the radiative, adiabatic and actual temperature gradients; `CPM` ($`c_P`$), `QDTM` (a thermodynamic derivative), `OM` (opacity), `ESUMM` (energy generation, `SESUM`) and `EPSM` (the same plus `SEG(6,J)` and `SEG(7,J)`), `THDIFM` (thermal diffusivity), `VISCM` (viscosity). Read by [`SETUPV`](setupv.f.md#setupv) (which interpolates most of them to the interfaces, into [`INTVAR_MOD`](intvar_mod.f.md#intvar_mod)), [`VCIRC`](vcirc.f.md#vcirc) (`THDIFM`, `VISCM`), [`ROTMIX`](rotmix.f.md#rotmix) (`DELM`), [`ROTGRID`](rotgrid.f.md#rotgrid) and [`MIXGRID`](mixgrid.f.md#mixgrid) (`EPSM`), and [`LIBURN`](liburn.f.md#liburn), [`LIBURN2`](liburn2.f.md#liburn2) (`DELAM`, `DELRM`, to find the convective boundary); MIDMOD itself uses `DELAM` − `DELRM` to decide whether a shell that changes state over the step is convective.
- `VELM`: the convective velocity, interpolated where the shell keeps its state, the larger of the two where it becomes convective, 0 where it becomes radiative ([midmod.f, lines 178–188](https://github.com/yreclab/yrec/blob/7be4133/src/midmod.f#L178-L188)); read nowhere: unused?
- `AMUM`: the mean molecular weight, set by MIDMOD, by [`CHECKC`](checkc.f.md#checkc) (from the new composition) and [`GETW`](getw.f.md#getw) (corrected for the change over the step); read by `SETUPV` and `VCIRC` (the $`\mu`$-gradient terms).

**Design.** A blanket `USE MDPHY_MOD`. At `rp_1`, [`CODIFF`](codiff.f.md#codiff) and [`MIXCZ`](mixcz.f.md#mixcz) also declared the block; they no longer do.

**Changed since `rp_1`.** New file: `COMMON/MDPHY/` as a module.
