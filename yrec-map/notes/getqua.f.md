## Explanation

**Purpose.** `GETQUA` solves for the quadrupole moment (the $P_2$ part of the gravitational potential perturbation) of a rotating star, "using the Sweet (1950) formulation as given in Zahn (1992)" (its comment). The result is needed for the meridional circulation velocity.

**How it fits.**
- **Who calls it:** only [[seculr.f#SECULR|SECULR]].
- **Inputs:** `HD` ($\log\rho$), `HG` (gravity $g$), `HRU` (radius, unlogged), `OMEGA`, `M`.
- **Outputs:** in [[quadru_mod.f#QUADRU_MOD|`QUADRU_MOD`]]: `QUAD` (the quadrupole term per shell) and `GG` (a copy of $g$), read by [[getw.f#GETW|GETW]] and [[vcirc.f#VCIRC|VCIRC]].
- **Modules:** `QUADRU_MOD` (output); [[tridi_mod.f#TRIDI_MOD|`TRIDI_MOD`]] as workspace for the tridiagonal solver (shared with `CCOEFT`, `CTRIDI`, `DCOEFT`, [[mixcom.f#MIXCOM|MIXCOM]], `TRIDIA`); constants from [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]].

**The method.** The comment states the equation
$$\frac{1}{r}\frac{d^2}{dr^2}(r\phi) - \frac{6\phi}{r^2} - 4\pi G\rho\frac{d\rho}{dP}\,\phi = -\frac{4\pi G}{3}\frac{r^2}{g}\frac{d}{dr}\left(\rho\Omega^2\right),$$
and the code discretizes, per point,
$$\phi'' + \frac{2}{r}\phi' - \frac{6}{r^2}\phi - \frac{4\pi G}{g}\frac{d\rho}{dr}\,\phi = -\frac{4\pi G\,r^2}{3g}\,\frac{d(\rho\Omega^2)}{dr},$$
with $\phi$ = `QUAD`. Derivatives are centred on the smaller of the two neighbouring intervals (weights `FPL`, `FMI`). Boundary conditions: $\phi \to 0$ at the centre; at the surface, $\phi \propto r^{-3}$ outside the star ("D PHI/DR + 3 PHI/R = 0"). The tridiagonal system is solved by the Thomas algorithm ("from Numerical Recipes"); the run stops on a zero pivot.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **A wrong index in $d\rho/dr$.** In the interior loop, `DRHO = 0.5*(FPL*rho(I+1) + (FMI-FPL)*rho(I) - FMI*rho(I))/DR`: the last term uses `HD(I)` where the matching expression for $d(\rho\Omega^2)/dr$ just below uses `DW2(I-1)`. It should probably be `HD(I-1)`. As written, the expression reduces to $\tfrac12(\rho_{i+1}-\rho_i)/\Delta r_+$, exactly half the forward difference.
2. **Two surface conditions in the comments.** The header says the quadrupole varies as $1/r^4$ outside the star; the surface comment says $\phi \propto (R/r)^3$, and the code uses `FX` $= (R/r)^3$ with a term $-12/r^2$. Which is meant?
3. **A sign.** With hydrostatic equilibrium, $dP/dr = -\rho g$, the comment's term $-4\pi G\rho\,(d\rho/dP)\,\phi$ equals $+(4\pi G/g)(d\rho/dr)\,\phi$, but the code has $-(4\pi G/g)(d\rho/dr)\,\phi$ (in `B(I)`). Is the sign in the code or in the comment wrong? (The comment's second form, "+4\*PI\*G\*RHO\*QUAD", matches neither.)
4. **Ideal gas.** The comment derives the equation "using hydrostatic equilibrium and the ideal gas law"; the code uses the model's $d\rho/dr$ directly, which does not need the ideal gas law. Is the comment out of date?
5. **The central row.** At the first point, $d\rho/dr$ is $(\rho_2-\rho_1)/\Delta r$ with $\Delta r = \min(r_1, r_2 - r_1)$, not divided by $r_2 - r_1$; and the right-hand side uses $\Omega_1^2\,d\rho/dr$ instead of $d(\rho\Omega^2)/dr$. Intended approximations near the centre?

### GETQUA

Solves the second-order ODE for the quadrupole moment with a tridiagonal solver (equation above); results in `QUADRU_MOD`.
