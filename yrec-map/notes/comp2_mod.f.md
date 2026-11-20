## Explanation

**Purpose.** `COMP2_MOD` holds the envelope's helium: `YENV` ($`^4\mathrm{He}`$, $`1 - X - Z - Y_3`$) and `Y3ENV` ($`^3\mathrm{He}`$). It replaces `COMMON/COMP2/` (MHP via Claude, 10/14/26); it completes [`COMP_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/comp_mod.f#L19-L34).

**Who sets them, who reads them.** [`STARIN`](starin.f.md#starin) sets both from the surface composition; [`PHYSIC`](https://github.com/yreclab/yrec/blob/7be4133/src/physic.f#L3-L191) and [`CHECKC`](checkc.f.md#checkc) read them.

**Changed since `rp_1`.** New file: `COMMON/COMP2/` as a module.
