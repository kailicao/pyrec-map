## Explanation

**Purpose.** `GTPURZ` returns the opacity from the LAOL89 table for pure metals ($Z = 1$), with its derivatives, at a given density and temperature.

**How it fits.** Called only by [[getopac.f#GETOPAC|`GETOPAC`]], when $Z > 0.1$ and $\log T > 7.0$ ([[getopac.f#L109]], lowered from 7.7 by "JCZ 211125"; its error message still says "Z>0.10 T > 5 X 10^7 K"; it stops if no pure-$Z$ table was read, `LPUREZ`): `GETOPAC` then interpolates $\log\kappa$ and its derivatives linearly in $Z$ between a normal table (at `ZIT`) and this pure-$Z$ table ($Z = 1$). The table is in the modules `ZLAOL_MOD` (read by [[rdzlaol.f#RDZLAOL|`RDZLAOL`]]) and `ZSLAOL_MOD` (its density splines, from [[zsulaol.f#ZSULAOL|`ZSULAOL`]]), COMMON blocks until `rp_1`; it takes `TOLLAOL` from `NMLPAR_MOD` (formerly `/NWLAOL/`) and the output unit from `IOUNITS_MOD`. Calls `LOCATE`, `XRNG4`, `CSPLINE`, `SPLINT`.

**The method.** As in `GTLAOL` (removed since `rp_1`) but without the composition step: a spline in $\log\rho$ at each of four temperatures (with linear extrapolation within the margin $\ln$ `TOLLAOL`, a natural log where the densities are base 10: [[#b2]]), then a natural spline in $\log T$; chord slopes for the derivatives; $\log\kappa$ capped at 35.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`, the local `TOLL` renamed `TOLLOG`, and the unused `/SLAOL/` no longer declared (question 1 of `rp_1`, now settled and removed).

**Changed since `a8a5950`.** The two stops for a point outside the table (in density, in temperature) now exit with status 1, the code for run-time errors, instead of a bare `STOP` (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(not reached)** **A density beyond the table's margin is reported as a temperature.** ([[#L81-L105]], [[#L120-L126]]) At each of the four temperatures `XRNG4` picks, a density inside the table or within `TOLLOG` of its edges adds a point; one beyond the margin adds none, silently. With one point missing, `NUMTS` < 4 and the run stops with "OUTSIDE Z OPACITY TABLE, IN TEMPERATURE," though the cause is the density. Only with the pure-metal table in use (`LPUREZ`, in helium-burning cores with $Z > 0.1$ above $\log T = 7.0$, [[getopac.f#L109-L116]]).

    **A possible fix:**

    ```diff
    --- a/src/gtpurz.f
    +++ b/src/gtpurz.f
    @@ -103,6 +103,13 @@
                    TT(NUMTS) = ZOT(IT)
                    DODR(NUMTS) = SLOPE
                 END IF
    +C 11/09/26 KC via Claude
    +C code changed to name the density when it lies beyond the table's
    +C margin at one of the four temperatures.
    +            IF(NUMTS.LT.IT-JT1+1) THEN
    +               WRITE(ISHORT,120)DL,TL
    +               STOP 1
    +            END IF
              ELSE
                 WRITE(ISHORT,120)DL,TL
       120       FORMAT(' OUTSIDE Z OPACITY TABLE, IN DENSITY.  ',
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): not reached in any of 34 runs, 26 of YREC's cases (from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning) and 8 made-up ones (each one of YREC's cases with a few settings changed), of which one stopped in its first second: No run stopped here. What would reach it: a density beyond the table's margin at one of the four temperatures. The fix only changes a message, so it was not run. Intent: none found.

2. **(never occurred)** **The extrapolation margin is a natural log.** ([[#L66]]; [[#L87]]; [[#L95-L96]]) `TOLLOG = LOG(TOLLAOL)` is the natural log of `TOLLAOL`, while it is compared with base-10 densities (`TR`, from `ZSRHOL`, which [[zsulaol.f#ZSULAOL|ZSULAOL]] fills with `LOG10(ZORHO(IR))`, [[zsulaol.f#L35]], [[zsulaol.f#L43]]): With the default `TOLLAOL` = 10, which no case sets and YREC's documentation does not describe, a density up to 2.30 dex beyond the table's edge is extrapolated linearly, silently, rather than up to 1 dex. Only with the pure-metal table in use (`LPUREZ`, in helium-burning cores with $Z > 0.1$ above $\log T = 7.0$, [[getopac.f#L109-L116]]) and a density 1 to 2.30 dex beyond the table's edge (in `PURECO.DBGLAOL`, the test suite's table, the densest entries of the temperatures near $\log T = 8$ end between $2 \times 10^5$ and $3 \times 10^6$ g/cm³); beyond the margin the run stops.

    **A possible fix:**

    ```diff
    --- a/src/gtpurz.f
    +++ b/src/gtpurz.f
    @@ -63,7 +63,10 @@
     C     IF WITHIN TOLLAOL OF EDGE THEN LINEAR EXTRAPOLATE
     C
     C     TOLLAOL PERMITS SOME EXTRAPLOATION BEYOND TABLE EDGE.
    -      TOLLOG = LOG(TOLLAOL)
    +C 11/10/26 KC via Claude
    +C code changed to take the margin in decades, as the log10 densities
    +C it is compared with.
    +      TOLLOG = LOG10(TOLLAOL)
           RTL = TL
           RDL = DL
           CALL LOCATE(ZOT,NUMTZ,RTL,JT)
    ```

    **Checked by running YREC** (Nov 10, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The density test ran 57,404,252 times (once at each of the four table temperatures of every call) in `testsuite/Test_m0p95feh+0p0_GN93_TAHB` and 53,733,784 times in `testsuite/Test_m9p0feh+0p0GS98_base_TAHB`, and the density stayed at least 0.48 dex inside the table's upper edge and at least 9.02 dex above its lower edge every time, so neither margin was used. What would reach it: a helium-burning core denser than the table's top by more than 1 dex (not run). The fix was not run, since there was nothing to compare. Intent: none found; the comment ([[#L63-L65]], "TOLLAOL PERMITS SOME EXTRAPLOATION BEYOND TABLE EDGE.") does not say whether `TOLLAOL` is a factor in density.

### GTPURZ

Opacity of a pure-metal mixture: spline in $\rho$, then in $T$.
