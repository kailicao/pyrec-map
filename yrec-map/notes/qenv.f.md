## Explanation

**Purpose.** The right-hand side of the envelope integration: with $\log P$ as the independent variable, it returns the derivatives of $\log m$ (relative to the total), $\log T$ and $\log r$, from hydrostatic equilibrium, mass conservation and the temperature gradient.

**How it fits.**
- **Inputs:** `X0` $=\log P$; `Y(1..3)` $= \log(m/M_\ast)$, $\log T$, $\log r$; the luminosity `B`, the distortion factors `FPL`, `FTL`, `TEFFL`, $X$, $Z$; `STOTAL` ($\log M_\ast$) from [[comp_mod.f#COMP_MOD|`COMP_MOD`]]; the mixing length `CMIXLQ` from [[qenvmix_mod.f#QENVMIX_MOD|`QENVMIX_MOD`]], set by `ENVINT` before every path that reaches `QENV` (the argument list must stay that of the `EXTERNAL` derivative routine, so `CMIXL` cannot be passed); `LPUMOD` from [[pulse1_mod.f#PULSE1_MOD|`PULSE1_MOD`]].
- **Who calls it:** [[envint.f#ENVINT|ENVINT]], directly and as the `EXTERNAL` derivative routine passed to [[bsstep.f#BSSTEP|BSSTEP]] and [[mmid.f#MMID|MMID]].
- **What it calls:** [[eqstat.f#EQSTAT|EQSTAT]], [[getopac.f#GETOPAC|GETOPAC]], and [[tpgrad.f#TPGRAD|TPGRAD]] (with `CMIXLQ`, and with `IOVIM = -1` in [[dpmix_mod.f#DPMIX_MOD|`DPMIX_MOD`]], so no overshoot point is flagged).
- **Outputs:** `DYDX(1..3)`; the counter `KENV`; the point's structure, gradients, $\beta$, convective velocity and ionization fractions in [[envprt_mod.f#ENVPRT_MOD|`ENVPRT_MOD`]] (always, since 07/02, 08/13 and 08/25), read by ENVINT, [[getnewenv.f#GETNEWENV|GETNEWENV]] and [[starin.f#STARIN|STARIN]]; and the quantities for pulsation output in [[pulse2_mod.f#PULSE2_MOD|`PULSE2_MOD`]] when saving.

**The method.** With $f_P$ = `FPL`,
$$\frac{d\log m}{d\log P} = -\frac{4\pi r^4 P}{G m^2 f_P},\qquad \frac{d\log T}{d\log P} = \nabla,\qquad \frac{d\log r}{d\log P} = -\frac{r P}{G m \rho}\,f_P,$$
with $\nabla$ from `TPGRAD`.

**KC's changes.** 2025-05-31: unused arguments removed from the call to `MEQOS` (that call is gone since `rp_1`); a never-executed `PRINT` keeps `GL` and `LOCOND` referenced, "for external procedure compatibility".

**Changed since `rp_1`.** The MHD equation of state removed: `EQSTAT` is always called (no `LMHD`, no `MEQOS`); `TPGRAD` takes the mixing length as a new last argument, `CMIXLQ` from `QENVMIX_MOD`; COMMON blocks to modules (the unused `/PULSE/`, `/FLAG/` and `/MHD/` dropped), `IMPLICIT NONE`.

## Questions for the experts

1. **The distortion factor in $d\log r/d\log P$.** The interior equations in [[coefft.f#COEFFT|COEFFT]] have $d\log P/d\log m \propto f_P$ and $d\log r/d\log m$ without $f_P$; dividing gives $d\log r/d\log P \propto 1/f_P$. `QENV` divides by $f_P$ in $d\log m/d\log P$ (consistent) but *multiplies* by it in $d\log r/d\log P$. Is this a sign slip in the exponent of $f_P$, or does the envelope use a different form on purpose? (The effect is small where $f_P \approx 1$.)
2. **Repeated assignments.** `EFXION`, `QQDP`, `QQDT` and `QQCP` are now set both always and again inside `IF(LSAVE .OR. LPUMOD)`. The second set can go.
