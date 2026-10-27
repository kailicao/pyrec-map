## Explanation

**Purpose.** `DWMAX_MOD` holds the critical rotation gradient for the shear instability at each shell, and its value at the start of the step, shared by [[physic.f#PHYSIC|`PHYSIC`]] and [[hpoint.f#HPOINT|`HPOINT`]]. It replaces `COMMON/DWMAX/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]].

**What its variables hold, who sets them, who reads them.**
- `QWRMAX(JSON)`: the critical $d\Omega/d\ln r$ (Endal and Sofia 1978, as PHYSIC's comments cite), set by `PHYSIC` for the interface between shells `IM-1` and `IM`: 0 where both shells are convective or the root is not real. Read only by `HPOINT`, to copy it.
- `QWRMX0(JSON)`: the start-of-step copy, made by `HPOINT` when it saves the old model; read nowhere.

**Design.** A blanket `USE DWMAX_MOD`. [[seculr.f#SECULR|`SECULR`]] has a local array of the same name, `QWRMAX`, which [[setupv.f#SETUPV|`SETUPV`]] fills for the angular momentum transport; it is not this module's. At `rp_1`, [[midmod.f#MIDMOD|`MIDMOD`]] also declared the block without using it.

**Changed since `rp_1`.** New file: `COMMON/DWMAX/` as a module (MIDMOD's unused declaration dropped).

## Questions for the experts

1. **A result no one uses.** PHYSIC computes `QWRMAX` at every shell, but the module's copy is read only by HPOINT, to save it in `QWRMX0`, which is read nowhere (so also at `rp_1`). Is the computation in PHYSIC still needed, or was it meant to reach SECULR's own `QWRMAX`?
