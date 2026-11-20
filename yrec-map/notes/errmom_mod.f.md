## Explanation

**Purpose.** `ERRMOM_MOD` holds `TOLERI`, the relative tolerance of the iteration for the moment of inertia and the surface rotation rate, shared by [`CHECKJ`](checkj.f.md#checkj) and [`SOLID`](solid.f.md#solid). It replaces `COMMON/ERRMOM/` (MHP via Claude, 10/14/26).

**What its variable holds, who sets it, who reads it.**
- `TOLERI` (`REAL*8`): $`10^{-12}`$, its initial value in the module (no namelist sets it). `CHECKJ` relaxes it to at least `DJOK`/100 around its call to [`GETROT`](getrot.f.md#getrot) in the early iterations and then restores it. `SOLID` iterates the surface $`\Omega`$ until the angular momentum of the convection zone matches within `TOLERI` (at most 20 tries).

**Design.** A blanket `USE ERRMOM_MOD`. The tolerance reaches GETROT's callees through the module rather than as an argument.

**Changed since `rp_1`.** New file: `COMMON/ERRMOM/` as a module.

**Changed since `a8a5950`.** `TOLERI` is given a value, $`10^{-12}`$: Nothing set it before, so SOLID's tolerance was 0 and every call ran all 20 Newton passes. This answers the question of where `TOLERI`'s value should come from, which this page asked before the change.
