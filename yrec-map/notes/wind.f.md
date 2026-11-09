## Explanation

**Purpose.** `WIND` removes angular momentum from the surface convection zone by a magnetized wind, "a Weber–Davis magnetic wind model" (its comment), over one time step. It is the older loss law; [[mwind.f#MWIND|MWIND]] calls it when `LMWIND` is off, and otherwise uses its own law.

**How it fits.**
- **Inputs:** $\log L$ (`BL`), the time step `DELTS` (s), the convection zone's mass range (`HSBOT`, `HSTOP`) and shells (`JSTART`, `JEND`), the switch `LJDOT`, the surface rate `OMEGAS`, the mass `SMASS` (in solar masses, probably), $\log T_\mathrm{eff}$, the zone's moment of inertia `HICZ`. Through modules: the law's constant and exponents (`NMLPAR_MOD`, formerly `COMMON/CWIND/`: `CONSTFACTOR`, `EXMD`, `EXW`, `EXR`, `EXM`, the saturation `WMAX`, set by [[parmin.f#PARMIN|PARMIN]]); the overturn time `TAUCZ` (`OVRTRN_MOD`, from [[gettau.f#GETTAU|GETTAU]]); `LINSTB` (`NMLPAR_MOD`, formerly `COMMON/ROT/`).
- **Who calls it:** only [[mwind.f#MWIND|MWIND]].
- **Output:** `HJM`, each shell's specific angular momentum in the zone, reduced.
- **Modules:** `NMLPAR_MOD`, `OVRTRN_MOD`, `CONSTANTS_MOD`, `DIMENSIONS_MOD`, `IOUNITS_MOD` (for `ISHORT`).

**The method.**
1. **Saturation.** $\Omega_\mathrm{sat}$ = `WMAX`; but with angular momentum transport (`LINSTB`) and `WMAX` > 1, `WMAX` is read as $\Omega_\mathrm{sat}\tau_\mathrm{cz}$ for the Sun, and $\Omega_\mathrm{sat} = $ `WMAX`$/\tau_\mathrm{cz}$ (MHP 3/09); the run stops if $\tau_\mathrm{cz} \le 1$, with exit code 1 and the message also in the `.short` file.

    > **Question** ([[#L64-L80]]). **The saturation's units.** `WMAX > 1` switches the meaning of `WMAX` (rad/s, or rad/s × s). A rate above 1 rad/s is unphysical, so the test works as a switch, but the Physics namelist page describes `WMAX` only in rad/s. Would a separate switch, or a sentence in the documentation, be clearer?

2. **The loss law.** With $R = \sqrt{L/(4\pi\sigma T_\mathrm{eff}^4)}$ and the fixed mass-loss rate $\dot M = 2\times10^{-14}\,M_\odot$/yr,
   $$I\,\frac{d\Omega}{dt} = -K\left(\frac{\dot M}{10^{-14}}\right)^{a}\left(\frac{R}{R_\odot}\right)^{c} M^{d}\;\Omega\,\min(\Omega, \Omega_\mathrm{sat})^{\,b-1},$$
   with $K$ = `CONSTFACTOR`, $a$ = `EXMD`, $b$ = `EXW`, $c$ = `EXR`, $d$ = `EXM`.

    > **Question** ([[#L87]]; [[#L97-L99]]). **A fixed mass-loss rate.** `DMDOT = 2.0D-14` is hard-coded, so the factor $(\dot M/10^{-14})^{a}$ is the constant $2^{a}$, whatever the model's own rate (`DMDT0`). Is this meant, as a part of the calibration through `CONSTFACTOR`?

3. **Integration.** If one explicit step would remove more than $\Omega$, the step is split into `NSTEP` substeps. In each, $\Omega_\mathrm{new}$ is found by iteration: the loss is evaluated at the mean of the start and the previous estimate, until the relative change is below $10^{-6}$ (at most 21 evaluations). The new rate is stored in `WNEW`, which is also a namelist variable (bug 1).

    > **Question** ([[#L117-L134]]). **No convergence check.** After 21 evaluations without convergence, the last estimate is used without a message. Should the routine warn, or cut the substep?

4. **Removal.** $\Delta j = (\Omega_\mathrm{s} - \Omega_\mathrm{new})\,I_\mathrm{cz}/\Delta M_\mathrm{cz}$, with $\Delta M_\mathrm{cz}$ = `HSTOP - HSBOT`, is subtracted from every shell of the zone.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/CWIND/` and `/ROT/` to `NMLPAR_MOD`, `/OVRTRN/` to `OVRTRN_MOD`, the constants to `CONSTANTS_MOD`; the unused `/DEUTER/` dropped), `IMPLICIT NONE`; former question 1 (now bug 1) stands, `WNEW` now being `NMLPAR_MOD`'s.

**Changed since `a8a5950`.** The error stop when $\tau_\mathrm{cz}$ is not defined now also writes its message to the `.short` file (`ISHORT`, through `IOUNITS_MOD`), and ends with `STOP 1` instead of a bare `STOP`, so that a failed run no longer exits with status 0 (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(a)** **`WNEW` overwrites the namelist's solid-body rate.** ([[#L122]]; [[#L133]]; [[#L142]]) The iterated new rate is assigned to `WNEW`, which `USE NMLPAR_MOD` makes the namelist variable `WNEW` ([[nmlpar_mod.f#L129]]): the rate at which [[starin.f#STARIN|STARIN]] starts a model in solid-body rotation when `LWNEW` is set ([[starin.f#L365-L371]]). Each call of WIND therefore replaces the input with the last wind rate. The main program calls STARIN again for each run of its `DO 200 NK = 1, NUMRUN` loop ([[main.f#L397]]), so a later run of the same job with `LWNEW` would start from the previous run's last surface rate, not from the input. Only with `LROT`, `LWNEW` (off by default), the old wind law (`LMWIND` off, the default), and more than one run (`NUMRUN` > 1); [[mwind.f#b1]] is the same for the new law. Read from the code, not run. **A possible fix:** a local name for the iterate, here and in MWIND:

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to iterate on the local WNEWL instead of WNEW, which
    C is the namelist's solid-body rate in NMLPAR_MOD.
          REAL*8 BL,CGRAV,DELTS,DM,DMDOT,DT,DW,DWTEST,FJDOM,HICZ,HJM,HSBOT,
         *       HSTOP,OMEGAS,RL,RTOT,SMASS,TEFFL,W,WNEW0,WNEWL,WS,WSAT
    ...
                WNEWL = WS - (DT/HICZ)*CONSTFACTOR*(DMDOT/1.0D-14)**EXMD
         *             *W*(RTOT/CRSUN)**EXR*SMASS**EXM
         *             *MIN(W,WSAT)**(EXW-1.0D0)
                DW = 2.0D0*ABS((WNEW0-WNEWL)/(WNEW0+WNEWL))
    ...
                IF(DW.GT.1.0D-6)THEN
                   W = 0.5D0*(WS+WNEWL)
                   WNEW0 = WNEWL
                   IF(K.LE.20)GOTO 5
                ENDIF
                WS = WNEWL
    ...
             FJDOM = (OMEGAS-WNEWL)*HICZ/DM
    ```

### WIND

The older wind braking law: $I\,d\Omega/dt \propto \Omega\,\min(\Omega,\Omega_\mathrm{sat})^{b-1}$ with fixed exponents, integrated over the step and taken from the surface convection zone's specific angular momentum.
