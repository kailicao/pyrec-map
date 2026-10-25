## Explanation

**Purpose.** Removes angular momentum from the surface convection zone by a magnetized stellar wind over one time step. If `LMWIND` is false it hands over to the older wind law in [[wind.f#WIND|WIND]]; otherwise it uses the wind law of Matt et al. (2012), as G. Somers' comments (3/17) call it, with a centrifugal correction from Matt et al. (2012, ApJ 754, L26; MHP 8/17) and optional Rossby scaling.

**How it fits.**
- **Inputs:** $\log L/L_\odot$ (`BL`), the step `DELTS` (s), the masses at the top and bottom of the convection zone (`HSTOP`, `HSBOT`), its shells `JSTART..JEND`, the surface angular velocity `OMEGAS`, the mass in solar units `SMASS`, $\log T_\mathrm{eff}$ (`TEFFL`), the zone's moment of inertia `HICZ`, and the specific angular momentum `HJM`. Wind parameters come from `/CWIND/` and `/PMMWIND/` (set by [[parmin.f#PARMIN|PARMIN]]); the convective turnover times at the start and end of the step and the fraction of the step (`TAUCZ0`, `TAUCZ`, `FRACSTEP`) from `/OVRTRN/` (`AMCALC` also reads the photospheric pressures there).
- **Who calls it:** [[getw.f#GETW|GETW]] and [[seculr.f#SECULR|SECULR]].
- **What it calls:** [[wind.f#WIND|WIND]] (old law) or [[amcalc.f#AMCALC|AMCALC]], which sets the structure factor `STRUCTFACTOR` in `/CWIND/`.
- **Output:** `HJM` of the convection zone's shells, reduced.
- **COMMON blocks:** `/CWIND/` (shared with AMCALC, WIND, COWIND, MCOWIND, MIDMOD, GETW, SECULR and the output routines), `/PMMWIND/` (with AMCALC, MCOWIND, PARMIN), `/OVRTRN/`, `/CONST/`, `/CONST1/`, `/CONST2/`, `/CONST3/`. `/ROT/` is declared, and its first element is `WNEW`, the name the routine uses for the new angular velocity; so MWIND overwrites `WNEW` in `/ROT/` (question 5). `/DEUTER/` is declared but not used.

**The method.**
1. **Rossby scaling** (`LROSSBY`): the turnover time is interpolated in the step, $\tau = \tau_0 + f\,(\tau_1 - \tau_0)$ (`FRACSTEP`). With `LBSCALE`, the rotation rate used in the saturation term is scaled, $\Omega' = \Omega\,\tau/\tau_\odot$; otherwise the saturation threshold is, $\Omega_\mathrm{sat}' = \Omega_\mathrm{sat}\,\tau_\odot/\tau$.
2. **The structure factor** from `AMCALC`: $S = (M/M_\odot)^{a_M}\,(R/R_\odot)^{a_R}\,(L/L_\odot)^{a_L}\,(P_\mathrm{phot}/P_{\mathrm{phot},\odot})^{a_P}\,(\tau/\tau_\odot)^{a_\tau}$.
3. **The centrifugal factor,** relative to the Sun, with $f = \Omega^2 R^3/(2GM)$ and $R$ from $L = 4\pi R^2\sigma T_\mathrm{eff}^4$:
$$F_\mathrm{cen} = \left(\frac{c_2^2 + f_\odot}{c_2^2 + f}\right)^{e}\quad(c_2 = \texttt{C\_2},\ e = \texttt{EXCEN}).$$
4. **The step.** The convection zone spins down as
$$\Omega_\mathrm{new} = \Omega_s - \frac{\Delta t}{I_\mathrm{cz}}\;K\,S\;\Omega\;\min(\Omega', \Omega_\mathrm{sat})^{\,a_\Omega - 1}\;F_\mathrm{cen},$$
with $K$ = `CONSTFACTOR`, $a_\Omega$ = `EXW`. If the first guess of the change exceeds $\Omega_s$, the step is split into $\lfloor \Delta\Omega/\Omega_s \rfloor + 1$ substeps, so $\Omega$ stays positive. In each, $\Omega$ in the loss term is iterated as the mean of the start and the previous end value (the mean of the explicit and implicit solutions), until the relative change is below $10^{-6}$ or 20 iterations.
5. **The loss.** $\Delta j = (\Omega_s - \Omega_\mathrm{new})\,I_\mathrm{cz}/\Delta M_\mathrm{cz}$ is subtracted from every shell of the zone.

**KC's changes.** 2025-05-30: the elements of `/PMMWIND/` reordered (the character variable `AWIND` moved to the end); 2025-05-31: the unused argument `SJTOT` removed from the routine and from the call to `WIND`.

## Questions for the experts

1. **`TCZ` undefined.** With `LBSCALE` true but `LROSSBY` false, the loop uses `TCZ`, which is set only in the `LROSSBY` branch (it then keeps a value from an earlier call, or none). Should `LBSCALE` require `LROSSBY`?
2. **Silent non-convergence.** After 20 iterations the loop continues with the last value without a warning.
3. **An outdated comment.** "The constant and exponents are set in PARMIN based on the input index ALFA" describes the old law. Does `PARMIN` still use `ALFA` for the Matt et al. law?
4. **Two masses.** `SMASS` is in solar masses (it is multiplied by `CMSUN` in $f$, and raised to `EXM` in `AMCALC`). The argument list does not say so; worth a comment.
5. **`WNEW` overwritten in `/ROT/`.** The local name `WNEW` is also the first element of `/ROT/`, the input parameter that [[starin.f#STARIN|STARIN]] uses (with `LWNEW`) to start a model in solid-body rotation at $\Omega =$ `WNEW`. Every call of MWIND (and of [[wind.f#WIND|WIND]], which does the same) overwrites it with the latest surface angular velocity. STARIN is called again for each run in the main program's `DO 200 NK = 1, NUMRUN` loop, so a later run with `LWNEW` true would start from the wind's last value, not the input. Should the local variable be renamed?
