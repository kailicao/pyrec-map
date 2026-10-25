## Explanation

**Purpose.** `ZERO` sets the first `NN` elements of a double-precision array to zero.

**How it fits.** Called by [[mhdpx2.f#MHDPX2|MHDPX2]] (the MHD equation of state). No COMMON blocks.

**KC's changes.** The loop's last statement was moved off the labelled line, to end the `DO` loop with `CONTINUE` (2025-05-30, for a compiler warning).

## Questions for the experts

None.

### ZERO

Sets `A(1..NN)` to zero.
