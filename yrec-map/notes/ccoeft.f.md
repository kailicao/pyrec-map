## Explanation

**Purpose.** This file sets up the tridiagonal system for one implicit time step of composition transport by rotationally induced mixing, on an evenly spaced grid in the coordinate $`\chi`$ built by [GETGRID](getgrid.f.md#getgrid) and [MIXGRID](mixgrid.f.md#mixgrid) (the comments' "radius" and "cm" are older than that grid).

**The comments describe an older use.** They speak of an even grid in radius, a spacing in cm, coefficients "COMPUTED IN SR COEFFT" ([lines 25–36](https://github.com/yreclab/yrec/blob/7be4133/src/ccoeft.f#L25-L36)) and "ANGULAR MOMENTUM" at the boundary ([lines 61–63](https://github.com/yreclab/yrec/blob/7be4133/src/ccoeft.f#L61-L63)), but MIXCOM calls the routine with `DCHI`, the spacing of the grid in $`\chi`$, for the composition ([mixcom.f, lines 84–89](https://github.com/yreclab/yrec/blob/7be4133/src/mixcom.f#L84-L89)), with coefficients from CODIFF and MIXGRID, so only the comments are out of date.

**How it fits.**
- **Inputs:** the arguments `COD` (diffusion coefficients, "computed in SR COEFFT" per the comment), `DR` (grid spacing: [MIXCOM](mixcom.f.md#mixcom) passes `DCHI`, the spacing in $`\chi`$), `DT` (time step, s), `ECOMP` (mass fractions at the start of the step on the even grid), `EM` (the masses of the grid's shells, g), `NTOT` (number of points).
- **Who calls it:** [MIXCOM](mixcom.f.md#mixcom).
- **Outputs:** the coefficients `A`, `B`, `C` and right-hand side `D` in [`TRIDI_MOD`](tridi_mod.f.md#tridi_mod), which [CTRIDI](ctridi.f.md#ctridi) then solves (MIXCOM calls only that one); `TRIDI_MOD` is shared with these and with [DCOEFT](dcoeft.f.md#dcoeft) and [GETQUA](getqua.f.md#getqua).

**The method.** The comment gives the equation as
```math
\frac{\partial X}{\partial t} = \frac{1}{4\pi\rho r^2}\frac{\partial}{\partial r}\left(D\,\frac{\partial X}{\partial r}\right),
```
differenced fully implicitly on the grid in $`\chi`$ ($`\Delta r`$ below is `DR`, that is, $`\Delta\chi`$; $`m_i`$ is the shell mass `EM`):
```math
X_i^{n+1} - X_i^{n} = \frac{\Delta t}{\Delta r\,m_i}\left[D_{i+1}\left(X_{i+1}^{n+1} - X_i^{n+1}\right) - D_i\left(X_i^{n+1} - X_{i-1}^{n+1}\right)\right],
```
where `COD(I)` is $`D`$ at the interface between points $`i-1`$ and $`i`$ (written $`D_{i-1/2}`$ in the comment). So, with $`f_i = \Delta t/(\Delta r\, m_i)`$:
```math
a_i = -f_i D_i, \qquad b_i = 1 + f_i (D_i + D_{i+1}), \qquad c_i = -f_i D_{i+1}, \qquad d_i = X_i^n.
```
At both ends there is no flux across the boundary: $`a_1 = 0`$, $`b_1 = 1 + f_1 D_2`$; $`c_N = 0`$, $`b_N = 1 + f_N D_N`$.

The scheme conserves mass: [CODIFF](codiff.f.md#codiff) includes $`4\pi`$ in `COD2`, and MIXGRID multiplies the coefficient by $`\rho r^2\,d\chi/dr`$, so `COD` is $`4\pi\rho r^2 D\,d\chi/dr`$, and the flux between shells is `COD` times the difference in $`X`$ over $`\Delta\chi`$.

**Changed since `rp_1`.** Declarations only: `/TRIDI/` to its module, the unused `/CCOUT/` and `/LUOUT/` dropped, `IMPLICIT NONE`.

### CCOEFT

Builds the implicit tridiagonal diffusion system for composition on the even grid in $`\chi`$, with zero-flux boundaries, into `TRIDI_MOD`.
