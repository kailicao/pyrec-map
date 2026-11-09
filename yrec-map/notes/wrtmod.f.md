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

> **Question** ([[#L152]]; [[#L171]]). **The deprecated `.full` file.** YREC's Quick Start lists `.full` (`FMODPT`) as a deprecated output, and the test suite's namelists say "No longer used", but PARMIN still opens it (and writes the run's description to it), and WRTMOD (with `LSOUND`), [[checkj.f#CHECKJ|`CHECKJ`]] and [[seculr.f#SECULR|`SECULR`]] still write to it. Should these writes be removed, or should the documentation say what the file now holds?

**Changed since `rp_1`.** `CMIXL` and `XMSOL` are now arguments (`CMIXL` is passed on to `ENVINT`); the sound-speed file is written to the unit `ISOUND`, opened once by `PARMIN`, instead of being opened on unit 500 at each call, which settles part of question 1; declarations: COMMON blocks to modules, `IMPLICIT NONE`.

**Changed since `a8a5950`.** Version 3 of the pulsation model writes literal zeros in its three mixing-length columns, which held `PUALPHA_MOD`'s always-zero `VALFMLT`, `VPHMLT`, and `VCMXMLT` (now removed), so that readers of `IPVER` = 3 see the same layout; `PUALPHA_MOD` is no longer used here.

## Bugs, by priority

1. **(c)** **A typo in $d\rho/dr$.** ([[#L165-L168]]) `QDR2`, the $d\rho/dr$-like term at shell `I+1`, multiplies by `QPR1`, the $dP/dr$-like term at shell `I`, instead of `QPR2`, as `QDR1` does with `QPR1`. What follows: The written `QDR2`-based difference `QQDR` ([[#L170-L171]]) is wrong in the `.full` file (`IMODPT`); nothing reads it back. Only with `LSOUND`, which main.f sets for the last model of a run. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to use QPR2, the term at shell I+1, in QDR2.
                  QDR2 = EXP(CLN*(HD(I+1)-HP(I+1)))*PQDP(I+1)*QPR2
    ```

2. **(c)** **The pulsation model's shell list is never set.** ([[#L51]]; [[#L255-L256]]; [[#L265-L266]]) `IDM` and `ID(J)` are locals, never assigned (the "long block" removed by G. Somers 11/14, [[#L307]], or the arguments `LSHELL`, `JXBEG`, `JXEND`, removed since, may have set them). The header prints `IDM`, and the loop `DO 220 J = 1,IDM` uses undefined values. What follows: With the usual static, zero-filled storage of `SAVE`d locals, `IDM` = 0, so the pulsation model (`LPULSE` and `LSTORE`) has a header with "NUMBER OF SHELLS IN MODEL= 0" and no shells; with another value, `ID(J)` could index out of bounds. Only with `LPULSE` (off by default). Read from the code, not run. **A possible fix:** a choice for the developers: what shells the pulsation model should list (every shell, `IDM = M` and `ID(J) = J`, is the simplest), or whether the `LPULSE` output is still in use.

3. **(c)** **Debugging prints.** ([[#L127]]; [[#L131]]) `print*,'wrtmod LSOUND 1: '` writes to the screen at every call, and `print*,'wrtmod LSOUND 2: '` at every call with `LSOUND`. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to remove the two debugging prints of LSOUND.
          SAVE

          IF(LSOUND)THEN

    CFD 10/09 Add an extra output to plot the sound speed profile easyly
    ...
    ```

4. **(d)** **`LPRT` may be unset.** ([[#L186]]; [[envint.f#L206]]; [[envint.f#L222]]) `LPRT` is a local, set to true only if `LSTORE`, and never set false; otherwise `ENVINT` gets its `SAVE`d or undefined value, which decides whether it prints the envelope and atmosphere. With the usual zero-filled storage it is false, which matches the design (the pulsation model, too, needs `LSTORE`, [[#L273]]), so this is correct today but rests on the compiler. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to set LPRT on every call, not only when LSTORE.
           LPRT = LSTORE
    ```

### WRTMOD

Extra profiles of one model: sound-speed table, a reprinted envelope, and the pulsation model (whose shell list is currently undefined).
