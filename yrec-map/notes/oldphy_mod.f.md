## Explanation

**Purpose.** `OLDPHY_MOD` holds physical quantities of the model at the start of the step, which [`MIDMOD`](https://github.com/yreclab/yrec/blob/7be4133/src/midmod.f#L2-L523) interpolates against the new model for the rotational-mixing substeps, shared by [`HPOINT`](hpoint.f.md#hpoint), `MIDMOD`, and [`GETW`](getw.f.md#getw). It replaces `COMMON/OLDPHY/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/dimensions_mod.f#L38-L44). All members are arrays of `JSON`.

**What its variables hold, who sets them, who reads them.** `HPOINT` saves them after it has remapped the model ("for diffusion store the auxiliary quantities needed to calculate velocities at the start of the timestep with the new point distribution"):
- `DELRO`, `DELO`, `DELAO`: the radiative, actual, and adiabatic gradients (`SDEL(1..3)`); `AMUO` (mean molecular weight), `OO` (opacity), `CPO` ($`c_P`$), `QDTO`, `VELO` (convective velocity), `VISCO` (viscosity), `THDIFO` (thermal diffusivity).
- `ESUMO`, `EPSO`: the energy generation, without and with the `SEG(6)`, `SEG(7)` terms, interpolated by HPOINT onto the new grid ("MHP 6/00").
- All are read by `MIDMOD`, which forms the mid-step values of [`MDPHY_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/mdphy_mod.f#L19-L41) from them; `GETW` reads `AMUO` (the change of $`\mu`$ over the step).

**Design.** A blanket `USE OLDPHY_MOD`. Until `a8a5950`, HPOINT also stored `DELAO` − `DELO` in `DDELM` ([`OLDROT2_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/oldrot2_mod.f#L19-L38)); it no longer does, since SETUPV overwrites `DDELM` before VCIRC reads it (hpoint.f's comment, 10/30/26).

**Changed since `rp_1`.** New file: `COMMON/OLDPHY/` as a module.
