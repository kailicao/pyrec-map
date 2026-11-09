## Explanation

**Purpose.** `GETQUA` solves for the quadrupole moment (the $P_2$ part of the gravitational potential perturbation) of a rotating star, "using the Sweet (1950) formulation as given in Zahn (1992)" (its comment). The result is needed for the meridional circulation velocity.

**How it fits.**
- **Who calls it:** only [[seculr.f#SECULR|SECULR]].
- **Inputs:** `HD` ($\log\rho$), `HG` (gravity $g$), `HRU` (radius, unlogged), `OMEGA`, `M`.
- **Outputs:** in [[quadru_mod.f#QUADRU_MOD|`QUADRU_MOD`]]: `QUAD` (the quadrupole term per shell) and `GG` (a copy of $g$), read by [[getw.f#GETW|GETW]] and [[vcirc.f#VCIRC|VCIRC]].
- **Modules:** `QUADRU_MOD` (output); [[tridi_mod.f#TRIDI_MOD|`TRIDI_MOD`]] as workspace for the tridiagonal solver (shared with `CCOEFT`, `CTRIDI`, `DCOEFT`, [[mixcom.f#MIXCOM|MIXCOM]], `TRIDIA`); constants from [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]]; `ISHORT` from [[iounits_mod.f#IOUNITS_MOD|`IOUNITS_MOD`]], for the error message.

**The method.** The comment states the equation
$$\frac{1}{r}\frac{d^2}{dr^2}(r\phi) - \frac{6\phi}{r^2} - 4\pi G\rho\frac{d\rho}{dP}\,\phi = -\frac{4\pi G}{3}\frac{r^2}{g}\frac{d}{dr}\left(\rho\Omega^2\right),$$
and the code discretizes, per point,
$$\phi'' + \frac{2}{r}\phi' - \frac{6}{r^2}\phi - \frac{4\pi G}{g}\frac{d\rho}{dr}\,\phi = -\frac{4\pi G\,r^2}{3g}\,\frac{d(\rho\Omega^2)}{dr},$$
with $\phi$ = `QUAD` (with $dP/dr = -\rho g$, the sign of the $d\rho/dr$ term differs from the comment's; [[#q1]]). The code uses the model's $d\rho/dr$ directly, which needs only hydrostatic equilibrium to stand for $\rho\,d\rho/dP$, not the ideal gas law the comment cites ([[#L40-L41]]) (settled from the code, Nov 9, 2026). Derivatives are centred on the smaller of the two neighbouring intervals (weights `FPL`, `FMI`). Boundary conditions: $\phi \to 0$ at the centre; at the surface, $\phi \propto r^{-3}$ outside the star ("D PHI/DR + 3 PHI/R = 0", [[#L87-L97]]), applied through a point outside, $\phi_{M+1} = (r_M/r_{M+1})^3\phi_M$ (`FX`), with $\tfrac{2}{r}\phi' = -6\phi/r^2$ added to $-6\phi/r^2$, hence the $-12/r^2$ of `B(M)`. Outside the star ($\rho = 0$) the comment's own equation has the solutions $r^2$ and $r^{-3}$, so the decaying $r^{-3}$ of the surface condition is the right one, and the header's "VARIES AS 1/R**4" ([[#L45-L47]]) is a slip; the two terms that the comment says "CANCEL" ([[#L88]]) add up, as they should (settled from the code, Nov 9, 2026). The tridiagonal system is solved by the Thomas algorithm ("from Numerical Recipes"); the run stops on a zero pivot (exit status 1), with a message naming the zone, to the terminal and the `.short` file.

> **Question** ([[#L36-L41]]; [[#L79-L80]]). **A sign.** With hydrostatic equilibrium, $dP/dr = -\rho g$, the comment's term $-4\pi G\rho\,(d\rho/dP)\,\phi$ equals $+(4\pi G/g)(d\rho/dr)\,\phi$, but the code has $-(4\pi G/g)(d\rho/dr)\,\phi$ (in `B(I)`). Linearizing Poisson's equation with $P' = -\rho\phi$ gives $\nabla^2\phi + 4\pi G\rho\,(d\rho/dP)\,\phi$, which is the code's sign (and the sign of the comment's second form, "+4\*PI\*G\*RHO\*QUAD", which lacks $d\rho/dP$). Is the comment's first form a slip, so that the code is right?

> **Question** ([[#L54-L65]]). **The central row.** At the first point, $d\rho/dr$ is $(\rho_2-\rho_1)/\Delta r$ with $\Delta r = \min(r_1, r_2 - r_1)$, not divided by $r_2 - r_1$; and the right-hand side uses $\Omega_1^2\,d\rho/dr$ instead of $d(\rho\Omega^2)/dr$. Are these intended approximations near the centre?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

**Changed since `a8a5950`.** The two stops on a zero pivot, which printed nothing, now write the zone to the terminal and the `.short` file and exit with status 1, the code for run-time errors (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(a)** **A wrong index in $d\rho/dr$.** ([[#L76-L77]]; [[#L82-L84]]) In the interior loop, `DRHO = 0.5*(FPL*rho(I+1) + (FMI-FPL)*rho(I) - FMI*rho(I))/DR`: The last term uses `HD(I)` where the matching expression for $d(\rho\Omega^2)/dr$ just below uses `DW2(I-1)`. As written, the expression reduces to $\tfrac12(\rho_{i+1}-\rho_i)/\Delta r_+$, half the forward difference, instead of the mean of the two one-sided differences. What follows: The $d\rho/dr$ term of the diagonal `B(I)` ([[#L79-L80]]) is about half its value at every interior point, so the quadrupole term `QUAD` is wrong; VCIRC reads it in its Zahn branch (`IES` = 1, the default) for the factor `RAT` of the circulation velocity ([[vcirc.f#L239-L241]]), and GETW prints `QUAD(M)`. Only with rotation (`LROT`, off by default), where SECULR calls GETQUA. Read from the code, not run; the size of the effect on `RAT` was not traced. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to take the last term of DRHO at shell I-1, as in
    C DRHOW2.
             DRHO = 0.5D0*(FPL*EXP(CLN*HD(I+1))+(FMI-FPL)*
         *          EXP(CLN*HD(I))-FMI*EXP(CLN*HD(I-1)))/DR
    ```

### GETQUA

Solves the second-order ODE for the quadrupole moment with a tridiagonal solver (equation above); results in `QUADRU_MOD`.
