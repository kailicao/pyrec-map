## Explanation

**Purpose.** `VISCOS` computes, for every shell, the kinematic viscosity (radiative plus molecular) and the radiative thermal diffusivity, which the rotational mixing routines use (for example the Prandtl number $\nu/K$ in [[vcirc.f|vcirc.f]]). It also computes the Endal & Sofia versions "for comparison only" (`VISCR2`, `VISMO2`, `VISC2`, [[#L67]], [[#L93-L103]]; unused?: they are neither stored nor returned).

**How it fits.**
- **Inputs:** the composition `HCOMP` (its first 11 species), $\log\rho$ (`HD`), $\log T$ (`HT`), and through modules the opacity `SO` (`SCRTCH_MOD`) and $c_P$ `CP` (`TEMP_MOD`), filled by [[physic.f#PHYSIC|PHYSIC]].
- **Who calls it:** only [[physic.f#PHYSIC|PHYSIC]].
- **Outputs:** in `TEMP_MOD` (formerly `COMMON/TEMP/`), `VISC` (cm²/s) and `THDIF` (cm²/s), shared with [[getw.f#GETW|GETW]], [[hpoint.f#HPOINT|HPOINT]] and [[midmod.f#MIDMOD|MIDMOD]].

**The method.** With `HCOMP`'s species $i$ of mass $A_i$ (`WEIGHT`) and charge $Z_i$ (`Z`), $n_i = X_i/A_i$, the mean ion charge $\bar Z = \sum n_i Z_i/\sum n_i$ and `ELECN` = $\bar Z\rho/m_u$ (used as $n_e$ below, which it is not: see Bugs, by priority, 1):
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

> **Question** ([[#L45-L46]]). **"Skip convective zones".** The comment above the loop says so, but every shell is computed; the argument `LC` that could have marked them was never read in the loop and has been removed ([[#L31]]). Is the comment stale, or should convective shells be skipped?

> **Question** ([[#L48-L57]], [[#L38-L42]]). **The total $Z$ as a species.** Species 3 (the total metal fraction $Z$) has weight 1.0 and charge 0; it is skipped in the sums over $Z_i^2$, but it adds $Z/1.0$ to `COMSUM`, and so lowers $\bar Z$, as a neutral particle of mass 1 would. Should it be left out of `COMSUM` (or given the mean mass and charge of the metals not among species 5–11)?

> **Question** ([[#L37-L40]], [[#L107]]). **Hard-coded constants.** The atomic mass unit, $\sigma$ and the isotope masses are written in the code, not taken from `CONSTANTS_MOD`; some masses differ from standard values ($^{15}$N 15.0011, $^{17}$O 16.99491 and $^{18}$O 17.99491, against about 15.0001, 16.9991 and 17.9992). Are the three masses typing slips, and should the constants come from `CONSTANTS_MOD`?

**Changed since `rp_1`.** Declarations only: `COMMON/TEMP/`, `/SCRTCH/` and `/CONST1/` to `TEMP_MOD`, `SCRTCH_MOD` and `CONSTANTS_MOD`, `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Bugs, by priority

1. **(a)** **`ELECN` is not the electron density.** ([[#L48]]; [[#L57]]; [[#L61]]; [[#L73]]) The comment says the loop finds "MEAN CHARGE PER ION(ZF) AND NE", and `ELECN` enters the Coulomb logarithm `LAMBD1` as the electron density. But `ELECN = ZF*RHO/AMU` uses the mean charge per ion, $\bar Z\rho/m_u$, while the electron density is $n_e = (\rho/m_u)\sum_i X_i Z_i/A_i = \bar Z\,\rho/m_u\,\sum_i n_i$: `ELECN` is too large by $1/\sum_i n_i$, the mean ion mass (about 1.3 in the Sun), so $\ln\Lambda$ is too small by about $\tfrac12\ln 1.3 \approx 0.13$. This changes the molecular viscosity, `VISC`, which reaches the rotational mixing ([[vcirc.f#VCIRC|VCIRC]], through [[midmod.f#MIDMOD|MIDMOD]]'s `VISCM`); only in rotating runs (`LROT`, off by default). Read from the code, not run; how much the mixing changes was not traced. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to compute the electron density NE from the number
    C densities, as the comment says, not the mean charge per ion.
             ELECN = ZF*COMSUM*RHO/AMU
    ```

### VISCOS

The kinematic viscosity (radiative, Ledoux 1958, plus molecular, Spitzer 1962) and the radiative thermal diffusivity of every shell, into `TEMP_MOD`.
