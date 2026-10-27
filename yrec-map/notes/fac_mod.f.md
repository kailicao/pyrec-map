## Explanation

**Purpose.** `FAC_MOD` holds the range of valid gravities at each temperature of the two surface-pressure tables, and the interpolation indices of the last lookup, shared by [[setups.f#SETUPS|`SETUPS`]], [[surfp.f#SURFP|`SURFP`]] and [[kcsurfp.f#KCSURFP|`KCSURFP`]]. It replaces `COMMON/FAC/` (MHP via Claude, 10/14/26). The table dimensions `NT` = 57 and `NTC` = 76 are `PRIVATE`, since the importing files declare their own.

**What its variables hold, who sets them, who reads them.** All are `INTEGER*4`.
- `IMIN(NT)`, `IMINMAX(NT)`: for each temperature of the surface-pressure table, the lowest and highest gravity index with a valid pressure (entries ≤ 0 are missing, −999), set by `SETUPS` when it reads the table ("G Somers 5/15"); read by `SURFP`. When no pressure is valid at a temperature, `IMIN` is the number of gravities, and SETUPS's comment expects the code to fail there.
- `IMIN2(NTC)`, `IMINMAX2(NTC)`: the same for the 76-temperature table, read by `KCSURFP`.
- `JP`, `KP(4)`: the temperature index and the four gravity indices of the last interpolation, set by `SURFP` and `KCSURFP`; read nowhere.

**Design.** A blanket `USE FAC_MOD`.

**Changed since `rp_1`.** New file: `COMMON/FAC/` as a module.
