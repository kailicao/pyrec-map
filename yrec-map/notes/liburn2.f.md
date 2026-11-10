## Explanation

**Purpose.** `LIBURN2` is a cheaper version of [[liburn.f#LIBURN|`LIBURN`]]: it burns ⁶Li, ⁷Li and ⁹Be over a step in one go, with the rate taken at the geometric mean of its start and end values, without substeps, extrapolation or accretion. Its banner comment still says "LIBURN" ([[#L4]]).

**How it fits.** Called by [[getw.f#GETW|`GETW`]] (rotating models, as an alternative to `LIBURN`) and [[bursmix.f#BURSMIX|`BURSMIX`]]. Same arguments (`DELTS` in seconds, as for `LIBURN`, whose comments' "in years" are stale: [[liburn.f#LIBURN|LIBURN]]), and the same modules as `LIBURN` without `DEUTER_MOD` and `IOUNITS_MOD` (it neither accretes nor writes): `NEWRAT_MOD`, `OLDRAT_MOD` (rates from [[lirate88.f#LIRATE88|`LIRATE88`]]), `SCRTCH_MOD`, `MDPHY_MOD`, `OLDMOD_MOD`, `LIOV_MOD`, `PREVCZ_MOD`, `NMLPAR_MOD` (`LOVSTE`, `LROT`, `LINSTB`), `CONSTANTS_MOD`, `DIMENSIONS_MOD`. No calls.

**The method.** The base of the convection zone is found as in `LIBURN`. Then, in each radiative point below both bases (skipping points where the ⁹Be rate, at the start or the end, is at most $10^{-32}$; destroying everything above $\log T = 7$), and in the convection zone as a whole,

$$x \leftarrow x\,\exp\!\left(-\Delta t\,\sqrt{\lambda_0\lambda_1}\right),$$

with $\lambda_0$, $\lambda_1$ the rates (mass-weighted means in the zone) at the start and end of the step; set to 0 when the exponent is 30 or more, or the result below $10^{-24}$. The zone's start rate is always computed from the start-of-step rates `RLI60`…, never taken from `LIBURN`'s stored end rates, and `LIBURN2` stores no end rates: It clears `PREVCZ_MOD`'s flag `LBLIOLD`, so that `LIBURN` does not reuse a rate after it (the code's comment: `BURSMIX` restarts each extrapolation sequence from the start-of-step model and does not advance `RLI60`). Points left by a retreating zone get the weighted rate of `LIBURN`'s step 4. A point whose ⁹Be rate is at most $10^{-32}$ is skipped in the radiative loop ([[#L158]]) but ends the last loop and the routine ([[#L334]]), as in both of `LIBURN`'s loops; which is meant is [[liburn.f#q1|LIBURN's question 1]].

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (the namelist members of `/DPMIX/` and `/ROT/` to `NMLPAR_MOD`, `/CONST1/` to `CONSTANTS_MOD`; the unused `/LUOUT/` dropped), `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

**Changed since `a8a5950`.** The start rate is always computed, and the end rates are no longer stored in `PREVCZ_MOD`; the routine clears the new flag `LBLIOLD` instead. (Before, the test `BLI6OLD.LE.0` was always true, so the start rate was always computed too.)

## Bugs, by priority

1. **(cannot be reached)** **The sign of `FRAD`.** ([[#L319-L339]]) The same lines as `LIBURN`'s ([[liburn.f#b1]]): `DMASS = HSBEG - HSEND` is negative when the zone retreats, so `FRAD` lies between −1 and 0 and the blended rate extrapolates beyond the zone's rate; and the weights are the other way round from the comment's "a point 1/3 from the old to the new CZ base in mass spent 1/3 of the time in the CZ." Only with `LEXCOM` (off by default), for rotating models through `GETW` and `BURSMIX`, on steps where the zone retreats.

    **A possible fix:** as for `LIBURN`,

    ```diff
    --- a/src/liburn2.f
    +++ b/src/liburn2.f
    @@ -327,16 +327,20 @@
              HSBEG = 0.0D0
           ENDIF
           HSEND = 0.5D0*(HS1(JENV)+HS1(JENV-1))
    -      DMASS = HSBEG - HSEND
    +C 11/09/26 KC via Claude
    +C code changed to make FRAD the fraction of the step spent in the CZ,
    +C between 0 at the old base and 1 at the new one, as the comment above
    +C says, and to give it the weight of the convective rate.
    +      DMASS = HSEND - HSBEG
           DO I = JENV0,JENV-1
     C MHP 9/91 CHANGE TO AVOID DIVISION BY ZERO.
     C SKIP IF SHELL TEMPERATURE DROPS BELOW BURNING THRESHOLD.
              IF(RBE9(I).LE.1.0D-32)GOTO 200
              FRAD = (HS1(I)-HSBEG)/DMASS
    -C USE FRAD*RADIATIVE RATE AND (1-FRAD)*CONVECTIVE RATE.
    -         DLI6 = DELTS*EXP(FRAD*LOG(RLI6(I))+(1.0D0-FRAD)*BLI60)
    -         DLI7 = DELTS*EXP(FRAD*LOG(RLI7(I))+(1.0D0-FRAD)*BLI70)
    -         DBE9 = DELTS*EXP(FRAD*LOG(RBE9(I))+(1.0D0-FRAD)*BBE90)
    +C USE FRAD*CONVECTIVE RATE AND (1-FRAD)*RADIATIVE RATE.
    +         DLI6 = DELTS*EXP((1.0D0-FRAD)*LOG(RLI6(I))+FRAD*BLI60)
    +         DLI7 = DELTS*EXP((1.0D0-FRAD)*LOG(RLI7(I))+FRAD*BLI70)
    +         DBE9 = DELTS*EXP((1.0D0-FRAD)*LOG(RBE9(I))+FRAD*BBE90)
     C***REMEMBER TO ADD FAILSAFES FOR LARGE DEPLETION***
              HCOMP(13,I) = HCOMP(13,I)/EXP(DLI6)
              IF(HCOMP(13,I).LT.1.0D-24)HCOMP(13,I)=0.0D0
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in any of the 34 runs, and cannot be reached at 7be4133: LIBURN2 is called only from GETW and from BURSMIX, both only when `LBURS` is true ([[getw.f#L403-L418]]; [[getw.f#L456-L460]]), and GETW sets `LBURS = .FALSE.` on every call ([[getw.f#L140]]), which no namelist setting changes. It is code that cannot run today; with `LBURS` switched on, the sign would matter as in LIBURN ([[liburn.f#b1]]).

2. **(cannot be reached)** **Points newly in a deepened zone are not burned.** ([[#L155-L157]]; [[#L274-L278]]; [[#L308-L312]]) As in `LIBURN` ([[liburn.f#b2]]): When the zone deepens, its starting abundance includes the points `JENV` to `JENV0`−1, but the result is written only from `MAXJ` = `JENV0` outward, and the radiative loop stops below `JENV`, so those points are not burned over the step. Only with `LEXCOM`, on steps where the zone deepens.

    **A possible fix:**

    ```diff
    --- a/src/liburn2.f
    +++ b/src/liburn2.f
    @@ -305,7 +305,10 @@
                 FBE9 = 0.0D0
              ENDIF
              IF(FBE9.LT.1.0D-24)FBE9 = 0.0D0
    -      DO I = MAXJ,M
    +C 11/09/26 KC via Claude
    +C code changed to give the burned abundances to the whole zone at the
    +C end of the step, including points that joined it as it deepened.
    +      DO I = JENV,M
              HCOMP(13,I) = FLI6
              HCOMP(14,I) = FLI7
              HCOMP(15,I) = FBE9
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in any of the 34 runs, and cannot be reached at 7be4133: LIBURN2 is called only from GETW and from BURSMIX, both only when `LBURS` is true ([[getw.f#L403-L418]]; [[getw.f#L456-L460]]), and GETW sets `LBURS = .FALSE.` on every call ([[getw.f#L140]]), which no namelist setting changes.

3. **(cannot be reached)** **The overshoot zone's width mixes two models.** ([[#L135-L142]]) With envelope overshoot, the offset `FX` of the new base is measured in a zone width `DR = EXP(CLN*HRO(J+1)) - R`, the start-of-step radius of the outer point minus the end-of-step radius of the inner one. `LIBURN` takes both from the end-of-step model since `a8a5950` ([[liburn.f#L172-L175]]). A wrong `FX` changes the mass and rates given to the bottom point of the zone. Only with `LOVSTE` (off by default) and `LEXCOM`.

    **A possible fix:**

    ```diff
    --- a/src/liburn2.f
    +++ b/src/liburn2.f
    @@ -136,7 +136,10 @@
                    R = EXP(CLN*HR(J))
                    IF(R.LT.ROS)THEN
                       JENV = J + 1
    -                  DR = EXP(CLN*HRO(J+1))-R
    +C 11/09/26 KC via Claude
    +C code changed to take the zone width from the end-of-step model alone,
    +C as in LIBURN.
    +                  DR = EXP(CLN*HR(J+1))-R
                       FX = 0.5D0-((ROS-R)/DR)
                       FX = MAX(-0.5D0,FX)
                       FX = MIN(0.5D0,FX)
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in any of the 34 runs, and cannot be reached at 7be4133: LIBURN2 is called only from GETW and from BURSMIX, both only when `LBURS` is true ([[getw.f#L403-L418]]; [[getw.f#L456-L460]]), and GETW sets `LBURS = .FALSE.` on every call ([[getw.f#L140]]), which no namelist setting changes. It would also need `LOVSTE`.

4. **(cannot be reached)** **`HRO(0)` read for a fully convective start.** ([[#L113-L115]]) With envelope overshoot, the starting base radius reads `HRO(JNENV0-1)`, which is `HRO(0)`, outside the array, when the start-of-step model is fully convective (`JNENV0` = 1). The development build's `-fcheck=all` (`src/Makefile` line 61) stops the run there; otherwise the radius is computed from whatever lies before `HRO` in memory. `LIBURN` guards this case ([[liburn.f#L139-L148]]). Only with `LOVSTE` (off by default) and `LEXCOM`, for a fully convective start.

    **A possible fix:**

    ```diff
    --- a/src/liburn2.f
    +++ b/src/liburn2.f
    @@ -111,8 +111,15 @@
              ELSE
     C STARTING CZ DEPTH
                 IF(RBASE0.EQ.0.0D0)THEN
    +C 11/09/26 KC via Claude
    +C code changed to take the radius below shell 1 as zero (the centre),
    +C as in LIBURN.
    +            IF(JNENV0.GT.1)THEN
                    RBASE0 = 0.5D0*(EXP(CLN*HRO(JNENV0))
          *                  +EXP(CLN*HRO(JNENV0-1)))
    +            ELSE
    +               RBASE0 = 0.5D0*EXP(CLN*HRO(1))
    +            ENDIF
                    ROS = RBASE0 - PSCAL0
                    DO J = JNENV0-1,1,-1
                       R = EXP(CLN*HRO(J))
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in any of the 34 runs, and cannot be reached at 7be4133: LIBURN2 is called only from GETW and from BURSMIX, both only when `LBURS` is true ([[getw.f#L403-L418]]; [[getw.f#L456-L460]]), and GETW sets `LBURS = .FALSE.` on every call ([[getw.f#L140]]), which no namelist setting changes. It would also need `LOVSTE` and a fully convective start.

5. **(cannot be reached)** **No overflow guard in the last loop.** ([[#L340-L346]]) The last loop divides by `EXP(DLI6)`, `EXP(DLI7)`, `EXP(DBE9)` without the cut at 30 of the other loops or `LIBURN`'s `SAFEDIVEXP`. For an exponent above 709.78 the default build gives 0, the intended result, and the development build (`-ffpe-trap=overflow`) stops the run.

    **A possible fix:**

    ```diff
    --- a/src/liburn2.f
    +++ b/src/liburn2.f
    @@ -338,11 +338,13 @@
              DLI7 = DELTS*EXP(FRAD*LOG(RLI7(I))+(1.0D0-FRAD)*BLI70)
              DBE9 = DELTS*EXP(FRAD*LOG(RBE9(I))+(1.0D0-FRAD)*BBE90)
     C***REMEMBER TO ADD FAILSAFES FOR LARGE DEPLETION***
    -         HCOMP(13,I) = HCOMP(13,I)/EXP(DLI6)
    +C 11/09/26 KC via Claude
    +C code changed to guard the division against overflow, as in LIBURN.
    +         CALL SAFEDIVEXP(HCOMP(13,I),DLI6)
              IF(HCOMP(13,I).LT.1.0D-24)HCOMP(13,I)=0.0D0
    -         HCOMP(14,I) = HCOMP(14,I)/EXP(DLI7)
    +         CALL SAFEDIVEXP(HCOMP(14,I),DLI7)
              IF(HCOMP(14,I).LT.1.0D-24)HCOMP(14,I)=0.0D0
    -         HCOMP(15,I) = HCOMP(15,I)/EXP(DBE9)
    +         CALL SAFEDIVEXP(HCOMP(15,I),DBE9)
              IF(HCOMP(15,I).LT.1.0D-24)HCOMP(15,I)=0.0D0
           END DO
      200  CONTINUE
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in any of the 34 runs, and cannot be reached at 7be4133: LIBURN2 is called only from GETW and from BURSMIX, both only when `LBURS` is true ([[getw.f#L403-L418]]; [[getw.f#L456-L460]]), and GETW sets `LBURS = .FALSE.` on every call ([[getw.f#L140]]), which no namelist setting changes.

6. **(cannot be reached)** **The bottom point's rates are left adjusted.** ([[#L233-L242]]; [[#L270-L271]]) As in `LIBURN` ([[liburn.f#b4]]): Only `HS2(JENV)` is restored, and the adjusted `RLI6`, `RLI7`, `RBE9` at `JENV` stay in `NEWRAT_MOD`. [[bursmix.f#BURSMIX|`BURSMIX`]] copies them into the start rates `OLDRAT_MOD` ([[bursmix.f#L138-L142]]), where this routine's mean start rate (loop 68) weights the adjusted rate with the unadjusted mass.

    **A possible fix:** as for `LIBURN`, save `RLI6(JENV)`, `RLI7(JENV)`, `RBE9(JENV)` with `HS2SAV` and restore them with it.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in any of the 34 runs, and cannot be reached at 7be4133: LIBURN2 is called only from GETW and from BURSMIX, both only when `LBURS` is true ([[getw.f#L403-L418]]; [[getw.f#L456-L460]]), and GETW sets `LBURS = .FALSE.` on every call ([[getw.f#L140]]), which no namelist setting changes.

### LIBURN2

One-step burning with the geometric-mean rate (above).
