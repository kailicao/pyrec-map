## Explanation

**Purpose.** This file computes the conductive opacity for a mixture of hydrogen, helium and metals from Potekhin's conductivity tables ("based on Chris Burke's conductive opacity code," LLP 5/31/04). [[getopac.f#GETOPAC|GETOPAC]] then adds it to the radiative opacity in harmonic sum.

**How it fits.**
- **Inputs:** the arguments `DL` ($\log\rho$), `TL` ($\log T$), `X`, `Z`, and `FXION`, the ionization fractions (of H; of He singly and doubly).
- **Who calls it:** [[getopac.f#GETOPAC|GETOPAC]], when the Potekhin option (`LcondOpacP`) is on.
- **What it calls:** [[condopacp.f#CONDOPACP|CONDOPACP]], for $Z_\mathrm{ion}$ = 1, 2 and 8.
- **Outputs:** `OC` and `OCL` (the conductive opacity and its log), `QODC`, `QOTC` (its derivatives in $\log\rho$ and $\log T$), and `LCONDO` (true if computed). If `LCONDO` is false, GETOPAC falls back to the Hubbard–Lampe formula or uses no conductive opacity.

**The method.**
1. Number fractions of H, He and metals (taken as oxygen, $A = 16$), $w_k = (X_k/A_k)/\sum_j(X_j/A_j)$, then weighted by ionization: $w_\mathrm{H} f_\mathrm{H^+}$, $w_\mathrm{He}(f_\mathrm{He^+} + 2f_\mathrm{He^{2+}})/2$; metals are taken as fully ionized.

    > **Question** ([[#L30-L40]]). **Weights by number of ions.** The comment says the weights count only charged atoms; for helium the weight $(f_1 + 2f_2)/2$ mixes ion number and charge. Is this what Chris Burke's code did?

2. Inside $3 \le \log T \le 9$, $-6 \le \log\rho \le 9.75$: the conductivity $K_k$ of each pure composition from CONDOPACP, combined as
$$\frac{1}{K} = \sum_k \frac{w_k}{K_k},$$
and the conductive opacity
$$\kappa_\mathrm{cond} = \frac{16\,\sigma\,T^3}{3\,\rho\,K}, \qquad \log\kappa_\mathrm{cond} = -3.5194 + 3\log T - \log\rho - \log K,$$
with $\log(16\sigma/3) = -3.5194$ in cgs. Its derivatives are $\partial\log\kappa/\partial\log\rho = -1 - \partial\log K/\partial\log\rho$ and $\partial\log\kappa/\partial\log T = 3 - \partial\log K/\partial\log T$.
   These limits are the table's edges (see the suspected bug 1 of [[condopacp.f#CONDOPACP|CONDOPACP]], [[condopacp.f#L99-L109]], for the upper ones).

    > **Question** ([[#L21]]; [[#L41]]; [[#L58]]). **The metals.** All metals are represented by $Z_\mathrm{ion} = 8$ with $A = 16$ and full ionization; the comment justifies this by their low abundance. Fine for the Sun; for metal-rich or evolved cores (C/O), is it adequate?

3. Below $\log\rho = -6$, where $\log R = \log\rho - 3(\log T - 6) \ge 0$ (so only for $\log T < 4$): evaluate at $\log\rho = -6$ and extrapolate linearly in $\log\rho$ with the hydrogen table's slope; $\partial\log\kappa/\partial\log T$ is hydrogen's alone, at $\log\rho = -6$.
4. Elsewhere, `LCONDO` stays false, and `OC` is left at $10^{9.9998}$ with `QODC = QOTC = OC`; GETOPAC then either returns before using them ($\log T < 4.2$, or low density) or replaces them with the Hubbard–Lampe formula.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

## Bugs, by priority

1. **(changes results, small)** **Checked by KC** (Nov 10, 2026). **The mixture's derivatives are multiplied by $\log K$.** ([[#L68]]; [[#L72]]) `QODC = CONDL * (WtH1*QODCX + …)` multiplies the weighted derivatives by `CONDL` = $\log K$ itself. The derivative of the harmonic sum $1/K = \sum_k w_k/K_k$ is $\partial\log K/\partial\log\rho = \sum_k (w_k K/K_k)\,\partial\log K_k/\partial\log\rho$, with no factor $\log K$: For pure hydrogen ($w_\mathrm{H} = 1$) the code gives $\log K$ times the right value. The commented-out older lines ([[#L69-L70]], [[#L73-L74]]) weight each derivative by its `CONDX`, as the fix below does, but also multiply by `CONDL`. What follows: `QODC` and `QOTC` are wrong wherever Potekhin's opacity is computed ($\log\rho \ge -6$), and `GETOPAC` folds them into the opacity's derivatives `QOD` and `QOT` with the weight $\kappa_\mathrm{rad}/(\kappa_\mathrm{rad} + \kappa_\mathrm{cond})$ ([[getopac.f#L219-L222]]), so the error counts where conduction matters (degenerate cores). Only with `LcondOpacP` (off by default, set in all 51 decks of the test suite and recommended by the user guide).

    **A possible fix:**

    ```diff
    --- a/src/condopacpint.f
    +++ b/src/condopacpint.f
    @@ -65,7 +65,11 @@
     c           CONDL = LOG10( (X + 1D0) / 2D0 ) -
     c     *             LOG10( X*CONDX + .5D0*Y*CONDY + .5D0*z*CONDZ)
     
    -           QODC = CONDL * (WtH1*QODCX + WtHe4*QODCY + WtOx*QODCZ)
    +C 11/09/26 KC via Claude
    +C code changed to take the derivative of the harmonic sum: each
    +C composition weighted by its share of 1/K, WT*CONDX*K, K = 10**CONDL.
    +           QODC = 10.0D0**CONDL*(WtH1*CONDX*QODCX + WtHe4*CONDY*QODCY
    +     *            + WtOx*CONDZ*QODCZ)
     c           QODC = 2D0 * CONDL / ( 1D0 + X ) *
     c     *          (X*CONDX*QODCX +.5D0*Y*CONDY*QODCY +.5D0*Z*COBDZ*QODCZ)
     
    ```

    **How the code itself shows it.** The routine's own lines fix what `QODC` must be. [[condopacp.f#CONDOPACP|`CondOpacP`]], which it calls, defines its outputs as $\log_{10}$ of the thermal conductivity $K$ and plain log derivatives ([[condopacp.f#L22-L24]]: "`DRK` - d log kappa / d log rho," "`DTK` - d log kappa / d log T"). [[#L76-L77]] build the opacity as `OCL = -3.5194D0+3.0D0*TL-DL-CONDL`, that is $\kappa_\mathrm{cond} = 16\sigma T^3/(3\rho K)$, and its density derivative as `-1.0D0-QODC`, so `QODC` must be $\partial$`CONDL`$/\partial\log\rho$: For pure, fully ionized hydrogen that is hydrogen's `DRK` itself, while [[#L68]] gives `CONDL` times it. The same routine's branch below $\log\rho = -6$ uses `DRK` exactly so, with no factor `CONDL`, both as the derivative and as the slope it extrapolates along ([[#L84]], [[#L97-L99]]). YREC's other conductive opacity, Hubbard and Lampe's in GETOPAC, returns `QODC = 0.3901D0*TL - 0.2772D0*DL - 3.5853D0` ([[getopac.f#L206-L211]]), exactly the density derivative of its own formula, and GETOPAC combines either option's `QODC` with the radiative one in the same way ([[getopac.f#L219-L222]]); both options must therefore deliver the same quantity, and only this branch does not. The factor is not small: `CONDL`, $\log_{10}K$, runs from about 1.1 to 19.3 in the table `condall06.d`. The combined derivatives reach the iteration's matrix ([[coefft.f#L263-L264]]) and, in rotating runs, the meridional circulation through $\partial\ln\chi/\partial\ln T = 3 - \partial\ln\kappa/\partial\ln T$ ([[setupv.f#L431-L433]]), each weighted by $\kappa_\mathrm{rad}/(\kappa_\mathrm{rad}+\kappa_\mathrm{cond})$, which goes to 1 where conduction dominates: The error counts most in degenerate cores, which no run with the fix reached. The fix above is the derivative of the harmonic sum the routine builds at [[#L64]]; the commented-out older lines ([[#L69-L70]]) already weight each element by its `CONDX`.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): 34 runs, 26 of YREC's cases (from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning) and 8 made-up ones (each one of YREC's cases with a few settings changed), of which one stopped in its first second. The step ran in all 33 others, from 0.06 million to 74 million times a run, at $\log T$ = 3 to 8.40 and $\log\rho$ = −6 to 7.45, and the derivative differed from the right one by more than 0.001 in nearly every call (74,434,834 of 74,434,834 in `testsuite/Test_m9p0feh+0p0GS98_base_TAHB`). With the fix, `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` moves by up to $1.4\times10^{-5}$ dex in $\log L$ and $7.1\times10^{-6}$ dex in $\log T_c$, against $1\times10^{-9}$ and $8\times10^{-11}$ for the null change used as a noise floor (nearly every opacity, all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$, times $1 + 10^{-10}$): real, but small (259 models in both, end age 5.23952 Gyr instead of 5.23984). On the 3 $M_\odot$ giant `testsuite/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2`, the change is within the noise: $\log L$ moves by up to 0.0037 dex and $\log T_c$ by 0.0015, against 0.0076 and 0.0008 for the null change (1,847 models instead of 1,853). Not run with the fix: a degenerate core (`testsuite/Test_m1p0feh+0p0GS98_base_HeIgnite`), where conduction matters most. `QOD` and `QOT` enter the solver's derivatives ([[tpgrad.f#TPGRAD|TPGRAD]], [[coefft.f#COEFFT|COEFFT]]), which fits so small a change. Intent: The commented-out older lines also multiply by `CONDL`.

2. **(changes results, small)** **Checked by KC** (Nov 10, 2026). **The temperature derivative is taken from the density derivatives.** ([[#L72]]) `QOTC` is computed from `QODCX`, `QODCY`, `QODCZ`, not from `QOTCX`, `QOTCY`, `QOTCZ` (which the calls at [[#L56-L58]] return and nothing reads), so $\partial\log\kappa/\partial\log T$ is $3 - \partial\log K/\partial\log\rho$ (and multiplied by $\log K$, the factor of [[#b1]]). The commented-out older lines [[#L73-L74]] used `QOTCX`, `QOTCY`, `QOTCZ`. Same path as [[#b1]]: Potekhin's opacity with `LcondOpacP` (off by default, set in all 51 decks of the test suite), at $\log\rho \ge -6$.

    **A possible fix** (in the form of the fix of [[#b1]], each composition weighted by its share of $1/K$, with no factor $\log K$):

    ```diff
    --- a/src/condopacpint.f
    +++ b/src/condopacpint.f
    @@ -69,7 +69,11 @@
     c           QODC = 2D0 * CONDL / ( 1D0 + X ) *
     c     *          (X*CONDX*QODCX +.5D0*Y*CONDY*QODCY +.5D0*Z*COBDZ*QODCZ)
     
    -            QOTC = CONDL * (WtH1*QODCX + WtHe4*QODCY + WtOx*QODCZ)
    +C 11/09/26 KC via Claude
    +C code changed to take the temperature derivatives QOTCX, QOTCY and
    +C QOTCZ, weighted as the density derivatives are.
    +            QOTC = 10.0D0**CONDL*(WtH1*CONDX*QOTCX + WtHe4*CONDY*QOTCY
    +     *             + WtOx*CONDZ*QOTCZ)
     c           QOTC = 2D0 * CONDL / ( 1D0 + X ) *
     c     *          (X*CONDX*QOTCX +.5D0*Y*CONDY*QOTCY +.5D0*Z*CONDZ*QOTCZ)
     
    ```

    **How the code itself shows it.** `QOTC` must be $\partial$`CONDL`$/\partial\log T$: [[#L76]] builds the opacity as `OCL = -3.5194D0+3.0D0*TL-DL-CONDL` and [[#L78]] its temperature derivative as `3.0D0-QOTC`. [[condopacp.f#CONDOPACP|`CondOpacP`]] returns that derivative for each element as its last argument, "`DTK` - d log kappa / d log T" ([[condopacp.f#L24]]), and the calls at [[#L56-L58]] store it in `QOTCX`, `QOTCY`, and `QOTCZ`, which nothing reads; [[#L72]] uses the density derivatives `QODCX`, `QODCY`, and `QODCZ` instead, the same expression as `QODC` on [[#L68]]. The commented-out older line it replaced ([[#L73-L74]]) reads `QOTCX`, `QOTCY`, and `QOTCZ`. YREC's other conductive opacity, Hubbard and Lampe's in GETOPAC, returns `QOTC = 0.3901D0*DL - 0.6438D0*TL + 5.1324D0` ([[getopac.f#L206-L211]]), the temperature derivative of its own formula, which GETOPAC combines with the radiative one as it does this routine's ([[getopac.f#L219-L222]]).

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The step ran as for [[#b1]] (in 33 of the 34 runs, from 0.06 million to 74 million times a run), and the temperature and density derivatives differed by more than 0.001 in nearly every call (74,434,834 of 74,434,834 in `testsuite/Test_m9p0feh+0p0GS98_base_TAHB`). With this bug's fix alone (the temperature derivatives, still times `CONDL`; measurement only), `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` moves by up to $5.0\times10^{-6}$ dex in $\log L$ and $6.0\times10^{-6}$ dex in $\log T_c$, against $1\times10^{-9}$ and $8\times10^{-11}$ for the null change: real, but small (259 models in both, end age 5.24007 Gyr instead of 5.23984). On the 3 $M_\odot$ giant the change is within the noise: $\log L$ moves by up to 0.0050 dex and $\log T_c$ by 0.00066, against 0.0076 and 0.0008 for the null change. Not run with the fix: a degenerate core. Intent: The commented-out older lines [[#L73-L74]] took `QOTCX`, `QOTCY`, and `QOTCZ`.

3. **(changes results, small)** **Checked by KC** (Nov 10, 2026). **A sign in the extrapolation below $\log\rho = -6$.** ([[#L92]]; [[#L64]]) In step 3, `CONDL = LOG10(…)`, while in step 2 `CONDL = -LOG10(…)`, with the same sum inside. Since $\sum_k w_k/K_k = 1/K$, step 2 gives $\log K$ but step 3 gives $-\log K$, so the extrapolated $\log\kappa_\mathrm{cond}$ ([[#L96]]) is off by $2\log K$. Probably a missing minus sign. The path: `LcondOpacP`, $\log\rho < -6$ and $\log R \ge 0$, so only for $\log T < 4$ (cool surface layers); `GETOPAC` uses the result whenever `LCONDO` is true ([[getopac.f#L197]]). How much the total opacity changes there was not traced.

    **A possible fix:**

    ```diff
    --- a/src/condopacpint.f
    +++ b/src/condopacpint.f
    @@ -89,7 +89,9 @@
                CONDY = 10.0D0**(-CONDYL)
                CONDZ = 10.0D0**(-CONDZL)
     
    -           CONDL = LOG10(WtH1*CONDX + WtHe4*CONDY + WtOx*CONDZ)
    +C 11/09/26 KC via Claude
    +C code changed to give CONDL the sign it has above, log K.
    +           CONDL = -LOG10(WtH1*CONDX + WtHe4*CONDY + WtOx*CONDZ)
     c           CONDL = LOG10( (X + 1D0) / 2D0 ) -
     c     *            LOG10( X*CONDX + .5D0*Y*CONDY + .5D0*Z*CONDZ)
     
    ```

    **How the code itself shows it.** The two steps compute the same quantity: [[#L88-L90]] repeat [[#L60-L62]], `CONDX = 10.0D0**(-CONDXL)` and its twins, so each `CONDX` is $1/K_k$ and the sum inside both logarithms is $1/K$. Step 2 takes `CONDL = -LOG10(…)` ([[#L64]]), and so does the older formula commented out under each step, `CONDL = LOG10( (X + 1D0) / 2D0 ) -` followed by `LOG10( X*CONDX + .5D0*Y*CONDY + .5D0*Z*CONDZ)` ([[#L93-L94]]; [[#L65-L66]] the same, with `z`): a minus before the logarithm of the sum. Step 3's opacity, `OCL = -3.5194D0+3.0D0*TL+6.0D0-CONDL` ([[#L96]]), is step 2's `OCL = -3.5194D0+3.0D0*TL-DL-CONDL` ([[#L76]]) at `DL` = −6, which needs the same `CONDL`, $\log_{10}K$; with the opposite sign the two opacities do not meet at $\log\rho = -6$, where the extrapolation starts. The fix gives [[#L92]] the sign of [[#L64]] and of both commented formulas.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The extrapolation ran in 21 of the 33 runs, from 41,369 to 3.6 million times a run, at $\log T$ = 3 to 4.00 and $\log\rho$ = −8.99 to −6, mostly the low-mass and solar models; `CONDL` had the wrong sign in every call. With the fix, the 0.04 $M_\odot$ brown dwarf `examples/run_from_dbl_to_zams/Test_m0040_feh0_noGS_ZAMS` moves by up to $2.4\times10^{-4}$ dex in $\log L$ and $3.6\times10^{-5}$ dex in $\log T_\mathrm{eff}$, against $2.5\times10^{-5}$ and $1.2\times10^{-5}$ for the null change: about ten times the noise in $\log L$, so real, but small (748 models in both, end age 8,692 Gyr instead of 8,681, against 8,687 for the null change). On `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` the change is $9\times10^{-9}$ dex in $\log L$, negligible. Intent: none found; the commented-out older line ([[#L93-L94]]) subtracts the log of the sum, as [[#L64]] does, so only [[#L92]] has the other sign.

4. **(harmless in the runs)** **The step of the extrapolation is reversed.** ([[#L99]]) `OCL = OCL + QODC*(-6.0D0-DL)` adds the slope times $(-6 - \log\rho)$, where a linear extrapolation from $\log\rho = -6$ adds the slope times $(\log\rho + 6)$; the extrapolated opacity moves the wrong way as the density falls. Same path as [[#b3]]: `LcondOpacP`, $\log\rho < -6$ and $\log R \ge 0$, so only for $\log T < 4$ (cool surface layers).

    **A possible fix:**

    ```diff
    --- a/src/condopacpint.f
    +++ b/src/condopacpint.f
    @@ -96,7 +96,9 @@
                OCL = -3.5194D0+3.0D0*TL+6.0D0-CONDL
                QODC = -1.0D0-QODC
                QOTC = 3.0D0-QOTC
    -           OCL = OCL + QODC*(-6.0D0-DL)
    +C 11/09/26 KC via Claude
    +C code changed to extrapolate from log rho = -6 down to DL.
    +           OCL = OCL + QODC*(DL+6.0D0)
                OC = 10.0D0**OCL
                LCONDO=.TRUE.
              END IF
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The step ran as for [[#b3]] (in 21 of the 33 runs, from 41,369 to 3.6 million times a run), and the extrapolation went the wrong way by more than 0.01 dex in nearly every call (3,629,479 of 3,630,172 in `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS`). With the fix, the brown dwarf `examples/run_from_dbl_to_zams/Test_m0040_feh0_noGS_ZAMS` moves by up to $9.5\times10^{-5}$ dex in $\log L$ and $7.6\times10^{-6}$ dex in $\log T_c$, against $2.5\times10^{-5}$ and $1.5\times10^{-6}$ for the null change: four to five times the noise, so small, and not clearly real (748 models in both). The track of `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` is identical with the fix. The extrapolated opacity is wrong in nearly every call, silently, but even the brown dwarf, which takes the path most often (3.2 million times), shows no change clearly above the noise. Intent: none found.

### CONDOPACPINT

Conductive opacity for an H/He/metal mixture: harmonic sum of Potekhin's conductivities for $Z_\mathrm{ion}$ = 1, 2, 8 weighted by ionized number fractions, then $\kappa_\mathrm{cond} = 16\sigma T^3/(3\rho K)$; linear extrapolation below $\log\rho = -6$.
