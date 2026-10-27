## Explanation

**Purpose.** `CCOUT_MOD` holds one switch, `LPHHD`: write the header of the stitched stored-model output. It replaces `COMMON/CCOUT/` (MHP via Claude, 10/14/26).

**Who sets it, who reads it.** [[parmin.f#PARMIN|`PARMIN`]] sets it to `LSTCH` (the stitched format); [[putstore.f#PUTSTORE|`PUTSTORE`]] writes the header on its first call and turns it off.

**Changed since `rp_1`.** New file: `COMMON/CCOUT/` as a module.
