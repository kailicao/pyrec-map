## Explanation

**Purpose.** `FPFT` computes, for every shell of a rotating model, the form factors $f_P$ and $f_T$ that correct the stellar structure equations for rotational distortion, together with the mean effective gravity on each equipotential. The equipotentials' shapes come from [[shape.f#SHAPE|SHAPE]]; the angular averages from a Gauss–Legendre quadrature.

**How it fits.**
- **Who calls it:** the main program ([[main.f#(file level)|main.f]]), [[crrect.f#CRRECT|CRRECT]] (the structure correction, iterated), [[hpoint.f#HPOINT|HPOINT]] and [[starin.f#STARIN|STARIN]].
- **Inputs:** `HD`, `HR`, `HS` ($\log\rho$, $\log r$, $\log m$ in cgs), `OMEGA` ($\Omega$ per shell, rad s$^{-1}$), `M`.
- **What it calls:** `SHAPE` (the run of $r_0$ and $\eta_2$), [[trapzd.f#TRAPZD|TRAPZD]] (trapezoid rule for the distortion integral), [[polint.f#POLINT|POLINT]] (polynomial extrapolation) and [[qgauss.f#QGAUSS|QGAUSS]] (the angular quadrature, which calls [[func.f#FUNC|FUNC]]).
- **Outputs:** `FP`, `FT` (the form factors), `HG` (mean gravity $\langle g\rangle$), `ETA2` ($\eta_2$, from Radau's equation as computed in `SHAPE`), `R0`. It also fills `/QUADD/` with the spherical, rotational and distortion potentials `PHISP`, `PHIROT`, `PHIDIS`, read by [[checkj.f#CHECKJ|CHECKJ]], [[vcirc.f#VCIRC|VCIRC]] and [[wrtmod.f#WRTMOD|WRTMOD]].
- **COMMON blocks:** `/QUADD/` (above); `/ROT/` and `/CCOUT/` are declared but not used here; constants from `/CONST1/`, `/CONST2/`.

**The method.** For each shell, outward:
1. The distortion amplitude $a = \dfrac{5}{3}\dfrac{\Omega^2 r_0^3}{Gm\,(2+\eta_2)}$.
2. The integral $I(r_0) = \int_0^{r_0}(\ldots)\,dr_0'$ (its integrand, per `TRAPZD`'s comment, is $(\rho/m)\,r_0'^7\,\Omega^2(5+\eta_2)/(2+\eta_2)$) is added shell by shell: the trapezoid rule on the step from the previous shell, refined once and extrapolated to zero step with `POLINT` (a Romberg step; `JMAX` = 2, tolerance $10^{-6}$).
3. `QGAUSS` integrates over $0 \le \theta \le \pi/2$ the surface element $S$, $gS$ and $S/g$, giving $S_\Phi$, $S_\Phi\langle g\rangle$ and $S_\Phi\langle g^{-1}\rangle$.
4. With $r_\Phi$ the shell's radius (`HR`),
$$f_P = \frac{4\pi r_\Phi^4}{Gm\,S_\Phi\langle g^{-1}\rangle},\qquad f_T = \frac{(4\pi r_\Phi^2)^2}{S_\Phi\langle g\rangle\;S_\Phi\langle g^{-1}\rangle},$$
which is the usual Kippenhahn–Thomas form, $f_T = (4\pi r_\Phi^2/S_\Phi)^2/(\langle g\rangle\langle g^{-1}\rangle)$, provided `QGAUSS`'s outputs are the surface integrals named above (read from its code). `HG` = $\langle g\rangle$.

**KC's changes.** The unused argument `I` was removed from the call to `TRAPZD` (2025-05-31).

## Questions for the experts

1. **Romberg with two levels.** With `JMAX` = 2 the refinement stops after one halving whether or not the tolerance is met; the result is then used without a warning. Is two levels enough?
2. **Unused COMMON blocks.** `/ROT/` and `/CCOUT/` are declared but not used here. Remove?

### FPFT

Form factors $f_P$, $f_T$ and $\langle g\rangle$ for every shell of a rotating model (method above); also the potentials in `/QUADD/`.
