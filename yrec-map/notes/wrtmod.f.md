## Explanation

**Purpose.** `WRTMOD` writes extra profiles of one model: with `LSOUND`, a sound-speed and structure table (to the units `IMODPT` and `ISOUND`, the file `Csound.dat`); with `LSTATM`, `LSTENV` or `LPULSE`, an envelope integrated again for printing; and with `LPULSE`, a model for pulsation codes on `IOPMOD`, in one of three versions (`IPVER`).

**How it fits.**
- **Inputs:** the model (arguments: `M`, `JENV`, `HCOMP`, `HS1`, $\log\rho$, $L$, $\log P$, $\log r$, $\log T$, `MODEL`, $\log L$, $\log T_\mathrm{eff}$, `FP`, `FT`, $\log m$ `HS`, the age, the mixing length `CMIXL` and the star's mass `XMSOL`, a snapshot of `SMASS` taken by the main program), and through modules the per-shell physics: $\Gamma_1$ and the switch `LSOUND` (`SOUND_MOD`), the pulsation derivatives `PQDP`, `PQDT`, … (`PULSE1_MOD`), energy rates, opacity and gradients (`SCRTCH_MOD`), the MLT quantities (`PUALPHA_MOD`, which [[tpgrad.f|tpgrad.f]] sets to zero), `STOTAL` (`COMP_MOD`), and the namelist switches and integration steps (`LSTORE`, `LSTATM`, `LSTENV`, `LPULSE`, `IPVER`, `SPOTF`, `SPOTX`, `ATMSTP`, `ENVSTP`, … in `NMLPAR_MOD`; formerly `CCOUT`, `PULSE`, `SPOTS`, `ENVGEN`, `INTATM`, `INTENV`).
- **Who calls it:** [[putstore.f#PUTSTORE|PUTSTORE]] (when the atmosphere or envelope is stored) and [[wrtout.f#WRTOUT|WRTOUT]] (for pulsation output between stored models).
- **What it calls:** [[envint.f#ENVINT|ENVINT]], which itself prints the envelope and atmosphere (and the pulsation envelope with `LPULPT`).
- **Outputs:** `IMODPT`, `ISOUND` (the file `FSOUND`, `Csound.dat` by default, opened once by [[parmin.f#PARMIN|PARMIN]]), `IOPMOD`, and the envelope printed by `ENVINT`.

**The method.**
1. **Sound speed** (`LSOUND`). For each shell, with $V = G m \rho/(P r)$ and $U = 4\pi\rho r^3/m$: $r/R_\odot$, $m/M_\odot$, $m/r^3$ (solar units), $V/\Gamma_1$, $\Gamma_1$,
   $$A = -V/\Gamma_1 + V\left(\frac{\partial\ln\rho}{\partial\ln P} + \nabla\,\frac{\partial\ln\rho}{\partial\ln T}\right)$$
   (the code's `XX4`; probably the buoyancy term, by its form), $U$, and $c_s = \sqrt{\Gamma_1 P/\rho}$ in km/s. Between shells it also writes $dP/dr$-like and $d\rho/dr$-like terms (`QPR`, `QDR`) and their differences scaled by $\Gamma_1 P\,\Delta r$ and $\rho\,\Delta r$.
2. **Envelope.** The integration steps are set to the output steps, `ENVINT` integrates from the surface to the last shell's pressure (for a spotted star at the ambient temperature, as in [[starin.f|starin.f]]), and the steps are restored afterwards.
3. **Pulsation model** (`LPULSE`). A header (`LPULSE` alone), then, only when both `LPULSE` and `LSTORE` are set, for each shell in the list `ID(1..IDM)`: $\log r$, $m/M$, $L$, $\log T$, $\log\rho$, $\log P$, $\varepsilon$, $\kappa$ and the derivatives, in format 1, 2 or 3 (version 3 adds the MLT quantities).

**KC's changes.** Removed the unused arguments `LSHELL`, `JXBEG`, `JXEND`, `JCORE`, `LC`, `OMEGA`, `ETA2`, `R0`, `HJM` and `HI` (2025-05-31); removed `DATA IHEADR/4H****/`, which drew compiler warnings (2025-05-30).

**Changed since `rp_1`.** `CMIXL` and `XMSOL` are now arguments (`CMIXL` is passed on to `ENVINT`); the sound-speed file is written to the unit `ISOUND`, opened once by `PARMIN`, instead of being opened on unit 500 at each call, which settles part of question 4; declarations: COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **The pulsation model's shell list is never set.** `IDM` and `ID(J)` are local and never assigned (the "long block" removed by G. Somers 11/14, or the arguments `LSHELL`, `JXBEG`, `JXEND`, may have set them). The header prints `IDM`, and the loop `DO 220 J = 1,IDM` uses undefined values. Is the pulsation output (`LPULSE`) still in use, and what should choose its shells?
2. **A typo in $d\rho/dr$.** `QDR2` multiplies by `QPR1` instead of `QPR2`.
3. **Debugging prints.** `print*,'wrtmod LSOUND 1: '` (and `2`) write to the screen at every call.
4. **`Csound.dat`'s header.** The header line is written again at every call, so a run that writes several models repeats it between their tables.
5. **`LPRT` may be unset.** `LPRT` is set to true only if `LSTORE`; otherwise `ENVINT` gets its `SAVE`d or undefined value.

### WRTMOD

Extra profiles of one model: sound-speed table, a reprinted envelope, and the pulsation model (whose shell list is currently undefined).
