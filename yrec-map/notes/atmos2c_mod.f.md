## Explanation

**Purpose.** `ATMOS2C_MOD` holds the surface-pressure table used when `KTTAU` is 5: $`\log P`$ on a grid of 76 values of $`\log T_\mathrm{eff}`$ and 11 of $`\log g`$. It replaces `COMMON/ATMOS2C/` (MHP via Claude, 10/14/26); the sizes `NGC`, `NTC` are private.

**What its variables hold, who sets them, who reads them.** [`SETUPS`](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L16-L396) reads `ATMTLC(NTC)` ($`\log T_\mathrm{eff}`$), `ATMGLC(NGC)` ($`\log g`$), and `ATMPLC(NTC,NGC)` ($`\log P`$) from the file `FATM` (the table's metallicity goes to `ATMZ` in [`ATMOS2_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/atmos2_mod.f#L23-L36)); [`KCSURFP`](kcsurfp.f.md#kcsurfp) interpolates in them.

**Changed since `rp_1`.** New file: `COMMON/ATMOS2C/` as a module.
