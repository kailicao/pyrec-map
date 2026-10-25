## Explanation

**Purpose.** `EQRELV` is the equation of state for fully ionized gas with partially degenerate, possibly relativistic electrons. Given $\log T$ and $\log P$, it finds the density whose total pressure (ions, electrons and radiation, plus an optional Debye–Hückel correction) equals $P$, and then the thermodynamic derivatives the structure equations need. The comment points to "Prather's thesis" for details.

**How it fits.**
- **Who calls it:** only [[eqstat2.f#EQSTAT2|EQSTAT2]]: alone where the gas is fully ionized ($\log T \ge$ `TSCUT`), and blended with the Saha solution ([[eqsaha.f#EQSAHA|EQSAHA]]) in a transition band below that.
- **Inputs:** `TL`, `PL` ($\log_{10}$ of T and P), `BETA` ($P_\mathrm{gas}/P$), `AMU` (ions per unit mass, in units of $1/m_\mathrm{H}$), `EMU` (electrons per unit mass, same units); `DL` is the starting guess.
- **Outputs:** density `DL`, `D`; electron degeneracy `ETA`; and the derivatives: `QDT` $=\partial\ln\rho/\partial\ln T$, `QDP` $=\partial\ln\rho/\partial\ln P$, `QCP` ($c_P$), `DELA` ($\nabla_\mathrm{ad}$), and their logarithmic derivatives `QDTT`, `QDTP`, `QCPT`, `QCPP`, `QAT`, `QAP`.
- **COMMON blocks:** `/CCR/` holds the electron (Fermi) table `DTABLE`, its abscissae `DVAL`, the degeneracy `ETAT8` and an index table `IDEN`; it is shared only with [[setups.f#SETUPS|SETUPS]], which reads it from the Fermi-table file (unit `IFERMI`) and builds `IDEN`. `/DEBHU/` holds the Debye–Hückel constants (`CDH`, the ramp limits `ETADH0`, `ETADH1`, the composition and the flag `LDH`); the callers of the equation of state (PHYSIC, COEFFT, CRRECT, SCONVEC, HSUBP, [[getnewenv.f#GETNEWENV|GETNEWENV]], STARIN, WRTMOD, WRTOUT) set its composition `XXDH`, `YYDH`, `ZZDH`, `ZDH` from the shell's `HCOMP` before each call. `/CONST1/`, `/CONST2/` hold constants ($\ln 10$ = `CLN`, $R$ = `CGAS`); `/LUOUT/` the output unit.

**The method.**
1. **Table lookup.** The electron pressure is tabulated as a function of $x = \log\rho + \log\mu_e^{-1} - \tfrac32\log T$ and $y = \log T$ (columns of `DTABLE`: $\log P_e$, $\log U_e$, and derivatives). The code interpolates with three points in each direction: Newton (equal spacing) in $y$, column $j$ at $\log T = 5 + 0.2j$, so the 20 columns span $\log T = 5.2$ to 9.0; Lagrange in $x$ (unequal spacing).
2. **Pressure balance.** With $P_\mathrm{rad} = (1-\beta)P$ and $P_\mathrm{ion} = R\mu_\mathrm{ion}^{-1}\rho T$ (`PA` = `CGAS*AMU*T*D`),
$$P_\mathrm{tot}(\rho) = P_\mathrm{ion} + P_e + P_\mathrm{rad}\;(+\,P_\mathrm{DH}),\qquad P_\mathrm{DH} = C_\mathrm{DH}\,c_\mathrm{mix}\,\rho^{3/2}T^{-1/2}.$$
It solves $\log P_\mathrm{tot} = \log P$ for $\log\rho$ by a Newton step with a second-order correction: with $f = (\log P_\mathrm{tot} - \log P)/\chi_\rho$ (`PR8`), $\chi_\rho = \partial\log P_\mathrm{tot}/\partial\log\rho$ (`PR7`) and the curvature term `PR9`,
$$\Delta\log\rho = -f - \tfrac12\,\mathrm{PR9}\,f^2,$$
limited to $\pm 4$ dex, until $|\Delta| < 10^{-8}$, at most 20 iterations.
3. **Debye–Hückel ramp.** With $c_0 = 2X + \tfrac32 Y + \tfrac12(Z + \alpha)$ (`CMFDH0`), $c_1 = X + Y + \tfrac12\alpha$ (`CMFDH1`) and $\alpha = \sum_i$ `DHNUE(i)*ZDH(i)` over the metal mixture, the composition factor $c_\mathrm{mix}$ is $c_0^{3/2}$ for non-degenerate electrons ($\eta <$ `ETADH0`), $c_0\sqrt{c_1}$ for degenerate ones ($\eta >$ `ETADH1`), and linear in $\eta$ between; the comment calls this "not correct but, hopefully, close enough".
4. **Derivatives.** From the table's derivative columns it forms $\partial\ln P/\partial\ln T$ and $\partial\ln P/\partial\ln\rho$ and their second derivatives, then inverts them: $Q_{\rho P} = 1/\chi_\rho$, $Q_{\rho T} = -\chi_T/\chi_\rho$. The internal energy is $U = \tfrac32 P_\mathrm{ion}/\rho + U_e + 3P_\mathrm{rad}/\rho\;(+\,3P_\mathrm{DH}/\rho)$, and
$$c_P = -\frac{P}{\rho T}Q_{\rho T}\,\chi_T + \frac{U}{T}\,\frac{\partial\ln U}{\partial\ln T}\Big|_\rho, \qquad \nabla_\mathrm{ad} = -\frac{P}{\rho T}\frac{Q_{\rho T}}{c_P}.$$

**KC's changes.** The unused argument `X` was removed (2025-05-31).

## Questions for the experts

1. **Unconverged return.** After 20 iterations without convergence the routine writes a message and returns at once (the `STOP` is commented out). It returns before `DL = DL8`, so `DL` and `D` keep the caller's starting guess, and the derivatives (all arguments) keep whatever the caller's variables held. Is this fallback intended, and does any caller check for it?
2. **A COMMON name.** `/DEBHU/` names its X element `XXDY` in [[eqstat.f#EQSTAT|EQSTAT]] and `XXDH` everywhere else. They are the same storage, so this is harmless; should the name be made the same?
3. **Unused COMMON.** `/CONST3/` is declared but not used.
4. **Table edges.** The temperature index is forced into the table (`JT1` between 1 and 18) and the density index into 1..261; outside the table the values are extrapolated silently. Should a warning be written?

### EQRELV

Solves the pressure balance for $\rho$ with the electron table and returns $\rho$, $\eta$, $c_P$, $\nabla_\mathrm{ad}$ and their derivatives for fully ionized gas (method above).
