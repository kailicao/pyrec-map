## Explanation

**Purpose.** Finds how much each shell of a rotating star is flattened. Its comment: "SHAPE FINDS THE DISTORTION OF A GIVEN SHELL FROM SPHERICAL SYMMETRY; IT CALCULATES THE CHARACTERISTIC RADIUS R0 AND ASSOCIATED PARAMETER ETA2. IN POLAR CO-ORDINATES THE RADIUS OF A SHELL IS R = R0*(1 - A*P2) … FOR MORE INFORMATION SEE ENDAL AND SOFIA."

**How it fits.**
- **Who calls it:** [[fpft.f#FPFT|`FPFT`]] (the rotational correction factors $f_P$, $f_T$ of the structure equations) and [[solid.f#SOLID|`SOLID`]] (solid-body rotation).
- **Inputs:** $\log\rho$, $\log r$, $\log m$ (`HD`, `HR`, `HS`), the angular velocities `OMEGA`, the range `JSTART`–`JEND`; from `NMLPAR_MOD` the tolerance `ACFPFT` and the iteration limits `ITFP1`, `ITFP2`; the constants from `CONSTANTS_MOD`. When `JSTART` > 1, the integration starts from the caller's `ETA2(JSTART-1)` and, in the second pass, `R0(JSTART-1)`, so both arrays are inputs as well as outputs.
- **Outputs:** `ETA2` (Radau's $\eta_2$) and `R0` (the characteristic radius) for each shell, which the callers use to compute the moments of inertia and the correction factors.

**The method.** With the mean density inside the shell $\bar\rho = m/(\tfrac43\pi r^3)$ and $r$ the radius of the sphere of equal volume (`RPHI`):
1. **Radau's equation** (as the comment states it),
   $$r\,\frac{d\eta_2}{dr} + 6\,\frac{\rho}{\bar\rho}\,(\eta_2 + 1) + \eta_2(\eta_2 - 1) = 6,$$
   integrated outward with a fourth-order Runge–Kutta step per shell, using the averages of $\rho$ and $\bar\rho$ at the midpoint ([[#L91-L118]]). At the first shell, $\eta_2 = 6(1 - \rho/\bar\rho)$ ([[#L60]]; a suspected bug, [[#b1]]). $\eta_2$ is 0 at the center (the comment's boundary condition, [[#L93]]), and it sets how strongly a shell is flattened, $A \propto 1/(2+\eta_2)$ (step 2). The code does not define $\eta_2$ beyond Radau's equation; what it stands for is [[#q1]].

    > **Question** ([[#L40-L45]]; [[#L92-L93]]). **What $\eta_2$ is.** The code names $\eta_2$ only through Radau's equation. Is it the logarithmic derivative of the distortion amplitude, $\eta_2 = d\ln A/d\ln r_0$ (Radau's equation being Clairaut's equation for the shells' distortion rewritten in it, so that a shell's flattening depends on how the shells inside it are distorted)? FPFT's step 2 uses the same reading. If so, it should approach 3 at the surface of a centrally condensed star; does it in YREC's models?
2. **The characteristic radius** $r_0$ solves, by Newton's method (at most `ITFP2` steps; the test compares the relative change of $r_0^3$ with `ACFPFT` itself, $10^{-36}$ by default, below double precision, so in practice the loop ends only when the update rounds to zero or after all `ITFP2` steps: [[#L71]], [[#L134]], a suspected bug, [[#b2]]),
   $$r^3 = r_0^3\Bigl(1 + \tfrac35 A^2 - \tfrac{2}{35}A^3\Bigr),\qquad A = \frac{5\,\Omega^2 r_0^3}{3\,G m\,(2 + \eta_2)} .$$
3. **Iteration between the two** (at most `ITFP1` times, [[#L122-L162]]): the first integration assumes $r_0 = r$; if $r_0$ differs from that guess by more than `ACFPFT`$^{1/3}$, $\eta_2$ is integrated again in $r_0$ and $r_0$ recomputed.

    > **Question** ([[#L137-L140]]; [[#L159-L160]]). **Tolerances compared with different quantities.** In the outer loop, the first test compares the relative change of $r_0$ with `ACC` = `ACFPFT`$^{1/3}$, and the second compares the absolute change of $\eta_2$ (`ERR = ETA2T - ETA2(I)`) with the same `ACC`. Is that intended?

    > **Question** ([[#L99-L100]]; [[#L144-L156]]). **Mixed variables in the second pass.** In the second Runge–Kutta pass, the step is in $r_0$, but the midpoint densities `RHOA`, `RHOBA` are the same averages as in the first pass, taken at the volume radii. Is this approximation intended?

    > **Question** ([[#L66-L72]]; [[#L124-L162]]). **Silent non-convergence.** Neither the Newton loop (`ITFP2` steps) nor the outer loop (`ITFP1` passes) warns when it ends without meeting its tolerance; the last values are kept. Should it warn?

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) (Structural effects of rotation): `ACFPFT` (default 1.0D-36) is the fractional accuracy of the departures from spherical symmetry, given cubed (so $10^{-12}$ by default); `ITFP1` (5) is the number of iterations between the equipotential shape and the effective radius, `ITFP2` (20) that for the effective radius at a given shape parameter.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/CONST1/`, `/CONST2/` to `CONSTANTS_MOD`, `/ROT/` to `NMLPAR_MOD`), the array size `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Bugs, by priority

1. **(a)** **The first shell's $\eta_2$ is seven times too large.** ([[#L60]]; [[#L93]]) The first shell takes $\eta_2 = 6(1-\rho/\bar\rho)$ (`ETA2(1) = 6.D0*(1.0D0 - RHO/RHOBAR)`). The series solution of Radau's equation as the comment states it ([[#L93]]) near the centre ($\rho = \rho_c(1-kr^2)$, so $\rho/\bar\rho \approx 1 - \tfrac25 kr^2$, and $\eta_2 = cr^2$) gives $7c = \tfrac{12}{5}k$, so $\eta_2 \approx \tfrac67(1-\rho/\bar\rho)$, a seventh of the code's value. What follows: The integration starts from a wrong $\eta_2$; the relative error decays outward as $r^{-7}$, so the effect on `ETA2`, `R0`, and so on FPFT's $f_P$, $f_T$ and MOMI's moments of inertia is probably small after a few shells. Only with rotation (`LROT`, off by default). Read from the code, not run; the size of the effect was not traced. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to start ETA2 from the series solution of Radau's
    C equation near the centre, ETA2 = 6/7*(1 - RHO/RHOBAR).
             ETA2(1) = 6.D0/7.D0*(1.0D0 - RHO/RHOBAR)
    ```

2. **(c)** **The Newton test for $r_0$ compares with `ACFPFT`, not its cube root.** ([[#L71]]; [[#L122]]; [[#L134]]) The documentation describes `ACFPFT` (default $10^{-36}$) as the fractional accuracy of the departures from spherical symmetry "given cubed", and the outer test uses its cube root, `ACC` ($10^{-12}$). The Newton tests compare `DABS(DELR03/R03)` with `ACFPFT` itself, so they pass only when the update is exactly zero; otherwise all `ITFP2` = 20 steps run for every shell at every call. What follows: The setting is not applied as documented, and the time spent in SHAPE grows; the results are converged to machine precision, so they should change only at about $10^{-12}$ with the fix. With rotation only (`LROT`, off by default). Read from the code, not run. If convergence to machine precision is meant, the fix is a comment instead. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to compare the Newton update of R0**3 with ACC, the
    C cube root of ACFPFT, as the outer test does.
          ACC = ACFPFT**CC13
          JBEGIN = JSTART
    ...
                IF(DABS(DELR03/R03).LE.ACC)GOTO 20
    ...
                   IF(DABS(DELR03/R03).LT.ACC)GOTO 50
    ```
