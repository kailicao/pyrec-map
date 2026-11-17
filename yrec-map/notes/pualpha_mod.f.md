## Explanation

**Purpose.** `PUALPHA_MOD` holds three mixing-length quantities at the current point, for the pulsation output. Shared by 2 routines. It replaces `COMMON/PUALPHA/` ("DBG 7/95," MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.**
- `ALFMLT`, `PHMLT`, `CMXMLT`: set to 0 on every entry to [`TPGRAD`](tpgrad.f.md#tpgrad) and computed nowhere; [`ENVINT`](envint.f.md#envint) writes them in the envelope's pulsation output (`IPVER` = 3).

**Design.** A blanket `USE PUALPHA_MOD` in each routine. Since the three scalars are always 0, so are the columns written (see TPGRAD's page).

**Changed since `rp_1`.** New file: `COMMON/PUALPHA/` as a module.

**Changed since `a8a5950`.** The per-shell arrays `VALFMLT`, `VPHMLT`, and `VCMXMLT`, always-zero copies of the three scalars that [`COEFFT`](coefft.f.md#coefft) stored and [`WRTMOD`](wrtmod.f.md#wrtmod) wrote, are gone; WRTMOD now writes zeros in their columns. The module still `USE`s `DIMENSIONS_MOD`, which nothing in it needs now.
