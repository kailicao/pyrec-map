## Explanation

**Purpose.** `CCOUT_MOD` holds one switch, `LPHHD`: write the header of the stitched stored-model output. It replaces `COMMON/CCOUT/` (MHP via Claude, 10/14/26).

**Who sets it, who reads it.** [`PARMIN`](parmin.f.md#parmin) sets it to `LSTCH` (the stitched format); [`PUTSTORE`](putstore.f.md#putstore) writes the header on its first call and turns it off.

**Changed since `rp_1`.** New file: `COMMON/CCOUT/` as a module.
