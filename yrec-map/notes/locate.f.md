## Explanation

**Purpose.** `LOCATE` finds, by bisection, the index $j$ such that $x$ lies between `XX(j)` and `XX(j+1)` in a monotonic array (ascending or descending), as in *Numerical Recipes*. $j = 0$ or $N$ means out of range.

**How it fits.** Called by the Livermore-table routine [[gtpurz.f#GTPURZ|`GTPURZ`]] (`GTLAOL` and `GTLAOL2` also called it; removed since `rp_1`) and by [[alsurfp.f#ALSURFP|`ALSURFP`]] (Allard atmospheres). No COMMON blocks, no calls.

**The method.** Standard bisection. Then two tolerances are added: if $j = 0$ but $x > 0.99\,\texttt{XX(1)}$, it returns $j = 1$; if $j = N$ but $x < 1.01\,\texttt{XX(N)}$, it returns $N-1$.

> **Question** ([[#L30-L35]]). **Relative tolerances.** The 1 % tolerances are relative to the end values, so they act only for positive end values in an ascending array (such as $\log T$). For an end value $\le 0$ (an $X$ grid starting at 0, or a grid in $\log\rho$) the test can never pass and there is no tolerance at all; for a descending array with positive ends, the tests pass for any $x$ beyond either end, which is then pulled in. Both callers today pass ascending tables with positive values, $\log T$ (`ZOT`, [[gtpurz.f#L69]]) and $\log T_\mathrm{eff}$ (`TEFFLs`, [[alsurfp.f#L205]]), so neither case arises. Was an absolute tolerance meant?

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE` with explicit declarations. Two of its callers (`GTLAOL`, `GTLAOL2`) are removed since `rp_1`.

### LOCATE

Bisection search with 1 % end tolerances (above).
