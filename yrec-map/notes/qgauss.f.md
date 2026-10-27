## Explanation

**Purpose.** Ten-point Gauss–Legendre quadrature over the polar angle on one equipotential shell of a rotating star. It returns three integrals that [[fpft.f#FPFT|FPFT]] uses to find the shell's mean gravity $\langle g\rangle$ and $\langle g^{-1}\rangle$ ("find <g> and <g-1> across the shell by Gaussian quadrature", in FPFT's comment), and from them the distortion factors $f_P$ and $f_T$.

**How it fits.**
- **Inputs:** the upper limit `B` of the angle; the shell's data passed through to the integrand (`R0`, `HS`, `AINT`, `Q`, `W2`, `A`, the shell index `I`).
- **Who calls it:** only [[fpft.f#FPFT|FPFT]].
- **What it calls:** [[func.f#FUNC|FUNC]], which returns at an angle the local effective gravity `G` $= |\nabla\Phi| = \sqrt{(\partial\Phi/\partial r)^2 + (\partial\Phi/\partial\theta)^2}$ (as the code writes it) and the surface element `S` ($\propto 2\pi r\sin\theta$, `C4PI*R*DSIN(X)*…`).
- **Outputs:** `G0G` $= \int g\,dS$, `GINVG` $= \int g^{-1}\,dS$, `SPHIG` $= \int dS$, all over $\theta\in[0, B]$.

**The method.** With $x_m = x_r = B/2$ and the five positive nodes $\xi_j$ and weights $w_j$ of the 10-point rule,
$$\int_0^B f\,d\theta \approx x_r \sum_{j=1}^{5} w_j\left[f(x_m + x_r\xi_j) + f(x_m - x_r\xi_j)\right],$$
applied to $g\,s$, $s/g$ and $s$.

**Changed since `rp_1`.** Declarations only: `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE` (the unused `/CONST1/` and `/CONST2/` dropped).
