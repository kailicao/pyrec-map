## Explanation

**Purpose.** This file solves the transport of angular momentum by rotational instabilities over one time step when advection by meridional circulation is included (the option `LDIFAD`, "combined diffusion/advection equation", MHP 06/02). Since the circulation velocity depends on $\Omega$ and its first three radial derivatives, it writes the problem as four first-order equations per shell and solves the resulting band system with [[bandw.f#BANDW|BANDW]]. It also returns the coefficient of composition mixing that results.

**How it fits.**
- **Inputs:** the arguments `DR` (the even grid's spacing), `DT` (time step), `EI` (moment of inertia of each grid point), `EW` ($\Omega$ at the start), `NTOT`, `WIND1`, `WIND2` (the wind's change of $\Omega$ at the start and end of the step, from [[cowind.f#COWIND|COWIND]] or [[mwind.f#MWIND|MWIND]] via the caller), `LFIX` (hold the surface $\Omega$ fixed). From modules: the velocity coefficients of the circulation and instabilities (`EV0`, `EV1A`, `EV1B`, `EV2A`, `EV2B`, `ECOD5`, `ECOD6`, `FGEOM`, `ESS`, `EGSF` in [[difad3_mod.f#DIFAD3_MOD|`DIFAD3_MOD`]]; `EQQCOD`, `EQQQCOD` in [[egridder_mod.f#EGRIDDER_MOD|`EGRIDDER_MOD`]]), set up by [[setupv.f#SETUPV|SETUPV]] and [[vcirc.f#VCIRC|VCIRC]]; from [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]], the multipliers `FW`, `FC`, `FESC`, `FSSC`, `FGSFC` (formerly `/VMULT/`, `/VMULT2/`), `DJOK`, `ITDIF2` (formerly `/DIFUS/`), `WMAX`, `EXW` (formerly `/CWIND/`) and `LROSSBY`, `PMMSOLTAU` (the Rossby scaling of the saturation); `TAUCZ` in [[ovrtrn_mod.f#OVRTRN_MOD|`OVRTRN_MOD`]]. `QCHIRE` (formerly `/EGRIDCHI/`), `EWST`, `EQWRST` (formerly `/DIFADDT/`), `REQ` and `FGEOMIX` (formerly `/DIFAD4/`) are now local saved arrays, since those COMMON blocks were declared in no other file.
- **Who calls it:** [[seculr.f#SECULR|SECULR]], for each unstable region when `LDIFAD` is on (otherwise [[dcoeft.f#DCOEFT|DCOEFT]] sets up a tridiagonal diffusion system).
- **What it calls:** [[bandw.f#BANDW|BANDW]].
- **Outputs:** `DJ` (the change of angular momentum of each point), `SUMDJ` (their sum), `LOKAD` (converged), `ECOD2` (the composition diffusion coefficient); `ECOD3`, `ECOD4` in [[difad_mod.f#DIFAD_MOD|`DIFAD_MOD`]] (read by [[checkj.f#CHECKJ|CHECKJ]] for printing); `VESN`, now a local array (`/DIFAD4/` was read nowhere else). Many lines to the screen.

**The equation.** In the comment's words, the diffusion part is
$$\frac{\partial\Omega}{\partial t} = \frac{1}{4\pi\rho r^2}\,\frac{1}{I/M}\,\frac{\partial}{\partial r}\left(D\,\frac{\partial\Omega}{\partial r}\right),$$
and `LDIFAD` adds an advective term $\partial_r(\rho r^4 V\Omega)$, with $V$ a function of $\Omega$, $\Omega'$, $\Omega''$ and $\Omega'''$.

**The method.**
1. **Unknowns.** Four per shell, stored in order $\Omega$, $\Omega''$, $\Omega'$, $\Omega'''$; $NM = 4N - 2$ unknowns in all (the surface has two). Each row couples to unknowns up to 4 places before and 5 after, a band that BANDW handles.
2. **Rows.** For shell $i$: the $\Omega$ equation, implicit in time, with advective terms ($\tfrac12\Delta t/(I_i\,\Delta r)$ times `ECOD3`, `ECOD5`) and diffusive terms ($\Delta t/(I_i\Delta r)$ times `ECOD4`, `ECOD6`); then three rows that define the derivatives by finite differences (for example $\Omega'_i = (\Omega_{i+1} - \Omega_i)/\Delta r$). At the centre, no flux; at the surface, the same unless `LFIX`, which holds $\Omega$ fixed.
3. **Coefficients.** From the current $\Omega$ (`EWPREV`), with $\bar\Omega$ the interface mean (corrected by a second difference): $V_1 = f_w E_0\bar\Omega^2(E_{1a} + \bar\Omega^2E_{1b})$, $V_2 = f_w E_0\bar\Omega^2(E_{2a} + E_{2b})$; `ECOD3` $= 0.2\,V_1\,f_\mathrm{geom}$ and `ECOD4` $= (0.2\,V_2 + E_{SS} + E_{GSF})\,f_\mathrm{geom}$, not below zero. The shear and GSF terms are rescaled by $(\partial\Omega/\partial r)^2$ relative to the start.
4. **The wind.** The surface row's right-hand side is reduced by $\Delta J = -\tfrac12(W_1 + W_2)\,I_N\,(\Delta t_\mathrm{sub}/\Delta t)$. From the second outer iteration, `WIND2` is rescaled to the current surface $\Omega$ with the saturation law, $W_2 = W_{2,0}\,(\Omega_n^\mathrm{sat}/\Omega_p^\mathrm{sat})^{n-1}\,\Omega_n/\Omega_p$.
5. **Iterations.** Three nested loops: substeps (`NSTEP`), an outer iteration (`NNN`, meant for the $d\theta/dt$ term, now zero) and an inner iteration (`NN`) on the coefficients. Inner convergence: $\max|\Delta\Omega/\Omega| <$ `DJOK`. Each inner solution is rescaled so that total angular momentum is conserved exactly: $\Omega \leftarrow \Omega\,(J_0 + \Delta J)/J$.
6. **Step cutting.** If a correction exceeds 10% ($|\Delta\Omega/\Omega| > 0.1$) or the iterations fail, double the number of substeps and restart; after 5 cuts, `STOP 111`.
7. **Composition mixing.** From the final solution, the circulation velocity $V_\mathrm{tot}$ (`VTOT2`: the sum of the advective and diffusive terms, with the `ECOD4` term replaced by its circulation part alone, `V1E`, so that shear and GSF are not counted twice) and
$$D_\mathrm{mix} = \left(5\,|f_c f_{ES}\,V_\mathrm{tot}\,r_\mathrm{eq}| + f_c f_{SS}E_{SS} + f_c f_{GSF}E_{GSF}\right) f_\mathrm{geom,mix}.$$

**Design.** The header comments are those of [[dcoeft.f#DCOEFT|DCOEFT]] ("DCOEFT sets up…", "a tridiagonal matrix"), not updated for the band system. A residual check of the band solution (`C = AA·B`) is computed but never used. The damping factor `FX` is always 1 (the alternative is commented out). The time-derivative terms of $\theta$ (`VTHN`, `VTHP`) are all set to zero.

**KC's changes.** 2025-05-31: the unused argument `EJ` removed; the call to BANDW no longer passes `M1`, `M2` (the band widths 4 and 5, now fixed in BANDW).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules or local arrays, `IMPLICIT NONE`, and the unused `/DEUTER/` gone. `LROSSBY` and `PMMSOLTAU` now come from `NMLPAR_MOD`, so the Rossby scaling of $\Omega_\mathrm{sat}$ applies here as in the wind routines; this settles the former question 1 (they were undeclared locals).

## Questions for the experts

1. **Unused residual check.** The array `C` (the product of the saved matrix and the solution) is computed "to check on the matrix inversion", then ignored. Should it be compared with `D`?
2. **The $d\theta/dt$ term.** The outer iteration exists for it, but every version of the term is commented out or zero. Can the loop go, or is the term meant to come back?
3. **Size limit.** `NM = 4*NTOT-2` must not exceed `NMAX = 8000`, so `NTOT` $\le$ 2000; nothing checks it.
4. **Hard-coded factors.** The factors 0.2 in `ECOD3`/`ECOD4` and 5 in `VESN`, and the 10% limit on corrections. Where do the 0.2 and 5 come from (they are reciprocal)?
5. **Screen output.** Several unconditional `WRITE(*,*)` per iteration (sums of $J$, iteration counters, the first and last 10 points). Debug leftovers?

### DADCOEFT

Implicit advection–diffusion of angular momentum on the even grid: four unknowns per shell ($\Omega$ and three derivatives) in a band system solved by [[bandw.f#BANDW|BANDW]]; iterates on $\Omega$-dependent coefficients, enforces angular-momentum conservation with the wind, cuts the substep on failure, and returns `DJ`, `SUMDJ`, `LOKAD` and the composition coefficient `ECOD2`.
