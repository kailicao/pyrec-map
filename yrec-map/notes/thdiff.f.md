## Explanation

**Purpose.** `THDIFF` solves Burgers' equations for the diffusion of the species in a fully ionised plasma, and returns the diffusion coefficients. Its header: the routine was written by Anne A. Thoul (Institute for Advanced Study), see Thoul et al. ([1994](https://ui.adsabs.harvard.edu/abs/1994ApJ...421..828T), ApJ 421, 828); `LUDCMP` and `LUBKSB` are from Numerical Recipes.

**How it fits.**
- **Inputs:** arguments: the number of species `M` (fluid 1 hydrogen, 2 helium, 3 to `M-1` heavy elements, `M` the electrons), their atomic masses `A` (with `A(M)` = $`m_e/m_u`$), charges `Z` (`Z(M)` = $`-1`$), mass fractions `X`, and the Coulomb logarithms `CL(M,M)`.
- **Who calls it:** [MICRODIFF_COD](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_cod.f#L4-L217) and [SETUP_GRSETT](https://github.com/yreclab/yrec/blob/7be4133/src/setup_grsett.f#L2-L330) (which, for the gravitational settling of hydrogen, uses `-AP(1)` and `-SDEL(2,I)*AT(1)`, or else a fitted polynomial in $`X`$).

    > **Question** ([setup_grsett.f, lines 275–285](https://github.com/yreclab/yrec/blob/7be4133/src/setup_grsett.f#L275-L285); [setup_grsett.f, line 306](https://github.com/yreclab/yrec/blob/7be4133/src/setup_grsett.f#L306)). **A mixed treatment.** In `SETUP_GRSETT` the concentration coefficient `AC = 1.15 - 1.42X + 0.647X^2`, the metals' `AH` and the derivatives `QAPX`, `QATX` always come from the fits, even when $`A_P`$ and $`A_T`$ come from `THDIFF`. Is this intended?

- **What it calls:** [LUDCMP](ludcmp.f.md#ludcmp) (LU decomposition) and [LUBKSB](lubksb.f.md#lubksb) (back substitution).
- **Outputs:** `AP(M)`, `AT(M)`, `AX(M,M)`, the coefficients of the pressure, temperature and concentration gradients in each species' diffusion velocity; also `X(M)`, the electrons' mass fraction, is overwritten ([line 99](https://github.com/yreclab/yrec/blob/7be4133/src/thdiff.f#L99)). Harmless with both callers: they pass a local array, `XFRAC`, refill its first three entries at every point and never read `XFRAC(4)` (settled from the code, Nov 9, 2026: [microdiff_cod.f, lines 79–81](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_cod.f#L79-L81); [setup_grsett.f, lines 224–226](https://github.com/yreclab/yrec/blob/7be4133/src/setup_grsett.f#L224-L226)).
- **COMMON blocks:** none.

**The method.**
1. Concentrations from mass fractions, normalised to the electrons ($`C_M = 1`$, by charge neutrality):
   
   $$\displaystyle C\_s = \frac{X\_s/A\_s}{\sum\_{t\lt{}M} Z\_t X\_t/A\_t},\qquad C = \sum\_s C\_s,\qquad \rho \propto \sum\_s A\_s C\_s ,$$
   
   and the electrons' mass fraction $`X_M = A_M / \sum_s A_s C_s`$.
2. The collision coefficients, with $`\ln\Lambda_{st}`$ = `CL`:
   
   $$\displaystyle K\_{st} = \ln\Lambda\_{st}\\,\sqrt{\frac{A\_s A\_t}{A\_s + A\_t}}\\;C\_s C\_t\\,Z\_s^2 Z\_t^2,$$
   
   and the mass ratios $`x_{st} = A_t/(A_s + A_t)`$, $`y_{st} = A_s/(A_s + A_t)`$, $`z_{st} = 3y_{st} + 1.3\,x_{st}A_t/A_s`$ (`XX`, `Y`, `YY`).
3. The $`N = 2M + 2`$ equations ($`M`$ momentum equations, $`M`$ heat-flow equations, current neutrality and zero mass flow), written as the code's comment does,
   
   $$\displaystyle \alpha\_s\\,\frac{d\ln p}{dr} + \nu\_s\\,\frac{d\ln T}{dr} + \sum\_{t \ne 2, M} \gamma\_{st}\\,\frac{d\ln C\_t}{dr} = \sum\_t \delta\_{st}\\,w\_t ,$$
   
   in the $`N`$ unknowns: $`M`$ diffusion velocities, $`M`$ heat fluxes, the electric field and the gravitational term. The matrix $`\delta`$ is assembled with the coefficients 0.6, 1.5, 1.6, 0.8 and 2.7 of Burgers' equations. The sum leaves out the electrons and helium because their gradients are not independent: the concentrations are normalised to the electrons, so $`C_M = 1`$ and $`d\ln C_M/dr = 0`$, and charge neutrality, $`\sum_{t\lt{}M} Z_t C_t = 1`$, gives helium's gradient in terms of the others, which is how its terms enter $`\gamma_{st}`$ (`GAMMA(I,J) = -C(J)/CC + C(2)/CC*Z(J)*C(J)/Z(2)/C(2)`, then 1 added when $`t = s`$, a term subtracted when $`s = 2`$, and the whole multiplied by $`C_s/C`$). In full, for $`t \ne 2, M`$,
   
   $$\displaystyle \gamma\_{st} = \frac{C\_s}{C}\Bigl\[\mathbb{1}\_{s=t} - \frac{C\_t}{C} + \frac{Z\_tC\_t}{Z\_2C\_2}\Bigl(\frac{C\_2}{C} - \mathbb{1}\_{s=2}\Bigr)\Bigr\],\qquad \alpha\_s = \frac{C\_s}{C},\qquad \nu\_s = 0,$$
   
   where $`C = \sum_t C_t`$ (`CC`) and $`\mathbb{1}_{s=t}`$ is 1 if $`s = t`$ and 0 otherwise (written so, to keep it apart from the matrix $`\delta`$).
4. `LUDCMP` factorises $`\delta`$ once; `LUBKSB` solves it for the right-hand sides $`\alpha`$, $`\nu`$ and each column of $`\gamma`$, which gives the coefficients
   
   $$\displaystyle w\_s = A^{(p)}\_s\\,\frac{d\ln p}{dr} + A^{(T)}\_s\\,\frac{d\ln T}{dr} + \sum\_t A^{(C)}\_{st}\\,\frac{d\ln C\_t}{dr},$$
   
   multiplied by `KO*AC*CC` $`= K_0 \left(\sum_s A_s C_s\right)\left(\sum_s C_s\right)`$ with $`K_0 = 2`$; $`\sum_s A_s C_s`$ is only proportional to $`\rho`$ (the comment: "multiplied by $`p/K_0`$"). The callers then multiply the coefficients by $`r^2T^{5/2}/\ln\Lambda`$ ($`r`$ in $`R_\odot`$, $`T`$ in $`10^7\,\mathrm{K}`$; `FAC` in [SETUP_GRSETT](https://github.com/yreclab/yrec/blob/7be4133/src/setup_grsett.f#L2-L330) and [MICRODIFF_COD](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_cod.f#L4-L217)), which gives the flux in the units of the settling equation on [GRSETT](grsett.f.md#grsett)'s page.

    > **Question** ([lines 278–286](https://github.com/yreclab/yrec/blob/7be4133/src/thdiff.f#L278-L286)). **The normalisation comment.** The comment says the results "must be multiplied by p/K_0," while the code multiplies by `KO*AC*CC` ($`K_0 \sum A_s C_s \sum C_s`$). Which units do the callers assume?

    > **Question** ([lines 112–114](https://github.com/yreclab/yrec/blob/7be4133/src/thdiff.f#L112-L114); [microdiff_cod.f, lines 130–154](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_cod.f#L130-L154); [setup_grsett.f, lines 261–275](https://github.com/yreclab/yrec/blob/7be4133/src/setup_grsett.f#L261-L275)). **Is the Coulomb logarithm counted twice?** `THDIFF` puts the Coulomb logarithms `CL` into $`K_{st}`$, so its coefficients already scale as $`1/\ln\Lambda`$. [MICRODIFF_COD](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_cod.f#L4-L217) computes `TCL` per pair (a fit in the Debye length or interionic distance), passes it to `THDIFF`, and then multiplies by `FAC`, divided by a fixed `LN_LAMBDA = 2.2D0`; [SETUP_GRSETT](https://github.com/yreclab/yrec/blob/7be4133/src/setup_grsett.f#L2-L330) with `LTHOUL` (not `LTHOULFIT`) passes `TCL` = `LN_LAMBDA` (or the fitted `TCL` with `ILAMBDA = 4`) and again divides `FAC` by `LN_LAMBDA`; and the time unit of both callers "includes factor of 2.2 from ln lambda." Only the fitted branch (`LTHOULFIT`) is clearly free of $`\ln\Lambda`$. Do `THDIFF`'s outputs need the division by $`\ln\Lambda`$ again, or does `KO*AC*CC` normalise them to $`\ln\Lambda = 1`$? If not, settling with the full Thoul solution would be too slow by a factor of about $`\ln\Lambda`$ (to be checked against Thoul et al. 1994 before calling it an error).

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

## Bugs, by priority

1. **(cannot be reached)** **No check of the array sizes.** ([lines 48–53](https://github.com/yreclab/yrec/blob/7be4133/src/thdiff.f#L48-L53); [line 72](https://github.com/yreclab/yrec/blob/7be4133/src/thdiff.f#L72)) The work arrays hold at most `MMAX = 20` species (`NMAX = 42` equations), with no test that `M` $`\le 20`$; a larger `M` would write past them. Correct today: both callers pass `M` = 4 (`NSPEC`).

    **A possible fix:**

    ```diff
    --- a/src/thdiff.f
    +++ b/src/thdiff.f
    @@ -68,6 +68,12 @@
     
     C Initialize parameters:
     
    +C 11/09/26 KC via Claude
    +C code changed to stop when M exceeds the size of the work arrays.
    +      IF(M.GT.MMAX)THEN
    +         WRITE(*,*) 'THDIFF: M EXCEEDS MMAX = ',MMAX
    +         STOP
    +      ENDIF
           KO=2
           N=2*M+2
           DO I=1,M
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Of 34 runs (26 of YREC's cases, from 0.04 to 9 $`M_\odot`$, with rotation, settling, and helium burning, and 8 made-up ones), the routine ran in the seven with settling, up to 37 million times per run (`testsuite/Test_solarM22M_difkur`), always with `M` = 4. It cannot be reached at 7be4133: Both callers pass `NSPEC` = 4 ([microdiff_cod.f, line 55](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_cod.f#L55); [setup_grsett.f, line 89](https://github.com/yreclab/yrec/blob/7be4133/src/setup_grsett.f#L89)). No fix was run, since the fix is a stop. Intent: `KNOWN_ISSUES.md` (line 1846) says that `NMAX` "is deliberately per-routine."

### THDIFF

Thoul et al. (1994) solution of Burgers' equations: diffusion coefficients for the pressure, temperature and concentration gradients of each species.
