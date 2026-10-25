## Explanation

**Purpose.** `GTLAOL2` is [[gtlaol.f#GTLAOL|`GTLAOL`]] for the second Livermore table (the comment: "identical to GTLAOL except gets opacity from second table"), the table at the second metallicity used when the run interpolates between two $Z$ (`L2Z`).

**How it fits.** Called only by [[getopac.f#GETOPAC|`GETOPAC`]], which then interpolates linearly in $Z$ between `GTLAOL` (at `ZLAOL1`) and `GTLAOL2` (at `ZLAOL2`). It reads the grids from `NWLAOL2` (`OXA2`, `OT2`, `NXYZ2`, `NT2`; filled by [[rdlaol.f#RDLAOL|`RDLAOL`]]) and the splines from `SLAOL2` (filled by [[sulaol.f#SULAOL|`SULAOL`]]), but the tolerance `TOLLAOL` from the first table's `NWLAOL`. Calls `LOCATE`, `XRNG4`, `CSPLINE`, `SPLINT`.

**The method.** Line for line that of [[gtlaol.f#GTLAOL|`GTLAOL`]], with the second table's arrays.

## Questions for the experts

1. **Unused blocks.** It declares `SLAOL` and `ZRAMP` (`RSCLZC`, …, `LZRAMP`) but uses neither. Can they go?
2. **Duplicated code.** The routine duplicates `GTLAOL`; one routine with the table passed as arguments would remove the risk of the two drifting apart. The same questions as for `GTLAOL` apply (the margin `LOG(TOLLAOL)`, the chord-slope derivatives).

### GTLAOL2

`GTLAOL` on the second-$Z$ table.
