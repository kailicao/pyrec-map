## Explanation

**Purpose.** This file computes the structure-dependent factor of the magnetic-braking torque, "according to the Matt et al. ([2012](https://ui.adsabs.harvard.edu/abs/2012ApJ...754L..26M)) formulation" (comment by G. Somers, 6/16). The factor scales the angular-momentum loss of the wind with the star's mass, radius, luminosity, photospheric pressure and, optionally, its convective overturn time.

**How it fits.**
- **Inputs:** the arguments `SMASS` (the star's mass in solar masses: [MDOT](mdot.f.md#mdot) updates it as `SMASS + DELM/CMSUN`, and COWIND's header says "stellar mass (solar units)"), `BL` ($`\log L/L_\odot`$) and `TEFFL` ($`\log T_\mathrm{eff}`$); the exponents `EXM`, `EXR`, `EXL`, `EXPR`, `EXTAU`, the solar normalizations `PMMSOLP` and `PMMSOLTAU` and the switch `LROSSBY`, all namelist parameters in [NMLPAR_MOD](nmlpar_mod.f.md#nmlpar_mod) (set in [PARMIN](parmin.f.md#parmin)); the photospheric pressure `PPHOT`, `PPHOT0`, the overturn time `TAUCZ`, `TAUCZ0` and `FRACSTEP` in [OVRTRN_MOD](ovrtrn_mod.f.md#ovrtrn_mod).
- **Who calls it:** [MWIND](mwind.f.md#mwind) and [MCOWIND](mcowind.f.md#mcowind).
- **Output:** the argument `STRUCTFACTOR`, which MWIND and MCOWIND multiply with `CONSTFACTOR` and the time step to get the spin-down.
- **Modules:** [CONSTANTS_MOD](constants_mod.f.md#constants_mod) (`CLSUNL`, `C4PIL`, `CSIGL`, `CLN`, `CRSUN`), [NMLPAR_MOD](nmlpar_mod.f.md#nmlpar_mod) and [OVRTRN_MOD](ovrtrn_mod.f.md#ovrtrn_mod).

**The method.**
1. The radius from the Stefan–Boltzmann law, in cgs units:
   
   $$\displaystyle \log R = \tfrac12\left(\log L - \log 4\pi - \log\sigma - 4\log T\_\mathrm{eff}\right),$$
   
   with $`\log L`$ = `BL + CLSUNL`; then $`R/R_\odot`$ (`RRAD`).
2. $`L/L_\odot = 10^{\mathtt{BL}}`$.
3. The photospheric pressure, interpolated within the step between its values at the start (`PPHOT0`) and end (`PPHOT`) of the step, both $`\log P`$, and normalized to the solar value:
   
   $$\displaystyle \frac{P\_\mathrm{phot}}{P\_{\mathrm{phot},\odot}} = \frac{10^{\\,p\_0 + f\\,(p - p\_0)}}{10^{\\,p\_\odot}},$$
   
   with $`f`$ = `FRACSTEP`.
4. If `LROSSBY`, the overturn time likewise, $`\tau/\tau_\odot = [\tau_0 + f(\tau - \tau_0)]/\tau_\odot`$; otherwise 1.
5. The factor:
   
   $$\displaystyle \mathtt{STRUCTFACTOR} = M^{a\_M}\\,\left(\frac{R}{R\_\odot}\right)^{a\_R}\left(\frac{L}{L\_\odot}\right)^{a\_L}\left(\frac{P\_\mathrm{phot}}{P\_{\mathrm{phot},\odot}}\right)^{a\_P}\left(\frac{\tau}{\tau\_\odot}\right)^{a\_\tau}.$$

**Design.** The radius comes from $`L`$ and $`T_\mathrm{eff}`$, not from the model's outer radius. The mass is used as given, with no solar normalization in this routine.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html): `PMMSOLP` (default 4.9304) is $`\log P`$ at $`T_\mathrm{eff}`$ in the solar model, for the magnetic field's calibration, and `PMMSOLTAU` (9.4805D5 s) the Sun's convective overturn time; `LROSSBY` scales the loss with the Rossby number.

**Changed since `rp_1`.** `STRUCTFACTOR` is now an output argument (`/CWIND/` retired); COMMON blocks to modules, `IMPLICIT NONE`; the unused constants and `AWIND` are gone, which settles the former question on them.

### AMCALC

Sets `STRUCTFACTOR`, the product of $`M`$, $`R/R_\odot`$, $`L/L_\odot`$, $`P_\mathrm{phot}/P_{\mathrm{phot},\odot}`$ and optionally $`\tau/\tau_\odot`$, each to its exponent from `NMLPAR_MOD` (Matt et al. 2012), and returns it in `STRUCTFACTOR`.
