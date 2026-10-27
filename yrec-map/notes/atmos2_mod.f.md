## Explanation

**Purpose.** `ATMOS2_MOD` holds the surface-pressure table used when `KTTAU` is 3 or 4: $\log P$ on a grid of 57 values of $\log T_\mathrm{eff}$ and 11 of $\log g$. It replaces `COMMON/ATMOS2/` (MHP via Claude, 10/14/26); the sizes `NG`, `NT` are private.

**What its variables hold, who sets them, who reads them.** [[setups.f#SETUPS|`SETUPS`]] reads them all from the file `FATM`: `ATMZ`, the table's metallicity; `ATMTL(NT)`, the $\log T_\mathrm{eff}$ grid; `ATMGL(NG)`, the $\log g$ grid; `ATMPL(NT,NG)`, $\log P$. [[surfp.f#SURFP|`SURFP`]] interpolates in them. `ATMZ` is read by no routine; `SETUPS` also stores in it the metallicity of the `KTTAU` = 5 table ([[atmos2c_mod.f#ATMOS2C_MOD|`ATMOS2C_MOD`]]).

**Changed since `rp_1`.** New file: `COMMON/ATMOS2/` as a module.
