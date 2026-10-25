## Explanation

**Purpose.** Quadratic interpolation through three points for the 2001 OPAL equation of state; a copy of [[quad.f#QUAD|QUAD]] under its own name (and with its own cache), so that the 2001 tables' routines do not share `QUAD`'s cache.

**How it fits.**
- **Who calls it:** [[esac01.f#ESAC01|ESAC01]] and [[t6rinteos01.f#T6RINTEOS01|T6RINTEOS01]].

**The method.** As in `QUAD`: $y(x) = c_1 + c_2 x + c_3 x^2$ through the three points; with `IC = 0` the abscissa factors are computed and cached in slot `I` (up to 30), otherwise reused.

## Questions for the experts

1. **Three copies.** `QUAD`, `QUADEOS01` and `QUADEOS06` are the same code. Separate caches are a reason to keep them apart; a single routine with the cache passed in would avoid the copies.
