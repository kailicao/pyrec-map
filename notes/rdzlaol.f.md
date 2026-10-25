## Explanation

**Purpose.** Reads a LAOL89 opacity table for pure metals (no hydrogen or helium), the "pure Z" table.

**How it fits.**
- **Who calls it:** [[setupopac.f#SETUPOPAC|`SETUPOPAC`]], when `LPUREZ` is true, before [[zsulaol.f#ZSULAOL|`ZSULAOL`]] sets up its interpolation.
- **Input:** the formatted file `FPUREZ`, on unit `IOPUREZ` (from `/NWLAOL/`).
- **Output, through COMMON:** `/ZLAOL/` (`ZOLAOL(rho, T)`, the grids `ZORHO`, `ZOT`, sizes `NUMRHOZ`, `NUMTZ`), read by `ZSULAOL` and [[gtpurz.f#GTPURZ|`GTPURZ`]].
- **Other COMMON:** `/NWLAOL/` (for the unit number), `/NEWOPAC/` (declared, not used), `/LUOUT/` (`ISHORT`).

**The method.** The file has the same layout as the LAOL89 tables of [[rdlaol.f#RDLAOL|`RDLAOL`]], with one composition: the header with the mix and the hydrogen fraction is read into a dummy array and skipped, then the density and temperature grids and one record of `NUMTZ` opacities per density. The run stops with "Z OPACITY INPUT ERROR." if the file has more than one composition or the grids are too large (104 × 52).

## Questions for the experts

1. **Unused declarations.** `/NEWOPAC/` and the `REAL*8` list `ZLAOL1, …` are declared but not used here. Remove them?
