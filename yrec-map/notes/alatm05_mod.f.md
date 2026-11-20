## Explanation

**Purpose.** `ALATM05_MOD` holds the Allard table's own first and last $`\log T_\mathrm{eff}`$, `AL_TEFFLmin` and `AL_TEFFLmax`. It replaces `COMMON/ALATM05/` (MHP via Claude, 10/14/26).

**Who sets them, who reads them.** Both are set by [`ALTABINIT`](altabinit.f.md#altabinit); [`SURFBC`](surfbc.f.md#surfbc) reads `AL_TEFFLmax` to decide when to switch from the Allard atmospheres to the gray one, and back. `AL_TEFFLmin` is read nowhere.

**Changed since `rp_1`.** New file: `COMMON/ALATM05/` as a module.
