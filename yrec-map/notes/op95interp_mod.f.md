## Explanation

**Purpose.** `OP95INTERP_MOD` holds the interpolation stencil and weights for the OPAL 1995 opacity tables: [[getopal95.f#GETOPAL95|`GETOPAL95`]] computes them for the current $\rho$, $T$, $X$, $Z$, and the interpolators [[op952d.f#OP952D|`OP952D`]], [[op953d.f#OP953D|`OP953D`]] and [[op954d.f#OP954D|`OP954D`]] apply them. Shared by 6 routines. It replaces three `rp_1` blocks, `COMMON/OP95INDX/` (the indices), `COMMON/OP95FACT/` (the weights) and `COMMON/OP95EXT/` (extrapolation), first merged into one `COMMON/OP95INTERP/` and then made a module (MHP via Claude, 10/9–10/14/26); `OP95EXT`'s `RL` and `RLL` are renamed `RHO_T63L` and `RHO_T63LL`, since `RL` means $\log r$ everywhere else in the code.

**What its variables hold, who sets them, who reads them.** All are set by `GETOPAL95` on each call; the interpolators read them.
- `JZ`, `JX(4,4)`, `JT`, `JD(4)`: the first table index of each four-point stencil, in $Z$, in $X$ (for each of the four $Z$), in $T$, and in $R$ (for each of the four $T$, since the stencil in $R$ may shift at high density). Initialized to 1, the values of [[ll95tbl.f#LL95TBL|`LL95TBL`]]'s `DATA` statement at `rp_1`.
- `BZ(4)`, `BX(4,4)`, `BT(4)`, `BD(4,4)`: the four-point weights in $Z$, $X$, $T$ and $R$ ([[intrp2.f#INTRP2|`INTRP2`]] for $Z$ and $X$, [[interp.f#INTERP|`INTERP`]] for $T$ and $R$); `BTT(4)`, `BDD(4,4)`: `INTERP`'s weights for the derivatives in $T$ and $R$.
- `RHO_T63L`: $\log R = \log\rho - 3(\log T - 6)$, the table's density variable; `RHO_T63LL`: the table's lowest $\log R$, used in place of `RHO_T63L` when extrapolating below the table.
- `LEXTL`: extrapolation below the table in $R$; `LEXTH`, `LEXH(4)`: extrapolation above it (the empty high-density corner), overall and for each of the four temperatures; `RLH(4)`: the table edge in $\log R$ at each temperature, from which the extrapolation is linear.

**Design.** A blanket `USE OP95INTERP_MOD` in each routine; the [[main.f#(file level)|main program]] and `LL95TBL` use it but refer to none of its names. The module's header says the four initialized indices came from PARMIN's `DATA` statements and are namelist variables; they came from `LL95TBL`'s `DATA` statement and are in no namelist.

**Changed since `rp_1`.** New file: `COMMON/OP95INDX/`, `/OP95FACT/` and `/OP95EXT/` as one module, with `RL`, `RLL` renamed `RHO_T63L`, `RHO_T63LL` and the indices' `DATA` moved from `LL95TBL`.
