## Explanation

**Purpose.** Reads the Kurucz low-temperature opacity table (and, when two metallicities are needed, a second one), then sets up its interpolation coefficients.

**How it fits.**
- **Who calls it:** [[setupopac.f#SETUPOPAC|`SETUPOPAC`]], when `LKUR90` is true (and neither of the Alexander/Ferguson options is chosen).
- **Inputs:** the files `FKUR` (unit `IKUR`, from `/LUNUM/`) and, when `L2Z` is true (`/NEWOPAC/`), `FKUR2` (unit `IKUR2`, from `/MISCOPAC/`).
- **Outputs, through COMMON:** `/GKRZ/` (`GRIDT`, the temperature grid), `/KRZ/` (`OPACITY(T, i)` and `RHO(T, i)`, `NUMTM`), and `/GKRZ2/`, `/KRZ2/` for the second table. They are read by [[ykoeff.f#YKOEFF|`YKOEFF`]], called at the end, and by [[kurucz.f#KURUCZ|`KURUCZ`]] and [[kurucz2.f#KURUCZ2|`KURUCZ2`]], which interpolate.

**The method.** After a two-line header, each record holds the temperature `TOUT`, the pressure, five opacity columns (`OKURU0`, `OKURU1`, `OKURU2`, `OKURU4`, `OKURU8`), electron and atom densities and the density `DENS`. A new temperature starts a new row of the grid; within a row, entries are stored in the order read. Only the first opacity column is kept, as $\kappa = 10^{\,\texttt{OKURU0}}$, with its density; the other columns are read and dropped. Records that fail to read are skipped (`ERR=110`). The run stops with "KURUCZ INPUT ERROR" if there are more than 60 temperatures (`NUMT`).

## Questions for the experts

1. **No check on the number of densities.** `ID` grows for every record at one temperature, but nothing checks it against `NUMD` = 50; a longer row would write past `OPACITY` and `RHO`. Add a check?
2. **Bad records skipped silently.** `ERR=110` skips any record that fails to read, which also hides a corrupted table. Is it meant only for the header and separator lines?
3. **Which opacity column?** Only `OKURU0` is used. What do the other four columns hold (by their names, perhaps different microturbulent velocities, 0, 1, 2, 4, 8 km/s)? The choice of column 0 should be documented.
4. **Comment and unused values.** The comment above `/KRZ/` says "LOS ALAMOS OPACITY", a leftover from another reader; `CONST` = 11604.5 and `NUMX` are not used.
