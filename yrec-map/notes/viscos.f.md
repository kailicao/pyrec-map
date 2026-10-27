## Explanation

**Purpose.** `VISCOS` computes, for every shell, the kinematic viscosity (radiative plus molecular) and the radiative thermal diffusivity, which the rotational mixing routines use (for example the Prandtl number $\nu/K$ in [[vcirc.f|vcirc.f]]). It also computes the Endal & Sofia versions "for comparison only".

**How it fits.**
- **Inputs:** the composition `HCOMP` (its first 11 species), $\log\rho$ (`HD`), $\log T$ (`HT`), and through modules the opacity `SO` (`SCRTCH_MOD`) and $c_P$ `CP` (`TEMP_MOD`), filled by [[physic.f#PHYSIC|PHYSIC]].
- **Who calls it:** only [[physic.f#PHYSIC|PHYSIC]].
- **Outputs:** in `TEMP_MOD` (formerly `COMMON/TEMP/`), `VISC` (cm²/s) and `THDIF` (cm²/s), shared with [[getw.f#GETW|GETW]], [[hpoint.f#HPOINT|HPOINT]] and [[midmod.f#MIDMOD|MIDMOD]].

**The method.** With `HCOMP`'s species $i$ of mass $A_i$ (`WEIGHT`) and charge $Z_i$ (`Z`), $n_i = X_i/A_i$, the mean ion charge $\bar Z = \sum n_i Z_i/\sum n_i$ and `ELECN` = $\bar Z\rho/m_u$:
1. **Radiative viscosity** (Ledoux 1958, electron scattering only, by the comment):
   $$\nu_\mathrm{rad} = 6.728\times10^{-26}\,\frac{T^4}{\kappa\,\rho^2}$$
   (the constant is $4a/15c$).
2. **Molecular viscosity** (Spitzer 1962). With the Coulomb logarithm
   $$\ln\Lambda = 9.4245 + \tfrac12\ln\!\left(\frac{T^3\,\min(1,\,4.2\times10^5/T)}{n_e\,\bar Z^2}\right),$$
   each species contributes
   $$\eta_i = \frac{3.125\times10^{-15}\,T^{5/2}\,n_i\sqrt{A_i}}{(\ln\Lambda - \ln Z_i)\,Z_i^2\,\sum_j n_j Z_j^2\sqrt{(A_i + A_j)/A_j}},$$
   and $\nu_\mathrm{mol} = \sum_i \eta_i/\rho$ (species 3, the total $Z$, has $Z_3 = 0$ and is skipped).
3. `VISC` $= \nu_\mathrm{rad} + \nu_\mathrm{mol}$.
4. **Thermal diffusivity** (radiation only; conduction neglected, by the comment):
   $$K = \frac{16\,\sigma\,T^3}{3\,\kappa\,\rho^2\,c_P},$$
   with $\sigma = 5.669\times10^{-5}$ written in the code.

**KC's changes.** The unused argument `LC` was removed (2025-05-31), with it the only means to skip convective zones (see question 1).

**Changed since `rp_1`.** Declarations only: `COMMON/TEMP/`, `/SCRTCH/` and `/CONST1/` to `TEMP_MOD`, `SCRTCH_MOD` and `CONSTANTS_MOD`, `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Questions for the experts

1. **"Skip convective zones".** The comment above the loop says so, but every shell is computed. Intended?
2. **The electron density.** `ELECN = ZF*RHO/AMU` uses the mean charge per ion, $\bar Z\rho/m_u$; the electron density is $\rho/m_u \sum_i X_i Z_i/A_i$, smaller by the mean ion mass. Is the Coulomb logarithm meant to use this approximation?
3. **The total $Z$ as a species.** Species 3 (the total metal fraction $Z$) has weight 1.0 and charge 0; it is skipped in the sums over $Z_i^2$, but it adds $Z/1.0$ to `COMSUM`, and so lowers $\bar Z$. Should it be left out of `COMSUM`?
4. **Comparison values never used.** `VISCR2`, `VISMO2`, `VISC2` (Endal & Sofia) are computed for every shell and discarded.
5. **Hard-coded constants.** The atomic mass unit, $\sigma$ and isotope masses are written in the code, not taken from `CONSTANTS_MOD`; some masses differ from standard values ($^{15}$N 15.0011, $^{17}$O 16.99491 and $^{18}$O 17.99491, against about 15.0001, 16.9991 and 17.9992).

### VISCOS

The kinematic viscosity (radiative, Ledoux 1958, plus molecular, Spitzer 1962) and the radiative thermal diffusivity of every shell, into `TEMP_MOD`.
