## Explanation

**Purpose.** `GRAVEZ_MOD` holds the metals ($`Z`$) on the equally spaced radial grid of the older settling routine [`GRSETT`](grsett.f.md#grsett), with their diffusion coefficients at the grid's points and midpoints, used with metal diffusion (`LDIFZ`). Shared by 5 routines. It replaces `COMMON/GRAVEZ/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](dimensions_mod.f.md#dimensions_mod).

**What its variables hold, who sets them, who reads them.**
- `EZ(JSON)`: $`Z`$ at the grid points, interpolated from the model by [`MODEL_TO_EQUAL`](model_to_equal.f.md#model_to_equal), advanced by [`LAX_WENDROF2`](lax_wendrof2.f.md#lax_wendrof2), and turned into the change over the step by `GRSETT` (`EZ - EZ_ORIG`), which [`EQUAL_TO_MODEL`](equal_to_model.f.md#equal_to_model) applies to the model's points.
- `EZ_H(JSON)`: $`Z`$ at the midpoints, set by `MODEL_TO_EQUAL` and by [`LAX_WENDROF1`](lax_wendrof1.f.md#lax_wendrof1) (the half step); read by `GRSETT`.
- `ECOD1Z(JSON)`: the settling coefficient at the grid points, set by `MODEL_TO_EQUAL`, read by `LAX_WENDROF1`.
- `ECOD1Z_H(JSON)`: the settling coefficient at the midpoints, set by `MODEL_TO_EQUAL` and updated by `GRSETT` with the half-step abundances (`ECOD1Z_H + EZ_H*EQCOD1Z_H`); read by `LAX_WENDROF2`.
- `EQCOD1Z_H(JSON)`: the abundance-dependent part of that coefficient, set by `MODEL_TO_EQUAL`, read by `GRSETT`.
- `ECOD2Z_H`, `EQCOD2Z_H` (`JSON` each): the diffusion coefficient and its abundance-dependent part at the midpoints, set by `MODEL_TO_EQUAL` ([model_to_equal.f, lines 105–107](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L105-L107); [model_to_equal.f, lines 180–187](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L180-L187)); read nowhere (unused?), since the metals get only the explicit settling term (see GRSETT's notes).

**Design.** A blanket `USE GRAVEZ_MOD`. The hydrogen counterparts (`EX`, `ECOD1`, …) are arguments of the same routines; only the metals go through the module.

**Changed since `rp_1`.** New file: `COMMON/GRAVEZ/` as a module.
