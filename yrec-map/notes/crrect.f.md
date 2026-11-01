## Explanation

**Purpose.** This file runs the Henyey iterations that correct the interior model at one level of the time step: it sets the surface boundary condition from the envelope, mixes and burns the composition, builds the linearized structure equations, solves them for the corrections to $\log P$, $\log T$, $\log r$ and $L$, applies the corrections (damped), and decides whether the model has converged.

**How it fits.**
- **Inputs:** the arguments: the model (`HP`, `HT`, `HR`, `HL`, `HD`, `HS`, `HS1`, `HS2`, `HCOMP`, `HPP`, `HTT`), `DELTS` (time step, s), `NITER` (the maximum number of iterations), `ITLVL` (the level of iteration within the step), the flags `LNEW`, `LRESET`, `LSBC`, the envelope triangle (envelopes integrated at three points around the model's $(\log T_\mathrm{eff}, \log L)$, whose values at the fitting point are fitted by a plane to give the outer boundary condition; [[surfbc.f#SURFBC|SURFBC]]: `TRIT`, `TRIL`, `PS`, `TS`, `RS`, `FTRI`, `ISTORE`, `ESTORE`), rotation (`FP`, `FT`, `OMEGA`, `HJM`, …), and `CMIXL` (the mixing length, set by main.f from the namelist's `CMIXLA`, passed on to SURFBC, MIX and COEFFT); from [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]], the tolerances `HTOLER`, the damping settings `FCORR0`, `FCORRI`, and the options `LKUTHE` (the helium flash), `LCORR` (print corrections), `LROT`, `LDH`, `LEXCOM`; the current damping `FCORR` ([[ctol_mod.f#CTOL_MOD|`CTOL_MOD`]]); the start-of-step composition `HCOMPP` ([[oldmod_mod.f#OLDMOD_MOD|`OLDMOD_MOD`]]), `XNEW`, `ZNEW` ([[comp_mod.f#COMP_MOD|`COMP_MOD`]]), the Debye–Hückel composition ([[debhu_mod.f#DEBHU_MOD|`DEBHU_MOD`]]), and the output units from `IOUNITS_MOD`.
- **Who calls it:** the main program ([[main.f#(file level)|main.f]]), within the evolution loop.
- **What it calls:** [[surfbc.f#SURFBC|SURFBC]] (the surface boundary condition from envelope integrations, as fitting coefficients `CFENV`), [[mix.f#MIX|MIX]] (burning and mixing over the step), [[coefft.f#COEFFT|COEFFT]] (the equations and their derivatives, reduced by REDUCE), [[hsolve.f#HSOLVE|HSOLVE]] (the back-substitution), and with rotation [[getrot.f#GETROT|GETROT]] and [[fpft.f#FPFT|FPFT]].
- **Outputs:** the corrected model, `BL`, `TEFFL`, `LFINI` (converged), `LARGE` (corrections too large: main.f then calls STARIN, which stops the run; see [[main.f#(file level)|main.f]], step 2 of the evolution step), `ITDONE`, `HMAX`/`NHMAX` (largest corrections and where), `TLUMX` (luminosity by source, renormalized), and with rotation `FP`, `FT`, `OMEGA`, `HKEROT`. With `LCORR`, a line per iteration to `ISHORT`.

**The method.**

*The system as a whole.* The unknowns are the corrections $\delta\log P$, $\delta\log T$, $\delta\log r$ and $\delta L$ at each of the $M$ points, $4M$ in all; the composition is not among them (MIX sets it: main.f's call before levels 1 and 2, and step 2 at levels 3 and 4). They are fixed by $4(M-1)$ difference equations, one for each structure equation between each pair of neighbouring points; two central conditions at point 1 ([[coefft.f#COEFFT|COEFFT]]); and two surface conditions, the envelope fit below (`HSRF`). The matrix is block-bidiagonal, and [[reduce.f#REDUCE|REDUCE]] and [[hsolve.f#HSOLVE|HSOLVE]] are the forward and backward sweeps that solve it.

1. If `LSBC`, call SURFBC with the envelope composition. It returns the fit of the envelope's base as linear relations in $\log P$ and $\log T$ at the outermost interior point:
$$\log r = c_1\log P + c_2\log T + c_3, \qquad \log L = c_4\log P + c_5\log T + c_6, \qquad \log T_\mathrm{eff} = c_7\log P + c_8\log T + c_9.$$
   With `LDH`, the composition for the Debye–Hückel correction (`XXDH`, `YYDH`, `ZZDH`, `ZDH`) is first set from shell `M`.
2. At `ITLVL > 2` with $\Delta t > 0$: reset the composition to its start-of-step value and call MIX.
3. If the boundary condition was recomputed, the triangle did not flip (`LFLP` from SURFBC) and the model had converged at the previous level (`LFINI`), return at once.
4. Iterate (at most `NITER` times):
   - COEFFT and REDUCE build the system. Renormalize `TLUMX` so that its sum equals $L$ at the surface (not during the helium flash).
   - From the second iteration, if the largest residuals of the equations (`HMAX` from REDUCE) are below `HTOLER(5,·)`, the model has converged.
   - The surface rows from the fit above: `HSRF(1..3)` linearize the $\log r$ relation and `HSRF(4..6)` the $\log L$ relation, multiplied by $\ln 10\,L$ since $L$, not $\log L$, is the unknown; the $T_\mathrm{eff}$ relation only updates `TEFFL` afterwards. HSOLVE gives the corrections $\delta$.
   - Converged if $\max|\delta\log P|$, $\max|\delta\log T|$, $\max|\delta\log r|$ and $\max \min(|\delta L|, |\delta L/L|)$ are all below `HTOLER(·,1)`; stop (return with `LARGE`) if any exceeds `HTOLER(·,2)`.
   - Apply $x \leftarrow x + f\,\delta x$, with the damping $f$ = `FCORR`, raised by `FCORRI` per iteration up to 1 if `FCORR0 > 0`; during the helium flash $f = 0.8$ once $|\delta L| \le 0.5$ and 1 once $\le 5\times10^{-3}$. The changes of $\log P$, $\log T$ over the step (`HPP`, `HTT`) are updated too.
   - New $\log L$ and $\log T_\mathrm{eff}$ (from the fit); with rotation, new $\Omega$, $f_P$, $f_T$ and rotational kinetic energy $\tfrac12\Omega j\,\Delta m$.

**KC's changes.** 2025-05-31: the unused arguments `MODEL`, `MRZONE`, `NRZONE`, `NZONE` removed; `LSBC` dropped from the call to SURFBC; `QDT`, `QDP` dropped from the call to MIX; `MODEL` dropped from the call to COEFFT.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) (Numerical convergence options):

| variable | default | meaning (documentation) |
| --- | --- | --- |
| `HTOLER(1..4,1)` | 6.0D-5, 4.5D-5, 3.0D-5, 9.0D-5 | convergence tolerances for $\log P$, $\log T$, $\log R$, $L/L_\mathrm{tot}$: the model has converged when the largest correction anywhere is below all four (all local) |
| `HTOLER(5,1)`, `HTOLER(5,2)` | 3.0D-5, 2.5D-6 | if analytic and numerical derivatives agree better than this ($P$ and $R$; $T$ and $L$), the iteration is skipped |
| `HTOLER(1..4,2)` | 0.9, 0.5, 0.5, 2.0 | abort thresholds: a correction larger than this is a divergence (rarely used) |
| `FCORR0` | 0.8 | the predicted corrections can be overestimated at first; the first iteration multiplies them by this |
| `FCORRI` | 0.1 | the increase of that factor at each iteration (with the defaults, 0.8, 0.9, 1.0); larger is faster but less stable |
| `LCORR` | true | write the details of convergence to the `.short` file |

The code does not compare derivatives for `HTOLER(5,·)`: it compares the largest residuals of the difference equations (`HMAX`, from REDUCE) with `HTOLER(5,1)` for $P$ and $r$ and `HTOLER(5,2)` for $T$ and $L$, and returns as converged ("R.H.S. BELOW TOLERANCES") without solving (step 4; question 6).

**Changed since `rp_1`.** The new argument `CMIXL` (the mixing length, formerly in `/CONST3/`), passed on to SURFBC, MIX and COEFFT; COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **Operator precedence.** `IF(LNEW.OR.LRESET .AND.ITLVL.EQ.2) LSBC = .TRUE.` reads as `LNEW .OR. (LRESET .AND. ITLVL.EQ.2)` in Fortran. Was `(LNEW.OR.LRESET) .AND. ITLVL.EQ.2` meant?
2. **The luminosity test.** The convergence test on $L$ uses $\min(|\delta L|, |\delta L/L|)$, with `HL` in solar units: where $L > 1\,L_\odot$ this is the relative change, elsewhere the absolute one (in a star fainter than the Sun, the absolute one everywhere); the first shell enters with $|\delta L|$ alone. Is the mixed test intended?
3. **Residual test before solving.** At iteration 2 and later, if the residuals are below `HTOLER(5,·)`, the routine returns as converged without solving. The comment notes that boundary equations are not checked. Can the surface condition then be unmet? (The message prints `ITDONE+1` as the iteration count, but `ITDONE` is not incremented on this path.)
4. **Commented-out OVROT.** The call to [[ovrot.f#OVROT|OVROT]] for rotating models is commented out here. Is overshoot for rotating models handled elsewhere now?
5. **Local zone arrays.** `MXZON0`, `JCORE`, `JENV` are local and set by MIX (only `MXZONE` is an argument, so the caller never sees the others). `JENV` is then passed to [[coefft.f#COEFFT|COEFFT]], which uses it with entropy terms and mass gain (`LMDOT`, `DMDT0 > 0`) to choose the shells whose $\log P$, $\log T$ changes get extra terms. At levels 1 and 2 MIX is not called, so COEFFT gets the value saved from an earlier call, or an unset value at the first call. Should `JENV` come from the caller?
6. **`HTOLER(5,·)` in the documentation.** The Physics namelist page says that if "analytic and numerical derivatives agree better than" `HTOLER(5,1)`, `HTOLER(5,2)`, "the iteration is skipped". The code ("CHECK ON SIGNIFICANCE OF R.H.S. EQUATIONS", message "R.H.S. BELOW TOLERANCES") compares the largest residuals of the difference equations, `HMAX`, with them, `HTOLER(5,1)` for $P$ and $r$ and `HTOLER(5,2)` for $T$ and $L$; no numerical derivatives are formed. Should the documentation describe the residual test?

### CRRECT

The Henyey iteration for one level of the time step: surface boundary condition ([[surfbc.f#SURFBC|SURFBC]]), mixing and burning ([[mix.f#MIX|MIX]]), equations ([[coefft.f#COEFFT|COEFFT]]), solution ([[hsolve.f#HSOLVE|HSOLVE]]), damped corrections and convergence tests against `HTOLER`.
