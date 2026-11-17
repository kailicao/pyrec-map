## Explanation

**Purpose.** Reads a LAOL89 opacity table for pure metals (no hydrogen or helium), the "pure Z" table.

**How it fits.**
- **Who calls it:** [`SETUPOPAC`](setupopac.f.md#setupopac), when `LPUREZ` is true, before [`ZSULAOL`](zsulaol.f.md#zsulaol) sets up its interpolation.
- **Input:** the formatted file `FPUREZ`, on unit `IOPUREZ` (from `IOUNITS_MOD`).
- **Output, through a module:** `ZLAOL_MOD` (`ZOLAOL(rho, T)`, the grids `ZORHO`, `ZOT`, sizes `NUMRHOZ`, `NUMTZ`), read by `ZSULAOL` and [`GTPURZ`](gtpurz.f.md#gtpurz).
- **Other module:** `IOUNITS_MOD` (`IOPUREZ`, `ISHORT`).

**The method.** The file has the same layout as the LAOL89 tables of `RDLAOL` (removed since `rp_1`), with one composition: the header with the mix and the hydrogen fraction is read into a dummy array and skipped, then the density and temperature grids and, for each density, a heading line and its `NUMTZ` opacities, six to a record ([lines 65–70](https://github.com/yreclab/yrec/blob/7be4133/src/rdzlaol.f#L65-L70)). The run stops with "Z OPACITY INPUT ERROR." if the file has more than one composition or the grids are too large ($`104 \times 52`$).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/ZLAOL/` to `ZLAOL_MOD`; the unit `IOPUREZ` of `/NWLAOL/` and `/LUOUT/` to `IOUNITS_MOD`), `IMPLICIT NONE`; the unused `/NEWOPAC/` and `REAL*8` list are gone, which settles the former question 1 (removed).

**Changed since `a8a5950`.** The stop on a bad file ("Z OPACITY INPUT ERROR.") now exits with status 3, the code for input errors, instead of a bare `STOP` (`KNOWN_ISSUES.md`, issue 38).
