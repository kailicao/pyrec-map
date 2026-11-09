## Explanation

**Purpose.** A binary search in an increasing table, part of the shape-preserving quadratic splines of McAllister and Roulier (coded by S. L. Dodd and M. Roulier, N.C. State University, as the header says).

**How it fits.** Its only caller is [[meval.f#MEVAL|`MEVAL`]], which evaluates the spline and is called by [[osplin.f#OSPLIN|`OSPLIN`]]. No COMMON blocks.

**The method.** Given `XTAB(1..NUM)` and a value `S` with `XTAB(1)` ≤ `S` ≤ `XTAB(NUM)`, it returns `LCN`, the index of the last entry below `S`, or the index of the entry equal to `S` (and then `FND` = 1). The interval is halved until it has length one. `FND` relies on exact equality of reals ([[#L55]], [[#L60]], [[#L77]]), so a value equal to a node up to rounding is reported as not found; MEVAL then evaluates the spline of the interval next to the node, which passes through the node's value, so the result differs only by about the same rounding (settled from the code, Nov 9, 2026: [[spline.f#L66-L73]]).

**Changed since `rp_1`.** Declarations only: the array size `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.
