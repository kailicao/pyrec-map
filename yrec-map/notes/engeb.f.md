## Explanation

**Purpose.** This file computes the nuclear energy generation rate at one point, its derivatives with respect to density and temperature, the rates of the individual reactions (for the abundance changes), the solar neutrino fluxes and, in hot cores, the neutrino energy losses. Its long header, mostly by John Bahcall (JNB, 1990–1997) and Marc Pinsonneault (MHP), documents the reaction data: rates from *Neutrino Astrophysics* (Bahcall 1989) and the Solar Fusion Workshop (Adelberger et al. 1998), energy releases from Bahcall and Ulrich (1988, RMP 60, 297), screening from Salpeter (1954) and Graboske et al. (1973), alpha captures from Caughlan and Fowler (1988), neutrino losses from Itoh et al. (1996) or an older fit.

**How it fits.**
- **Inputs:** the arguments `DL`, `TL` ($\log\rho$, $\log T$), the mass fractions `X`, `Y`, `XHE3`, `XC12`, `XC13`, `XN14`, `XO16`, `XO18`, `XH2`, and `IU` (the point's index, used to store the rates and for the deuterium cap). From the modules: the derivative factors `QS0E`, `QQS0EE` and the N15+p branch factors `FO16`, `FC12` ([[cross_mod.f#CROSS_MOD|`CROSS_MOD`]], set by [[remap.f#REMAP|REMAP]]: all 1, or with `LNEWNUC` from the namelist's cross-sections and their derivatives); from [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]], the cross-section factors `SSTANDARD(17)`, `WEAKSCREENING` (0.03 by default), the cut-off temperatures `TCUT`, `LSNU` (compute neutrino fluxes) and `LNULOS1` (Itoh losses); `JCZ` ([[deuter_mod.f#DEUTER_MOD|`DEUTER_MOD`]]) and `TAUCZ` ([[ovrtrn_mod.f#OVRTRN_MOD|`OVRTRN_MOD`]]) for the deuterium cap; `CLN`, `CC13`, `CC23` and `CAVOG` (Avogadro's number, $1/m_u$, for the deuterium rate) from [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]].
- **Who calls it:** [[coefft.f#COEFFT|COEFFT]] (every point, every iteration), the main program ([[main.f#(file level)|main.f]], for the neutrino fluxes and Be-7 of the output) and [[ytime.f#YTIME|YTIME]] (the time step). main.f's call sits in a neutrino-table block switched off by a hard-coded `.FALSE.` ([[main.f#L463]]), which passes an `IU` that main.f never sets ([[main.f#L506-L508]]); so the index never goes wrong in a run (settled from the code, Nov 9, 2026).
- **What it calls:** [[neutrino.f#NEUTRINO|NEUTRINO]] (the Itoh et al. losses), when `LNULOS1`.
- **Outputs:**
  - arguments: `EPP1`, `EPP2`, `EPP3` (energy from the pp chain's branches), `ECN` (CNO), `E3AL` (triple alpha), `SUM1` (the total, erg g$^{-1}$ s$^{-1}$), `PEP`, `PET` (its derivatives), and per point `HR1`…`HR13` (the reaction rates, per Gyr per amu) and `HF1` = $f_3$, `HF2` = $f_1$ (branching fractions); the abundance routines ([[kemcom.f#KEMCOM|KEMCOM]] and others) use the rates, per the comment; `EALPCA` (energy from alpha captures) and `ENU` (neutrino losses), read by COEFFT and YTIME right after their calls (main.f passes locals it does not use); `BE7MASSFRACTION`, set only with `LSNU` and read only by main.f, which keeps it between calls by its `SAVE`;
  - modules: `FLUX(10)` ([[fluxes_mod.f#FLUXES_MOD|`FLUXES_MOD`]], neutrino fluxes at Earth per gram, read by COEFFT, main.f, [[wrtout.f#WRTOUT|WRTOUT]]).

**The method.**
1. **Screening.** With the mass fractions over 13 isotopes, $\mu_I^{-1} = \sum X_i/A_i$, $\mu_e^{-1} = \sum Z_iX_i/A_i$, $\zeta = \sum Z_i^2X_i/A_i$, and a degeneracy factor $f'/f$ (a fit to Salpeter's figure 1 in $\log E_F/kT$):
$$\Lambda_0 = 5.9426\times10^{-6}\,T_9^{-3/2}\sqrt{\rho/\mu_I}, \qquad U_\mathrm{weak} = Z_1Z_2\,\Lambda_0\,\sqrt{\frac{\zeta + (f'/f)\,\mu_e^{-1}}{\mu_I^{-1}}}.$$
Weak screening (Salpeter 1954) if $U_\mathrm{weak} \le$ `WEAKSCREENING`; otherwise Graboske et al.'s intermediate form ($U \le 2$), or the strong form ($U \ge 5$ or where it is smaller). The rate is multiplied by $e^{U}$, with $\partial U/\partial\ln\rho$ and $\partial U/\partial\ln T$.

    > **Question** ([[#L668-L679]]). **The default screening.** The code's default `WEAKSCREENING` = 0.03 uses weak screening only where $U_\mathrm{weak} \le 0.03$, so where $U_\mathrm{weak}$ exceeds 0.03 (in the solar core, a reader would expect) the pp and CNO rates take Graboske et al.'s intermediate form; the comment calls 0.03 the value for the standard solar model. The YREC paper (§2.3.4) says the default settings recommend weak screening for general use, and every test-suite run sets `WEAKSCREENING` = 30 (weak screening always). Which is meant to be the default, and how much does the choice change the solar calibration?
2. **pp chain and CNO** (reactions 1–7: pp, $^3$He+$^3$He, $^3$He+$^4$He, p+$^{12}$C, p+$^{13}$C, p+$^{14}$N, p+$^{16}$O), in the form of *Neutrino Astrophysics* eq. 3.14 and Fowler, Caughlan and Zimmerman:
$$r_j = \rho\left[T_9^{-2/3} + Q_1T_9^{-1/3} + s'_j(Q_2 + Q_3T_9^{1/3}) + s''_j(Q_4T_9^{2/3} + Q_5T_9)\right]\exp\!\left(Q_6T_9^{-1/3} + Q_7 + (Q_8T_9)^2 + U_j\right)S_j,$$
where $T_9 = T/10^9$ K; $Q_6T_9^{-1/3}$ is $-\tau$, the comments' TAU of *Neutrino Astrophysics* eq. 3.10 ("NOTE Q6 IS NEGATIVE"), $Q_7$ "the constant in front of the reaction rate", a logarithm that carries $-\ln S_0$ ($S_0$ in keV b), $-\ln(A_0A_1)$ and $-\ln(1+\delta_{01})$ by the comments' formula, $Q_1$–$Q_5$ the terms of the expansion of $S(E)$ about the Gamow peak (from $S'$ and $S''$), and $Q_8$ a high-temperature cutoff (zero for these reactions); $S_j$ = `SSTANDARD(J)` is a dimensionless factor on the reference cross section (1 for the coded value; the comments list the sets that reproduce published solar models, such as BP03 or the Gran Sasso 2009 values); $s'$, $s''$ = `QS0E`, `QQS0EE` (user factors on the S-factor derivatives, MHP 8/14), and the logarithmic derivatives `DRATRO`, `DRATT` (the temperature derivative of the bracket carries the same factors $s'_j$, $s''_j$).
3. **Branchings.** $^7$Be: electron capture against proton capture (with its own screening), $f_1$, $f_2$; $^{15}$N+p: ($p,\alpha$) against ($p,\gamma$), $f_3$, $f_4$.
4. **Alpha captures** (above `TCUT(4)`): $^{13}$C($\alpha$,n), $^{12}$C($\alpha,\gamma$), $^{14}$N($\alpha,\gamma$), and triple alpha, $r_{3\alpha} \propto \rho^2T_9^{-3}e^{-4.4027/T_9}$.
5. **Deuterium burning** (if $X_D > 10^{-11}$, and like every rate here only above `TCUT(1)`: below it the routine zeroes all rates, the deuterium rate included, before reaching this block; the documentation calls the default `TCUT(1)` = 6.5 "bad for D burning in preMS", and every test-suite run sets `TCUT(1)` = 5.5), as in [[deutrate.f#DEUTRATE|DEUTRATE]] (the rate $\propto T_9^{-2/3}$, times $N_A/A_D$ = `CAVOG/ANUC(3)`), with $Q = 5.494$ MeV; its logarithmic temperature derivative `QRTDEUT` is that of the same form. In the convective envelope (`IU` $\ge$ `JCZ`), when `TAUCZ` $> 1$, the rate is capped so that $r X \le (N_A/A_D)/\tau_\mathrm{cz}$ (`RDEUTMAX`).

    > **Question** ([[#L537]]; [[nmlpar_mod.f#L182]]). **The default `TCUT(1)`.** All rates, deuterium burning included, are zero for $\log T \le$ `TCUT(1)`, 6.5 by default, which the documentation calls "bad for D burning in preMS" and the test suite sets 5.5 everywhere. Should the default be lowered, or the deuterium term be taken out of the gate? The same cut stops pp burning and $^3$He production below $\log T = 6.5$, which a reader would expect to matter for the $^3$He profile of the Sun's outer core and for stars near the hydrogen-burning limit (the test suite's 0.1 $M_\odot$ run), whose central temperature is close to it.
6. **Energy.** $\epsilon_j = r_j X_aX_b\,Q_j$, with the $Q$ values in MeV net of neutrino losses: for example 6.664 for pp, 12.860 for $^3$He+$^3$He, and $1.586 + 17.394f_1 + 11.499f_2$ for $^3$He+$^4$He. A comment beside the pp value records a 1997 lowering by 0.002 MeV for a better estimate of the neutrino energy loss; the code does not say which reactions the 6.664 MeV covers ([[#L979]]). Then `SUM1` $= \sum\epsilon_j$, `PEP` $= \sum\epsilon_j\,\partial\ln r_j/\partial\ln\rho$, `PET` likewise in $T$: absolute derivatives, $\partial\epsilon/\partial\ln\rho$ and $\partial\epsilon/\partial\ln T$, which is how COEFFT uses them.

    > **Question** ([[#L973-L979]]; [[#L576]]). **What the pp $Q$ value covers.** The value 6.664 MeV matches p+p→d followed at once by d+p→³He, net of the pp neutrino's mean energy: 1.442 − 0.265 + 5.494 ≈ 6.67 MeV (only the 5.494 MeV of d+p is in the code, as deuterium's `QDEUT`; [[kemcom.f#KEMCOM|KEMCOM]]'s $-3r_1X^2$ does take three protons per pp reaction). Is that what 6.664 stands for, and where does the 0.007 MeV difference come from (the comment accounts for 0.002 MeV)? If so, the deuterium made by the pp reaction is taken to burn at once, and step 5 burns only the deuterium already present, so that nothing is counted twice: is that the intent?

    > **Question** ([[#L1054-L1063]]). **A comment that contradicts the code.** The comment "MHP 5/90 CHANGE DERIVATIVES TO BE D LN EPS/D LN RHO AND D LN EPS/D LN T" describes the commented-out lines below it, which divided by `SUM1`; the code returns `PEP = SUM2`, `PET = SUM3`, the absolute derivatives $\partial\epsilon/\partial\ln\rho$, $\partial\epsilon/\partial\ln T$. Should the comment be updated to say so?

    > **Question** ([[#L753]]; [[#L1043-L1049]]; [[#L1069-L1071]]). **Hard-coded thresholds.** Rates below $10^{-30}$ (before the abundances multiply them) and $10^{-5}$ (after the energies are summed) are set to zero; `SUM1` $\le 10^{-12}$ zeroes `PEP`, `PET` and the `EG` array (so the neutrino fluxes), but keeps `SUM1` itself and the `DG` array (so `EPP1`, `ECN`, …). Are these still appropriate, and should `SUM1` be zeroed too?
7. **Rates for the abundances:** `HR`$_j$ = $r_j C_{21}$, with $C_{21}$ = (s per $10^9$ yr) × (amu in g), per the comment.
8. **Neutrino fluxes** (if `LSNU` and $X > 10^{-6}$): pp, pep, hep, $^7$Be, $^8$B, $^{13}$N, $^{15}$O, $^{17}$F and two "fictional" diagnostics, per gram at 1 AU, in $10^{10}$ cm$^{-2}$ s$^{-1}$.
9. **Neutrino losses** (above `TCUT(5)`): from [[neutrino.f#NEUTRINO|NEUTRINO]] (Itoh et al. 1996) or the older fits for pair, photo- and plasma neutrinos; the loss is subtracted from `SUM1` and its derivatives from `PEP`, `PET`.

    > **Question** ([[#L1228]]; [[nmlpar_mod.f#L182]]). **Neutrino losses only above `TCUT(5)`.** Plasma, photo-, and pair-neutrino losses are computed only above $\log T$ = 7.5 (default and test suite). Is that low enough for the degenerate helium cores of low-mass red giants, where plasma neutrinos cool the center and move the helium ignition off center?

**Design.** About half the file is comments: the history of every constant, and sets of `SSTANDARD` from published solar models (BP92, BP95, BP03, Gran Sasso 2009, …). Reactions 8–13 are partly "holdovers from the earlier Yale code"; 9 and 13 are zeroed.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html): `TCUT(1)` (default 6.5) is the $\log T$ above which $\epsilon_\mathrm{nuc}$ is computed (too high for deuterium burning on the pre-main sequence); `LSNU` computes the solar neutrino fluxes; `WEAKSCREENING` (0.03) is the threshold for weak screening of the rates; `LNULOS1`, listed among the legacy options, uses the neutrino losses of Itoh et al. (1996).

**Changed since `rp_1`.** `EALPCA`, `ENU` (formerly `/NEWEPS/`) and `BE7MASSFRACTION` (formerly `/BE7/`) are now arguments, the last three; `DSNUDT`, `DSNUDD` (formerly `/NULOSS/`, read nowhere else) are locals; the constants given in single precision (the reaction and screening coefficients, the $Q$ values, `C21`, `CONVERT`, the neutrino-loss fits) are now double precision, and the exponents `0.6666667` and `0.666667` are now `CC23`, exactly 2/3, so results change slightly (probably in about the seventh digit); COMMON blocks to modules, `IMPLICIT NONE`.

**Changed since `09c3b9b`.** The deuterium rate now goes as $T_9^{-2/3}$ (`T9M23`, not `T9P23`), matching its derivative `QRTDEUT`, and uses `CAVOG` from `CONSTANTS_MOD` in place of $6.023\times10^{23}$, in the rate and in the cap `RDEUTMAX`; DEUTRATE now uses the same constants, which settles former question 4. In the pp/CNO loop, `DRATT` now multiplies the $Q_3$ term by `QS0E(I)` and the $Q_4$, $Q_5$ terms by `QQS0EE(I)`, as the rate does, which settles former question 9. Former questions 5–8 are now 4–7.

**Changed since `a8a5950`.** The energy deposited by $^{14}$N($\alpha,\gamma$)$^{18}$F($e^+\nu$)$^{18}$O (`DG(11)`, which enters `SUM1`, its derivatives, and `EALPCA`) is now 5.646 MeV, not 5.815: the code's comment derives it as $Q$ = 6.071 MeV (AME2020 mass excesses) less the mean neutrino energy, 0.425 MeV, where 5.815 had subtracted the mean positron energy. `ENGHE3` and `HE3ALL`, which fed only COEFFT's never-read arrays, are no longer set, and `GRAB_MOD` (removed since `a8a5950`) is no longer used.

## Bugs, by priority

1. **(a)** **The Itoh branch replaces the temperature derivative by the density derivative.** ([[#L1255-L1256]]) With `LNULOS1`, `PEP = PEP + DSNUDD` is followed by `PET = PEP + DSNUDT`, so `PET` becomes the density derivative of $\epsilon$ plus the loss's temperature term; `PET = PET + DSNUDT` is almost certainly meant. What follows: `PET` (COEFFT's `QET`) enters the derivative of the luminosity equation, `QLT` ([[coefft.f#L319]]), so the Henyey matrix is wrong wherever $\log T >$ `TCUT(5)` (7.5), which can slow or stop the convergence (a converged model satisfies the equations themselves, which do not use `PET`); in rotating runs COEFFT also stores it as `SQET` ([[coefft.f#L487]]), which SETUPV reads as a value ([[setupv.f#L439]]). `LNULOS1` is off by default (a legacy option in the documentation), but 41 of the 51 test-suite runs set it ("recommended to be set to TRUE"). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to add the neutrino loss's temperature derivative to
    C PET, not to PEP.
              PEP = PEP + DSNUDD
              PET = PET + DSNUDT
    ```

2. **(a)** **Relative derivatives added to absolute ones in the Itoh branch.** ([[#L1247-L1249]]; [[#L1255-L1256]]) `DSNUDT = -DSNUDT*T/ENU` and `DSNUDD = -DSNUDD*D/ENU` make the loss's derivatives relative, $\partial\ln\epsilon_\nu/\partial\ln T$, and they are then added to `PET`, `PEP`, which are absolute, $\partial\epsilon/\partial\ln T$ (step 6). The older branch adds absolute terms (`QETNX`, `QEDNX`, [[#L1314-L1315]]). What follows: the same reach as bug 1 (the Henyey matrix above `TCUT(5)`, and `SQET` in rotating runs), with `LNULOS1`. The division by `ENU` also fails where NEUTRINO returns `SNU` = 0. Read from the code, not run. **A possible fix** (with bug 1's):

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to keep the neutrino loss's derivatives absolute,
    C d ENU/d ln T and d ENU/d ln rho, as PEP and PET are.
              ENU = -SNU
              DSNUDT = -DSNUDT*T
              DSNUDD = -DSNUDD*D
    ```

3. **(a)** **The alpha captures' temperature derivatives.** ([[#L896-L898]]; [[#L909-L912]]; [[#L925-L927]]) For reactions 8, 10 and 11, `DRATT = DSCT + RHO/RATE*(…)` divides the derivative of the bracket by the whole rate, which includes the constant ($\sim10^{22}$) and $e^U$, not by the bracket alone; `DRATT` is then close to the screening term `DSCT` only. Also, in reaction 10, the derivatives of $R_1^2$ and $R_2^2$ lack a factor $T_9^{-2/3}$ ([[#L910-L911]]); in reaction 8, the terms of `A2`…`A5` lack the factor $T_9^{-3/2}$ that multiplies them in the rate ([[#L892]]; [[#L897-L898]]). The rates themselves are right. What follows: above `TCUT(4)` (7.7, on by default), `PET` misses most of the temperature dependence of $^{13}$C($\alpha$,n), $^{12}$C($\alpha,\gamma$) and $^{14}$N($\alpha,\gamma$), with the same reach as bug 1 (the Henyey matrix, and `SQET` in rotating runs). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to divide the derivative of each bracket by the
    C bracket, not by the rate, and to add the factors T9M32 (reaction 8)
    C and T9M23 (reaction 10) that the rates' terms carry.
          DRATT(8) = DSCT(8)+(DR1*A1 + R1*DA1 + T9M32*(
         *           A2*(9.373D0*T9M1-1.5D0)+A3*(11.873D0*T9M1-1.5D0)+
         *           A4*(20.409D0*T9M1-1.5D0)+A5*(29.283D0*T9M1-1.5D0)))
         *           /(A1*R1+T9M32*(A2+A3+A4+A5))
    ...
          DRATT(10) = DSCT(10)+(A1*((CC13*32.120D0*T9M13-2.0D0)*
         *            (A2+A3)+A2*(R1*CC13*0.1956D0*T9M23-2.0D0*
         *            (T9/3.496D0)**2)+A3*(CC13*1.0616D0*R2*T9M23))+
         *            A4*(27.499D0*T9M1-1.5D0)+A5*(5.0D0+15.541D0*T9M1))
         *            /(A1*(A2+A3)+A4+A5)
    ...
          DRATT(11) = DSCT(11)+(DR1*A1+R1*DA1+A2*
         *            (2.798D0*T9M1-1.5D0)+A3*(5.054D0*T9M1-1.5D0)+
         *            A4*(12.310D0*T9M1-CC23))/(A1*R1+A2+A3+A4)
    ```

4. **(d)** **The low-temperature path returns stale values.** ([[#L537-L550]]; [[#L1081-L1095]]; [[#L1132-L1219]]) Below `TCUT(1)` the routine jumps to label 200 without setting `SUM1` (an argument, so the caller gets back its own value), `F1`, `F3` (locals kept by `SAVE`, so `HF1`, `HF2` get the last burning point's branchings), or `RHO`, `T9` and the screening terms ([[#L555-L564]]), which with `LSNU` enter `FLUX(3)`. No caller takes this path today: COEFFT calls only above `TCUT(1)` ([[coefft.f#L281]]), YTIME at the hottest point of a model with $\log\rho_c \ge 5$ and at points above `TCUT(4)` ([[ytime.f#L69]]; [[ytime.f#L148]]), and main.f's call is switched off ([[main.f#L463]]). A new caller would get the stale values. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to return zero energy, branchings and neutrino fluxes
    C below TCUT(1), not values left from an earlier call.
          IF(TL.LE.TCUT(1)) THEN
    ...
             PET = 0.
             SUM1 = 0.0D0
             F1 = 0.0D0
             F3 = 0.0D0
    ...
          IF(LSNU)THEN
    C MHP 9/91 CHANGE TO TURN OFF NEUTRINO CALC FOR HYDROGEN-EXHAUSTED CORE.
             IF(X.LE.1.0D-6 .OR. TL.LE.TCUT(1))THEN
    ```

### ENGEB

Nuclear energy generation at one point: screening, the pp/CNO rates with S-factor scaling, $^7$Be and $^{15}$N branchings, alpha captures, deuterium burning, energies net of neutrinos, derivatives `PEP`/`PET`, per-reaction rates `HR1`–`HR13`, solar neutrino fluxes and neutrino losses.
