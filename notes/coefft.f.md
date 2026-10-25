## Explanation

**Purpose.** This file evaluates, at every point of the interior model, the four equations of stellar structure and their partial derivatives, and passes them to [[reduce.f#REDUCE|REDUCE]], which builds the linearized (Henyey) system that [[crrect.f#CRRECT|CRRECT]] solves for the corrections. On the way it calls the physics (equation of state, opacity, temperature gradient, nuclear energy), totals the luminosity by source, and stores many per-point quantities for output and for other routines.

**How it fits.**
- **Inputs:** the arguments, the current model `HS` ($\log m$), `HR` ($\log r$), `HP` ($\log P$), `HT` ($\log T$), `HL` ($L/L_\odot$), `HD` ($\log\rho$), `HCOMP`; `HS1`, `HS2` (the mass at each point and in each shell, in g, probably); the changes over the step `HTT`, `HPP` ($\Delta\log T$, $\Delta\log P$) and `DELTS` (the time step, s); the rotational factors `FP`, `FT` and kinetic energies `HKEROT`, `HKEROTO`; `JENV`, `TEFFL`. COMMON blocks bring the options: `LMHD` (`/MHD/`), `LDH` (`/DEBHU/`), `LROT` (`/ROT/`), `LSNU` (`/NEWENG/`), `LPULSE` (`/PULSE/`), the accretion terms in `/MASSCHG/`, `/MASSCHG2/`, and the nuclear cut-off `TCUT(1)` (`/CTLIM/`).
- **Who calls it:** [[crrect.f#CRRECT|CRRECT]], at each iteration of the structure solution.
- **What it calls:** for each point, [[meqos.f#MEQOS|MEQOS]] (the MHD equation of state) or [[eqstat.f#EQSTAT|EQSTAT]]; [[getopac.f#GETOPAC|GETOPAC]]; [[tpgrad.f#TPGRAD|TPGRAD]] (the temperature gradient and convection); [[engeb.f#ENGEB|ENGEB]] (nuclear energy) above `TCUT(1)`, with `IU = IM` so that its per-point rates `HR1`… land at the right point; and [[reduce.f#REDUCE|REDUCE]] for each pair of points.
- **Outputs:**
  - the matrices `HHA`, `HHB`, `HMAX` (through REDUCE and the central conditions), `HHC` (the gravothermal energy per point), `LC` (convective or not), `HD` (density from the EOS), `QDT`, `QDP`;
  - `TLUMX(1:8)`, the luminosity by source in $L_\odot$: 1–5 the nuclear terms from ENGEB, 6 the neutrino term `ENU`, 7 gravothermal, 8 alpha captures (`EALPCA`); CRRECT renormalizes them;
  - per point, in `/SCRTCH/`: the nuclear total `SESUM` (the five ENGEB terms) and `SEG` (`SEG(1:5)` the fractions of `SESUM`, `SEG(6)` the neutrino term and `SEG(7)` the gravothermal term, both in erg g$^{-1}$ s$^{-1}$), $\beta$, $\eta$, opacity, the gradients $\nabla_\mathrm{rad}$, $\nabla$, $\nabla_\mathrm{ad}$, ionization fractions, convective velocity, $c_P$; read by 21 routines (output, mixing, diffusion);
  - `GAM1` in `/SOUND/` ($\Gamma_1$); with rotation, `SQOD`, `SQOT`, `SQED`, `SQET`, `FRACNUC` ($(\mathtt{SESUM} - \mathtt{SEG(6)} - \mathtt{SEG(7)})/\mathtt{SESUM}$) in `/ROTDER/` (for [[setupv.f#SETUPV|SETUPV]]) and `DEROT` in `/ROTEN/`; for pulsation output, `/PULSE1/` and `/PUALPHA/`; the solar neutrino fluxes `FLUXTOT` in `/FLUXES/`; the $^3$He luminosities `UMHE33`, `UMHEAL` in `/GRAB/` (JVS 10/11).

**The method.** With $\ln m$ as the independent variable and the code's variables in $\log_{10}$, the structure equations at each point are (the code's names in parentheses):
$$\frac{d\ln r}{d\ln m} = \frac{m}{4\pi r^3\rho} \;(\mathtt{QR}), \qquad \frac{d\ln P}{d\ln m} = -\frac{G m^2}{4\pi r^4 P}\,f_P \;(\mathtt{QP}), \qquad \frac{d\ln T}{d\ln m} = \nabla\,\frac{d\ln P}{d\ln m} \;(\mathtt{QT}),$$
$$\frac{d(L/L_\odot)}{d\log m} = \frac{\ln 10\; m}{L_\odot}\left(\epsilon_\mathrm{nuc} + \epsilon_\mathrm{grav} - \epsilon_\mathrm{rot}\right) \;(\mathtt{QL}),$$
where $f_P$ is the rotational correction (`FP`) and $\nabla$ the temperature gradient from TPGRAD. Their derivatives with respect to $\ln r$, $\ln P$, $\ln T$ and $L$ follow; for example $\partial\mathtt{QR}/\partial\ln r = -3\,\mathtt{QR}$, $\partial\mathtt{QP}/\partial\ln r = -4\,\mathtt{QP}$, and $\partial\mathtt{QR}/\partial\ln P = -\mathtt{QR}\,(\partial\ln\rho/\partial\ln P)_T$. For the temperature gradient:
- **radiative:** $\partial\mathtt{QT}/\partial\ln T = \mathtt{QT}\,(-4 + \kappa_T + \kappa_\rho\,\rho_T)$, $\partial\mathtt{QT}/\partial\ln P = \mathtt{QT}\,\kappa_\rho\,\rho_P$, and a term in $L$, $\mathtt{QT}/(L \ln 10)$;
- **convective:** from TPGRAD's derivatives of $\nabla$ (`QACP`, `QACT`, `QACR`), with no dependence on $L$.

Here $\kappa_T$, $\kappa_\rho$ are `QOT`, `QOD` and $\rho_T$, $\rho_P$ are `QDT`, `QDP` ($\partial\ln\rho/\partial\ln T$ and $\partial\ln\rho/\partial\ln P$).

**Gravothermal energy.** With $\Delta\log T$, $\Delta\log P$ over the step:
$$\epsilon_\mathrm{grav} = \frac{\ln 10}{\Delta t}\,\frac{P\rho_T}{\rho}\left(\frac{\Delta\log T}{\nabla_\mathrm{ad}} - \Delta\log P\right),$$
which, with $\rho_T = -\delta$ and $c_P = P\delta/(\rho T\nabla_\mathrm{ad})$, is the usual $-c_P\,dT/dt + (\delta/\rho)\,dP/dt$. During accretion (`LMDOT`, `DMDT0 > 0`), points at and above `JENV` add `DLOGT`, `DLOGP` to the changes; `JENV` comes from CRRECT, which has it from MIX only at levels 3 and 4 (CRRECT's question 5). With rotation, the change of rotational kinetic energy per gram per second is subtracted.

**The centre.** Point 1 gets the central boundary conditions: $r^3 = 3m/(4\pi\rho)$ in log form, and $L = \epsilon\, m$.

**$\Gamma_1$.** Always computed (JVS 01/11), by Cox and Giuli's relations: $\chi_\rho = 1/\rho_P$, $\chi_T = -\chi_\rho\rho_T$, $c_V = c_P - (P/\rho T)\,\chi_T^2/\chi_\rho$, $\Gamma_1 = \chi_\rho c_P/c_V$.

**Design.** The routine holds many options and outputs that grew over decades (the comments are dated from 1990 to 2012). It sets `LOCOND`, `LDERIV`, `LATMO`, `LMIX` (arguments) and the opacity search indices `IDT = 15`, `IDD = 5` (`/OPTAB/`) at every call.

**KC's changes.** 2025-05-31: the unused argument `MODEL` removed; the call to MEQOS no longer passes `LDERIV`, `LATMO`, `KSAHA`; the call to ENGEB drops the unused arguments (`Z`, `XN15`, `XO17`, `XLI6`, `XLI7`, `XBE9` and others).

## Questions for the experts

1. **A one-year floor on the time step.** `IF(HCOMP(1,IM).GT.0.01D0 .AND. DELTS.LT.TIME) DT = TIMEI`: where hydrogen is present and the step is shorter than a year (3.1558e7 s), $\epsilon_\mathrm{grav}$ uses $1/(1\,\mathrm{yr})$ instead of $1/\Delta t$. So for short steps $\epsilon_\mathrm{grav}$ is underestimated by the factor $\Delta t/1\,\mathrm{yr}$. What is this for? The year here is also hard-coded rather than taken from `CSECYR`.
2. **Rotation in $d\ln P/dr$.** The terms in $d\ln f_P/d\ln r$ and $d\ln f_T/d\ln r$ (`QFPR`, `QFTR`) are commented out ("MHP 10/02 not used"), so the derivatives treat $f_P$ and $f_T$ as constants. Is that accurate enough for fast rotators?
3. **$f_T$ unused.** $f_P$ multiplies `QP`, but $f_T$ enters only through TPGRAD; is that the intended form of the rotating structure equations?
4. **Debye–Hückel only with EQSTAT.** The Debye–Hückel composition (`ZDH`, `XXDH`, …) is set only when the MHD EOS is off. Is that because the MHD EOS includes it?
5. **Accretion entropy.** A term for the entropy of accreted material (`QACC`) is commented out. Is accretion meant to change the energy equation only through `DLOGT`, `DLOGP`?

### COEFFT

For each point: EOS, opacity, temperature gradient and nuclear energy; the structure equations and their derivatives, passed to [[reduce.f#REDUCE|REDUCE]] (central conditions at point 1); luminosity totals by source; per-point physics stored for output and other routines.
