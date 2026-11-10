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

    The spotted-star branch tests `LC(M)` (the last shell convective), as the surface boundary condition does; [[starin.f#STARIN|STARIN]], `CALCAD`, and `WRTMOD` test `JENV.EQ.M`, the opposite case ([[#b6]]).

3. **Atmosphere** (`LSTATM`): the atmosphere's points, outermost last, with $r = R_\mathrm{env} + $ `ATMOR`, the total mass and the surface luminosity; $R_\mathrm{env}$ is the envelope's last point, `ENVR(NUMENV)`, or the outer shell's `HR(M)` when no envelope point is stored (`NUMENV` = 0, as for the starting model). The gravity and luminosity columns are not computed for these points (bugs 3 and 4).

    > **Question** ([[#L182]], [[#L215]]). **Two points with one number.** The envelope's points are numbered `M+1` to `M+NUMENV`, outermost last, and the atmosphere's from `NUMATM-I+M+NUMENV` with `I = NUMATM` first, that is `M+NUMENV` again. If the atmosphere's first point is the envelope's last (both at the base of the atmosphere, `RBASE = ENVR(NUMENV)`), the shared number is right and the point is written twice; if not, should the atmosphere start at `M+NUMENV+1`? Comparing $P$ and $T$ of the two rows with the shared number in a stitched `.store` file (`LSTCH`, `LSTENV`, and `LSTATM`) would settle it.

    > **Question** ([[#L202-L217]]). **Atmosphere without envelope.** With `LSTATM` but not `LSTENV`, `ENVINT` is not called here, so the atmosphere's points, their numbering, and their base radius come from whatever envelope integration ran last (`NUMENV`, `ENVR(NUMENV)`; `HR(M)` only when `NUMENV` is 0). Should the atmosphere require the envelope?


**Changed since `rp_1`.** COMMON blocks to modules, `IMPLICIT NONE` (the unused `OVRTRN` dropped); a new argument `CMIXL`, passed on to `ENVINT`; the formats of the lines (62, 63) now put a blank between the $\log P$, $\log T$, $\log\rho$ columns and between the six `F9.5` columns ($\Gamma_1$ to $\eta$), so that neighbouring values no longer run together.

**Changed since `a8a5950`.** The atmosphere's base radius is the outer shell's `HR(M)` when `NUMENV` is 0; for the starting model it was read from `ENVR(0)`, which put meaningless radii in the `.store` file. The question on the atmosphere without envelope stays, for a stale `NUMENV` above 0.

## Bugs, by priority

1. **(changes results, small)** **Checked by KC** (Nov 10, 2026). **The integration steps are not restored.** ([[#L140-L151]]) `STITCH` saves `ATMBEG`, `ATMMIN`, `ATMMAX`, `ENVBEG`, `ENVMIN`, `ENVMAX` into `ABEG0` … `EMAX0` and sets them to the output steps, but never restores them (`ABEG0` … `EMAX0` are never read), so every later envelope integration of the run, those of the surface boundary condition included, starts and steps with the output steps ([[envint.f#L376-L377]]; [[envint.f#L556-L558]]): with the defaults, a fixed step of 0.5 in place of steps between 0.1 and 0.5 ([[nmlpar_mod.f#L92-L98]]; [[nmlpar_mod.f#L223-L224]]); in YREC's cases, which set `ATMSTP` = `ENVSTP` = 0.05, a fixed 0.05 in place of steps up to 0.25. [[wrtmod.f#WRTMOD|WRTMOD]] ([[wrtmod.f#L237-L242]]) and [[getnewenv.f#GETNEWENV|GETNEWENV]] restore the steps they change; [[calcad.f#CALCAD|CALCAD]] does not either. What follows: the models after the first stored one are computed with other integration steps (coarser with the defaults, finer in YREC's cases). Only with `LSTCH` (off by default) and `LSTENV`.

    **A possible fix:**

    ```diff
    --- a/src/stitch.f
    +++ b/src/stitch.f
    @@ -174,6 +174,15 @@
           CALL ENVINT(B,FPL,FTL,GL,HSTOT,IXX,LPRT,LSBC0,
          *   PLIM,RL,ATEFFL,X,Z,DUM1,IDUM,KATM,KENV,KSAHA,
          *   DUM2,DUM3,DUM4,LPULPT,CMIXL)
    +C 11/09/26 KC via Claude
    +C code changed to restore the integration steps saved above, as
    +C WRTMOD does.
    +      ATMBEG = ABEG0
    +      ATMMIN = AMIN0
    +      ATMMAX = AMAX0
    +      ENVBEG = EBEG0
    +      ENVMIN = EMIN0
    +      ENVMAX = EMAX0
     
     C DEFINE SOME ARRAYS WE NEED
           DO I=1,NUMENV
    ```

    **How the code itself shows it.** STITCH's twelve lines that save and set the steps ([[#L140-L151]]) are WRTMOD's ([[wrtmod.f#L192-L203]]), where a comment states their purpose, "`SAVE THE INTEGRATION STEP PARAMETERS AND ENFORCE THE SPACING REQUESTED FOR PRINTOUT PURPOSES.`" ([[wrtmod.f#L190-L191]]), and after its call to ENVINT, WRTMOD puts all six back ([[wrtmod.f#L237-L242]]). STARIN does the same around its own envelope integration: It saves `ENVMAX`, `ENVMIN`, and `ENVBEG` into `EMAX0`, `EMIN0`, and `EBEG0` ([[starin.f#L688-L690]]) and restores them after ENVINT ([[starin.f#L732-L734]]). In STITCH, `ABEG0` … `EMAX0` are local variables that appear only in the declaration ([[#L41-L42]]) and the saves ([[#L140-L145]]), so the values saved are never used. The fix adds WRTMOD's six restoring lines after the call.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): STITCH integrated an envelope in 17 of 34 runs (13 of YREC's cases, from 0.1 to 4 $M_\odot$, and 4 made-up ones), at the stored models, one to three times a run (nine in a made-up run: YREC's 3 $M_\odot$ case `testsuite/Test_m3p0feh+0p0GS98_std25_TAMS` with Reimers mass loss on). At its first call in each run (models 7 to 41) it replaced the cases' own steps (`ATMMAX` = 0.25) with the output step 0.05, and every later integration of the run kept that fixed step. Rerun with the steps restored (the fix above), `testsuite/Test_m0p1feh+0p0GS98_spot25_ZAMS` moves $\log L$ by up to $5.8\times10^{-5}$ dex, against $9.4\times10^{-9}$ for a null change (nearly every opacity, all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$, times $1 + 10^{-10}$), and its last model (939 in both runs) is at 16.677 Gyr instead of 16.714; `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` moves $\log L$ by up to $3.4\times10^{-5}$ dex, against $1\times10^{-9}$. The effect is real, thousands of times the noise, but small; the test suite's 2% test fails on the `.track`, `.short`, and `.store` files of both. The effect is real, and with the default steps (a fixed 0.5 in place of 0.1 to 0.5) it may be larger, which was not run. Intent: none found; [[wrtmod.f#WRTMOD|WRTMOD]] saves and restores the same steps ([[wrtmod.f#L190-L242]]).

2. **(wrong output)** **Checked by KC** (Nov 10, 2026). **β of the interior is read from the envelope's array.** ([[#L117-L120]]) Column 39 (BETA) for interior shell `I` is `EBETAS(I)`, the envelope's array at index `I`, while COEFFT stores each shell's β in `SBETA(I)` ([[coefft.f#L442]]), which [[putstore.f#PUTSTORE|PUTSTORE]] writes in its own format ([[putstore.f#L307-L309]]). What follows: a wrong β column for the interior in the stitched `.store` file. Only with `LSTCH`.

    **A possible fix:**

    ```diff
    --- a/src/stitch.f
    +++ b/src/stitch.f
    @@ -114,9 +114,12 @@
                 WRITE(ISTOR,62,ADVANCE='no') MODEL,I,HS(I),HR(I),HL(I),HP(I),
          *         HT(I),HD(I),OMEGA(I),LC(I),.TRUE.,.FALSE.,.FALSE.,(HCOMP(J,I),J=1,15)
     C write out additional physics if desired
    +C 11/09/26 KC via Claude
    +C code changed to write the interior's BETA, SBETA, in place of the
    +C envelope's EBETAS.
                 WRITE(ISTOR,63,ADVANCE='no') SO(I),SG,SDEL(1,I),SDEL(2,I),
          *           SDEL(3,I),SVEL(I),GAM1(I),SFXION(1,I),SFXION(2,I),SFXION(3,I),
    -     *           EBETAS(I),SETA(I),(SEG(K,I),K=1,5),SESUM(I),SEG(6,I),SEG(7,I),
    +     *           SBETA(I),SETA(I),(SEG(K,I),K=1,5),SESUM(I),SEG(6,I),SEG(7,I),
          *           SCP(I),PQDT(I)
     C write out additional rotation info if rotation is on
                 IF(LROT)THEN
    ```

    **How the outputs show it.** In `testsuite/Test_solarGS98_dif`, at model 1208 (the last), the `.store` file's column 39 for interior shells 1 to 76 repeats, value for value, column 39 of envelope lines 798 to 873 (0.99999 at shell 1 and at line 798), since both come from `EBETAS` ([[#L117-L120]]; [[#L189-L192]]), and it is 0.00000 on 718 of the 797 interior shells, the surface included. The `.track` gives the center's β for the same model, Beta_cen, as 9.99356686E-001 ([[wrtout.f#L558]]), where the `.store` file writes 0.99999 for shell 1.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The interior's lines were written in 17 runs, and on almost every shell (all 2,285 in `testsuite/Test_solarGS98_dif`) the written β, `EBETAS(I)`, differed from the shell's own `SBETA(I)`: The column held values from 0 to 1 where the interior's β was 0.960 to 1. With the fix, the tracks of `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` and `testsuite/Test_solarM22M_difkur` are identical, and only their `.store` files change (beyond 2%), as expected for an output column. Intent: none found; the comment at [[#L104]] names column 39 BETA.

3. **(wrong output)** **Checked by KC** (Nov 10, 2026). **The atmosphere's gravity is the last point's.** ([[#L212-L223]]) The atmosphere's lines write `SG`, left from the last envelope point (or the last interior shell when no envelope point is written), not computed for each atmosphere point. What follows: a wrong gravity column for the atmosphere in the stitched `.store` file. Only with `LSTCH` and `LSTATM`.

    **A possible fix:**

    ```diff
    --- a/src/stitch.f
    +++ b/src/stitch.f
    @@ -212,6 +212,9 @@
                 DO I=NUMATM,1,-1
     C write out the basic info. Omega and abundances take value of last interior point.
                 RAD = DLOG10(DEXP(CLN*RBASE) + ATMOR(I))
    +C 11/09/26 KC via Claude
    +C code changed to compute the gravity at each atmosphere point.
    +            SG = DEXP(CLN*(CGL + HSTOT - 2.0D0*RAD))
                 WRITE(ISTOR,62,ADVANCE='no') MODEL,NUMATM-I+M+NUMENV,HSTOT,RAD,B,
          *      ATMOP(I),ATMOT(I),ATMOD(I),OMEGA(M),
          *      .FALSE.,.FALSE.,.FALSE.,.TRUE.,(HCOMP(J,M),J=1,15)
    ```

    **How the outputs show it.** In `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS`, at model 7, all 113 atmosphere lines of the `.store` file write the same gravity in column 30, 5.950E+02 cm s⁻², the last envelope point's ([[#L183]]; [[#L219-L223]]), from the atmosphere's base to its top. The lines' own radii (column 4) cannot give each point's true gravity: Each is the base radius plus that point's own step in depth, `ATMOR(I)`, not its height above the base ([[#L214]]; [[envint.f#L442]]; [[envint.f#L467]]), and the outermost line's step is the stale first step of [[envint.f#b3]].

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The atmosphere's lines were written in 13 runs (none in the four with table atmospheres, for which STITCH gives no atmosphere, [[#L92-L93]]). The written gravity was off by more than 0.001 dex in only four of them, one to four times each: `examples/class_exercises/exercise_4/Grid_m4p0feh+0p0GS98_std25_TAMS`, `testsuite/Test_m0p1feh+0p0GS98_spot25_ZAMS`, `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS`, and the made-up Reimers run of [[#b1]] (YREC's 3 $M_\odot$ case `testsuite/Test_m3p0feh+0p0GS98_std25_TAMS` with Reimers mass loss on). These departures are measured at the radius written, the base plus one step (above), and for the outermost line they include the stale first step of [[envint.f#b3]]. With the fix, the tracks of the spotted 0.1 $M_\odot$ and the 0.3 $M_\odot$ cases are identical, and their `.store` files stay within 2%. The error grows with the atmosphere's depth relative to the radius (an inference, not measured), so it may matter more for extended atmospheres, such as giants or the Reimers run, which were not run with the fix. Intent: none found.

4. **(never occurred)** **The atmosphere's luminosity is set only in the envelope branch.** ([[#L153]]; [[#L215]]) The atmosphere's luminosity column writes `B`, which is set (`B = DEXP(CLN*BL)`) only when `LSTENV` is on; with `LSTATM` alone it holds the value of an earlier call (it is `SAVE`d) or, at the first call, is undefined. Only with `LSTCH` and `LSTATM`, and `LSTENV` off.

    **A possible fix:** move `B = DEXP(CLN*BL)` before `IF(LSTENV)THEN` ([[#L138]]).

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): not reached. The atmosphere's lines were written in 13 runs ($\log L$ = −2.96 to 2.67), all with `LSTENV` on, so `B` was always set: Every one of YREC's cases that sets `LSTCH` sets `LSTENV` too, and a made-up run with `LSTCH` off (YREC's `testsuite/Test_m1p0feh+0p0GS98_base_TAMS`, with the default) does not call STITCH. Not run: `LSTCH` and `LSTATM` on with `LSTENV` off, which the documentation offers as separate switches (`docs/source/namelist_control.md`, lines 129–130). Intent: none found.

5. **(never occurred)** **`LPULPT` is never set.** ([[#L174-L176]]) `LPULPT` is passed to `ENVINT` but never set in `STITCH` (`CALCAD` sets its own to true). With `LPRT` true here, `ENVINT` turns on its pulsation-output path when `LPULPT` is true ([[envint.f#L206-L209]]). It is correct today only if the compiler zero-initializes the `SAVE`d local to `.FALSE.`. Only with `LSTCH` and `LSTENV`.

    **A possible fix:**

    ```diff
    --- a/src/stitch.f
    +++ b/src/stitch.f
    @@ -158,6 +158,9 @@
           KSAHA = 0
           IXX=0
           LPRT=.TRUE.
    +C 11/09/26 KC via Claude
    +C code changed to set LPULPT, which was passed to ENVINT unset.
    +      LPULPT=.FALSE.
           LSBC0 = .FALSE.
           X = HCOMP(1,M)
           Z = HCOMP(3,M)
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): `ENVINT` was called from here in 17 runs, one to nine times each, and `LPULPT` was false every time, as gfortran's zero-filled storage gives, so the results are right today. Intent: none found.

6. **(not reached)** **Three routines apply the spots only without a surface convection zone.** ([[#L167-L173]]; [[starin.f#L723]]; [[calcad.f#L228]]; [[wrtmod.f#L228]]) For a spotted star the envelope is integrated from the ambient temperature of the unspotted surface. STITCH ([[#L169]]), [[surfbc.f#SURFBC|SURFBC]] ([[surfbc.f#L218]]), [[gettau.f#GETTAU|GETTAU]] ([[gettau.f#L125]]), and [[getnewenv.f#GETNEWENV|GETNEWENV]] ([[getnewenv.f#L138]]) do so when the outer shell is convective (`LC(M)`), but [[starin.f#STARIN|STARIN]], [[calcad.f#CALCAD|CALCAD]], and [[wrtmod.f#WRTMOD|WRTMOD]] when `JENV.EQ.M`, which [[findsh.f#FINDSH|FINDSH]] ([[findsh.f#L113-L120]]) and [[convec.f#CONVEC|CONVEC]] ([[convec.f#L145-L150]]) set when there is no surface convection zone (FINDSH also for one of a single shell): the opposite case. What follows: For a spotted star with a convective envelope, STARIN's envelope for a shallower fitting point (with `LSENV0`) and WRTMOD's printed envelope start from $T_\mathrm{eff}$ instead of the ambient temperature, while a star with no surface convection zone gets the spot correction there and nowhere else. CALCAD never runs today (`LACOUT` is false and set nowhere). WRTMOD and CALCAD have no `LC` argument, so the fix tests `JENV.LT.M` there, which differs from `LC(M)` only for a one-shell zone. Only with spots (`SPOTF` ≠ 0 and `SPOTX` ≠ 1; the defaults are 0 and 1).

    **A possible fix:**

    ```diff
    --- a/src/starin.f
    +++ b/src/starin.f
    @@ -720,7 +720,10 @@
                 IDUM = 0
     C G Somers 10/14, FOR SPOTTED RUNS, FIND THE
     C PRESSURE AT THE AMBIENT TEMPERATURE ATEFFL
    -          IF(JENV.EQ.M.AND.SPOTF.NE.0.0.AND.SPOTX.NE.1.0)THEN
    +C 11/10/26 KC via Claude
    +C code changed to apply the spots when the surface is convective, as
    +C SURFBC, GETTAU, GETNEWENV and STITCH do, not only when it is not.
    +          IF(LC(M).AND.SPOTF.NE.0.0.AND.SPOTX.NE.1.0)THEN
                    ATEFFL = TEFFL - 0.25*LOG10(SPOTF * SPOTX**4.0 + 1.0 - SPOTF)
               ELSE
                  ATEFFL = TEFFL
    --- a/src/calcad.f
    +++ b/src/calcad.f
    @@ -225,7 +225,10 @@
     c      IF (KTTAU .EQ. 3) LAOLY = .FALSE.      ! for grey atm intergration: stores values in common block
     C      G Somers 10/14, FOR SPOTTED RUNS, FIND THE PRESSURE AT
     C      THE AMBIENT TEMPERATURE ATEFFL
    -      IF(JENV.EQ.M.AND.SPOTF.NE.0.0.AND.SPOTX.NE.1.0)THEN
    +C 11/10/26 KC via Claude
    +C code changed to apply the spots when there is a surface convection
    +C zone (JENV < M), as SURFBC, GETTAU, GETNEWENV and STITCH do.
    +      IF(JENV.LT.M.AND.SPOTF.NE.0.0.AND.SPOTX.NE.1.0)THEN
                 ATEFFL = TEFFL - 0.25*LOG10(SPOTF * SPOTX**4.0 + 1.0 - SPOTF)
           ELSE
                 ATEFFL = TEFFL
    --- a/src/wrtmod.f
    +++ b/src/wrtmod.f
    @@ -225,7 +225,10 @@
              IDUM = 0
     C G Somers 10/14, FOR SPOTTED RUNS, FIND THE
     C PRESSURE AT THE AMBIENT TEMPERATURE ATEFFL
    -        IF(JENV.EQ.M.AND.SPOTF.NE.0.0.AND.SPOTX.NE.1.0)THEN
    +C 11/10/26 KC via Claude
    +C code changed to apply the spots when there is a surface convection
    +C zone (JENV < M), as SURFBC, GETTAU, GETNEWENV and STITCH do.
    +        IF(JENV.LT.M.AND.SPOTF.NE.0.0.AND.SPOTX.NE.1.0)THEN
                 ATEFFL = TEFFL - 0.25*LOG10(SPOTF * SPOTX**4.0 + 1.0 - SPOTF)
            ELSE
               ATEFFL = TEFFL
    ```

    **Checked by running YREC** (Nov 10, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): In `testsuite/Test_m1p0feh+0p0GS98_spot25_ZAMS` (1 $M_\odot$, `SPOTF` = 0.25, `SPOTX` = 0.85, a convective envelope), none of the three tests was reached: STARIN tests the spots only in the branch that moves the fitting point outward ([[starin.f#L685]]), and the starting model needed no move, and PUTSTORE calls WRTMOD only without `LSTCH` ([[putstore.f#L184]]; [[putstore.f#L342-L349]]), which this case sets. With the fix the outputs are identical. YREC's other spotted cases (`testsuite/Test_m0p1feh+0p0GS98_spot25_ZAMS` and `testsuite/Test_m0p3feh+0p0GS98_spot25_ZAMS`) set `LSTCH` too and were not run. What would reach it: a spotted run with `LSENV0` and a fitting point shallower than the starting model's (STARIN, the results), or with `LSTATM` or `LSTENV` and `LSTCH` off (WRTMOD, output only).

### STITCH

Writes one model's interior, envelope and atmosphere to `ISTOR` in the 61-column `.store` format, integrating the envelope again with `ENVINT` at fixed output steps.
