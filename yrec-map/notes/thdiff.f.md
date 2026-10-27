## Explanation

**Purpose.** `THDIFF` solves Burgers' equations for the diffusion of the species in a fully ionised plasma, and returns the diffusion coefficients. Its header: the routine was written by Anne A. Thoul (Institute for Advanced Study), see Thoul et al. (1994, ApJ 421, 828); `LUDCMP` and `LUBKSB` are from Numerical Recipes.

**How it fits.**
- **Inputs:** arguments: the number of species `M` (fluid 1 hydrogen, 2 helium, 3 to `M-1` heavy elements, `M` the electrons), their atomic masses `A` (with `A(M)` = $m_e/m_u$), charges `Z` (`Z(M)` = $-1$), mass fractions `X`, and the Coulomb logarithms `CL(M,M)`.
- **Who calls it:** [[microdiff_cod.f#MICRODIFF_COD|MICRODIFF_COD]] and [[setup_grsett.f#SETUP_GRSETT|SETUP_GRSETT]] (which, for the gravitational settling of hydrogen, uses `-AP(1)` and `-SDEL(2,I)*AT(1)`, or else a fitted polynomial in $X$).
- **What it calls:** [[ludcmp.f#LUDCMP|LUDCMP]] (LU decomposition) and [[lubksb.f#LUBKSB|LUBKSB]] (back substitution).
- **Outputs:** `AP(M)`, `AT(M)`, `AX(M,M)`, the coefficients of the pressure, temperature and concentration gradients in each species' diffusion velocity; also `X(M)`, the electrons' mass fraction, is overwritten.
- **COMMON blocks:** none.

**The method.**
1. Concentrations from mass fractions, normalised to the electrons ($C_M = 1$, by charge neutrality):
   $$C_s = \frac{X_s/A_s}{\sum_{t<M} Z_t X_t/A_t},\qquad C = \sum_s C_s,\qquad \rho \propto \sum_s A_s C_s ,$$
   and the electrons' mass fraction $X_M = A_M / \sum_s A_s C_s$.
2. The collision coefficients, with $\ln\Lambda_{st}$ = `CL`:
   $$K_{st} = \ln\Lambda_{st}\,\sqrt{\frac{A_s A_t}{A_s + A_t}}\;C_s C_t\,Z_s^2 Z_t^2,$$
   and the mass ratios $x_{st} = A_t/(A_s + A_t)$, $y_{st} = A_s/(A_s + A_t)$, $z_{st} = 3y_{st} + 1.3\,x_{st}A_t/A_s$ (`XX`, `Y`, `YY`).
3. The $N = 2M + 2$ equations ($M$ momentum equations, $M$ heat-flow equations, current neutrality and zero mass flow), written as the code's comment does,
   $$\alpha_s\,\frac{d\ln p}{dr} + \nu_s\,\frac{d\ln T}{dr} + \sum_{t \ne 2, M} \gamma_{st}\,\frac{d\ln C_t}{dr} = \sum_t \delta_{st}\,w_t ,$$
   in the $N$ unknowns: $M$ diffusion velocities, $M$ heat fluxes, the electric field and the gravitational term. The matrix $\delta$ is assembled with the coefficients 0.6, 1.5, 1.6, 0.8 and 2.7 of Burgers' equations.
4. `LUDCMP` factorises $\delta$ once; `LUBKSB` solves it for the right-hand sides $\alpha$, $\nu$ and each column of $\gamma$, which gives the coefficients
   $$w_s = A^{(p)}_s\,\frac{d\ln p}{dr} + A^{(T)}_s\,\frac{d\ln T}{dr} + \sum_t A^{(C)}_{st}\,\frac{d\ln C_t}{dr},$$
   multiplied by `KO*AC*CC` $= K_0 \left(\sum_s A_s C_s\right)\left(\sum_s C_s\right)$ with $K_0 = 2$; $\sum_s A_s C_s$ is only proportional to $\rho$ (the comment: "multiplied by $p/K_0$").

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

## Questions for the experts

1. **No check of the array sizes.** The work arrays hold at most `MMAX = 20` species (`NMAX = 42` equations), with no test that `M` ≤ 20.
2. **`X(M)` is overwritten.** The electrons' mass fraction is written into the caller's array. Do the callers expect it?
3. **The normalisation comment.** The comment says the results "must be multiplied by p/K_0", while the code multiplies by `KO*AC*CC` ($K_0 \sum A_s C_s \sum C_s$). Which units do the callers assume?

### THDIFF

Thoul et al. (1994) solution of Burgers' equations: diffusion coefficients for the pressure, temperature and concentration gradients of each species.
