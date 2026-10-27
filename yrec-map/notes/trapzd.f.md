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
and doubles $n_\mathrm{it}$ (`IT`, kept by `SAVE`). Between the shells, $\rho$, $\Omega^2$ and $\eta_2$ are interpolated linearly in $r_0$, and $m$ linearly in $r_0^2$.

**KC's changes.** The unused argument `I` was removed (2025-05-31).

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`; the unused `COMMON/CONST1/` and `/CONST2/` dropped.

## Questions for the experts

1. **The interpolation does not move.** Inside the loop over midpoints, $\rho$, $\Omega^2$ and $\eta_2$ are interpolated at `RHOP+DRHO*DEL` (and likewise), the same value for every midpoint $y_j$; only $m$ uses $y_j$. Should `DEL` be `Y-B1` there?
2. **The state between calls.** The number of intervals `IT` lives in a `SAVE`d local, set on the call with `N = 1`. The routine relies on its caller to start every integral with `N = 1`.

### TRAPZD

One refinement of the trapezoidal rule for FPFT's integral of $\rho\,\Omega^2 r_0^7/m \cdot (5 + \eta_2)/(2 + \eta_2)$ between two shells.
