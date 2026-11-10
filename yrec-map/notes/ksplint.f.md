## Explanation

**Purpose.** `KSPLINT` evaluates at $x$ the 4-point cubic spline whose second derivatives [[kspline.f#KSPLINE|`KSPLINE`]] computed (*Numerical Recipes*' `SPLINT`, with `NM` = 4 fixed).

**How it fits.** Called by the same routines as `KSPLINE`: [[kcsurfp.f#KCSURFP|`KCSURFP`]], [[surfp.f#SURFP|`SURFP`]], [[eqscve.f#EQSCVE|`EQSCVE`]], [[tauintnew.f#TAUINTNEW|`TAUINTNEW`]]. No calls; it uses `IOUNITS_MOD` for the unit `ISHORT` of its error message.

**The method.** It finds the interval $[x_\mathrm{lo}, x_\mathrm{hi}]$ by bisection, then with $h = x_\mathrm{hi}-x_\mathrm{lo}$, $A = (x_\mathrm{hi}-x)/h$, $B = (x-x_\mathrm{lo})/h$:

$$y = A\,y_\mathrm{lo} + B\,y_\mathrm{hi} + \frac{h^2}{6}\left[(A^3-A)\,y''_\mathrm{lo} + (B^3-B)\,y''_\mathrm{hi}\right].$$

Outside the 4 points it extrapolates with the end interval's cubic. If two nodes coincide it stops the run (`STOP 1`), with a message giving the node and $x$, written to the terminal and to `ISHORT`.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE` with explicit declarations.

**Changed since `a8a5950`.** The stop on two equal nodes now writes a message with the node and $x$ (it was "Ksplint failure," to the terminal only) to the terminal and to the `.short` file (the routine now uses `IOUNITS_MOD`), and exits with status 1, the code for run-time errors, instead of a bare `STOP` (`KNOWN_ISSUES.md`, issue 38).

### KSPLINT

Spline evaluation (above).
