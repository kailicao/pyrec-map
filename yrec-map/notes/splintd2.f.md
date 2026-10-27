## Explanation

**Purpose.** `SPLINTD2` evaluates a cubic spline at one point; it is [[splint.f|splint.f]]'s algorithm and equation, with arrays of the fixed size `JSON` (5000, from `DIMENSIONS_MOD`), for the second derivatives made by [[splinc.f#SPLINC|SPLINC]]. Its header comment still names it "SUBROUTINE SPLINTD".

**How it fits.**
- **Who calls it:** only [[hpoint.f#HPOINT|HPOINT]], after [[splinc.f#SPLINC|SPLINC]].
- **Modules:** `IOUNITS_MOD`, for the unit `ISHORT` of its error message ("ERROR IN SPLINT ROUTINE", then `STOP`).

**Changed since `rp_1`.** Declarations only: `/LUOUT/` to `IOUNITS_MOD`, the array size `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Questions for the experts

1. **Duplicates.** `SPLINTD2` and `SPLINT` differ only in their array declarations (and the comment's name `SPLINTD`). Could one routine serve both callers?

### SPLINTD2

Cubic-spline interpolation at one point, arrays sized 5000; the same as [[splint.f#SPLINT|SPLINT]].
