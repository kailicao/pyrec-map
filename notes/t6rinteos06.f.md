## Explanation

**Purpose.** `T6RINTEOS06` interpolates one equation-of-state quantity in temperature `T6` and density for the OPAL 2006 EOS (its comment's words). It is [[t6rinteos01.f|t6rinteos01.f]] line for line (method and equations in [[t6rinterp.f|t6rinterp.f]]), with `NT = 197` temperatures and COMMON blocks ending in `06`.

**How it fits.**
- **Who calls it:** only [[esac06.f#ESAC06|ESAC06]].
- **What it calls:** [[quadeos06.f#QUADEOS06|QUADEOS06]].
- **Output:** `ESACT` in COMMON `EEOS06`, shared with `ESAC06`, [[oeqos06.f#OEQOS06|OEQOS06]], [[radsub06.f#RADSUB06|RADSUB06]], [[readcoeos06.f#READCOEOS06|READCOEOS06]], [[rhoofp06.f#RHOOFP06|RHOOFP06]] and [[calcad.f#CALCAD|CALCAD]].

## Questions for the experts

1. **`RECURSIVE`.** The routine is declared `recursive`, but does not call itself and has `SAVE`; `T6RINTEOS01` is not recursive. Why?
2. **One routine for both releases.** The 2001 and 2006 versions differ only in `NT` and COMMON names; could one routine with the table as an argument replace them?

### T6RINTEOS06

Interpolation in temperature and density for the OPAL 2006 EOS tables; result in `ESACT` (COMMON `EEOS06`).
