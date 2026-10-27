## Explanation

**Purpose.** `COMP2_MOD` holds the envelope's helium: `YENV` (⁴He, $1 - X - Z - Y_3$) and `Y3ENV` (³He). It replaces `COMMON/COMP2/` (MHP via Claude, 10/14/26); it completes [[comp_mod.f#COMP_MOD|`COMP_MOD`]].

**Who sets them, who reads them.** [[starin.f#STARIN|`STARIN`]] sets both from the surface composition; [[physic.f#PHYSIC|`PHYSIC`]] and [[checkc.f#CHECKC|`CHECKC`]] read them.

**Changed since `rp_1`.** New file: `COMMON/COMP2/` as a module.
