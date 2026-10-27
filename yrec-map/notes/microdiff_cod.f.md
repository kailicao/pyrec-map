## Explanation

**Purpose.** Computes the settling coefficients of one species at each point of the equally spaced grid, "in the method of the Thoul routine", for [[microdiff_run.f#MICRODIFF_RUN|MICRODIFF_RUN]]. Its header (G. Somers, 5/15) says it was written for light-element diffusion; it now serves hydrogen and metals too.

**How it fits.**
- **Inputs:** `NPT` points with radius `ER` (units of $R_\odot$), density `EDEN` (g cm⁻³), temperature `ETEM` (K), $d\ln P/dr$ (`EHQPR`), $\nabla$ (`EDELR`), the three abundances `ESPEC(3,·)`, and the species' weight `THEA`, charge `THEZ` and column `J`.
- **Who calls it:** only `MICRODIFF_RUN`, once on the grid points and once on the midpoints.
- **What it calls:** [[thdiff.f#THDIFF|THDIFF]], which solves for the diffusion coefficients of the four-species mixture (H, He, the species, electrons).
- **Outputs:** `ECOD1` and `ECOD2`, and the hydrogen concentration gradient `EDXDR`, written on the hydrogen call ($J = 1$) and read on later calls.
- **Modules:** `CONSTANTS_MOD` (`CC13` $=1/3$), `NMLPAR_MOD` (the namelist factors `FGRY` and `FGRZ`, set by [[parmin.f#PARMIN|PARMIN]]) and `DIMENSIONS_MOD` (`JSON`).

**The method.** At each point, with mass fractions $X_k$ (floored at $10^{-24}$), weights $A_k$ (1.008, 4.004, `THEA`, $5.486\times10^{-4}$) and charges $Z_k$ (1, 2, `THEZ`, −1):
1. **Concentrations** relative to electrons: $c_k = \dfrac{X_k/A_k}{\sum_l Z_l X_l/A_l}$ for the three ions, $c_e = 1$.
2. **Electron and ion densities:** $n_e = \rho / (m_p \sum_k A_k c_k)$ with $m_p = 1.6726\times10^{-24}$ g, $n_i = \sum_\mathrm{ions} c_k\, n_e$.
3. **Lengths:** the inter-ionic distance $a_0 = (3/(4\pi n_i))^{1/3}$ (`0.23873` $= 3/4\pi$), the Debye length $\lambda_D = 6.9010\,\sqrt{T/(n_e \sum_k c_k Z_k^2)}$ cm, and $\lambda = \max(\lambda_D, a_0)$.
4. **Coulomb logarithms** for each pair:
$$x_{kl} = \frac{2.3939\times10^{3}\, T\, \lambda}{|Z_k Z_l|},\qquad \ln\Lambda_{kl} = 0.81245\,\ln\!\left(1 + 0.18769\, x_{kl}^{1.2}\right).$$
5. **`THDIFF`** returns the coefficients $A_P$ (`TAP`), $A_T$ (`TAT`) and $A_{kl}$ (`TAC`).
6. **The coefficients.** With $f = F\, r'^2\, T'^{5/2} / 2.2$ ($r'$ in $R_\odot$, $T'$ in $10^7$ K, 2.2 the fixed `LN_LAMBDA`; $F$ is `FGRY` on the hydrogen call, $J = 1$, `FGRZ` on the third column, $J = 3$, and 1 otherwise, the same factors as in [[setup_grsett.f#SETUP_GRSETT|SETUP_GRSETT]]):
$$C_1 = -f\left[(A_P + A_T\nabla)\,\frac{d\ln P}{dr} + A_{j1}\,\frac{d\ln c_H}{dr}\right] X_j ,\qquad C_2 = -f\,A_{jj}.$$
The comment writes the velocity as $A_P\, d\ln P/dr + A_T\, d\ln T/dr + A_X\, d\ln X/dr + A_D\, d\ln D/dr$; here $d\ln T/dr = \nabla\, d\ln P/dr$. The hydrogen term is dropped on the hydrogen call (it is the same as the last term) and is zero at the first and last points; $d\ln c_H/dr$ is a centred difference.

**KC's changes.** 2025-05-31: the unused array `FGRLI` (a per-element factor, commented out in the code) removed from the declarations.

**Changed since `rp_1`.** The settling coefficients are now scaled by `FGRY` (hydrogen) and `FGRZ` (the third column), as in the older settling routines (JvS, 01/26); `LN_LAMBDA` is now the double-precision `2.2D0`; COMMON blocks to modules, `IMPLICIT NONE`; the unused `/SCRTCH/` and `/THEAGE/` are gone and `/GRAVS3/`'s factors are now used, which settles the former question 4 (declared but unused blocks).

## Questions for the experts

1. **The hydrogen gradient on the midpoints.** On the midpoint call, `EDXDR` is the midpoint array `EDXDR_H`, filled only when hydrogen is diffused. When `LDIFY` is false, `EDXDR` is never computed and holds zeros (or old values), so the $A_{j1}$ term silently vanishes for metals and light elements. Intended?
2. **Two Coulomb logarithms.** Pairwise Coulomb logarithms go into `THDIFF`, but the coefficient is also divided by a fixed $\ln\Lambda = 2.2$, and the time unit in [[microdiff_setup.f#MICRODIFF_SETUP|MICRODIFF_SETUP]] "includes factor of 2.2 from ln Lambda". Do the two cancel exactly, as the units suggest?
3. **Skipped points.** Where the species' abundance is exactly zero at a point and the next, only `ADS(I)` is set to zero; `FACS`, `APS`, `ATS` and `AHS` keep values from an earlier point or call (`SAVE`). The product with $X_j = 0$ makes $C_1$ zero, so this is harmless, but fragile.
4. **`FGRZ` for light elements.** `FGRZ` scales every call with $J = 3$, which [[microdiff.f#MICRODIFF|MICRODIFF]] uses both for the metals (`LDIFZ`) and for each light element (`LDIFLI`), so a factor named for metals also scales lithium, beryllium and boron settling; in [[setup_grsett.f#SETUP_GRSETT|SETUP_GRSETT]] it scales the metals only. Intended?
