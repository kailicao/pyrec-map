## Explanation

**Purpose.** `FPFT` computes, for every shell of a rotating model, the form factors $f_P$ and $f_T$ that correct the stellar structure equations for rotational distortion, together with the mean effective gravity on each equipotential. The equipotentials' shapes come from [[shape.f#SHAPE|SHAPE]]; the angular averages from a Gauss–Legendre quadrature.

**How it fits.**
- **Who calls it:** the main program ([[main.f#(file level)|main.f]]), [[crrect.f#CRRECT|CRRECT]] (the structure correction, iterated), [[hpoint.f#HPOINT|HPOINT]] and [[starin.f#STARIN|STARIN]].
- **Inputs:** `HD`, `HR`, `HS` ($\log\rho$, $\log r$, $\log m$ in cgs), `OMEGA` ($\Omega$ per shell, rad s$^{-1}$), `M`.
- **What it calls:** `SHAPE` (the run of $r_0$ and $\eta_2$), [[trapzd.f#TRAPZD|TRAPZD]] (trapezoid rule for the distortion integral), [[polint.f#POLINT|POLINT]] (polynomial extrapolation) and [[qgauss.f#QGAUSS|QGAUSS]] (the angular quadrature, which calls [[func.f#FUNC|FUNC]]).
- **Outputs:** `FP`, `FT` (the form factors), `HG` (mean gravity $\langle g\rangle$), `ETA2` ($\eta_2$, from Radau's equation as computed in `SHAPE`), `R0`. It also fills [[quadd_mod.f#QUADD_MOD|`QUADD_MOD`]] with the spherical, rotational and distortion potentials `PHISP`, `PHIROT`, `PHIDIS`, read by [[checkj.f#CHECKJ|CHECKJ]], [[vcirc.f#VCIRC|VCIRC]] and [[wrtmod.f#WRTMOD|WRTMOD]].
- **Modules:** `QUADD_MOD` (above); constants from [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]].

**The method.** The method is, in the YREC paper's words (§2.6.2), "a modified version of the R. Kippenhahn & H. C. Thomas (1970) technique," which "assumes uniform rotation on equipotential surfaces" (the paper's §2.6 traces the approach to Endal & Sofia 1976, whom SHAPE's comment cites too): each shell has one $\Omega$ (one `OMEGA` per shell), and the equipotentials are $r = r_0(1 - aP_2)$ (SHAPE's comment), keeping only the $P_2$ term (how accurate that stays for fast rotators is [[#q3]]). For each shell, outward:
1. The distortion amplitude $a = \dfrac{5}{3}\dfrac{\Omega^2 r_0^3}{Gm\,(2+\eta_2)}$.
2. The integral $I(r_0) = \int_0^{r_0}(\ldots)\,dr_0'$ (its integrand, per `TRAPZD`'s comment, is $(\rho/m)\,r_0'^7\,\Omega^2(5+\eta_2)/(2+\eta_2)$) is added shell by shell: the trapezoid rule on the step from the previous shell, refined once and extrapolated to zero step with `POLINT` (a Romberg step; `JMAX` = 2, tolerance $10^{-6}$). `PHIDIS` $= \tfrac{4\pi}{3} I/r^3$ (`C4PI*CC13*AINT/RPHI3`, [[#L98]]), the distorted potential of the comment ("needed for the evaluation of the distorted potential," [[#L45-L47]]); what $I$ is physically is [[#q2]]. The interpolation inside `TRAPZD` that this integral relies on is a suspected bug, [[trapzd.f#b1]].

    > **Question** ([[#L41-L42]]; [[#L67-L85]]). **Romberg with two levels.** With `JMAX` = 2 the refinement stops after one halving whether or not the tolerance is met; the result is then used without a warning (the jump to label 50 and the end of the loop lead to the same line, [[#L85]]). Is two levels enough?

    > **Question** ([[#L60-L62]]; [[trapzd.f#L23-L26]]). **What $I$ is.** If $\eta_2 = d\ln a/d\ln r_0$ ([[shape.f#q1]]), the integrand $(\rho/m)\,r_0'^7\,\Omega^2(5+\eta_2)/(2+\eta_2)$, with step 1's $a$, is $\tfrac{3G}{5}\rho\,d(a r_0'^5)/dr_0'$, so that $I(r_0) = \tfrac{3G}{5}\int_0^{r_0}\rho\,d(a r_0'^5)$ would be ($G$ times) the quadrupole moment of the distorted mass inside $r_0$, and `PHIDIS` the amplitude of the $P_2/r^3$ term it adds to the gravitational potential (the YREC paper, §2.6.2, mentions "contributions from the quadrupole term in the potential"). Is that the reading?

3. `QGAUSS` integrates over $0 \le \theta \le \pi/2$ the surface element $S$, $gS$ and $S/g$, giving $S_\Phi$, $S_\Phi\langle g\rangle$ and $S_\Phi\langle g^{-1}\rangle$.
4. With $r_\Phi$ the shell's radius (`HR`),
$$f_P = \frac{4\pi r_\Phi^4}{Gm\,S_\Phi\langle g^{-1}\rangle},\qquad f_T = \frac{(4\pi r_\Phi^2)^2}{S_\Phi\langle g\rangle\;S_\Phi\langle g^{-1}\rangle},$$
which is the usual Kippenhahn–Thomas form, $f_T = (4\pi r_\Phi^2/S_\Phi)^2/(\langle g\rangle\langle g^{-1}\rangle)$, provided `QGAUSS`'s outputs are the surface integrals named above (read from its code). `HG` = $\langle g\rangle$. They enter the structure as $d\ln P/d\ln m = -\dfrac{Gm^2}{4\pi r^4P}f_P$ ([[coefft.f#COEFFT|COEFFT]]) and $\nabla_\mathrm{rad} = \dfrac{3\kappa LP}{64\pi\sigma Gm T^4}\dfrac{f_T}{f_P}$ ([[tpgrad.f#TPGRAD|TPGRAD]]); both are 1 without rotation.

    > **Question** ([[shape.f#L40-L45]]; [[#L60-L62]]). **Accuracy for fast rotators.** Keeping only the $P_2$ term makes the shapes, and so $f_P$ and $f_T$, first order in $\Omega^2$, with each equipotential one of constant $P$, $T$ and $\rho$ under the assumed rotation law. Does the method lose accuracy for rapid rotators near break-up, and does the code limit $\Omega$ (or warn) where it does?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`; the unused `/ROT/` and `/CCOUT/` are gone, which settles the former question 2.

### FPFT

Form factors $f_P$, $f_T$ and $\langle g\rangle$ for every shell of a rotating model (method above); also the potentials in `QUADD_MOD`.
