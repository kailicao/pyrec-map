## Explanation

**Purpose.** This file gives the change of the surface convection zone's angular velocity over a time step due to magnetized-wind angular-momentum loss, with the older "Kawaler-type" wind law and a saturation threshold. It is used when the newer Matt et al. law (`LMWIND`) is off.

**How it fits.**
- **Inputs:** the arguments `BL` ($`\log L/L_\odot`$), `TEFFL`, `SMASS` ($`M/M_\odot`$), `DT` (the time step), `HICZ` (the moment of inertia of the surface convection zone), `OMEGAS` (the surface $`\Omega`$ after the previous iteration), `WOLD` (at the start of the step), `IT` (the iteration); `WMAX`, `EXMD`, `EXW`, `EXR`, `EXM`, `CONSTFACTOR` in [`NMLPAR_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/nmlpar_mod.f#L32-L279) (set in [PARMIN](https://github.com/yreclab/yrec/blob/7be4133/src/parmin.f#L16-L1489) from the input index "ALFA," per the comment); `TAUCZ` (the convective overturn time) in [`OVRTRN_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/ovrtrn_mod.f#L19-L30); the solar constants in [`CONSTANTS_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/constants_mod.f#L37-L75).
- **Who calls it:** [MCOWIND](mcowind.f.md#mcowind), when `LMWIND` is false ("run old windlaw").
- **Outputs:** `WIND1`, `WIND2`, the change of $`\Omega`$ over the step computed with $`\Omega`$ at its start and at its end. The comment says they enter the diffusion equations and are averaged: [SECULR](https://github.com/yreclab/yrec/blob/7be4133/src/seculr.f#L6-L532), which calls MCOWIND, passes them to [DCOEFT](dcoeft.f.md#dcoeft) or [DADCOEFT](dadcoeft.f.md#dadcoeft), where the surface boundary takes $`-\tfrac12(\mathtt{WIND1}+\mathtt{WIND2})`$ times the moment of inertia.

**The method.**
1. **Saturation.** If `WMAX` $`\gt{} 1`$, it is read as $`\Omega_\mathrm{sat,\odot}\,\tau_\odot`$ and $`\Omega_\mathrm{sat} = \mathtt{WMAX}/\tau_\mathrm{cz}`$ (MHP 3/09; the run stops if $`\tau_\mathrm{cz}`$ is not defined, with exit code 1 and the message also in the `.short` file); otherwise $`\Omega_\mathrm{sat} = \mathtt{WMAX}`$. Unlike [WIND](wind.f.md#wind), the reinterpretation does not depend on `LINSTB`.

    > **Question** ([lines 80–96](https://github.com/yreclab/yrec/blob/7be4133/src/cowind.f#L80-L96)). **The test `WMAX > 1`.** A real $`\Omega_\mathrm{sat}`$ is far below 1 rad $`\mathrm{s}^{-1}`$, so the test works as a switch; but the Physics namelist page describes `WMAX` only as an angular velocity in $`\mathrm{rad/s}`$ (and `WMAX_SUN`, which PARMIN converts for the new law only), not this second meaning. Should the documentation describe it, or a separate switch replace it?

2. The radius from $`L`$ and $`T_\mathrm{eff}`$: $`\log R = \tfrac12(\log(L/L_\odot) + \log L_\odot - \log 4\pi - \log\sigma - 4\log T_\mathrm{eff})`$, in $`\mathrm{cm}`$.
3. The comment's law, $`dJ/dt \propto K\,(\dot M/10^{-14})^{a}\,\Omega^{n}\,(M/M_\odot)^{c}(R/R_\odot)^{b}`$, gives
   
   $$\displaystyle C = \frac{\Delta t}{I\_\mathrm{CZ}}\\,K\left(\frac{\dot M}{10^{-14}\\,M\_\odot\\,\mathrm{yr}^{-1}}\right)^{a}\left(\frac{R}{R\_\odot}\right)^{b}\left(\frac{M}{M\_\odot}\right)^{c},$$
   
   $$\displaystyle \Delta\Omega = C\\,\min(\Omega, \Omega\_\mathrm{sat})^{\\,n-1}\\,\Omega,$$
   
   with $`K`$ = `CONSTFACTOR`, $`a`$ = `EXMD`, $`b`$ = `EXR`, $`c`$ = `EXM`, $`n`$ = `EXW`. So $`\Delta\Omega \propto \Omega^n`$ below saturation and $`\propto \Omega\,\Omega_\mathrm{sat}^{n-1}`$ above.
4. `WIND1` uses `WOLD`. `WIND2` uses `OMEGAS`; from the second iteration on, it is the mean of its previous value and the new one, which damps the iteration.

    > **Question** ([lines 111–115](https://github.com/yreclab/yrec/blob/7be4133/src/cowind.f#L111-L115)). **The damping of `WIND2`.** Averaging the previous `WIND2` with the new value at each iteration means the converged `WIND2` mixes values from several iterations, weighting the latest most. Is this only for stability, and does it converge to the value at the end of the step?

**Design.** The mass-loss rate is fixed: `DMDOT = 2.0D-14` ($`M_\odot\,\mathrm{yr}^{-1}`$), so the factor $`(\dot M/10^{-14})^a`$ is the constant $`2^a`$.

> **Question** ([lines 99–106](https://github.com/yreclab/yrec/blob/7be4133/src/cowind.f#L99-L106)). **A fixed mass-loss rate.** $`\dot M`$ is hard-coded to $`2\times10^{-14}\,M_\odot\,\mathrm{yr}^{-1}`$, not taken from the model's mass-loss rate (`DMDT0`, now in `NMLPAR_MOD`). Is it intended as a calibration constant, absorbed into `CONSTFACTOR`?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`; the unused `/DEUTER/` is gone, and the wind parameters this file does not use (`EXTAU`, `EXL`, `EXPR`, `EXCEN`, `C_2`) are now namelist variables in `NMLPAR_MOD`, shared by all its users, which settles the former question 3 on unused inputs.

**Changed since `a8a5950`.** The error stop when $`\tau_\mathrm{cz}`$ is not defined now also writes its message to the `.short` file (`ISHORT`, through [`IOUNITS_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/iounits_mod.f#L19-L54)), and ends with `STOP 1` instead of a bare `STOP`, so that a failed run no longer exits with status 0 (`KNOWN_ISSUES.md`, issue 38).

### COWIND

Older wind law: $`\Delta\Omega = (\Delta t/I_\mathrm{CZ})\,K\,(\dot M/10^{-14})^{a}(R/R_\odot)^{b}(M/M_\odot)^{c}\,\min(\Omega,\Omega_\mathrm{sat})^{n-1}\,\Omega`$, at the start (`WIND1`) and end (`WIND2`) of the step; saturation optionally scaled by the overturn time.
