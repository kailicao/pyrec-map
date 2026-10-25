## Explanation

**Purpose.** `T6RINTEOS01` interpolates one equation-of-state quantity in temperature `T6` and density, for the OPAL EOS tables read by [[readcoeos01.f#READCOEOS01|READCOEOS01]] (probably the 2001 release, from the name). It is the routine of [[t6rinterp.f|t6rinterp.f]], with the method and equations described there, for larger tables (`NR = 169`, `NT = 191`) and COMMON blocks of its own (`AEOS`, `AAEOS`, `BBEOS`, `EEOS`, `EEEOS`).

**How it fits.**
- **Who calls it:** only [[esac01.f#ESAC01|ESAC01]], after the interpolation in $X$.
- **What it calls:** [[quadeos01.f#QUADEOS01|QUADEOS01]].
- **Output:** `ESACT` in COMMON `EEOS`, shared with [[esac01.f#ESAC01|ESAC01]], [[oeqos01.f#OEQOS01|OEQOS01]], [[radsub01.f#RADSUB01|RADSUB01]], [[readcoeos01.f#READCOEOS01|READCOEOS01]] and [[rhoofp01.f#RHOOFP01|RHOOFP01]].

**Design.** Unlike `T6RINTERP`, the smoothing in temperature of the second set of quadratics (`ESACTQ`) is inside the `IP = 3` block ("moved to loc a"), so the weight `DIX` is always defined when it is used.

## Questions for the experts

1. **The density blend without `IP = 3`.** When `IQ = 3` but `IP` ≠ 3, `ESACTQ` is computed but not used (the final blend needs both). Is falling back to the lower quadratic in density intended there?

### T6RINTEOS01

Interpolation in temperature and density for the OPAL 2001 (probably) EOS tables; result in `ESACT` (COMMON `EEOS`).
