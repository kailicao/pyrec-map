## Explanation

**Purpose.** This file limits the time step so that the surface changes from one model to the next stay within the envelope "triangle": the changes of $\log T_\mathrm{eff}$ and $\log L$ must not exceed the triangle's size, so that the surface boundary condition is not extrapolated far outside the envelope integrations.

**How it fits.**
- **Inputs:** the arguments `DELTS` (the previous step), `HL` (luminosity), `TEFFL`, `M`; the previous model's `HLO`, `MO`, `TEFFLO` (`/OLDMOD/`); the triangle's sizes `TRIDT`, `TRIDL` (`/CENV/`); the limit `ATIME(13)` (`/CTLIM/`).
- **Who calls it:** [[htimer.f#HTIMER|HTIMER]], which sets the next time step.
- **Output:** `EDELT`, the time step this criterion allows.

**The method.**
$$f = \max\left(\frac{|\Delta\log T_\mathrm{eff}|}{\Delta T_\mathrm{tri}}, \frac{|\Delta\log L|}{\Delta L_\mathrm{tri}}\right), \qquad f \leftarrow \min\!\left(\max\left(f, \frac{1}{a}\right), a\right), \qquad \mathtt{EDELT} = \frac{\Delta t}{f},$$
with $a$ = `ATIME(13)`, the largest factor by which the step may change; $f = 1$ if nothing changed.

## Questions for the experts

1. **Dead declarations.** `HMAX(1:2)` is filled but never used; the many COMMON blocks except `/CTLIM/`, `/OLDMOD/` and `/CENV/` are unused. Harmless.
2. **The comment.** It speaks of "changes in P, T, R, L", but only $T_\mathrm{eff}$ and $L$ are tested.

### ENTIME

Time step from the envelope triangle: scales the last step so that $\Delta\log T_\mathrm{eff}$ and $\Delta\log L$ stay within the triangle, by a factor bounded by `ATIME(13)`.
