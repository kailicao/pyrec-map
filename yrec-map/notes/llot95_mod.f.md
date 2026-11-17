## Explanation

**Purpose.** `LLOT95_MOD` holds the OPAL95 opacity tables interpolated to the current surface $`Z`$, one table for each $`X`$, and that $`Z`$, shared by 4 routines. It replaces `COMMON/LLOT95/` (MHP via Claude, 10/14/26). The table dimensions `NUMX` = 10, `NUMT` = 70, `NUMD` = 19 are `PRIVATE`, since other tables use the same names with other values.

**What its variables hold, who sets them, who reads them.**
- `CAPPA(NUMX,NUMT,NUMD)`: $`\log\kappa`$ on the ($`X`$, $`\log T`$, $`\log R`$) grid at $`Z`$ = `ZTAB`, interpolated in $`Z`$ (four points) by [`OP95ZTAB`](op95ztab.f.md#op95ztab) from all the tables (`CAPPA2` in [`LLOT95A_MOD`](llot95a_mod.f.md#llot95a_mod)).
- `ZTAB`: the $`Z`$ of those tables, set by `OP95ZTAB`.
- Read by [`OP95XTAB`](op95xtab.f.md#op95xtab), which interpolates them further to one $`X`$, [`OP953D`](op953d.f.md#op953d) (interpolation in $`X`$, $`T`$, $`R`$) and [`GETOPAL95`](getopal95.f.md#getopal95), which compares the local $`Z`$ with `ZTAB` to choose between a 2D, 3D or 4D interpolation.

**Design.** A blanket `USE LLOT95_MOD`. At `rp_1`, `calcad.f` declared a shortened copy of the block, `ZTAB` alone, which under storage association was in fact `CAPPA(1,1,1)` (harmless: CALCAD used it only in commented-out lines), and `main.f` one dimensioned with its own `NUMTT` (also 70); both declarations are gone.

**Changed since `rp_1`.** New file: `COMMON/LLOT95/` as a module.
