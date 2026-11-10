## Explanation

**Purpose.** `TAUINTNEW` computes the convective overturn time scale $\tau_\mathrm{cz}$ (`TAUCZ`) and the radius of the base of the convection zone (`RBCZ`), by the method G. Somers introduced in 3/17. Its comment: search from the centre up for the base of the surface convection zone, and from the surface down; if both agree the zone is unique and the "old top-down sinkline method" is used; if not, several convective cells exist, and the crossing time of the lowest cell in the envelope is taken.

**How it fits.**
- **Inputs:** the full profile from [[gettau.f#GETTAU|GETTAU]] (interior and envelope; `M` points, of which `MINT` are interior shells): `HS1`, `LCZ`, `HR`, `HP`, `HD`, `HG`, `SVEL`, and `DEL1`, `DEL2`: for interior shells GETTAU passes `SDEL(1,·)` and `SDEL(3,·)`, the radiative and adiabatic gradients, but for the stitched envelope points `EDELS(1,·)` and `EDELS(2,·)`, the radiative and actual gradients.
- **Who calls it:** only [[gettau.f#GETTAU|GETTAU]], when `LNEWTCZ` is set; otherwise `GETTAU` calls [[tauint.f#TAUINT|TAUINT]].
- **What it calls:** [[kspline.f#KSPLINE|KSPLINE]] and [[ksplint.f#KSPLINT|KSPLINT]], a natural cubic spline through four points.
- **Outputs:** `TAUCZ` in [[ovrtrn_mod.f|`OVRTRN_MOD`]] (read by the mass-loss and rotation routines, by their names), and the argument `RBCZ` in solar radii.
- **Modules:** [[ovrtrn_mod.f|`OVRTRN_MOD`]] (`TAUCZ`), [[constants_mod.f|`CONSTANTS_MOD`]] (`CLN`, `CMSUN`, `CRSUN`), `JSON` from [[dimensions_mod.f|`DIMENSIONS_MOD`]].

**The method.**
1. **Find the zone.** From shell `IBEG` (first 1) upward: pass the convective core, if any (its top `JCORE`, 0 at the start of each call), then the first convective shell above a radiative region is `IMAX`. From the surface downward, the base of the outermost zone is `JMAX`: the first point `J` below a convective point `J+1` that is radiative, plus one, so that radiative points at the surface are passed over (JvS 02/2026; if no such point exists, `JMAX` = 1). A star with no such zone is radiative ($\tau_\mathrm{cz} = 0$); one convective throughout is fully convective.

    > **Question** ([[#L73-L82]]; [[#L115-L119]]). **`JCORE` may be stale.** `JCORE` is set only when the upward search leaves a convective region that started at `IBEG`. It is 0 at the start of each call, but not reset at label 50, so when a restart begins in a radiative shell, `JCORE` keeps its value from the earlier pass. KC's check avoids an index of 0, but not a stale index. Should `JCORE` be reset at label 50?

    > **Question** ([[#L74]]; [[#L85-L98]]). **A fully convective star.** The code reaches "fully convective" only when every point from `IBEG` to `M` is convective, and then sets `IMAX = 1`, `JCORE = 1`. A star convective throughout its interior is not stitched (GETTAU stitches the envelope only when its `CHKPRS` = `HP(IMAX)-HP(M)` < 1, and here `IMAX` = 1: [[gettau.f#L88-L103]]), so `M = MINT` and the near-core test is skipped; but after a restart that begins inside a zone reaching `M`, with the envelope stitched (`M` ≠ `MINT`), the near-core test `HP(1) - HP(1) < 1` holds, `IBEG = 2`, and the search starts again, possibly in the same state. And if the outermost points are radiative (point `M`, which GETTAU's own search skips), the whole convective interior is taken as a convective core, and $\tau_\mathrm{cz} = 0$. How should a fully convective star be handled?

2. **Reject false zones** and search again from above: a zone less than one decade in pressure above the core, $\log P(\mathrm{JCORE}) - \log P(\mathrm{IMAX}) < 1$ (unless the profile is the interior only); a zone fewer than 3 shells thick; in the interior-only case with two zones (`IJMAX` ≠ 0, `M = MINT`), `IMAX` is set to `JMAX`; and, at the end, a result $\tau_\mathrm{cz} > 10^{20}$. For a zone, `HSTOP` > `HSBOT`, so `LCZSUR` is always true ([[#L137-L150]]); `HSTOP` and `HSBOT` serve only that test.

    Nothing bounds the restarts or keeps their tests inside the profile ([[#b2]]).

3. **The base:** $r_b$ where $\nabla_1 - \nabla_2$ changes sign, by linear interpolation in $\log r$ (for a fully convective star, $\log r_b = 1$: The comment's "very small number" is `RBCZ = 1.`, then `EXP(CLN*RBCZ)`, that is 10 cm, harmless next to a star's radius; settled from the code, Nov 9, 2026: [[#L157-L168]]).

    > **Question** ([[#L163-L166]]; [[gettau.f#L155-L157]]; [[gettau.f#L177-L179]]). **Two kinds of gradient.** `DEL2` is the adiabatic gradient for interior shells but the actual gradient for the stitched envelope points, so the sign change of $\nabla_1 - \nabla_2$ means different things on the two sides of the fitting point. Intended?

4. **One zone** (`IMAX = JMAX`): go up from the base to where $r - r_b = H_p$, with $H_p = P/(\rho g)$. Around that point, four shells give $\delta_k = (r_k - r_b) - H_{p,k}$, and natural cubic splines in $\delta$ evaluated at $\delta = 0$ give $v$ and $H_p$ (the four shells `KK-2` to `KK+1`, with `KK` kept between 3 and `M-1`, so that they lie inside the profile); then
   $$\tau_\mathrm{cz} = \frac{H_p}{v}\bigg|_{\,r - r_b = H_p} .$$
   If already at `IMAX` $r - r_b > H_p$, $\tau_\mathrm{cz} = H_p/v$ there; but the code then goes on to step 5, which replaces it (bug 1). A third spline gives the radius at that point, `ENVRCL`, which nothing reads (unused?, [[#L218-L223]]).
5. **Several cells, or $r_b + H_p$ outside the star:** the lowest zone's top $r_t$ (again where $\nabla_1 - \nabla_2$ changes sign), its width $\Delta r = r_t - r_b$, and $v$ at its middle, $r_b + \Delta r/2$, from a four-point spline in $r$ (the same limits on `KK`):
   $$\tau_\mathrm{cz} = \frac{\Delta r}{v(r_b + \Delta r/2)} .$$

**Changed since `rp_1`.** COMMON blocks to modules, `IMPLICIT NONE` (the unused blocks dropped); the downward search for the base of the outermost zone now requires a convective point above the radiative one (JvS 02/2026), so a radiative layer at the surface no longer makes `JMAX` = `M`. No question is settled: question 6 (now the question on a fully convective star) concerns the upward search.

**Changed since `a8a5950`.** `JCORE` starts at 0 in each call, so a model with a radiative centre no longer reads a value left from an earlier call (narrows question 1); the four-point stencils keep `KK` between 3 and `M-1`, so they no longer read point `M+1` (settles former question 3).

## Bugs, by priority

1. **(not reached)** **The overturn time at `IMAX` is overwritten.** ([[#L176-L181]]; [[#L229-L231]]; [[#L235-L272]]) When the first convective shell is already more than $H_p$ above the base (`VALTEST > 0` at `IMAX`), the code sets `TAUCZ = PSCA/CVEL`, but the `ENDIF` moved on 2025-05-31 to avoid a block mismatch ([[#L229-L230]]) now closes the `IF` before label 110, so this branch falls through to the averaging method, which sets `TAUCZ = DELR/CVEL` instead. Before the move, label 110 was inside the `ELSE` block and the branch went on past it. On the default path (`LNEWTCZ` true), for one zone (`IJMAX` = 0) whose first shell lies more than one scale height above the base, as on a coarse grid.

    **A possible fix:**

    ```diff
    --- a/src/tauintnew.f
    +++ b/src/tauintnew.f
    @@ -179,6 +179,10 @@
                 CVEL = SVEL(IMAX)
                 PSCA = PSCA2
                 TAUCZ = PSCA/CVEL
    +C 11/09/26 KC via Claude
    +C code changed to skip the averaging method, as the branch did before
    +C the ENDIF was moved (2025-05-31).
    +            GOTO 140
              ELSE
                 DO K = IMAX+1,M-1,1
                    PSCA1 = PSCA2
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached: In the 33 runs no model took the branch at [[#L176-L181]], that is, none had its first convective shell more than one pressure scale height above the base of a single zone. The fix was not run. What would reach it: a single surface zone with few shells near its base. Intent: The move is marked "KC 2025-05-31 MOVED ENDIF HERE TO AVOID BLOCK MISMATCH" ([[#L229-L230]]); it made the jump to label 110 legal, and the fall-through looks like a side effect of the move, not a design.

2. **(never occurred)** **The restarts can read past the profile, and can loop forever.** ([[#L75]]; [[#L115-L131]]; [[#L284-L287]]; [[#L92-L98]]) The searches restart with `GOTO 50` for a zone near the core ([[#L115-L118]]), a zone thinner than 3 shells ([[#L124-L131]]), and $\tau_\mathrm{cz} > 10^{20}$ ([[#L284-L287]]). Each restart raises `IBEG`, but nothing stops it from passing `M`, after which `LCZ(IBEG)` is read beyond the profile ([[#L75]]), and the 3-shell test reads `LCZ(IMAX+2)` beyond `M` when `IMAX` ≥ `M-1`, and `LCZ(IMAX+1)` too when `IMAX` = `M` ([[#L124]]). Past its `MM` points, GETTAU's array `LCF` holds values from earlier calls ([[gettau.f#L59]]; [[gettau.f#L158]]; [[gettau.f#L180]]). If such a value is true, the fully convective branch sets `I = 1` and `JCORE = 1` ([[#L92-L98]]) and the tests that follow send the search back to `IBEG` = 2, where it can come round again; and a profile convective at every point, the envelope's surface included, with the envelope stitched (`M` ≠ `MINT`) restarts at `IBEG` = 2 without end, since the near-core test then holds at once, $\log P_1 - \log P_1 = 0 < 1$ ([[#L115-L118]]). Only on the default path (`LNEWTCZ` on), for a profile whose only convective shells above the core lie within two points of the surface, or a stitched profile convective at every point, the envelope's surface included.

    **A possible fix:**

    ```diff
    --- a/src/tauintnew.f
    +++ b/src/tauintnew.f
    @@ -20,7 +20,7 @@
           REAL*8 CVEL,DD1,DD2,DEL1,DEL2,DELR,ENVRCL,FX,HD,HG,HP,HR,HS1,
          *       HSBOT,HSTOP,PSCA,PSCA1,PSCA2,RBCZ,RTCZ,RTEST,RTEST1,RTEST2,
          *       SVEL,VALTEST,XDEL,XRAD,YPSC,YRAD,YSPL,YVEL
    -      INTEGER I,IBEG,IJMAX,IMAX,ITOP,J,JCORE,JMAX,K,KK,M,MINT
    +      INTEGER I,IBEG,IJMAX,IMAX,ITOP,J,JCORE,JMAX,K,KK,M,MINT,NREST
           LOGICAL*4 LALLCZ,LCZ,LCZSUR,LRADZONE
     C 10/13/26 MHP via Claude: removed the unused COMMON/COMP/ declaration
     C (no member referenced here; residue of the obsolete-option removals).
    @@ -71,8 +71,17 @@
     C is radiative never set JCORE, so the test below read the value left
     C from an earlier call (SAVE).
           JCORE = 0
    +C 11/10/26 KC via Claude
    +C code changed to bound the restarts: once IBEG passes M, or after M
    +C restarts (a search that comes round again), the search ends as for
    +C a radiative envelope (TAUCZ = 0), and LCZ is not read past M.
    +      NREST = 0
        50 LRADZONE = .TRUE.
    -      IF (LCZ(IBEG)) LRADZONE = .FALSE.
    +      NREST = NREST + 1
    +      IF(IBEG.GT.M .OR. NREST.GT.M) IBEG = M+1
    +      IF(IBEG.LE.M) THEN
    +         IF(LCZ(IBEG)) LRADZONE = .FALSE.
    +      ENDIF
           DO 60 I = IBEG,M,1
              IF (.NOT.LRADZONE.AND..NOT.LCZ(I)) THEN
                 JCORE = I-1
    @@ -112,7 +121,11 @@
     C ENSURE THIS CZ IS SUFFICIENTLY FAR FROM THE CONVECTIVE CORE. IN SOME CASES
     C THERE ARE A FEW SHELLS RIGHT ABOVE THE CORE THAT ARE CONVECTIVE. SKIP THESE.
     C KC 2025-05-30 ADDED IF CHECK TO AVOID RUNTIME ERROR.
    -      IF (IMAX .GT. 0 .AND. JCORE .GT. 0) THEN
    +C 11/10/26 KC via Claude
    +C code changed to skip this test for a fully convective model, which
    +C has no core: there HP(JCORE)-HP(IMAX) is 0, and with the envelope
    +C stitched (M.NE.MINT) the search went back to IBEG = 2 without end.
    +      IF (IMAX .GT. 0 .AND. JCORE .GT. 0 .AND. .NOT.LALLCZ) THEN
              IF(M.NE.MINT .AND. HP(JCORE)-HP(IMAX).LT.1)THEN
                 IBEG = IMAX+1
                 GOTO 50
    @@ -121,6 +134,13 @@
     C ENSURE THIS CZ IS AT LEAST 3 SHELLS THICK. IF NOT, WE ARE LIKELY SNAGGED
     C ON A SINGLE SHELL CONV ZONE DEEP IN THE INTERIOR. RECOMMENSE SEARCH FROM
     C ABOVE THIS SHELL.
    +C 11/10/26 KC via Claude
    +C code changed to treat a zone with fewer than 3 shells below M as thin
    +C without reading LCZ past M.
    +      IF(IMAX+2.GT.M) THEN
    +         IBEG = M+1
    +         GOTO 50
    +      ENDIF
           IF(.NOT.(LCZ(IMAX).AND.LCZ(IMAX+1).AND.LCZ(IMAX+2)))THEN
              IF(.NOT.LCZ(IMAX+1))THEN
                 IBEG = IMAX+1
    ```

    **Checked by running YREC** (Nov 10, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): In `testsuite/Test_m1p4feh+0p0GS98_dif_TAMS` the search restarted 120 times, at `IBEG` = 298 to 352 in profiles of 407 to 427 points, never more than 20 times in a call; in the other four cases run (`testsuite/Test_m1p0feh+0p0GS98_base_TAMS`, `testsuite/Test_m0p3feh+0p0GS98_base_ZAMS`, `testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`, and `examples/run_standard_solar_model/Test_solarcal_noGS_norot`) it never restarted. `IBEG` never passed `M`, and the 3-shell test never had `IMAX` + 2 > `M`, so nothing was read past the profile and every search ended. The fix was not run: Its guards never act in these runs, so it changes nothing there. The fully convective `testsuite/Test_m0p3feh+0p0GS98_base_ZAMS` (`LNEWTCZ` and `LCALCENV` on by default) never restarted, presumably because its profile's outermost points are radiative, so that it is not convective at every point; this was not checked. What would reach it: a profile whose only convective shells above the core lie within two points of the surface, or a stitched profile convective at every point, the envelope's surface included. Intent: none found.

### TAUINTNEW

The newer overturn time (G. Somers 3/17): finds the base of the main surface convection zone from both directions, then $H_p/v$ one pressure scale height above the base (by four-point splines), or the lowest cell's width over its central velocity; also returns the base's radius in solar units.
