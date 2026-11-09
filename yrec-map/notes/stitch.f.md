## Explanation

**Purpose.** `STITCH` writes one model's full profile to the `.store` file, in an alternative format (JvS 08/25): the interior shells, then, if asked, the envelope and atmosphere "stitched" onto them, one line per point with 61 columns. Its comment lists the columns: model, shell, $\log m$ [g], $\log r$ [cm], $L/L_\odot$, $\log P$, $\log T$, $\log\rho$, $\Omega$ [rad/s], three flags for the point's kind, the 15 mass fractions, the opacity, gravity, the three temperature gradients, the convective velocity, $\Gamma_1$, ionisation fractions, $\beta$, $\eta$, the energy rates of each burning chain, neutrino and gravitational energy, $c_P$, $d\ln\rho/d\ln T$, and the rotation columns (51–61).

**How it fits.**
- **Inputs:** the model through the arguments (and the mixing length `CMIXL`, passed on to `ENVINT`), and the per-shell physics left in modules by earlier routines: [[scrtch_mod.f|`SCRTCH_MOD`]] (opacity `SO`, gradients `SDEL`, `SVEL`, ionisation `SFXION`, $\eta$ `SETA`, energy rates `SEG` and `SESUM`, `SCP`; filled by the physics routines such as [[physic.f#PHYSIC|PHYSIC]]), [[sound_mod.f|`SOUND_MOD`]] (`GAM1`), [[pulse1_mod.f|`PULSE1_MOD`]] (`PQDT`), [[roten_mod.f|`ROTEN_MOD`]] (`DEROT`) and [[temp2_mod.f|`TEMP2_MOD`]] (the circulation velocities `VES`, `VGSF`, `VSS`, written by [[vcirc.f#VCIRC|VCIRC]] among others).
- **Who calls it:** [[putstore.f#PUTSTORE|PUTSTORE]], when `LSTCH` is set; PUTSTORE is called by [[wrtout.f#WRTOUT|WRTOUT]] every `NPRTMOD` models and by the main program.
- **What it calls:** [[envint.f#ENVINT|ENVINT]], to integrate the envelope (and atmosphere) again for output.
- **Output:** lines on the unit `ISTOR` ([[iounits_mod.f|`IOUNITS_MOD`]]).
- **Modules:** besides those above, [[envstruct_mod.f|`ENVSTRUCT_MOD`]] and [[atmstruct_mod.f|`ATMSTRUCT_MOD`]] (the envelope's and atmosphere's points, filled by `ENVINT`), [[nmlpar_mod.f|`NMLPAR_MOD`]] (the output steps `ATMSTP`, `ENVSTP`, the integration steps `ATMBEG` … `ENVMAX`, the switches `LSTENV`, `LSTATM`, the spot parameters and `LROT`), [[constants_mod.f|`CONSTANTS_MOD`]], `JSON` from [[dimensions_mod.f|`DIMENSIONS_MOD`]].

**The method.**
1. **Interior** (shells 1 to $M$): the gravity $g = G m / r^2$, and, with rotation, the shape quantities
   $$A = \frac{\Omega^2 r_0^3}{3\,G m}\,\frac{5}{2 + \eta_2},\qquad \frac{R_p}{R_e} = \frac{1 - A}{1 + A/2},$$
   with $r_0$ (`R0`) and $\eta_2$ (`ETA2`) from the rotation routines, and the total circulation velocity `VTOT = VES + VGSF + VSS`. Without rotation the 11 rotation columns are zeros. Column 39 ($\beta$) is read from the envelope's array (bug 2).
2. **Envelope** (`LSTENV`): the integration steps are set to the fixed output steps `ATMSTP`, `ENVSTP` ("dropping a sinkline"; they are not restored, bug 1), and `ENVINT` integrates from the surface, at $\log R = \tfrac12(\log L + \log L_\odot - 4\log T_\mathrm{eff} - \log 4\pi - \log\sigma)$ and $\log g = \log G + \log M - 2\log R$, down to the pressure of the last interior shell; for a spotted star at the ambient temperature (the formula in [[starin.f|starin.f]]). The envelope points get shell numbers $M+1, \dots$; $\Omega$ and the composition are those of the last interior shell; the burning and rotation columns are zero. `LPULPT`, passed to `ENVINT`, is never set (bug 5).

    > **Question** ([[#L167-L173]]). **Spot test.** The spotted-star branch tests `LC(M)` (the last shell convective), while [[starin.f#STARIN|STARIN]] and `CALCAD` test `JENV.EQ.M`. Same intent?

3. **Atmosphere** (`LSTATM`): the atmosphere's points, outermost last, with $r = R_\mathrm{env} + $ `ATMOR`, the total mass and the surface luminosity; $R_\mathrm{env}$ is the envelope's last point, `ENVR(NUMENV)`, or the outer shell's `HR(M)` when no envelope point is stored (`NUMENV` = 0, as for the starting model). The gravity and luminosity columns are not computed for these points (bugs 3 and 4).

    > **Question** ([[#L182]], [[#L215]]). **Two points with one number.** The envelope's points are numbered `M+1` to `M+NUMENV`, outermost last, and the atmosphere's from `NUMATM-I+M+NUMENV` with `I = NUMATM` first, that is `M+NUMENV` again. If the atmosphere's first point is the envelope's last (both at the base of the atmosphere, `RBASE = ENVR(NUMENV)`), the shared number is right and the point is written twice; if not, should the atmosphere start at `M+NUMENV+1`?

    > **Question** ([[#L202-L217]]). **Atmosphere without envelope.** With `LSTATM` but not `LSTENV`, `ENVINT` is not called here, so the atmosphere's points, their numbering, and their base radius come from whatever envelope integration ran last (`NUMENV`, `ENVR(NUMENV)`; `HR(M)` only when `NUMENV` is 0). Should the atmosphere require the envelope?


**Changed since `rp_1`.** COMMON blocks to modules, `IMPLICIT NONE` (the unused `OVRTRN` dropped); a new argument `CMIXL`, passed on to `ENVINT`; the formats of the lines (62, 63) now put a blank between the $\log P$, $\log T$, $\log\rho$ columns and between the six `F9.5` columns ($\Gamma_1$ to $\eta$), so that neighbouring values no longer run together.

**Changed since `a8a5950`.** The atmosphere's base radius is the outer shell's `HR(M)` when `NUMENV` is 0; for the starting model it was read from `ENVR(0)`, which put meaningless radii in the `.store` file. The question on the atmosphere without envelope stays, for a stale `NUMENV` above 0.

## Bugs, by priority

1. **(a)** **The integration steps are not restored.** ([[#L140-L151]]) `STITCH` saves `ATMBEG`, `ATMMIN`, `ATMMAX`, `ENVBEG`, `ENVMIN`, `ENVMAX` into `ABEG0` … `EMAX0` and sets them to the output steps, but never restores them (`ABEG0` … `EMAX0` are never read), so every later envelope integration of the run, those of the surface boundary condition included, starts and steps with the output steps ([[envint.f#L376-L377]]; [[envint.f#L556-L558]]): with the defaults, a fixed step of 0.5 in place of steps between 0.1 and 0.5 ([[nmlpar_mod.f#L92-L98]]; [[nmlpar_mod.f#L223-L224]]). [[wrtmod.f#WRTMOD|WRTMOD]] ([[wrtmod.f#L237-L242]]) and [[getnewenv.f#GETNEWENV|GETNEWENV]] restore the steps they change; [[calcad.f#CALCAD|CALCAD]] does not either. What follows: the models after the first stored one are computed with a coarser envelope integration; how much that changes them was not traced. Only with `LSTCH` (off by default) and `LSTENV`. Read from the code, not run. **A possible fix:**

    ```fortran
          CALL ENVINT(B,FPL,FTL,GL,HSTOT,IXX,LPRT,LSBC0,
         *   PLIM,RL,ATEFFL,X,Z,DUM1,IDUM,KATM,KENV,KSAHA,
         *   DUM2,DUM3,DUM4,LPULPT,CMIXL)
    C 11/09/26 KC via Claude
    C code changed to restore the integration steps saved above, as
    C WRTMOD does.
          ATMBEG = ABEG0
          ATMMIN = AMIN0
          ATMMAX = AMAX0
          ENVBEG = EBEG0
          ENVMIN = EMIN0
          ENVMAX = EMAX0
    ```

2. **(c)** **β of the interior is read from the envelope's array.** ([[#L117-L120]]) Column 39 (BETA) for interior shell `I` is `EBETAS(I)`, the envelope's array at index `I`, while COEFFT stores each shell's β in `SBETA(I)` ([[coefft.f#L442]]), which [[putstore.f#PUTSTORE|PUTSTORE]] writes in its own format ([[putstore.f#L307-L309]]). What follows: a wrong β column for the interior in the stitched `.store` file. Only with `LSTCH`. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to write the interior's BETA, SBETA, in place of the
    C envelope's EBETAS.
                WRITE(ISTOR,63,ADVANCE='no') SO(I),SG,SDEL(1,I),SDEL(2,I),
         *           SDEL(3,I),SVEL(I),GAM1(I),SFXION(1,I),SFXION(2,I),SFXION(3,I),
         *           SBETA(I),SETA(I),(SEG(K,I),K=1,5),SESUM(I),SEG(6,I),SEG(7,I),
         *           SCP(I),PQDT(I)
    ```

3. **(c)** **The atmosphere's gravity is the last point's.** ([[#L212-L223]]) The atmosphere's lines write `SG`, left from the last envelope point (or the last interior shell when no envelope point is written), not computed for each atmosphere point. What follows: a wrong gravity column for the atmosphere in the stitched `.store` file. Only with `LSTCH` and `LSTATM`. Read from the code, not run. **A possible fix:**

    ```fortran
                RAD = DLOG10(DEXP(CLN*RBASE) + ATMOR(I))
    C 11/09/26 KC via Claude
    C code changed to compute the gravity at each atmosphere point.
                SG = DEXP(CLN*(CGL + HSTOT - 2.0D0*RAD))
    ```

4. **(c)** **The atmosphere's luminosity is set only in the envelope branch.** ([[#L153]]; [[#L215]]) The atmosphere's luminosity column writes `B`, which is set (`B = DEXP(CLN*BL)`) only when `LSTENV` is on; with `LSTATM` alone it holds the value of an earlier call (it is `SAVE`d) or, at the first call, is undefined. Only with `LSTCH` and `LSTATM`, and `LSTENV` off. Read from the code, not run. **A possible fix:** move `B = DEXP(CLN*BL)` before `IF(LSTENV)THEN` ([[#L138]]).

5. **(d)** **`LPULPT` is never set.** ([[#L174-L176]]) `LPULPT` is passed to `ENVINT` but never set in `STITCH` (`CALCAD` sets its own to true). With `LPRT` true here, `ENVINT` turns on its pulsation-output path when `LPULPT` is true ([[envint.f#L206-L209]]). It is correct today only if the compiler zero-initializes the `SAVE`d local to `.FALSE.`. Only with `LSTCH` and `LSTENV`. Read from the code, not run. **A possible fix:**

    ```fortran
          LPRT=.TRUE.
    C 11/09/26 KC via Claude
    C code changed to set LPULPT, which was passed to ENVINT unset.
          LPULPT=.FALSE.
    ```

### STITCH

Writes one model's interior, envelope and atmosphere to `ISTOR` in the 61-column `.store` format, integrating the envelope again with `ENVINT` at fixed output steps.
