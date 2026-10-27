## Explanation

**Purpose.** `OLDRAT_MOD` holds the proton-capture rates of ⁶Li, ⁷Li and ⁹Be at each shell for the model at the start of the step, shared by 5 routines; the current model's rates are in [[newrat_mod.f#NEWRAT_MOD|`NEWRAT_MOD`]]. It replaces `COMMON/OLDRAT/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]].

**What its variables hold, who sets them, who reads them.** All are arrays of `JSON`.
- `RLI60`, `RLI70`, `RBE90`: set by [[lirate88.f#LIRATE88|`LIRATE88`]] when called with `J` = 2 (from the old model), and copied from `RLI6`, `RLI7`, `RBE9` by [[getw.f#GETW|`GETW`]] and [[bursmix.f#BURSMIX|`BURSMIX`]] at the end of a step, for the next.
- Read by [[liburn.f#LIBURN|`LIBURN`]] and [[liburn2.f#LIBURN2|`LIBURN2`]], which burn with the rates at both ends of the step.

**Design.** A blanket `USE OLDRAT_MOD`.

**Changed since `rp_1`.** New file: `COMMON/OLDRAT/` as a module.
