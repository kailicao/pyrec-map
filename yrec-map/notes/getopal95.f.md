## Explanation

**Purpose.** `GETOPAL95` is the driver for the OPAL 1995 opacity tables ("7/98 MHP"): given $\rho$, $T$, $X$, $Z$, it finds the interpolation stencil and weights in $T$, $R = \rho/T_6^3$, $X$ and $Z$, handles the table's empty corner at high density, and calls a 2D, 3D or 4D interpolator depending on how far the composition is from the tables already prepared.

**How it fits.**
- **Who calls it:** only [[getopac.f#GETOPAC|GETOPAC]], when `LOPAL95` is set (with $Z$ = 0.1 in metal-rich helium-burning cores).
- **Inputs:** `DL`, `TL`, `X`, `Z`.
- **What it calls:** [[interp.f#INTERP|INTERP]] (four-point Lagrange weights with derivative weights, for $T$ and $R$), [[intrp2.f#INTRP2|INTRP2]] (weights only, for $X$ and $Z$), and one of [[op952d.f#OP952D|OP952D]] (2D, in the table for the surface $X$ and $Z$), [[op953d.f#OP953D|OP953D]] (3D, in the tables for the model's $Z$) or [[op954d.f#OP954D|OP954D]] (4D, in the full set).
- **Outputs:** `O`, `OL`, `QOD`, `QOT`, as from `GETOPAC`.
- **Modules** (COMMON blocks until `rp_1`): the tables `LLOT95A_MOD` (the full set `CAPPA2`, indexed by a combined X–Z table number, and the grids `TGR`, `R0GR`, `XXG`, `ZZG`; read by [[ll95tbl.f#LL95TBL|LL95TBL]]), `LLOT95_MOD` (`CAPPA` at the model's $Z$, `ZTAB`, made by [[op95ztab.f#OP95ZTAB|OP95ZTAB]]), `LLOT95E_MOD` (`CAPPAE` at the surface $X$, `XOP95` (formerly `XTAB`), made by [[op95xtab.f#OP95XTAB|OP95XTAB]]); `OP95INTERP_MOD`, which merges the former `/OP95INDX/` (indices), `/OP95FACT/` (weights) and `/OP95EXT/` (extrapolation flags), shared with the `OP95*D` routines, $\log R$ now named `RHO_T63L` (formerly `RL`, which clashed with the radius elsewhere) and its edge value `RHO_T63LL` (formerly `RLL`); `ACDPTH_MOD` for the flags `LADON`, `LACOUT` (acoustic-depth output; shared with [[calcad.f#CALCAD|CALCAD]], [[envint.f#ENVINT|ENVINT]], [[wrtout.f#WRTOUT|WRTOUT]]).

**The method.**
1. $\log R = \log\rho - 3(\log T - 6)$ (`RHO_T63L`). The run stops if $\log T$ is outside the table. Below the smallest $\log R$, the weights are computed at the table edge and the value is extrapolated linearly later (`LEXTL`).
2. Stencils in $\log T$ (`JT`) and $\log R$ (`JD`), each starting from the last one found.
3. **Empty corner.** Values of 9.9 or more mark missing entries. If the stencil's high-density, high-temperature corner is missing, each of the four temperatures gets its own density stencil (`LSHIFT`), and where even that is outside the data, its weights are computed at the last valid density and the value is extrapolated linearly (`LEXH`, `RLH`).
4. **Which interpolation.** If $Z$ is within a relative $10^{-4}$ of the model table's $Z$: 2D if $X$ is within $10^{-4}$ of the surface table's $X$, else 3D in $X$, $T$, $R$. Otherwise 4D. The 4D path is forced when acoustic-depth output is on (`LADON` and `LACOUT`, "JVS 04/11").
5. **Missing high-$X$ tables.** The $X$ nodes are 0, 0.1, 0.2, 0.35, 0.5, 0.7, 0.8, 0.9, 0.95, 1. For $X \ge 0.8$: if $0.04 \le Z < 0.1$, the $X = 0.95$ table is absent and the stencil is 0.7, 0.8, 0.9 and the last node, set to $1 - Z$; if $Z \ge 0.1$, the last two are absent and the stencil is 0.5, 0.7, 0.8, 0.9. (In 3D the test is on the model table's $Z$, in 4D on each $Z$ node. [[op95ztab.f#OP95ZTAB|OP95ZTAB]] stops the run for $Z > 0.08$, so the 3D case $Z \ge 0.1$ is never reached; the 4D path can still meet the node $Z = 0.1$.)

**KC's changes.** The elements of `/ACDPTH/` (now `ACDPTH_MOD`) were reordered (2025-05-30).

**Changed since `rp_1`.** Declarations and names only: COMMON blocks to modules (the three interpolation blocks merged into `OP95INTERP_MOD`), `IMPLICIT NONE`, `RL`, `RLL` and `XTAB` renamed `RHO_T63L`, `RHO_T63LL` and `XOP95`, and the unused parameters `NUMXZ` and `JSON` removed. The computation is unchanged; no question settled.

## Questions for the experts

1. **Wrong array in the empty-corner search.** The stencil search for each temperature (`LSHIFT` block) tests `CAPPA2(IXX,ITT,J)`, with `IXX` = `JX(1,1)`, an index into the $X$ tables of `CAPPA`. `CAPPA2`'s first index is the combined X–Z table number (`OP954D` and `OP95ZTAB` use it so). Should it read `CAPPA(IXX,ITT,J)`?
2. **`LSHIFT` left over from the last call.** When $X < 0.2$ and `JT` ≤ 5, the code jumps past the line that resets `LSHIFT` and `LEXTH` to false, so their values from the previous call (the routine has `SAVE`) decide the density stencil. The flag `LCHK` set on that path is never used. Is a check missing there?
3. **Stale `JX(1,1)` in the corner test.** The empty-corner test uses `JX(1,1)` before it is updated for the current $X$ (that happens later, in the 3D and 4D branches). Intended?
4. **Header vs code.** The header says the facility uses "cubic spline interpolation"; the code uses four-point Lagrange weights throughout.
5. **Negative index.** In the `LSHIFT` search, `JD(I) = J - 3` can be zero or negative if the only valid densities are the first two. Can that happen?

### GETOPAL95

Driver for the OPAL 1995 opacities: stencils and weights in $T$, $R$, $X$, $Z$, the empty-corner handling, and the choice of 2D, 3D or 4D interpolation (method above).
