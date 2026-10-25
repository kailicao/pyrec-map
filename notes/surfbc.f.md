## Explanation

**Purpose.** `SURFBC` provides the outer boundary condition of the interior solution, by the "envelope triangle". Envelopes are integrated at three points around the model's $(\log T_\mathrm{eff}, \log L)$; each gives $\log P$, $\log T$ and $\log R$ at the fitting point. A plane through the three points then gives $\log R$, $\log L$ and $\log T_\mathrm{eff}$ as linear functions of $\log P$ and $\log T$ at the fitting point, which the Henyey solution uses as its outer boundary. It also switches between atmosphere tables and the gray atmosphere as $T_\mathrm{eff}$ changes.

**How it fits.**
- **Inputs:** arguments from [[crrect.f#CRRECT|CRRECT]]: the current $\log T_\mathrm{eff}$ (`TEFFL`), $\log L/L_\odot$ (`BL`), the triangle (`TRIT`, `TRIL`, `FTRI`) and its envelopes' results (`PS`, `TS`, `RS`) from earlier calls, the surface $X$, $Z$, the rotation factors `FPL`, `FTL`, and the pressure limit `PLIM`. The triangle's size `TRIDT`, `TRIDL` comes from COMMON `CENV`; the atmosphere choice from `ATMOS` (`KTTAU`, `KTTAU0`, `LTTAU`); the Allard table's upper limit from `ALATM05`, set by [[altabinit.f#ALTABINIT|ALTABINIT]].
- **Who calls it:** only [[crrect.f#CRRECT|CRRECT]].
- **What it calls:** [[envint.f#ENVINT|ENVINT]] for each envelope to be recomputed.
- **Outputs:** `CFENV(1:9)`, the plane's coefficients, which `CRRECT` uses for the boundary equations and to update $T_\mathrm{eff}$; the triangle and `PS`, `TS`, `RS`; `LFLP` (true if an envelope was recomputed); a table of the triangle on `ISHORT`.
- **COMMON blocks:** `ATMOS` (shared with [[envint.f#ENVINT|ENVINT]], [[parmin.f#PARMIN|PARMIN]], [[setups.f#SETUPS|SETUPS]] and others), `CENV`, `COMP` (the total mass `STOTAL`), `SPOTS`, `ALATM05`, the constants, `LUOUT`, and `CCOUT`, `CCOUT1`, declared but not used here.

**The method.**
1. **Atmosphere switch** (MHP 9/01, 06/13). With Kurucz tables (`KTTAU = 3`) above $\log T_\mathrm{eff} = 3.95$, or Allard tables (`KTTAU = 4`) above the table's maximum, the code switches to the gray atmosphere (`KTTAU = 0`), remembers it (`LTTAU`), and starts a new triangle; it switches back when $T_\mathrm{eff}$ drops below the limit again.
2. **A new triangle** (`LNEW`). With `LRESET` (from [[crrect.f#CRRECT|CRRECT]]) all three envelopes are recomputed without starting a new triangle; with `LNEW` the triangle is new too, and its vertices, with $T = \log T_\mathrm{eff}$, $L = \log L$,
   $$(T - \tfrac12\Delta T,\ L - \tfrac12\Delta L),\quad (T + \tfrac12\Delta T,\ L - \tfrac12\Delta L),\quad (T,\ L + \tfrac12\Delta L).$$
   Otherwise the code checks that the point lies inside the triangle: for each vertex $i$, with the other two $j$, $k$, the sign of
   $$f\left[(L_j - L_k)(T - T_j) + (T_k - T_j)(L - L_j)\right]$$
   ($f$ = `FTRI`, the orientation) must not be negative. If it is, vertex $i$ is replaced by $T_i \to T_j + T_k - T_i$, $L_i \to L_j + L_k - L_i$ (the triangle flips across that side, and its orientation changes), and the check repeats.
3. **New envelopes.** For each new vertex, `ENVINT` integrates at $L_i$ and $T_i$, with $\log R = \tfrac12(\log L + \log L_\odot - 4\log T_\mathrm{eff} - \log 4\pi - \log\sigma)$ and $\log g = \log G + \log M - 2\log R$; for a spotted star, at the ambient temperature (the formula in [[starin.f|starin.f]]).
4. **The plane.** With $(P_i, T^\mathrm{f}_i)$ the fitting point's $\log P$ and $\log T$ of envelope $i$, each $Q \in \{\log R, \log L, \log T_\mathrm{eff}\}$ is fitted exactly through the three envelopes:
   $$Q = c_1\,\log P + c_2\,\log T + c_3,$$
   with `CFENV(1:3)` for $\log R$, `CFENV(4:6)` for $\log L$, `CFENV(7:9)` for $\log T_\mathrm{eff}$.

**Design.** `TEFFL` is overwritten with each new vertex's temperature, and so returns changed to the caller. `NUMENV` here is a local counter (`DATA NUMENV/0/`), not the envelope's point count in COMMON `ENVSTRUCT`. The comment "IF LNEW0, REDO ALL 3 ENVELOPES EVERY MODEL" refers to the caller; `LNEW0` is not used here.

**KC's changes.** The unused argument `LSBC` was removed (2025-05-31).

## Questions for the experts

1. **`TEFFL` changed on return.** Inside the loop over vertices, `TEFFL = TRIT(I)`, and `TEFFL` is an argument, so the caller's $T_\mathrm{eff}$ becomes the last recomputed vertex's. Does `CRRECT` rely on recomputing it afterwards (it sets `TEFFL` from `CFENV(7:9)` later), or is this a side effect to remove?
2. **The Kurucz–Castelli tables.** The switch to the gray atmosphere covers `KTTAU = 3` (Kurucz) and `4` (Allard), but not `KTTAU = 5` (Kurucz–Castelli, used by [[envint.f#ENVINT|ENVINT]] through `KCSURFP`). Does that table need no limit?
3. **The tolerance `TRIERR`.** It is always zero, so the point must be strictly inside or on the triangle. Is the variable left from an older tolerance?
4. **Hard-coded limit.** The gray switch for Kurucz tables is at $\log T_\mathrm{eff} = 3.95$, written in the code; should it come from the table's range, as for the Allard tables?
5. **Switching back keeps the gray envelopes.** Switching to the gray atmosphere sets `LNEW`, but switching back to the Kurucz or Allard tables (`LTTAU`, then `LTTAU = .FALSE.`) does not, so the triangle's envelopes computed with the gray atmosphere are kept. Should the switch back also start a new triangle?

### SURFBC

The envelope triangle: keeps three envelope integrations around $(\log T_\mathrm{eff}, \log L)$, flips the triangle when the model leaves it, and fits the plane `CFENV` that gives $\log R$, $\log L$ and $\log T_\mathrm{eff}$ from $\log P$ and $\log T$ at the fitting point.
