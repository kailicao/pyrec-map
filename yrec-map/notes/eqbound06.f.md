## Explanation

**Purpose.** `EQBOUND06` decides whether $(T,\rho)$ lies inside the OPAL 2006 equation-of-state table and, near its edges, returns the weight for blending OPAL with the Yale/SCV equation of state ("LLP 10/16/06"). Unlike the 1995 and 2001 versions, it follows the table's irregular edge in both temperature and density, and combines the ramps.

**How it fits.**
- **Who calls it:** only [[eqstat2.f#EQSTAT2|EQSTAT2]], after [[oeqos06.f#OEQOS06|OEQOS06]], when `LOPALE06` is set and $1870 \le T \le 2\times10^8$ K and $\log\rho \le 7$ (EQSTAT2's own density).
- **Inputs and outputs:** `T` (K) and `DL` ($\log_{10}\rho$) in; `LTAB`, `LRAMP` and `FAC` out.
- **Modules:** [[aeos06_mod.f#AEOS06_MOD|`AEOS06_MOD`]] (formerly `/AEOS06/`) holds the table (`T6A`, `RHO`), shared with [[esac06.f#ESAC06|ESAC06]], `READCOEOS06`, `RHOOFP06` and `T6RINTEOS06`. [[eos06misc_mod.f#EOS06MISC_MOD|`EOS06MISC_MOD`]] (formerly `/BEOS06/` and `/BBEOS06/`) holds `NTA` (for each density, the index of the lowest allowed temperature) and `NRA` (for each temperature, the index of the highest allowed density), set by DATA statements in the module (formerly in `ESAC06`), and the interpolation indices `K3` and `L2` that `ESAC06` found on its last call; this routine starts its search from them.

**The method.** With $T_6 = T/10^6$, $\rho = 10^{\mathrm{DL}}$, `T6A` decreasing and `RHO` increasing:
1. Out of table if $\rho < \rho_1$, $\rho \ge \rho_{N}$, $T_6 > T_{6,1}$ or $T_6 \le T_{6,N}$.
2. Ramps at the "easy borders": at high temperature, $f_T = (T_6 - T_{6,1})/(T_{6,2} - T_{6,1})$ when $T_6 > T_{6,2}$; at low density, $f_\rho = (\rho - \rho_1)/(\rho_2 - \rho_1)$ when $\rho < \rho_2$.
3. Find $k$ and $l$ with $T_{6,k-1} \ge T_6 > T_{6,k}$ and $\rho_{l-1} < \rho \le \rho_l$, by a linear search from `K3` and `L2`.
4. The irregular edge: out of table if $l > $ `NRA(k)` or $k > $ `NTA(l)`. On the last allowed row or column, a ramp: $f_\rho = (\rho_l - \rho)/(\rho_l - \rho_{l-1})$ if $l = $ `NRA(k)`; $f_T = (T_6 - T_{6,k})/(T_{6,k-1} - T_{6,k})$ if $k = $ `NTA(l)`.
5. The weight is the product, $f = f_\rho f_T$.

The ramps are linear in $\rho$ and $T_6$, not in their logarithms.

**KC's changes.** The unused argument `DL0` was removed, and the elements of `/BEOS06/` were reordered (2025-05-30/31).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **Hidden dependence on ESAC06.** The search starts from `K3` and `L2` in `EOS06MISC_MOD`, left by the last call of `ESAC06`. That is true when `OEQOS06` has just called it, but the routine would misbehave if called alone. Should the indices be passed explicitly?
2. **Linear ramps.** The 1995 and 2001 versions ramp in $\log\rho$; this one ramps in $\rho$. Is the difference intended?
3. **Overwritten ramp.** At high temperature, step 2 sets $f_T$; if step 4 also finds $k = $ `NTA(l)`, it replaces that $f_T$ rather than combining them. Can both happen, and which should win?

### EQBOUND06

In-table test and blending weight $f = f_\rho f_T$ for the OPAL 2006 table, following its irregular edge (`NTA`, `NRA`).
