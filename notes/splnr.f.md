## Explanation

**Purpose.** `splnr` is Numerical Recipes' `spline` in single precision, identical to [[splinnr.f|splinnr.f]] (see there for the method): the second derivatives of a cubic spline, with given end slopes or natural ends.

**How it fits.** Nothing in `src/` calls it, and it uses no COMMON block.

## Questions for the experts

1. **Unused duplicate.** No routine calls `splnr`, and it is identical to `splinnr`. Can it be removed?

### SPLNR

Unused copy of [[splinnr.f#SPLINNR|SPLINNR]].
