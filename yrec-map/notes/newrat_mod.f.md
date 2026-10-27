## Explanation

**Purpose.** `NEWRAT_MOD` holds the proton-capture rates of ⁶Li, ⁷Li and ⁹Be at each shell for the current model, shared by 5 routines. It replaces `COMMON/NEWRAT/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]]. The rates at the start of the step are in [[oldrat_mod.f#OLDRAT_MOD|`OLDRAT_MOD`]].

**What its variables hold, who sets them, who reads them.** All are arrays of `JSON`.
- `RLI6`, `RLI7`, `RBE9`: the rates (the Caughlan–Fowler fit times $\rho X$, scaled by the user factors `SLI6`, `SLI7`, `SBE91`–`SBE93`), set by [[lirate88.f#LIRATE88|`LIRATE88`]] when called with `J` = 1, and zero above the burning region. [[liburn.f#LIBURN|`LIBURN`]] and [[liburn2.f#LIBURN2|`LIBURN2`]] read them to burn the light elements, and adjust the value at the base of the convection zone by interpolation (`0.5*FX` toward the shell below).
- [[getw.f#GETW|`GETW`]] and [[bursmix.f#BURSMIX|`BURSMIX`]] copy them into the start-of-step rates of `OLDRAT_MOD` for the next step.

**Design.** A blanket `USE NEWRAT_MOD`.

**Changed since `rp_1`.** New file: `COMMON/NEWRAT/` as a module.
