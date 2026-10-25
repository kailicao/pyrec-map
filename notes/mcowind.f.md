## Explanation

**Purpose.** `MCOWIND` returns the change in the angular velocity of the surface convection zone caused by magnetized-wind angular-momentum loss over a (diffusion) time step. It implements the newer wind law (G. Somers 3/17, "PMM-style", by its comment after van Saders and Pinsonneault, probably) with saturation, an optional Rossby scaling and the centrifugal correction of Matt et al. (2012, ApJ 754, L26). When the new law is off (`LMWIND` false) it hands over to the older [[cowind.f#COWIND|`COWIND`]].

**How it fits.**
- **Who calls it:** only [[seculr.f#SECULR|`SECULR`]], in the angular-momentum transport, once per iteration `IT` of the diffusion solution.
- **Inputs:** `BL` ($\log L/L_\odot$), `DT` (the diffusion step, s), `HICZ` (moment of inertia of the surface convection zone), `IT`, `OMEGAS` (surface $\Omega$ at the end of the previous iteration), `WOLD` (surface $\Omega$ at the start of the step), `SMASS` ($M/M_\odot$), `TEFFL`.
- **Outputs:** `WIND1` and `WIND2`, the changes in $\Omega$ over the step computed with $\Omega$ at the start and at the end of the step; the caller averages them (its comment).
- **Calls:** [[cowind.f#COWIND|`COWIND`]] (old law) or [[amcalc.f#AMCALC|`AMCALC`]], which sets `STRUCTFACTOR` in `CWIND` from $M$, $L$ and $T_\mathrm{eff}$.
- **COMMON blocks:** `CWIND` (`WMAX`, `EXW`, `CONSTFACTOR`, `STRUCTFACTOR`, `EXCEN`, `C_2`, …; from [[parmin.f#PARMIN|`PARMIN`]], with `AMCALC`, `COWIND`, `MWIND`, `GETW` and others), `PMMWIND` (`LMWIND`, `LROSSBY`, `LBSCALE`, the solar values `PMMSOLW`, `PMMSOLTAU`; with `AMCALC`, `MWIND`, `PARMIN`), `OVRTRN` (`TAUCZ`, `TAUCZ0`, `FRACSTEP`: the convective turnover time at the start and end of the step and the fraction of the step reached), and the constants. `DEUTER` is declared but not used.

**The method.**
1. **Saturation.** With Rossby scaling, the turnover time is interpolated in the step, $\tau = \tau_0 + f\,(\tau_1 - \tau_0)$, and the saturation rate is $\Omega_\mathrm{sat} = \Omega_\mathrm{max}\,\tau_\odot/\tau$. With the extra field scaling as well (`LBSCALE`, which acts only with Rossby scaling) the rates $\Omega$ and $\Omega_\mathrm{sat}$ are multiplied by $\tau/\tau_\odot$. Otherwise $\Omega_\mathrm{sat}$ = `WMAX`.
2. **Coefficient.** $C = (\Delta t/I_\mathrm{cz})\,K_\mathrm{const}\,K_\mathrm{struct}$.
3. **Centrifugal term.** With $f = \Omega^2R^3/(2GM)$, for the star (at the start and end values of $\Omega$) and for the Sun ($f_\odot$),
$$F_\mathrm{cen} = \left(\frac{c_2^2 + f_\odot}{c_2^2 + f}\right)^{n},$$
$c_2$ = `C_2`, $n$ = `EXCEN`; $R$ from $L = 4\pi R^2\sigma T_\mathrm{eff}^4$.
4. **Torque.** With $\Omega_p = \min(\Omega,\Omega_\mathrm{sat})$ and the exponent $a$ = `EXW`,
$$\Delta\Omega_1 = C\,\Omega_{p,\mathrm{start}}^{\,a-1}\,\Omega_\mathrm{start}\,F_{\mathrm{cen},1},\qquad \Delta\Omega_2 = C\,\Omega_{p,\mathrm{now}}^{\,a-1}\,\Omega_\mathrm{now}\,F_{\mathrm{cen},2},$$
and `WIND2` is the running mean of $\Delta\Omega_2$ over the iterations (set at `IT` = 1, then averaged with the previous value).

**KC's changes.** 2025-05-30: the variables of COMMON `PMMWIND` reordered (the character variable `AWIND` and the logicals moved to the end), the same in all units that share it.

## Questions for the experts

1. **`GL` is never set.** The solar term is `FSUN = 0.5*PMMSOLW**2*CRSUN**3/EXP(CLN*GL)/CMSUN`; `GL` is a local variable that is never assigned (the stellar terms use `CGL`, $\log G$). So $f_\odot$ is computed with an undefined $G$ (probably $10^0 = 1$ if the compiler zeroes it). Was `CGL` meant?
2. **`WIND2` averaging.** For `IT` > 1, `WIND2` is $\tfrac12$(previous `WIND2` + new value), which weights the latest iterations most, not an average over iterations. Intended (as a damping)?
3. **Rates scaled for `LBSCALE`.** With `LBSCALE`, `WFIRST` and `WNOW` are scaled by $\tau/\tau_\odot$ but the final formula multiplies by the unscaled `WOLD` and `OMEGAS`. So the torque goes as $(\Omega\tau)^{a-1}\Omega$. Is that the intended law?
4. **Single-precision literals.** `0.5`, `3.0` in the centrifugal terms are single precision; harmless here, but inconsistent with the rest.

### MCOWIND

The new wind law: saturated power law in $\Omega$, optional Rossby scaling, Matt et al. centrifugal factor (above); otherwise `COWIND`.
