## Explanation

**Purpose.** `HSUBP` computes the local pressure scale height at one point, the edge of a convective region, for the overshoot calculation (comment: "PD Dec. 1984, revised for YREC/Mark6 by MHP 2/91").

**How it fits.**
- **Who calls it:** only [[oversh.f#OVERSH|`OVERSH`]], with `JEDGE` the point at the edge of the convection zone.
- **Inputs:** the model's composition `HCOMP`, and $\log\rho$, $\log P$, $\log r$, $\log m$, $\log T$ (`HD`, `HP`, `HR`, `HS`, `HT`). **Output:** `PSCAHE`, the scale height in cm.
- **Calls:** [[eqstat.f#EQSTAT|`EQSTAT`]], the equation of state.
- **COMMON blocks:** the constants `CONST1` and `CONST2` (for `CLN` and $\log G$, `CGL`), and `DEBHU`, where it sets the composition used by the Debye–Hückel correction (`XXDH`, `YYDH`, `ZZDH`, `ZDH(1..3)`) before calling the EOS; `DEBHU` is shared with `EQSTAT`, `EQRELV`, `PHYSIC`, `COEFFT` and others.

**The method.** The scale height returned is the hydrostatic one,

$$H_P = \frac{P}{\rho g} = \frac{P\,r^2}{\rho\,G\,m},$$

computed in logs: `PSCAHE` $= 10^{\log P + 2\log r - \log\rho - \log G - \log m}$. Here $\log\rho$ is not the model's `HD(JEDGE)`: `DL` is an output argument of [[eqstat.f#EQSTAT|`EQSTAT`]], which recomputes the density from $P$, $T$, $X$, $Z$, and `PSCAHE` uses that value. The EOS call also returns `RMU` (probably $\mathcal{R}/\mu$), which goes only into a second, ideal-gas estimate `PSCAP` $= (\mathcal{R}/\mu)\,T r^2/(G m)$, which is never returned.

## Questions for the experts

1. **Unused result; which density.** `PSCAP` is computed and dropped, and `RMU` from `EQSTAT` is used only for it; the comment says the EOS is called "to determine the mean molecular weight". The EOS call does change the result, though, through the density it returns in `DL`. Was the EOS density meant (rather than the model's `HD(JEDGE)`), and is `PSCAP` a leftover?
2. **Debye–Hückel side effect.** When `LDH` is true, `HSUBP` overwrites `XXDH`, `YYDH`, `ZZDH`, `ZDH(1..3)` in `DEBHU` with the composition at `JEDGE`. Do later EOS calls rely on these being set by their own callers?

### HSUBP

Returns $H_P = P r^2/(\rho G m)$ at point `JEDGE`, with $\rho$ from the EOS (above).
