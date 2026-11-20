## Explanation

**Purpose.** `EQSCVE` interpolates the Saumon–Chabrier–Van Horn (SCV) equation of state in its table for the surface (envelope) composition. It returns the density, the thermodynamic derivatives and the ionization fractions of hydrogen and helium. For any other composition it hands the work to [EQSCVG](eqscvg.f.md#eqscvg), which combines the pure-hydrogen, pure-helium and metal tables.

**How it fits.**
- **Who calls it:** only [EQSTAT2](eqstat2.f.md#eqstat2), when `LSCV` is set and $`\log T \lt{}`$ `TSCUT`, right after [EQSAHA](eqsaha.f.md#eqsaha). If the point is outside the table (`LCALC` false), the routine returns without touching its outputs, so the `EQSAHA` values stand.

    > **Question** ([eqstat2.f, lines 181–187](https://github.com/yreclab/yrec/blob/7be4133/src/eqstat2.f#L181-L187); [eqsaha.f, lines 194–196](https://github.com/yreclab/yrec/blob/7be4133/src/eqsaha.f#L194-L196)). **Mixed EOS outputs.** When SCV succeeds, `EQSTAT2` keeps `RMU`, `EMU` and the second derivatives from `EQSAHA`, while the density comes from SCV. So $`\mu`$ is no longer consistent with $`\rho = \beta P\mu/(\mathcal{R}T)`$ (below the transition band, where `EQSTAT2` does not recompute `RMU`). `RMU` is read later by [hsubp.f, line 74](https://github.com/yreclab/yrec/blob/7be4133/src/hsubp.f#L74) and `EMU` by [sconvec.f, line 223](https://github.com/yreclab/yrec/blob/7be4133/src/sconvec.f#L223). Is that intended?

- **Inputs:** `TL`, `T`, `P`, `BETA`, `X`, `Z`. It compares `X`, `Z` with `XENV`, `ZENV` from `/COMP/`.
- **What it calls:** [KSPLINE](kspline.f.md#kspline) and [KSPLINT](ksplint.f.md#ksplint) (a four-point natural spline), [INTERP](interp.f.md#interp) (four-point Lagrange) and `EQSCVG`.
- **Outputs:** `DL`, `D`, `QDT`, `QDP`, `QCP`, `DELA`, `FXION`, `LCALC`.
- **Modules:** `SCVEOS_MOD` holds the tables (`TLOGX`, `TABLENV` for the envelope mixture, `TABLEX`, `TABLEY`, `TABLEZ`, `SMIX`, `NPTSX`) and the last indices `IDTSCV`, `IDP`; it is filled by [SETSCV](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L4-L255) and used also by `EQSCVG` and [SETUPS](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L16-L396). The flag `LSCV` is now in `NMLPAR_MOD`. `COMP_MOD` gives the envelope composition; `CONSTANTS_MOD` the constants.

**The method.**
1. The table is in $`\log T`$ and $`\log P_\mathrm{gas}`$, with $`P_\mathrm{gas} = \beta P`$. Out of table if $`\log T`$ is outside `TLOGX`, if $`\log P_\mathrm{gas} \lt{} 4`$, or if it is above the last pressure of the stencil's lowest-temperature row.
2. Find the $`4\times4`$ stencil (`IDTSCV`, `IDP`), starting from the last one. For each of the 4 temperatures, a natural spline in $`\log P_\mathrm{gas}`$ gives five quantities (columns 2–6 of `TABLENV`: $`\log\rho`$, $`Q_{\rho T}`$, $`Q_{\rho P}`$, $`c_P`$, $`\partial U/\partial T`$); a second spline in $`\log T`$ gives their values at the point. Column 5, the tabulated $`c_P`$ (`TEMPT(4)`, `QCP0`), is interpolated but never used, since step 4 rebuilds $`c_P`$ from $`\partial U/\partial T`$: unused? ([line 384](https://github.com/yreclab/yrec/blob/7be4133/src/eqscve.f#L384)).

    **One pressure grid serves all four temperatures.** The pressure abscissae are always taken from the row `IDTSCV`, the lowest temperature of the stencil, also for the other three rows ([lines 102–103](https://github.com/yreclab/yrec/blob/7be4133/src/eqscve.f#L102-L103); [lines 164–166](https://github.com/yreclab/yrec/blob/7be4133/src/eqscve.f#L164-L166)), and the ionization step (5) uses `TABLENV`'s pressures, which are `TABLEX`'s ([setscv.f, line 165](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L165)), for `TABLEX` and `TABLEY` too ([lines 407–409](https://github.com/yreclab/yrec/blob/7be4133/src/eqscve.f#L407-L409)). That is right: In `input/eos/scv`, every row of `h_tab_i.dat` and `he_tab_i.dat` (63 temperatures) is a prefix of one grid, $`\log P_\mathrm{gas} = 4.00`$, $`4.20`$, …, its length growing with $`T`$ from 30 to 76 points, so the row `IDTSCV` is the shortest of the stencil and its pressures are those of the three hotter rows; the metal table `z_tab_i.dat`, read in reverse order ([setups.f, lines 388–389](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L388-L389)), has the same pressures row by row (checked from the files, Nov 10, 2026).

3. **Smoothing at stencil changes.** When the point is within `TOLST` = 0.032 in $`\log T`$ (or `TOLSP` = 0.08 in $`\log P`$) of the edge of the middle interval, the routine also interpolates on the stencil shifted by one, and blends the two linearly (`FST`, `FSP`), so that the result does not jump when the stencil changes.
4. **Radiation.** The tables hold the gas alone. With $`Q_{\rho P,0}`$ and $`Q_{\rho T,0}`$ from the table,
   
   $$\displaystyle Q\_{\rho P} = \frac{Q\_{\rho P,0}}{\beta},\qquad \chi\_T = \beta\left(-\frac{Q\_{\rho T,0}}{Q\_{\rho P,0}}\right) + 4(1-\beta),\qquad Q\_{\rho T} = -\chi\_T\\,Q\_{\rho P},$$
   
   $$\displaystyle \frac{\partial U}{\partial T} \mathrel{+}= \frac{4}{T}\cdot\frac{3P\_\mathrm{rad}}{\rho},\qquad c\_P = \frac{\partial U}{\partial T} - \frac{P}{\rho T}Q\_{\rho T}\chi\_T,\qquad \nabla\_\mathrm{ad} = -\frac{P\\,Q\_{\rho T}}{\rho T\\,c\_P}.$$
5. **Ionization.** From the pure-hydrogen table `TABLEX` and the pure-helium table `TABLEY` (columns 2 and 3, Lagrange interpolation on the same stencil and pressure abscissae as `TABLENV`), the particle fractions of $`\mathrm{H_2}`$, H, He and $`\mathrm{He^+}`$; charge and particle conservation give the rest, and
   
   $$\displaystyle x\_{\mathrm{H}^+} = \frac{n\_{\mathrm{H}^+}}{n\_{\mathrm{H}\_2} + n\_\mathrm{H} + n\_{\mathrm{H}^+}}, \quad x\_{\mathrm{He}^+} = \frac{n\_{\mathrm{He}^+}}{n\_\mathrm{He} + n\_{\mathrm{He}^+} + n\_{\mathrm{He}^{++}}},$$
   
   and likewise for $`\mathrm{He^{++}}`$ (the code's formula for $`\mathrm{H^+}`$; see bug 1).

    > **Question** ([lines 403–425](https://github.com/yreclab/yrec/blob/7be4133/src/eqscve.f#L403-L425); [lines 162–190](https://github.com/yreclab/yrec/blob/7be4133/src/eqscve.f#L162-L190)). **Spline and Lagrange.** The thermodynamic quantities use splines, the ionization fractions Lagrange interpolation without the smoothing of step 3. Is the difference intended?

**Changed since `rp_1`.** Declarations (COMMON blocks to modules, `IMPLICIT NONE`); the saved temperature index `IDT` is renamed `IDTSCV` in `SCVEOS_MOD`, and the unused `/NMLPAR/` declaration is removed. The arithmetic is unchanged.

## Bugs, by priority

1. **(harmless in the runs)** **$`\mathrm{H_2}`$ counted as one hydrogen nucleus.** ([line 463](https://github.com/yreclab/yrec/blob/7be4133/src/eqscve.f#L463); [setscv.f, lines 58–59](https://github.com/yreclab/yrec/blob/7be4133/src/setscv.f#L58-L59)) In step 5 the denominator `XTF_H2 + XTF_H1 + XTF_HP` counts each $`\mathrm{H_2}`$ molecule once, but it holds two hydrogen nuclei, and the comment says the result is "the fraction XHP of hydrogen nuclei that are singly ionized" ([line 460](https://github.com/yreclab/yrec/blob/7be4133/src/eqscve.f#L460)). `SETSCV` counts the nuclei with the factor 2 for the same table columns (its `1+3*TABLEX(I,J,2)+TABLEX(I,J,3)` is twice $`2x_{\mathrm{H}_2} + x_\mathrm{H} + x_{\mathrm{H}^+}`$). So `FXION(1)` is too large wherever $`\mathrm{H_2}`$ is present; it is read by the conductive opacity ([condopacpint.f, line 39](https://github.com/yreclab/yrec/blob/7be4133/src/condopacpint.f#L39)) and written to the outputs. Where $`\mathrm{H_2}`$ is abundant, few H nuclei are ionized, so the absolute error is probably small; not traced. Only with `LSCV` (off by default, [nmlpar_mod.f, line 258](https://github.com/yreclab/yrec/blob/7be4133/src/nmlpar_mod.f#L258)).

    **A possible fix:**

    ```diff
    --- a/src/eqscve.f
    +++ b/src/eqscve.f
    @@ -460,7 +460,9 @@
     C We are seeking the fraction XHP of hydrogen nuclei that are singly ionized,
     C the fraction XHeP of helium huclei that are singly ionized and XHePP, the
     C helium fraction that is doubly ionized.
    -      XHP = XTF_HP / (XTF_H2 + XTF_H1 + XTF_HP)
    +C 11/09/26 KC via Claude
    +C code changed to count the two hydrogen nuclei of each H2 molecule.
    +      XHP = XTF_HP / (2D0*XTF_H2 + XTF_H1 + XTF_HP)
           XHeP = XTF_HeP / (XTF_He + XTF_HeP + XTF_HePP)
           XHePP = XTF_HePP / (XTF_He + XTF_HeP + XTF_HePP)
     
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged). The path was taken in 32 of the 34 cases run, from 28,366 to 40,729,900 times, at $`\log T`$ from 3.40 to 6, and $`\mathrm{H_2}`$ was present (the condition) in all 32, with a molecular fraction up to 0.80: in `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS`, for example, at 1,175,356 of 1,319,735 calls. With the page's fix, that case's track moves by at most $`10^{-11}`$ in $`\log L`$, against $`10^{-9}`$ for a null change (nearly every opacity, all with $`3 \le \log T \le 9`$ and $`-6 \le \log\rho \le 9.75`$, times $`1 + 10^{-10}`$), with the same 259 models and end age; in `testsuite/Test_m0p95feh+0p0_GN93_TAHB`, $`\log L`$ moves by at most $`3\times10^{-8}\,\mathrm{dex}`$ and $`\log T_\mathrm{eff}`$ by $`10^{-7}`$, against $`1.67\times10^{-7}`$ and $`1.54\times10^{-8}`$ for a null change, with the same 966 models and end age. Both runs' `.short` and `.store` files differ beyond 2%, which YREC's iterations make likely for almost any change. So the fix moves these tracks by no more than $`10^{-7}\,\mathrm{dex}`$, at the level of the noise. Intent: none found. The same miscount in [eqscvg.f, suspected bug 1](eqscvg.f.md#b1) changes a $`0.04\,M_\odot`$ track well beyond the noise, so a run whose envelope composition reaches such layers could show it here.

### EQSCVE

SCV equation of state at the envelope composition: 2D spline interpolation with smoothing at stencil changes, radiation added, ionization fractions from the H and He tables (method above). Hands other compositions to `EQSCVG`.
