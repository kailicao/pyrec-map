## Explanation

**Purpose.** Reads a LAOL89 opacity table for pure metals (no hydrogen or helium), the "pure Z" table.

**How it fits.**
- **Who calls it:** [[setupopac.f#SETUPOPAC|`SETUPOPAC`]], when `LPUREZ` is true, before [[zsulaol.f#ZSULAOL|`ZSULAOL`]] sets up its interpolation.
- **Input:** the formatted file `FPUREZ`, on unit `IOPUREZ` (from `IOUNITS_MOD`).
- **Output, through a module:** `ZLAOL_MOD` (`ZOLAOL(rho, T)`, the grids `ZORHO`, `ZOT`, sizes `NUMRHOZ`, `NUMTZ`), read by `ZSULAOL` and [[gtpurz.f#GTPURZ|`GTPURZ`]].
- **Other module:** `IOUNITS_MOD` (`IOPUREZ`, `ISHORT`).

**The method.** The file has the same layout as the LAOL89 tables of `RDLAOL` (removed since `rp_1`), with one composition: the header with the mix and the hydrogen fraction is read into a dummy array and skipped, then the density and temperature grids and one record of `NUMTZ` opacities per density. The run stops with "Z OPACITY INPUT ERROR." if the file has more than one composition or the grids are too large (104 × 52).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/ZLAOL/` to `ZLAOL_MOD`; the unit `IOPUREZ` of `/NWLAOL/` and `/LUOUT/` to `IOUNITS_MOD`), `IMPLICIT NONE`; the unused `/NEWOPAC/` and `REAL*8` list are gone, which settles the former question 1 (removed).
