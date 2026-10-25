## Explanation

**Purpose.** This file checks each iteration of angular-momentum transport. Its header lists five tasks: catch negative specific angular momentum $j = J/M$; test convergence of the iteration on the diffusion coefficients; compute $\Omega$ (and the moment of inertia) from the new $j$; remove reversals of the $\Omega$ gradient by imposing solid-body rotation locally; and print details.

**How it fits.**
- **Inputs:** the arguments, the model (`HD`, `HR`, `HS`, `HS2`, `LCZ`), `HJM` ($j$ after this iteration), `HJMP` ($j$ after the previous iteration), `HJMSAV` ($j$ at the start of the step), `IT`, `LOKAD`; `DJOK`, `ITDIF2` from `/DIFUS/`; `WOLD` ($\Omega$ of the previous model) from `/OLDROT/`; `TOLERI` (`/ERRMOM/`) and `ACFPFT` (`/ROT/`), the tolerances of the moment-of-inertia iteration.
- **Who calls it:** [[seculr.f#SECULR|SECULR]].
- **What it calls:** [[getrot.f#GETROT|GETROT]] ($\Omega$, moment of inertia $I$ and $\partial I/\partial\Omega$ from $j$) and [[solid.f#SOLID|SOLID]] (solid-body rotation over a range of shells).
- **Outputs:** `OMEGA`, `HI`, `QIW`, `ETA2`, `R0`, `HJMP` (set to `HJM`), `LOK`, `LREDO`, `DT`, `IREDO`.
- **COMMON blocks:** `/CCOUT1/`, `/TEMP2/`, `/QUADD/`, `/EGRID/`, `/DIFAD/`, `/DIFAD2/`, `/VARFC/` are used only in the detailed print, which is now switched off (see Design).

**The method.**
1. If $j \le 0$ anywhere, stop (see question 1).
2. **Convergence:** $\delta_\mathrm{it} = \max_i |j_i - j_i^\mathrm{prev}|/j_i^\mathrm{prev}$; converged (`LOK`) if $\delta_\mathrm{it} \le$ `DJOK`. If `LOKAD` is set on entry, `LOK` starts true.
3. **$\Omega$ from $j$:** call GETROT. Before the last iteration and while not converged, the tolerances `TOLERI` and `ACFPFT` are relaxed to $\max(10^{-2}\,\mathrm{DJOK}, \text{tolerance})$, "because the error in the diffusion is of order DJOK", and restored after.
4. **Gradient reversals:** from the surface inward, where $\Omega_i - \Omega_{i-1}$ is positive (by more than 1, see question 2) but was not positive in the previous model (`WOLD`), mix the two shells (and any adjacent convection zone) to solid-body rotation with SOLID; then widen the range while the boundaries show new reversals.
5. **Print** at the last iteration or on convergence: the largest $\Delta j/j$ over the step, and $\delta$ of each iteration.

**Design.** The detailed output to `IMODPT` is switched off by `IF(.TRUE.)GOTO 240` (G. Somers 11/14: "this can be trivially extracted from the extended .STORE file"), so more than 60 lines below it never run.

**KC's changes.** 2025-05-31: the unused argument `LPRT` removed.

## Questions for the experts

1. **No time-step cut.** The test `IF(IREDO.GT.0)` (replacing the commented-out `IREDO.GT.3`) stops the run at the first negative $j$, so the branch that halves the time step never runs, while the message still says "3 attempts at cutting timestep failed". Which is intended?
2. **The threshold of the reversal test.** The first test is `OMEGA(I)-OMEGA(I-1).GT.1.0d0`, an increase of 1 rad s$^{-1}$, which is far larger than any stellar $\Omega$; the later tests use $10^{-15}$. With 1.0 the reversal correction practically never fires. Is `1.0D-15` meant?
3. **Array bounds.** `DELJI(16)` and `IMAXI(16)` are indexed by the iteration `IT`; if `ITDIF2` exceeds 16, they overflow.
4. **Dead output.** Can the switched-off print (and the COMMON blocks it alone needs) be removed in the overhaul?

### CHECKJ

Checks one iteration of angular-momentum diffusion: stops on $j \le 0$, tests convergence against `DJOK`, gets $\Omega$ from $j$ ([[getrot.f#GETROT|GETROT]]), and removes $\Omega$-gradient reversals with [[solid.f#SOLID|SOLID]].
