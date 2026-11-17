## Explanation

**Purpose.** `HSUBP` computes the local pressure scale height at one point, the edge of a convective region, for the overshoot calculation (comment: "PD Dec. 1984, revised for YREC/Mark6 by MHP 2/91").

**How it fits.**
- **Who calls it:** only [`OVERSH`](oversh.f.md#oversh), with `JEDGE` the point at the edge of the convection zone.
- **Inputs:** the model's composition `HCOMP`, and $`\log\rho`$, $`\log P`$, $`\log r`$, $`\log m`$, $`\log T`$ (`HD`, `HP`, `HR`, `HS`, `HT`). **Output:** `PSCAHE`, the scale height in cm.
- **Calls:** [`EQSTAT`](eqstat.f.md#eqstat), the equation of state.
- **Modules:** the constants of [`CONSTANTS_MOD`](constants_mod.f.md#constants_mod) (for `CLN` and $`\log G`$, `CGL`); [`DEBHU_MOD`](debhu_mod.f.md#debhu_mod), where it sets the composition used by the Debye–Hückel correction (`XXDH`, `YYDH`, `ZZDH`, `ZDH(1..3)`) before calling the EOS, shared with `EQRELV`, `PHYSIC`, `COEFFT` and others; and the flag `LDH` from [`NMLPAR_MOD`](nmlpar_mod.f.md#nmlpar_mod) (formerly in `/DEBHU/`).

When `LDH` is true, `HSUBP` overwrites `XXDH`, `YYDH`, `ZZDH`, `ZDH(1..3)` in `DEBHU_MOD` with the composition at `JEDGE` ([lines 60–67](https://github.com/yreclab/yrec/blob/7be4133/src/hsubp.f#L60-L67)). The interior's EOS callers set them again first, shell by shell ([coefft.f, lines 207–209](https://github.com/yreclab/yrec/blob/7be4133/src/coefft.f#L207-L209); [physic.f, lines 100–102](https://github.com/yreclab/yrec/blob/7be4133/src/physic.f#L100-L102)), as CRRECT does before SURFBC ([crrect.f, lines 136–143](https://github.com/yreclab/yrec/blob/7be4133/src/crrect.f#L136-L143)), so the overwrite does not reach them.

> **Question** ([lines 60–67](https://github.com/yreclab/yrec/blob/7be4133/src/hsubp.f#L60-L67); [crrect.f, line 144](https://github.com/yreclab/yrec/blob/7be4133/src/crrect.f#L144); [crrect.f, line 158](https://github.com/yreclab/yrec/blob/7be4133/src/crrect.f#L158)). **Debye–Hückel side effect.** GETTAU ([getw.f, line 243](https://github.com/yreclab/yrec/blob/7be4133/src/getw.f#L243); [wrtout.f, line 552](https://github.com/yreclab/yrec/blob/7be4133/src/wrtout.f#L552)), STITCH ([putstore.f, line 198](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L198)), and CALCAD call `ENVINT` without setting the composition, and after CRRECT's call of MIX (which comes after SURFBC) the last to set it can be `HSUBP`, with the composition at `JEDGE` (or WRTOUT, with the center's, [wrtout.f, lines 243–245](https://github.com/yreclab/yrec/blob/7be4133/src/wrtout.f#L243-L245)). Do these envelope EOS calls expect the surface composition there?

**The method.** The scale height returned is the hydrostatic one,

```math
H_p = \frac{P}{\rho g} = \frac{P\,r^2}{\rho\,G\,m},
```

computed in logs: `PSCAHE` $`= 10^{\log P + 2\log r - \log\rho - \log G - \log m}`$. Here $`\log\rho`$ is not the model's `HD(JEDGE)`: `DL` is an output argument of [`EQSTAT`](eqstat.f.md#eqstat), which recomputes the density from $`P`$, $`T`$, $`X`$, $`Z`$, and `PSCAHE` uses that value. The EOS call also returns `RMU` (probably $`\mathcal{R}/\mu`$), which goes only into a second, ideal-gas estimate `PSCAP` $`= (\mathcal{R}/\mu)\,T r^2/(G m)`$, which is never returned (unused?).

> **Question** ([line 51](https://github.com/yreclab/yrec/blob/7be4133/src/hsubp.f#L51); [line 59](https://github.com/yreclab/yrec/blob/7be4133/src/hsubp.f#L59); [lines 68–75](https://github.com/yreclab/yrec/blob/7be4133/src/hsubp.f#L68-L75)). **Which density.** The comment says the EOS is called "to determine the mean molecular weight," but `RMU` is used only for the dropped `PSCAP`; the EOS call changes the result through the density it returns in `DL`. Was the EOS density meant, rather than the model's `HD(JEDGE)`?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

### HSUBP

Returns $`H_p = P r^2/(\rho G m)`$ at point `JEDGE`, with $`\rho`$ from the EOS (above).
