## Explanation

**Purpose.** `LLOT95E_MOD` holds the OPAL95 opacity table interpolated to the surface composition (one $X$ and $Z$), and that $X$, shared by 3 routines. It replaces `COMMON/LLOT95E/` (MHP via Claude, 10/14/26), with its member `XTAB` renamed `XOP95` (a name collision resolved before the conversion). The table dimensions `NUMT` = 70, `NUMD` = 19 are `PRIVATE`.

**What its variables hold, who sets them, who reads them.**
- `CAPPAE(NUMT,NUMD)`: $\log\kappa$ on the ($\log T$, $\log R$) grid at $X$ = `XOP95` and $Z$ = `ZTAB` ([[llot95_mod.f#LLOT95_MOD|`LLOT95_MOD`]]), interpolated in $X$ (four points) by [[op95xtab.f#OP95XTAB|`OP95XTAB`]], which [[setupopac.f#SETUPOPAC|`SETUPOPAC`]] and [[surfopac.f#SURFOPAC|`SURFOPAC`]] call with the envelope's $X$. Read by [[op952d.f#OP952D|`OP952D`]] (interpolation in $T$ and $R$).
- `XOP95`: the $X$ of that table, set by `OP95XTAB`; read by [[getopal95.f#GETOPAL95|`GETOPAL95`]], which uses the 2D interpolation when the local $X$ and $Z$ match the table's to $10^{-4}$.

**Design.** A blanket `USE LLOT95E_MOD`. At `rp_1`, `main.f` declared the block with its own `NUMTT` (also 70); that declaration is gone.

**Changed since `rp_1`.** New file: `COMMON/LLOT95E/` as a module, `XTAB` renamed `XOP95`.
