## Explanation

**Purpose.** `GETQUA` solves for the quadrupole moment (the $P_2$ part of the gravitational potential perturbation) of a rotating star, "using the Sweet (1950) formulation as given in Zahn (1992)" (its comment). The result is needed for the meridional circulation velocity.

**How it fits.**
- **Who calls it:** only [[seculr.f#SECULR|SECULR]].
- **Inputs:** `HD` ($\log\rho$), `HG` (gravity $g$), `HRU` (radius, unlogged), `OMEGA`, `M`.
- **Outputs:** in [[quadru_mod.f#QUADRU_MOD|`QUADRU_MOD`]]: `QUAD` (the quadrupole term per shell) and `GG` (a copy of $g$), read by [[getw.f#GETW|GETW]] and [[vcirc.f#VCIRC|VCIRC]].
- **Modules:** `QUADRU_MOD` (output); [[tridi_mod.f#TRIDI_MOD|`TRIDI_MOD`]] as workspace for the tridiagonal solver (shared with `CCOEFT`, `CTRIDI`, `DCOEFT`, [[mixcom.f#MIXCOM|MIXCOM]], `TRIDIA`); constants from [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]]; `ISHORT` from [[iounits_mod.f#IOUNITS_MOD|`IOUNITS_MOD`]], for the error message.

**The method.** The comment states the equation
$$\frac{1}{r}\frac{d^2}{dr^2}(r\phi) - \frac{6\phi}{r^2} - 4\pi G\rho\frac{d\rho}{dP}\,\phi = -\frac{4\pi G}{3}\frac{r^2}{g}\frac{d}{dr}\left(\rho\Omega^2\right),$$
and the code discretizes, per point,
$$\phi'' + \frac{2}{r}\phi' - \frac{6}{r^2}\phi - \frac{4\pi G}{g}\frac{d\rho}{dr}\,\phi = -\frac{4\pi G\,r^2}{3g}\,\frac{d(\rho\Omega^2)}{dr},$$
with $\phi$ = `QUAD` (with $dP/dr = -\rho g$, the sign of the $d\rho/dr$ term differs from that of the comment's first form, which is a slip, below). The code uses the model's $d\rho/dr$ directly, which needs only hydrostatic equilibrium to stand for $\rho\,d\rho/dP$, not the ideal gas law the comment cites ([[#L40-L41]]) (settled from the code, Nov 9, 2026). Derivatives are centered on the smaller of the two neighboring intervals (weights `FPL`, `FMI`). Boundary conditions: $\phi \to 0$ at the center; at the surface, $\phi \propto r^{-3}$ outside the star ("D PHI/DR + 3 PHI/R = 0," [[#L87-L97]]), applied through a point outside, $\phi_{M+1} = (r_M/r_{M+1})^3\phi_M$ (`FX`), with $\tfrac{2}{r}\phi' = -6\phi/r^2$ added to $-6\phi/r^2$, hence the $-12/r^2$ of `B(M)`. Outside the star ($\rho = 0$) the comment's own equation has the solutions $r^2$ and $r^{-3}$, so the decaying $r^{-3}$ of the surface condition is the right one, and the header's "VARIES AS 1/R**4" ([[#L45-L47]]) is a slip; the two terms that the comment says "CANCEL" ([[#L88]]) add up, as they should (settled from the code, Nov 9, 2026). The tridiagonal system is solved by the Thomas algorithm ("from Numerical Recipes"); the run stops on a zero pivot (exit status 1), with a message naming the zone, to the terminal and the `.short` file.

**The comment's first form has the wrong sign.** Linearizing Poisson's equation with $P' = -\rho\phi$ gives $\nabla^2\phi + 4\pi G\rho\,(d\rho/dP)\,\phi$, and with hydrostatic equilibrium, $dP/dr = -\rho g$, the last term is $-(4\pi G/g)(d\rho/dr)\,\phi$: the code's `-C4PIG*DRHO/HG` ([[#L62-L63]]; [[#L79-L80]]), and the sign of the comment's second form ("+4\*PI\*G\*RHO\*QUAD," [[#L38-L39]], which lacks $d\rho/dP$). So the code is right, and the comment's first form, $-4\pi G\rho\,(d\rho/dP)\,\phi$ ([[#L36]]), has the sign slip (settled from the code, Nov 10, 2026).

At the first point, $d\rho/dr$ is divided by $\Delta r = \min(r_1, r_2 - r_1)$, not by $r_2 - r_1$ ([[#b2]]).

> **Question** ([[#L61]]; [[#L65]]). **The central right-hand side.** The first row's right-hand side `D(1)` uses $\Omega_1^2\,d\rho/dr$ instead of $d(\rho\Omega^2)/dr$. Is this an intended approximation near the center?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

**Changed since `a8a5950`.** The two stops on a zero pivot, which printed nothing, now write the zone to the terminal and the `.short` file and exit with status 1, the code for run-time errors (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(changes results, large)** **Checked by KC** (Nov 10, 2026). **A wrong index in $d\rho/dr$.** ([[#L76-L77]]; [[#L82-L84]]) In the interior loop, `DRHO = 0.5*(FPL*rho(I+1) + (FMI-FPL)*rho(I) - FMI*rho(I))/DR`: The last term uses `HD(I)` where the matching expression for $d(\rho\Omega^2)/dr$ just below uses `DW2(I-1)`. As written, the expression reduces to $\tfrac12(\rho_{i+1}-\rho_i)/\Delta r_+$, half the forward difference, instead of the mean of the two one-sided differences. What follows: The $d\rho/dr$ term of the diagonal `B(I)` ([[#L79-L80]]) is about half its value at every interior point, so the quadrupole term `QUAD` is wrong; VCIRC reads it in its Zahn branch (`IES` = 1, the default) for the factor `RAT` of the circulation velocity ([[vcirc.f#L239-L241]]), and GETW prints `QUAD(M)`. Only with rotation (`LROT`, off by default), where SECULR calls GETQUA.

    **A possible fix:**

    ```diff
    --- a/src/getqua.f
    +++ b/src/getqua.f
    @@ -73,8 +73,11 @@
              FMI = DR/DRMI
              FAC = 1.0D0/DR**2
              DRI = 1.0D0/DR/HRU(I)
    +C 11/09/26 KC via Claude
    +C code changed to take the last term of DRHO at shell I-1, as in
    +C DRHOW2.
              DRHO = 0.5D0*(FPL*EXP(CLN*HD(I+1))+(FMI-FPL)*
    -     *          EXP(CLN*HD(I))-FMI*EXP(CLN*HD(I)))/DR
    +     *          EXP(CLN*HD(I))-FMI*EXP(CLN*HD(I-1)))/DR
              A(I) = FMI*(FAC-DRI)
              B(I) = -FAC*(FPL+FMI)+DRI*(FMI-FPL)-6.0D0/HRU(I)**2
          *          -C4PIG*DRHO/HG(I)
    ```

    **How the code itself shows it.** The routine's other three-point first derivatives all weight shell I−1. [[#L82-L84]] compute $d(\rho\Omega^2)/dr$ as `0.5D0*(FPL*DW2(I+1) + (FMI-FPL)*DW2(I) - FMI*DW2(I-1))/DR`, and the matrix applies the same stencil to $(2/r)\,dQ/dr$: `C(I) = FPL*(FAC+DRI)`, `B(I)` holds `DRI*(FMI-FPL)`, and `A(I) = FMI*(FAC-DRI)` puts `-FMI*DRI` on `QUAD(I-1)` ([[#L78-L81]]), with `DRI = 1.0D0/DR/HRU(I)` ([[#L75]]). The weights `FPL`, `FMI-FPL`, and `-FMI` sum to zero, as a derivative's must, and give the mean of the two one-sided differences, the centered derivative the comment asks for ("CENTER NUMERICAL DERIVATIVES," [[#L52-L53]]). In `DRHO` ([[#L76-L77]]) the last two weights both fall on `HD(I)`, so its stencil is `FPL` on shell I+1 and `-FPL` on shell I alone.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The interior loop ran in all five rotating test cases, from 794,212 times (`testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS`) to 1,584,439 (`testsuite/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2`), at shells 2 to 1069, and at every one of them the dropped term was more than 10% of the corrected $d\rho/dr$. With the fix, the 3 $M_\odot$ case to the red giant branch changes far beyond the noise: $\log L$ moves by up to 0.42 dex and $\log T_\mathrm{eff}$ by 0.27 (at about 0.39 Gyr), against 0.0076 and 0.00085 for a null change (nearly every opacity, all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$, times $1 + 10^{-10}$, on the same case); central $\log T$ by 0.39 against 0.0008, central $Y$ by 0.042 against 0.014; the track has 1,919 models instead of 1,853 and ends at 0.4424 Gyr instead of 0.4397. In the 0.8 $M_\odot$ case (`testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`) central $X$ moves by up to 0.00075 (at 6.3 Gyr), against 0.000034 for a null change, central $\log T$ by 0.0018 against 0.0002, and $\log L$ by 0.00095 against 0.00014. Intent: The matching $d(\rho\Omega^2)/dr$ just below takes shell `I-1` ([[#L82-L84]]), so this looks like a slip.

2. **(never occurred)** **The central $d\rho/dr$ is divided by the wrong interval.** ([[#L54-L56]]; [[#L61]]; [[#L72-L77]]) At the first point, `DR = MIN(HRU(1),HRU(2)-HRU(1))` ([[#L54]]) and `DRHO = (EXP(CLN*HD(2))-EXP(CLN*HD(1)))/DR` ([[#L61]]): a difference over the interval $r_2 - r_1$ divided by $\Delta r$, while the interior weights its forward difference by `FPL = DR/DRPL` ([[#L72]]; [[#L76-L77]]). When $r_1 < r_2 - r_1$, $\Delta r = r_1$, and the central $d\rho/dr$ is too large by the factor $(r_2 - r_1)/r_1$. What follows: The $d\rho/dr$ terms of `B(1)` and of the right-hand side `D(1)` ([[#L62-L65]]) would be wrong, and with them `QUAD` near the center. Only with rotation (`LROT`, off by default), and only on a grid whose first point lies closer to the center than to the second.

    **A possible fix:**

    ```diff
    --- a/src/getqua.f
    +++ b/src/getqua.f
    @@ -58,7 +58,10 @@
           DRI = 1.0D0/DR/HRU(1)
     C CENTRAL BOUNDARY CONDITION : QUADRUPOLE GOES TO ZERO.
           A(1) = 0.0D0
    -      DRHO = (EXP(CLN*HD(2))-EXP(CLN*HD(1)))/DR
    +C 11/10/26 KC via Claude
    +C code changed to divide by the interval R2-R1, not by DR, which is R1
    +C when R1 < R2-R1.
    +      DRHO = (EXP(CLN*HD(2))-EXP(CLN*HD(1)))/(HRU(2)-HRU(1))
           B(1) = -FAC*(FPL+FMI)+DRI*(FMI-FPL)-6.0D0/HRU(1)**2
          *        -C4PIG*DRHO/HG(1)
           C(1) = FPL*(FAC+DRI)
    ```

    **Checked by running YREC** (Nov 10, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Of the five cases run, only the rotating one, `testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`, called GETQUA (the others were `testsuite/Test_m1p0feh+0p0GS98_base_TAMS`, `testsuite/Test_m0p3feh+0p0GS98_base_ZAMS`, `testsuite/Test_m1p4feh+0p0GS98_dif_TAMS`, and `examples/run_standard_solar_model/Test_solarcal_noGS_norot`). There the central row was set up 2,252 times, for models of 350 to 419 shells, with $r_1/(r_2 - r_1)$ from 16.0 to 17.9. The first point always lay farther from the center than from the second, so `DR` was $r_2 - r_1$ and the central $d\rho/dr$ the right forward difference; the condition $r_1 < r_2 - r_1$ never held. The fix was not run: With `DR` equal to $r_2 - r_1$ it computes the same number. What would reach it: a model whose first shell is closer to the center than to the second. Intent: none found.

### GETQUA

Solves the second-order ODE for the quadrupole moment with a tridiagonal solver (equation above); results in `QUADRU_MOD`.
