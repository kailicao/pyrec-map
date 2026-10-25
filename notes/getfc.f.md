## Explanation

**Purpose.** `GETFC` computes, shell by shell, the factor $f_c$ that relates the diffusion coefficient for chemical mixing to that for angular momentum transport by meridional circulation, "using the prescription of Zahn (1992)" (its comment).

**How it fits.**
- **Who calls it:** only [[seculr.f#SECULR|SECULR]], when `LVFC` is set, for the shells `IMIN..IMAX`.
- **Inputs:** `HD` ($\log\rho$ at zone centres), `HRU` (radii at zone centres), `HV` (circulation velocities $U$ at zone edges), `OMEGA`; and from `/INTVAR/`, `RM` (radii at zone edges, the means of neighbouring centre radii) and `DM` (density at zone edges, interpolated in $\log\rho$), both set by [[setupv.f#SETUPV|SETUPV]].
- **Output:** `VFC` in `/VARFC/`, read by `SECULR`, [[codiff.f#CODIFF|CODIFF]], `DCOEFT`, [[checkj.f#CHECKJ|CHECKJ]], `ROTGRID` and [[vcirc.f#VCIRC|VCIRC]].
- **COMMON blocks:** `/VMULT/` gives `FC` (set in [[parmin.f#PARMIN|PARMIN]]); `/INTVAR/` (the edge quantities), shared with `CODIFF`, `SECULR`, `SETUPV`, `VCIRC`; `/VARFC/` (output).

**The method.** The comment gives
$$f_c = \min\left(1,\ \frac{C}{30}\,\frac{U}{2V - \alpha U}\right),\qquad \alpha = \frac12\frac{d\ln(r^2\Omega)}{d\ln r},\qquad V = \frac{1}{6\rho r}\frac{d}{dr}(\rho r^2 U).$$
The code computes:
1. `ALPHA` $= \dfrac{1}{\Omega_m r_m}\dfrac{\Delta(\Omega r^2)}{\Delta r}$ between neighbouring zone centres, with $\Omega_m$ the mean of the two and $r_m$ = `RM` the edge between them, which is $d\ln(r^2\Omega)/d\ln r$, without the factor ½. It uses shell `IMIN-1`, which exists: MIDMOD sets `IMIN` ≥ 2.
2. `V` $= \dfrac{1}{3\rho r}\dfrac{d}{dr}(\rho r^2 U)$, which is $2V$; at the first and last shells, by the product rule with $dU/dr$ from the neighbour.
3. `VFC` $= \dfrac{f_c^{\mathrm{in}}}{\max\left(|{\tt V} - {\tt ALPHA}\,U|/U,\ f_c^{\mathrm{in}}\right)} = \min\left(1,\ \dfrac{f_c^{\mathrm{in}}\,U}{|2V - {\tt ALPHA}\,U|}\right)$, with $f_c^{\mathrm{in}}$ = `FC`; zero where $U \le 0$, and everywhere if `FC` ≤ 0. The absolute value is the code's; the comment's formula has none.

## Questions for the experts

1. **The factor ½ in $\alpha$.** The comment defines $\alpha$ with a factor ½; the code has none. Which is right?
2. **`FC` and $C/30$.** The input `FC` plays the part of $C/30$ in the comment. Is that the intended meaning of the parameter?
3. **Negative velocities.** Where $U \le 0$, $f_c = 0$: no chemical mixing where the circulation flows inward. Intended, or should $|U|$ be used?

### GETFC

Zahn (1992) ratio $f_c$ of the chemical to the angular-momentum diffusion coefficient, per shell, capped at 1 (equations above).
