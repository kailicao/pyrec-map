## Explanation

**Purpose.** `PUALPHA_MOD` holds three mixing-length quantities, at the current point and at every shell, for the pulsation output. Shared by 4 routines. It replaces `COMMON/PUALPHA/` ("DBG 7/95", MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.**
- `ALFMLT`, `PHMLT`, `CMXMLT`: set to 0 on every entry to [[tpgrad.f#TPGRAD|`TPGRAD`]] and computed nowhere; [[envint.f#ENVINT|`ENVINT`]] writes them in the envelope's pulsation output (`IPVER` = 3).
- `VALFMLT(JSON)`, `VPHMLT(JSON)`, `VCMXMLT(JSON)`: their values at each shell, stored by [[coefft.f#COEFFT|`COEFFT`]] when `LPULSE` is set; [[wrtmod.f#WRTMOD|`WRTMOD`]] writes them (`IPVER` = 3).

**Design.** A blanket `USE PUALPHA_MOD` in each routine. Since the three scalars are always 0, so are the arrays and the columns written (TPGRAD's notes raise this).

**Changed since `rp_1`.** New file: `COMMON/PUALPHA/` as a module.
