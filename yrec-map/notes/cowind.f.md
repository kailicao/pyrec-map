## Explanation

**Purpose.** This file gives the change of the surface convection zone's angular velocity over a time step due to magnetized-wind angular-momentum loss, with the older "Kawaler-type" wind law and a saturation threshold. It is used when the newer Matt et al. law (`LMWIND`) is off.

**How it fits.**
- **Inputs:** the arguments `BL` ($\log L/L_\odot$), `TEFFL`, `SMASS` ($M/M_\odot$), `DT` (the time step), `HICZ` (the moment of inertia of the surface convection zone), `OMEGAS` (the surface $\Omega$ after the previous iteration), `WOLD` (at the start of the step), `IT` (the iteration); `WMAX`, `EXMD`, `EXW`, `EXR`, `EXM`, `CONSTFACTOR` in [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] (set in [[parmin.f#PARMIN|PARMIN]] from the input index "ALFA", per the comment); `TAUCZ` (the convective overturn time) in [[ovrtrn_mod.f#OVRTRN_MOD|`OVRTRN_MOD`]]; the solar constants in [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]].
- **Who calls it:** [[mcowind.f#MCOWIND|MCOWIND]], when `LMWIND` is false ("run old windlaw").
- **Outputs:** `WIND1`, `WIND2`, the change of $\Omega$ over the step computed with $\Omega$ at its start and at its end. The comment says they enter the diffusion equations and are averaged: [[seculr.f#SECULR|SECULR]], which calls MCOWIND, passes them to [[dcoeft.f#DCOEFT|DCOEFT]] or [[dadcoeft.f#DADCOEFT|DADCOEFT]], where the surface boundary takes $-\tfrac12(\mathtt{WIND1}+\mathtt{WIND2})$ times the moment of inertia.

**The method.**
1. **Saturation.** If `WMAX` $> 1$, it is read as $\Omega_\mathrm{sat,\odot}\,\tau_\odot$ and $\Omega_\mathrm{sat} = \mathtt{WMAX}/\tau_\mathrm{CZ}$ (MHP 3/09; the run stops if $\tau_\mathrm{CZ}$ is not defined); otherwise $\Omega_\mathrm{sat} = \mathtt{WMAX}$.
2. The radius from $L$ and $T_\mathrm{eff}$: $\log R = \tfrac12(\log(L/L_\odot) + \log L_\odot - \log 4\pi - \log\sigma - 4\log T_\mathrm{eff})$, in cm.
3. The comment's law, $dJ/dt \propto K\,(\dot M/10^{-14})^{a}\,\Omega^{n}\,(M/M_\odot)^{c}(R/R_\odot)^{b}$, gives
$$C = \frac{\Delta t}{I_\mathrm{CZ}}\,K\left(\frac{\dot M}{10^{-14}\,M_\odot\,\mathrm{yr}^{-1}}\right)^{a}\left(\frac{R}{R_\odot}\right)^{b}\left(\frac{M}{M_\odot}\right)^{c},$$
$$\Delta\Omega = C\,\min(\Omega, \Omega_\mathrm{sat})^{\,n-1}\,\Omega,$$
with $K$ = `CONSTFACTOR`, $a$ = `EXMD`, $b$ = `EXR`, $c$ = `EXM`, $n$ = `EXW`. So $\Delta\Omega \propto \Omega^n$ below saturation and $\propto \Omega\,\Omega_\mathrm{sat}^{n-1}$ above.
4. `WIND1` uses `WOLD`. `WIND2` uses `OMEGAS`; from the second iteration on, it is the mean of its previous value and the new one, which damps the iteration.

**Design.** The mass-loss rate is fixed: `DMDOT = 2.0D-14` ($M_\odot$ yr$^{-1}$), so the factor $(\dot M/10^{-14})^a$ is the constant $2^a$.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`; the unused `/DEUTER/` is gone, and the wind parameters this file does not use (`EXTAU`, `EXL`, `EXPR`, `EXCEN`, `C_2`) are now namelist variables in `NMLPAR_MOD`, shared by all its users, which settles the former question 3 on unused inputs.

## Questions for the experts

1. **A fixed mass-loss rate.** $\dot M$ is hard-coded to $2\times10^{-14}\,M_\odot$ yr$^{-1}$, not taken from the model's mass-loss rate (`DMDT0`, now in `NMLPAR_MOD`). Intended as a calibration constant?
2. **The damping of `WIND2`.** Averaging the previous `WIND2` with the new value at each iteration means the converged `WIND2` mixes values from several iterations. Is this only for stability, and does it converge to the right value?
3. **The test `WMAX > 1`.** A real $\Omega_\mathrm{sat}$ is far below 1 rad s$^{-1}$, so the test works as a switch; is that documented for users?

### COWIND

Older wind law: $\Delta\Omega = (\Delta t/I_\mathrm{CZ})\,K\,(\dot M/10^{-14})^{a}(R/R_\odot)^{b}(M/M_\odot)^{c}\,\min(\Omega,\Omega_\mathrm{sat})^{n-1}\,\Omega$, at the start (`WIND1`) and end (`WIND2`) of the step; saturation optionally scaled by the overturn time.
