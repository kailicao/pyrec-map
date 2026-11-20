## Explanation

**Purpose.** This file evaluates, at every point of the interior model, the four equations of stellar structure and their partial derivatives, and passes them to [REDUCE](https://github.com/yreclab/yrec/blob/7be4133/src/reduce.f#L6-L113), which builds the linearized (Henyey) system that [CRRECT](crrect.f.md#crrect) solves for the corrections. On the way it calls the physics (equation of state, opacity, temperature gradient, nuclear energy), totals the luminosity by source, and stores many per-point quantities for output and for other routines.

**How it fits.**
- **Inputs:** the arguments, the current model `HS` ($`\log m`$), `HR` ($`\log r`$), `HP` ($`\log P`$), `HT` ($`\log T`$), `HL` ($`L/L_\odot`$), `HD` ($`\log\rho`$), `HCOMP`; `HS1`, `HS2` (the mass $`m`$ at each point and the shell's mass $`\Delta m`$, in g; [STARIN](starin.f.md#starin), step 7); the changes over the step `HTT`, `HPP` ($`\Delta\log T`$, $`\Delta\log P`$) and `DELTS` (the time step, s); the rotational factors `FP`, `FT` and kinetic energies `HKEROT`, `HKEROTO`; `JENV`, `TEFFL`, `CMIXL` (the mixing length, passed on to TPGRAD). [`NMLPAR_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/nmlpar_mod.f#L32-L279) brings the options `LDH`, `LROT`, `LSNU`, `LPULSE`, the accretion switches `LMDOT`, `DMDT0` and the nuclear cut-off `TCUT(1)`; [`MASSCHG2_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/masschg2_mod.f#L19-L30) the accretion terms `DLOGT`, `DLOGP`.
- **Who calls it:** [CRRECT](crrect.f.md#crrect), at each iteration of the structure solution.
- **What it calls:** for each point, [EQSTAT](eqstat.f.md#eqstat) (the MHD equation of state, MEQOS, removed since `rp_1`); [GETOPAC](getopac.f.md#getopac); [TPGRAD](tpgrad.f.md#tpgrad) (the temperature gradient and convection); [ENGEB](engeb.f.md#engeb) (nuclear energy) above `TCUT(1)`, with `IU = IM` so that its per-point rates `HR1`… land at the right point, which also returns `EALPCA`, `ENU` and the $`^7`$Be mass fraction (unused here); and [REDUCE](https://github.com/yreclab/yrec/blob/7be4133/src/reduce.f#L6-L113) for each pair of points.
- **Outputs:**
  - the matrices `HHA`, `HHB`, `HMAX` (through REDUCE and the central conditions), `HHC` (the gravothermal energy per point), `LC` (convective or not), `HD` (density from the EOS);
  - `TLUMX(1:8)`, the luminosity by source in $`L_\odot`$: 1–5 the nuclear terms from ENGEB, 6 the neutrino term `ENU`, 7 gravothermal, 8 $`\alpha`$ captures (`EALPCA`); CRRECT renormalizes them;
  - per point, in [`SCRTCH_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/scrtch_mod.f#L19-L39): the nuclear total `SESUM` (the five ENGEB terms) and `SEG` (`SEG(1:5)` the fractions of `SESUM`, `SEG(6)` the neutrino term and `SEG(7)` the gravothermal term, both in $`\mathrm{erg\,g^{-1}\,s^{-1}}`$), $`\beta`$, $`\eta`$, opacity, the gradients $`\nabla_\mathrm{rad}`$, $`\nabla`$, $`\nabla_\mathrm{ad}`$, ionization fractions, convective velocity, $`c_P`$; read by 21 routines (output, mixing, diffusion);
  - `GAM1` in [`SOUND_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/sound_mod.f#L19-L31) ($`\Gamma_1`$); with rotation, `SQOT`, `SQET`, `FRACNUC` ($`(\mathtt{SESUM} - \mathtt{SEG(6)} - \mathtt{SEG(7)})/\mathtt{SESUM}`$) in [`ROTDER_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/rotder_mod.f#L19-L32) (for [SETUPV](https://github.com/yreclab/yrec/blob/7be4133/src/setupv.f#L3-L467)) and `DEROT` in [`ROTEN_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/roten_mod.f#L19-L30); for pulsation output, [`PULSE1_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/pulse1_mod.f#L19-L39); the solar neutrino fluxes `FLUXTOT` in [`FLUXES_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/fluxes_mod.f#L19-L29).

**The method.** With $`\ln m`$ as the independent variable and the code's variables in $`\log_{10}`$, the structure equations at each point are (the code's names in parentheses):
```math
\frac{d\ln r}{d\ln m} = \frac{m}{4\pi r^3\rho} \;(\mathtt{QR}), \qquad \frac{d\ln P}{d\ln m} = -\frac{G m^2}{4\pi r^4 P}\,f_P \;(\mathtt{QP}), \qquad \frac{d\ln T}{d\ln m} = \nabla\,\frac{d\ln P}{d\ln m} \;(\mathtt{QT}),
```
```math
\frac{d(L/L_\odot)}{d\log m} = \frac{\ln 10\; m}{L_\odot}\left(\epsilon_\mathrm{nuc} - \epsilon_\nu + \epsilon_\mathrm{grav} - \epsilon_\mathrm{rot}\right) \;(\mathtt{QL}),
```
where $`f_P`$ is the rotational correction (`FP`) and $`\nabla`$ the temperature gradient from TPGRAD. $`f_T`$ (`FT`) enters through $`\nabla`$: TPGRAD multiplies $`\nabla_\mathrm{rad}`$ by $`f_T/f_P`$ ([tpgrad.f, lines 80–81](https://github.com/yreclab/yrec/blob/7be4133/src/tpgrad.f#L80-L81)), so the radiative $`d\ln T/d\ln m`$ carries $`f_T`$ (settled from the code, Nov 9, 2026). The nuclear term is ENGEB's `SUM1`, which is net of the neutrino losses: above `TCUT(5)` [ENGEB](engeb.f.md#engeb) adds `ENU` $`= -\epsilon_\nu`$ to it (from the Itoh et al. [1996](https://ui.adsabs.harvard.edu/abs/1996ApJS..102..411I) fits with `LNULOS1`, otherwise from older fitting formulae), the same `ENU` that goes to `TLUMX(6)` and `SEG(6)`. Their derivatives with respect to $`\ln r`$, $`\ln P`$, $`\ln T`$ and $`L`$ follow; for example $`\partial\mathtt{QR}/\partial\ln r = -3\,\mathtt{QR}`$, $`\partial\mathtt{QP}/\partial\ln r = -4\,\mathtt{QP}`$, and $`\partial\mathtt{QR}/\partial\ln P = -\mathtt{QR}\,(\partial\ln\rho/\partial\ln P)_T`$. For the temperature gradient:
- **radiative:** $`\partial\mathtt{QT}/\partial\ln T = \mathtt{QT}\,(-4 + \kappa_T + \kappa_\rho\,\rho_T)`$, $`\partial\mathtt{QT}/\partial\ln P = \mathtt{QT}\,\kappa_\rho\,\rho_P`$, and a term in $`L`$, $`\mathtt{QT}/(L \ln 10)`$;
- **convective:** from TPGRAD's derivatives of $`\nabla`$ (`QACP`, `QACT`, `QACR`), with no dependence on $`L`$.

Here $`\kappa_T`$, $`\kappa_\rho`$ are `QOT`, `QOD` and $`\rho_T`$, $`\rho_P`$ are `QDT`, `QDP` ($`\partial\ln\rho/\partial\ln T`$ and $`\partial\ln\rho/\partial\ln P`$), locals that EQSTAT sets at each point.

> **Question** ([lines 156–160](https://github.com/yreclab/yrec/blob/7be4133/src/coefft.f#L156-L160); [lines 226–246](https://github.com/yreclab/yrec/blob/7be4133/src/coefft.f#L226-L246); [lines 253–254](https://github.com/yreclab/yrec/blob/7be4133/src/coefft.f#L253-L254)). **Rotation in $`d\ln P/dr`$.** The terms in $`d\ln f_P/d\ln r`$ and $`d\ln f_T/d\ln r`$ (`QFPR`, `QFTR`) are commented out ("MHP 10/02 not used"), so the derivatives treat $`f_P`$ and $`f_T`$ as constants. Is that accurate enough for fast rotators?

**Gravothermal energy.** With $`\Delta\log T`$, $`\Delta\log P`$ over the step:
```math
\epsilon_\mathrm{grav} = \frac{\ln 10}{\Delta t}\,\frac{P\rho_T}{\rho}\left(\frac{\Delta\log T}{\nabla_\mathrm{ad}} - \Delta\log P\right),
```
which, with $`\rho_T = -\delta`$ and $`c_P = P\delta/(\rho T\nabla_\mathrm{ad})`$, is the usual $`-c_P\,dT/dt + (\delta/\rho)\,dP/dt`$, without a term in $`d\mu/dt`$ (the question below). $`\Delta\log T`$, $`\Delta\log P`$ (`HTT`, `HPP`) are changes at fixed mass: [HPOINT](hpoint.f.md#hpoint) moves the mass points before the structure is solved (interpolating the model and the previous step's rates of change, `ENTROP_MOD`, onto the new points), main.f then starts `HTT`, `HPP` from zero (or from the extrapolated guess), CRRECT adds each correction to them, and no routine moves the points during the iteration. During accretion (`LMDOT`, `DMDT0 > 0`), points at and above `JENV` add `DLOGT`, `DLOGP` to the changes; `JENV` comes from CRRECT, which has it from MIX only at levels 3 and 4 (CRRECT's suspected bug 1, [crrect.f, suspected bug 1](crrect.f.md#b1)). With rotation, the change of rotational kinetic energy per gram per second is subtracted.

> **Question** ([lines 338–341](https://github.com/yreclab/yrec/blob/7be4133/src/coefft.f#L338-L341)). **$`\epsilon_\mathrm{grav}`$ without the composition term.** The formula used, $`-c_P\,dT/dt + (\delta/\rho)\,dP/dt`$, omits the term in $`d\mu/dt`$ of the full $`-T\,ds/dt`$ (Kippenhahn, Weigert & Weiss, §4.4), which matters where burning or settling changes $`\mu`$ quickly. A student would expect it in cores near hydrogen exhaustion. Is the neglect deliberate (for example because `HTT`, `HPP` are measured after MIX has changed the composition), and has its effect on solar models been checked?

> **Question** ([lines 165–170](https://github.com/yreclab/yrec/blob/7be4133/src/coefft.f#L165-L170); [line 337](https://github.com/yreclab/yrec/blob/7be4133/src/coefft.f#L337)). **A one-year floor on the time step.** `IF(HCOMP(1,IM).GT.0.01D0 .AND. DELTS.LT.TIME) DT = TIMEI`: where hydrogen is present and the step is shorter than a year (3.1558e7 s), $`\epsilon_\mathrm{grav}`$ uses $`1/(1\,\mathrm{yr})`$ instead of $`1/\Delta t`$. So for short steps $`\epsilon_\mathrm{grav}`$ is underestimated by the factor $`\Delta t/1\,\mathrm{yr}`$. What is this for? The year here is also hard-coded rather than taken from `CSECYR`.

> **Question** ([lines 360–367](https://github.com/yreclab/yrec/blob/7be4133/src/coefft.f#L360-L367)). **Accretion entropy.** A term for the entropy of accreted material (`QACC`) is commented out. Is accretion meant to change the energy equation only through `DLOGT`, `DLOGP`?

**The centre.** Point 1 gets the central boundary conditions: $`r^3 = 3m/(4\pi\rho)`$ in log form, and $`L = \epsilon\, m`$.

**$`\Gamma_1`$.** Always computed (JVS 01/11), by Cox and Giuli's relations: $`\chi_\rho = 1/\rho_P`$, $`\chi_T = -\chi_\rho\rho_T`$, $`c_V = c_P - (P/\rho T)\,\chi_T^2/\chi_\rho`$, $`\Gamma_1 = \chi_\rho c_P/c_V`$.

**Design.** The routine holds many options and outputs that grew over decades (the comments are dated from 1990 to 2012). It sets `LOCOND`, `LDERIV`, `LATMO`, `LMIX` (arguments) at every call.

**Changed since `rp_1`.** The MHD equation of state removed (EQSTAT always), which settles the former question on the Debye–Hückel composition being set only without it; the new argument `CMIXL`, passed on to TPGRAD; `EALPCA`, `ENU` and the $`^7`$Be mass fraction returned by ENGEB (`/NEWEPS/` retired); the write-only `SQOD`, `SQED` and the write-only opacity indices `IDT`, `IDD` (`/OPTAB/`) no longer set; COMMON blocks to modules, `IMPLICIT NONE`.

**Changed since `a8a5950`.** `QDT` and `QDP` are locals instead of arguments, since EQSTAT sets them at each point before they are read; the derivatives of $`\epsilon_\mathrm{grav}`$ with respect to $`\log P`$ and $`\log T`$ (`QLP`, `QLT`) divide `QDTP` and `QDTT` by `QDT`, since $`\epsilon_\mathrm{grav}`$ carries the factor $`\rho_T`$ (`QDT`) and `QDTP`, `QDTT` are derivatives of $`\rho_T`$, not of its logarithm (only the Jacobian changes, not the residual); the derivatives of the nuclear energy `QED`, `QET` are zeroed below `TCUT(1)`, where they used to keep the last burning shell's values, which reached `SQET` and the pulsation arrays; the never-read $`^3`$He luminosities `UMHE33`, `UMHEAL` and the copies `VALFMLT`, `VPHMLT`, `VCMXMLT` of TPGRAD's always-zero `ALFMLT`, `PHMLT`, `CMXMLT` are no longer set, so `GRAB_MOD` (removed since `a8a5950`) and `PUALPHA_MOD` are no longer used.

## Bugs, by priority

1. **(never occurred)** **The nuclear terms at exactly `TCUT(1)`.** ([line 281](https://github.com/yreclab/yrec/blob/7be4133/src/coefft.f#L281); [line 416](https://github.com/yreclab/yrec/blob/7be4133/src/coefft.f#L416); [lines 425–427](https://github.com/yreclab/yrec/blob/7be4133/src/coefft.f#L425-L427)) ENGEB is called, and `EG(1..6)` set, only where `TL.GT.TCUT(1)`, but the store into `SESUM` and `SEG` is skipped only where `HT(IM).LT.TCUT(1)`. At a shell with $`\log T`$ exactly equal to `TCUT(1)`, `SESUM` and `SEG(1..6)` get the previous shell's `EG` (or values from an earlier call), while `QL` has no nuclear term there. Correct today in practice, since an exact equality of a real is unlikely, but the two tests disagree.

    **A possible fix:**

    ```diff
    --- a/src/coefft.f
    +++ b/src/coefft.f
    @@ -413,7 +413,10 @@
     C MHP 10/02 LSHORT NOT USED, OMIT
     C         LSHORT = .NOT.LONG .AND. MOD(MODEL,NPRT1).EQ.0
     C  ZERO OUT NUCLEAR ENERGY TERMS IF T < NUCLEAR CUTOFF.
    -         IF(HT(IM).LT.TCUT(1)) THEN
    +C 11/09/26 KC via Claude
    +C code changed to skip the nuclear terms with the same test as the
    +C call to ENGEB.
    +         IF(HT(IM).LE.TCUT(1)) THEN
                 SESUM(IM) = 0.0D0
                 SEG(7,IM) = HHC(IM)
                 DO J = 1,6
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The store of the nuclear terms ran in 33 of 34 runs (26 of YREC's cases, from a $`0.04\,M_\odot`$ brown dwarf and the solar models to $`9\,M_\odot`$, rotation, and helium burning, and 8 made-up ones; one of these, with `FCORE` = 1.0, stopped in its first second), from 49,743 to about 72 million times each, at $`\log T`$ = 5.5 to 8.40 and shells 1 to 3239; $`\log T`$ never equaled `TCUT(1)` exactly, so the two tests never disagreed and results are unchanged today. No fix was run. Intent: The comment above the test, "ZERO OUT NUCLEAR ENERGY TERMS IF T < NUCLEAR CUTOFF.," matches the `.LT.` and says nothing of the equal case.

### COEFFT

For each point: EOS, opacity, temperature gradient and nuclear energy; the structure equations and their derivatives, passed to [REDUCE](https://github.com/yreclab/yrec/blob/7be4133/src/reduce.f#L6-L113) (central conditions at point 1); luminosity totals by source; per-point physics stored for output and other routines.
