## Explanation

**Purpose.** This file computes the structure-dependent factor of the magnetic-braking torque, "according to the Matt et al. (2012) formulation" (comment by G. Somers, 6/16). The factor scales the angular-momentum loss of the wind with the star's mass, radius, luminosity, photospheric pressure and, optionally, its convective overturn time.

**How it fits.**
- **Inputs:** the arguments `SMASS` (the star's mass in solar masses: [[mdot.f#MDOT|MDOT]] updates it as `SMASS + DELM/CMSUN`, and COWIND's header says "stellar mass (solar units)"), `BL` ($\log L/L_\odot$) and `TEFFL` ($\log T_\mathrm{eff}$); the exponents `EXM`, `EXR`, `EXL`, `EXPR`, `EXTAU` in `/CWIND/`; the solar normalizations `PMMSOLP` and `PMMSOLTAU` and the switch `LROSSBY` in `/PMMWIND/` (set in [[parmin.f#PARMIN|PARMIN]]); the photospheric pressure `PPHOT`, `PPHOT0`, the overturn time `TAUCZ`, `TAUCZ0` and `FRACSTEP` in `/OVRTRN/`.
- **Who calls it:** [[mwind.f#MWIND|MWIND]] and [[mcowind.f#MCOWIND|MCOWIND]].
- **Output:** `STRUCTFACTOR` in `/CWIND/`, which MWIND and MCOWIND multiply with `CONSTFACTOR` and the time step to get the spin-down.
- **COMMON blocks:** the constants `/CONST/`, `/CONST1/`, `/CONST2/`, `/CONST3/`; `/CWIND/` (12 units, among them [[cowind.f#COWIND|COWIND]], [[dadcoeft.f#DADCOEFT|DADCOEFT]]); `/PMMWIND/` (MWIND, MCOWIND, PARMIN); `/OVRTRN/` (21 units).

**The method.**
1. The radius from the Stefan–Boltzmann law, in cgs units:
$$\log R = \tfrac12\left(\log L - \log 4\pi - \log\sigma - 4\log T_\mathrm{eff}\right),$$
with $\log L$ = `BL + CLSUNL`; then $R/R_\odot$ (`RRAD`).
2. $L/L_\odot = 10^{\mathtt{BL}}$.
3. The photospheric pressure, interpolated within the step between its values at the start (`PPHOT0`) and end (`PPHOT`) of the step, both $\log P$, and normalized to the solar value:
$$\frac{P_\mathrm{phot}}{P_{\mathrm{phot},\odot}} = \frac{10^{\,p_0 + f\,(p - p_0)}}{10^{\,p_\odot}},$$
with $f$ = `FRACSTEP`.
4. If `LROSSBY`, the overturn time likewise, $\tau/\tau_\odot = [\tau_0 + f(\tau - \tau_0)]/\tau_\odot$; otherwise 1.
5. The factor:
$$\mathtt{STRUCTFACTOR} = M^{a_M}\,\left(\frac{R}{R_\odot}\right)^{a_R}\left(\frac{L}{L_\odot}\right)^{a_L}\left(\frac{P_\mathrm{phot}}{P_{\mathrm{phot},\odot}}\right)^{a_P}\left(\frac{\tau}{\tau_\odot}\right)^{a_\tau}.$$

**Design.** The radius comes from $L$ and $T_\mathrm{eff}$, not from the model's outer radius. The mass is used as given, with no solar normalization in this routine.

**KC's changes.** 2025-05-30: the elements of `/PMMWIND/` reordered (reals first, then logicals and the character `AWIND`); the old order is kept as a comment.

## Questions for the experts

1. **Unused constants.** `/CONST2/` and `/CONST3/` and the declaration of `AWIND` are included but only `CSIGL` (from `/CONST2/`) is used. Harmless; noted for the overhaul.

### AMCALC

Sets `STRUCTFACTOR`, the product of $M$, $R/R_\odot$, $L/L_\odot$, $P_\mathrm{phot}/P_{\mathrm{phot},\odot}$ and optionally $\tau/\tau_\odot$, each to its exponent from `/CWIND/` (Matt et al. 2012).
