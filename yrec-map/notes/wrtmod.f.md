## Explanation

**Purpose.** `WRTMOD` writes extra profiles of one model: with `LSOUND`, a sound-speed and structure table (to the units `IMODPT` and `ISOUND`, the file `Csound.dat`); with `LSTATM`, `LSTENV` or `LPULSE`, an envelope integrated again for printing; and with `LPULSE`, a model for pulsation codes on `IOPMOD`, in one of three versions (`IPVER`).

**How it fits.**
- **Inputs:** the model (arguments: `M`, `JENV`, `HCOMP`, `HS1`, $\log\rho$, $L$, $\log P$, $\log r$, $\log T$, `MODEL`, $\log L$, $\log T_\mathrm{eff}$, `FP`, `FT`, $\log m$ `HS`, the age, the mixing length `CMIXL` and the star's mass `XMSOL`, a snapshot of `SMASS` taken by the main program), and through modules the per-shell physics: $\Gamma_1$ and the switch `LSOUND` (`SOUND_MOD`), the pulsation derivatives `PQDP`, `PQDT`, … (`PULSE1_MOD`), energy rates, opacity and gradients (`SCRTCH_MOD`), `STOTAL` (`COMP_MOD`), and the namelist switches and integration steps (`LSTORE`, `LSTATM`, `LSTENV`, `LPULSE`, `IPVER`, `SPOTF`, `SPOTX`, `ATMSTP`, `ENVSTP`, … in `NMLPAR_MOD`; formerly `CCOUT`, `PULSE`, `SPOTS`, `ENVGEN`, `INTATM`, `INTENV`).
- **Who calls it:** [[putstore.f#PUTSTORE|PUTSTORE]] (when the atmosphere or envelope is stored) and [[wrtout.f#WRTOUT|WRTOUT]] (for pulsation output between stored models).
- **What it calls:** [[envint.f#ENVINT|ENVINT]], which itself prints the envelope and atmosphere (and the pulsation envelope with `LPULPT`).
- **Outputs:** `IMODPT`, `ISOUND` (the file `FSOUND`, `Csound.dat` by default, opened once by [[parmin.f#PARMIN|PARMIN]]), `IOPMOD`, and the envelope printed by `ENVINT`.

**The method.**
1. **Sound speed** (`LSOUND`). For each shell, with $V = G m \rho/(P r)$ and $U = 4\pi\rho r^3/m$: $r/R_\odot$, $m/M_\odot$, $m/r^3$ (solar units), $V/\Gamma_1$, $\Gamma_1$,
   $$A = -V/\Gamma_1 + V\left(\frac{\partial\ln\rho}{\partial\ln P} + \nabla\,\frac{\partial\ln\rho}{\partial\ln T}\right)$$
   (the code's `XX4`; probably the buoyancy term, by its form), $U$, and $c_s = \sqrt{\Gamma_1 P/\rho}$ in km/s. Between shells it also writes $dP/dr$-like and $d\rho/dr$-like terms (`QPR`, `QDR`) and their differences scaled by $\Gamma_1 P\,\Delta r$ and $\rho\,\Delta r$.

    > **Question** ([[#L138]]; [[#L140]]). **`Csound.dat`'s header.** The header line is written again at every call to the file `PARMIN` opened once, so a run that writes several models repeats it between their tables, with no model number or age. Is the repeated header meant to separate the models, and should it say which model follows?

2. **Envelope.** The integration steps are set to the output steps, `ENVINT` integrates from the surface to the last shell's pressure (for a spotted star at the ambient temperature, as in [[starin.f|starin.f]]), and the steps are restored afterwards.
3. **Pulsation model** (`LPULSE`). A header (`LPULSE` alone), then, only when both `LPULSE` and `LSTORE` are set, for each shell in the list `ID(1..IDM)`: $\log r$, $m/M$, $L$, $\log T$, $\log\rho$, $\log P$, $\epsilon$, $\kappa$ and the derivatives, in format 1, 2 or 3 (version 3 adds three columns for the MLT quantities, written as zeros).

**For users** (from YREC's [Quick Start](https://yrec.readthedocs.io/en/latest/quickstart.html)). With `LPULSE`, the pulsation output: the interior model on `IOPMOD` (`.pmod`, written here) and the envelope and atmosphere on `IOPENV` and `IOPATM` (`.penv`, `.patm`, written by [[envint.f#ENVINT|`ENVINT`]] when called from here); the Quick Start names the last `.atm`, the test suite's namelists `.patm`. `IMODPT` is the `.full` file (`FMODPT`).

> **Question** ([[#L152]]; [[#L171]]). **The deprecated `.full` file.** YREC's Quick Start lists `.full` (`FMODPT`) as a deprecated output, and the test suite's namelists say "No longer used," but PARMIN still opens it (and writes the run's description to it), and WRTMOD (with `LSOUND`), [[checkj.f#CHECKJ|`CHECKJ`]] and [[seculr.f#SECULR|`SECULR`]] still write to it. Should these writes be removed, or should the documentation say what the file now holds?

**Changed since `rp_1`.** `CMIXL` and `XMSOL` are now arguments (`CMIXL` is passed on to `ENVINT`); the sound-speed file is written to the unit `ISOUND`, opened once by `PARMIN`, instead of being opened on unit 500 at each call, which settles part of question 1; declarations: COMMON blocks to modules, `IMPLICIT NONE`.

**Changed since `a8a5950`.** Version 3 of the pulsation model writes literal zeros in its three mixing-length columns, which held `PUALPHA_MOD`'s always-zero `VALFMLT`, `VPHMLT`, and `VCMXMLT` (now removed), so that readers of `IPVER` = 3 see the same layout; `PUALPHA_MOD` is no longer used here.

## Bugs, by priority

1. **(wrong output)** **Checked by KC** (Nov 10, 2026). **A typo in $d\rho/dr$.** ([[#L165-L168]]) `QDR2`, the $d\rho/dr$-like term at shell `I+1`, multiplies by `QPR1`, the $dP/dr$-like term at shell `I`, instead of `QPR2`, as `QDR1` does with `QPR1`. What follows: The written `QDR2`-based difference `QQDR` ([[#L170-L171]]) is wrong in the `.full` file (`IMODPT`); nothing reads it back. Only with `LSOUND`, which main.f sets for the last model of a run.

    **A possible fix:**

    ```diff
    --- a/src/wrtmod.f
    +++ b/src/wrtmod.f
    @@ -165,7 +165,9 @@
                   QPR1 = EXP(CLN*(CGL+HS(I)+HD(I)-2.0D0*HR(I)))
                   QDR1 = EXP(CLN*(HD(I)-HP(I)))*PQDP(I)*QPR1
                   QPR2 = EXP(CLN*(CGL+HS(I+1)+HD(I+1)-2.0D0*HR(I+1)))
    -              QDR2 = EXP(CLN*(HD(I+1)-HP(I+1)))*PQDP(I+1)*QPR1
    +C 11/09/26 KC via Claude
    +C code changed to use QPR2, the term at shell I+1, in QDR2.
    +              QDR2 = EXP(CLN*(HD(I+1)-HP(I+1)))*PQDP(I+1)*QPR2
                   QQPR = (QPR1-QPR2)/DIVP
                   QQDR = (QDR1-QDR2)/DIVR
                   WRITE(IMODPT,124)RMID/CRSUN,QPR1,QDR1,QQPR,QQDR
    ```

    **How the outputs show it.** The right `QDR2` is the next shell's `QDR1`, which the `.full` file writes on the next line of format 124 ([[#L166]]; [[#L171]]; the file alternates them with the shells' format-123 lines, [[#L152]]), so the right `QQDR` follows from the file's own columns: the written value times $(Q_{D,i}-Q_{D,i+1})/(Q_{D,i}-Q_{D,i+1}Q_{P,i}/Q_{P,i+1})$, with $Q_P$ and $Q_D$ the second and third columns. In `testsuite/Test_solarGS98_dif`, at the last model (1208), the 301st line of this kind (at 0.1598544 $R_\odot$) writes `QQDR` as -6.19613054E-21, where the columns give 1.54E-20; the two differ in sign on 766 of the 795 lines, and the median ratio is -2.5.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The sound-speed block ran once per run, at the last model (models 748 to 1,723), in 10 of 34 runs: seven of YREC's solar cases with `LPULSE` (for example, `testsuite/Test_solarGS98_dif`), two made-up ones built on them, and a made-up run with `LSTCH` off (YREC's `testsuite/Test_m1p0feh+0p0GS98_base_TAMS`, with the default). On every shell, `QPR1` differed from `QPR2` by −5.6% to +10.3%, the factor by which `QDR2` is off. With the fix, `testsuite/Test_solarGS98_allard` and `testsuite/Test_solarM22M_difkur` have identical tracks and `.store` files and `.short` files within 2%; the `.full` file that holds `QQDR` is not among the files the test suite compares. Intent: none found; `QDR1` uses `QPR1`, at its own shell.

2. **(wrong output)** **Checked by KC** (Nov 10, 2026). **The pulsation model's shell list is never set.** ([[#L51]]; [[#L255-L256]]; [[#L265-L266]]) `IDM` and `ID(J)` are locals, never assigned (the "long block" removed by G. Somers 11/14, [[#L307]], or the arguments `LSHELL`, `JXBEG`, `JXEND`, removed since, may have set them). The header prints `IDM`, and the loop `DO 220 J = 1,IDM` uses undefined values. What follows: With the usual static, zero-filled storage of `SAVE`d locals, `IDM` = 0, so the pulsation model (`LPULSE` and `LSTORE`) has a header with "NUMBER OF SHELLS IN MODEL= 0" and no shells; with another value, `ID(J)` could index out of bounds. Only with `LPULSE` (off by default).

    **A possible fix:** a choice for the developers: what shells the pulsation model should list (every shell, `IDM = M` and `ID(J) = J`, is the simplest), or whether the `LPULSE` output is still in use.

    **How the outputs show it.** In `testsuite/Test_solarGS98_dif`, all 1,186 model headers of the `.pmod` file read "NUMBER OF SHELLS IN MODEL=    0" ([[#L255-L256]]), and the file holds nothing but these headers (7,116 lines, six a model). The `.track` gives the same models' shell counts in its Shls column ([[wrtout.f#L558]]): 709 at model 22, the first header, and 797 at model 1208, the last. The envelope and atmosphere parts of the same pulsation output, the `.penv` and `.patm` files, are written in full (34 and 57 MB).

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): WRTMOD reached the pulsation header in the nine runs with `LPULSE` (seven of YREC's solar cases and two made-up ones built on them), at every model not stored (1,186 to 1,701 times a run), and `IDM` was 0 every time: The header says the model has 0 shells, and no shell is written, so the pulsation model is empty in every run that asks for it. `IDM` never held another value, so `ID(J)` never indexed out of bounds. The fix is the developers' choice, and none was run. Intent: The comment at [[#L307]] records the removal of a block, not what was to replace it.

3. **(wrong output)** **Checked by KC** (Nov 10, 2026). **Debugging prints.** ([[#L127]]; [[#L131]]) `print*,'wrtmod LSOUND 1: '` writes to the screen at every call, and `print*,'wrtmod LSOUND 2: '` at every call with `LSOUND`.

    **A possible fix:**

    ```diff
    --- a/src/wrtmod.f
    +++ b/src/wrtmod.f
    @@ -122,14 +122,12 @@
     C (no member referenced here; residue of the obsolete-option removals).
     C G Somers END
     
    +C 11/09/26 KC via Claude
    +C code changed to remove the two debugging prints of LSOUND.
           SAVE
     
    -         print*,'wrtmod LSOUND 1: ',LSOUND
    -
           IF(LSOUND)THEN
     
    -         print*,'wrtmod LSOUND 2: ',LSOUND
    -
     CFD 10/09 Add an extra output to plot the sound speed profile easyly
     C 9/25/26 MHP via Claude
     C code changed to use the managed ISOUND unit (opened once in PARMIN
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The first print ran at every call of WRTMOD: 1,186 to 1,701 times a run in the nine runs with `LPULSE`, and once in the run with `LSTCH` off; the second once per run, at the last model. With the prints removed, `testsuite/Test_solarAAG21_dif` and `testsuite/Test_solarGS98_allard` have identical tracks and `.store` files and `.short` files within 2%; the prints go to the screen, which the test suite does not compare. Intent: The matching print in the main program is commented out ([[main.f#L670-L671]]).

4. **(never occurred)** **`LPRT` may be unset.** ([[#L186]]; [[envint.f#L206]]; [[envint.f#L222]]) `LPRT` is a local, set to true only if `LSTORE`, and never set false; otherwise `ENVINT` gets its `SAVE`d or undefined value, which decides whether it prints the envelope and atmosphere. With the usual zero-filled storage it is false, which matches the design (the pulsation model, too, needs `LSTORE`, [[#L273]]), so this is correct today but rests on the compiler.

    **A possible fix:**

    ```diff
    --- a/src/wrtmod.f
    +++ b/src/wrtmod.f
    @@ -183,7 +183,9 @@
     C  PRINTING OUT THE RESULTS.
     C  SET UP FLAGS AND COUNTERS.
            LSBC0 = .FALSE.
    -       IF(LSTORE)LPRT = .TRUE.
    +C 11/09/26 KC via Claude
    +C code changed to set LPRT on every call, not only when LSTORE.
    +       LPRT = LSTORE
            KATM = 0
            KENV = 0
            KSAHA = 0
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): not reached. The line ran in 10 runs (1,186 to 1,701 times a run in the nine with `LPULSE`), always with `LSTORE` on, so `LPRT` was set every time. Not run: `LPULSE` with `LSTORE` off, which none of YREC's cases uses. Intent: none found.

### WRTMOD

Extra profiles of one model: sound-speed table, a reprinted envelope, and the pulsation model (whose shell list is currently undefined).
