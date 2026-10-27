## Explanation

**Purpose.** `INTMOM` returns the moment of inertia per unit mass of a rotationally distorted shell, and its derivative with respect to $\Omega$, at one point (the comment: "moment of inertia per unit mass at the specified point (HI) and dI/dΩ per unit mass (QIW)").

**How it fits.** Called only by [[momi.f#MOMI|`MOMI`]], at each zone centre. `MOMI` passes `QR0R` = 1, `R0R` $= r_0^5/r^3$ (with $r_0$ the equivalent radius `R0` and $r$ the model's radius), `ETA2X` = $\eta_2$ (`ETA2`, from the Clairaut–Radau treatment of the distortion, as far as the names show) and $a = \dfrac{5}{3}\,\dfrac{\Omega^2 r_0^3}{G\,m\,(2+\eta_2)}$ (`A`; `CON` = $5/(3G)$ in `MOMI`). `MOMI` multiplies both results by the shell mass to get `HI` and `QIW`; it calls `INTMOM` only when `WALPCZ` = 0 (otherwise it uses $I = \tfrac23 \Delta m\, r^2$). Module: only [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]] (for $2/3$, `CC23`).

**The method.** With fixed coefficients $c_j$ (`C`: 0.6, 0.7286, 0.5088, 0.4973, 0.4285),

$$h = \tfrac{2}{3}\,q\,R,\qquad I/m = h\left(1 + 0.15\sum_{j=1}^{5} c_j\,(j\eta_2 + 5)\,a^j\right),\qquad \frac{dI/m}{d\ln a} = h\;0.15\sum_{j=1}^{5} j\,c_j\,(j\eta_2+5)\,a^j,$$

with $q$ = `QR0R`, $R$ = `R0R`; the two results are `HIM` and `QIWM`.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **Source of the series.** Where do the coefficients `C` and the factor 0.15 come from? A reference in the code would help.
2. **What `QIWM` is.** The sum is $a\,\partial(I/m)/\partial a$, a logarithmic derivative in $a \propto \Omega^2$, so $d(I/m)/d\Omega = (2/\Omega)\,$`QIWM`. `MOMI` stores `QIWM` times the shell mass as `QIW` without that factor, while the comment calls it $dI/d\Omega$. Where it is used, in the Newton step of [[solid.f#SOLID|`SOLID`]] (`DELW = DELJ/(CZI + WGUESS*CZQIW)`), it is treated as $dI/d\Omega$, so the derivative of $J = I\Omega$ becomes $I + \Omega\,\texttt{QIW}$ instead of $I + 2\,\texttt{QIW}$. This would change only the convergence of the iteration, not its result; was the factor $2/\Omega$ meant?

### INTMOM

The series above for $I/m$ and its derivative.
