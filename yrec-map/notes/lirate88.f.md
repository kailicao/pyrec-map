## Explanation

**Purpose.** `LIRATE88` computes the burning rates of ⁶Li, ⁷Li and ⁹Be by protons at every point, from the fits of Caughlan and Fowler (1988) (spelled "Caughlin" in the comment), scaled by user factors. Called with `J` = 1 it computes the rates for the current model; with `J` = 2, for the model at the start of the step.

**How it fits.**
- **Who calls it:** the main program, [[main.f#(file level)|main.f]] (with `J` = 1 before the structure iteration and `J` = 2 after it, then [[liburn.f#LIBURN|`LIBURN`]]), and [[getw.f#GETW|`GETW`]] (`J` = 2) for rotating models.
- **Inputs:** with `J` = 1, the arguments `HD` ($\log\rho$), `HT` ($\log T$), `HCOMP(1)` ($X$); with `J` = 2, the old model `HDO`, `HTO`, `HCOMPP` from `OLDMOD_MOD`. The scale factors `SLI6`, `SLI7`, `SBE91`, `SBE92`, `SBE93` from `NMLPAR_MOD` (namelist values read by [[parmin.f#PARMIN|`PARMIN`]]; formerly `/BURNSCS/`, G. Somers 6/14). The constants (`CLN`, `CC13`, `CC23`) come from `CONSTANTS_MOD`.
- **Outputs:** `RLI6`, `RLI7`, `RBE9` in `NEWRAT_MOD` (`J` = 1) or `RLI60`, `RLI70`, `RBE90` in `OLDRAT_MOD` (`J` = 2), read by `LIBURN`, [[liburn2.f#LIBURN2|`LIBURN2`]], [[bursmix.f#BURSMIX|`BURSMIX`]] and `GETW`.

**The method.** With $T_9 = T/10^9$, each rate is the Caughlan–Fowler fit $N_A\langle\sigma v\rangle(T_9)$ for: ⁶Li(p,³He)α; ⁷Li(p,α)α; and the sum of ⁹Be(p,γ)¹⁰B, ⁹Be(p,d)2α and ⁹Be(p,α)⁶Li. For example ⁷Li(p,α)α, with $T_{9a} = T_9/(1 + 0.759\,T_9)$:

$$N_A\langle\sigma v\rangle = \frac{1.096\times10^{9}}{T_9^{2/3}}\,e^{-8.472/T_9^{1/3}} - 4.830\times10^{8}\,\frac{T_{9a}^{5/6}}{T_9^{3/2}}\,e^{-8.472/T_{9a}^{1/3}} + \frac{1.06\times10^{10}}{T_9^{3/2}}\,e^{-30.442/T_9}.$$

Each is multiplied by its scale factor and by $\rho X$, giving the rate per nucleus, $\lambda = \rho X\,N_A\langle\sigma v\rangle$ (per second, if the fits are in the usual cm³ mol⁻¹ s⁻¹; the code does not say). The loop runs from the centre outward and stops at the first point where both the new and the old $\log T$ are below 6 (`TLIM`); from there to the surface all six rate arrays are set to zero.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/NEWRAT/`, `/OLDRAT/`, `/OLDMOD/`; `/CONST1/` to `CONSTANTS_MOD`; the scale factors of `/BURNSCS/` to `NMLPAR_MOD`), `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Questions for the experts

1. **Zeroing both sets.** Above the cut, a call with `J` = 1 also zeroes the start-of-step rates (`OLDRAT_MOD`) and a call with `J` = 2 the new ones. Harmless if the cut point is the same in both calls, but it depends on both the old and new temperatures; intended?
2. **Unused arguments with `J` = 2.** With `J` = 2 the arguments `HD`, `HT` and `HCOMP` serve only for the temperature cut; the rates come from `OLDMOD_MOD`. Is `OLDMOD_MOD` always on the current grid at that point (it is after `HPOINT`)?
3. **Hard-coded cut.** `TLIM` = 6 (in $\log T$).
4. **Old typos noted in the comments.** The comments record a typo in the old ⁶Li rate (0.50 for 0.050; the $T_9^{5/3}$ coefficient also differs, 0.006 in the old line, 0.005 in the code) and a changed last term of ⁹Be(p,γ) (2.72 vs 2.76 × 10⁶). Have these been checked against the published table?

5. **Are end-of-step rates ever computed? (apparent bug)** main.f saves the starting model into `OLDMOD_MOD` (through `HPOINT` at line 744, or at lines 755–759 when `LKUTHE` is set), then calls `LIRATE88` with `J` = 1 (line 785, comment "find burning rates at the beginning of the time step"), which fills `NEWRAT_MOD` from that same starting model. After convergence it calls `J` = 2 (line 1001, comment "end of the time step"), which fills `OLDRAT_MOD` from `OLDMOD_MOD`, again the starting model. So `LIBURN` receives the starting rates in both arrays, and the rates of the converged model are never used. [[getw.f#GETW|`GETW`]] also calls `J` = 2 "at the end of the time step" (line 396), and after `LIBURN` copies `NEWRAT_MOD` into `OLDRAT_MOD` as the next step's start. The callers' comments fit the code if, with `J` = 2, the routine used the arguments `HD`, `HT`, `HCOMP` and filled `NEWRAT_MOD`. Are the two branches swapped?

### LIRATE88

The Caughlan–Fowler (1988) rates for ⁶Li, ⁷Li and ⁹Be, times $\rho X$ and the user scale factors (above).
