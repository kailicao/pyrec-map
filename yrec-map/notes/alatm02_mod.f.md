## Explanation

**Purpose.** `ALATM02_MOD` holds the valid range of the Allard table, shared by 3 routines. It replaces `COMMON/ALATM02/` (MHP via Claude, 10/14/26); the size `NTA` = 250 is private.

**What its variables hold, who sets them, who reads them.** Set by [`ALTABINIT`](altabinit.f.md#altabinit):
- `GLmin(NTA)`, `GLmax(NTA)`, `IGLmin(NTA)`, `IGLmax(NTA)`: for each $`\log T_\mathrm{eff}`$ row, the allowed range in $`\log g`$ and the first and last valid column;
- `TEFFLmin`, `TEFFLmax`: the range in $`\log T_\mathrm{eff}`$ (recomputed, with the same formulas, by [`ALPRINT`](alprint.f.md#alprint));
- `GLXmin`, `GLXmax`: the extremes of $`\log g`$ over all rows.

Read by [`ALSURFP`](alsurfp.f.md#alsurfp), which checks each request against them, and `ALPRINT`.

**Changed since `rp_1`.** New file: `COMMON/ALATM02/` as a module.
