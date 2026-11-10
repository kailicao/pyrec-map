## Explanation

**Purpose.** This file takes one adaptive step of the Bulirsch–Stoer method for the envelope and atmosphere integration: the modified midpoint method for an increasing number of substeps, extrapolated to zero substep size. It is the Numerical Recipes routine `BSSTEP` (first edition, with rational extrapolation), extended with the physical arguments that the derivative routine needs.

**How it fits.**
- **Inputs:** `Y(3)`, `DYDX(3)` at `X0` (the independent variable), the trial step `HTRY`, the tolerance `EPS`, the scales `YSCAL`, the derivative routine `DERIV` (passed as an argument by ENVINT: [[qatm.f#QATM|QATM]] for the atmosphere, [[qenv.f#QENV|QENV]] for the envelope) and the stellar quantities it needs (`B`, `FPL`, `FTL`, `GL`, `RL`, `TEFFL`, `X`, `Z`, …); `IMAX` and `NUSE` from the module [[intpar_mod.f|INTPAR_MOD]] (initialized there to 11 and 7; both are also in the `PHYSICS` namelist, read by [[parmin.f#PARMIN|PARMIN]], so a run can change them).
- **Who calls it:** [[envint.f#ENVINT|ENVINT]].
- **What it calls:** [[mmid.f#MMID|MMID]] (modified midpoint) and [[ratext.f#RATEXT|RATEXT]] (rational extrapolation).
- **Outputs:** `Y` and `X0` advanced, `HDID` (the step taken), `HNEXT` (the suggested next step), `ERR` (the scaled error of each variable); on a step-size underflow, a message on the screen and on `ISHORT` (from [[iounits_mod.f|IOUNITS_MOD]]).

**The method.** For $i = 1, \dots, I_\mathrm{max}$, integrate across $H$ with $n_i$ = 2, 4, 6, 8, 12, 16, … midpoint substeps, and extrapolate the results in $(H/n_i)^2$ to zero. Accept the step when
$$\max_j \frac{|\epsilon_j|}{y_{\mathrm{scal},j}} < \mathrm{EPS}.$$
The next step is $0.95H$ if it took `NUSE` sequences, $1.2H$ if one fewer, otherwise $H\,n_{\mathrm{NUSE}-1}/n_i$. If all $I_\mathrm{max}$ sequences fail, retry with
$$H \leftarrow \frac{H/4}{2^{\lfloor (I_\mathrm{max} - N_\mathrm{use})/2 \rfloor}}.$$
If the new step no longer changes `X` (the hydrogen abundance, not the position: suspected bug 1), the run stops with exit status 1, printing `X` and $H$ ([[#L62-L71]]).

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) describes `IMAX` and `NUSE` (defaults 11 and 7) together: the integrators of the envelope and the atmosphere start with a large step, divide it into smaller ones and extrapolate to zero step size; `IMAX` is the largest number of such divisions, `NUSE` the number of earlier steps used in the extrapolation.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/INTPAR/` to `INTPAR_MOD`), `IMPLICIT NONE`.

**Changed since `a8a5950`.** The step-size underflow stop gives `X` and $H$, writes them to `ISHORT` as well as the screen, and ends the run with exit status 1 instead of 0 (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(never occurred)** **The step-size underflow test uses the hydrogen abundance.** ([[#L64]]) `IF(X+H.EQ.X)` tests `X`, which here is the hydrogen abundance passed through to `DERIV`, not the independent variable `X0` ($\log\tau$ in the atmosphere, $\log P$ in the envelope: [[envint.f#L395-L397]], [[envint.f#L693-L695]]); Numerical Recipes tests the independent variable. What follows: The test fires when $H$ is negligible next to $X \approx 0.7$, not next to the position, so a failing step goes on shrinking $H$ (by a factor 16 per round of `IMAX` sequences, with the defaults) somewhat longer before the run stops with "ERROR IN BSSTEP"; with $X = 0$ it fires only once $H$ underflows to zero. The stop and its message come late, the result is not changed. On every run's path, but only when the integration fails.

    **A possible fix:**

    ```diff
    --- a/src/bsstep.f
    +++ b/src/bsstep.f
    @@ -61,9 +61,12 @@
        40 CONTINUE
           H = 0.25D0*H/2.0D0**INT((IMAX-NUSE)/2)
     C      H = 0.25D0*H/2**((IMAX-NUSE)/2)
    -      IF(X+H.EQ.X) THEN
    -         WRITE(*,900)X,H
    -         WRITE(ISHORT,900)X,H
    +C 11/09/26 KC via Claude
    +C code changed to test the independent variable X0, not the
    +C hydrogen abundance X, for a step-size underflow.
    +      IF(X0+H.EQ.X0) THEN
    +         WRITE(*,900)X0,H
    +         WRITE(ISHORT,900)X0,H
      900     FORMAT(' ERROR IN BSSTEP: STEP SIZE UNDERFLOW AT X',1PE14.6,
          *          ' H',E12.3/' RUN STOPPED')
     C 10/30/26 MHP via Claude: bare STOP -> STOP 1, the run-time error code (issue 38).
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): In 33 of 34 runs (26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones; one of these, with `FCORE` = 1.0, stopped in its first second), every one that got past its start, a step failed through all `IMAX` sequences and was shrunk: up to 25,983 times (the 0.04 $M_\odot$ brown dwarf), with the independent variable from $-7.5$ to 12.8 and $H$ down to $1.4\times10^{-6}$. The two tests never disagreed: Neither `X+H.EQ.X` nor `X0+H.EQ.X0` ever held, so the stop was never reached and the step never came near an underflow. It would take an integration that fails completely; none was run. No fix was run. Intent: none found.

2. **(never occurred)** **No check of `IMAX` and `NUSE` against the sizes of the arrays.** ([[#L27-L28]]; [[#L38-L42]]; [[#L57]]; [[ratext.f#L11-L12]]) `IMAX` and `NUSE` are `PHYSICS` namelist variables (defaults 11 and 7, from [[intpar_mod.f|`INTPAR_MOD`]]). The loop runs `I` up to `IMAX` and reads `NSEQ(I)`, declared `NSEQ(11)`; [[ratext.f#RATEXT|RATEXT]] stores `X(IEST)` in `X(11)` and fills up to `NUSE` columns of `D(15,7)` and `FX(7)`. A value of `IMAX` above 11 or `NUSE` above 7 reads and writes out of bounds, and `NUSE` = 1 reads `NSEQ(0)` at line 57. Correct with the defaults (and in [[liburn.f#LIBURN|LIBURN]], which passes `NUSE` = 7 to RATEXT itself).

    **A possible fix:**

    ```diff
    --- a/src/bsstep.f
    +++ b/src/bsstep.f
    @@ -29,6 +29,16 @@
           EXTERNAL DERIV
           DATA NSEQ /2,4,6,8,12,16,24,32,48,64,96/
           SAVE
    +C 11/09/26 KC via Claude
    +C code changed to stop when IMAX or NUSE exceed the sizes of NSEQ
    +C here and of X, D and FX in RATEXT.
    +      IF(IMAX.GT.11 .OR. NUSE.GT.7 .OR. NUSE.LT.2) THEN
    +         WRITE(*,910) IMAX,NUSE
    +         WRITE(ISHORT,910) IMAX,NUSE
    + 910     FORMAT(' ERROR IN BSSTEP: IMAX',I4,' OR NUSE',I4,
    +     *          ' OUT OF RANGE'/' RUN STOPPED')
    +         STOP 1
    +      ENDIF
           H = HTRY
           XSAV = X0
           DO 10 I = 1,NV
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): BSSTEP ran in 33 runs, from 1,020 to 4,437,788 times each, always with `IMAX` = 11 and `NUSE` = 7, the defaults, which every namelist of YREC's cases that sets them keeps. A run with other values would reach it; none was run. No fix was run, since the page's fix is a stop. Intent: none found.

### BSSTEP

One Bulirsch–Stoer step (modified midpoint plus rational extrapolation) of the 3 envelope variables, with step-size control.
