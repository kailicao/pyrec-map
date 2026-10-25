## Explanation

**Purpose.** `YTIME` gives the time step allowed by helium burning. Its comment: stars with a helium luminosity have a time step limited by the time to burn `ATIME(4)` of $Y$ at the temperature maximum, or the fraction `ATIME(5)` of $Y$ there; a high central density is taken as the sign of a giant in the helium flash rather than a horizontal-branch star.

**How it fits.**
- **Inputs:** the model (arguments: $\log\rho$ `HD`, `HCOMP`, $L$, $m$, $\log T$, `JCORE`, `M`, `JXBEG`), work arrays for the rates, and through COMMON blocks the limits `ATIME` (`CTLIM`), the extended-composition switch `LEXCOM` (`FLAG`), and `ENU`, `EALPCA` (`NEWEPS`, set by [[engeb.f#ENGEB|ENGEB]]).
- **Who calls it:** only [[htimer.f#HTIMER|HTIMER]].
- **What it calls:** [[engeb.f#ENGEB|ENGEB]], for the energy rates at the temperature maximum.
- **Outputs:** `DELTSY`, the step (in seconds, by its use in `HTIMER`), and `EG(1..6)`, the energy rates at the temperature maximum.

**The method.**
- **Helium flash** ($\log\rho_c \ge 5$): find the shell of maximum temperature, compute its energy rates with `ENGEB`, and take
  $$\Delta t = \frac{10^{15}}{\varepsilon_5},$$
  with $\varepsilon_5$ = `EG(5)` (probably the triple-α rate, by the order in `ENGEB`), at least $10^{-22}$.
- **Otherwise:** with $Y_\mathrm{core}$ at `JCORE` and $q = 5.85\times10^{17}$ erg/g (the commented-out `Q3A`), if $Y_\mathrm{core} \ge$ `ATIME(1)`,
  $$\Delta Y = \min(\texttt{ATIME(4)},\ \texttt{ATIME(5)}\,Y_\mathrm{core}),\qquad \Delta t = \frac{q}{L_\odot}\,\frac{m}{L/L_\odot}\,\Delta Y$$
  at `JCORE`; otherwise the same with $m$ and $L$ just below the hydrogen shell (`JXBEG-1`).

**KC's changes.** Removed the unused arguments `QDP` and `QDT`, and shortened the call to `ENGEB` to its new argument list (2025-05-31).

## Questions for the experts

1. **$Y$ or $1 - Z$?** `YCORE = 1D0 - HCOMP(3,JCORE)` is $X + Y$, not $Y$ (`HCOMP(2,·)`). In a helium core $X \approx 0$ and the two agree, but during hydrogen burning they do not. Intended?
2. **An undefined step.** In the `ELSE` branch ($Y_\mathrm{core} <$ `ATIME(1)`), `DELTSY` is used on the right-hand side before it is set in this call; it holds the value `SAVE`d from an earlier call. A line like `DELTSY = MIN(ATIME(4), ATIME(5)*Y)` seems to be missing.
3. **The same threshold for $X$ and $Y$.** `ATIME(1)` is the central-hydrogen threshold in [[xtime.f#XTIME|XTIME]], and here the threshold for $Y_\mathrm{core}$. Two parameters?
4. **Hard-coded values.** The flash criterion $\log\rho_c \ge 5$, the constant $10^{15}$ (whose units are unclear) and the floor $10^{-22}$.

### YTIME

The helium-burning time step: during the helium flash $10^{15}/\varepsilon_{3\alpha}$ at the temperature maximum; otherwise the time to burn a fraction of the core's helium.
