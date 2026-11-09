## Explanation

**Purpose.** `SPLINTD2` evaluates a cubic spline at one point; it is [[splint.f|splint.f]]'s algorithm and equation, with arrays of the fixed size `JSON` (5000, from `DIMENSIONS_MOD`), for the second derivatives made by [[splinc.f#SPLINC|SPLINC]]. Its header comment still names it "SUBROUTINE SPLINTD" ([[#L3]]).

> **Question** ([[#L31]]; [[splint.f#L28]]). **Duplicates.** `SPLINTD2` and `SPLINT` differ only in their array declarations (and the comment's name `SPLINTD`). Could one routine serve both callers?

**How it fits.**
- **Who calls it:** only [[hpoint.f#HPOINT|HPOINT]], after [[splinc.f#SPLINC|SPLINC]].
- **Modules:** `IOUNITS_MOD`, for the unit `ISHORT` of its error message ("ERROR IN SPLINT ROUTINE: TWO ABSCISSAE COINCIDE", with the abscissa and $x$, also written to the terminal, then `STOP 1`).

**Changed since `rp_1`.** Declarations only: `/LUOUT/` to `IOUNITS_MOD`, the array size `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

**Changed since `a8a5950`.** The stop on two equal abscissas now gives the abscissa and $x$ in its message, writes it to the terminal as well as the `.short` file, and exits with status 1, the code for run-time errors, instead of a bare `STOP` (`KNOWN_ISSUES.md`, issue 38). `SPLINT` changed the same way, so question 1 stands.

### SPLINTD2

Cubic-spline interpolation at one point, arrays sized 5000; the same as [[splint.f#SPLINT|SPLINT]].
