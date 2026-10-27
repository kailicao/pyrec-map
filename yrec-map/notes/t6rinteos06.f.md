## Explanation

**Purpose.** `T6RINTEOS06` interpolates one equation-of-state quantity in temperature `T6` and density for the OPAL 2006 EOS (its comment's words). At `rp_1` it had two twins, line for line apart from table sizes and COMMON names: `t6rinteos01.f` for the 2001 tables and `t6rinterp.f` for the original OPAL tables (both removed since `rp_1`); this version has `NT = 197` temperatures.

**How it fits.**
- **Who calls it:** only [[esac06.f#ESAC06|ESAC06]].
- **What it calls:** [[quadeos06.f#QUADEOS06|QUADEOS06]].
- **Inputs:** `SLR` and `SLT`, the density and temperature; from `AEOS06_MOD` the grids `RHO`, `T6A`, the inverse spacings `DFS`, `DFSR` and `ESK`, the values already interpolated in $X$; from `EOS06MISC_MOD` the grid indices `K1`–`K4`, `L1`–`L4` and the switches `IP`, `IQ`, set by `ESAC06`, and the work arrays `H`, `Q`.
- **Output:** `ESACT` in `EOS06MISC_MOD`, read by `ESAC06`; the module is also used by [[oeqos06.f#OEQOS06|OEQOS06]], [[radsub06.f#RADSUB06|RADSUB06]], [[readcoeos06.f#READCOEOS06|READCOEOS06]], [[rhoofp06.f#RHOOFP06|RHOOFP06]], [[eqbound06.f#EQBOUND06|EQBOUND06]] and [[calcad.f#CALCAD|CALCAD]].

**The method.** `QUADEOS06` gives the quadratic through three points, evaluated at $x$. For each of the temperatures $T_{k_1}, \dots$, a quadratic in density through the rows $l_1$–$l_3$ gives $h_k$, and, if `IQ = 3`, another through $l_2$–$l_4$ gives $q_k$. Quadratics in temperature through $h_{k_1..k_3}$ and $h_{k_2..k_4}$ (if `IP = 3`) are then blended linearly:
$$f = w\,f_{123} + (1 - w)\,f_{234},\qquad w = (T_{k_3} - T)\,/\,(T_{k_3} - T_{k_2}),$$
the weight from `DFS(K3)`, the inverse grid spacing. The same is done for the $q$'s, and, when `IP = 3`, the two results are blended in density with $w_\rho = (\rho_{l_3} - \rho)\,/\,(\rho_{l_3} - \rho_{l_2})$ (`DFSR(L3)`). A result above $10^{15}$ stops the run ("interpolation indices out of range").

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/AEOS06/` to `AEOS06_MOD`, `/EEEOS06/` to `EEEOS06_MOD`, `/AAEOS06/`, `/BBEOS06/` and `/EEOS06/` to `EOS06MISC_MOD`, `/LUOUT/` to `IOUNITS_MOD`), `IMPLICIT NONE`. The question on the two releases is settled: the 2001 version, `t6rinteos01.f`, was removed.

## Questions for the experts

1. **`RECURSIVE`.** The routine is declared `recursive`, but does not call itself and has `SAVE`; `T6RINTEOS01` (removed since `rp_1`) was not recursive. Why?

### T6RINTEOS06

Interpolation in temperature and density for the OPAL 2006 EOS tables; result in `ESACT` (`EOS06MISC_MOD`).
