## Explanation

**Purpose.** Finds how much each shell of a rotating star is flattened. Its comment: "SHAPE FINDS THE DISTORTION OF A GIVEN SHELL FROM SPHERICAL SYMMETRY; IT CALCULATES THE CHARACTERISTIC RADIUS R0 AND ASSOCIATED PARAMETER ETA2. IN POLAR CO-ORDINATES THE RADIUS OF A SHELL IS R = R0*(1 - A*P2) … FOR MORE INFORMATION SEE ENDAL AND SOFIA."

**How it fits.**
- **Who calls it:** [[fpft.f#FPFT|`FPFT`]] (the rotational correction factors $f_P$, $f_T$ of the structure equations) and [[solid.f#SOLID|`SOLID`]] (solid-body rotation).
- **Inputs:** $\log\rho$, $\log r$, $\log m$ (`HD`, `HR`, `HS`), the angular velocities `OMEGA`, the range `JSTART`–`JEND`; from `NMLPAR_MOD` the tolerance `ACFPFT` and the iteration limits `ITFP1`, `ITFP2`; the constants from `CONSTANTS_MOD`. When `JSTART` > 1, the integration starts from the caller's `ETA2(JSTART-1)` and, in the second pass, `R0(JSTART-1)`, so both arrays are inputs as well as outputs.
- **Outputs:** `ETA2` (Radau's $\eta_2$) and `R0` (the characteristic radius) for each shell, which the callers use to compute the moments of inertia and the correction factors.

**The method.** With the mean density inside the shell $\bar\rho = m/(\tfrac43\pi r^3)$ and $r$ the radius of the sphere of equal volume (`RPHI`):
1. **Radau's equation** (as the comment states it),
   $$r\,\frac{d\eta_2}{dr} + 6\,\frac{\rho}{\bar\rho}\,(\eta_2 + 1) + \eta_2(\eta_2 - 1) = 6,$$
   integrated outward with a fourth-order Runge–Kutta step per shell, using the averages of $\rho$ and $\bar\rho$ at the midpoint. At the first shell, $\eta_2 = 6(1 - \rho/\bar\rho)$. $\eta_2$ is 0 at the center (the comment's boundary condition), and it sets how strongly a shell is flattened, $A \propto 1/(2+\eta_2)$ (step 2). The code does not define $\eta_2$ beyond Radau's equation; what it stands for is question 6.
2. **The characteristic radius** $r_0$ solves, by Newton's method (at most `ITFP2` steps; the test compares the relative change of $r_0^3$ with `ACFPFT` itself, $10^{-36}$ by default, below double precision, so in practice the loop ends only when the update rounds to zero or after all `ITFP2` steps: question 5),
   $$r^3 = r_0^3\Bigl(1 + \tfrac35 A^2 - \tfrac{2}{35}A^3\Bigr),\qquad A = \frac{5\,\Omega^2 r_0^3}{3\,G m\,(2 + \eta_2)} .$$
3. **Iteration between the two** (at most `ITFP1` times): the first integration assumes $r_0 = r$; if $r_0$ differs from that guess by more than `ACFPFT`$^{1/3}$, $\eta_2$ is integrated again in $r_0$ and $r_0$ recomputed.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) (Structural effects of rotation): `ACFPFT` (default 1.0D-36) is the fractional accuracy of the departures from spherical symmetry, given cubed (so $10^{-12}$ by default); `ITFP1` (5) is the number of iterations between the equipotential shape and the effective radius, `ITFP2` (20) that for the effective radius at a given shape parameter.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/CONST1/`, `/CONST2/` to `CONSTANTS_MOD`, `/ROT/` to `NMLPAR_MOD`), the array size `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Questions for the experts

1. **Tolerances compared with different quantities.** In the outer loop, the first test compares the relative change of $r_0$ with `ACC` = `ACFPFT`$^{1/3}$, and the second compares the absolute change of $\eta_2$ (`ERR = ETA2T - ETA2(I)`) with the same `ACC`. Intended?
2. **The center.** The comment states $\eta_2(0) = 0$, and the first shell takes $\eta_2 = 6(1-\rho/\bar\rho)$ (`ETA2(1) = 6.D0*(1.0D0 - RHO/RHOBAR)`). The series solution of Radau's equation near the center ($\rho = \rho_c(1-kr^2)$, $\eta_2 = cr^2$) gives $\eta_2 \approx \tfrac67(1-\rho/\bar\rho)$, a seventh of the code's value. The relative error decays outward as $r^{-7}$, so the effect is probably small after a few shells. Is the factor 6 intended, or should it be 6/7?
3. **Mixed variables in the second pass.** In the second Runge–Kutta pass, the step is in $r_0$, but the midpoint densities `RHOA`, `RHOBA` are the same averages as in the first pass, taken at the volume radii. Is this approximation intended?
4. **Silent non-convergence.** Neither the Newton loop (`ITFP2` steps) nor the outer loop (`ITFP1` passes) warns when it ends without meeting its tolerance; the last values are kept. Should it warn?
5. **A Newton tolerance below double precision.** The outer test uses `ACC` = `ACFPFT`$^{1/3}$ ($10^{-12}$ by default, as the documentation describes `ACFPFT`: "given cubed"), but the Newton test compares `DABS(DELR03/R03)` with `ACFPFT` itself, $10^{-36}$. It passes only when the update is exactly zero, so otherwise all `ITFP2` = 20 steps run for every shell at every call. Should the Newton test compare with `ACC`, or is $10^{-36}$ meant to force convergence to machine precision?
6. **What $\eta_2$ is.** The code names $\eta_2$ only through Radau's equation. Is it the logarithmic derivative of the distortion amplitude, $\eta_2 = d\ln A/d\ln r_0$ (Radau's equation being Clairaut's equation for the shells' distortion rewritten in it, so that a shell's flattening depends on how the shells inside it are distorted)? If so, it should approach 3 at the surface of a centrally condensed star; does it in YREC's models? FPFT's step 2 uses the same reading.
