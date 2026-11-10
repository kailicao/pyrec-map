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

> **Question** ([[#L45-L46]]). **"Skip convective zones."** The comment above the loop says so, but every shell is computed; the argument `LC` that could have marked them was never read in the loop and has been removed ([[#L31]]). Is the comment stale, or should convective shells be skipped?

Species 3 still counts among the ions in $\sum n_i$ ([[#b2]]), and three of the isotope masses in `WEIGHT` are mistyped ([[#b3]]).

**Changed since `rp_1`.** Declarations only: `COMMON/TEMP/`, `/SCRTCH/` and `/CONST1/` to `TEMP_MOD`, `SCRTCH_MOD` and `CONSTANTS_MOD`, `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Bugs, by priority

1. **(harmless in the runs)** **`ELECN` is not the electron density.** ([[#L48]]; [[#L57]]; [[#L61]]; [[#L73]]) The comment says the loop finds "MEAN CHARGE PER ION(ZF) AND NE," and `ELECN` enters the Coulomb logarithm `LAMBD1` as the electron density. But `ELECN = ZF*RHO/AMU` uses the mean charge per ion, $\bar Z\rho/m_u$, while the electron density is $n_e = (\rho/m_u)\sum_i X_i Z_i/A_i = \bar Z\,\rho/m_u\,\sum_i n_i$: `ELECN` is too large by $1/\sum_i n_i$, the mean ion mass (about 1.3 in the Sun), so $\ln\Lambda$ is too small by about $\tfrac12\ln 1.3 \approx 0.13$. This changes the molecular viscosity, `VISC`, which reaches the rotational mixing ([[vcirc.f#VCIRC|VCIRC]], through [[midmod.f#MIDMOD|MIDMOD]]'s `VISCM`); only in rotating runs (`LROT`, off by default).

    **A possible fix:**

    ```diff
    --- a/src/viscos.f
    +++ b/src/viscos.f
    @@ -58,7 +58,10 @@
              T = DEXP(CLN*HT(IM))
              T2 = T**2
              RHO = DEXP(CLN*HD(IM))
    -         ELECN = ZF*RHO/AMU
    +C 11/09/26 KC via Claude
    +C code changed to compute the electron density NE from the number
    +C densities, as the comment says, not the mean charge per ion.
    +         ELECN = ZF*COMSUM*RHO/AMU
     C  RADIATIVE DYNAMIC VISCOSITY (ELECTRON SCATTERING ONLY):
     C  METHOD USED(VISCR) IS FROM LEDOUX,1958,HANDBUCH DER PHYSIK VOL.LI,P.445
     C  ENDAL-SOFIA(VISCR2) METHOD REF. THOMAS,L.H. 1930,QUART.J.MATH,1,237
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): VISCOS ran in all 33 cases run, with rotation or without (from 441 to about 7.5 million times), at $\log T$ = 3.58 to 8.34, and $\sum_i n_i$ (`COMSUM`) differed from 1 by more than $10^{-3}$ nearly everywhere (from 0.26 to 1.07), so `ELECN` was off by the factor $1/\sum_i n_i$. Without rotation the viscosity is unused, and the fix leaves `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` identical. In the 3 $M_\odot$ rotating case (`testsuite/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2`) the fix's effect is about the size of the null change, not clearly beyond it (central $Y$ moves 1.2 times as much): $\log L$ moves by up to 0.0022 dex, against 0.0076 for a null change (nearly every opacity, all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$, times $1 + 10^{-10}$, on the same case), and central $Y$ by 0.017 against 0.014. The other rotating cases were not run with the fix. Intent: The comment ([[#L48]]) promises $n_e$.

2. **(harmless in the runs)** **The total $Z$ counts as an ion.** ([[#L38-L42]]; [[#L52-L57]]; [[#L73]]) Species 3, the total metal fraction $Z$, has weight 1.0 and charge 0 ([[#L38-L42]]). The loops over $Z_i^2$ skip it ([[#L78]]; [[#L83]]; [[#L97]]), but it adds $Z/1.0$ to `COMSUM` ([[#L54]]), as a neutral particle of mass 1 would, so the mean charge per ion $\bar Z$ = `ZF` is too small, and the CNO isotopes of species 5–11 are counted twice in $\sum n_i$. What follows: $\bar Z$ enters the Coulomb logarithm `LAMBD1` ([[#L73]]), and so the molecular viscosity `VISC`, which reaches the rotational mixing; only in rotating runs (`LROT`, off by default). Leaving species 3 out drops the metals other than CNO from $\sum n_i$; giving it their mean mass and charge instead would keep them.

    **A possible fix:**

    ```diff
    --- a/src/viscos.f
    +++ b/src/viscos.f
    @@ -51,7 +51,11 @@
              COMSUM = 0.0D0
              DO 10 I = 1,11
                 COMPN(I) = HCOMP(I,IM)/WEIGHT(I)
    -            COMSUM = COMSUM + COMPN(I)
    +C 11/10/26 KC via Claude
    +C code changed to leave species 3, the total Z, out of the number of
    +C ions, as the sums over Z**2 do: It has no charge, and its CNO is
    +C already counted in species 5 to 11.
    +            IF(I.NE.3) COMSUM = COMSUM + COMPN(I)
                 ZF = ZF + COMPN(I)*Z(I)
        10    CONTINUE
              ZF = ZF/COMSUM
    ```

    **Checked by running YREC** (Nov 10, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): In `testsuite/Test_solarGS98_difrotmixper18p4d1p0` (a rotating solar model with settling, to 4.568 Gyr), VISCOS added species 3 to `COMSUM` at 1,789,275 shells, at $\log T$ = 4.04 to 7.19, with $Z$ = 0.0169 to 0.0190. With the fix, the effect is about the size of the null change, not clearly beyond it (the surface rotation velocity, the closest, moves 1.3 times as much): $\log L$ moves by up to 0.00021 dex, against 0.00029 for a null change (nearly every opacity, all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$, times $1 + 10^{-10}$, on the same case); the surface rotation velocity by 0.0089 km/s against 0.0068, the surface $\log$ Li by 0.00056 dex against 0.00061, and central $Y$ by 0.0000067 against 0.000061; the track has 1,203 models in both. VISCOS also ran, 1,209 times, in the non-rotating `testsuite/Test_m1p0feh+0p0GS98_spot25_ZAMS`, where the viscosity is unused. Intent: none found; the comment ([[#L48]]) asks for the "MEAN CHARGE PER ION."

3. **(harmless in the runs)** **Three isotope masses are mistyped.** ([[#L38-L40]]) `WEIGHT` gives $^{15}$N 15.0011, $^{17}$O 16.99491, and $^{18}$O 17.99491, against the atomic masses 15.00011, 16.99913, and 17.99916; the code's own nuclear mass of $^{18}$O is 17.994772 ([[rates.f#L150]]; [[engeb.f#L260]]). The atomic mass unit and $\sigma$ ([[#L37]]; [[#L107]]) are also written in the code rather than taken from `CONSTANTS_MOD`. What follows: The number densities of the three trace species, and through them `COMSUM`, `ZF`, and the molecular viscosity, are slightly off; only in rotating runs (`LROT`, off by default).

    **A possible fix:**

    ```diff
    --- a/src/viscos.f
    +++ b/src/viscos.f
    @@ -35,9 +35,12 @@
     C and COMMON/CONST3/ into a single COMMON/CONSTANTS/
           REAL*8 LAMBD1
           DATA AMU/1.6605655D-24/
    +C 11/10/26 KC via Claude
    +C code changed to the atomic masses of N15, O17 and O18 (15.00011,
    +C 16.99913, 17.99916), which were mistyped.
           DATA WEIGHT/1.007825D0,4.0026D0,1.0D0,3.01603D0,12.0D0,
    -     * 13.00335D0,14.00307D0,15.0011D0,15.99491D0,16.99491D0,
    -     * 17.99491D0/
    +     * 13.00335D0,14.00307D0,15.00011D0,15.99491D0,16.99913D0,
    +     * 17.99916D0/
           DATA Z/1.0D0,2.0D0,0.0D0,2.0D0,6.0D0,6.0D0,7.0D0,7.0D0,8.0D0,
          * 8.0D0,8.0D0/
           SAVE
    ```

    **Checked by running YREC** (Nov 10, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): In `testsuite/Test_solarGS98_difrotmixper18p4d1p0`, the masses were used at 1,789,275 shells, at $\log T$ = 4.04 to 7.19, where the three species together make up a mass fraction of 0.0000029 to 0.0000033. With the fix, the effect is about the size of the null change, not clearly beyond it (the surface rotation velocity moves 1.4 times as much, the surface $\log$ Li 1.1 times): $\log L$ moves by up to 0.00027 dex, against 0.00029 for a null change (nearly every opacity, all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$, times $1 + 10^{-10}$, on the same case); the surface rotation velocity by 0.0095 km/s against 0.0068, the surface $\log$ Li by 0.00068 dex against 0.00061, and central $Y$ by 0.000046 against 0.000061; the track has 1,203 models in both. Intent: The other masses in `WEIGHT` are atomic masses, and those of $^{17}$O and $^{18}$O repeat the decimals of $^{16}$O's 15.99491, so these look like typing slips.

### VISCOS

The kinematic viscosity (radiative, Ledoux 1958, plus molecular, Spitzer 1962) and the radiative thermal diffusivity of every shell, into `TEMP_MOD`.
