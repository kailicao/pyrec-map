## Explanation

**Purpose.** `MDPHY_MOD` holds physical quantities at each shell at an intermediate time of the model step, for the rotational-mixing and angular-momentum transport loop, shared by 10 routines. It replaces `COMMON/MDPHY/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]]. All members are arrays of `JSON`.

**What its variables hold, who sets them, who reads them.** [[midmod.f#MIDMOD|`MIDMOD`]] sets them by linear interpolation, with weight `FX`, between the old model (`…O`) and the new one:
- `DELRM`, `DELAM`, `DELM`: the radiative, adiabatic and actual temperature gradients; `CPM` ($c_P$), `QDTM` (a thermodynamic derivative), `OM` (opacity), `ESUMM` (energy generation, `SESUM`) and `EPSM` (the same plus `SEG(6,J)` and `SEG(7,J)`), `THDIFM` (thermal diffusivity), `VISCM` (viscosity). Read by [[setupv.f#SETUPV|`SETUPV`]] (which interpolates most of them to the interfaces, into [[intvar_mod.f#INTVAR_MOD|`INTVAR_MOD`]]), [[vcirc.f#VCIRC|`VCIRC`]] (`THDIFM`, `VISCM`), [[rotmix.f#ROTMIX|`ROTMIX`]] (`DELM`), [[rotgrid.f#ROTGRID|`ROTGRID`]] and [[mixgrid.f#MIXGRID|`MIXGRID`]] (`EPSM`), and [[liburn.f#LIBURN|`LIBURN`]], [[liburn2.f#LIBURN2|`LIBURN2`]] (`DELAM`, `DELRM`, to find the convective boundary); MIDMOD itself uses `DELAM` − `DELRM` to decide whether a shell that changes state over the step is convective.
- `VELM`: the convective velocity, interpolated where the shell keeps its state, the larger of the two where it becomes convective, 0 where it becomes radiative; read nowhere.
- `AMUM`: the mean molecular weight, set by MIDMOD, by [[checkc.f#CHECKC|`CHECKC`]] (from the new composition) and [[getw.f#GETW|`GETW`]] (corrected for the change over the step); read by `SETUPV` and `VCIRC` (the μ-gradient terms).

**Design.** A blanket `USE MDPHY_MOD`. At `rp_1`, [[codiff.f#CODIFF|`CODIFF`]] and [[mixcz.f#MIXCZ|`MIXCZ`]] also declared the block; they no longer do.

**Changed since `rp_1`.** New file: `COMMON/MDPHY/` as a module.

## Questions for the experts

1. **An unused result.** `VELM` is set by MIDMOD and read nowhere. Is the convective velocity at mid-step still needed?
