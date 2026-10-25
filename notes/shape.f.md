## Explanation

**Purpose.** Finds how much each shell of a rotating star is flattened. Its comment: "SHAPE FINDS THE DISTORTION OF A GIVEN SHELL FROM SPHERICAL SYMMETRY; IT CALCULATES THE CHARACTERISTIC RADIUS R0 AND ASSOCIATED PARAMETER ETA2. IN POLAR CO-ORDINATES THE RADIUS OF A SHELL IS R = R0*(1 - A*P2) … FOR MORE INFORMATION SEE ENDAL AND SOFIA."

**How it fits.**
- **Who calls it:** [[fpft.f#FPFT|`FPFT`]] (the rotational correction factors $f_P$, $f_T$ of the structure equations) and [[solid.f#SOLID|`SOLID`]] (solid-body rotation).
- **Inputs:** $\log\rho$, $\log r$, $\log m$ (`HD`, `HR`, `HS`), the angular velocities `OMEGA`, the range `JSTART`–`JEND`; from `/ROT/` the tolerance `ACFPFT` and the iteration limits `ITFP1`, `ITFP2`. When `JSTART` > 1, the integration starts from the caller's `ETA2(JSTART-1)` and, in the second pass, `R0(JSTART-1)`, so both arrays are inputs as well as outputs.
- **Outputs:** `ETA2` (Radau's $\eta_2$) and `R0` (the characteristic radius) for each shell, which the callers use to compute the moments of inertia and the correction factors.

**The method.** With the mean density inside the shell $\bar\rho = m/(\tfrac43\pi r^3)$ and $r$ the radius of the sphere of equal volume (`RPHI`):
1. **Radau's equation** (as the comment states it),
   $$r\,\frac{d\eta_2}{dr} + 6\,\frac{\rho}{\bar\rho}\,(\eta_2 + 1) + \eta_2(\eta_2 - 1) = 6,$$
   integrated outward with a fourth-order Runge–Kutta step per shell, using the averages of $\rho$ and $\bar\rho$ at the midpoint. At the first shell, $\eta_2 = 6(1 - \rho/\bar\rho)$.
2. **The characteristic radius** $r_0$ solves, by Newton's method (at most `ITFP2` steps, to `ACFPFT`),
   $$r^3 = r_0^3\Bigl(1 + \tfrac35 A^2 - \tfrac{2}{35}A^3\Bigr),\qquad A = \frac{5\,\Omega^2 r_0^3}{3\,G m\,(2 + \eta_2)} .$$
3. **Iteration between the two** (at most `ITFP1` times): the first integration assumes $r_0 = r$; if $r_0$ differs from that guess by more than `ACFPFT`$^{1/3}$, $\eta_2$ is integrated again in $r_0$ and $r_0$ recomputed.

## Questions for the experts

1. **Tolerances compared with different quantities.** In the outer loop, the first test compares the relative change of $r_0$ with `ACC` = `ACFPFT`$^{1/3}$, and the second compares the absolute change of $\eta_2$ (`ERR = ETA2T - ETA2(I)`) with the same `ACC`. Intended?
2. **The center.** The comment states $\eta_2(0) = 0$, while the first shell takes $6(1 - \rho/\bar\rho)$, which is the leading term near the center. Fine, but the comment could say so.
3. **Mixed variables in the second pass.** In the second Runge–Kutta pass, the step is in $r_0$, but the midpoint densities `RHOA`, `RHOBA` are the same averages as in the first pass, taken at the volume radii. Is this approximation intended?
4. **Silent non-convergence.** Neither the Newton loop (`ITFP2` steps) nor the outer loop (`ITFP1` passes) warns when it ends without meeting its tolerance; the last values are kept. Should it warn?
