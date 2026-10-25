## Explanation

**Purpose.** The right-hand side of the envelope integration: with $\log P$ as the independent variable, it returns the derivatives of $\log m$ (relative to the total), $\log T$ and $\log r$, from hydrostatic equilibrium, mass conservation and the temperature gradient.

**How it fits.**
- **Inputs:** `X0` $=\log P$; `Y(1..3)` $= \log(m/M_\ast)$, $\log T$, $\log r$; the luminosity `B`, the distortion factors `FPL`, `FTL`, `TEFFL`, $X$, $Z$; `STOTAL` ($\log M_\ast$) from `/COMP/`; `LMHD`.
- **Who calls it:** [[envint.f#ENVINT|ENVINT]], directly and as the `EXTERNAL` derivative routine passed to [[bsstep.f#BSSTEP|BSSTEP]] and [[mmid.f#MMID|MMID]].
- **What it calls:** [[meqos.f#MEQOS|MEQOS]] or [[eqstat.f#EQSTAT|EQSTAT]], [[getopac.f#GETOPAC|GETOPAC]], and [[tpgrad.f#TPGRAD|TPGRAD]] (with `IOVIM = -1`, so no overshoot point is flagged).
- **Outputs:** `DYDX(1..3)`; the counter `KENV`; the point's structure, gradients, $\beta$, convective velocity and ionization fractions in `/ENVPRT/` (always, since 07/02, 08/13 and 08/25), read by ENVINT, [[getnewenv.f#GETNEWENV|GETNEWENV]] and [[starin.f#STARIN|STARIN]]; and the quantities for pulsation output in `/PULSE2/` when saving.

**The method.** With $f_P$ = `FPL`,
$$\frac{d\log m}{d\log P} = -\frac{4\pi r^4 P}{G m^2 f_P},\qquad \frac{d\log T}{d\log P} = \nabla,\qquad \frac{d\log r}{d\log P} = -\frac{r P}{G m \rho}\,f_P,$$
with $\nabla$ from `TPGRAD`.

**KC's changes.** 2025-05-31: unused arguments removed from the call to `MEQOS`; a never-executed `PRINT` keeps `GL` and `LOCOND` referenced, "for external procedure compatibility".

## Questions for the experts

1. **The distortion factor in $d\log r/d\log P$.** The interior equations in [[coefft.f#COEFFT|COEFFT]] have $d\log P/d\log m \propto f_P$ and $d\log r/d\log m$ without $f_P$; dividing gives $d\log r/d\log P \propto 1/f_P$. `QENV` divides by $f_P$ in $d\log m/d\log P$ (consistent) but *multiplies* by it in $d\log r/d\log P$. Is this a sign slip in the exponent of $f_P$, or does the envelope use a different form on purpose? (The effect is small where $f_P \approx 1$.)
2. **Repeated assignments.** `EFXION`, `QQDP`, `QQDT` and `QQCP` are now set both always and again inside `IF(LSAVE .OR. LPUMOD)`. The second set can go.
