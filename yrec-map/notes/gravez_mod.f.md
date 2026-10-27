## Explanation

**Purpose.** `GRAVEZ_MOD` holds the metals ($Z$) on the equally spaced radial grid of the older settling routine [[grsett.f#GRSETT|`GRSETT`]], with their diffusion coefficients at the grid's points and midpoints, used with metal diffusion (`LDIFZ`). Shared by 5 routines. It replaces `COMMON/GRAVEZ/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]].

**What its variables hold, who sets them, who reads them.**
- `EZ(JSON)`: $Z$ at the grid points, interpolated from the model by [[model_to_equal.f#MODEL_TO_EQUAL|`MODEL_TO_EQUAL`]], advanced by [[lax_wendrof2.f#LAX_WENDROF2|`LAX_WENDROF2`]], and turned into the change over the step by `GRSETT` (`EZ - EZ_ORIG`), which [[equal_to_model.f#EQUAL_TO_MODEL|`EQUAL_TO_MODEL`]] applies to the model's points.
- `EZ_H(JSON)`: $Z$ at the midpoints, set by `MODEL_TO_EQUAL` and by [[lax_wendrof1.f#LAX_WENDROF1|`LAX_WENDROF1`]] (the half step); read by `GRSETT`.
- `ECOD1Z(JSON)`: the settling coefficient at the grid points, set by `MODEL_TO_EQUAL`, read by `LAX_WENDROF1`.
- `ECOD1Z_H(JSON)`: the settling coefficient at the midpoints, set by `MODEL_TO_EQUAL` and updated by `GRSETT` with the half-step abundances (`ECOD1Z_H + EZ_H*EQCOD1Z_H`); read by `LAX_WENDROF2`.
- `EQCOD1Z_H(JSON)`: the abundance-dependent part of that coefficient, set by `MODEL_TO_EQUAL`, read by `GRSETT`.
- `ECOD2Z_H`, `EQCOD2Z_H` (`JSON` each): the diffusion coefficient and its abundance-dependent part at the midpoints, set by `MODEL_TO_EQUAL`; read nowhere, since the metals get only the explicit settling term (see GRSETT's notes).

**Design.** A blanket `USE GRAVEZ_MOD`. The hydrogen counterparts (`EX`, `ECOD1`, …) are arguments of the same routines; only the metals go through the module.

**Changed since `rp_1`.** New file: `COMMON/GRAVEZ/` as a module.
