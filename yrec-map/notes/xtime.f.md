## Explanation

**Purpose.** `XTIME` gives the time step allowed by hydrogen burning (its comment). While the central hydrogen abundance is at least `ATIME(1)`, the step is the time to burn a given amount of the core's hydrogen; afterwards, in shell burning, the smaller of the time to burn a fraction of the star's hydrogen and the time to deplete a given amount of $X$ at the shell's midpoint.

**How it fits.**
- **Inputs:** the model (arguments: $\rho$, `HCOMP`, $L$, $m$, shell masses, $T$), the hydrogen-burning luminosity `HYDLUM`, the convective core's edge `JCORE`, the shell's midpoint `JXMID`; through modules the limits `ATIME` (`NMLPAR_MOD`), the constants (`CONSTANTS_MOD`).
- **Who calls it:** only [[htimer.f#HTIMER|HTIMER]].
- **What it calls:** [[rates.f#RATES|RATES]] and [[eqburn.f#EQBURN|EQBURN]], for $dX/dt$ at the shell's midpoint.
- **Output:** `DELTSH`, in seconds (by its use in `HTIMER`).
- **Modules:** `NMLPAR_MOD` (formerly `COMMON/CTLIM/`), `CONSTANTS_MOD`, `DIMENSIONS_MOD`.

**The method.** With $q = 6.0\times10^{18}$ erg released per gram of hydrogen burned (the code's constant):
- **Core burning** ($X_c \ge$ `ATIME(1)`): $\Delta X = \min(\texttt{ATIME(2)},\ \texttt{ATIME(3)}\,X_\mathrm{core})$ and
  $$\Delta t = \frac{q}{L_\odot}\,\frac{m_\mathrm{core}}{L(m_\mathrm{core})/L_\odot}\,\Delta X,$$
  with $m$ and $L$ at `JCORE`, so that a convective core counts as a whole (the comment). The header speaks of "the fraction ATIME(3) of the central X," and the code takes $X$ at `JCORE`: The two agree, since `JCORE` is the outermost point of the convective core, which is mixed, or 1 (the center) when there is no convective core or the star is fully convective (settled from the code, Nov 9, 2026: [[#L53-L55]]; [[#L66]]; [[findsh.f#L65]]; [[findsh.f#L108-L110]]; [[findsh.f#L124]]).
- **Shell burning:** $\Delta t = q\,\texttt{ATIME(6)}\,X_s M_\odot/L_\odot\,/\,L_H$, with $X_s$ the surface $X$ and $L_H$ = `HYDLUM`; and, if $dX/dt < 0$ at the shell's midpoint and `ATIME(7)` > 0,
  $$\Delta t = \min\!\left(\Delta t,\ \left|\frac{\texttt{ATIME(7)}}{dX/dt}\right|\,\mathrm{CSECYR}\times10^9\right).$$
  `ATIME(6)` is a mass in solar masses, whatever the star's mass: REMAP's comment calls it the "max permitted solar masses of X burned in timestep" (`TIME_DX_TOTAL`, "max absolute H burned per timestep (post-MS)" in the documentation); the code burns the hydrogen of `ATIME(6)` $M_\odot$ of matter at the surface $X$, and the header's "the mass fraction ATIME(6) of X in the entire star" is older wording (settled from the code and the documentation, Nov 9, 2026: [[#L56-L60]]; [[#L73-L74]]; [[remap.f#L266-L267]]). The factor $\mathrm{CSECYR}\times10^9$ is there because `EQBURN` returns $dX/dt$ per Gyr: The rates of [[rates.f#RATES|RATES]] are per $10^9$ yr per amu (settled from the code, Nov 9, 2026: [[#L105-L106]]; [[rates.f#L656-L658]]).

**Changed since `rp_1`.** Declarations only: `/CTLIM/` to `NMLPAR_MOD`, the constants to `CONSTANTS_MOD`; the unused `/CT3/` and `/FLAG/` dropped; `IMPLICIT NONE`.

### XTIME

The hydrogen-burning time step: a fraction of the core's hydrogen while $X_c \ge$ `ATIME(1)`, then the smaller of a shell criterion and the depletion time at the shell's midpoint.
