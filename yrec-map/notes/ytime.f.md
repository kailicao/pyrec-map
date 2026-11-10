## Explanation

**Purpose.** `YTIME` gives the time step allowed by helium burning. Its comment: stars with a helium luminosity have a time step limited by the time to burn `ATIME(4)` of $Y$ at the temperature maximum, or the fraction `ATIME(5)` of $Y$ there; a high central density is taken as the sign of a giant in the helium flash rather than a horizontal-branch star.

**How it fits.**
- **Inputs:** the model (arguments: $\log\rho$ `HD`, `HCOMP`, $L$, $m$, $\log T$, `JCORE`, `M`, `JXBEG`), work arrays for the rates, and from modules the limits `ATIME`, the temperature cuts `TCUT` and the extended-composition switch `LEXCOM` (`NMLPAR_MOD`), and $L_\odot$ `CLSUN` and $M_\odot$ `CMSUN` (`CONSTANTS_MOD`).
- **Who calls it:** only [[htimer.f#HTIMER|HTIMER]].
- **What it calls:** [[engeb.f#ENGEB|ENGEB]], for the energy rates at the temperature maximum (and, below `ATIME(1)`, at each helium-burning point), which also returns `EALPCA` and `ENU` (and a $^7$Be mass fraction this routine does not use).
- **Outputs:** `DELTSY`, the step (in seconds, by its use in `HTIMER`), and `EG(1..6)`, the energy rates at the temperature maximum.

**The method.**
- **Helium flash** ($\log\rho_c \ge 5$): find the shell of maximum temperature, compute its energy rates with `ENGEB`, and take
  $$\Delta t = \frac{10^{15}}{\epsilon_5},$$
  with $\epsilon_5$ = `EG(5)`, ENGEB's fifth argument `E3AL`, the triple-α rate (settled from the code, Nov 9, 2026: [[#L104]]; [[#L115]]; [[engeb.f#L4]]), at least $10^{-22}$.

    > **Question** ([[#L69]]; [[#L118-L119]]). **Hard-coded values.** The flash criterion $\log\rho_c \ge 5$, the constant $10^{15}$, and the floor $10^{-22}$ are fixed in the code. With $\epsilon_5$ in erg g$^{-1}$ s$^{-1}$, $10^{15}$ is in erg g$^{-1}$: the step lets the hottest point release $10^{15}$ erg g$^{-1}$, which burns $\Delta Y \approx 10^{15}/5.85\times10^{17} \approx 0.0017$ there. Is that the intent, and should it follow `ATIME(4)` or `ATIME(5)`, as the other branches do?

- **Otherwise:** with $Y_\mathrm{core}$ at `JCORE` and $q = 5.85\times10^{17}$ erg/g (the commented-out `Q3A`), if $Y_\mathrm{core} \ge$ `ATIME(1)`,
  $$\Delta Y = \min(\texttt{ATIME(4)},\ \texttt{ATIME(5)}\,Y_\mathrm{core}),\qquad \Delta t = \frac{q}{L_\odot}\,\frac{m}{L/L_\odot}\,\Delta Y$$
  at `JCORE`. `ATIME(1)` is one threshold for both elements by design: [[xtime.f#XTIME|XTIME]] compares the central $X$ with it, this routine $Y_\mathrm{core}$; REMAP's comment calls it the "minimum central abundance to use core burning dt criterion," and the documentation of `TIME_CORE_MIN`, the "minimum X,Y for using core vs shell burning criteria" (settled from the code and the documentation, Nov 9, 2026: [[#L123]]; [[remap.f#L260-L261]]).

    > **Question** ([[#L122-L127]]; [[#L171-L173]]). **$Y$ or $1 - Z$?** `YCORE = 1D0 - HCOMP(3,JCORE)` is $X + Y$, not $Y$ (`HCOMP(2,·)`). In a helium core $X \approx 0$ and the two agree, but during hydrogen burning they do not. With the defaults (`ATIME(4)` = 0.02, `ATIME(5)` = 0.3) $\Delta Y$ is the same for both unless $Y_\mathrm{core} < 0.067$, so the choice matters little in practice. Is $1 - Z$ intended?

  Otherwise (the shell branch) the step is the smallest of three limits, starting from $10^{20}$ s:
  - burning `ATIME(14)` $M_\odot$ of helium at the luminosity just below the hydrogen shell, $\Delta t = (q/L_\odot)\,\texttt{ATIME(14)}\,M_\odot/(L/L_\odot)$ at `JXBEG-1` (when `JXBEG` > 1 and that $L > 0$);
  - burning the fraction `ATIME(12)` of $Y$ at any point with $Y \ge$ `ATIME(1)` and $\log T \ge$ `TCUT(4)`, $\Delta t = \texttt{ATIME(12)}\,Y/\dot Y$, with $\dot Y = \epsilon_{3\alpha}/q + \epsilon_{\alpha\mathrm{cap}}/(1.7276\times10^{18}\ \mathrm{erg/g})$ from `ENGEB` (`EGG55` and `EALPCA`, negative values taken as zero);
  - while $Y_\mathrm{core}$ > `YFLOOR` ($10^{-5}$, below every `END_YCEN` in use) and $L > 0$ at `JCORE`, the core criterion without its cap: $\Delta t = (q/L_\odot)\,\texttt{ATIME(5)}\,Y_\mathrm{core}\,m/(L/L_\odot)$ at `JCORE`, which resolves central helium exhaustion down to the `END_YCEN` stop.

**Changed since `rp_1`.** `EALPCA` and `ENU` come back from ENGEB as arguments (`/NEWEPS/` retired), with the new `BE7MFLOC` for ENGEB's $^7$Be mass fraction (formerly `/BE7/`); COMMON blocks to modules, `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

**Changed since `a8a5950`.** The shell branch (below `ATIME(1)`) has real limits: It used to rescale `DELTSY`, which held HTIMER's helium step in seconds, as if it were an amount of $Y$, so the step grew through core helium exhaustion; it now takes the smallest of the `ATIME(14)`, `ATIME(12)`, and core limits above, so `ATIME(12)` and `ATIME(14)`, read but never used before, now count (this settles former question 2).

### YTIME

The helium-burning time step: during the helium flash $10^{15}/\epsilon_{3\alpha}$ at the temperature maximum; otherwise the time to burn a fraction of the core's helium, or, below `ATIME(1)`, the smallest of the shell and core limits.
