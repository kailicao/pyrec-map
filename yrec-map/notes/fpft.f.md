## Explanation

**Purpose.** `FPFT` computes, for every shell of a rotating model, the form factors $`f_P`$ and $`f_T`$ that correct the stellar structure equations for rotational distortion, together with the mean effective gravity on each equipotential. The equipotentials' shapes come from [SHAPE](https://github.com/yreclab/yrec/blob/7be4133/src/shape.f#L2-L170); the angular averages from a Gauss–Legendre quadrature.

**How it fits.**
- **Who calls it:** the main program ([main.f](main.f.md#file-level)), [CRRECT](crrect.f.md#crrect) (the structure correction, iterated), [HPOINT](hpoint.f.md#hpoint) and [STARIN](starin.f.md#starin).
- **Inputs:** `HD`, `HR`, `HS` ($`\log\rho`$, $`\log r`$, $`\log m`$ in cgs), `OMEGA` ($`\Omega`$ per shell, $`\mathrm{rad\,s^{-1}}`$), `M`.
- **What it calls:** `SHAPE` (the run of $`r_0`$ and $`\eta_2`$), [TRAPZD](trapzd.f.md#trapzd) (trapezoid rule for the distortion integral), [POLINT](https://github.com/yreclab/yrec/blob/7be4133/src/polint.f#L6-L61) (polynomial extrapolation) and [QGAUSS](https://github.com/yreclab/yrec/blob/7be4133/src/qgauss.f#L4-L43) (the angular quadrature, which calls [FUNC](func.f.md#func)).
- **Outputs:** `FP`, `FT` (the form factors), `HG` (mean gravity $`\langle g\rangle`$), `ETA2` ($`\eta_2`$, from Radau's equation as computed in `SHAPE`), `R0`. It also fills [`QUADD_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/quadd_mod.f#L19-L33) with the spherical, rotational and distortion potentials `PHISP`, `PHIROT`, `PHIDIS`, read by [CHECKJ](checkj.f.md#checkj), [VCIRC](vcirc.f.md#vcirc) and [WRTMOD](wrtmod.f.md#wrtmod).
- **Modules:** `QUADD_MOD` (above); constants from [`CONSTANTS_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/constants_mod.f#L37-L75).

**The method.** The method is, in the YREC paper's words (§2.6.2), "a modified version of the R. Kippenhahn & H. C. Thomas ([1970](https://ui.adsabs.harvard.edu/abs/1970stro.coll...20K)) technique," which "assumes uniform rotation on equipotential surfaces" (the paper's §2.6 traces the approach to Endal & Sofia [1976](https://ui.adsabs.harvard.edu/abs/1976ApJ...210..184E), whom SHAPE's comment cites too): each shell has one $`\Omega`$ (one `OMEGA` per shell), and the equipotentials are $`r = r_0(1 - aP_2)`$ (SHAPE's comment), keeping only the $`P_2`$ term (how accurate that stays for fast rotators is [question 3](#q3)). For each shell, outward:
1. The distortion amplitude $`a = \dfrac{5}{3}\dfrac{\Omega^2 r_0^3}{Gm\,(2+\eta_2)}`$.
2. The integral $`I(r_0) = \int_0^{r_0}(\ldots)\,dr_0'`$ (its integrand, per `TRAPZD`'s comment, is $`(\rho/m)\,r_0'^7\,\Omega^2(5+\eta_2)/(2+\eta_2)`$) is added shell by shell: the trapezoid rule on the step from the previous shell, refined once and extrapolated to zero step with `POLINT` (a Romberg step; `JMAX` = 2, tolerance $`10^{-6}`$). `PHIDIS` $`= \tfrac{4\pi}{3} I/r^3`$ (`C4PI*CC13*AINT/RPHI3`, [line 98](https://github.com/yreclab/yrec/blob/7be4133/src/fpft.f#L98)), the distorted potential of the comment ("needed for the evaluation of the distorted potential," [lines 45–47](https://github.com/yreclab/yrec/blob/7be4133/src/fpft.f#L45-L47)); what $`I`$ is physically is [question 2](#q2). The interpolation inside `TRAPZD` that this integral relies on is a suspected bug, [trapzd.f, suspected bug 1](trapzd.f.md#b1).

    > **Question** ([lines 41–42](https://github.com/yreclab/yrec/blob/7be4133/src/fpft.f#L41-L42); [lines 67–85](https://github.com/yreclab/yrec/blob/7be4133/src/fpft.f#L67-L85)). **Romberg with two levels.** With `JMAX` = 2 the refinement stops after one halving whether or not the tolerance is met; the result is then used without a warning (the jump to label 50 and the end of the loop lead to the same line, [line 85](https://github.com/yreclab/yrec/blob/7be4133/src/fpft.f#L85)). Is two levels enough?

    > **Question** ([lines 60–62](https://github.com/yreclab/yrec/blob/7be4133/src/fpft.f#L60-L62); [trapzd.f, lines 23–26](https://github.com/yreclab/yrec/blob/7be4133/src/trapzd.f#L23-L26)). **What $`I`$ is.** If $`\eta_2 = d\ln a/d\ln r_0`$ ([shape.f, question 1](shape.f.md#q1)), the integrand $`(\rho/m)\,r_0'^7\,\Omega^2(5+\eta_2)/(2+\eta_2)`$, with step 1's $`a`$, is $`\tfrac{3G}{5}\rho\,d(a r_0'^5)/dr_0'`$, so that $`I(r_0) = \tfrac{3G}{5}\int_0^{r_0}\rho\,d(a r_0'^5)`$ would be ($`G`$ times) the quadrupole moment of the distorted mass inside $`r_0`$, and `PHIDIS` the amplitude of the $`P_2/r^3`$ term it adds to the gravitational potential (the YREC paper, §2.6.2, mentions "contributions from the quadrupole term in the potential"). Is that the reading?

3. `QGAUSS` integrates over $`0 \le \theta \le \pi/2`$ the surface element $`S`$, $`gS`$ and $`S/g`$, giving $`S_\Phi`$, $`S_\Phi\langle g\rangle`$ and $`S_\Phi\langle g^{-1}\rangle`$.
4. With $`r_\Phi`$ the shell's radius (`HR`),
   
   $$\displaystyle f\_P = \frac{4\pi r\_\Phi^4}{Gm\\,S\_\Phi\langle g^{-1}\rangle},\qquad f\_T = \frac{(4\pi r\_\Phi^2)^2}{S\_\Phi\langle g\rangle\\;S\_\Phi\langle g^{-1}\rangle},$$
   
   which is the usual Kippenhahn–Thomas form, $`f_T = (4\pi r_\Phi^2/S_\Phi)^2/(\langle g\rangle\langle g^{-1}\rangle)`$, provided `QGAUSS`'s outputs are the surface integrals named above (read from its code). `HG` = $`\langle g\rangle`$. They enter the structure as $`d\ln P/d\ln m = -\dfrac{Gm^2}{4\pi r^4P}f_P`$ ([COEFFT](coefft.f.md#coefft)) and $`\nabla_\mathrm{rad} = \dfrac{3\kappa LP}{64\pi\sigma Gm T^4}\dfrac{f_T}{f_P}`$ ([TPGRAD](tpgrad.f.md#tpgrad)); both are 1 without rotation.

    > **Question** ([shape.f, lines 40–45](https://github.com/yreclab/yrec/blob/7be4133/src/shape.f#L40-L45); [lines 60–62](https://github.com/yreclab/yrec/blob/7be4133/src/fpft.f#L60-L62)). **Accuracy for fast rotators.** Keeping only the $`P_2`$ term makes the shapes, and so $`f_P`$ and $`f_T`$, first order in $`\Omega^2`$, with each equipotential one of constant $`P`$, $`T`$ and $`\rho`$ under the assumed rotation law. Does the method lose accuracy for rapid rotators near break-up, and does the code limit $`\Omega`$ (or warn) where it does?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`; the unused `/ROT/` and `/CCOUT/` are gone, which settles the former question 2.

### FPFT

Form factors $`f_P`$, $`f_T`$ and $`\langle g\rangle`$ for every shell of a rotating model (method above); also the potentials in `QUADD_MOD`.
