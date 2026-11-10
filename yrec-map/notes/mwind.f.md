## Explanation

**Purpose.** Removes angular momentum from the surface convection zone by a magnetized stellar wind over one time step. If `LMWIND` is false it hands over to the older wind law in [[wind.f#WIND|WIND]]; otherwise it uses the wind law of Matt et al. (2012), as G. Somers' comments (3/17) call it, with a centrifugal correction from Matt et al. (2012, ApJ 754, L26; MHP 8/17) and optional Rossby scaling.

**How it fits.**
- **Inputs:** $\log L/L_\odot$ (`BL`), the step `DELTS` (s), the wind switch `LJDOT` (no angular momentum is removed when it is false), the masses at the top and bottom of the convection zone (`HSTOP`, `HSBOT`), its shells `JSTART..JEND`, the surface angular velocity `OMEGAS`, the mass in solar units `SMASS` (settled from the code, Nov 9, 2026: $f$ divides by `SMASS` and `CMSUN`, [[#L140]], and [[mdot.f#L262]] updates it in solar masses), $\log T_\mathrm{eff}$ (`TEFFL`), the zone's moment of inertia `HICZ`, and the specific angular momentum `HJM`. Wind parameters (`LMWIND`, `LROSSBY`, `LBSCALE`, `WMAX`, `EXW`, `CONSTFACTOR`, `EXCEN`, `PMMSOLW`, `PMMSOLTAU`) are namelist inputs in [[nmlpar_mod.f|NMLPAR_MOD]], read by [[parmin.f#PARMIN|PARMIN]]; the constant `C_2` is in [[constants_mod.f|CONSTANTS_MOD]] (set in `PARMIN`); the convective turnover times at the start and end of the step and the fraction of the step (`TAUCZ0`, `TAUCZ`, `FRACSTEP`) come from [[ovrtrn_mod.f|OVRTRN_MOD]] (`AMCALC` also reads the photospheric pressures there).
- **Who calls it:** [[getw.f#GETW|GETW]] and [[seculr.f#SECULR|SECULR]].
- **What it calls:** [[wind.f#WIND|WIND]] (old law) or [[amcalc.f#AMCALC|AMCALC]], which returns the structure factor `STRUCTFACTOR` as an output argument.
- **Output:** `HJM` of the convection zone's shells, reduced.
- **Modules:** [[dimensions_mod.f|DIMENSIONS_MOD]] (`JSON`), [[ovrtrn_mod.f|OVRTRN_MOD]], [[nmlpar_mod.f|NMLPAR_MOD]] and [[constants_mod.f|CONSTANTS_MOD]]. `NMLPAR_MOD` holds `WNEW`, the name the routine uses for the new angular velocity, so MWIND overwrites the input `WNEW` (bug 1).

**The method.**
1. **The switch.** With `LJDOT` false, nothing is removed.
2. **Rossby scaling** (`LROSSBY`): the turnover time is interpolated in the step, $\tau = \tau_0 + f\,(\tau_1 - \tau_0)$ (`FRACSTEP`). With `LBSCALE`, the rotation rate used in the saturation term is scaled, $\Omega' = \Omega\,\tau/\tau_\odot$; otherwise the saturation threshold is scaled, $\Omega_\mathrm{sat}' = \Omega_\mathrm{sat}\,\tau_\odot/\tau$. `LBSCALE` acts only with `LROSSBY`.

    > **Question** ([[#L90-L98]]). **$\tau_\mathrm{cz}$ = 0.** With `LROSSBY`, `WSAT = WMAX*PMMSOLTAU/TCZ`, and with `LROSSBY` and `LBSCALE`, `WNOW = OMEGAS*TCZ/PMMSOLTAU`. [[gettau.f#GETTAU|GETTAU]] sets `TAUCZ` = 0 first ([[gettau.f#L79]]), and [[tauintnew.f#TAUINTNEW|TAUINTNEW]] ([[tauintnew.f#L279]]) and [[massloss.f#MASSLOSS|MASSLOSS]] ([[massloss.f#L120]]) set it to 0 when they find no surface convection zone. MWIND's callers call it only with a surface convection zone (`LCZSUR`), but GETTAU and the callers judge the zone differently. Can MWIND be reached with `TAUCZ` and `TAUCZ0` both 0, for example as a surface convection zone appears or vanishes, giving an infinite saturation threshold (a division by zero) or $\Omega' = 0$ (no torque)? Should it guard against it?

3. **The structure factor** from `AMCALC`: $S = (M/M_\odot)^{a_M}\,(R/R_\odot)^{a_R}\,(L/L_\odot)^{a_L}\,(P_\mathrm{phot}/P_{\mathrm{phot},\odot})^{a_P}\,(\tau/\tau_\odot)^{a_\tau}$.
4. **The centrifugal factor,** relative to the Sun, with $f = \Omega^2 R^3/(2GM)$ and $R$ from $L = 4\pi R^2\sigma T_\mathrm{eff}^4$:
$$F_\mathrm{cen} = \left(\frac{c_2^2 + f_\odot}{c_2^2 + f}\right)^{e}\quad(c_2 = \texttt{C\_2},\ e = \texttt{EXCEN}),$$
where $f_\odot = \Omega_\odot^2R_\odot^3/(2GM_\odot)$ with $\Omega_\odot$ = `PMMSOLW`. The constant $c_2$ = 0.0506 (set in PARMIN) and $f$, which is $\tfrac12 f_\mathrm{M}^2$ for Matt et al.'s $f_\mathrm{M} = \Omega R^{3/2}/(GM)^{1/2}$, follow the centrifugal correction of Matt et al. (2012), written in PARMIN's comment as $\{K_2^2/(K_2^2 + 0.5\,\Omega^2R^3/GM)\}$ raised to a power.
5. **The step.** The torque law is $dJ/dt = -K\,S\,\Omega\,\min(\Omega', \Omega_\mathrm{sat})^{a_\Omega-1}F_\mathrm{cen}$: $\propto\Omega^{a_\Omega}$ unsaturated ($a_\Omega$ = 3; the YREC paper, §2.6.4, says of the Kawaler law that "the torque for slow rotators therefore scales as $\Omega^3$"; the spin-down this gives is asked below) and $\propto\Omega$ saturated; with `LBSCALE`, $\propto \Omega\,(\Omega\tau/\tau_\odot)^{a_\Omega-1}$, a dependence on $\mathrm{Ro}^{-1}$. PARMIN sets `EXW` $= 1 + a - 2am + 4mb$ from the law's exponents (`PMMA`, `PMMM`, `PMMB`), which is 3 for both `V13` and `K97` (with $a = 2$, $b = 1$ the terms in $m$ cancel); only `CUS` can give another value. The loop's comment, "THE CONSTANT AND EXPONENTS ARE SET IN PARMIN BASED ON THE INPUT INDEX ALFA" ([[#L158-L159]]), describes the old law: PARMIN uses `ALFA` only when `LMWIND` is off ([[parmin.f#L1024-L1040]]), and sets `EXW` for this law from `PMMA`, `PMMM`, `PMMB` ([[parmin.f#L1092]]) (settled from the code, Nov 9, 2026). The convection zone spins down as
$$\Omega_\mathrm{new} = \Omega_s - \frac{\Delta t}{I_\mathrm{cz}}\;K\,S\;\Omega\;\min(\Omega', \Omega_\mathrm{sat})^{\,a_\Omega - 1}\;F_\mathrm{cen},$$
with $K$ = `CONSTFACTOR`, $a_\Omega$ = `EXW`. If the first guess of the change exceeds $\Omega_s$, the step is split into $\lfloor \Delta\Omega/\Omega_s \rfloor + 1$ substeps, so $\Omega$ stays positive. In each, $\Omega$ in the loss term is iterated as the mean of the start and the previous end value (the mean of the explicit and implicit solutions), until the relative change is below $10^{-6}$ or 20 iterations. The new rate is stored in `WNEW`, which is also a namelist variable (bug 1).

    > **Question** ([[#L164-L200]]). **Silent non-convergence.** After 21 evaluations without convergence ([[#L194-L197]]), the substep continues with the last value, without a warning. Should the routine warn, or cut the substep?

    > **Question** ([[#L142-L143]]; [[#L186-L187]]; [[parmin.f#L1092]]). **The spin-down law.** With $a_\Omega$ = 3, $dJ/dt \propto \Omega^3$ unsaturated; at fixed moment of inertia that integrates to $\Omega \propto t^{-1/2}$, the Skumanich law. Is matching the Skumanich spin-down the reason both presets give `EXW` = 3, and does a changing moment of inertia on the pre-main sequence or the subgiant branch spoil the match?

6. **The loss.** $\Delta j = (\Omega_s - \Omega_\mathrm{new})\,I_\mathrm{cz}/\Delta M_\mathrm{cz}$ is subtracted from every shell of the zone.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) (Angular momentum loss & winds): `LJDOT0` turns on angular-momentum loss and `LMWIND` the wind model of Matt et al. (2012); `AWIND` chooses the law: `V13` (van Saders & Pinsonneault 2013), `K97` (the legacy Krishnamurthi et al. 1997) or `CUS`, custom, which alone reads `PMMA`…`PMMM`. `FK` scales the loss, usually to reproduce the Sun's rotation at its age. `LROSSBY` (default true) scales the loss with the Rossby number, and should go with a saturation threshold: `WMAX` (rad/s), replaced by `WMAX_SUN` $\times\,\Omega_\odot$ when `WMAX_SUN` is below 1000. `PMMSOLTAU` is the Sun's convective overturn time, and `PMMSOLP` $\log P$ at $T_\mathrm{eff}$ in a solar model, for the field's calibration.

**Changed since `rp_1`.** Declarations only, apart from one call: COMMON blocks to modules (`/CWIND/` retired, its namelist members and those of `/PMMWIND/` to `NMLPAR_MOD`, `C_2` to `CONSTANTS_MOD`; `/CONST/`…`/CONST3/` merged into `CONSTANTS_MOD`; `/DEUTER/` and the character `AWIND` dropped), `IMPLICIT NONE`; `AMCALC` now returns `STRUCTFACTOR` as a fourth argument instead of setting it in `/CWIND/`. `/ROT/` is no longer declared, but `WNEW` now comes from `NMLPAR_MOD`, so question 5 (now bug 1) stands.

**Changed since `a8a5950`.** With the Matt et al. law, the routine now returns without removing angular momentum when `LJDOT` is false, as `WIND` does (`SECULR` calls it whatever `LJDOT0` is, so before, a run without the wind still lost angular momentum here); the extra field scaling by `TCZ` in the iteration now acts only with `LROSSBY`, as in the scaling above it (before, `LBSCALE` without `LROSSBY` used `TCZ`, which is set only under `LROSSBY`, and gave no torque), which settles former question 1; former questions 2–7 are now 1–6.

## Bugs, by priority

1. **(never occurred)** **`WNEW` overwrites the namelist's solid-body rate.** ([[#L186]]; [[#L199]]; [[#L208]]) As in [[wind.f#b1]]: The iterated new rate is assigned to `WNEW`, which `USE NMLPAR_MOD` makes the namelist variable `WNEW` ([[nmlpar_mod.f#L129]]), the rate at which [[starin.f#STARIN|STARIN]] starts a model in solid-body rotation when `LWNEW` is set ([[starin.f#L365-L371]]). Every call of MWIND replaces it with the latest surface rate. STARIN is called again for each run in the main program's `DO 200 NK = 1, NUMRUN` loop ([[main.f#L397]]), and applies `WNEW` to a model it reads from file (`LFIRST`, [[starin.f#L255-L263]]), so a later run that reads its model from file with `LWNEW` would start from the wind's last value, not from the input. Only with `LROT`, `LWNEW` (off by default), `LJDOT`, and more than one run (`NUMRUN` > 1).

    **A possible fix:**

    ```diff
    --- a/src/mwind.f
    +++ b/src/mwind.f
    @@ -20,9 +20,12 @@
     C code changed to replace implicit typing with IMPLICIT NONE and
     C explicit declarations.
           IMPLICIT NONE
    +C 11/09/26 KC via Claude
    +C code changed to iterate on the local WNEWL instead of WNEW, which
    +C is the namelist's solid-body rate in NMLPAR_MOD.
           REAL*8 BL,DELTS,DM,DT,DW,DWTEST,FCEN,FCORR,FJDOM,FSUN,HICZ,HJM,
          *       HSBOT,HSTOP,OMEGAS,RL,SMASS,STRUCTFACTOR,TCZ,TEFFL,W,WNEW0,
    -     *       WNOW,WS,WSAT
    +     *       WNEWL,WNOW,WS,WSAT
           INTEGER II,JEND,JSTART,K,N,NSTEP
           LOGICAL*4 LJDOT
     
    @@ -183,20 +186,20 @@
     C NOTE THAT THIS IS IMPLEMENTED HERE RELATIVE TO THE SUN
              FCORR = 0.5*W**2*EXP(CLN*(3.0*RL-CGL))/SMASS/CMSUN
              FCEN = ((C_2**2+FSUN)/(C_2**2+FCORR))**EXCEN
    -         WNEW = WS - (DT/HICZ)*CONSTFACTOR*STRUCTFACTOR*W
    +         WNEWL = WS - (DT/HICZ)*CONSTFACTOR*STRUCTFACTOR*W
          *          *MIN(WNOW,WSAT)**(EXW-1.0D0)*FCEN
     C         WNEW = WS - (DT/HICZ)*CONSTFACTOR*STRUCTFACTOR*W
     C     *          *MIN(W,WSAT)**(EXW-1.0D0)
     C G Somers END
    -         DW = 2.0D0*ABS((WNEW0-WNEW)/(WNEW0+WNEW))
    +         DW = 2.0D0*ABS((WNEW0-WNEWL)/(WNEW0+WNEWL))
     C       WRITE(*,4)WS,W,WNEW,DW,HICZ
     C    4 FORMAT(1X,1P5E14.6)
              IF(DW.GT.1.0D-6)THEN
    -            W = 0.5D0*(WS+WNEW)
    -            WNEW0 = WNEW
    +            W = 0.5D0*(WS+WNEWL)
    +            WNEW0 = WNEWL
                 IF(K.LE.20)GOTO 5
              ENDIF
    -         WS = WNEW
    +         WS = WNEWL
       100 CONTINUE
     C     CON = DELTS*FACTOR*(DMDOT/1.0D-14)**EXMD*OMEGAS**(EXW-1.0D0)
     C    *        *(RTOT/CRSUN)**EXR*SMASS**EXM
    @@ -205,7 +208,7 @@
           DM = HSTOP - HSBOT
     C FIND CHANGE IN ANGULAR MOMENTUM PER UNIT MASS AND SUBTRACT THIS
     C NUMBER FROM THE J/M OF EACH SHELL IN THE SURFACE CONVECTION ZONE.
    -      FJDOM = (OMEGAS-WNEW)*HICZ/DM
    +      FJDOM = (OMEGAS-WNEWL)*HICZ/DM
     C      WRITE(*,11)FJDOM,HJM(JSTART),HJM(JEND)
     C   11 FORMAT(5X,1P3E14.6)
     C     FJDOM=FJDOT/DM
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The overwrite happens at every step with the new law: 360 times in `testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS` and 80 times in `testsuite/Test_solarGS98_difrotmixper18p4d1p0` (`WNEW` from $3.9\times10^{-6}$ to $4.9\times10^{-5}$). No later run used it: The line added where STARIN applies `LWNEW` never saw a changed `WNEW`, since every multi-run case of YREC with `LWNEW` sets `LFIRST` false for its later runs, which then start from the model in memory. The fix was not run. What would reach it: a later run (`LFIRST(k)` true, k > 1) with `LROT`, `LWNEW`, and `LMWIND`. No comment says the shared name is meant.
