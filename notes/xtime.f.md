## Explanation

**Purpose.** `XTIME` gives the time step allowed by hydrogen burning (its comment). While the central hydrogen abundance is at least `ATIME(1)`, the step is the time to burn a given amount of the core's hydrogen; afterwards, in shell burning, the smaller of the time to burn a fraction of the star's hydrogen and the time to deplete a given amount of $X$ at the shell's midpoint.

**How it fits.**
- **Inputs:** the model (arguments: $\rho$, `HCOMP`, $L$, $m$, shell masses, $T$), the hydrogen-burning luminosity `HYDLUM`, the convective core's edge `JCORE`, the shell's midpoint `JXMID`; through COMMON blocks the limits `ATIME` (`CTLIM`), the constants.
- **Who calls it:** only [[htimer.f#HTIMER|HTIMER]].
- **What it calls:** [[rates.f#RATES|RATES]] and [[eqburn.f#EQBURN|EQBURN]], for $dX/dt$ at the shell's midpoint.
- **Output:** `DELTSH`, in seconds (by its use in `HTIMER`).
- **COMMON blocks:** `CTLIM`, `CONST`, `CONST3`; `CT3` (`LPTIME`) and `FLAG` are declared but not used.

**The method.** With $q = 6.0\times10^{18}$ erg released per gram of hydrogen burned (the code's constant):
- **Core burning** ($X_c \ge$ `ATIME(1)`): $\Delta X = \min(\texttt{ATIME(2)},\ \texttt{ATIME(3)}\,X_\mathrm{core})$ and
  $$\Delta t = \frac{q}{L_\odot}\,\frac{m_\mathrm{core}}{L(m_\mathrm{core})/L_\odot}\,\Delta X,$$
  with $m$ and $L$ at `JCORE`, so that a convective core counts as a whole (the comment).
- **Shell burning:** $\Delta t = q\,\texttt{ATIME(6)}\,X_s M_\odot/L_\odot\,/\,L_H$, with $X_s$ the surface $X$ and $L_H$ = `HYDLUM`; and, if $dX/dt < 0$ at the shell's midpoint and `ATIME(7)` > 0,
  $$\Delta t = \min\!\left(\Delta t,\ \left|\frac{\texttt{ATIME(7)}}{dX/dt}\right|\,\mathrm{CSECYR}\times10^9\right).$$

**KC's changes.** Removed the unused argument `JXBEG`, and shortened the calls to `RATES` and `EQBURN` to their new argument lists (2025-05-31).

## Questions for the experts

1. **The star's mass or the Sun's?** In shell burning, the hydrogen mass is `ATIME(6)*HCOMP(1,M)*CMSUN`, one solar mass, whatever the star's mass. The comment says "the mass fraction ATIME(6) of X in the entire star". Should it use the star's mass?
2. **Units of $dX/dt$.** The second limit multiplies by `CSECYR*1.0D9`, as if `EQBURN` returned $dX/dt$ per Gyr. Is that its unit?
3. **The core's hydrogen.** The comment says the core criterion burns "the fraction ATIME(3) of the central X"; the code uses $X$ at `JCORE` (the core's edge), which equals the centre's only for a mixed core.

### XTIME

The hydrogen-burning time step: a fraction of the core's hydrogen while $X_c \ge$ `ATIME(1)`, then the smaller of a shell criterion and the depletion time at the shell's midpoint.
