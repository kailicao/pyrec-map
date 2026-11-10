## Explanation

**Purpose.** This file runs the Henyey iterations that correct the interior model at one level of the time step: it sets the surface boundary condition from the envelope, mixes and burns the composition, builds the linearized structure equations, solves them for the corrections to $\log P$, $\log T$, $\log r$ and $L$, applies the corrections (damped), and decides whether the model has converged.

**How it fits.**
- **Inputs:** the arguments: the model (`HP`, `HT`, `HR`, `HL`, `HD`, `HS`, `HS1`, `HS2`, `HCOMP`, `HPP`, `HTT`), `DELTS` (time step, s), `NITER` (the maximum number of iterations), `ITLVL` (the level of iteration within the step), the flags `LNEW`, `LRESET`, `LSBC`, the envelope triangle (envelopes integrated at three points around the model's $(\log T_\mathrm{eff}, \log L)$, whose values at the fitting point are fitted by a plane to give the outer boundary condition; [[surfbc.f#SURFBC|SURFBC]]: `TRIT`, `TRIL`, `PS`, `TS`, `RS`, `FTRI`, `ISTORE`, `ESTORE`), rotation (`FP`, `FT`, `OMEGA`, `HJM`, …), and `CMIXL` (the mixing length, set by main.f from the namelist's `CMIXLA`, passed on to SURFBC, MIX and COEFFT); from [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]], the tolerances `HTOLER`, the damping settings `FCORR0`, `FCORRI`, and the options `LKUTHE` (the helium flash), `LCORR` (print corrections), `LROT`, `LDH`, `LEXCOM`; the current damping `FCORR` ([[ctol_mod.f#CTOL_MOD|`CTOL_MOD`]]); the start-of-step composition `HCOMPP` and, with rotation, the convective flags `LCZO` that [[hpoint.f#HPOINT|HPOINT]] (or [[starin.f#STARIN|STARIN]], for the starting model) stored from OVROT ([[oldmod_mod.f#OLDMOD_MOD|`OLDMOD_MOD`]]), `XNEW`, `ZNEW` ([[comp_mod.f#COMP_MOD|`COMP_MOD`]]), the Debye–Hückel composition ([[debhu_mod.f#DEBHU_MOD|`DEBHU_MOD`]]), and the output units from `IOUNITS_MOD`.
- **Who calls it:** the main program ([[main.f#(file level)|main.f]]), within the evolution loop.
- **What it calls:** [[surfbc.f#SURFBC|SURFBC]] (the surface boundary condition from envelope integrations, as fitting coefficients `CFENV`), [[mix.f#MIX|MIX]] (burning and mixing over the step), [[coefft.f#COEFFT|COEFFT]] (the equations and their derivatives, reduced by REDUCE), [[hsolve.f#HSOLVE|HSOLVE]] (the back-substitution), and with rotation [[getrot.f#GETROT|GETROT]] and [[fpft.f#FPFT|FPFT]].
- **Outputs:** the corrected model, `BL`, `TEFFL`, `LFINI` (converged), `LARGE` (corrections too large: main.f then calls STARIN, which stops the run; see [[main.f#(file level)|main.f]], step 2 of the evolution step), `ITDONE`, `HMAX`/`NHMAX` (largest corrections and where), `TLUMX` (luminosity by source, renormalized), and with rotation `FP`, `FT`, `OMEGA`, `HKEROT`. With `LCORR`, a line per iteration to `ISHORT`.

**The method.**

*The system as a whole.* The unknowns are the corrections $\delta\log P$, $\delta\log T$, $\delta\log r$ and $\delta L$ at each of the $M$ points, $4M$ in all; the composition is not among them (MIX sets it: main.f's call before levels 1 and 2, and step 2 at levels 3 and 4). They are fixed by $4(M-1)$ difference equations, one for each structure equation between each pair of neighbouring points; two central conditions at point 1 ([[coefft.f#COEFFT|COEFFT]]); and two surface conditions, the envelope fit below (`HSRF`). The matrix is block-bidiagonal, and [[reduce.f#REDUCE|REDUCE]] and [[hsolve.f#HSOLVE|HSOLVE]] are the forward and backward sweeps that solve it.

1. If `LSBC`, call SURFBC with the envelope composition. It returns the fit of the envelope's base as linear relations in $\log P$ and $\log T$ at the outermost interior point:
$$\log r = c_1\log P + c_2\log T + c_3, \qquad \log L = c_4\log P + c_5\log T + c_6, \qquad \log T_\mathrm{eff} = c_7\log P + c_8\log T + c_9.$$
   With `LDH`, the composition for the Debye–Hückel correction (`XXDH`, `YYDH`, `ZZDH`, `ZDH`) is first set from shell `M`.
2. At `ITLVL > 2` with $\Delta t > 0$: reset the composition to its start-of-step value and call MIX. The call to [[ovrot.f#OVROT|OVROT]] that followed is commented out ([[#L162-L165]]); with rotation, OVROT runs in HPOINT after each rezone ("CALCULATE OVERSHOOT," [[hpoint.f#L779-L781]]) and in STARIN for the starting model ([[starin.f#L1032-L1033]]), and CRRECT uses the flags they store, `LCZO` (settled from the code, Nov 9, 2026).
3. If the boundary condition was recomputed, the triangle did not flip (`LFLP` from SURFBC) and the model had converged at the previous level (`LFINI`), return at once.
4. Iterate (at most `NITER` times):
   - COEFFT and REDUCE build the system. Renormalize `TLUMX` so that its sum equals $L$ at the surface (not during the helium flash).
   - From the second iteration, if the largest residuals of the equations (`HMAX` from REDUCE) are below `HTOLER(5,·)`, the model has converged.

    > **Question** ([[#L190-L201]]). **Residual test before solving.** At iteration 2 and later, if the residuals are below `HTOLER(5,·)`, the routine returns as converged without solving. The comment notes that boundary equations are not checked. Can the surface condition then be unmet? (The message prints `ITDONE+1` as the iteration count, but `ITDONE` is not incremented on this path.)

   - The surface rows from the fit above: `HSRF(1..3)` linearize the $\log r$ relation and `HSRF(4..6)` the $\log L$ relation, multiplied by $\ln 10\,L$ since $L$, not $\log L$, is the unknown; the $T_\mathrm{eff}$ relation only updates `TEFFL` afterwards. HSOLVE gives the corrections $\delta$.
   - Converged if $\max|\delta\log P|$, $\max|\delta\log T|$, $\max|\delta\log r|$ and $\max \min(|\delta L|, |\delta L/L|)$ are all below `HTOLER(·,1)`; stop (return with `LARGE`) if any exceeds `HTOLER(·,2)`.

    > **Question** ([[#L234]]). **The luminosity test.** The convergence test on $L$ uses $\min(|\delta L|, |\delta L/L|)$, with `HL` in solar units: where $L > 1\,L_\odot$ this is the relative change, elsewhere the absolute one (in a star fainter than the Sun, the absolute one everywhere); the first shell enters with $|\delta L|$ alone ([[#L215]]). Is the mixed test intended?

   - Apply $x \leftarrow x + f\,\delta x$, with the damping $f$ = `FCORR`, raised by `FCORRI` per iteration up to 1 if `FCORR0 > 0`; during the helium flash $f = 0.8$ once $|\delta L| \le 0.5$ and 1 once $\le 5\times10^{-3}$. The changes of $\log P$, $\log T$ over the step (`HPP`, `HTT`) are updated too.
   - New $\log L$ and $\log T_\mathrm{eff}$ (from the fit); with rotation, new $\Omega$, $f_P$, $f_T$ and rotational kinetic energy $\tfrac12\Omega j\,\Delta m$. GETROT gets the flags `LCZO`, so that it imposes the convection-zone rotation law on each convection zone as a whole ([[wczimp.f#WCZIMP|WCZIMP]]) and inverts the other shells one by one.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) (Numerical convergence options):

| variable | default | meaning (documentation) |
| --- | --- | --- |
| `HTOLER(1..4,1)` | 6.0D-5, 4.5D-5, 3.0D-5, 9.0D-5 | convergence tolerances for $\log P$, $\log T$, $\log R$, $L/L_\mathrm{tot}$: the model has converged when the largest correction anywhere is below all four (all local) |
| `HTOLER(5,1)`, `HTOLER(5,2)` | 3.0D-5, 2.5D-6 | if analytic and numerical derivatives agree better than this ($P$ and $R$; $T$ and $L$), the iteration is skipped |
| `HTOLER(1..4,2)` | 0.9, 0.5, 0.5, 2.0 | abort thresholds: a correction larger than this is a divergence (rarely used) |
| `FCORR0` | 0.8 | the predicted corrections can be overestimated at first; the first iteration multiplies them by this |
| `FCORRI` | 0.1 | the increase of that factor at each iteration (with the defaults, 0.8, 0.9, 1.0); larger is faster but less stable |
| `LCORR` | true | write the details of convergence to the `.short` file |

The code does not compare derivatives for `HTOLER(5,·)`: it compares the largest residuals of the difference equations (`HMAX`, from REDUCE) with `HTOLER(5,1)` for $P$ and $r$ and `HTOLER(5,2)` for $T$ and $L$, and returns as converged ("R.H.S. BELOW TOLERANCES") without solving (step 4).

**`HTOLER(5,·)` bounds residuals, not derivatives.** The Physics namelist page says that "If the difference between analytic and numerical derivatives is better than this, iteration is skipped." The code ("CHECK ON SIGNIFICANCE OF R.H.S. EQUATIONS," message "R.H.S. BELOW TOLERANCES": [[#L190-L196]]) compares with them `HMAX`, the largest residuals of the difference equations, which REDUCE fills ([[reduce.f#L33-L40]]), `HTOLER(5,1)` for $P$ and $r$ and `HTOLER(5,2)` for $T$ and $L$, before HSOLVE's call ([[#L212]]) reuses `HMAX` for the corrections; no numerical derivatives are formed, so the documentation could describe the residual test.

**Changed since `rp_1`.** The new argument `CMIXL` (the mixing length, formerly in `/CONST3/`), passed on to SURFBC, MIX and COEFFT; COMMON blocks to modules, `IMPLICIT NONE`.

**Changed since `a8a5950`.** GETROT gets `LCZO`, the convective flags from OVROT, instead of the argument `LCZ`, which main.f never set, so that every shell was inverted on its own and the convection-zone law ([[wczimp.f#WCZIMP|WCZIMP]]) was never imposed in the structure solve; the argument `LCZ`, then unused, is removed, and so are `QDT` and `QDP`, now locals of COEFFT; the test that sets `LSBC` is parenthesized as the compiler parses it, `LNEW .OR. (LRESET .AND. ITLVL.EQ.2)`, since a new run needs a triangle at level 1 (this settles former question 1). The later questions are renumbered.

## Bugs, by priority

1. **(not reached)** **`JENV` is unset at levels 1 and 2.** ([[#L57]]; [[#L150-L161]]; [[#L176-L179]]) `JENV`, the first shell of the convective envelope, is a local of CRRECT, set only by its own call to MIX at levels 3 and 4 (`ITLVL > 2`), and passed to [[coefft.f#COEFFT|COEFFT]]. COEFFT reads it when the entropy terms are on and mass is gained (`LMDOT` and `DMDT0 > 0`): shells with `IM.GE.JENV` get the extra changes `DLOGT`, `DLOGP` in $\log T$, $\log P$ ([[coefft.f#L324-L331]]). At levels 1 and 2 of the first step, `JENV` has never been set; at levels 1 and 2 of later steps it is the value from the previous step's MIX, not the one the main program's own MIX and FINDSH have just computed (main.f keeps its own `JENV`). What follows: with accretion, the extra terms go to the wrong shells (or, with an unset value, to all or none) until level 3. Only with `LMDOT` (off by default) and `DMDT0 > 0` (the default is $-10^{-14}$, mass loss).

    **A possible fix:** pass the main program's `JENV` (set by STARIN, MIX and FINDSH) to CRRECT as an argument, in place of the local, so that CRRECT's MIX at levels 3 and 4 updates the same variable.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): not reached in any of 34 runs (26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones; one of these, with `FCORE` = 1.0, stopped in its first second). Two made-up runs had mass loss on (`LMDOT` and `LREIMER`: YREC's 1 $M_\odot$ case to helium ignition, and a 3 $M_\odot$ main-sequence case), but mass loss makes the rate negative, and the path needs `LMDOT` with a mass gain (`DMDT0` > 0, `LREIMER` off), which no case or document sets; the namelists' comment on `LMDOT` reads "Constant Mdot (negative) and Reimers are currently enabled." A run with accretion would reach it; none was run, and whether level 3 removes the effect is still not traced. No fix was run.

### CRRECT

The Henyey iteration for one level of the time step: surface boundary condition ([[surfbc.f#SURFBC|SURFBC]]), mixing and burning ([[mix.f#MIX|MIX]]), equations ([[coefft.f#COEFFT|COEFFT]]), solution ([[hsolve.f#HSOLVE|HSOLVE]]), damped corrections and convergence tests against `HTOLER`.
