## Explanation

**Purpose.** This file evaluates, at every point of the interior model, the four equations of stellar structure and their partial derivatives, and passes them to [[reduce.f#REDUCE|REDUCE]], which builds the linearized (Henyey) system that [[crrect.f#CRRECT|CRRECT]] solves for the corrections. On the way it calls the physics (equation of state, opacity, temperature gradient, nuclear energy), totals the luminosity by source, and stores many per-point quantities for output and for other routines.

**How it fits.**
- **Inputs:** the arguments, the current model `HS` ($\log m$), `HR` ($\log r$), `HP` ($\log P$), `HT` ($\log T$), `HL` ($L/L_\odot$), `HD` ($\log\rho$), `HCOMP`; `HS1`, `HS2` (the mass $m$ at each point and the shell's mass $\Delta m$, in g; [[starin.f#STARIN|STARIN]], step 7); the changes over the step `HTT`, `HPP` ($\Delta\log T$, $\Delta\log P$) and `DELTS` (the time step, s); the rotational factors `FP`, `FT` and kinetic energies `HKEROT`, `HKEROTO`; `JENV`, `TEFFL`, `CMIXL` (the mixing length, passed on to TPGRAD). [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] brings the options `LDH`, `LROT`, `LSNU`, `LPULSE`, the accretion switches `LMDOT`, `DMDT0` and the nuclear cut-off `TCUT(1)`; [[masschg2_mod.f#MASSCHG2_MOD|`MASSCHG2_MOD`]] the accretion terms `DLOGT`, `DLOGP`.
- **Who calls it:** [[crrect.f#CRRECT|CRRECT]], at each iteration of the structure solution.
- **What it calls:** for each point, [[eqstat.f#EQSTAT|EQSTAT]] (the MHD equation of state, MEQOS, removed since `rp_1`); [[getopac.f#GETOPAC|GETOPAC]]; [[tpgrad.f#TPGRAD|TPGRAD]] (the temperature gradient and convection); [[engeb.f#ENGEB|ENGEB]] (nuclear energy) above `TCUT(1)`, with `IU = IM` so that its per-point rates `HR1`… land at the right point, which also returns `EALPCA`, `ENU` and the $^7$Be mass fraction (unused here); and [[reduce.f#REDUCE|REDUCE]] for each pair of points.
- **Outputs:**
  - the matrices `HHA`, `HHB`, `HMAX` (through REDUCE and the central conditions), `HHC` (the gravothermal energy per point), `LC` (convective or not), `HD` (density from the EOS);
  - `TLUMX(1:8)`, the luminosity by source in $L_\odot$: 1–5 the nuclear terms from ENGEB, 6 the neutrino term `ENU`, 7 gravothermal, 8 alpha captures (`EALPCA`); CRRECT renormalizes them;
  - per point, in [[scrtch_mod.f#SCRTCH_MOD|`SCRTCH_MOD`]]: the nuclear total `SESUM` (the five ENGEB terms) and `SEG` (`SEG(1:5)` the fractions of `SESUM`, `SEG(6)` the neutrino term and `SEG(7)` the gravothermal term, both in erg g$^{-1}$ s$^{-1}$), $\beta$, $\eta$, opacity, the gradients $\nabla_\mathrm{rad}$, $\nabla$, $\nabla_\mathrm{ad}$, ionization fractions, convective velocity, $c_P$; read by 21 routines (output, mixing, diffusion);
  - `GAM1` in [[sound_mod.f#SOUND_MOD|`SOUND_MOD`]] ($\Gamma_1$); with rotation, `SQOT`, `SQET`, `FRACNUC` ($(\mathtt{SESUM} - \mathtt{SEG(6)} - \mathtt{SEG(7)})/\mathtt{SESUM}$) in [[rotder_mod.f#ROTDER_MOD|`ROTDER_MOD`]] (for [[setupv.f#SETUPV|SETUPV]]) and `DEROT` in [[roten_mod.f#ROTEN_MOD|`ROTEN_MOD`]]; for pulsation output, [[pulse1_mod.f#PULSE1_MOD|`PULSE1_MOD`]]; the solar neutrino fluxes `FLUXTOT` in [[fluxes_mod.f#FLUXES_MOD|`FLUXES_MOD`]].

**The method.** With $\ln m$ as the independent variable and the code's variables in $\log_{10}$, the structure equations at each point are (the code's names in parentheses):
$$\frac{d\ln r}{d\ln m} = \frac{m}{4\pi r^3\rho} \;(\mathtt{QR}), \qquad \frac{d\ln P}{d\ln m} = -\frac{G m^2}{4\pi r^4 P}\,f_P \;(\mathtt{QP}), \qquad \frac{d\ln T}{d\ln m} = \nabla\,\frac{d\ln P}{d\ln m} \;(\mathtt{QT}),$$
$$\frac{d(L/L_\odot)}{d\log m} = \frac{\ln 10\; m}{L_\odot}\left(\epsilon_\mathrm{nuc} - \epsilon_\nu + \epsilon_\mathrm{grav} - \epsilon_\mathrm{rot}\right) \;(\mathtt{QL}),$$
where $f_P$ is the rotational correction (`FP`) and $\nabla$ the temperature gradient from TPGRAD. $f_T$ (`FT`) enters through $\nabla$: TPGRAD multiplies $\nabla_\mathrm{rad}$ by $f_T/f_P$ ([[tpgrad.f#L80-L81]]), so the radiative $d\ln T/d\ln m$ carries $f_T$ (settled from the code, Nov 9, 2026). The nuclear term is ENGEB's `SUM1`, which is net of the neutrino losses: above `TCUT(5)` [[engeb.f#ENGEB|ENGEB]] adds `ENU` $= -\epsilon_\nu$ to it (from the Itoh et al. 1996 fits with `LNULOS1`, otherwise from older fitting formulae), the same `ENU` that goes to `TLUMX(6)` and `SEG(6)`. Their derivatives with respect to $\ln r$, $\ln P$, $\ln T$ and $L$ follow; for example $\partial\mathtt{QR}/\partial\ln r = -3\,\mathtt{QR}$, $\partial\mathtt{QP}/\partial\ln r = -4\,\mathtt{QP}$, and $\partial\mathtt{QR}/\partial\ln P = -\mathtt{QR}\,(\partial\ln\rho/\partial\ln P)_T$. For the temperature gradient:
- **radiative:** $\partial\mathtt{QT}/\partial\ln T = \mathtt{QT}\,(-4 + \kappa_T + \kappa_\rho\,\rho_T)$, $\partial\mathtt{QT}/\partial\ln P = \mathtt{QT}\,\kappa_\rho\,\rho_P$, and a term in $L$, $\mathtt{QT}/(L \ln 10)$;
- **convective:** from TPGRAD's derivatives of $\nabla$ (`QACP`, `QACT`, `QACR`), with no dependence on $L$.

Here $\kappa_T$, $\kappa_\rho$ are `QOT`, `QOD` and $\rho_T$, $\rho_P$ are `QDT`, `QDP` ($\partial\ln\rho/\partial\ln T$ and $\partial\ln\rho/\partial\ln P$), locals that EQSTAT sets at each point.

> **Question** ([[#L156-L160]]; [[#L226-L246]]; [[#L253-L254]]). **Rotation in $d\ln P/dr$.** The terms in $d\ln f_P/d\ln r$ and $d\ln f_T/d\ln r$ (`QFPR`, `QFTR`) are commented out ("MHP 10/02 not used"), so the derivatives treat $f_P$ and $f_T$ as constants. Is that accurate enough for fast rotators?

**Gravothermal energy.** With $\Delta\log T$, $\Delta\log P$ over the step:
$$\epsilon_\mathrm{grav} = \frac{\ln 10}{\Delta t}\,\frac{P\rho_T}{\rho}\left(\frac{\Delta\log T}{\nabla_\mathrm{ad}} - \Delta\log P\right),$$
which, with $\rho_T = -\delta$ and $c_P = P\delta/(\rho T\nabla_\mathrm{ad})$, is the usual $-c_P\,dT/dt + (\delta/\rho)\,dP/dt$, without a term in $d\mu/dt$ (the question below). $\Delta\log T$, $\Delta\log P$ (`HTT`, `HPP`) are changes at fixed mass: [[hpoint.f#HPOINT|HPOINT]] moves the mass points before the structure is solved (interpolating the model and the previous step's rates of change, `ENTROP_MOD`, onto the new points), main.f then starts `HTT`, `HPP` from zero (or from the extrapolated guess), CRRECT adds each correction to them, and no routine moves the points during the iteration. During accretion (`LMDOT`, `DMDT0 > 0`), points at and above `JENV` add `DLOGT`, `DLOGP` to the changes; `JENV` comes from CRRECT, which has it from MIX only at levels 3 and 4 (CRRECT's suspected bug 1, [[crrect.f#b1]]). With rotation, the change of rotational kinetic energy per gram per second is subtracted.

> **Question** ([[#L338-L341]]). **$\epsilon_\mathrm{grav}$ without the composition term.** The formula used, $-c_P\,dT/dt + (\delta/\rho)\,dP/dt$, omits the term in $d\mu/dt$ of the full $-T\,ds/dt$ (Kippenhahn, Weigert & Weiss, §4.4), which matters where burning or settling changes $\mu$ quickly. A student would expect it in cores near hydrogen exhaustion. Is the neglect deliberate (for example because `HTT`, `HPP` are measured after MIX has changed the composition), and has its effect on solar models been checked?

> **Question** ([[#L165-L170]]; [[#L337]]). **A one-year floor on the time step.** `IF(HCOMP(1,IM).GT.0.01D0 .AND. DELTS.LT.TIME) DT = TIMEI`: where hydrogen is present and the step is shorter than a year (3.1558e7 s), $\epsilon_\mathrm{grav}$ uses $1/(1\,\mathrm{yr})$ instead of $1/\Delta t$. So for short steps $\epsilon_\mathrm{grav}$ is underestimated by the factor $\Delta t/1\,\mathrm{yr}$. What is this for? The year here is also hard-coded rather than taken from `CSECYR`.

> **Question** ([[#L360-L367]]). **Accretion entropy.** A term for the entropy of accreted material (`QACC`) is commented out. Is accretion meant to change the energy equation only through `DLOGT`, `DLOGP`?

**The centre.** Point 1 gets the central boundary conditions: $r^3 = 3m/(4\pi\rho)$ in log form, and $L = \epsilon\, m$.

**$\Gamma_1$.** Always computed (JVS 01/11), by Cox and Giuli's relations: $\chi_\rho = 1/\rho_P$, $\chi_T = -\chi_\rho\rho_T$, $c_V = c_P - (P/\rho T)\,\chi_T^2/\chi_\rho$, $\Gamma_1 = \chi_\rho c_P/c_V$.

**Design.** The routine holds many options and outputs that grew over decades (the comments are dated from 1990 to 2012). It sets `LOCOND`, `LDERIV`, `LATMO`, `LMIX` (arguments) at every call.

**Changed since `rp_1`.** The MHD equation of state removed (EQSTAT always), which settles the former question on the Debye–Hückel composition being set only without it; the new argument `CMIXL`, passed on to TPGRAD; `EALPCA`, `ENU` and the $^7$Be mass fraction returned by ENGEB (`/NEWEPS/` retired); the write-only `SQOD`, `SQED` and the write-only opacity indices `IDT`, `IDD` (`/OPTAB/`) no longer set; COMMON blocks to modules, `IMPLICIT NONE`.

**Changed since `a8a5950`.** `QDT` and `QDP` are locals instead of arguments, since EQSTAT sets them at each point before they are read; the derivatives of $\epsilon_\mathrm{grav}$ with respect to $\log P$ and $\log T$ (`QLP`, `QLT`) divide `QDTP` and `QDTT` by `QDT`, since $\epsilon_\mathrm{grav}$ carries the factor $\rho_T$ (`QDT`) and `QDTP`, `QDTT` are derivatives of $\rho_T$, not of its logarithm (only the Jacobian changes, not the residual); the derivatives of the nuclear energy `QED`, `QET` are zeroed below `TCUT(1)`, where they used to keep the last burning shell's values, which reached `SQET` and the pulsation arrays; the never-read $^3$He luminosities `UMHE33`, `UMHEAL` and the copies `VALFMLT`, `VPHMLT`, `VCMXMLT` of TPGRAD's always-zero `ALFMLT`, `PHMLT`, `CMXMLT` are no longer set, so `GRAB_MOD` (removed since `a8a5950`) and `PUALPHA_MOD` are no longer used.

## Bugs, by priority

1. **(d)** **The nuclear terms at exactly `TCUT(1)`.** ([[#L281]]; [[#L416]]; [[#L425-L427]]) ENGEB is called, and `EG(1..6)` set, only where `TL.GT.TCUT(1)`, but the store into `SESUM` and `SEG` is skipped only where `HT(IM).LT.TCUT(1)`. At a shell with $\log T$ exactly equal to `TCUT(1)`, `SESUM` and `SEG(1..6)` get the previous shell's `EG` (or values from an earlier call), while `QL` has no nuclear term there. Correct today in practice, since an exact equality of a real is unlikely, but the two tests disagree. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to skip the nuclear terms with the same test as the
    C call to ENGEB.
             IF(HT(IM).LE.TCUT(1)) THEN
    ```

### COEFFT

For each point: EOS, opacity, temperature gradient and nuclear energy; the structure equations and their derivatives, passed to [[reduce.f#REDUCE|REDUCE]] (central conditions at point 1); luminosity totals by source; per-point physics stored for output and other routines.
