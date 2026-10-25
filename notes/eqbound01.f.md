## Explanation

**Purpose.** `EQBOUND01` is [[eqbound.f#EQBOUND|EQBOUND]] for the OPAL 2001 equation-of-state table ("MHP 7/2003"): it says whether $(T,\rho)$ is in the table and returns the weight for blending with the Yale/SCV equation of state.

**How it fits.**
- **Who calls it:** only [[eqstat2.f#EQSTAT2|EQSTAT2]], after [[oeqos01.f#OEQOS01|OEQOS01]], when `LOPALE01` is set and $2000 \le T \le 10^8$ K and $\log\rho \le 7$ (EQSTAT2's own density).
- **Inputs and outputs:** as for `EQBOUND`: `T`, `DL` in; `LTAB`, `LRAMP`, `FAC` out.
- **COMMON blocks:** `/AEOS/` holds the OPAL 2001 table, shared with [[esac01.f#ESAC01|ESAC01]], `READCOEOS01`, `RHOOFP01` and `T6RINTEOS01`. `/RMPOPEOS01/` holds `RMX`, `KRA` and `KT`, filled by `READCOEOS01`.

**The method.** The same as `EQBOUND`, line for line, with the larger 2001 table (169 densities, 191 temperatures) and the upper density cut at $\log\rho = 7$ instead of 5. See [[eqbound.f|eqbound.f]] for the equations.

**KC's changes.** The unused argument `DL0` was removed (2025-05-31).

## Questions for the experts

1. **Near-duplicate code.** This file differs from `eqbound.f` only in the table size, the COMMON names and one constant. Could the three `EQBOUND` routines share one implementation, with the table passed in?
2. The questions on `EQBOUND` (edges not interpolated, one ramp at a time, no low-density ramp) apply here too.

### EQBOUND01

In-table test and blending weight for the OPAL 2001 table; same logic as `EQBOUND`.
