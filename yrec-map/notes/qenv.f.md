## Explanation

**Purpose.** The right-hand side of the envelope integration: with $\log P$ as the independent variable, it returns the derivatives of $\log m$ (relative to the total), $\log T$ and $\log r$, from hydrostatic equilibrium, mass conservation and the temperature gradient.

**How it fits.**
- **Inputs:** `X0` $=\log P$; `Y(1..3)` $= \log(m/M_\ast)$, $\log T$, $\log r$; the luminosity `B`, the distortion factors `FPL`, `FTL`, `TEFFL`, $X$, $Z$; `STOTAL` ($\log M_\ast$) from [[comp_mod.f#COMP_MOD|`COMP_MOD`]]; the mixing length `CMIXLQ` from [[qenvmix_mod.f#QENVMIX_MOD|`QENVMIX_MOD`]], set by `ENVINT` before every path that reaches `QENV` (the argument list must stay that of the `EXTERNAL` derivative routine, so `CMIXL` cannot be passed); `LPUMOD` from [[pulse1_mod.f#PULSE1_MOD|`PULSE1_MOD`]].
- **Who calls it:** [[envint.f#ENVINT|ENVINT]], directly and as the `EXTERNAL` derivative routine passed to [[bsstep.f#BSSTEP|BSSTEP]] and [[mmid.f#MMID|MMID]].
- **What it calls:** [[eqstat.f#EQSTAT|EQSTAT]], [[getopac.f#GETOPAC|GETOPAC]], and [[tpgrad.f#TPGRAD|TPGRAD]] (with `CMIXLQ`, and with `IOVIM = -1` in [[dpmix_mod.f#DPMIX_MOD|`DPMIX_MOD`]], so no overshoot point is flagged).
- **Outputs:** `DYDX(1..3)`; the counter `KENV`; the point's structure, gradients, $\beta$, convective velocity and ionization fractions in [[envprt_mod.f#ENVPRT_MOD|`ENVPRT_MOD`]] (always, since 07/02, 08/13 and 08/25), read by ENVINT, [[getnewenv.f#GETNEWENV|GETNEWENV]] and [[starin.f#STARIN|STARIN]]; and the quantities for pulsation output in [[pulse2_mod.f#PULSE2_MOD|`PULSE2_MOD`]] when saving. `EFXION`, `QQDP`, `QQDT` and `QQCP` are set always ([[#L89-L94]]) and again, to the same values, inside `IF(LSAVE .OR. LPUMOD)` ([[#L107-L109]], [[#L120]], [[#L125]], [[#L127]]); the second assignments are redundant.

**The method.** With $f_P$ = `FPL`,
$$\frac{d\log m}{d\log P} = -\frac{4\pi r^4 P}{G m^2 f_P},\qquad \frac{d\log T}{d\log P} = \nabla,\qquad \frac{d\log r}{d\log P} = -\frac{r P}{G m \rho}\,f_P,$$
with $\nabla$ from `TPGRAD` ([[#L72-L74]]; on $f_P$ in the last, suspected bug 1).

**Changed since `rp_1`.** The MHD equation of state removed: `EQSTAT` is always called (no `LMHD`, no `MEQOS`); `TPGRAD` takes the mixing length as a new last argument, `CMIXLQ` from `QENVMIX_MOD`; COMMON blocks to modules (the unused `/PULSE/`, `/FLAG/` and `/MHD/` dropped), `IMPLICIT NONE`.

## Bugs, by priority

1. **(a)** **The distortion factor in $d\log r/d\log P$.** ([[#L72]]; [[#L74]]) The interior equations in [[coefft.f#COEFFT|COEFFT]] have $d\log P/d\log m \propto f_P$ and $d\log r/d\log m$ without $f_P$ ([[coefft.f#L247-L252]]); dividing gives $d\log r/d\log P \propto 1/f_P$. `QENV` divides by $f_P$ in $d\log m/d\log P$ (consistent) but *multiplies* by it in $d\log r/d\log P$. What follows: In a rotating model the slope $d\log r/d\log P$ is $f_P^2$ times the one COEFFT's form gives, so the fitting point's $\log r$ (`RS`) and the boundary plane of [[surfbc.f#SURFBC|SURFBC]] are off; the effect is small where $f_P \approx 1$. Only with rotation (`LROT`, off by default; [[crrect.f#CRRECT|CRRECT]] passes $f_P$ of the outermost point, otherwise 1). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to divide d log r/d log P by FPL, as the interior
    C equations of COEFFT imply (FPL multiplies d log P/d log m only).
          DYDX(3) = -DEXP(CLN*(PL+RL-CGL-SL-DL))/FPL
    ```
