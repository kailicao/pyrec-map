## Explanation

**Purpose.** The right-hand side of the atmosphere integration: with $\log\tau$ as the independent variable and $\log P$ as the dependent one, it returns $d\log P/d\log\tau$ from a $T$–$\tau$ relation. Its comment: "QATM calculates the derivative d(P)/d(tau), using the Eddington approximation for a T-tau relation."

> **Question** ([[#L36-L39]]; [[#L77-L83]]). **The comment.** It says the routine computes $dP/d\tau$ "using the Eddington approximation"; it computes $d\log P/d\log\tau$ with any of three relations (`KTTAU` = 0, 1, 2). Should the comment be corrected?

**How it fits.**
- **Inputs:** `X0` $=\log\tau$, `Y(1)` $=\log P$; $\log g$ (`GL`), the distortion factor `FPL`, `TEFFL`, $X$, $Z$; the choice of relation `KTTAU` from [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] and `HRAS` from [[atmos_mod.f#ATMOS_MOD|`ATMOS_MOD`]]; `LPUMOD` (pulsation output) from [[pulse1_mod.f#PULSE1_MOD|`PULSE1_MOD`]].
- **Who calls it:** [[envint.f#ENVINT|ENVINT]], directly and as the `EXTERNAL` derivative routine passed to [[bsstep.f#BSSTEP|BSSTEP]] (and so to [[mmid.f#MMID|MMID]]); this is why it keeps arguments it does not use.
- **What it calls:** [[eqstat.f#EQSTAT|EQSTAT]], [[getopac.f#GETOPAC|GETOPAC]], and the function [[hra.f#HRA|HRA]] (the Harvard–Smithsonian reference atmosphere).
- **Outputs:** `DYDX(1)`; the counter `KATM`; the point's $\log P$, $\log T$ (and, when saving or for pulsation output, $\log\rho$, $\kappa$, ionization fractions) in [[atmprt_mod.f#ATMPRT_MOD|`ATMPRT_MOD`]]; the thermodynamic quantities for pulsation output in [[pulse2_mod.f#PULSE2_MOD|`PULSE2_MOD`]].

**The method.** The temperature from the $T$–$\tau$ relation:
- Eddington (`KTTAU = 0`): $T^4 = \tfrac34\,T_\mathrm{eff}^4\,(\tau + \tfrac23)$, coded as $\log T = \log T_\mathrm{eff} - 0.031235 + \tfrac14\log(\tau + \tfrac23)$ (with $\tfrac14\log\tfrac34 = -0.031235$);
- Krishna Swamy (1966, ApJ 145, 176; `KTTAU = 1`): the same with $q(\tau) = 1.39 - 0.815\,e^{-2.54\tau} - 0.025\,e^{-30\tau}$ in place of $\tfrac23$;
- Harvard–Smithsonian (`KTTAU = 2`): $\log T = \log T_\mathrm{eff} + \mathrm{HRA}(\tau) - \mathrm{HRA}(\tfrac23)$ (`HRAS` $=\mathrm{HRA}(\tfrac23)$, set once by [[setups.f#SETUPS|SETUPS]]).

For the tabulated atmospheres (`KTTAU` = 3, 4, 5) no branch sets `TL` ([[#L77-L83]]), but QATM is not called with them: [[envint.f#ENVINT|ENVINT]] takes their surface pressure from SURFP, KCSURFP, or ALSURFP and goes past the atmosphere integration, and after a failed Allard lookup it sets `KTTAU` = 0 before integrating ([[envint.f#L228-L257]]; settled from the code, Nov 9, 2026).

Then $\rho$ and $\kappa$ at $(P, T)$, and hydrostatic equilibrium in the form $dP/d\tau = g/\kappa$:
$$\frac{d\log P}{d\log\tau} = \frac{g\,\tau}{\kappa\,P},\qquad g = 10^{\log g}\,f_P .$$
Here $P$ is the total pressure, gas plus radiation (EQSTAT is called with it, and returns $\rho$ from $P - aT^4/3$), so the radiative force enters through the radiation pressure $aT^4/3$ set by the $T$–$\tau$ relation, and $g$ is not reduced by a radiative acceleration.

**Changed since `rp_1`.** The MHD equation of state removed: `EQSTAT` is always called (no `LMHD`, no `MEQOS`); COMMON blocks to modules (the unused `/PULSE/`, `/NWLAOL/`, `/MHD/` dropped), `IMPLICIT NONE`.
