## Explanation

**Purpose.** `NEWRAT_MOD` holds the proton-capture rates of ⁶Li, ⁷Li and ⁹Be at each shell for the current model, shared by 5 routines. It replaces `COMMON/NEWRAT/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](dimensions_mod.f.md#dimensions_mod). The rates at the start of the step are in [`OLDRAT_MOD`](oldrat_mod.f.md#oldrat_mod).

**What its variables hold, who sets them, who reads them.** All are arrays of `JSON`.
- `RLI6`, `RLI7`, `RBE9`: the rates (the Caughlan–Fowler fit times $`\rho X`$, scaled by the user factors `SLI6`, `SLI7`, `SBE91`–`SBE93`), set by [`LIRATE88`](lirate88.f.md#lirate88) when called with `J` = 1, and zero above the burning region. [`LIBURN`](liburn.f.md#liburn) and [`LIBURN2`](liburn2.f.md#liburn2) read them to burn the light elements, and adjust the value at the base of the convection zone by interpolation (`0.5*FX` toward the shell below).
- [`GETW`](getw.f.md#getw) and [`BURSMIX`](bursmix.f.md#bursmix) copy them into the start-of-step rates of `OLDRAT_MOD` for the next step.

**Design.** A blanket `USE NEWRAT_MOD`.

**Changed since `rp_1`.** New file: `COMMON/NEWRAT/` as a module.
