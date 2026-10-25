## Explanation

**Purpose.** Reads the Los Alamos opacity tables of 1989 (LAOL89) for the stellar interior, and, when two metallicities are needed, a second LAOL89 table.

**How it fits.**
- **Who calls it:** [[setupopac.f#SETUPOPAC|`SETUPOPAC`]], when `LLAOL89` is true, right before [[sulaol.f#SULAOL|`SULAOL`]], which sets up the interpolation in what is read here.
- **Inputs:** the formatted table files `FLAOL` and, when `L2Z` is true, `FLAOL2` (names passed from the namelist through [[setups.f#SETUPS|`SETUPS`]]), on units `IOLAOL` and `IOLAOL2`.
- **Outputs, through COMMON:**
  - `/NWLAOL/`: the first table, `OLAOL(X, rho, T)` with its grids `OXA` (hydrogen mass fractions), `ORHO`, `OT` and sizes `NUMOFXYZ`, `NUMRHO`, `NUMT`. Read by [[sulaol.f#SULAOL|`SULAOL`]], [[gtlaol.f#GTLAOL|`GTLAOL`]], [[gtlaol2.f#GTLAOL2|`GTLAOL2`]], [[getopac.f#GETOPAC|`GETOPAC`]] and others.
  - `/NWLAOL2/`: the second table (`OLAOL2`, `OXA2`, `ORHO2`, `OT2`), read by `SULAOL` and `GTLAOL2`.
  - `/DEBHU/`: the relative abundances `ZDH(18)` of 18 metals, for the Debye–Hückel correction in [[eqrelv.f#EQRELV|`EQRELV`]]; the first three (C, N, O) are later replaced by the model's own abundances (question 3).
  - the argument `V(12)`: the relative abundances of the Cox–Stewart metal mix (C, N, O, Ne, Na, Mg, Si, Ar, Fe), which `SETUPOPAC` passes back to `SETUPS`.
- **Other COMMON:** `/NEWOPAC/` (the opacity switches, here `L2Z`), `/ZRAMP/` (the unit `IOLAOL2`), `/LUOUT/` (the unit `ISHORT` for messages).

**The method.** A formatted read, in this order: the array sizes; `ZLOT` and the Cox–Stewart mix; `ZHIT` and the 18 Debye–Hückel abundances; the grids in $X$, $\rho$ and $T$; then the opacities, one record of `NUMT` values per $(X,\rho)$ pair. The second table is read the same way.

**Design.** The fixed sizes are 12 × 104 × 52. The table's own metallicities (`ZLOT`, `ZHIT`) are read into local variables and not kept, and the second table's mix (`V2`, `ZDH2`, `ZLOT2`, `ZHIT2`) is read and discarded.

## Questions for the experts

1. **The size check.** `OLAOL` and `OXA` have 12 entries in $X$, but the check stops when `NUMOFXYZ` exceeds 11. Is 11 intended?
2. **Unused metallicities.** `ZLOT` and `ZHIT` (and `ZLOT2`, `ZHIT2`) are read and thrown away. Should the code check them against the metallicities the run expects (`ZLAOL1`, `ZLAOL2` in `/NEWOPAC/`)?
3. **`ZDH`: partly the table's, partly the model's.** Of the 18 abundances in `ZDH` read here (scaled to sum to `ZHIT`, by the comment), only the first three (C, N, O) are later replaced by the model's mass fractions, in [[coefft.f#COEFFT|`COEFFT`]], [[hsubp.f#HSUBP|`HSUBP`]], [[crrect.f#CRRECT|`CRRECT`]], [[starin.f#STARIN|`STARIN`]] and others; the other 15 keep the table's values and enter the Debye–Hückel sum in [[eqrelv.f#EQRELV|`EQRELV`]]. They are not rescaled to the model's $Z$. Is this mix of the model's C, N, O and the table's heavier metals intended?
4. **"WEIGTH".** A typo in the comments ("BY WEIGTH"); harmless.
