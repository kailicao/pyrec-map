## Explanation

**Purpose.** `MCOWIND` returns the change in the angular velocity of the surface convection zone caused by magnetized-wind angular-momentum loss over a (diffusion) time step. It implements the newer wind law (G. Somers 3/17, "PMM-style", by its comment after van Saders and Pinsonneault, probably) with saturation, an optional Rossby scaling and the centrifugal correction of Matt et al. (2012, ApJ 754, L26). When the new law is off (`LMWIND` false) it hands over to the older [[cowind.f#COWIND|`COWIND`]].

**How it fits.**
- **Who calls it:** only [[seculr.f#SECULR|`SECULR`]], in the angular-momentum transport, once per iteration `IT` of the diffusion solution.
- **Inputs:** `BL` ($\log L/L_\odot$), `DT` (the diffusion step, s), `HICZ` (moment of inertia of the surface convection zone), `IT`, `OMEGAS` (surface $\Omega$ at the end of the previous iteration), `WOLD` (surface $\Omega$ at the start of the step), `SMASS` ($M/M_\odot$), `TEFFL`.
- **Outputs:** `WIND1` and `WIND2`, the changes in $\Omega$ over the step computed with $\Omega$ at the start and at the end of the step; the caller averages them (its comment).
- **Calls:** [[cowind.f#COWIND|`COWIND`]] (old law) or [[amcalc.f#AMCALC|`AMCALC`]], which returns `STRUCTFACTOR` (an output argument, formerly in `CWIND`) from $M$, $L$ and $T_\mathrm{eff}$.
- **Modules:** `NMLPAR_MOD` (the run's parameters, from [[parmin.f#PARMIN|`PARMIN`]]: the wind law's `WMAX`, `EXW`, `CONSTFACTOR`, `EXCEN`, formerly in `CWIND`, and `LMWIND`, `LROSSBY`, `LBSCALE`, the solar values `PMMSOLW`, `PMMSOLTAU`, formerly in `PMMWIND`), `OVRTRN_MOD` (`TAUCZ`, `TAUCZ0`, `FRACSTEP`: the convective turnover time at the start and end of the step and the fraction of the step reached), and `CONSTANTS_MOD` (the constants, with `C_2`, set once in `PARMIN`).

**The method.**
1. **Saturation.** With Rossby scaling, the turnover time is interpolated in the step, $\tau = \tau_0 + f\,(\tau_1 - \tau_0)$, and the saturation rate is $\Omega_\mathrm{sat} = \Omega_\mathrm{max}\,\tau_\odot/\tau$. With the extra field scaling as well (`LBSCALE`, which acts only with Rossby scaling) the rates $\Omega$ and $\Omega_\mathrm{sat}$ are multiplied by $\tau/\tau_\odot$. Otherwise $\Omega_\mathrm{sat}$ = `WMAX`.

    > **Question** ([[#L105-L108]]). **$\tau_\mathrm{cz}$ = 0.** With `LROSSBY`, `WSAT = WMAX*PMMSOLTAU/TCZ` divides by the interpolated turnover time, which is 0 when `TAUCZ` and `TAUCZ0` are both 0, as for a star with no surface convection zone; MWIND has the same division ([[mwind.f#q1]]). Is a model without a surface convection zone kept from reaching here, or should the saturation be skipped when `TCZ` = 0?

    > **Question** ([[#L110-L114]]; [[#L159-L162]]). **Rates scaled for `LBSCALE`.** With `LBSCALE`, `WFIRST` and `WNOW` are scaled by $\tau/\tau_\odot$, but the final formula multiplies by the unscaled `WOLD` and `OMEGAS`, so the torque goes as $(\Omega\tau)^{a-1}\Omega$ ([[mwind.f#MWIND|MWIND]] does the same). Is that the intended law?

2. **Coefficient.** $C = (\Delta t/I_\mathrm{cz})\,K_\mathrm{const}\,K_\mathrm{struct}$.
3. **Centrifugal term.** With $f = \Omega^2R^3/(2GM)$, for the star (at the start and end values of $\Omega$) and for the Sun ($f_\odot$),
$$F_\mathrm{cen} = \left(\frac{c_2^2 + f_\odot}{c_2^2 + f}\right)^{n},$$
$c_2$ = `C_2`, $n$ = `EXCEN`; $R$ from $L = 4\pi R^2\sigma T_\mathrm{eff}^4$. The literals `0.5` and `3.0` in these lines are single precision but exact in binary, so the results are those of double precision ([[#L150-L154]]; settled from the code, Nov 9, 2026).
4. **Torque.** With $\Omega_p = \min(\Omega,\Omega_\mathrm{sat})$ and the exponent $a$ = `EXW`,
$$\Delta\Omega_1 = C\,\Omega_{p,\mathrm{start}}^{\,a-1}\,\Omega_\mathrm{start}\,F_{\mathrm{cen},1},\qquad \Delta\Omega_2 = C\,\Omega_{p,\mathrm{now}}^{\,a-1}\,\Omega_\mathrm{now}\,F_{\mathrm{cen},2},$$
and `WIND2` is the running mean of $\Delta\Omega_2$ over the iterations (set at `IT` = 1, then averaged with the previous value).

    > **Question** ([[#L165-L169]]). **`WIND2` averaging.** For `IT` > 1, `WIND2` is $\tfrac12$(previous `WIND2` + new value), which weights the latest iterations most, not an average over iterations. Is it intended, as a damping?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`; `CWIND` and `PMMWIND` retired (`C_2` to `CONSTANTS_MOD`, the rest to `NMLPAR_MOD`), so `STRUCTFACTOR` is now returned by `AMCALC` as an argument; the unused `DEUTER` dropped. No question settled: `GL` is still a local that is never set.

**Changed since `a8a5950`.** The Sun's centrifugal term `FSUN` now divides by $G$ (`CGL`, as the star's terms do) instead of `EXP(CLN*GL)` with `GL` an unset local, and `GL` is no longer declared; the code's comment puts the old $f_\odot$ about $1.5\times10^7$ too small. This settles former question 1; former questions 2–4 are now 1–3.

### MCOWIND

The new wind law: saturated power law in $\Omega$, optional Rossby scaling, Matt et al. centrifugal factor (above); otherwise `COWIND`.
