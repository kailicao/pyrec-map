## Explanation

**Purpose.** `ATMOS2_MOD` holds the surface-pressure table read when `KTTAU` is 3 or 4 (used only with 3; see below): $\log P$ on a grid of 57 values of $\log T_\mathrm{eff}$ and 11 of $\log g$. It replaces `COMMON/ATMOS2/` (MHP via Claude, 10/14/26); the sizes `NG`, `NT` are private.

**What its variables hold, who sets them, who reads them.** [[setups.f#SETUPS|`SETUPS`]] reads them all from the file `FATM`: `ATMZ`, the table's metallicity; `ATMTL(NT)`, the $\log T_\mathrm{eff}$ grid; `ATMGL(NG)`, the $\log g$ grid; `ATMPL(NT,NG)`, $\log P$. [[surfp.f#SURFP|`SURFP`]] interpolates in them. `ATMZ` is read by no routine; `SETUPS` also stores in it the metallicity of the `KTTAU` = 5 table ([[atmos2c_mod.f#ATMOS2C_MOD|`ATMOS2C_MOD`]]).

**Why `KTTAU` = 4 loads it.** With `KTTAU` = 4 (Allard atmospheres, [[alfilein.f#ALFILEIN|`ALFILEIN`]], [[alsurfp.f#ALSURFP|`ALSURFP`]]) `SETUPS` reads this Kurucz table too, but no routine then uses it: above the Allard table's top $T_\mathrm{eff}$ (`AL_TEFFLmax`, [[alatm05_mod.f#ALATM05_MOD|`ALATM05_MOD`]]), or off its gravities, [[surfbc.f#SURFBC|`SURFBC`]] and [[envint.f#ENVINT|`ENVINT`]] switch to the gray atmosphere (`KTTAU` = 0), not to Kurucz, although `ALSURFP`'s header names Kurucz (`KTTAU` = 3) as a fallback the caller could choose (question 1).

**Changed since `rp_1`.** New file: `COMMON/ATMOS2/` as a module.

## Questions for the experts

1. **The Kurucz table with Allard atmospheres.** `SETUPS` reads the Kurucz table `FATM` whenever `KTTAU` is 3 or 4, but with `KTTAU` = 4 nothing reads it: when $T_\mathrm{eff}$ leaves the Allard table, `SURFBC` and `ENVINT` fall back to the gray atmosphere. A student expected the Kurucz table to take over there, as `ALSURFP`'s header suggests. Is the read a remnant of an older fallback to Kurucz, and should a hot Allard run switch to Kurucz rather than gray? It matters for the boundary condition of stars that heat past the Allard table.
