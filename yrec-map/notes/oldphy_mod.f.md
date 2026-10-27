## Explanation

**Purpose.** `OLDPHY_MOD` holds physical quantities of the model at the start of the step, which [[midmod.f#MIDMOD|`MIDMOD`]] interpolates against the new model for the rotational-mixing substeps, shared by [[hpoint.f#HPOINT|`HPOINT`]], `MIDMOD` and [[getw.f#GETW|`GETW`]]. It replaces `COMMON/OLDPHY/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]]. All members are arrays of `JSON`.

**What its variables hold, who sets them, who reads them.** `HPOINT` saves them after it has remapped the model ("for diffusion store the auxiliary quantities needed to calculate velocities at the start of the timestep with the new point distribution"):
- `DELRO`, `DELO`, `DELAO`: the radiative, actual and adiabatic gradients (`SDEL(1..3)`); `AMUO` (mean molecular weight), `OO` (opacity), `CPO` ($c_P$), `QDTO`, `VELO` (convective velocity), `VISCO` (viscosity), `THDIFO` (thermal diffusivity).
- `ESUMO`, `EPSO`: the energy generation, without and with the `SEG(6)`, `SEG(7)` terms, interpolated by HPOINT onto the new grid ("MHP 6/00").
- All are read by `MIDMOD`, which forms the mid-step values of [[mdphy_mod.f#MDPHY_MOD|`MDPHY_MOD`]] from them; `GETW` reads `AMUO` (the change of μ over the step).

**Design.** A blanket `USE OLDPHY_MOD`. HPOINT also uses `DELAO` − `DELO` for `DDELM` in [[oldrot2_mod.f#OLDROT2_MOD|`OLDROT2_MOD`]].

**Changed since `rp_1`.** New file: `COMMON/OLDPHY/` as a module.
