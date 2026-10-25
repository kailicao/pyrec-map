## Explanation

**Purpose.** `T6RINTERP` is the last stage of the OPAL equation-of-state interpolation in [[esac.f#ESAC|ESAC]]: after `ESAC` has interpolated the tables in hydrogen abundance $X$, it interpolates one quantity in temperature `T6` ($T/10^6$ K, by the name) and density `R`, on a 4×4 grid around the point, by mixing overlapping quadratics "to obtain smoothed derivatives" (the caller's comment). [[t6rinteos01.f|t6rinteos01.f]] and [[t6rinteos06.f|t6rinteos06.f]] are the same routine for the 2001 and 2006 table families (the year of the first is probably 2001, from its name).

**How it fits.**
- **Inputs:** `SLR` and `SLT`, the density and temperature (`ESAC` sets `SLT = T6`, `SLR = R`). Through COMMON blocks: `A` (the grids `RHO`, `T6A`, the inverse spacings `DFS`, `DFSR`, and `ESK`, the values already interpolated in $X$), `BB` (the grid indices `K1`–`K4`, `L1`–`L4` and the switches `IP`, `IQ`, set by `ESAC`), and `AA` (work arrays `H`, `Q`).
- **Who calls it:** only [[esac.f#ESAC|ESAC]].
- **What it calls:** [[quad.f#QUAD|QUAD]], the quadratic through three points.
- **Output:** `ESACT` in COMMON `E`, which `ESAC` stores in `EOS`; read by [[oeqos.f#OEQOS|OEQOS]], [[radsub.f#RADSUB|RADSUB]] and [[rhoofp.f#RHOOFP|RHOOFP]] among others.
- **COMMON blocks:** `A` (also [[readco.f#READCO|READCO]], which fills it, [[eqbound.f#EQBOUND|EQBOUND]], [[rhoofp.f#RHOOFP|RHOOFP]] and the BLOCK DATA), `AA`, `BB`, `E`, `EE`, `LUOUT`.

**The method.** `QUAD` gives the quadratic through $(x_1, y_1), (x_2, y_2), (x_3, y_3)$ evaluated at $x$. For each of the temperatures $T_{k_1}, \dots$, a quadratic in density through the rows $l_1$–$l_3$ gives $h_k$, and, if `IQ = 3`, another through $l_2$–$l_4$ gives $q_k$. Quadratics in temperature through $h_{k_1..k_3}$ and $h_{k_2..k_4}$ (if `IP = 3`) are then blended linearly:
$$f = w\,f_{123} + (1 - w)\,f_{234},\qquad w = (T_{k_3} - T)\,/\,(T_{k_3} - T_{k_2}),$$
the weight from `DFS(K3)`, the inverse grid spacing. The same is done for the $q$'s, and the two results are blended in density with $w_\rho = (\rho_{l_3} - \rho)\,/\,(\rho_{l_3} - \rho_{l_2})$ (`DFSR(L3)`). A result above $10^{15}$ stops the run ("interpolation indices out of range").

## Questions for the experts

1. **An undefined weight.** When `IQ = 3` but `IP` ≠ 3, the block "EOS(I) IN UPPER-RIGHT 3X3" uses `DIX`, which is set only in the `IP = 3` block (here, or `SAVE`d from an earlier call). The 2001 and 2006 versions moved that block inside `IF (IP .EQ. 3)` ("moved to loc a"). When `IP` ≠ 3, though, the `ESACTQ` computed with the undefined `DIX` is not used, since the final blend needs `IP = 3`, so the result is not affected. Should this version get the same fix, for tidiness?
2. **Three copies.** `T6RINTERP`, `T6RINTEOS01` and `T6RINTEOS06` differ only in table sizes and COMMON names. Is the oldest (OPAL, with `NR = 77`, `NT = 56`) still used?

### T6RINTERP

Interpolates one equation-of-state quantity in temperature and density by blended overlapping quadratics; result in `ESACT` (COMMON `E`).
