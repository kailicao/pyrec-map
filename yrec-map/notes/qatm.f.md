## Explanation

**Purpose.** The right-hand side of the atmosphere integration: with $`\log\tau`$ as the independent variable and $`\log P`$ as the dependent one, it returns $`d\log P/d\log\tau`$ from a $`T`$–$`\tau`$ relation. Its comment: "QATM calculates the derivative d(P)/d(tau), using the Eddington approximation for a T-tau relation."

**The comment names one relation of three.** It says the routine computes $`dP/d\tau`$ "USING THE EDDINGTON APPROXIMATION FOR A T-TAU RELATION" ([lines 36–39](https://github.com/yreclab/yrec/blob/7be4133/src/qatm.f#L36-L39)), but it computes $`d\log P/d\log\tau`$ with any of three $`T(\tau)`$ relations, chosen by `KTTAU` = 0, 1, 2 ([lines 77–83](https://github.com/yreclab/yrec/blob/7be4133/src/qatm.f#L77-L83)), so the comment is stale.

**How it fits.**
- **Inputs:** `X0` $`=\log\tau`$, `Y(1)` $`=\log P`$; $`\log g`$ (`GL`), the distortion factor `FPL`, `TEFFL`, $`X`$, $`Z`$; the choice of relation `KTTAU` from [`NMLPAR_MOD`](nmlpar_mod.f.md#nmlpar_mod) and `HRAS` from [`ATMOS_MOD`](atmos_mod.f.md#atmos_mod); `LPUMOD` (pulsation output) from [`PULSE1_MOD`](pulse1_mod.f.md#pulse1_mod).
- **Who calls it:** [ENVINT](envint.f.md#envint), directly and as the `EXTERNAL` derivative routine passed to [BSSTEP](bsstep.f.md#bsstep) (and so to [MMID](mmid.f.md#mmid)); this is why it keeps arguments it does not use.
- **What it calls:** [EQSTAT](eqstat.f.md#eqstat), [GETOPAC](getopac.f.md#getopac), and the function [HRA](hra.f.md#hra) (the Harvard–Smithsonian reference atmosphere).
- **Outputs:** `DYDX(1)`; the counter `KATM`; the point's $`\log P`$, $`\log T`$ (and, when saving or for pulsation output, $`\log\rho`$, $`\kappa`$, ionization fractions) in [`ATMPRT_MOD`](atmprt_mod.f.md#atmprt_mod); the thermodynamic quantities for pulsation output in [`PULSE2_MOD`](pulse2_mod.f.md#pulse2_mod).

**The method.** The temperature from the $`T`$–$`\tau`$ relation:
- Eddington (`KTTAU = 0`): $`T^4 = \tfrac34\,T_\mathrm{eff}^4\,(\tau + \tfrac23)`$, coded as $`\log T = \log T_\mathrm{eff} - 0.031235 + \tfrac14\log(\tau + \tfrac23)`$ (with $`\tfrac14\log\tfrac34 = -0.031235`$);
- Krishna Swamy ([1966](https://ui.adsabs.harvard.edu/abs/1966ApJ...145..174K), ApJ 145, 176 in the comment, though the paper begins on page 174; `KTTAU = 1`): the same with $`q(\tau) = 1.39 - 0.815\,e^{-2.54\tau} - 0.025\,e^{-30\tau}`$ in place of $`\tfrac23`$;
- Harvard–Smithsonian (`KTTAU = 2`): $`\log T = \log T_\mathrm{eff} + \mathrm{HRA}(\tau) - \mathrm{HRA}(\tfrac23)`$ (`HRAS` $`=\mathrm{HRA}(\tfrac23)`$, set once by [SETUPS](setups.f.md#setups)).

For the tabulated atmospheres (`KTTAU` = 3, 4, 5) no branch sets `TL` ([lines 77–83](https://github.com/yreclab/yrec/blob/7be4133/src/qatm.f#L77-L83)), but QATM is not called with them: [ENVINT](envint.f.md#envint) takes their surface pressure from SURFP, KCSURFP, or ALSURFP and goes past the atmosphere integration, and after a failed Allard lookup it sets `KTTAU` = 0 before integrating ([envint.f, lines 228–257](https://github.com/yreclab/yrec/blob/7be4133/src/envint.f#L228-L257); settled from the code, Nov 9, 2026).

Then $`\rho`$ and $`\kappa`$ at $`(P, T)`$, and hydrostatic equilibrium in the form $`dP/d\tau = g/\kappa`$:
```math
\frac{d\log P}{d\log\tau} = \frac{g\,\tau}{\kappa\,P},\qquad g = 10^{\log g}\,f_P .
```
Here $`P`$ is the total pressure, gas plus radiation (EQSTAT is called with it, and returns $`\rho`$ from $`P - aT^4/3`$), so the radiative force enters through the radiation pressure $`aT^4/3`$ set by the $`T`$–$`\tau`$ relation, and $`g`$ is not reduced by a radiative acceleration.

**Changed since `rp_1`.** The MHD equation of state removed: `EQSTAT` is always called (no `LMHD`, no `MEQOS`); COMMON blocks to modules (the unused `/PULSE/`, `/NWLAOL/`, `/MHD/` dropped), `IMPLICIT NONE`.
