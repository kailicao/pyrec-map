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

1. **(harmless in the runs)** **The first shell's $\eta_2$ is seven times too large.** ([[#L60]]; [[#L93]]) The first shell takes $\eta_2 = 6(1-\rho/\bar\rho)$ (`ETA2(1) = 6.D0*(1.0D0 - RHO/RHOBAR)`). The series solution of Radau's equation as the comment states it ([[#L93]]) near the centre ($\rho = \rho_c(1-kr^2)$, so $\rho/\bar\rho \approx 1 - \tfrac25 kr^2$, and $\eta_2 = cr^2$) gives $7c = \tfrac{12}{5}k$, so $\eta_2 \approx \tfrac67(1-\rho/\bar\rho)$, a seventh of the code's value. What follows: The integration starts from a wrong $\eta_2$; the relative error decays outward as $r^{-7}$, so the effect on `ETA2`, `R0`, and so on FPFT's $f_P$, $f_T$ and MOMI's moments of inertia is probably small after a few shells. Only with rotation (`LROT`, off by default).

    **A possible fix:**

    ```diff
    --- a/src/shape.f
    +++ b/src/shape.f
    @@ -57,7 +57,10 @@
              RHOBAR = DEXP(CLN*(HS(1) - C4PI3L - 3.0D0*HR(1)))
              RPHI = DEXP(CLN*HR(1))
              RHO = DEXP(CLN*HD(1))
    -         ETA2(1) = 6.D0*(1.0D0 - RHO/RHOBAR)
    +C 11/09/26 KC via Claude
    +C code changed to start ETA2 from the series solution of Radau's
    +C equation near the centre, ETA2 = 6/7*(1 - RHO/RHOBAR).
    +         ETA2(1) = 6.D0/7.D0*(1.0D0 - RHO/RHOBAR)
     C ITERATE FOR R0 GIVEN RPHI AND ETA2
              GM = CG*DEXP(CLN*HS(1))
              RPHI3 = RPHI**3
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The first shell's $\eta_2$ was set in all five rotating test cases, from 26,314 to 90,623 times, with values from $-1.80$ to 0.68. With the fix, the 3 $M_\odot$ case (`testsuite/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2`) stays within the noise: $\log L$ moves by up to 0.0012 dex, against 0.0076 for a null change (nearly every opacity, all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$, times $1 + 10^{-10}$, on the same case), and central $Y$ by 0.018 against 0.014 (1,863 models instead of 1,853). In the 0.8 $M_\odot$ case (`testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`) $\log L$ and $\log T_\mathrm{eff}$ stay within the noise, and central $X$ and $Y$ moved by up to 0.00015 at 0.395 Gyr, about four times a null change, as with TRAPZD's fix ([[trapzd.f#TRAPZD|TRAPZD]], bug 1). Rechecked on Nov 10, 2026, with a build without counting lines in SHAPE and TRAPZD, and beside it a null change of the distortion itself (the first shell's $\eta_2$ times $1 + 10^{-10}$): Model by model, every change, the null one included, stays below $10^{-7}$ in central $X$ until about 0.046 Gyr, where central $X$ stops falling, and grows to some $10^{-5}$ by 0.16 Gyr, so this case amplifies whatever perturbs it there, and the size of the change depends on the build. In that build, SHAPE's fix moves central $X$ by up to $5.8\times10^{-5}$ at 0.222 Gyr, against $2.9\times10^{-5}$ for the null change at the same age ($6.8\times10^{-5}$ and $6.1\times10^{-5}$ model by model), while TRAPZD's fix again gives 0.00015 at 0.3955 Gyr: The shared number came not from one fix acting through the other but from the case's sensitivity, and SHAPE's fix is within the noise there. The 2 $M_\odot$ cases, which rotate faster, were not run with the fix. Intent: none found.

2. **(harmless in the runs)** **The Newton test for $r_0$ compares with `ACFPFT`, not its cube root.** ([[#L71]]; [[#L122]]; [[#L134]]) The documentation describes `ACFPFT` (default $10^{-36}$) as the fractional accuracy of the departures from spherical symmetry "given cubed," and the outer test uses its cube root, `ACC` ($10^{-12}$). The Newton tests compare `DABS(DELR03/R03)` with `ACFPFT` itself, so they pass only when the update is exactly zero, or, in the calls from CHECKJ before its last iteration, which relax `ACFPFT` to $10^{-6}$ ([[checkj.f#L195-L203]]), when it is below $10^{-6}$; otherwise all `ITFP2` = 20 steps run. What follows: The setting is not applied as documented, and the time spent in SHAPE grows; the results are converged to machine precision, so they should change only at about $10^{-12}$ with the fix. With rotation only (`LROT`, off by default).

    **A possible fix:**

    ```diff
    --- a/src/shape.f
    +++ b/src/shape.f
    @@ -48,6 +48,10 @@
           C2 = 2.0D0/3.5D1
           C3 = 3.0D0*C1
           C4 = 4.0D0*C2
    +C 11/09/26 KC via Claude
    +C code changed to compare the Newton update of R0**3 with ACC, the
    +C cube root of ACFPFT, as the outer test does.
    +      ACC = ACFPFT**CC13
           JBEGIN = JSTART
           IF(JSTART.EQ.1) THEN
     C  CALCULATE FIRST POINT ETA2 USING CENTRAL B.C.
    @@ -68,7 +72,7 @@
                 DELR03 = (RPHI3-R03*(1.0D0 + C1*A**2 - C2*A**3))/
          *      (1.0D0 + C3*A**2 - C4*A**3)
                 R03 = R03 + DELR03
    -            IF(DABS(DELR03/R03).LE.ACFPFT)GOTO 20
    +            IF(DABS(DELR03/R03).LE.ACC)GOTO 20
        10    CONTINUE
        20    R0(1) = R03**CC13
              IF(JEND.EQ.1) GOTO 9999
    @@ -119,7 +123,6 @@
              RPHI3 = RPHI**3
              R03 = RPHI3
              R0EST = RPHI
    -         ACC = ACFPFT**CC13
     C ITERATE BETWEEN SOLUTION FOR ETA2 AND SOLUTION FOR R0 ITFP1 TIMES.
              DO 60 K = 1,ITFP1
                 FACT = 5.0D0*CC13*OMEGA(I)**2/(GM*(2.0D0+ETA2(I)))
    @@ -131,7 +134,7 @@
                    DELR03 = (RPHI3-R03*(1.0D0 + C1*A**2 - C2*A**3))/
          *         (1.0D0 + C3*A**2 - C4*A**3)
                    R03 = R03 + DELR03
    -               IF(DABS(DELR03/R03).LT.ACFPFT)GOTO 50
    +               IF(DABS(DELR03/R03).LT.ACC)GOTO 50
        40       CONTINUE
        50       R0(I) = R03**CC13
                 ERR = R0(I) - R0EST
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The Newton solve for $r_0$ ran about 29 to 95 million times in each rotating test case. It nearly always ended early (after 1 to 20 steps), with an update of zero, or of up to $10^{-6}$ in CHECKJ's relaxed calls; it ran all 20 steps, with updates of $1$ to $4\times10^{-16}$ that had long met the cube-root accuracy, in 47 (`testsuite/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2`) to 15,909 (`testsuite/Test_m2p0_feh+0p0_vzams150_IES1_TAMS`) solves. With the fix, the 2 $M_\odot$ case stays within the noise (every track difference at most $1.6\times10^{-8}$, against $1.1\times10^{-7}$ for a null change, nearly every opacity (all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$) times $1 + 10^{-10}$ on the same case), and so does the 0.8 $M_\odot$ case (`testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`), except central $\log T$ at its last model (0.00047 dex, against 0.0002). The setting is not applied as documented, but neither the results nor the time spent change measurably. In CHECKJ's relaxed calls the fix's `ACC` would be $10^{-2}$. If convergence to machine precision is meant, the fix is a comment instead. Intent: The outer test's comment asks for the cube root ([[#L138-L139]]); nothing is said of the inner one.
