## Explanation

**Purpose.** `TPGRAD` decides whether a point is convective and gives its temperature gradient $\nabla = d\ln T/d\ln P$. It computes the radiative gradient, compares it with the adiabatic one (the Schwarzschild criterion), and in convective regions solves the mixing-length theory's cubic for the actual gradient and the convective velocity; on request it also gives the gradient's derivatives for the Henyey solution. Its comments assume that the equation of state and the opacity have been computed already.

**How it fits.**
- **Inputs:** arguments: $\log T$, $T$, $\log P$, $P$, $\rho$ (`D`), $\log r$, $\log m$ (`SL`), $L/L_\odot$ (`B`), the opacity $\kappa$ (`O`) and its derivatives, the equation-of-state quantities ($\delta = -$`QDT`, $c_P$ = `QCP`, $\nabla_\mathrm{ad}$ = `DELA`, and derivatives), the rotation factors `FPL`, `FTL`, $\log T_\mathrm{eff}$, and the mixing length `CMIXL` (set for each run by the main program, `CMIXL = CMIXLA(NK)`, and passed down by the callers). Through modules: the constants `CDELRL`, `CMIXL2`, `CMIXL3`, set by [[setups.f#SETUPS|SETUPS]], and `CC13` ([[constants_mod.f|`CONSTANTS_MOD`]]); the temperature above which MLT is skipped, `TGCUT`, the overshoot switch `LADOV` and the spot parameters `SPOTF`, `SPOTX`, `LSDEPTH` ([[nmlpar_mod.f|`NMLPAR_MOD`]]); the overshoot shells `IOV1`, `IOV2`, `IOVIM` ([[dpmix_mod.f|`DPMIX_MOD`]]); `ISHORT` ([[iounits_mod.f|`IOUNITS_MOD`]]).
- **Who calls it:** the routines that evaluate the physics at a point: [[physic.f#PHYSIC|PHYSIC]], [[coefft.f#COEFFT|COEFFT]], [[qenv.f#QENV|QENV]], [[sconvec.f#SCONVEC|SCONVEC]] and [[starin.f#STARIN|STARIN]].
- **Outputs:** `LCONV`, `DELR` ($\nabla_\mathrm{rad}$), `DEL` ($\nabla$), `VEL` (the convective velocity, cm/s), and with `LDERIV` the logarithmic derivatives of $\nabla$ (`QACT`, `QACP`, `QACR`). It sets `ALFMLT`, `PHMLT`, `CMXMLT` in [[pualpha_mod.f|`PUALPHA_MOD`]] to zero ([[#L77-L79]]) and never computes them, so the pulsation output's mixing-length columns are zeros: [[envint.f#ENVINT|ENVINT]] writes the three variables, and [[wrtmod.f#WRTMOD|WRTMOD]] writes literal zeros in their place, "which were always zero" (settled from the code, Nov 9, 2026: [[wrtmod.f#L291-L296]], [[coefft.f#L500-L502]], [[envint.f#L590-L592]]).

**The method.**
1. **Radiative gradient.** With `CDELRL` = $-\log(4\pi/3) - \log\sigma - \log 16$ (from `SETUPS`),
   $$\nabla_\mathrm{rad} = \frac{3\,\kappa\,L\,P}{64\pi\,\sigma\,G\,m\,T^4}\;\frac{f_T}{f_P},$$
   with $L = $ `B`$\,L_\odot$, and $f_P$, $f_T$ the rotational distortion factors.
2. **Radiative** if $\nabla_\mathrm{rad} - \nabla_\mathrm{ad} \le 10^{-6}$: $\nabla = \nabla_\mathrm{rad}$, $v = 0$; but inside an adiabatic overshoot region (`LADOV`, shell `IOVIM` between `IOV1` and `IOV2`) $\nabla = \nabla_\mathrm{ad}$. This is the Schwarzschild criterion, without the composition term $\nabla_\mu$; the YREC paper (§2.3.3) says the code "considers the Schwarzschild criterion for instability, not the Ledoux criterion," and semiconvection (`LSEMIC`, [[sconvec.f#SCONVEC|SCONVEC]]) is the option for $\mu$-gradient regions (settled from the YREC paper, Nov 9, 2026: [[#L80-L93]]).

    > **Question** ([[#L83]]). **The threshold $10^{-6}$.** A point is radiative when $\nabla_\mathrm{rad} - \nabla_\mathrm{ad} \le 10^{-6}$, not $\le 0$. Is the margin meant to keep `LC` from flickering at a zone's edge from one iteration to the next, and does it shift the edges measurably?
3. **Convective:** above `TGCUT` (cores), $\nabla = \nabla_\mathrm{ad}$ and $v = 10^{-11}$, without MLT. The YREC paper (§2.3.3) gives the reason: "In convective cores the specific heat is quite high and there is an option to skip MLT calculations; in this case the adopted temperature gradient is the adiabatic one." The $v = 10^{-11}$ cm/s set there is not a convective velocity, so `VEL` in these regions should not be used for overturn times or mixing.

    > **Question** ([[#L97-L107]]). **Skipping MLT in cores.** Above `TGCUT` the gradient is set to $\nabla_\mathrm{ad}$ without solving the cubic. Deep in a convective core, $\nabla - \nabla_\mathrm{ad}$ would be tiny (of order $10^{-7}$ or less), so the skip should change the structure negligibly while saving time: Is that the reasoning, and has the effect been measured?
4. **Spots** (G. Somers 9/14): the radiative flux in convective regions is reduced, $\nabla_\mathrm{rad} \to \nabla_\mathrm{rad}/(f x^4 + 1 - f)$, with $f$ = `SPOTF`; the contrast $x$ is `SPOTX`, or with `LSDEPTH` varies with depth as the comment derives, $x(T) = 1 - (1 - x_\mathrm{surf})\,T_\mathrm{amb}/T$. The correction comes after the point is found convective (but see bug 1).

    The returned `DELR` stays uncorrected, while `DEL` and `VEL` use the corrected gradient; the derivatives of `DELDEL` do not follow the correction ([[#b2]]).
5. **Mixing-length theory.** With $g = Gm/r^2$, $H_p = P/(\rho g)$, the mixing length $\ell = \alpha H_p$, with $\alpha$ = `CMIXL`, $\phi = \alpha\,\kappa\rho H_p$ (the optical thickness of an element), `CMIXL2` = 1/3 and `CMIXL3` = $16\sqrt2\,\sigma$:
   $$A_1 = \frac{16\sqrt2\,\sigma\,T^3\kappa}{c_P\,(1 + \phi^2/3)\,\sqrt{(\nabla_\mathrm{rad} - \nabla_\mathrm{ad})\,g\,\delta/H_p}},\qquad A_3 = \frac{3\phi^2}{4\,(1 + \phi^2/3)\,A_1},$$
   and the cubic
   $$A_3 V^3 + V^2 + A_1 V - 1 = 0$$
   is solved for $V$ by a Newton iteration with a second-order correction (at most 25 steps, tolerance $10^{-10}$), starting from $V = 1/A_1$, or $V = A_3^{-1/3}$ when $A_3 > 10^3$. Then
   $$\nabla = \nabla_\mathrm{ad} + (\nabla_\mathrm{rad} - \nabla_\mathrm{ad})\,V(V + A_1),\qquad v = V\,\sqrt{\frac{g\,\delta\,\alpha^2 H_p\,(\nabla_\mathrm{rad} - \nabla_\mathrm{ad})}{8}} .$$
   This is mixing-length theory (Böhm-Vitense 1958, as the YREC paper, §2.3.3, says). From the code's constants, for $\phi \gg 1$ the factor $1/(1 + \phi^2/3)$ drops out and $A_1 \to 2U/\sqrt{\nabla_\mathrm{rad} - \nabla_\mathrm{ad}}$, with $U = \dfrac{3acT^3}{c_P\rho^2\kappa\ell^2}\sqrt{\dfrac{8H_p}{g\delta}}$ (with $\ell = \alpha H_p$ in cm, $ac = 4\sigma$); $V$ is then the convective velocity in units of $\sqrt{g\delta\ell^2(\nabla_\mathrm{rad} - \nabla_\mathrm{ad})/(8H_p)}$. If the cubic does not converge, the point is taken as adiabatic, with a message. If $A_1$'s square root would be of a negative number, the run stops (`STOP 912`, "RUN ENDED"). The routine also computes `DELPM` and `RRR`, which nothing reads (unused?).

    > **Question** ([[#L139-L147]]; [[#L161]]). **Which variant of the theory.** The optically thin factor $1/(1 + \phi^2/3)$ and `CMIXL3` $= 16\sqrt2\,\sigma$ fix the variant of mixing-length theory; the calibrated $\alpha$ depends on it. Which published formulation do these constants follow? The factor looks like the correction for optically thin elements of the kind Henyey, Vardya & Bodenheimer (1965) introduced, and $U$ above like the efficiency in Kippenhahn, Weigert & Weiss's textbook: Are they?
6. **Derivatives** (`LDERIV`): of $A_1$, $A_3$ and $V$ with respect to $\ln T$, $\ln P$, $\ln r$, combined into those of $\nabla$.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html): above $\log T$ = `TGCUT` (default 6.9) convection is taken as adiabatic; `LADOV` (experimental) makes overshoot regions adiabatic. Starspots: `SPOTF` is the filling factor (default 0; 0.25 is the bound for active main-sequence stars), `SPOTX` the spots' temperature contrast (default 1; 0.85 is typical of sunspots; change it only if `SPOTF` > 0), and `LSDEPTH` lowers the contrast with depth, assuming a constant field, with no dramatic effect on the results.

**Changed since `rp_1`.** COMMON blocks to modules, `IMPLICIT NONE` (the unused `CTLIM` dropped); `CMIXL` is now an argument instead of a COMMON variable; the cubic's starting value uses `CC13` instead of the literal 0.333333333; the negative-square-root message now says "RUN ENDED" instead of "assumed adiabatic convection," which settles former question 2 (stopping is intended), so former questions 3–5 are now 2–4.

**Changed since `a8a5950`.** The convective velocity's second sign test is gone: Its radicand is the first test's times $H_p^2$, and a non-positive first test already stops the run (`STOP 912`), so its branch, which set `VEL = 1.0D0-11`, that is $-10$, could not be reached (settles former question 1).

## Bugs, by priority

1. **(never occurred)** **Spots can stop the run on a point that is convective without them.** ([[#L82-L83]]; [[#L127-L135]]; [[#L145-L156]]) The Schwarzschild test uses $\nabla_\mathrm{rad}$ without the spot correction. For a point found convective, `DELDEL` is then recomputed with the spotted $\nabla_\mathrm{rad}/(f x^4 + 1 - f)$, which is smaller; if this makes `DELDEL` zero or negative (a point near a zone's edge, where $\nabla_\mathrm{rad} - \nabla_\mathrm{ad}$ is small), `TEST` is not positive and the run stops (`STOP 912`, "RUN ENDED"). Only with spots (`SPOTF` ≠ 0; the default is 0).

    **A possible fix** (one choice: treat the point as radiative with the spotted gradient):

    ```diff
    --- a/src/tpgrad.f
    +++ b/src/tpgrad.f
    @@ -131,7 +131,16 @@
              ELSE
                 DEEPX = SPOTX
              ENDIF
    +C 11/09/26 KC via Claude
    +C code changed to treat a point as radiative when the spot correction
    +C makes it stable, instead of stopping at the square root below.
              DELDEL = DELR/(SPOTF * DEEPX**4.0 + 1.0 - SPOTF) - DELA
    +         IF(DELDEL.LE.1.0D-6)THEN
    +            LCONV = .FALSE.
    +            DEL = DELR/(SPOTF * DEEPX**4.0 + 1.0 - SPOTF)
    +            VEL = 0.0D0
    +            GOTO 200
    +         ENDIF
           ENDIF
     C G Somers END
           G = DEXP(CLN*(CGL + SL - RL - RL))
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Of 34 runs (26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones), one is spotted, `testsuite/Test_m0p1feh+0p0GS98_spot25_ZAMS`: The spot correction was applied 1,418,129 times, at $\log T$ = 3.46 to 6.66, and `DELDEL` stayed at 0.0788 or more, so it never turned a point stable and the run never stopped there. YREC's other spotted cases (`testsuite/Test_m0p3feh+0p0GS98_spot25_ZAMS` and `testsuite/Test_m1p0feh+0p0GS98_spot25_ZAMS`) were not run; reaching it needs a spotted point near a zone's edge where the correction makes `DELDEL` vanish. (`KNOWN_ISSUES.md` mentions the spot recomputation as a place to check for a `DELDEL` that is `NaN`, not this case.)

2. **(changes results, small)** **Checked by KC** (Nov 10, 2026). **With spots, the derivatives of the gradient are those of the unspotted one.** ([[#L127-L135]]; [[#L201-L202]]) With spots, `DELDEL` is $\nabla_\mathrm{rad}/S - \nabla_\mathrm{ad}$, with $S = f x^4 + 1 - f$ ([[#L134]]), but its logarithmic derivatives `QDDELT` and `QDDELP` ([[#L201-L202]]) put the unspotted `DELR` in their numerators and divide by the spotted `DELDEL`, so they are too small by about the factor $S$ ($S < 1$) where `DELDEL` is dominated by $\nabla_\mathrm{rad}$; with `LSDEPTH`, $x$ depends on $T$, and $d\ln S/d\ln T = 4 f x^3 (1 - x)/S$ is missing too. What follows: The derivatives of the convective gradient (`QACT`, `QACP`), which enter the Henyey solution's matrix, are wrong in spotted convective regions; the converged model should change only within the convergence tolerance. Whether the returned `DELR` should carry the factor $1/S$ as well is a separate choice. Only with spots (`SPOTF` ≠ 0; the default is 0).

    **A possible fix:**

    ```diff
    --- a/src/tpgrad.f
    +++ b/src/tpgrad.f
    @@ -30,7 +30,7 @@
          *       QA1R,QA1T,QA3P,QA3R,QA3T,QACP,QACR,QACT,QAP,QAT,QCP,QCPP,
          *       QCPT,QDDELP,QDDELT,QDELAP,QDELAT,QDP,QDT,QDTP,QDTT,QOD,QOT,
          *       QVP,QVR,QVT,RL,RRR,SL,T,TEFFL,TEMP1,TEMP2,TEMP3,TEMPOP,
    -     *       TEMPOT,TEST,TL,V,VD,VEL,VP,VTOL
    +     *       TEMPOT,TEST,TL,V,VD,VEL,VP,VTOL,SPFAC,DSPFT
           INTEGER ITER
           LOGICAL*4 LCONV,LDERIV
     
    @@ -133,6 +133,15 @@
              ENDIF
              DELDEL = DELR/(SPOTF * DEEPX**4.0 + 1.0 - SPOTF) - DELA
           ENDIF
    +C 11/10/26 KC via Claude
    +C code changed to keep the spot factor S and its derivative d ln S/d ln T
    +C (with LSDEPTH, X depends on T), for the derivatives of DELDEL below.
    +      SPFAC = 1.0D0
    +      DSPFT = 0.0D0
    +      IF(SPOTF .NE. 0.00)THEN
    +         SPFAC = SPOTF * DEEPX**4.0 + 1.0 - SPOTF
    +         IF(LSDEPTH) DSPFT = 4.0D0*SPOTF*DEEPX**3*(1.0D0 - DEEPX)/SPFAC
    +      ENDIF
     C G Somers END
           G = DEXP(CLN*(CGL + SL - RL - RL))
           PRESHT = P/(D*G)
    @@ -198,8 +207,10 @@
            QDELAP = QAP*DELA
            TEMPOT = QOD*QDT + QOT
            TEMPOP = QOD*QDP
    -       QDDELT = ((-4.0D0 + TEMPOT)*DELR - QDELAT)/DELDEL
    -       QDDELP = ((+1.0D0 + TEMPOP)*DELR - QDELAP)/DELDEL
    +C 11/10/26 KC via Claude
    +C code changed to differentiate the spotted DELR/S that DELDEL holds.
    +       QDDELT = ((-4.0D0 + TEMPOT - DSPFT)*DELR/SPFAC - QDELAT)/DELDEL
    +       QDDELP = ((+1.0D0 + TEMPOP)*DELR/SPFAC - QDELAP)/DELDEL
            TEMP1 = 2.0D0*CMIXL2*PHI2*PHIPHI
            QA1T = TEMPOT*(1D0-TEMP1)-QCPT-0.5D0*(QDT+QDDELT+QDTT/QDT)+3D0
            QA1P = TEMPOP*(1D0-TEMP1)-TEMP1-QCPP-0.5D0
    ```

    **How the code itself shows it.** Without spots, `DELDEL = DELR - DELA` ([[#L82]]), and the numerators `(-4.0D0 + TEMPOT)*DELR - QDELAT` and `(+1.0D0 + TEMPOP)*DELR - QDELAP` ([[#L201-L202]]) are its derivatives with respect to $\ln T$ and $\ln P$ ($\nabla_\mathrm{rad} \propto \kappa P/T^4$, `QDELAT = QAT*DELA`), so `QDDELT` and `QDDELP` are $d\ln$`DELDEL`$/d\ln T$ and $d\ln$`DELDEL`$/d\ln P$, which `QA1T` and `QA1P` use as such (`-0.5D0*(QDT+QDDELT+QDTT/QDT)`, [[#L204-L206]]; $A_1 \propto$ `DELDEL`$^{-1/2}$, [[#L147]]). With spots, `DELDEL = DELR/(SPOTF * DEEPX**4.0 + 1.0 - SPOTF) - DELA` ([[#L134]]), and the numerators are left unchanged.

    **Checked by running YREC** (Nov 10, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): In `testsuite/Test_m1p0feh+0p0GS98_spot25_ZAMS` (1 $M_\odot$, `SPOTF` = 0.25, `SPOTX` = 0.85, `LSDEPTH`), the derivatives were computed 974,865 times in spotted convective points, at $\log T$ = 3.64 to 6.57, with $S$ from 0.878 to 0.99982, so the condition held at every one. With the fix, $\log L$ moves by up to 0.00055 dex and $\log T_\mathrm{eff}$ by 0.000077 (at 0.038 Gyr), against 0.000051 and 0.0000088 for a null change (nearly every opacity, all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$, times $1 + 10^{-10}$, on the same case); central $\log T$ by 0.000096 against 0.0000034, and central $X$ by 0.0000095 against 0.00000036; the track has 277 models in both, and ends at 0.1598 Gyr instead of 0.1596. The effect is 9 to 28 times the null change's, small in size, as expected of a change to the matrix alone. YREC's other spotted cases (`testsuite/Test_m0p1feh+0p0GS98_spot25_ZAMS` and `testsuite/Test_m0p3feh+0p0GS98_spot25_ZAMS`) were not run.

### TPGRAD

The Schwarzschild test and the temperature gradient: radiative, adiabatic (cores, overshoot), or from the mixing-length cubic, with the convective velocity and, on request, the gradient's derivatives.
