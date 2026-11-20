## Explanation

**Purpose.** `LLOT95A_MOD` holds all the OPAL95 opacity tables as read, with their grids in $`\log T`$, $`\log R`$, $`X`$, and $`Z`$, shared by 5 routines. It replaces `COMMON/LLOT95A/` (MHP via Claude, 10/14/26). The dimensions `NUMX` = 10, `NUMT` = 70, `NUMD` = 19, `NUMZ` = 13, and `NUMXZ` = 126 (the number of tables) are `PRIVATE`.

**What its variables hold, who sets them, who reads them.**
- `CAPPA2(NUMXZ,NUMT,NUMD)`: $`\log\kappa`$ of every table, read by [`LL95TBL`](ll95tbl.f.md#ll95tbl) (missing entries set to 9.999); interpolated in $`Z`$ by [`OP95ZTAB`](https://github.com/yreclab/yrec/blob/7be4133/src/op95ztab.f#L6-L126), and in all four variables by [`OP954D`](https://github.com/yreclab/yrec/blob/7be4133/src/op954d.f#L6-L114) and [`GETOPAL95`](getopal95.f.md#getopal95).
- `TGR(NUMT)`, `R0GR(NUMD)`: the $`\log T`$ and $`\log R`$ grids, read from the tables by `LL95TBL`; used by `GETOPAL95` to locate a point.
- `XXG(NUMX)`, `ZZG(NUMZ)`: the $`X`$ values (0 to 1) and $`Z`$ values (0 to 0.10) of the tables; `LL95TBL` checks each table's header against them, `OP95XTAB`, `OP95ZTAB`, and `GETOPAL95` interpolate in them. (For the last $`X`$, LL95TBL's check uses $`1 - Z`$ instead of `XXG(NUMX)`.)
- `NZ(NUMZ)`: the offset of each $`Z`$'s tables in `CAPPA2`'s first index (0, 10, … , 118); with nine slots for $`Z`$ = 0.06 and 0.08, the tables `LL95TBL` stores at `NZ(IZ)+10` overwrite others ([LL95TBL's suspected bug 1](ll95tbl.f.md#b1); [line 47](https://github.com/yreclab/yrec/blob/7be4133/src/llot95a_mod.f#L47)).
- `NUMXM(NUMZ)`: the number of $`X`$ tables for each $`Z`$ (10, but 9, 9 and 8 for the three largest, $`Z`$ = 0.06, 0.08, 0.1); read nowhere: unused?
- `XXG`, `ZZG`, `NZ`, and `NUMXM` carry initial values, moved from LL95TBL's `DATA` statements.

**Design.** A blanket `USE LLOT95A_MOD`. The module's header says its initializers came from PARMIN's `DATA` statements and are namelist variables; at `rp_1` they were in LL95TBL, and they are in no namelist. At `rp_1`, `main.f` declared the block with its own `NUMTT` (also 70); that declaration is gone.

**Changed since `rp_1`.** New file: `COMMON/LLOT95A/` as a module, with its fixed grids moved from LL95TBL's `DATA` statements.
