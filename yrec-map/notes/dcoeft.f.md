## Explanation

**Purpose.** This file sets up the tridiagonal system for one implicit step of angular-momentum transport by diffusion (and, with `LDIFAD`, a simple advective term), on the even grid in the coordinate $`\chi`$ (`DR` is `DCHI`, set by [ROTGRID](https://github.com/yreclab/yrec/blob/7be4133/src/rotgrid.f#L2-L285)). It is the solver setup used when the band solver of [DADCOEFT](dadcoeft.f.md#dadcoeft) is not.

**How it fits.**
- **Inputs:** the arguments `ECOD` (the diffusion coefficients at the grid points), `DR`, `DT`, `EI` (moments of inertia), `EJ` (angular momenta), `EW` ($`\Omega`$), `NTOT`, `WIND1`, `WIND2` (the wind's change of $`\Omega`$, explicit and implicit), `LFIX` (fixed surface $`\Omega`$); with `LDIFAD` (a setting in [`NMLPAR_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/nmlpar_mod.f#L32-L279), formerly `/VARFC/`), the advective and diffusive coefficients `ECOD3`, `ECOD4` from [`DIFAD_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/difad_mod.f#L19-L31). ROTGRID has already multiplied `ECOD` by $`\rho r^2\,(d\chi/dr)`$ and by the shell's $`I/\Delta m`$ ($`4\pi`$ is in CODIFF), and with `LDIFAD` added the composition coefficient `ECOD2` to `ECOD4`.
- **Who calls it:** [SECULR](https://github.com/yreclab/yrec/blob/7be4133/src/seculr.f#L6-L532).
- **Outputs:** `A`, `B`, `C`, `D` in [`TRIDI_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/tridi_mod.f#L19-L35), solved next by [TRIDIA](tridia.f.md#tridia); also `GAMA(NTOT)`, set to the wind's loss of angular momentum, $`\Delta J = -\tfrac12(W_1 + W_2)\,I_N`$, which TRIDIA reads before overwriting it ([line 82](https://github.com/yreclab/yrec/blob/7be4133/src/dcoeft.f#L82); [tridia.f, line 22](https://github.com/yreclab/yrec/blob/7be4133/src/tridia.f#L22)). `GAMA` is the solver's work array, so this is a message passed through work space, which an explicit argument would make clearer.

**The method.** The header gives
```math
\frac{\partial\Omega}{\partial t} = \frac{1}{4\pi\rho r^2}\,\frac{1}{I/M}\,\frac{\partial}{\partial r}\left(D\frac{\partial\Omega}{\partial r}\right),
```
differenced implicitly with $`f_i = \Delta t/(\Delta r\,I_i)`$:
```math
a_i = -f_i D_i, \qquad b_i = 1 + f_i(D_i + D_{i+1}), \qquad c_i = -f_i D_{i+1}, \qquad d_i = \Omega_i^n,
```
with no flux at the centre and at the surface (or a fixed surface $`\Omega`$ if `LFIX`). The wind enters the surface: $`d_N = \Omega_N(1 + \Delta J/J_N)`$. With `LDIFAD`, $`D`$ is `ECOD4` and centred advective terms $`\pm\tfrac12\Delta t\,\mathtt{ECOD3}/I_i`$ are added, in conservative form: each interface's flux, $`\tfrac12\mathtt{ECOD3}_i(\Omega_{i-1}+\Omega_i)`$, enters both neighbouring rows, and none crosses the centre or the surface. This `LDIFAD` branch ([lines 108–139](https://github.com/yreclab/yrec/blob/7be4133/src/dcoeft.f#L108-L139)) is unused?: SECULR calls DCOEFT only when `LDIFAD` is off and calls [DADCOEFT](dadcoeft.f.md#dadcoeft) otherwise ([seculr.f, lines 390–404](https://github.com/yreclab/yrec/blob/7be4133/src/seculr.f#L390-L404); settled from the code, Nov 9, 2026). Its advective factor, `FACTA = 0.5D0*DT/EI(I)` ([line 116](https://github.com/yreclab/yrec/blob/7be4133/src/dcoeft.f#L116), [line 122](https://github.com/yreclab/yrec/blob/7be4133/src/dcoeft.f#L122), [line 130](https://github.com/yreclab/yrec/blob/7be4133/src/dcoeft.f#L130)), has no $`1/\Delta r`$, unlike DADCOEFT's `0.5D0*DT/EI(1)/DR` ([dadcoeft.f, line 305](https://github.com/yreclab/yrec/blob/7be4133/src/dadcoeft.f#L305)).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

### DCOEFT

Builds the implicit tridiagonal system for $`\Omega`$ on the even grid (diffusion, optionally a centred advective term), with zero-flux or fixed-$`\Omega`$ boundaries and the wind's loss at the surface.
