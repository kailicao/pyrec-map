## Explanation

**Purpose.** This file drives the solar calibration: after each solar model, it checks whether the model has the solar luminosity and radius (and, optionally, the solar surface $Z/X$) at the solar age; if not, it computes new guesses for the hydrogen abundance $X$ and the mixing length $\alpha$ (and $Z$) for the next model, by a Newton step.

**How it fits.**
- **Inputs:** the arguments `BL` ($\log L/L_\odot$ of the model), `RL` ($\log R/R_\odot$, computed by the caller from $L$ and $T_\mathrm{eff}$), `N` (the current kind card) and `SOLZX` (the model's surface $Z/X$); the tolerances `TOLL`, `TOLR`, `TOLZ`, the switch `LCALSOLZX` and the target `CALSOLZX` in [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]], set in [[parmin.f#PARMIN|PARMIN]] and [[setcal.f#SETCAL|SETCAL]].
- **Who calls it:** the main program ([[main.f#(file level)|main.f]]), when solar calibration is on (`LCALS`), at every third kind card (`MOD(NK,3).EQ.0`, [[main.f#L1147-L1152]]): "solar models in 3 kind cards" (MHP 5/96).

    **The header predates the three-card cycle.** It says "ONLY CALLED FOR EVEN NK, ASSUMES RESCALING ON ODD NK AND EVOLVING ON EVEN NK" ([[#L22-L23]]), but main.f calls it when `NK` is a multiple of 3 ([[main.f#L1147]]), which matches the routine's use of `N-2` and `N+1..N+3` ([[#L93-L97]]; [[#L153-L163]]).

- **Outputs:** the arguments `LSOL` and the derivatives `DLDX`, `DRDX`, `DLDA`, `DRDA`, which the main program keeps (they were in `/CALSUN/`, also used by WRTMONTE, removed since `rp_1`); the new $X$ (`RESCAL(2,N+1)`, and `XENV0A` for cards $N+1$ to $N+3$), $\alpha$ (`CMIXLA`, cards $N+1$ to $N+3$) and $Z$ (`RESCAL(3,N+1)`, `ZENV0A`) in [[runloop_mod.f#RUNLOOP_MOD|`RUNLOOP_MOD`]] (`RESCAL`) and `NMLPAR_MOD` (the others); lines to unit `IOWR`.
- **Kept between calls:** the previous model's `BLP`, `RLP` and the steps `DX`, `DA`, now local variables kept by `SAVE`.

**The method.**
1. **Converged** if $|\log L/L_\odot| <$ `TOLL` and $|\log R/R_\odot| <$ `TOLR` and, with the $Z/X$ option, $|\log_{10}(Z/X) - \log_{10}(Z/X)_\odot| <$ `TOLZ`: set `LSOL` and return. The target is thus exactly $L_\odot$ and $R_\odot$. These are the code's `CLSUN` and `CRSUN` (in `CONSTANTS_MOD`, settable in the `PHYSICS` namelist), $3.8515\times10^{33}$ erg s⁻¹ and $6.9598\times10^{10}$ cm by default; `BL` and `RL` are measured in them (how these compare with other adopted solar values is the question below).

    > **Question** ([[#L59]]; [[constants_mod.f#L44-L49]]). **The solar values targeted.** Convergence means $|\log L/L_\odot| <$ `TOLL` with the default $L_\odot$ = `CLSUN` = $3.8515\times10^{33}$ erg s⁻¹ and $R_\odot$ = `CRSUN` = $6.9598\times10^{10}$ cm, while the IAU 2015 nominal values are $3.828\times10^{33}$ erg s⁻¹ and $6.957\times10^{10}$ cm. With `TOLL` = $10^{-5}$, the 0.6% difference in $L_\odot$ ($0.0027$ in $\log L$) is far larger than the tolerance, so the calibrated $X$ and $\alpha$ depend on which value is used. Are the defaults kept for continuity with published YREC solar models, and should the documentation of `TOLL`, `CLSUN` and `CRSUN` say that a calibration matches whatever $L_\odot$, $R_\odot$ the namelist sets?

    > **Question** ([[#L59-L72]]). **$Z/X$ not converged.** If $L$ and $R$ are within tolerance but $Z/X$ is not, the routine falls through to the Newton step and also changes $X$ and $\alpha$ slightly. Is this intended? (A target `CALSOLZX` of 0 is bug 2.)

2. **Newton step** with fixed partial derivatives ("empirical," LLP 6/28/09): $\partial\log L/\partial X = -3.78$, $\partial\log R/\partial X = -0.89$, $\partial\log L/\partial\alpha = 0.0139$, $\partial\log R/\partial\alpha = -0.050$. It solves
$$\log L + L_X\,\Delta X + L_\alpha\,\Delta\alpha = 0, \qquad \log R + R_X\,\Delta X + R_\alpha\,\Delta\alpha = 0,$$
that is
$$\Delta\alpha = \frac{\log L\,R_X/L_X - \log R}{R_\alpha - L_\alpha R_X/L_X}, \qquad \Delta X = -\frac{\log L + L_\alpha\,\Delta\alpha}{L_X}.$$

    > **Question** ([[#L74-L84]]; [[main.f#L1163]]). **Fixed derivatives.** Why fixed "empirical" derivatives rather than secants from the previous cycles (`BLP`, `RLP` are already saved)? A user changing the physics (another opacity, say) would want to know whether convergence slows, or fails within the 15 cycles main.f allows, when the true derivatives differ from these.

3. The new values go to kind cards $N+1$ to $N+3$, starting from those of card $N-2$ (the start of the current cycle). With the $Z/X$ option, $Z$ is scaled: $Z_\mathrm{new} = Z_\mathrm{old}\,(Z/X)_\odot / (Z/X)_\mathrm{model}$.

**Design.** An older method, which measured the derivatives with extra runs at kind cards 3, 6 and 9, is still in the file but skipped by `GOTO 1234` ([[#L85-L146]]; unused?; on that path `DX` and `DA` are never set, their assignments being commented out, [[#L91]], [[#L110]]). The local `ZLP` is set ([[#L181]]) and never read (unused?).

**From YREC's documentation.** [Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html) (Calibration): `TOLL`, `TOLR` are the tolerances of the solar calibration in $L$ and $R$; `LCALSOLZX` enforces the mixture's $Z/X$, `CALSOLZX` (0.02292 for GS98), and without it $Z$ is held constant in the calibration loop.

**Changed since `rp_1`.** `/CALSUN/` retired: the derivatives and `LSOL` are now arguments, and `BLP`, `RLP`, `DX`, `DA` saved locals; COMMON blocks to modules, `IMPLICIT NONE`.

**Changed since `a8a5950`.** Only the comment on `DLDA` changed: It read "+0.139," ten times the value used, and now reads "+0.0139"; a fit over the iterates of a recalibration of 11 solar decks gives $\partial\log L/\partial\alpha$ of order 0.01, so 0.0139 is the value meant (this settles former question 1).

## Bugs, by priority

1. **(wrong output)** **Checked by KC** (Nov 10, 2026). **The first cycle prints an "Old BL" and "Old RL" that were never set.** ([[#L167-L170]]; [[#L179-L180]]) `BLP` and `RLP` are saved locals with no `DATA` and are set only at the end of the Newton step, so on the first call (`N` = 3) the lines "New BL, Old BL, Delta BL" and "New RL, Old RL, Delta RL" print whatever they hold before any assignment (zero under most compilers, not promised by the standard). Only the output to `IOWR` is affected; the Newton step does not use them. Only with `LCALS` (off by default).

    **A possible fix:**

    ```diff
    --- a/src/chkcal.f
    +++ b/src/chkcal.f
    @@ -164,10 +164,15 @@
              XENV0A(N+1) = RESCAL(2,N+1)
              XENV0A(N+2) = RESCAL(2,N+1)
              XENV0A(N+3) = RESCAL(2,N+1)
    -         WRITE(IOWR,*) "New BL, Old BL, Delta BL: ",
    -     *       BL, BLP, BL-BLP
    -         WRITE(IOWR,*) "New RL, Old RL, Delta RL: ",
    -     *       RL, RLP, RL-RLP
    +C 11/09/26 KC via Claude
    +C code changed to print the previous model's L and R only once there
    +C is one.
    +         IF(N.GT.3)THEN
    +            WRITE(IOWR,*) "New BL, Old BL, Delta BL: ",
    +     *          BL, BLP, BL-BLP
    +            WRITE(IOWR,*) "New RL, Old RL, Delta RL: ",
    +     *          RL, RLP, RL-RLP
    +         ENDIF
              WRITE(IOWR,*) "New X, Old X, DX: ",
          *       RESCAL(2,N+1), RESCAL(2,N-2), DX
              WRITE(IOWR,*) "New A, Old A, DA: ",
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged). YREC's solar calibration (`examples/run_standard_solar_model/Test_solarcal_noGS_norot`, the only case with `LCALS` on) printed these lines twice, the first time on the first call ($N$ = 3, with $\log L$ and $\log R$ off by about $1.4\times10^{-4}$ and $2.2\times10^{-5}$ dex), before `BLP` and `RLP` had been set: The suspected path is taken in every calibration that needs more than one cycle. No fix was run, since it changes only two printed lines and nothing computed reads them. Intent: none found; the comment at [[#L42-L45]] explains why `BLP` and `RLP` are saved across calls, not what they hold on the first. Only the printed output is wrong.

2. **(never occurred)** **A target $Z/X$ of 0 sets $Z = 0$.** ([[#L61]]; [[#L156-L157]]) The convergence test uses $Z/X$ only when `LCALSOLZX` is true and `CALSOLZX` > 0; the update of $Z$ tests only `LCALSOLZX`. With `LCALSOLZX` true and `CALSOLZX` = 0 (or negative), the test ignores $Z/X$ while the update sets `RESCAL(3,N+1)` = `RESCAL(3,N-2)*CALSOLZX/SOLZX` = 0, so the next three runs start with no metals. Not on the default path: `LCALSOLZX` is false by default and `CALSOLZX` is 0.02292 ([[nmlpar_mod.f#L53-L54]]); a target of 0 is not a sensible input, so this is fragile code rather than a wrong result in practice.

    **A possible fix:**

    ```diff
    --- a/src/chkcal.f
    +++ b/src/chkcal.f
    @@ -153,7 +153,9 @@
              CMIXLA(N+1) = CMIXLA(N-2)+DA
              CMIXLA(N+2) = CMIXLA(N+1)
              CMIXLA(N+3) = CMIXLA(N+1)
    -         IF(LCALSOLZX)THEN
    +C 11/09/26 KC via Claude
    +C code changed to scale Z only under the test the convergence check uses.
    +         IF(LCALSOLZX .AND. CALSOLZX.GT.0.0D0)THEN
                 RESCAL(3,N+1) = RESCAL(3,N-2)*CALSOLZX/SOLZX
                 DZ = RESCAL(3,N+1) - RESCAL(3,N-2)
                 ZENV0A(N+1) = RESCAL(3,N+1)
    @@ -172,7 +174,7 @@
          *       RESCAL(2,N+1), RESCAL(2,N-2), DX
              WRITE(IOWR,*) "New A, Old A, DA: ",
          *       CMIXLA(N+1), CMIXLA(N-2), DA
    -         IF(LCALSOLZX)THEN
    +         IF(LCALSOLZX .AND. CALSOLZX.GT.0.0D0)THEN
                 WRITE(IOWR,*) "New Z, Old Z, DZ: ",
          *       RESCAL(3,N+1), RESCAL(3,N-2), DZ
              ENDIF
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged). The same calibration took the path twice, with `CALSOLZX` = 0.02292 both times (the model's $Z/X$ between 0.0229188 and 0.02292); the target was never 0 or below, and every one of YREC's namelists that sets it gives 0.02292, the GS98 value. The fix was not run, since no case reaches the condition. What would reach it: `LCALS` and `LCALSOLZX` on with `CALSOLZX` $\le 0$. Intent: none found.

### CHKCAL

Checks a solar model against $L_\odot$, $R_\odot$ (and $Z/X$); if not calibrated, sets new $X$, $\alpha$ (and $Z$) for the next three kind cards by a Newton step with fixed derivatives.
