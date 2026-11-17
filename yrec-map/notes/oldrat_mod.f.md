## Explanation

**Purpose.** `OLDRAT_MOD` holds the proton-capture rates of ⁶Li, ⁷Li and ⁹Be at each shell for the model at the start of the step, shared by 5 routines; the current model's rates are in [`NEWRAT_MOD`](newrat_mod.f.md#newrat_mod). It replaces `COMMON/OLDRAT/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](dimensions_mod.f.md#dimensions_mod).

**What its variables hold, who sets them, who reads them.** All are arrays of `JSON`.
- `RLI60`, `RLI70`, `RBE90`: set by [`LIRATE88`](lirate88.f.md#lirate88) when called with `J` = 2 (from the old model), and copied from `RLI6`, `RLI7`, `RBE9` by [`GETW`](getw.f.md#getw) and [`BURSMIX`](bursmix.f.md#bursmix) at the end of a step, for the next.
- Read by [`LIBURN`](liburn.f.md#liburn) and [`LIBURN2`](liburn2.f.md#liburn2), which burn with the rates at both ends of the step.

**Design.** A blanket `USE OLDRAT_MOD`.

**Changed since `rp_1`.** New file: `COMMON/OLDRAT/` as a module.
