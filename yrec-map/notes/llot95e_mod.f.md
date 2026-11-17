## Explanation

**Purpose.** `LLOT95E_MOD` holds the OPAL95 opacity table interpolated to the surface composition (one $`X`$ and $`Z`$), and that $`X`$, shared by 3 routines. It replaces `COMMON/LLOT95E/` (MHP via Claude, 10/14/26), with its member `XTAB` renamed `XOP95` (a name collision resolved before the conversion). The table dimensions `NUMT` = 70, `NUMD` = 19 are `PRIVATE`.

**What its variables hold, who sets them, who reads them.**
- `CAPPAE(NUMT,NUMD)`: $`\log\kappa`$ on the ($`\log T`$, $`\log R`$) grid at $`X`$ = `XOP95` and $`Z`$ = `ZTAB` ([`LLOT95_MOD`](llot95_mod.f.md#llot95_mod)), interpolated in $`X`$ (four points) by [`OP95XTAB`](op95xtab.f.md#op95xtab), which [`SETUPOPAC`](setupopac.f.md#setupopac) and [`SURFOPAC`](surfopac.f.md#surfopac) call with the envelope's $`X`$. Read by [`OP952D`](op952d.f.md#op952d) (interpolation in $`T`$ and $`R`$).
- `XOP95`: the $`X`$ of that table, set by `OP95XTAB`; read by [`GETOPAL95`](getopal95.f.md#getopal95), which uses the 2D interpolation when the local $`X`$ and $`Z`$ match the table's to $`10^{-4}`$.

**Design.** A blanket `USE LLOT95E_MOD`. At `rp_1`, `main.f` declared the block with its own `NUMTT` (also 70); that declaration is gone.

**Changed since `rp_1`.** New file: `COMMON/LLOT95E/` as a module, `XTAB` renamed `XOP95`.
