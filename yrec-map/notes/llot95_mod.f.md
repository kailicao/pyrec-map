## Explanation

**Purpose.** `LLOT95_MOD` holds the OPAL95 opacity tables interpolated to the current surface $Z$, one table for each $X$, and that $Z$, shared by 4 routines. It replaces `COMMON/LLOT95/` (MHP via Claude, 10/14/26). The table dimensions `NUMX` = 10, `NUMT` = 70, `NUMD` = 19 are `PRIVATE`, since other tables use the same names with other values.

**What its variables hold, who sets them, who reads them.**
- `CAPPA(NUMX,NUMT,NUMD)`: $\log\kappa$ on the ($X$, $\log T$, $\log R$) grid at $Z$ = `ZTAB`, interpolated in $Z$ (four points) by [[op95ztab.f#OP95ZTAB|`OP95ZTAB`]] from all the tables (`CAPPA2` in [[llot95a_mod.f#LLOT95A_MOD|`LLOT95A_MOD`]]).
- `ZTAB`: the $Z$ of those tables, set by `OP95ZTAB`.
- Read by [[op95xtab.f#OP95XTAB|`OP95XTAB`]], which interpolates them further to one $X$, [[op953d.f#OP953D|`OP953D`]] (interpolation in $X$, $T$, $R$) and [[getopal95.f#GETOPAL95|`GETOPAL95`]], which compares the local $Z$ with `ZTAB` to choose between a 2D, 3D or 4D interpolation.

**Design.** A blanket `USE LLOT95_MOD`. At `rp_1`, `calcad.f` declared a shortened copy of the block, `ZTAB` alone, which under storage association was in fact `CAPPA(1,1,1)` (harmless: CALCAD used it only in commented-out lines), and `main.f` one dimensioned with its own `NUMTT` (also 70); both declarations are gone.

**Changed since `rp_1`.** New file: `COMMON/LLOT95/` as a module.
