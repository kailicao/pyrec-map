## Explanation

**Purpose.** `COMP2_MOD` holds the envelope's helium: `YENV` ($`^4\mathrm{He}`$, $`1 - X - Z - Y_3`$) and `Y3ENV` ($`^3\mathrm{He}`$). It replaces `COMMON/COMP2/` (MHP via Claude, 10/14/26); it completes [`COMP_MOD`](comp_mod.f.md#comp_mod).

**Who sets them, who reads them.** [`STARIN`](starin.f.md#starin) sets both from the surface composition; [`PHYSIC`](physic.f.md#physic) and [`CHECKC`](checkc.f.md#checkc) read them.

**Changed since `rp_1`.** New file: `COMMON/COMP2/` as a module.
