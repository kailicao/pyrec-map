## Explanation

**Purpose.** `BURN_MOD` holds one array, `HCOMPM(15,JSON)`, a copy of the composition (or of its changes) passed between the mixing routines. It replaces `COMMON/BURN/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**Who sets it, who reads it.** [[mix.f#MIX|`MIX`]] copies the fifteen arrays `HR1`…`HF2` into it, and [[rotmix.f#ROTMIX|`ROTMIX`]] copies them back; [[hpoint.f#HPOINT|`HPOINT`]] interpolates it onto the new grid when points are added or removed.

**Changed since `rp_1`.** New file: `COMMON/BURN/` as a module.
