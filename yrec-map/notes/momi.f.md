## Explanation

**Purpose.** Computes the moment of inertia `HI` of each shell of a rotating, distorted model, and its derivative with respect to $\ln A$, $A$ being the distortion parameter below, `QIW` $= dI/d\ln A$, which at fixed shape ($\eta_2$, $r_0$) is $\tfrac12\,\Omega\,\partial I/\partial\Omega$ (since $A \propto \Omega^2$; the comments name it a derivative in $\Omega$: question 3). The comment: "Moment of inertia is calculated by the method used in Wai-Yuen Law's thesis (Yale, 1980) p.61", and "MOMI assumes that SHAPE has already been called".

**How it fits.**
- **Inputs:** the shape parameters `ETA2` (Radau's $\eta_2$) and `R0` (the characteristic radius $r_0$ of the equipotential, $r = r_0(1 - AP_2)$) per shell, from [[shape.f#SHAPE|SHAPE]]; $\log r$ (`HR`), $\log m$ (`HS`), the shell masses `HS2`, the angular velocities `OMEGA`, and the shell range `JSTART..JEND`.
- **Who calls it:** [[hpoint.f#HPOINT|HPOINT]], [[solid.f#SOLID|SOLID]] and [[starin.f#STARIN|STARIN]].
- **What it calls:** [[intmom.f#INTMOM|INTMOM]], which evaluates the integral at each shell.
- **Outputs:** `HI` and `QIW` per shell.
- **Modules:** `NMLPAR_MOD` (`WALPCZ`), `CONSTANTS_MOD` (`CLN`, `CC13`, `CC23`, and $\log G$, `CGL`), `DIMENSIONS_MOD` (`JSON`). The unused `/CCOUT/` and `/LUOUT/` of `rp_1` are no longer declared.

**The method.**
- **Spherical shortcut.** If `WALPCZ` $\ne 0$ (`WALPCZ` is the exponent of the rotation law $\Omega\, r^{\mathrm{WALPCZ}} =$ constant in the surface convection zone, as [[getnewenv.f#GETNEWENV|GETNEWENV]]'s comment says; [[parmin.f#PARMIN|PARMIN]] keeps it between −2 and 0, so 0 is solid-body rotation), each shell is a thin spherical shell, $I = \tfrac23\,\Delta m\, r^2$, with $dI/d\Omega = 0$; the central shell is a sphere, $I = 0.4\,\Delta m\, r^2$, at the mean of the first two $\log r$.
- **Distorted shells.** Otherwise, for each shell, with $r_0$ = `R0`, the parameter
$$A = \frac{5}{3}\,\frac{\Omega^2\, r_0^3}{G\,m\,(2 + \eta_2)}$$
(`CON` $=5/(3G)$), the ratio `R0R` $= r_0^5/r^3$, and `QR0R` $= d\ln r_0/d\ln r$ set to 1, go to `INTMOM`, which returns $I$ and `QIWM` per unit mass; these are multiplied by `HS2`. `INTMOM` sums a series to $A^5$ (Law 1980's coefficients $c_j$): $I = H_1\bigl(1 + 0.15\sum_j c_j(j\eta_2+5)A^j\bigr)$ and `QIWM` $= H_1\cdot0.15\sum_j j\,c_j(j\eta_2+5)A^j = A\,dI/dA$ at fixed $\eta_2$ and $r_0$.

**KC's changes.** 2025-05-31: the unused arguments `HD` and `M` removed.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **Unused values.** `R0P` and `RPHIP` (the previous shell's $\ln r_0$ and $\ln r$) and `H0` (the thin-shell moment of inertia) are computed in each pass but never used, and `QR0R` is fixed at 1. Were they meant for a derivative $d\ln r_0/d\ln r$ between shells?
2. **`WALPCZ` as a switch.** The spherical shortcut is taken for every shell in `JSTART..JEND`, not only those in the convection zone, whenever the convection zone's rotation law is not solid-body (`WALPCZ` $\ne 0$). Why should that law switch off the distortion of all shells?
3. **`QIW` and SOLID's Newton step.** `QIW` is $A\,dI/dA = \tfrac12\,\Omega\,dI/d\Omega$, not $dI/d\Omega$ as the comments say. [[solid.f#SOLID|SOLID]] solves $J = \Omega I(\Omega)$ with `DELW = DELJ/(CZI + WGUESS*CZQIW)`; Newton's step needs $I + \Omega\,dI/d\Omega = I + 2\,$`QIW`, while $I + \Omega\cdot$`QIW` adds a term with units of $I$ s$^{-1}$, a fraction $\Omega/2$ (with $\Omega$ in rad s$^{-1}$) of the needed one, about $10^{-6}$ for the Sun's rate. The missing term is of order $A$ relative to $I$, so the iteration, in effect a fixed-point one, still converges almost as fast as Newton's (its error shrinks by about $2\,$`QIW`$/I \approx 0.18(\eta_2+5)A$ per step, from INTMOM's leading term) for any $A$ in the method's range; the fix is for correctness, not convergence. Should SOLID's denominator be `CZI + 2*CZQIW`, or should INTMOM return $dI/d\Omega$ (`QIWM`$\cdot 2/\Omega$)?
4. **A series to $A^5$ on a first-order shape.** INTMOM expands $I$ to $A^5$, while SHAPE keeps the equipotentials to first order in $\Omega^2$ (only the $P_2$ term). Is the expansion the exact moment of a body $r = r_0(1-AP_2)$, kept for accuracy at large $A$, or should it be truncated consistently with the shape?
