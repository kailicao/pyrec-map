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

1. **(changes results, small)** **Checked by KC** (Nov 10, 2026). **The factor ½ in $\alpha$.** ([[#L63]]; [[#L75-L79]]; [[#L112]]) The comment defines $\alpha = \tfrac12\,d\ln(J/M)/d\ln r$, as in Zahn (1992), and uses $2V - \alpha U$. The code computes `ALPHA` $= d\ln(r^2\Omega)/d\ln r$, with no ½, and then `V - ALPHA*HV`, where `V` is already $2V$. So the code's denominator is $2V - 2\alpha U$, and the $\alpha$ term is twice what the comment gives, which changes $f_c$ wherever that term matters. Only with `LVFC` (off by default; "experimental" in the Physics namelist page).

    **A possible fix** (unless the comment is the slip):

    ```diff
    --- a/src/getfc.f
    +++ b/src/getfc.f
    @@ -72,9 +72,12 @@
              GOTO 9999
           ENDIF
     C DETERMINE ALPHA.
    +C 11/09/26 KC via Claude
    +C code changed to include the factor 1/2 of the comment's
    +C ALPHA=1/2 D(LN J/M)/D LN R.
           DO I = IMIN,IMAX
              WM = 0.5D0*(OMEGA(I)+OMEGA(I-1))
    -         ALPHA(I) = (OMEGA(I)*HRU(I)**2-OMEGA(I-1)*HRU(I-1)**2)/
    +         ALPHA(I) = 0.5D0*(OMEGA(I)*HRU(I)**2-OMEGA(I-1)*HRU(I-1)**2)/
          *              (HRU(I)-HRU(I-1))/(WM*RM(I))
           END DO
     C DETERMINE 2V.
    ```

    **How the code itself shows it.** The routine carries the comment's factors into `V` but not into `ALPHA`. The comment defines $V = 1/(6\rho r)\,d(\rho r^2 U)/dr$ ([[#L64]]); the loop under "DETERMINE 2V." ([[#L80]]) computes `V(I) = CC13*(DR2VP-DR2VM)/RHOR/(HRU(I)-HRU(I-1))` ([[#L89]]), with `CC13` = 1/3, twice the comment's 1/6, and [[#L99]] and [[#L105]] do the same at the end shells. For `ALPHA`, [[#L77-L78]] compute $d(\Omega r^2)/dr$ divided by $\Omega r$, that is $d\ln(r^2\Omega)/d\ln r$. YREC's $J/M$ is $\Omega$ times $I/M$ (`HJM(J) = OMEGA(J)*HI(J)`, [[getnewenv.f#L297]]), with $I/M = \tfrac23 r^2$ as MIDMOD's first guess (`HIM(I) = CC23*EXP(CLN*2.0D0*HRM(I))`, [[midmod.f#L493]]), so `ALPHA` is the comment's $d\ln(J/M)/d\ln r$ in full, without the ½ of [[#L63]]. [[#L112]] then takes `V(I)-ALPHA(I)*HV(I)`: the comment's $2V$ with twice its $\alpha U$. Is the comment's ½, the factor of Zahn (1992) it cites, the one intended?

    **Checked by running YREC** (Nov 9 and 10, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): None of the five rotating test cases (`testsuite/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2`, `testsuite/Test_solarGS98_difrotmixper18p4d1p0`, `testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`, `testsuite/Test_m2p0_feh+0p0_vzams150_IES1_TAMS`, and `testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS`) reaches it, since none sets `LVFC`. No namelist in the repository does: Those that list it set it false, with the comment "Not recommended (disables FC setting.)," and the documentation lists it among the experimental options (`docs/source/namelist_physics.md`, line 298). So on Nov 10, `testsuite/Test_m2p0_feh+0p0_vzams150_IES1_TAMS` (2 $M_\odot$, solid-body rotation at about 148 km/s at the start, run from the ZAMS to the TAMS) was run with only `LVFC` switched on: a documented option that YREC's own namelists call "Not recommended," which replaces the case's constant `FC` = 0.033 with the variable factor computed here. GETFC then computed $f_c$ at 536,252 shells over the run (shells 2 to 758), at every iteration of SECULR ([[seculr.f#L192]], [[seculr.f#L232]]). At all but 370 of them, the factor ½ of the comment would change $f_c$ by more than 1%, by factors from 0.03 to 31. With the factor ½ (the fix above), the star mixes more: The main sequence lasts 1.357 Gyr instead of 1.344 Gyr (635 models instead of 624); before central $X$ falls below 0.05, surface $^{14}$N rises by up to 0.0039 dex, against $7 \times 10^{-6}$ dex for a null change (nearly every opacity, all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$, times $1 + 10^{-10}$, the noise floor); surface $X$ falls by up to $4.9 \times 10^{-5}$, against $4.8 \times 10^{-7}$; central $X$ differs by up to 0.018, against 0.002; and $\log L$ by up to 0.0075 dex, against 0.0011 dex. The effect is small but well above the noise, in a setting YREC does not recommend. Intent: The comment ([[#L63]]) gives the factor ½, so either the code or the comment is the slip.

### GETFC

Zahn (1992) ratio $f_c$ of the chemical to the angular-momentum diffusion coefficient, per shell, capped at 1 (equations above).
