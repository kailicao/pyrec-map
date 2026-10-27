## Explanation

**Purpose.** `FUNC` evaluates, at one colatitude $\theta$ on an equipotential surface of a rotating star, the effective gravity $g = |\nabla\Phi|$ and the surface element. It is the integrand for the angular averages $\langle g\rangle$ and $\langle g^{-1}\rangle$ that the rotation form factors need.

**How it fits.**
- **Who calls it:** only [[qgauss.f#QGAUSS|QGAUSS]], a ten-point Gauss–Legendre quadrature over $0 \le \theta \le \pi/2$, called by [[fpft.f#FPFT|FPFT]].
- **Inputs:** `X` ($\theta$), `R0` (mean radii of the equipotentials), `HS` ($\log m$), `AINT` and `Q` (the distortion integral and its integrand, from [[trapzd.f#TRAPZD|TRAPZD]]), `W2` ($\Omega^2$), `A` (the distortion amplitude), `I` (the shell).
- **Outputs:** `G` ($g$) and `S` (the surface element per unit $\theta$).
- **Modules:** constants only ([[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]]: $4\pi$, $1/3$, $\ln 10$, $\log G$).

**The method.** With $P_2 = 1 - \tfrac32\sin^2\theta$, the equipotential is $r = r_0(1 - aP_2)$. Then
$$\frac{\partial\Phi}{\partial r} = \frac{Gm}{r^2} - \frac{4\pi}{3r^4}P_2\left(3I - rQ\,\frac{\partial r_0}{\partial r}\right) - \Omega^2 r\sin^2\theta,$$
$$\frac{\partial\Phi}{\partial\theta} = \frac{4\pi}{3r^4}\left(P_2\,Q\,\frac{\partial r_0}{\partial\theta} - 3I\cos\theta\sin\theta\right) - \Omega^2 r\cos\theta\sin\theta,$$
with $I$ = `AINT`, $\partial r_0/\partial r = 1/(1-4aP_2)$ and $\partial r_0/\partial\theta = 3a\cos\theta\sin\theta\,(\partial r_0/\partial r)/(1-aP_2)$, and
$$g = \sqrt{(\partial_r\Phi)^2 + (\partial_\theta\Phi)^2},\qquad S = 4\pi r\sin\theta\, r_0\sqrt{(1-aP_2)^2 + (3a\cos\theta\sin\theta)^2}.$$

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **Comment vs code.** The comment says "ASSUME DR0/DR = 1", but the code multiplies by `QR0R` $= 1/(1-4aP_2)$. Which is intended?
2. **Constants.** The comment writes the distortion terms as $12\pi G P_2 I/(5r^4)$ and $4\pi G P_2 Q/(5r^3)$; the code uses $4\pi/(3r^4)$ with no $G$ or 1/5. Probably those factors are absorbed into $I$ and $Q$ as `TRAPZD` defines them; could the comment be brought in line?
3. **The factor $4\pi$.** `S` carries $4\pi$ rather than the $2\pi$ of a ring, probably to count both hemispheres, since `QGAUSS` integrates over $0 \le \theta \le \pi/2$ only. Could a comment say so?

### FUNC

Effective gravity $g = |\nabla\Phi|$ and surface element on a distorted equipotential at colatitude $\theta$ (equations above).
