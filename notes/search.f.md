## Explanation

**Purpose.** A binary search in an increasing table, part of the shape-preserving quadratic splines of McAllister and Roulier (coded by S. L. Dodd and M. Roulier, N.C. State University, as the header says).

**How it fits.** Its only caller is [[meval.f#MEVAL|`MEVAL`]], which evaluates the spline and is called by [[osplin.f#OSPLIN|`OSPLIN`]]. No COMMON blocks.

**The method.** Given `XTAB(1..NUM)` and a value `S` with `XTAB(1)` ≤ `S` ≤ `XTAB(NUM)`, it returns `LCN`, the index of the last entry below `S`, or the index of the entry equal to `S` (and then `FND` = 1). The interval is halved until it has length one.

**KC's changes.** An arithmetic `IF` was rewritten as `IF … ELSE IF … ELSE` (KC 2025-05-30).

## Questions for the experts

1. **Exact equality.** `FND` relies on `XTAB(MIDDLE) .EQ. S` for reals, so a value equal to a node up to rounding is reported as not found. Does `MEVAL` behave the same either way?
