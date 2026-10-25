## Explanation

**Purpose.** The right-hand side of the atmosphere integration: with $\log\tau$ as the independent variable and $\log P$ as the dependent one, it returns $d\log P/d\log\tau$ from a $T$–$\tau$ relation. Its comment: "QATM calculates the derivative d(P)/d(tau), using the Eddington approximation for a T-tau relation."

**How it fits.**
- **Inputs:** `X0` $=\log\tau$, `Y(1)` $=\log P$; $\log g$ (`GL`), the distortion factor `FPL`, `TEFFL`, $X$, $Z$; the choice of relation `KTTAU` and `HRAS` from `/ATMOS/`; `LMHD`.
- **Who calls it:** [[envint.f#ENVINT|ENVINT]], directly and as the `EXTERNAL` derivative routine passed to [[bsstep.f#BSSTEP|BSSTEP]] (and so to [[mmid.f#MMID|MMID]]); this is why it keeps arguments it does not use.
- **What it calls:** [[meqos.f#MEQOS|MEQOS]] or [[eqstat.f#EQSTAT|EQSTAT]], [[getopac.f#GETOPAC|GETOPAC]], and the function [[hra.f#HRA|HRA]] (the Harvard–Smithsonian reference atmosphere).
- **Outputs:** `DYDX(1)`; the counter `KATM`; the point's $\log P$, $\log T$ (and, when saving or for pulsation output, $\log\rho$, $\kappa$, ionization fractions) in `/ATMPRT/`; the thermodynamic quantities for pulsation output in `/PULSE2/`.

**The method.** The temperature from the $T$–$\tau$ relation:
- Eddington (`KTTAU = 0`): $T^4 = \tfrac34\,T_\mathrm{eff}^4\,(\tau + \tfrac23)$, coded as $\log T = \log T_\mathrm{eff} - 0.031235 + \tfrac14\log(\tau + \tfrac23)$ (with $\tfrac14\log\tfrac34 = -0.031235$);
- Krishna Swamy (1966, ApJ 145, 176; `KTTAU = 1`): the same with $q(\tau) = 1.39 - 0.815\,e^{-2.54\tau} - 0.025\,e^{-30\tau}$ in place of $\tfrac23$;
- Harvard–Smithsonian (`KTTAU = 2`): $\log T = \log T_\mathrm{eff} + \mathrm{HRA}(\tau) - \mathrm{HRA}(\tfrac23)$ (`HRAS` $=\mathrm{HRA}(\tfrac23)$, set once by [[setups.f#SETUPS|SETUPS]]).

Then $\rho$ and $\kappa$ at $(P, T)$, and hydrostatic equilibrium in the form $dP/d\tau = g/\kappa$:
$$\frac{d\log P}{d\log\tau} = \frac{g\,\tau}{\kappa\,P},\qquad g = 10^{\log g}\,f_P .$$

**KC's changes.** 2025-05-31: unused arguments removed from the call to `MEQOS`; a never-executed `PRINT` keeps the unused arguments `B`, `FTL`, `LOCOND`, `RL` referenced, "for external procedure compatibility".

## Questions for the experts

1. **`KTTAU` 3–5.** For the tabulated atmospheres (Kurucz, Allard, Kurucz/Castelli), no branch sets `TL`, so it keeps its value from the previous call. Are these atmospheres never integrated through `QATM` (their surface pressures come from tables), and should the routine stop if called with them?
2. **The comment.** It says the routine computes $dP/d\tau$ "using the Eddington approximation"; it computes $d\log P/d\log\tau$ with any of three relations.
