## Explanation

**Purpose.** `LIRATE88` computes the burning rates of ⁶Li, ⁷Li and ⁹Be by protons at every point, from the fits of Caughlan and Fowler (1988) (spelled "Caughlin" in the comment), scaled by user factors. Called with `J` = 1 it computes the rates for the model passed in, stored as the end-of-step set; with `J` = 2, for the saved model at the start of the step, stored as the start-of-step set (the convention its comment now states).

**How it fits.**
- **Who calls it:** the main program, [[main.f#(file level)|main.f]] (with `J` = 2 before the structure iteration and `J` = 1 after it, then [[liburn.f#LIBURN|`LIBURN`]]), and [[getw.f#GETW|`GETW`]] (`J` = 1, with its midpoint model) for rotating models.
- **Inputs:** with `J` = 1, the arguments `HD` ($\log\rho$), `HT` ($\log T$), `HCOMP(1)` ($X$); with `J` = 2, the old model `HDO`, `HTO`, `HCOMPP` from `OLDMOD_MOD`. With `J` = 2, `HD` and `HCOMP` are not read and `HT` serves only the temperature cut ([[#L65]]); at that call ([[main.f#L815]], before the structure iteration) the old model is on the current grid and is the model passed in: [[hpoint.f#HPOINT|HPOINT]] splines `HCOMPP` onto the new points ([[hpoint.f#L656-L663]]) and ends by copying its splined `HTO`, `HDO` into `HT`, `HD` ([[hpoint.f#L691-L692]], [[hpoint.f#L733-L739]]), and without rezoning (the helium flash) main.f copies `HT`, `HD` into `HTO`, `HDO` ([[main.f#L774-L780]]) (settled from the code, Nov 9, 2026). The scale factors `SLI6`, `SLI7`, `SBE91`, `SBE92`, `SBE93` from `NMLPAR_MOD` (namelist values read by [[parmin.f#PARMIN|`PARMIN`]]; formerly `/BURNSCS/`, G. Somers 6/14). The constants (`CLN`, `CC13`, `CC23`) come from `CONSTANTS_MOD`.
- **Outputs:** `RLI6`, `RLI7`, `RBE9` in `NEWRAT_MOD` (`J` = 1) or `RLI60`, `RLI70`, `RBE90` in `OLDRAT_MOD` (`J` = 2), read by `LIBURN`, [[liburn2.f#LIBURN2|`LIBURN2`]], [[bursmix.f#BURSMIX|`BURSMIX`]] and `GETW`.

**The method.** With $T_9 = T/10^9$, each rate is the Caughlan–Fowler fit $N_A\langle\sigma v\rangle(T_9)$ for: ⁶Li(p,³He)α; ⁷Li(p,α)α; and the sum of ⁹Be(p,γ)¹⁰B, ⁹Be(p,d)2α and ⁹Be(p,α)⁶Li. For example ⁷Li(p,α)α, with $T_{9a} = T_9/(1 + 0.759\,T_9)$:

$$N_A\langle\sigma v\rangle = \frac{1.096\times10^{9}}{T_9^{2/3}}\,e^{-8.472/T_9^{1/3}} - 4.830\times10^{8}\,\frac{T_{9a}^{5/6}}{T_9^{3/2}}\,e^{-8.472/T_{9a}^{1/3}} + \frac{1.06\times10^{10}}{T_9^{3/2}}\,e^{-30.442/T_9}.$$

Each is multiplied by its scale factor and by $\rho X$, giving the rate per nucleus, $\lambda = \rho X\,N_A\langle\sigma v\rangle$ (per second, if the fits are in the usual cm³ mol⁻¹ s⁻¹; the code does not say). The loop runs from the centre outward and stops at the first point where both the new and the old $\log T$ are below 6 (`TLIM`); from there to the surface the set being filled (`NEWRAT_MOD`'s with `J` = 1, `OLDRAT_MOD`'s with `J` = 2) is set to zero.

> **Question** ([[#L51]]; [[#L65]]). **Hard-coded cut.** `TLIM` = 6 (in $\log T$) is fixed by a `DATA` statement. Is $10^6$ K meant to stay fixed, and is it low enough for all three rates to be negligible beyond it (the size of `RLI6` at the cut would show it)?

> **Question** ([[#L83-L90]]; [[#L104-L108]]). **Old typos noted in the comments.** The comments record a typo in the old ⁶Li rate (0.50 for 0.050; the $T_9^{5/3}$ coefficient also differs, 0.006 in the old line, 0.005 in the code) and a changed last term of ⁹Be(p,γ) (2.72 vs 2.76 × 10⁶). Have these been checked against the published table?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/NEWRAT/`, `/OLDRAT/`, `/OLDMOD/`; `/CONST1/` to `CONSTANTS_MOD`; the scale factors of `/BURNSCS/` to `NMLPAR_MOD`), `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

**Changed since `a8a5950`.** The callers' flags are swapped (in main.f and `GETW`), so that the end-of-step rates now come from the end-of-step model; before, both sets held start-of-step rates and `LIBURN` interpolated between two copies of them. This settles former question 5. Past the cut, only the set being filled is zeroed, which settles former question 1; the other questions are renumbered.

### LIRATE88

The Caughlan–Fowler (1988) rates for ⁶Li, ⁷Li and ⁹Be, times $\rho X$ and the user scale factors (above).
