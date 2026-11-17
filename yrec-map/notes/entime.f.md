## Explanation

**Purpose.** This file limits the time step so that the surface changes from one model to the next stay within the envelope "triangle": the changes of $`\log T_\mathrm{eff}`$ and $`\log L`$ must not exceed the triangle's size, so that the surface boundary condition is not extrapolated far outside the envelope integrations.

**How it fits.**
- **Inputs:** the arguments `DELTS` (the previous step), `HL` (luminosity), `TEFFL`, `M`; the previous model's surface luminosity `HLSURO` and `TEFFLO` ([`OLDMOD_MOD`](oldmod_mod.f.md#oldmod_mod), saved by [HPOINT](hpoint.f.md#hpoint) before the rezoning, and by main.f and STARIN); the settings `TRIDT`, `TRIDL` (the triangle's sizes, formerly `/CENV/`) and `ATIME(13)` (the limit, formerly `/CTLIM/`), from [`NMLPAR_MOD`](nmlpar_mod.f.md#nmlpar_mod).
- **Who calls it:** [HTIMER](htimer.f.md#htimer), which sets the next time step.
- **Output:** `EDELT`, the time step this criterion allows.

**The method.**
```math
f = \max\left(\frac{|\Delta\log T_\mathrm{eff}|}{\Delta T_\mathrm{tri}}, \frac{|\Delta\log L|}{\Delta L_\mathrm{tri}}\right), \qquad f \leftarrow \min\!\left(\max\left(f, \frac{1}{a}\right), a\right), \qquad \mathtt{EDELT} = \frac{\Delta t}{f},
```
with $`a`$ = `ATIME(13)`, the largest factor by which the step may change; $`f = 1`$ if nothing changed. A previous step of 0 thus gives `EDELT` = 0, which HTIMER does not catch ([htimer.f, suspected bug 1](htimer.f.md#b1)). The triangle's sizes are also copied into `HMAX(1:2)`, which nothing reads (unused?). The header's output line, "time step for requested change in P,T,R,L," is copied from [PTIME](ptime.f.md#ptime): Only $`T_\mathrm{eff}`$ and $`L`$ are tested here (settled from the code, Nov 9, 2026: [line 68](https://github.com/yreclab/yrec/blob/7be4133/src/entime.f#L68); [lines 73–95](https://github.com/yreclab/yrec/blob/7be4133/src/entime.f#L73-L95)).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`; the unused COMMON blocks are gone, which settles that half of former question 1.

**Changed since `a8a5950`.** $`\Delta\log L`$ is taken against the saved surface luminosity `HLSURO` instead of `HLO(MO)`: HPOINT re-splines `HLO` onto the new mesh, so `HLO(MO)` was an interior point or a stale entry whenever the number of points changed (this settles HPOINT's former question 6).

### ENTIME

Time step from the envelope triangle: scales the last step so that $`\Delta\log T_\mathrm{eff}`$ and $`\Delta\log L`$ stay within the triangle, by a factor bounded by `ATIME(13)`.
