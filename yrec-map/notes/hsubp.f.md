## Explanation

**Purpose.** `HSUBP` computes the local pressure scale height at one point, the edge of a convective region, for the overshoot calculation (comment: "PD Dec. 1984, revised for YREC/Mark6 by MHP 2/91").

**How it fits.**
- **Who calls it:** only [[oversh.f#OVERSH|`OVERSH`]], with `JEDGE` the point at the edge of the convection zone.
- **Inputs:** the model's composition `HCOMP`, and $\log\rho$, $\log P$, $\log r$, $\log m$, $\log T$ (`HD`, `HP`, `HR`, `HS`, `HT`). **Output:** `PSCAHE`, the scale height in cm.
- **Calls:** [[eqstat.f#EQSTAT|`EQSTAT`]], the equation of state.
- **Modules:** the constants of [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]] (for `CLN` and $\log G$, `CGL`); [[debhu_mod.f#DEBHU_MOD|`DEBHU_MOD`]], where it sets the composition used by the Debye–Hückel correction (`XXDH`, `YYDH`, `ZZDH`, `ZDH(1..3)`) before calling the EOS, shared with `EQRELV`, `PHYSIC`, `COEFFT` and others; and the flag `LDH` from [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] (formerly in `/DEBHU/`).

> **Question** ([[#L60-L67]]). **Debye–Hückel side effect.** When `LDH` is true, `HSUBP` overwrites `XXDH`, `YYDH`, `ZZDH`, `ZDH(1..3)` in `DEBHU_MOD` with the composition at `JEDGE`. Do later EOS calls rely on these being set by their own callers?

**The method.** The scale height returned is the hydrostatic one,

$$H_p = \frac{P}{\rho g} = \frac{P\,r^2}{\rho\,G\,m},$$

computed in logs: `PSCAHE` $= 10^{\log P + 2\log r - \log\rho - \log G - \log m}$. Here $\log\rho$ is not the model's `HD(JEDGE)`: `DL` is an output argument of [[eqstat.f#EQSTAT|`EQSTAT`]], which recomputes the density from $P$, $T$, $X$, $Z$, and `PSCAHE` uses that value. The EOS call also returns `RMU` (probably $\mathcal{R}/\mu$), which goes only into a second, ideal-gas estimate `PSCAP` $= (\mathcal{R}/\mu)\,T r^2/(G m)$, which is never returned (unused?).

> **Question** ([[#L51]]; [[#L59]]; [[#L68-L75]]). **Which density.** The comment says the EOS is called "to determine the mean molecular weight", but `RMU` is used only for the dropped `PSCAP`; the EOS call changes the result through the density it returns in `DL`. Was the EOS density meant, rather than the model's `HD(JEDGE)`?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

### HSUBP

Returns $H_p = P r^2/(\rho G m)$ at point `JEDGE`, with $\rho$ from the EOS (above).
