## Explanation

**Purpose.** `GETFC` computes, shell by shell, the factor $f_c$ that relates the diffusion coefficient for chemical mixing to that for angular momentum transport by meridional circulation, "using the prescription of Zahn (1992)" (its comment).

**How it fits.**
- **Who calls it:** only [[seculr.f#SECULR|SECULR]], when `LVFC` is set, for the shells `IMIN..IMAX`.
- **Inputs:** `HD` ($\log\rho$ at zone centres), `HRU` (radii at zone centres), `HV` (circulation velocities $U$ at zone edges), `OMEGA`; and from `INTVAR_MOD`, `RM` (radii at zone edges, the means of neighbouring centre radii) and `DM` (density at zone edges, interpolated in $\log\rho$), both set by [[setupv.f#SETUPV|SETUPV]].
- **Output:** the argument `VFC`, an array that `SECULR` owns (it clears it, and passes it on to [[codiff.f#CODIFF|CODIFF]], which reads it).
- **Modules:** `NMLPAR_MOD` gives `FC` and `LVFC` (namelist parameters, read in [[parmin.f#PARMIN|PARMIN]]); `INTVAR_MOD` (the edge quantities), shared with `CODIFF`, `SECULR`, `SETUPV`, `VCIRC`; `CONSTANTS_MOD` (`CLN`, `CC13`); `DIMENSIONS_MOD` (`JSON`).

**The method.** The comment gives
$$f_c = \min\left(1,\ \frac{C}{30}\,\frac{U}{2V - \alpha U}\right),\qquad \alpha = \frac12\frac{d\ln(r^2\Omega)}{d\ln r},\qquad V = \frac{1}{6\rho r}\frac{d}{dr}(\rho r^2 U).$$
The code computes:
1. `ALPHA` $= \dfrac{1}{\Omega_m r_m}\dfrac{\Delta(\Omega r^2)}{\Delta r}$ between neighbouring zone centres, with $\Omega_m$ the mean of the two and $r_m$ = `RM` the edge between them, which is $d\ln(r^2\Omega)/d\ln r$, without the factor ½ (Bugs, by priority, 1). It uses shell `IMIN-1`, which exists: MIDMOD sets `IMIN` ≥ 2.
2. `V` $= \dfrac{1}{3\rho r}\dfrac{d}{dr}(\rho r^2 U)$, which is $2V$; at the first and last shells, by the product rule with $dU/dr$ from the neighbour.
3. `VFC` $= \dfrac{f_c^{\mathrm{in}}}{\max\left(|{\tt V} - {\tt ALPHA}\,U|/U,\ f_c^{\mathrm{in}}\right)} = \min\left(1,\ \dfrac{f_c^{\mathrm{in}}\,U}{|2V - {\tt ALPHA}\,U|}\right)$, with $f_c^{\mathrm{in}}$ = `FC`; zero where $U \le 0$, and everywhere if `FC` ≤ 0. The absolute value is the code's; the comment's formula has none.

    > **Question** ([[#L63]], [[#L112-L113]]). **`FC` and $C/30$.** The input `FC` plays the part of $C/30$ in the comment's formula, while without `LVFC` it is the constant ratio of the two coefficients ([[codiff.f#CODIFF|CODIFF]]). Is that the intended meaning of the parameter with `LVFC`?

    > **Question** ([[#L109-L110]]). **Negative velocities.** Where $U \le 0$, $f_c = 0$: no chemical mixing where the circulation flows inward. Intended, or should $|U|$ be used?

**Changed since `rp_1`.** `VFC` is a new argument (it was in `/VARFC/`, now removed; `SECULR` owns the array); COMMON blocks to modules (`FC` from `NMLPAR_MOD`, `/VMULT/` gone), `IMPLICIT NONE`. No question is settled.

## Bugs, by priority

1. **(a)** **The factor ½ in $\alpha$.** ([[#L63]]; [[#L75-L79]]; [[#L112]]) The comment defines $\alpha = \tfrac12\,d\ln(J/M)/d\ln r$, as in Zahn (1992), and uses $2V - \alpha U$. The code computes `ALPHA` $= d\ln(r^2\Omega)/d\ln r$, with no ½, and then `V - ALPHA*HV`, where `V` is already $2V$. So the code's denominator is $2V - 2\alpha U$, and the $\alpha$ term is twice what the comment gives, which changes $f_c$ wherever that term matters. Only with `LVFC` (off by default; "experimental" in the Physics namelist page). Read from the code, not run. **A possible fix** (unless the comment is the slip):

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to include the factor 1/2 of the comment's
    C ALPHA=1/2 D(LN J/M)/D LN R.
          DO I = IMIN,IMAX
             WM = 0.5D0*(OMEGA(I)+OMEGA(I-1))
             ALPHA(I) = 0.5D0*(OMEGA(I)*HRU(I)**2-OMEGA(I-1)*HRU(I-1)**2)/
         *              (HRU(I)-HRU(I-1))/(WM*RM(I))
          END DO
    ```

### GETFC

Zahn (1992) ratio $f_c$ of the chemical to the angular-momentum diffusion coefficient, per shell, capped at 1 (equations above).
