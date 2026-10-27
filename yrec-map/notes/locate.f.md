## Explanation

**Purpose.** `LOCATE` finds, by bisection, the index $j$ such that $x$ lies between `XX(j)` and `XX(j+1)` in a monotonic array (ascending or descending), as in *Numerical Recipes*. $j = 0$ or $N$ means out of range.

**How it fits.** Called by the Livermore-table routine [[gtpurz.f#GTPURZ|`GTPURZ`]] (`GTLAOL` and `GTLAOL2` also called it; removed since `rp_1`) and by [[alsurfp.f#ALSURFP|`ALSURFP`]] (Allard atmospheres). No COMMON blocks, no calls.

**The method.** Standard bisection. Then two tolerances are added: if $j = 0$ but $x > 0.99\,\texttt{XX(1)}$, it returns $j = 1$; if $j = N$ but $x < 1.01\,\texttt{XX(N)}$, it returns $N-1$.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE` with explicit declarations. Two of its callers (`GTLAOL`, `GTLAOL2`) are removed since `rp_1`.

## Questions for the experts

1. **Relative tolerances.** The 1 % tolerances are relative to the end values, so they act only for positive end values in an ascending array (such as $\log T$). For an end value $\le 0$ (an $X$ grid starting at 0, or a grid in $\log\rho$) the test can never pass and there is no tolerance at all; for a descending array the tests do not match the bisection's convention. Was an absolute tolerance meant?

### LOCATE

Bisection search with 1 % end tolerances (above).
