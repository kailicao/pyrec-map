## Explanation

**Purpose.** This file checks each iteration of angular-momentum transport. Its header lists five tasks: catch negative specific angular momentum $j = J/M$; test convergence of the iteration on the diffusion coefficients; compute $\Omega$ (and the moment of inertia) from the new $j$; remove reversals of the $\Omega$ gradient by imposing solid-body rotation locally; and print details.

**How it fits.**
- **Inputs:** the arguments, the model (`HD`, `HR`, `HS`, `HS2`, `LCZ`), `HJM` ($j$ after this iteration), `HJMP` ($j$ after the previous iteration), `HJMSAV` ($j$ at the start of the step), `IT`, `LOKAD`; `DJOK`, `ITDIF2` (which also sizes the per-iteration history `DELJI`, `IMAXI`) from [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]]; `WOLD` ($\Omega$ of the previous model) from [[oldrot_mod.f#OLDROT_MOD|`OLDROT_MOD`]]; `TOLERI` ([[errmom_mod.f#ERRMOM_MOD|`ERRMOM_MOD`]]) and `ACFPFT` (`NMLPAR_MOD`), the tolerances of the moment-of-inertia iteration.
- **Who calls it:** [[seculr.f#SECULR|SECULR]].
- **What it calls:** [[getrot.f#GETROT|GETROT]] ($\Omega$, moment of inertia $I$ and $\partial I/\partial\Omega$ from $j$) and [[solid.f#SOLID|SOLID]] (solid-body rotation over a range of shells).
- **Outputs:** `OMEGA`, `HI`, `QIW`, `ETA2`, `R0`, `HJMP` (set to `HJM`), `LOK`, `LREDO`, `DT`, `IREDO`.
- **Modules:** `TEMP2_MOD`, `QUADD_MOD`, `EGRID_MOD`, `DIFAD_MOD`, `DIFAD2_MOD`, and from `NMLPAR_MOD` `NPRTPT` and `LDIFAD`, are used only in the detailed print, which is now switched off (see Design).

**The method.**
1. If $j \le 0$ anywhere, stop with exit status 1. The branch that would halve the time step instead ([[#L160-L167]]) never runs (unused?).

    > **Question** ([[#L149-L159]]). **No time-step cut.** The test `IF(IREDO.GT.0)` (replacing the commented-out `IREDO.GT.3`) stops the run at the first negative $j$, so the branch that halves the time step never runs, while the message still says "3 attempts at cutting timestep failed". Which is intended: the stop at once (and the message corrected), or up to three cuts?

2. **Convergence:** $\delta_\mathrm{it} = \max_i |j_i - j_i^\mathrm{prev}|/j_i^\mathrm{prev}$; converged (`LOK`) if $\delta_\mathrm{it} \le$ `DJOK`. If `LOKAD` is set on entry, `LOK` starts true.
3. **$\Omega$ from $j$:** call GETROT. Before the last iteration and while not converged, the tolerances `TOLERI` and `ACFPFT` are relaxed to $\max(10^{-2}\,\mathrm{DJOK}, \text{tolerance})$, "because the error in the diffusion is of order DJOK", and restored after.
4. **Gradient reversals:** from the surface inward, where $\Omega_i - \Omega_{i-1}$ is positive (by more than $10^{-15}$) but was not positive in the previous model (`WOLD`), mix the two shells (and any adjacent convection zone) to solid-body rotation with SOLID; then widen the range while the boundaries show new reversals.
5. **Print** at the last iteration or on convergence: the largest $\Delta j/j$ over the step, and $\delta$ of each iteration.

**Design.** The detailed output to `IMODPT` is switched off by `IF(.TRUE.)GOTO 240` (G. Somers 11/14: "this can be trivially extracted from the extended .STORE file"), so more than 60 lines below it never run ([[#L326-L401]]; unused?, with the modules only they need).

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html): `DJOK` (default 1.0D-4) is the numerical tolerance of rotational mixing; `ITDIF2` (1) the number of iterations between nuclear burning and rotational mixing (1 = none). [Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html): `NPRTPT` writes details for every `NPRTPT`-th point. The per-shell file `FMODPT` is "no longer used"; CHECKJ's writes to it are skipped (`IF(.TRUE.)GOTO 240`), though PARMIN still opens it.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

**Changed since `a8a5950`.** The reversal search enters at $\Omega_i - \Omega_{i-1} > 10^{-15}$ rad s$^{-1}$ instead of 1 (settles former question 2); `DELJI` and `IMAXI` are `SAVE`d allocatable arrays sized $\max(\mathrm{ITDIF2}, \mathrm{IT}, 1)$ instead of 16 (settles former question 3); the stop on $j \le 0$ is `STOP 1` (`KNOWN_ISSUES.md`, issue 38).

### CHECKJ

Checks one iteration of angular-momentum diffusion: stops on $j \le 0$, tests convergence against `DJOK`, gets $\Omega$ from $j$ ([[getrot.f#GETROT|GETROT]]), and removes $\Omega$-gradient reversals with [[solid.f#SOLID|SOLID]].
