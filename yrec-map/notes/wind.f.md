## Explanation

**Purpose.** `WIND` removes angular momentum from the surface convection zone by a magnetized wind, "a Weber–Davis magnetic wind model" (its comment), over one time step. It is the older loss law; [[mwind.f#MWIND|MWIND]] calls it when `LMWIND` is off, and otherwise uses its own law.

**How it fits.**
- **Inputs:** $\log L$ (`BL`), the time step `DELTS` (s), the convection zone's mass range (`HSBOT`, `HSTOP`) and shells (`JSTART`, `JEND`), the switch `LJDOT`, the surface rate `OMEGAS`, the mass `SMASS` (in solar masses, probably), $\log T_\mathrm{eff}$, the zone's moment of inertia `HICZ`. Through modules: the law's constant and exponents (`NMLPAR_MOD`, formerly `COMMON/CWIND/`: `CONSTFACTOR`, `EXMD`, `EXW`, `EXR`, `EXM`, the saturation `WMAX`, set by [[parmin.f#PARMIN|PARMIN]]); the overturn time `TAUCZ` (`OVRTRN_MOD`, from [[gettau.f#GETTAU|GETTAU]]); `LINSTB` (`NMLPAR_MOD`, formerly `COMMON/ROT/`).
- **Who calls it:** only [[mwind.f#MWIND|MWIND]].
- **Output:** `HJM`, each shell's specific angular momentum in the zone, reduced.
- **Modules:** `NMLPAR_MOD`, `OVRTRN_MOD`, `CONSTANTS_MOD`, `DIMENSIONS_MOD`.

**The method.**
1. **Saturation.** $\Omega_\mathrm{sat}$ = `WMAX`; but with angular momentum transport (`LINSTB`) and `WMAX` > 1, `WMAX` is read as $\Omega_\mathrm{sat}\tau_\mathrm{cz}$ for the Sun, and $\Omega_\mathrm{sat} = $ `WMAX`$/\tau_\mathrm{cz}$ (MHP 3/09); the run stops if $\tau_\mathrm{cz} \le 1$.
2. **The loss law.** With $R = \sqrt{L/(4\pi\sigma T_\mathrm{eff}^4)}$ and the fixed mass-loss rate $\dot M = 2\times10^{-14}\,M_\odot$/yr,
   $$I\,\frac{d\Omega}{dt} = -K\left(\frac{\dot M}{10^{-14}}\right)^{a}\left(\frac{R}{R_\odot}\right)^{c} M^{d}\;\Omega\,\min(\Omega, \Omega_\mathrm{sat})^{\,b-1},$$
   with $K$ = `CONSTFACTOR`, $a$ = `EXMD`, $b$ = `EXW`, $c$ = `EXR`, $d$ = `EXM`.
3. **Integration.** If one explicit step would remove more than $\Omega$, the step is split into `NSTEP` substeps. In each, $\Omega_\mathrm{new}$ is found by iteration: the loss is evaluated at the mean of the start and the previous estimate, until the relative change is below $10^{-6}$ (at most 21 evaluations).
4. **Removal.** $\Delta j = (\Omega_\mathrm{s} - \Omega_\mathrm{new})\,I_\mathrm{cz}/\Delta M_\mathrm{cz}$, with $\Delta M_\mathrm{cz}$ = `HSTOP - HSBOT`, is subtracted from every shell of the zone.

**KC's changes.** The unused argument `SJTOT` was removed (2025-05-31).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/CWIND/` and `/ROT/` to `NMLPAR_MOD`, `/OVRTRN/` to `OVRTRN_MOD`, the constants to `CONSTANTS_MOD`; the unused `/DEUTER/` dropped), `IMPLICIT NONE`; question 1 stands, `WNEW` now being `NMLPAR_MOD`'s.

## Questions for the experts

1. **`WNEW` overwrites a module variable.** `WNEW`, the iterated new rate, is also `NMLPAR_MOD`'s `WNEW` (formerly the first element of COMMON `ROT`), where it is the rate for converting a model to solid-body rotation (used by [[starin.f#STARIN|STARIN]] with `LWNEW`). Each call of `WIND` (and of `MWIND`, which does the same) changes it. A later run of the same job that sets up rotation from `WNEW` would get the last wind rate. A bug?
2. **A fixed mass-loss rate.** `DMDOT = 2.0D-14` is hard-coded, so the factor $(\dot M/10^{-14})^{a}$ is a constant $2^{a}$. Is this meant?
3. **No convergence check.** After 21 evaluations without convergence, the last estimate is used without a message.
4. **The saturation's units.** `WMAX > 1` switches the meaning of `WMAX` (rad/s or rad/s × s). A rate above 1 rad/s is unphysical, so the test works, but a separate switch would be clearer.

### WIND

The older wind braking law: $I\,d\Omega/dt \propto \Omega\,\min(\Omega,\Omega_\mathrm{sat})^{b-1}$ with fixed exponents, integrated over the step and taken from the surface convection zone's specific angular momentum.
