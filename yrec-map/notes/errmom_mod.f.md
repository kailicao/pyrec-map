## Explanation

**Purpose.** `ERRMOM_MOD` holds `TOLERI`, the relative tolerance of the iteration for the moment of inertia and the surface rotation rate, shared by [[checkj.f#CHECKJ|`CHECKJ`]] and [[solid.f#SOLID|`SOLID`]]. It replaces `COMMON/ERRMOM/` (MHP via Claude, 10/14/26).

**What its variable holds, who sets it, who reads it.**
- `TOLERI` (`REAL*8`): nothing in the code gives it a first value (no namelist, `DATA` statement or assignment), so it starts at zero in practice. `CHECKJ` relaxes it to at least `DJOK`/100 around its call to [[getrot.f#GETROT|`GETROT`]] in the early iterations and then restores it. `SOLID` iterates the surface $\Omega$ until the angular momentum of the convection zone matches within `TOLERI` (at most 20 tries).

**Design.** A blanket `USE ERRMOM_MOD`. The tolerance reaches GETROT's callees through the module rather than as an argument.

**Changed since `rp_1`.** New file: `COMMON/ERRMOM/` as a module.

## Questions for the experts

1. **A tolerance with no value.** `TOLERI` is set nowhere except CHECKJ's temporary relaxation, so outside it SOLID compares with zero and runs its 20 tries (so also at `rp_1`). Where should its value come from?
