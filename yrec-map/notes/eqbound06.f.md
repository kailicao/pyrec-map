## Explanation

**Purpose.** `EQBOUND06` decides whether $`(T,\rho)`$ lies inside the OPAL 2006 equation-of-state table and, near its edges, returns the weight for blending OPAL with the Yale/SCV equation of state ("LLP 10/16/06"). Unlike the 1995 and 2001 versions, it follows the table's irregular edge in both temperature and density, and combines the ramps.

**How it fits.**
- **Who calls it:** only [EQSTAT2](eqstat2.f.md#eqstat2), after [OEQOS06](https://github.com/yreclab/yrec/blob/7be4133/src/oeqos06.f#L30-L132), when `LOPALE06` is set and $`1870 \le T \le 2\times10^8\,\mathrm{K}`$ and $`\log\rho \le 7`$ (EQSTAT2's own density).
- **Inputs and outputs:** `T` (K) and `DL` ($`\log_{10}\rho`$) in; `LTAB`, `LRAMP` and `FAC` out.
- **Modules:** [`AEOS06_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/aeos06_mod.f#L27-L52) (formerly `/AEOS06/`) holds the table (`T6A`, `RHO`), shared with [ESAC06](esac06.f.md#esac06), `READCOEOS06`, `RHOOFP06` and `T6RINTEOS06`. [`EOS06MISC_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/eos06misc_mod.f#L29-L72) (formerly `/BEOS06/` and `/BBEOS06/`) holds `NTA` (for each density, the index of the lowest allowed temperature) and `NRA` (for each temperature, the index of the highest allowed density), set by DATA statements in the module (formerly in `ESAC06`), and the interpolation indices `K3` and `L2` that `ESAC06` found on its last call; this routine starts its search from them.

**The method.** With $`T_6 = T/10^6`$, $`\rho = 10^{\mathrm{DL}}`$, `T6A` decreasing and `RHO` increasing:
1. Out of table if $`\rho \lt{} \rho_1`$, $`\rho \ge \rho_{N}`$, $`T_6 \gt{} T_{6,1}`$ or $`T_6 \le T_{6,N}`$.
2. Ramps at the "easy borders": at high temperature, $`f_T = (T_6 - T_{6,1})/(T_{6,2} - T_{6,1})`$ when $`T_6 \gt{} T_{6,2}`$; at low density, $`f_\rho = (\rho - \rho_1)/(\rho_2 - \rho_1)`$ when $`\rho \lt{} \rho_2`$.
3. Find $`k`$ and $`l`$ with $`T_{6,k-1} \ge T_6 \gt{} T_{6,k}`$ and $`\rho_{l-1} \lt{} \rho \le \rho_l`$, by a linear search from `K3` and `L2`. EQSTAT2 calls this routine only after OEQOS06 has returned normally, so ESAC06 has just set `K3` and `L2` for the same point (settled from the code, Nov 9, 2026: [eqstat2.f, lines 313–317](https://github.com/yreclab/yrec/blob/7be4133/src/eqstat2.f#L313-L317), [oeqos06.f, lines 94–102](https://github.com/yreclab/yrec/blob/7be4133/src/oeqos06.f#L94-L102)).

    > **Question** ([lines 69–88](https://github.com/yreclab/yrec/blob/7be4133/src/eqbound06.f#L69-L88)). **Hidden dependence on ESAC06.** The search starts from `K3` and `L2` in `EOS06MISC_MOD`, left by the last call of `ESAC06`. That holds at the one call today, but a call without a preceding `ESAC06` would start from unset indices (`T6A(0)` or `RHO(0)` could be read). Should the indices be passed explicitly, or the search start from a fixed index?

4. The irregular edge: out of table if $l > $ `NRA(k)` or $k > $ `NTA(l)`. On the last allowed row or column, a ramp: $`f_\rho = (\rho_l - \rho)/(\rho_l - \rho_{l-1})`$ if $l = $ `NRA(k)`; $`f_T = (T_6 - T_{6,k})/(T_{6,k-1} - T_{6,k})`$ if $k = $ `NTA(l)`.
5. The weight is the product, $`f = f_\rho f_T`$.

The ramps are linear in $`\rho`$ and $`T_6`$, not in their logarithms.

> **Question** ([lines 55–63](https://github.com/yreclab/yrec/blob/7be4133/src/eqbound06.f#L55-L63); [lines 100–117](https://github.com/yreclab/yrec/blob/7be4133/src/eqbound06.f#L100-L117)). **Linear ramps.** The 1995 and 2001 versions ramp in $`\log\rho`$; this one ramps in $`\rho`$. Is the difference intended?

A high-temperature ramp of step 2 ($`k = 2`$) and an edge ramp in temperature of step 4 ($k = $ `NTA(l)`) never meet, nor do the two density ramps ($`l = 2`$ and $l = $ `NRA(k)`): The smallest `NTA` is 26 and the smallest `NRA` is 87 (settled from the code, Nov 9, 2026: [eos06misc_mod.f, lines 61–70](https://github.com/yreclab/yrec/blob/7be4133/src/eos06misc_mod.f#L61-L70)), so step 4's assignment of $`f_T`$ or $`f_\rho`$ never replaces one from step 2.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

### EQBOUND06

In-table test and blending weight $`f = f_\rho f_T`$ for the OPAL 2006 table, following its irregular edge (`NTA`, `NRA`).
