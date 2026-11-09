## Explanation

**Purpose.** `GTPURZ` returns the opacity from the LAOL89 table for pure metals ($Z = 1$), with its derivatives, at a given density and temperature.

**How it fits.** Called only by [[getopac.f#GETOPAC|`GETOPAC`]], when $Z > 0.1$ and $\log T > 7.0$ ([[getopac.f#L109]], lowered from 7.7 by "JCZ 211125"; its error message still says "Z>0.10 T > 5 X 10^7 K"; it stops if no pure-$Z$ table was read, `LPUREZ`): `GETOPAC` then interpolates $\log\kappa$ and its derivatives linearly in $Z$ between a normal table (at `ZIT`) and this pure-$Z$ table ($Z = 1$). The table is in the modules `ZLAOL_MOD` (read by [[rdzlaol.f#RDZLAOL|`RDZLAOL`]]) and `ZSLAOL_MOD` (its density splines, from [[zsulaol.f#ZSULAOL|`ZSULAOL`]]), COMMON blocks until `rp_1`; it takes `TOLLAOL` from `NMLPAR_MOD` (formerly `/NWLAOL/`) and the output unit from `IOUNITS_MOD`. Calls `LOCATE`, `XRNG4`, `CSPLINE`, `SPLINT`.

**The method.** As in `GTLAOL` (removed since `rp_1`) but without the composition step: a spline in $\log\rho$ at each of four temperatures (with linear extrapolation within the margin $\ln$ `TOLLAOL`), then a natural spline in $\log T$; chord slopes for the derivatives; $\log\kappa$ capped at 35.

> **Question** ([[#L65-L66]]; [[#L87]]; [[#L95-L96]]). **Natural log for the margin.** `LOG(TOLLAOL)` is a natural log, while the density it is compared with, `DL`, is $\log_{10}\rho$; is that intended? With the default `TOLLAOL` = 10 (`NMLPAR_MOD`; YREC's documentation does not describe it), the extrapolation reaches $\ln 10 = 2.30$ in $\log\rho$ beyond each temperature's first and last nonzero entries, where a factor 10 in $\rho$ would be 1.0. The comment says only that it "permits some extrapolation beyond table edge". It matters only past the densest entries of the four temperatures used, which in `PURECO.DBGLAOL` (the test suite's table) end between $2 \times 10^5$ and $3 \times 10^6$ g/cm³ near $\log T = 8$; beyond the margin the run stops. (The same question was raised for `GTLAOL`, removed since `rp_1`.)

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`, the local `TOLL` renamed `TOLLOG`, and the unused `/SLAOL/` no longer declared (question 1 of `rp_1`, now settled and removed).

**Changed since `a8a5950`.** The two stops for a point outside the table (in density, in temperature) now exit with status 1, the code for run-time errors, instead of a bare `STOP` (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(c)** **A density beyond the table's margin is reported as a temperature.** ([[#L81-L105]], [[#L120-L126]]) At each of the four temperatures `XRNG4` picks, a density inside the table or within `TOLLOG` of its edges adds a point; one beyond the margin adds none, silently. With one point missing, `NUMTS` < 4 and the run stops with "OUTSIDE Z OPACITY TABLE, IN TEMPERATURE", though the cause is the density. Read from the code, not run; only with the pure-metal table in use (`L2Z`, helium-burning cores). **A possible fix:**

    ```fortran
                END IF
    C 11/09/26 KC via Claude
    C code changed to name the density when it lies beyond the table's
    C margin at one of the four temperatures.
                IF(NUMTS.LT.IT-JT1+1) THEN
                   WRITE(ISHORT,120)DL,TL
                   STOP 1
                END IF
    ```

### GTPURZ

Opacity of a pure-metal mixture: spline in $\rho$, then in $T$.
