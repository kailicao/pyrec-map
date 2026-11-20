## Explanation

**Purpose.** `OLDRAT_MOD` holds the proton-capture rates of ⁶Li, ⁷Li, and ⁹Be at each shell for the model at the start of the step, shared by 5 routines; the current model's rates are in [`NEWRAT_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/newrat_mod.f#L19-L32). It replaces `COMMON/OLDRAT/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/dimensions_mod.f#L38-L44).

**What its variables hold, who sets them, who reads them.** All are arrays of `JSON`.
- `RLI60`, `RLI70`, `RBE90`: set by [`LIRATE88`](lirate88.f.md#lirate88) when called with `J` = 2 (by the [main program](main.f.md#file-level), from the old model: `HTO`, `HDO`, `HCOMPP`), and copied from `RLI6`, `RLI7`, `RBE9` by [`GETW`](getw.f.md#getw) after each of its substeps and by [`BURSMIX`](bursmix.f.md#bursmix), as the starting rates of the next.
- Read by [`LIBURN`](liburn.f.md#liburn) and [`LIBURN2`](liburn2.f.md#liburn2), which burn with the rates at both ends of the step.

**Design.** A blanket `USE OLDRAT_MOD`.

**Changed since `rp_1`.** New file: `COMMON/OLDRAT/` as a module.
