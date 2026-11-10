## Explanation

**Purpose.** `TRAPZD` is a refinement step of the trapezoidal rule (Numerical Recipes' `trapzd`), specialised to one integral of the rotation code: between two shells, $r_{0,i-1}$ and $r_{0,i}$ (`B1`, `B2`), it integrates, by its comment,
$$\int \frac{\rho}{m}\; r_0^7\;\Omega^2\;\frac{5 + \eta_2}{2 + \eta_2}\; dr_0 ,$$
which [[fpft.f#FPFT|FPFT]] needs, with its derivatives, to find the mean effective gravity.

**How it fits.**
- **Who calls it:** only [[fpft.f#FPFT|FPFT]], with `N = 1, 2, 3, …` (each call doubles the number of points).
- **Inputs:** $\rho$, $m$, $\Omega^2$ and $\eta_2 + 2$ at both shells (`RHO`/`RHOP`, `SM`/`SMP`, `W2`/`W2P`, `ETA22`/`ETA22P`), and `QP`, the integrand at the inner shell.
- **Outputs:** the running estimate `S`, and `Q`, the integrand at the outer shell (on the first call).
- **Modules:** none.

**The method.** The integrand is
$$q(r_0) = \frac{\rho\,\Omega^2\,r_0^7}{m}\;\frac{3 + (\eta_2 + 2)}{\eta_2 + 2}.$$
On the first call, $S = \tfrac12 (b_2 - b_1)(q_1 + q_2)$. Each later call adds the midpoints of the current intervals,
$$S \leftarrow \tfrac12\left(S + \Delta \sum_j q(y_j)\right),\qquad \Delta = \frac{b_2 - b_1}{n_\mathrm{it}},$$
and doubles $n_\mathrm{it}$ (`IT`, kept by `SAVE`). Between the shells, $\rho$, $\Omega^2$ and $\eta_2$ are meant to be interpolated linearly in $r_0$ (the code takes them at the same point for every midpoint: [[#b1]]), and $m$ linearly in $r_0^2$. The number of intervals `IT` is set on the call with `N = 1` ([[#L30]]), so every integral must start with `N = 1`; FPFT's loop does so for every shell ([[fpft.f#L67-L71]]) (settled from the code, Nov 9, 2026).

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`; the unused `COMMON/CONST1/` and `/CONST2/` dropped.

## Bugs, by priority

1. **(harmless in the runs)** **The interpolation does not move with the midpoint.** ([[#L34-L35]]; [[#L44-L47]]) Inside the loop over midpoints, $\rho$, $\Omega^2$ and $\eta_2+2$ are interpolated at `RHOP+DRHO*DEL` (and likewise), the same value for every midpoint $y_j$; only $m$ uses $y_j$ (`SMT`, [[#L45]]). With FPFT's `JMAX` = 2 ([[fpft.f#L42]]) only the call with `N` = 2 refines, with `IT` = 1 and `DEL` = $b_2 - b_1$, so that the "midpoint" values are those of the outer shell, while $m$ and $r_0$ are taken at the midpoint. What follows: The distortion integral `AINT`, and through [[func.f#FUNC|FUNC]] the gravity $g$ and FPFT's $f_P$, $f_T$, are computed with the wrong integrand at the midpoint; the error is of the order of the change of $\rho$, $\Omega^2$ and $\eta_2$ between neighbouring shells. Only with rotation (`LROT`, off by default).

    **A possible fix:**

    ```diff
    --- a/src/trapzd.f
    +++ b/src/trapzd.f
    @@ -41,10 +41,13 @@
            DO 10 J = 1,IT
               R03T = Y**3
     C INTERPOLATE RHO,M,OMEGA,ETA2+2 BETWEEN SHELL I AND SHELL I-1
    -          RHOT = RHOP+DRHO*DEL
    +C 11/09/26 KC via Claude
    +C code changed to interpolate RHO, OMEGA**2 and ETA2+2 at the midpoint
    +C Y, as M already is.
    +          RHOT = RHOP+DRHO*(Y-B1)
               SMT = SMP+DM*(Y**2 - B1**2)
    -          W2T = W2P + DW2*DEL
    -          ETA22T = ETA22P + DETA2*DEL
    +          W2T = W2P + DW2*(Y-B1)
    +          ETA22T = ETA22P + DETA2*(Y-B1)
     C CALCULATE Q BETWEEN SHELLS
               Q0 = (RHOT*W2T*R03T*(3.0D0+ETA22T)/(SMT*ETA22T))*R03T*Y
     C Q0 = RHO*W2*R07T*(3.0D0+ETA22)/(SM*ETA22)
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The midpoint was evaluated in all five rotating test cases, from about 1.2 to 19.8 million times, and the interpolated density was off by more than 0.1% in most of them (1.1 to 19.7 million times; by up to 100%). With the fix, the 3 $M_\odot$ case (`testsuite/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2`) stays within the noise: $\log L$ moves by up to 0.009 dex, against 0.0076 for a null change (nearly every opacity, all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$, times $1 + 10^{-10}$, on the same case), central $\log T$ by 0.0010 against 0.0008. In the 0.8 $M_\odot$ case (`testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`) $\log L$ and central $\log T$ stay within the noise, and central $X$ and $Y$ moved by up to 0.00015 at 0.395 Gyr, about four and a half times a null change, the same amount at the same age as with SHAPE's fix of $\eta_2$ ([[shape.f#SHAPE|SHAPE]], bug 1). Rechecked on Nov 10, 2026, with a build without counting lines in SHAPE and TRAPZD, and beside it a null change of the distortion itself (the first shell's $\eta_2$ times $1 + 10^{-10}$): Model by model, every change, the null one included, stays below $10^{-7}$ in central $X$ until about 0.046 Gyr, where central $X$ stops falling, and grows to some $10^{-5}$ by 0.16 Gyr, so this case amplifies whatever perturbs it there, and the size of the change depends on the build. In that build, TRAPZD's fix again moves central $X$ by 0.00015 at 0.3955 Gyr ($1.7\times10^{-4}$ at that one model, against at most $6.1\times10^{-5}$ for the null change, and about $6\times10^{-5}$ against $4\times10^{-5}$ over the main sequence after it), while SHAPE's fix now gives $5.8\times10^{-5}$ at 0.222 Gyr: The shared number was a coincidence of the case's sensitivity, not one fix acting through the other. TRAPZD's change is about three times the null change at one model and of its size elsewhere, and $\log L$ moves by up to 0.00018 dex against 0.00019: not clearly above the noise. The 2 $M_\odot$ cases, which rotate faster, were not run with the fix. Intent: The comment ([[#L43]]) says the values are interpolated between the shells, as $m$ is, so this looks like a slip.

### TRAPZD

One refinement of the trapezoidal rule for FPFT's integral of $\rho\,\Omega^2 r_0^7/m \cdot (5 + \eta_2)/(2 + \eta_2)$ between two shells.
