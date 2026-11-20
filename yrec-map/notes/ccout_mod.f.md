## Explanation

**Purpose.** `CCOUT_MOD` holds one switch, `LPHHD`: write the header of the stitched stored-model output. It replaces `COMMON/CCOUT/` (MHP via Claude, 10/14/26).

**Who sets it, who reads it.** [`PARMIN`](https://github.com/yreclab/yrec/blob/7be4133/src/parmin.f#L16-L1489) sets it when the stored-model output (`LSTORE`) is in the stitched format (`LSTCH`); [`PUTSTORE`](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L13-L360) writes the header on its first call and turns it off.

**Changed since `rp_1`.** New file: `COMMON/CCOUT/` as a module.
