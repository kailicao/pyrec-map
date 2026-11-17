## Explanation

**Purpose.** `LIRATE88` computes the burning rates of $`^6\mathrm{Li}`$, $`^7\mathrm{Li}`$ and $`^9\mathrm{Be}`$ by protons at every point, from the fits of Caughlan and Fowler ([1988](https://ui.adsabs.harvard.edu/abs/1988ADNDT..40..283C)) (spelled "Caughlin" in the comment), scaled by user factors. Called with `J` = 1 it computes the rates for the model passed in, stored as the end-of-step set; with `J` = 2, for the saved model at the start of the step, stored as the start-of-step set (the convention its comment now states).

**How it fits.**
- **Who calls it:** the main program, [main.f](main.f.md#file-level) (with `J` = 2 before the structure iteration and `J` = 1 after it, then [`LIBURN`](liburn.f.md#liburn)), and [`GETW`](getw.f.md#getw) (`J` = 1, with its midpoint model) for rotating models.
- **Inputs:** with `J` = 1, the arguments `HD` ($`\log\rho`$), `HT` ($`\log T`$), `HCOMP(1)` ($`X`$); with `J` = 2, the old model `HDO`, `HTO`, `HCOMPP` from `OLDMOD_MOD`. With `J` = 2, `HD` and `HCOMP` are not read and `HT` serves only the temperature cut ([line 65](https://github.com/yreclab/yrec/blob/7be4133/src/lirate88.f#L65)); at that call ([main.f, line 815](https://github.com/yreclab/yrec/blob/7be4133/src/main.f#L815), before the structure iteration) the old model is on the current grid and is the model passed in: [HPOINT](hpoint.f.md#hpoint) splines `HCOMPP` onto the new points ([hpoint.f, lines 656–663](https://github.com/yreclab/yrec/blob/7be4133/src/hpoint.f#L656-L663)) and ends by copying its splined `HTO`, `HDO` into `HT`, `HD` ([hpoint.f, lines 691–692](https://github.com/yreclab/yrec/blob/7be4133/src/hpoint.f#L691-L692), [hpoint.f, lines 733–739](https://github.com/yreclab/yrec/blob/7be4133/src/hpoint.f#L733-L739)), and without rezoning (the helium flash) main.f copies `HT`, `HD` into `HTO`, `HDO` ([main.f, lines 774–780](https://github.com/yreclab/yrec/blob/7be4133/src/main.f#L774-L780)) (settled from the code, Nov 9, 2026). The scale factors `SLI6`, `SLI7`, `SBE91`, `SBE92`, `SBE93` from `NMLPAR_MOD` (namelist values read by [`PARMIN`](parmin.f.md#parmin); formerly `/BURNSCS/`, G. Somers 6/14). The constants (`CLN`, `CC13`, `CC23`) come from `CONSTANTS_MOD`.
- **Outputs:** `RLI6`, `RLI7`, `RBE9` in `NEWRAT_MOD` (`J` = 1) or `RLI60`, `RLI70`, `RBE90` in `OLDRAT_MOD` (`J` = 2), read by `LIBURN`, [`LIBURN2`](liburn2.f.md#liburn2), [`BURSMIX`](bursmix.f.md#bursmix) and `GETW`.

**The method.** With $`T_9 = T/10^9`$, each rate is the Caughlan–Fowler fit $`N_A\langle\sigma v\rangle(T_9)`$ for: $`^6\mathrm{Li}(\mathrm{p},{}^3\mathrm{He})\alpha`$; $`^7\mathrm{Li}(\mathrm{p},\alpha)\alpha`$; and the sum of $`^9\mathrm{Be}(\mathrm{p},\gamma){}^{10}\mathrm{B}`$, $`^9\mathrm{Be}(\mathrm{p},\mathrm{d})2\alpha`$ and $`^9\mathrm{Be}(\mathrm{p},\alpha){}^6\mathrm{Li}`$. For example $`^7\mathrm{Li}(\mathrm{p},\alpha)\alpha`$, with $`T_{9a} = T_9/(1 + 0.759\,T_9)`$:

```math
N_A\langle\sigma v\rangle = \frac{1.096\times10^{9}}{T_9^{2/3}}\,e^{-8.472/T_9^{1/3}} - 4.830\times10^{8}\,\frac{T_{9a}^{5/6}}{T_9^{3/2}}\,e^{-8.472/T_{9a}^{1/3}} + \frac{1.06\times10^{10}}{T_9^{3/2}}\,e^{-30.442/T_9}.
```

Each is multiplied by its scale factor and by $`\rho X`$, giving the rate per nucleus, $`\lambda = \rho X\,N_A\langle\sigma v\rangle`$ (per second, if the fits are in the usual $`\mathrm{cm^3\,mol^{-1}\,s^{-1}}`$; the code does not say). The loop runs from the centre outward and stops at the first point where both the new and the old $`\log T`$ are below 6 (`TLIM`); from there to the surface the set being filled (`NEWRAT_MOD`'s with `J` = 1, `OLDRAT_MOD`'s with `J` = 2) is set to zero.

> **Question** ([line 51](https://github.com/yreclab/yrec/blob/7be4133/src/lirate88.f#L51); [line 65](https://github.com/yreclab/yrec/blob/7be4133/src/lirate88.f#L65)). **Hard-coded cut.** `TLIM` = 6 (in $`\log T`$) is fixed by a `DATA` statement. Is $`10^6\,\mathrm{K}`$ meant to stay fixed, and is it low enough for all three rates to be negligible beyond it (the size of `RLI6` at the cut would show it)?

> **Question** ([lines 83–90](https://github.com/yreclab/yrec/blob/7be4133/src/lirate88.f#L83-L90); [lines 104–108](https://github.com/yreclab/yrec/blob/7be4133/src/lirate88.f#L104-L108)). **Old typos noted in the comments.** The comments record a typo in the old $`^6\mathrm{Li}`$ rate (0.50 for 0.050; the $`T_9^{5/3}`$ coefficient also differs, 0.006 in the old line, 0.005 in the code) and a changed last term of $`^9\mathrm{Be}(\mathrm{p},\gamma)`$ (2.72 vs $`2.76 \times 10^{6}`$). Have these been checked against the published table?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/NEWRAT/`, `/OLDRAT/`, `/OLDMOD/`; `/CONST1/` to `CONSTANTS_MOD`; the scale factors of `/BURNSCS/` to `NMLPAR_MOD`), `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

**Changed since `a8a5950`.** The callers' flags are swapped (in main.f and `GETW`), so that the end-of-step rates now come from the end-of-step model; before, both sets held start-of-step rates and `LIBURN` interpolated between two copies of them. This settles former question 5. Past the cut, only the set being filled is zeroed, which settles former question 1; the other questions are renumbered.

### LIRATE88

The Caughlan–Fowler (1988) rates for $`^6\mathrm{Li}`$, $`^7\mathrm{Li}`$ and $`^9\mathrm{Be}`$, times $`\rho X`$ and the user scale factors (above).
