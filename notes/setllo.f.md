## Explanation

**Purpose.** Reads the OPAL 1992 interior opacity tables ("LL", for Livermore, by the names) for three compositions, and, when two metallicities are needed, a second set; then sets up their interpolation.

**How it fits.**
- **Who calls it:** [[setupopac.f#SETUPOPAC|`SETUPOPAC`]], when `LOPAL92` is true, followed by [[ll4th.f#LL4TH|`LL4TH`]].
- **Inputs:** the file `FLLDAT` (unit `ILLDAT`, `/LUNUM/`) and, with `L2Z` (`/NEWOPAC/`), `FOPAL2` (unit `IOOPAL2`, `/ZRAMP/`).
- **Outputs, through COMMON:** `/GLLOT/` (the grids: `GRIDT` = $\log T$, `GRIDX` = $X$, `GRHOT3` = $\log(\rho/T^3)$ by the comment), `/LLOT/` (`OPACITY`, `NUMXM`, `NUMTM`), and `/GLLOT2/`, `/LLOT2/` for the second table. Read by [[ylloc.f#YLLOC|`YLLOC`]] (called at the end), `LL4TH`, and the interpolators [[yllo2d.f#YLLO2D|`YLLO2D`]], [[yllo3d.f#YLLO3D|`YLLO3D`]] and their `…2` twins.

**The method.** For each of the three compositions: a header with $X$ and $Z$; the 17 values of $\log(\rho/T^3)$; then up to 50 rows, each with $T$ and 17 opacities (stored as read, probably $\log\kappa$). The temperature is stored as $\log_{10} T$. `END=93` and `END=97` catch the end of the file: a last composition with fewer than 50 rows, or fewer than three compositions; `NUMTM` and `NUMXM` record the counts. A composition with fewer rows that is not the last one is not detected: the next composition's header would be read as a data row.

## Questions for the experts

1. **`NUMTM` after an early end.** `NUMTM = K-1` is set for each composition, so it keeps the value of the last one; and `GRIDT` is overwritten by each. This assumes all compositions have the same temperatures. Is that guaranteed for these tables?
2. **Unused values.** `GRIDY` and `GRIDZ` (local) are computed and never used; the second table even writes its $Z$ into the first table's `GRIDZ`. The table's $Z$ is therefore not checked against `ZOPAL1` or `ZOPAL2`. Should it be? `CONST` and `/GRAVS3/` are also unused.
3. **No `STATUS='OLD'`.** The files are opened without a status, so a wrong file name creates an empty file and the run fails later, at `END=97`, with `NUMXM` = 0 and no message.
