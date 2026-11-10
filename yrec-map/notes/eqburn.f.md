## Explanation

**Purpose.** `EQBURN` gives explicit hydrogen and helium burning rates for one shell or one convection zone, assuming that $^3$He and the CN cycle are in equilibrium. Its comment says the result is "an initial guess at the burning rates at the start of the time step," which a fully implicit non-equilibrium calculation can supplement later.

**How it fits.**
- **Who calls it:** [[mix.f#MIX|MIX]] (twice, to use the explicit hydrogen burning rate) and [[xtime.f#XTIME|XTIME]], which turns `DXDT` into a nuclear time step limit.
- **Inputs:** the reaction-rate arrays `HR1`…`HR12`, which both callers compute with [[rates.f#RATES|RATES]] just before the call. [[kemcom.f#KEMCOM|KEMCOM]]'s header gives their units: rates "per gigayear per amu," to be multiplied by the reactants' mass fractions and the product's atomic weight; so `DXDT` and the other outputs are changes of mass fraction per Gyr. Also: the shell masses `HS2`, the temperatures `HT` ($\log T$), and the range `IBEGIN..IEND`. The abundances come from the previous model, `HCOMPP` in `OLDMOD_MOD`.
- **Outputs:** the rates `DXDT`, `DYDT`, `DCDT`, `DODT` (hydrogen, helium, $^{12}$C, $^{16}$O) and the zone's mean `X`, `Z`, `XC12`, `XO16`.
- **Modules:** [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] gives the temperature cutoffs `TCUT(1..4)` (cutoffs in $\log T$, settings read in [[parmin.f#PARMIN|PARMIN]]; the defaults are 6.5, 6.5, 6.82, 7.7; formerly `/CTLIM/`); [[oldmod_mod.f#OLDMOD_MOD|`OLDMOD_MOD`]] (formerly `/OLDMOD/`) holds the previous model, written by the main program and read by many routines (listed on the modules page).

**The method.**
1. Below `TCUT(1)` at the zone's first shell, all rates are zero.
2. For a convection zone (`IBEGIN` ≠ `IEND`), abundances $X_j$ and rates $R_k$ are mass-weighted means over the zone, $\bar q = \sum_i q_i m_i / \sum_i m_i$ with $m_i$ = `HS2`.
3. **pp chains** (above `TCUT(2)`, if $X > 10^{-10}$). The equilibrium $^3$He abundance solves $2R_{33}x^2 + R_{34}Y x - R_{11}X^2 = 0$:
$$x_{3,\mathrm{eq}} = \frac{\sqrt{(R_{34}Y)^2 + 8R_{33}R_{11}X^2} - R_{34}Y}{4R_{33}},$$
with $R_{11}$ = `GR1`, $R_{33}$ = `GR2`, $R_{34}$ = `GR3`. The code takes $x_3 = \min(x_3, x_{3,\mathrm{eq}})$ "to avoid spuriously high burning rates in outer layers," and
$$\dot X = -3R_{11}X^2 + 2R_{33}x_3^2 - R_{34}Y x_3 .$$
4. **CN cycle** (above `TCUT(3)`, and only if step 3 ran). In equilibrium, $X_{12} = X_{14}R_{14}/R_{12}$ and $X_{13} = X_{14}R_{14}/R_{13}$, with $R_{12}, R_{13}, R_{14}$ = `GR4`, `GR5`, `GR6`, and the number of CN nuclei $S = X_{12}/12 + X_{13}/13 + X_{14}/14$ is conserved, so
$$X_{14} = \frac{S}{R_{14}/(12R_{12}) + R_{14}/(13R_{13}) + 1/14}.$$
Then $\dot X \mathrel{-}= X\,(R_{12}X_{12} + R_{13}X_{13} + 2R_{14}X_{14} + 2R_{16}X_{16})$, with $R_{16}$ = `GR7` ($^{16}$O + p). Two protons are counted for $^{16}$O + p as for $^{14}$N + p, since each rate stands for a pair of reactions: [[kemcom.f#KEMCOM|KEMCOM]]'s comments name them "N14,P + N15,P" and "O16,P + O17,P" ([[kemcom.f#L161-L164]]), and its network counts them the same way (settled from the code, Nov 9, 2026).

    **`MIX` expects the equilibrium CN abundances.** `XC12` is overwritten by its CN-equilibrium value in step 4 ([[#L199]]) and returned to the caller; [[mix.f#MIX|MIX]] (at `ITLVL` = 1) sets `HCOMP(5,·)` to `XC12 + DCDT*DT` from it where helium burns ([[mix.f#L311-L314]]; [[mix.f#L337-L346]]), and [[xtime.f#XTIME|XTIME]] uses only `DXDT`. That is consistent with MIX's comment that its explicit step solves for the rates "ASSUMING EQUILIBRIUM HE3 AND CN CYCLE ABUNDANCES" ([[mix.f#L286-L289]]), though the comment is about the rates and does not say that the equilibrium ¹²C should be stored. The helium-burning step also uses this equilibrium `XC12` for $^{12}$C + $\alpha$ ([[#L208]]); where $X \le 10^{-10}$ or $T$ is below `TCUT(2)`, no CN cycle runs ([[#L169]]) and the actual abundance passes through.
5. **Helium burning** (above `TCUT(4)`, if $Y > 10^{-10}$): with $r_{3\alpha} = R_{3\alpha}Y^3$ (`GR12`) and $r_{12\alpha} = R_{12\alpha}YX_{12}$ (`GR10`),
$$\dot Y = -4(r_{12\alpha} + 3r_{3\alpha}),\quad \dot X_{12} = 12(r_{3\alpha} - r_{12\alpha}),\quad \dot X_{16} = 16\,r_{12\alpha}.$$

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) lists `TCUT(2)` and `TCUT(3)` under "Unused parameters," as the former thresholds for pp-chain and CNO-cycle equilibrium; `TCUT(1)` (6.5) is the threshold for computing $\epsilon_\mathrm{nuc}$.

> **Question** ([[#L169]]; [[#L185]]; [[mix.f#L284-L351]]). **`TCUT(2)`, `TCUT(3)` "not used."** The documentation lists them as unused, but `EQBURN` tests them (`HT(IBEGIN).GT.TCUT(2)` for the equilibrium He3 and pp burning, `TCUT(3)` for the CN cycle), and [[mix.f#MIX|`MIX`]] calls `EQBURN` for each radiative shell and convection zone at `ITLVL = 1`. So they still matter there (defaults 6.5 and 6.82). Is the documentation out of date, or is that call meant to go?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Bugs, by priority

1. **(never occurred)** **Division by a rate that can be zero.** ([[#L174]]; [[#L190-L191]]) Step 3 divides by `GR2` ($^3$He + $^3$He), and step 4 by `GR4` and `GR5` (p + $^{12}$C, p + $^{13}$C). [[rates.f#RATES|RATES]] sets a rate to zero when it is at or below $10^{-5}$ ([[rates.f#L646-L648]]), when `SSTANDARD(J)` = 0, or when the shell's $X$ is 0, while the test here is on the previous model's mean $X$ (`HCOMPP`). With the default `TCUT(2)`, `TCUT(3)` (6.5, 6.82) the rates are well above the cut, so this is correct today; a zero rate would give `XHE3E` = 0/0 or an infinite `R1214`, and a NaN in `DXDT`.

    **A possible fix:**

    ```diff
    --- a/src/eqburn.f
    +++ b/src/eqburn.f
    @@ -171,18 +171,24 @@
     C THE EQUATION IS -2*R(3,3)*XHE3**2 - R(3,4)*XHE3*XHE4 + R(1,1)X**2 = 0.
              R11 = GR1*X**2
              R34 = GR3*Y
    -         XHE3E = 0.25D0*(SQRT(R34**2+8.0D0*GR2*R11)-R34)/GR2
    +C 11/09/26 KC via Claude
    +C code changed to skip the equilibrium 3He abundance, and the CN
    +C equilibrium, when a rate they divide by is zero.
    +         IF(GR2.GT.0.0D0)THEN
    +            XHE3E = 0.25D0*(SQRT(R34**2+8.0D0*GR2*R11)-R34)/GR2
     C USE THE MINIMUM OF THE CURRENT AND EQUILIBRIUM HE3 ABUNDANCE -
     C NEEDED TO AVOID SPURIOUSLY HIGH BURNING RATES IN OUTER LAYERS,
     C WHERE THE TIMESCALE FOR HELIUM-3 TO REACH EQUILIBRIUM IS LONG.
    -         XHE3 = MIN(XHE3,XHE3E)
    +            XHE3 = MIN(XHE3,XHE3E)
    +         ENDIF
     C PP BURNING.
              DXDT = -3.0D0*R11+2.0D0*GR2*XHE3**2-R34*XHE3
           ELSE
              DXDT = 0.0D0
              GOTO 100
           ENDIF
    -      IF(HT(IBEGIN).GT.TCUT(3))THEN
    +      IF(HT(IBEGIN).GT.TCUT(3) .AND. GR4.GT.0.0D0 .AND.
    +     *   GR5.GT.0.0D0)THEN
     C FIND EQUILIBRIUM C12,C13,N14 ABUNDANCES TREATING CN PROCESSING AS
     C A CLOSED LOOP.
              SUMCNO = XC12/1.2D1+XC13/1.3D1+XN14/1.4D1
    ```

    **Checked by running YREC** (Nov 9, 2026, the counts of `testsuite/Test_m1p0feh+0p0GS98_base_HeIgnite` repeated on Nov 10 with a private start model; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The explicit burning ran in 30 of 34 runs (26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones), up to 4,009,747 times (`testsuite/Test_m1p0feh+0p0GS98_base_HeIgnite`), at $\log T$ = 6.5 to 7.75 and $X$ from just above $10^{-10}$ to 0.745. `GR2`, `GR4`, and `GR5` were never zero, so the divisions never failed. A zero rate needs `TCUT(2)` or `TCUT(3)` lowered to where RATES cuts a rate at $10^{-5}$, or an `SSTANDARD` set to 0, which no case or document does. (Every namelist calls `TCUT(2)` and `TCUT(3)` "Not used," though this routine uses them.)

### EQBURN

Explicit burning rates for a shell or a convection zone, with $^3$He and CN in equilibrium (equations above).
