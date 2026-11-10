## Explanation

**Purpose.** This file integrates the outer layers of the star, which the interior model does not contain: first the atmosphere, from small optical depth to the photosphere, then the envelope, from the photosphere down to the interior's outermost mass point. The result is the pressure, temperature and radius at that fitting point, which [[surfbc.f#SURFBC|SURFBC]] turns into the surface boundary condition of the interior; the run of the envelope is stored for output, the acoustic depth and the convective overturn time.

**How it fits.**
- **Inputs:** the arguments `B` ($L$), `TEFFL`, `GL` ($\log g$), `RL` ($\log R$), `HSTOT` ($\log M$), `X`, `Z`, `FPL`, `FTL` (rotational corrections), `PLIM` (the expected end pressure), `IE` (which point of the envelope triangle), `LSBC`, `LPRT`, `LPULPT`, and `CMIXL` (the mixing-length constant, passed on to [[qenv.f#QENV|QENV]] through `QENVMIX_MOD`, since QENV is called through BSSTEP with a fixed argument list). From `NMLPAR_MOD`: the atmosphere choice `KTTAU` (0 Eddington gray, 1 Krishna Swamy, 2 the `HRA` $T$–$\tau$ relation, 3 Kurucz, 4 Allard, 5 Castelli–Kurucz 2004); the integration controls (`ATMERR`, `ATMD0`, `ATMBEG`, … and `ENVERR`, `ENVBEG`, …); `TENV0`, `TENV1`, from which `TENV` = (`TENV0` + `TENV1`)/2 is computed here; `LCALCENV`, `LNEWTCZ`; the output switches (`LSTATM`, `LSTENV`, `LSTCH`, `IPVER`). Also `STOLR0` (`INTPAR_MOD`), `SENV` ($\log$ of the fitting point's mass fraction, `COMP_MOD`), `HRAS` (`ATMOS_MOD`), `LCLCD` (`ACDPTH_MOD`), the constants (`CONSTANTS_MOD`) and the unit numbers (`IOUNITS_MOD`).
- **Who calls it:** [[surfbc.f#SURFBC|SURFBC]] (the boundary condition), [[calcad.f#CALCAD|CALCAD]], [[getnewenv.f#GETNEWENV|GETNEWENV]], [[gettau.f#GETTAU|GETTAU]], [[starin.f#STARIN|STARIN]], [[stitch.f#STITCH|STITCH]] and [[wrtmod.f#WRTMOD|WRTMOD]].
- **What it calls:** for tabulated atmospheres [[surfp.f#SURFP|SURFP]], [[kcsurfp.f#KCSURFP|KCSURFP]] or [[alsurfp.f#ALSURFP|ALSURFP]]; for gray ones [[hra.f#HRA|HRA]], [[eqstat.f#EQSTAT|EQSTAT]] and [[getopac.f#GETOPAC|GETOPAC]]; for both integrations [[bsstep.f#BSSTEP|BSSTEP]] with the derivative routines [[qatm.f#QATM|QATM]] and [[qenv.f#QENV|QENV]]; at the end [[taucal.f#TAUCAL|TAUCAL]].
- **Outputs:**
  - arguments: `PS(IE)`, `TS(IE)`, `RS(IE)` (the fitting point's $\log P$, $\log T$, $\log r$), `ESTORE`, `ISTORE` (the state where $T$ first reaches `TENV`), all set only when `LSBC`; counters `KATM`, `KENV`, `KSAHA`;
  - `ENVSTRUCT_MOD`: the envelope profile ($\log P$, $\log T$, $\log m$, $\log\rho$, $\log r$, $X$, $Z$, convective flag, gradients, velocities, $\beta$, $\Gamma_1$, $c_P$, ionization, opacity, $L$, $\rho_T$), reordered from the centre outward; read by CALCAD, GETNEWENV, GETTAU, STARIN, STITCH, TAUINT;
  - `ATMSTRUCT_MOD` (the atmosphere profile, for STITCH); `PPHOT` (`OVRTRN_MOD`, the photospheric pressure, for [[amcalc.f#AMCALC|AMCALC]]); `LPUMOD` (`PULSE1_MOD`, whether QATM and QENV compute the pulsation values) and `QQED`, `QQET`, `QFS` (`PULSE2_MOD`);
  - text: the atmosphere and envelope tables to `ISTOR`, summaries to `ISHORT`, pulsation files `IOPATM`, `IOPENV`.

**The atmosphere.**
- **Tables** (`KTTAU` = 3, 4, 5): the routine reads $\log P$ (and $\log T$) at the photosphere from the table; if the Allard table fails, it switches to the gray atmosphere: it sets `KTTAU = 0` and `LTTAU`, and integrates the gray atmosphere at once ([[#L241-L254]]). The switch is not for good: at its next call [[surfbc.f#SURFBC|SURFBC]] switches back to the Allard tables, with a new triangle, as soon as $\log T_\mathrm{eff}$ is below the table's top ([[surfbc.f#L109-L128]]; settled from the code, Nov 9, 2026).

    > **Question** ([[#L244-L254]]; [[surfbc.f#L120-L127]]). **A failure in $\log g$.** ALSURFP also fails when $\log g$ is outside the table at a $T_\mathrm{eff}$ inside it ([[alsurfp.f#L162-L172]], [[alsurfp.f#L225-L237]]). SURFBC's switch back tests only $T_\mathrm{eff}$, so such a star would go back to the Allard tables at each call of SURFBC, fail again in ENVINT, and start a new triangle each time (not traced in a run). Should the switch back also test $\log g$, or should a failure in $\log g$ stop the run?

- **Gray** (`KTTAU` = 0, 1, 2): start at a small optical depth, with the temperature from the $T$–$\tau$ relation at $\tau \to 0$ (Eddington: $\log T = \log T_\mathrm{eff} - \tfrac14\log\tfrac43 + \tfrac14\log\tfrac23$, that is $T^4 = T_\mathrm{eff}^4/2$; Krishna Swamy: $T^4 = \tfrac34 T_\mathrm{eff}^4 \times 0.550$; `HRA`: its own value at $\tau = 2/3$ shifted by `HRAS`) and the pressure $P = \rho\mathcal{R}T + aT^4/3$ at a chosen density `ATMD0` (the gas term with $\mu$ taken as 1, as the code writes `CGAS*ATMDX*T`; it only sets the starting point: "The integration starts at an arbitrary low density," YREC paper §2.3.6). The starting optical depth is $\tau_0 = \kappa P/g$, where $\kappa$ is the opacity at that $P$ and $T$ (`X0 = PL - GL + DLOG10(O)`, [[#L291]]; whether this is meant as the optical depth of the column above the starting layer is [[#q2|question 2]]). Then, with $\log\tau$ as the variable,
$$\frac{d\log P}{d\log\tau} = \frac{g\,\tau}{\kappa P},$$
with $g$ multiplied by the rotational factor $f_P$ (`FPL`) in QATM's slopes and in the starting slope `DYDX(1)` alike, up to $\tau = 2/3$ (Eddington and `HRA`; $\tau = 0.312$ for Krishna Swamy, the depth where its $T = T_\mathrm{eff}$). The tables, too, give $P$ at $\tau = 2/3$ (YREC paper, §2.3.6), so every option ends where $T = T_\mathrm{eff}$ and the envelope below starts at $r = R$ from $L = 4\pi R^2\sigma T_\mathrm{eff}^4$; switching `KTTAU` changes the photospheric pressure, not the radius. If the starting $\tau$ lies beyond the end, the density is divided by 10 and the start retried, with no limit on the retries ([[#L367-L372]]; suspected bug 5).

    **`ATMD0` is the starting density itself, not its logarithm.** The documentation calls it the "log10 of starting density at τ = 0" (`docs/source/namelist_physics.md`, line 143), but `ENVINT` uses it as the density (`PL = DLOG10((CGAS*ATMDX + CA3*T**3)*T)`, with `ATMDX` = `ATMD0`, [[#L280-L281]]) and divides it by 10 to retry ([[#L367-L372]]), and the default, `1.0D-10` ([[nmlpar_mod.f#L91]]), is a density in g cm⁻³; the documentation could say "starting density."

    > **Question** ([[#L283-L291]]). **The starting optical depth.** The integration starts at $\tau_0 = \kappa P/g$. If the pressure there is the weight of the column above, $P = g\Sigma$, this is $\kappa\Sigma$, the optical depth of that column with $\kappa$ taken as constant: is that the reasoning, and does the start's error matter once the integration reaches $\tau = 2/3$?

**The envelope.** With $\log P$ as the variable and $y = (\log(m/M), \log T, \log r)$, QENV gives
$$\frac{d\log m}{d\log P} = -\frac{4\pi r^4 P}{G m^2 f_P}, \qquad \frac{d\log T}{d\log P} = \nabla, \qquad \frac{d\log r}{d\log P} = -\frac{P r f_P}{G m \rho},$$
where $f_P$ is the rotational distortion factor (`FPL`); note that it multiplies $d\log r/d\log P$ where consistency with the interior equations asks for $1/f_P$ ([[qenv.f#b1]]). The integration starts at the photosphere, with $\log(m/M) = 0$, $r = R$ (`RL`), and the photospheric $T$ and $P$ from the atmosphere or the table, and runs with BSSTEP until $\log(m/M)$ reaches `SENV`; the step is shortened or reversed to land on it, and, when `LSBC` is false, the first step past `PLIM` is cut to end on it. The end point is interpolated linearly to `SENV`. On the way down, when `LSBC`, the state where $\log T$ first reaches `TENV` (6.0 with the defaults `TENV0` = 3, `TENV1` = 9) is kept in `ESTORE` ($\log P$, $\log T$, $\log r$, $\log(m/M)$) and `ISTORE` (the vertex), for HPOINT. `TENV0` and `TENV1` bound the fitting point's temperature: [[hpoint.f#HPOINT|HPOINT]] deletes the outer interior points cooler than `TENV0` (moving `SENV` inward), and, using `ESTORE`, adds a new outermost interior point, at `SENV = ESTORE(4)`, when the outermost point has grown hotter than `TENV1`. The defaults are 3 and 9; all 51 test-suite runs use 2 and 9, and their input files' comment calls the bounds a failsafe, while the documentation says "Code stops below this" and "above this" (whether they are only safeguards, and whether the documentation describes an older behavior, is [[hpoint.f#q2|HPOINT's question 2]]). If the envelope mass is negligible (`SENV > -1e-12`), the photosphere is the fitting point. In the convection zone the loop also sums $\Delta r/v$ into `TAUCZENV` ([[#L627]], [[#L783-L791]]), which is never stored or returned: unused?.

**After the integration.** The profile is reversed (when `SENV` $\le -10^{-12}$, the complement of the test that skips the integration); for TAUCAL the masses are passed in grams (`ENVS1`) and as differences in units of the total mass (`ENVS2`, used only as weights in an average, so the unit cancels); the base of the convection zone is found by linear interpolation of $\nabla_\mathrm{rad} - \nabla$ (its radius, `ENVCZL`, is computed but no longer kept or used: unused?, although the comment after it says "ENVCZL above is still used below," [[#L950-L953]]), and TAUCAL computes the overturn time (unless `LNEWTCZ`, true by default; with rotation it reads the gravity `ENVG`, never set: suspected bug 1). With `LCALCENV` false, the routine stops after the atmosphere, having set `PPHOT`.

**Design.** The routine mixes physics with output for several purposes (the `.store` tables, pulsation files, acoustic-depth arrays), and each output path keeps its own copies of $\Gamma_1$ and related values. Failure to finish in 2000 steps stops the run, with exit status 1 (`STOP 1`). `LDERIV` is set by the pulsation test and then forced to `.TRUE.` on the next line. The atmosphere's two sets of arrays for STITCH stay in step: `ATMOP`, `ATMOT`, … are stored when `LPRT.AND.LSTATM` ([[#L403-L425]]), `ATMOR`, `ADELS` and `NUMATM` when `LCLCD`, `LSTCH` or pulsation output is on ([[#L433-L475]]), and [[stitch.f#STITCH|STITCH]] calls ENVINT with `LPRT = .TRUE.` ([[stitch.f#L160]]) and writes the atmosphere only when `LSTATM` ([[stitch.f#L202]]), so with `LSTCH` both sets come from the same steps (settled from the code, Nov 9, 2026).

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) (Atmospheric integration, Envelope integrator, Surface boundary conditions):

| variable | default | meaning (documentation) |
| --- | --- | --- |
| `ATMERR`, `ENVERR` | 3.0D-4 | numerical tolerance of the atmosphere, envelope integration |
| `ATMBEG`, `ATMMIN`, `ATMMAX` | 0.1, 0.1, 0.5 | first, smallest, largest step in $\log\tau$ |
| `ENVBEG`, `ENVMIN`, `ENVMAX` | 0.1, 0.1, 0.5 | first, smallest, largest step in $\log P$ |
| `ATMD0` | 1.0D-10 | starting density at $\tau = 0$ (may need adjusting for massive stars) |
| `STOLR0` | 1.0D-3 | fractional agreement required between the envelope's mass and the mass at the fitting point |
| `IMAX`, `NUSE` | 11, 7 | the integrator starts with a large step, divides it and extrapolates to zero step: the largest number of divisions, and the earlier steps used in the extrapolation |
| `KTTAU` | 0 | the atmosphere: 0 Eddington, 1 Krishna Swamy, 3 Kurucz, 4 Allard |
| `TENV0`, `TENV1` | 3.0, 9.0 | smallest and largest $\log T$ of the envelope integration |

The code also has `KTTAU = 2` (the Harvard–Smithsonian reference atmosphere, as PARMIN prints it) and `KTTAU = 5` (the Kurucz/Castelli tables, JNT 6/14), which the documentation does not list. [Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html) adds that `LSTCH` writes the interior, envelope and atmosphere to the `.store` file in one consistent format (recommended), and that `LPULSE` needs `LSTATM` and `LSTENV`.

**Changed since `rp_1`.** COMMON blocks to modules, `IMPLICIT NONE`; the MHD equation of state (`LMHD`, the call to MEQOS, removed since `rp_1`) is gone, so the gray atmosphere always uses EQSTAT; `CMIXL` is a new argument (formerly `/CONST3/`), relayed to QENV by `QENVMIX_MOD`; `TENV` is computed here from `TENV0`, `TENV1` (formerly `/CTLIM/`, set by PARMIN); `ENVRCZ` (`/ENVCZ/`) is no longer set, since nothing read it; the write-only `/OPTAB/` settings (`IDT = 15`, `IDD = 5`) are gone; the optical depth in `ATMPRT_MOD` is now named `TAUL`. No question is settled.

**Changed since `a8a5950`.** The atmosphere's starting slope includes `FPL`, as QATM's later slopes do, so the first step of a rotating star no longer starts from slope 1; the reversal swaps `ENVL` completely (settles former question 1); it now also runs for `SENV` $= -10^{-12}$ exactly, which was integrated but not reversed; the two integration failures stop with `STOP 1` (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(not reached)** **`ENVG` never set.** ([[#L82]]; [[#L969-L970]]; [[taucal.f#L130-L142]]) The local array `ENVG` is passed to [[taucal.f#TAUCAL|TAUCAL]] as `HG` (gravity) but never filled here. TAUCAL computes `HG` itself at the two points it needs when `LROT` is false; with rotation it uses `HG` as passed, so the overturn time `TAUCZ` of a rotating model would use an unset $g$ (zero, or what the array held), and `TAUCZ` feeds the angular-momentum loss. Only with `LROT` (off by default) and `LNEWTCZ` = false (true by default).

    **A possible fix:**

    ```diff
    --- a/src/envint.f
    +++ b/src/envint.f
    @@ -954,6 +954,10 @@
     
                 DO I=1,NUMENV
                       ENVS1(I) = DEXP(CLN*(ENVS(I)+HSTOT))
    +C 11/09/26 KC via Claude
    +C code changed to fill ENVG, which TAUCAL uses as HG when LROT, with
    +C G*m/r**2, as TAUCAL computes it otherwise.
    +                  ENVG(I) = ENVS1(I)*DEXP(CLN*(CGL-2.0D0*ENVR(I)))
     
                       IF (I.EQ.NUMENV) THEN
                             ENVS2(I) = 0.0
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): not reached in any of 34 runs (26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones; one of these, with `FCORE` = 1.0, stopped in its first second). Five of them rotate, but `LNEWTCZ` is true by default and in every case, so the call to TAUCAL is skipped ([[#L937]]). A rotating run with `LNEWTCZ` = false would reach it; none was run. No fix was run. Intent: none found.

2. **(wrong output)** **Checked by KC** (Nov 10, 2026). **Wrong $c_P$ in a print.** ([[#L299-L313]]; [[#L403-L412]]) At the first atmosphere point, the printed $\Gamma_1$ and $c_V$ use `QCPP` ($\partial c_P/\partial\ln P$) in place of `QCP`, and the line prints `QCPP` in the column where the later points print $c_P$ (`QQCP`, which QATM sets from `QCP`). It affects only the `.store` output (`LPRT` and `LSTATM`, without `LSTCH`).

    **A possible fix:**

    ```diff
    --- a/src/envint.f
    +++ b/src/envint.f
    @@ -301,11 +301,14 @@
              BETA = 1.0D0 - CA3*(T**2)**2/P
              CHRH = 1.0D0/QDP
              CHT = -CHRH*QDT
    -         CV = QCPP - EXP(CLN*(PL-DL-TL))*CHT**2/CHRH
    -         GAM1 = CHRH*QCPP/CV
    +C 11/09/26 KC via Claude
    +C code changed to use c_P (QCP), not its derivative QCPP, as the
    +C later points do.
    +         CV = QCP - EXP(CLN*(PL-DL-TL))*CHT**2/CHRH
    +         GAM1 = CHRH*QCP/CV
                IF(.NOT.LSTCH)THEN
                  WRITE(ISTOR,20)X0,PL,TL,DL,O,(FXION(I),I=1,3),KSAHA,KATM,
    -     *                   GAM1,QDP,QDT,BETA,QCPP,CV
    +     *                   GAM1,QDP,QDT,BETA,QCP,CV
                ENDIF
        10    FORMAT(6X,'TAU',9X,'P',10X,'T',10X,'D',11X,'O',9X,
          *         'HII  HEII HEIII   SAHA   KATM')
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The print's block ran in 16 runs, but in all of YREC's cases `LSTATM` comes with `LSTCH`, which skips the line. In a made-up run, YREC's 1 $M_\odot$ main-sequence case (`testsuite/Test_m1p0feh+0p0GS98_base_TAMS`) with `LSTCH` off (the default), the line was written 626 times, each with `QCPP` = 0 and $c_P$ from $1.8\times10^{8}$ to $2.2\times10^{8}$, so it printed $c_P$ = 0, $\Gamma_1$ = 0, and a negative $c_V$. With the page's fix, the track is identical and the `.store` file changes beyond the 2% tolerance (a null change, nearly every opacity (all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$) times $1 + 10^{-10}$, moves $\log L$ by up to 0.000267 dex on this case): the print alone, as expected. Intent: none found.

3. **(harmless in the runs)** **The previous point's values on other paths.** ([[#L315-L322]]; [[#L433-L474]]) The block run at each atmosphere step when `LCLCD` or `LSTCH` (not only for pulsation output) uses `TAUP`, `OP`, `DP`, the previous point's $\tau$, $\kappa$ and $\rho$, which are set at the start only when `LPULPT.AND.LPRT`; otherwise, at the first step they keep the values of the last step of an earlier call (all locals are `SAVE`d). What follows: the first `ATMOR` (the step in depth, `DELTR`), which [[stitch.f#STITCH|STITCH]] adds to the base radius it writes to the `.store` file, is wrong. Only with `LSTCH` (off by default; `LCLCD` cannot be set).

    **A possible fix:**

    ```diff
    --- a/src/envint.f
    +++ b/src/envint.f
    @@ -312,14 +312,20 @@
        20    FORMAT(1X,4F11.7,1PE14.7,0P3F6.3,2I7,4F12.8,1P2E12.5)
           ENDIF
     C DBG PULSE INITIAL POINT FOR PULSATION
    +C 11/09/26 KC via Claude
    +C code changed to set the previous point's TAUP, OP and DP whenever
    +C the atmosphere loop uses them (LCLCD or LSTCH), not only for
    +C pulsation output.
    +      IF ((LPULPT.AND.LPRT) .OR. LCLCD .OR. LSTCH) THEN
    +        TAUP = DEXP(CLN*X0)
    +        OP = O
    +        DP = DEXP(CLN*DL)
    +      ENDIF
           IF (LPULPT.AND.LPRT) THEN
             QQED = 0.0D0
             QESUM = 0.0D0
             QQET = 0.0D0
             QFS = 1.0D0
    -        TAUP = DEXP(CLN*X0)
    -        OP = O
    -        DP = DEXP(CLN*DL)
             DELTR = 0.0D0
             PELPF = CGAS * T * D * EMU
     C FROM FIRST LINES OF TPGRAD
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The condition held in all 15 runs with `LSTCH` on and an atmosphere integrated here (the runs with a tabulated atmosphere integrate none), at the first step of each atmosphere integration, from 378 to 33,378 times each, with a stale `TAUP` from 0 (the first call) to 2/3 (the end of the previous atmosphere). With the page's fix, in `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` and `testsuite/Test_solarGS98_difrotmixper18p4d1p0`, the track is identical and the `.store` file changes within 2%: STITCH uses `ATMOR` only as a step added to the base radius ([[stitch.f#L214]]), so the wrong value barely moves the radius it writes. The `.store` file of `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` shows it at model 7: $GM/r^2$ from columns 3 and 4 is 595.0 cm s⁻² at the atmosphere's base and 597.2 at its outermost line (log r = 11.41196), so that line, whose step is the first, lies deeper than the base line, where the outermost point belongs above it: The stale first step shows there, though by only 0.0008 dex in radius. The value is wrong, but no output changes beyond the tolerance. Intent: "JVS 02/11 - Added LCLCD option to IF statement" ([[#L432]]) widened the loop's test but not the initialization.

4. **(wrong output)** **Checked by KC** (Nov 10, 2026). **A stale summary when the envelope is skipped.** ([[#L530-L540]]; [[#L925-L930]]) When the envelope's mass is negligible (`SENV > -1e-12`), the routine jumps to label 300 without integrating, and the summary "ENVELOPE INTEGRATION COMPLETE" on `ISHORT` prints `NOK`, `NBAD`, `SDIF`, `Y(1)` and `ERRSUM` left from the atmosphere integration or, for `SDIF` and with a tabulated atmosphere, from an earlier call. Output only.

    **A possible fix:**

    ```diff
    --- a/src/envint.f
    +++ b/src/envint.f
    @@ -922,7 +922,11 @@
              END IF
           ENDIF
     
    -      WRITE(ISHORT,215)NOK,NBAD,SDIF,Y(1),(ERRSUM(J),J=1,3)
    +C 11/09/26 KC via Claude
    +C code changed to write the summary only when the envelope was
    +C integrated.
    +      IF(SENV.LE.-1.0D-12) WRITE(ISHORT,215)NOK,NBAD,SDIF,Y(1),
    +     *   (ERRSUM(J),J=1,3)
      215  FORMAT(1X,'ENVELOPE INTEGRATION COMPLETE',1X,
          *     'NUMBER OF STEPS ACCEPTED',I5,' REJECTED',
          *     I5/5X,'SENV-LAST M=',1PE22.13,'  LAST M=',E22.13/
    ```

    **How the outputs show it.** In `testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS`, at the starting model (lines 425-429 of the `.short` file), the atmosphere's summary ([[#L481]]) reads 11 steps accepted, 1 rejected, and a largest relative error in $P$ of 3.3397757971120E-09. The envelope's summary that follows ([[#L925]]), for an envelope that was skipped, repeats it: 11 accepted, 1 rejected, a largest error "in M" of 3.33978E-09, "SENV-LAST M" 0, and a "LAST M" of 3.5150923795936E+00, the atmosphere's last `Y(1)`, a log pressure ([[#L292]]), not a mass. The next envelope summary (line 441) reports 84 steps and a "LAST M" of -9.9999999886368E-05.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The summary was written in 33 runs; the envelope was skipped once each in four: the rotating 3 $M_\odot$ case, both 2 $M_\odot$ `vzams150` cases, and `testsuite/Test_m9p0feh+0p0GS98_base_TAHB`, with `SENV` = 0 and stale step counts from 7 to 11. With the page's fix, in the 3 $M_\odot$ case and `testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS`, the track and the `.store` file are identical and the `.short` file changes beyond 2%: the summary alone, as expected. Intent: none found.

5. **(never occurred)** **No limit on the retries of the atmosphere's start.** ([[#L273-L281]]; [[#L367-L372]]) When the starting $\tau_0$ lies beyond the end, `ATMDX` is divided by 10 and the start retried, with no limit. As `ATMDX` falls, $P$ tends to the radiation pressure $aT^4/3$, so $\tau_0 = \kappa P/g$ no longer falls; if that alone puts $\tau_0$ past $\tau = 2/3$, which for the starting $T^4 = T_\mathrm{eff}^4/2$ means $\kappa L/(4\pi c G M) \gtrsim 1$ with the starting opacity (a model at or beyond the Eddington limit, as a diverging iteration might give), the loop never ends: the run hangs instead of stopping.

    **A possible fix:**

    ```diff
    --- a/src/envint.f
    +++ b/src/envint.f
    @@ -74,6 +74,7 @@
          *       NOK,NSTEP,NV
           LOGICAL*4 LALFAIL,LATMO,LDERIV,LDUM,LLSTORE,LOCOND,LPRT,LPULPT,
          *       LSBC,LSURCZ,LTEST
    +      INTEGER NRETRY
     
     C PARAMETERS NT AND NG FOR TABULATED SURFACE PRESSURES OF KURUCZ.
     C JNT 06/14 ADDED NTC/NGC FOR KTTAU=5
    @@ -271,6 +272,7 @@
     C                 point (XLIM). When this happens, we divide the effective
     C                 starting density (atmd0) by 10 and retry.
           atmdx = atmd0
    +      NRETRY = 0
      1998 continue
     C Return point if X0 > XLIM
           T = DEXP(CLN*TL)
    @@ -366,6 +368,14 @@
           END IF
     
           if  (x0 .gt. xlim) then ! Check that starting point is before endpoint
    +C 11/09/26 KC via Claude
    +C code changed to stop after 30 retries (ATMDX = 1D-30 * ATMD0)
    +C instead of looping without end.
    +         NRETRY = NRETRY + 1
    +         IF(NRETRY.GT.30) THEN
    +            WRITE(ISHORT,*)'ENVINT: ATMOSPHERE START NOT FOUND'
    +            STOP 1
    +         ENDIF
              write(ishort,*)"ENVINT: X0>XLIM, X0,XLIM:",x0,xlim
            write(ishort,*)"ENVINT: get new X0 by dividing ATMD0 by 10"
            atmdx = atmdx / 10D0   ! If not before, divide starting density by 10
    ```

    with `NRETRY = 0` set before label 1998.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The start was retried in two runs, both 9 $M_\odot$ helium-burning cases (`testsuite/Test_m9p0feh+0p0GS98_base_TAHB` 68 times, `sample_cases/UpperMS/Sample_m9p0feh+0p0GS98_none_TAHB` 40 times), with $\tau_0$ past the end by 0.0038 to 0.246 in $\log\tau$; every retry began from `ATMD0`, so one division by 10 always sufficed, and the 30 retries of the condition were never approached. A model near the Eddington limit would reach it; none was run. No fix was run, since the page's fix is a stop. Intent: The comment ([[#L269-L272]]) says the retry is meant ("very occasionally the integration fails because the starting point (X0) is past the end point (XLIM)"); it says nothing of a limit.

### ENVINT

Integrates the atmosphere (gray $T$–$\tau$ or tabulated) and the envelope (in $\log P$, with [[bsstep.f#BSSTEP|BSSTEP]] and [[qenv.f#QENV|QENV]]) down to the fitting mass, returns the fitting point's $P$, $T$, $r$, stores the envelope profile in `/ENVSTRUCT/`, and finds the convection zone's base and overturn time.
