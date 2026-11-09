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

1. **(a)** **The interpolation does not move with the midpoint.** ([[#L34-L35]]; [[#L44-L47]]) Inside the loop over midpoints, $\rho$, $\Omega^2$ and $\eta_2+2$ are interpolated at `RHOP+DRHO*DEL` (and likewise), the same value for every midpoint $y_j$; only $m$ uses $y_j$ (`SMT`, [[#L45]]). With FPFT's `JMAX` = 2 ([[fpft.f#L42]]) only the call with `N` = 2 refines, with `IT` = 1 and `DEL` = $b_2 - b_1$, so that the "midpoint" values are those of the outer shell, while $m$ and $r_0$ are taken at the midpoint. What follows: The distortion integral `AINT`, and through [[func.f#FUNC|FUNC]] the gravity $g$ and FPFT's $f_P$, $f_T$, are computed with the wrong integrand at the midpoint; the error is of the order of the change of $\rho$, $\Omega^2$ and $\eta_2$ between neighbouring shells. Only with rotation (`LROT`, off by default). Read from the code, not run; the size of the effect was not traced. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to interpolate RHO, OMEGA**2 and ETA2+2 at the midpoint
    C Y, as M already is.
              RHOT = RHOP+DRHO*(Y-B1)
              SMT = SMP+DM*(Y**2 - B1**2)
              W2T = W2P + DW2*(Y-B1)
              ETA22T = ETA22P + DETA2*(Y-B1)
    ```

### TRAPZD

One refinement of the trapezoidal rule for FPFT's integral of $\rho\,\Omega^2 r_0^7/m \cdot (5 + \eta_2)/(2 + \eta_2)$ between two shells.
