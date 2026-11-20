## Explanation

**Purpose.** The right-hand side of the envelope integration: with $`\log P`$ as the independent variable, it returns the derivatives of $`\log m`$ (relative to the total), $`\log T`$ and $`\log r`$, from hydrostatic equilibrium, mass conservation and the temperature gradient.

**How it fits.**
- **Inputs:** `X0` $`=\log P`$; `Y(1..3)` $`= \log(m/M_\ast)`$, $`\log T`$, $`\log r`$; the luminosity `B`, the distortion factors `FPL`, `FTL`, `TEFFL`, $`X`$, $`Z`$; `STOTAL` ($`\log M_\ast`$) from [`COMP_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/comp_mod.f#L19-L34); the mixing length `CMIXLQ` from [`QENVMIX_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/qenvmix_mod.f#L19-L26), set by `ENVINT` before every path that reaches `QENV` (the argument list must stay that of the `EXTERNAL` derivative routine, so `CMIXL` cannot be passed); `LPUMOD` from [`PULSE1_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/pulse1_mod.f#L19-L39).
- **Who calls it:** [ENVINT](envint.f.md#envint), directly and as the `EXTERNAL` derivative routine passed to [BSSTEP](bsstep.f.md#bsstep) and [MMID](https://github.com/yreclab/yrec/blob/7be4133/src/mmid.f#L8-L55).
- **What it calls:** [EQSTAT](eqstat.f.md#eqstat), [GETOPAC](getopac.f.md#getopac), and [TPGRAD](tpgrad.f.md#tpgrad) (with `CMIXLQ`, and with `IOVIM = -1` in [`DPMIX_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/dpmix_mod.f#L19-L28), so no overshoot point is flagged).
- **Outputs:** `DYDX(1..3)`; the counter `KENV`; the point's structure, gradients, $`\beta`$, convective velocity and ionization fractions in [`ENVPRT_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/envprt_mod.f#L19-L35) (always, since 07/02, 08/13 and 08/25), read by ENVINT, [GETNEWENV](getnewenv.f.md#getnewenv) and [STARIN](starin.f.md#starin); and the quantities for pulsation output in [`PULSE2_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/pulse2_mod.f#L19-L45) when saving. `EFXION`, `QQDP`, `QQDT` and `QQCP` are set always ([lines 89–94](https://github.com/yreclab/yrec/blob/7be4133/src/qenv.f#L89-L94)) and again, to the same values, inside `IF(LSAVE .OR. LPUMOD)` ([lines 107–109](https://github.com/yreclab/yrec/blob/7be4133/src/qenv.f#L107-L109), [line 120](https://github.com/yreclab/yrec/blob/7be4133/src/qenv.f#L120), [line 125](https://github.com/yreclab/yrec/blob/7be4133/src/qenv.f#L125), [line 127](https://github.com/yreclab/yrec/blob/7be4133/src/qenv.f#L127)); the second assignments are redundant.

**The method.** With $`f_P`$ = `FPL`,
```math
\frac{d\log m}{d\log P} = -\frac{4\pi r^4 P}{G m^2 f_P},\qquad \frac{d\log T}{d\log P} = \nabla,\qquad \frac{d\log r}{d\log P} = -\frac{r P}{G m \rho}\,f_P,
```
with $`\nabla`$ from `TPGRAD` ([lines 72–74](https://github.com/yreclab/yrec/blob/7be4133/src/qenv.f#L72-L74); on $`f_P`$ in the last, suspected bug 1).

**Changed since `rp_1`.** The MHD equation of state removed: `EQSTAT` is always called (no `LMHD`, no `MEQOS`); `TPGRAD` takes the mixing length as a new last argument, `CMIXLQ` from `QENVMIX_MOD`; COMMON blocks to modules (the unused `/PULSE/`, `/FLAG/` and `/MHD/` dropped), `IMPLICIT NONE`.

## Bugs, by priority

1. **(harmless in the runs)** **The distortion factor in $`d\log r/d\log P`$.** ([line 72](https://github.com/yreclab/yrec/blob/7be4133/src/qenv.f#L72); [line 74](https://github.com/yreclab/yrec/blob/7be4133/src/qenv.f#L74)) The interior equations in [COEFFT](coefft.f.md#coefft) have $`d\log P/d\log m \propto f_P`$ and $`d\log r/d\log m`$ without $`f_P`$ ([coefft.f, lines 247–252](https://github.com/yreclab/yrec/blob/7be4133/src/coefft.f#L247-L252)); dividing gives $`d\log r/d\log P \propto 1/f_P`$. `QENV` divides by $`f_P`$ in $`d\log m/d\log P`$ (consistent) but *multiplies* by it in $`d\log r/d\log P`$. What follows: In a rotating model the slope $`d\log r/d\log P`$ is $`f_P^2`$ times the one COEFFT's form gives, so the fitting point's $`\log r`$ (`RS`) and the boundary plane of [SURFBC](surfbc.f.md#surfbc) are off; the effect is small where $`f_P \approx 1`$. Only with rotation (`LROT`, off by default; [CRRECT](crrect.f.md#crrect) passes $`f_P`$ of the outermost point, otherwise 1).

    **A possible fix:**

    ```diff
    --- a/src/qenv.f
    +++ b/src/qenv.f
    @@ -71,7 +71,10 @@
          *     LDERIV,LCONV,FPL,FTL,TEFFL,CMIXLQ)
           DYDX(1) = -DEXP(CLN*(C4PIL+4.0D0*RL+PL-CGL-SL-SL))/FPL
           DYDX(2) = DEL
    -      DYDX(3) = -DEXP(CLN*(PL+RL-CGL-SL-DL))*FPL
    +C 11/09/26 KC via Claude
    +C code changed to divide d log r/d log P by FPL, as the interior
    +C equations of COEFFT imply (FPL multiplies d log P/d log m only).
    +      DYDX(3) = -DEXP(CLN*(PL+RL-CGL-SL-DL))/FPL
           KENV = KENV + 1
     C 07/02 ALWAYS STORE THE BASIC STRUCTURE VARIABLES.
           EP = PL
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The condition ($`f_P \ne 1`$) held in all five rotating runs of 34 runs (26 of YREC's cases, from a 0.04 $`M_\odot`$ brown dwarf and the solar models to 9 $`M_\odot`$, rotation, and helium burning, and 8 made-up ones; one of these, with `FCORE` = 1.0, stopped in its first second), from about 2.4 million to 11.9 million envelope steps each, with `FPL` from 0.924 to 3.21. With the page's fix, in the rotating 3 $`M_\odot`$ case (`testsuite/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2`) the track moves within the noise ($`\log L`$ by up to $`0.00515\,\mathrm{dex}`$, against 0.00758 for a null change, nearly every opacity (all with $`3 \le \log T \le 9`$ and $`-6 \le \log\rho \le 9.75`$) times $`1 + 10^{-10}`$; 1,844 models instead of 1,853, against 1,839). In the rotating 0.8 $`M_\odot`$ case (`testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`), $`\log T_\mathrm{eff}`$ moves by up to 0.000105 and central $`X`$ by 0.000155, against 0.0000272 and 0.0000336 for a null change, four to five times the noise, while $`\log L`$ (0.000224 against 0.00014) and $`\log T_c`$ stay at it: not clearly above the noise. Both runs end normally. The slope is wrong in every rotating model (`FPL` reached 3.21), and the error (a factor $`f_P^2`$ in the slope) grows as $`f_P`$ departs from 1; the runs measured no clear effect at these rotation rates, and faster rotators were not run. Intent: none found.
