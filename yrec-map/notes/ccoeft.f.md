## Explanation

**Purpose.** This file sets up the tridiagonal system for one implicit time step of composition transport by rotationally induced mixing, on an evenly spaced grid in the coordinate $\chi$ built by [[getgrid.f#GETGRID|GETGRID]] and [[mixgrid.f#MIXGRID|MIXGRID]] (the comments' "radius" and "cm" are older than that grid).

**How it fits.**
- **Inputs:** the arguments `COD` (diffusion coefficients, "computed in SR COEFFT" per the comment), `DR` (grid spacing: [[mixcom.f#MIXCOM|MIXCOM]] passes `DCHI`, the spacing in $\chi$), `DT` (time step, s), `ECOMP` (mass fractions at the start of the step on the even grid), `EM` (the masses of the grid's shells, g), `NTOT` (number of points).
- **Who calls it:** [[mixcom.f#MIXCOM|MIXCOM]].
- **Outputs:** the coefficients `A`, `B`, `C` and right-hand side `D` in [[tridi_mod.f#TRIDI_MOD|`TRIDI_MOD`]], which [[ctridi.f#CTRIDI|CTRIDI]] then solves (MIXCOM calls only that one); `TRIDI_MOD` is shared with these and with [[dcoeft.f#DCOEFT|DCOEFT]] and [[getqua.f#GETQUA|GETQUA]].

**The method.** The comment gives the equation as
$$\frac{\partial X}{\partial t} = \frac{1}{4\pi\rho r^2}\frac{\partial}{\partial r}\left(D\,\frac{\partial X}{\partial r}\right),$$
differenced fully implicitly on the grid in $\chi$ ($\Delta r$ below is `DR`, that is, $\Delta\chi$; $m_i$ is the shell mass `EM`):
$$X_i^{n+1} - X_i^{n} = \frac{\Delta t}{\Delta r\,m_i}\left[D_{i+1}\left(X_{i+1}^{n+1} - X_i^{n+1}\right) - D_i\left(X_i^{n+1} - X_{i-1}^{n+1}\right)\right],$$
where `COD(I)` is $D$ at the interface between points $i-1$ and $i$ (written $D_{i-1/2}$ in the comment). So, with $f_i = \Delta t/(\Delta r\, m_i)$:
$$a_i = -f_i D_i, \qquad b_i = 1 + f_i (D_i + D_{i+1}), \qquad c_i = -f_i D_{i+1}, \qquad d_i = X_i^n.$$
At both ends there is no flux across the boundary: $a_1 = 0$, $b_1 = 1 + f_1 D_2$; $c_N = 0$, $b_N = 1 + f_N D_N$.

The scheme conserves mass: [[codiff.f#CODIFF|CODIFF]] includes $4\pi$ in `COD2`, and MIXGRID multiplies the coefficient by $\rho r^2\,d\chi/dr$, so `COD` is $4\pi\rho r^2 D\,d\chi/dr$, and the flux between shells is `COD` times the difference in $X$ over $\Delta\chi$.

**Changed since `rp_1`.** Declarations only: `/TRIDI/` to its module, the unused `/CCOUT/` and `/LUOUT/` dropped, `IMPLICIT NONE`.

## Questions for the experts

1. **Outdated comments.** The comments speak of an even grid in radius, a spacing in cm, coefficients "computed in SR COEFFT" and "angular momentum" at the boundary, while the routine works on the grid in $\chi$ with coefficients from CODIFF and MIXGRID, for composition. Should the comments be updated?

### CCOEFT

Builds the implicit tridiagonal diffusion system for composition on the even grid in $\chi$, with zero-flux boundaries, into `TRIDI_MOD`.
