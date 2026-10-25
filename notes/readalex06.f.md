## Explanation

**Purpose.** Reads the low-temperature opacity tables of Ferguson et al. (2005, ApJ 623, 585), called the "Alexander 2006" tables in the code, for all compositions at once.

**How it fits.**
- **Who calls it:** [[setupopac.f#SETUPOPAC|`SETUPOPAC`]], when `LALEX06` is true.
- **Input:** the formatted file `FALEX06` (its name passed through `SETUPOPAC` since the change "MHP 8/25"), opened on unit `IALEX06` from `/ALEX06/` (set in [[parmin.f#PARMIN|`PARMIN`]]).
- **Outputs, through COMMON:**
  - `/ALOT06ALL/`: `CAPTALEX06(143, 85, 19)`, all tables, read by [[alex06tab.f#ALEX06TAB|`ALEX06TAB`]];
  - `/GALOT06/`: the grids `TGR06` ($\log T$), `XXG06` ($X$), `R0GR06` ($\log R$), `ZZG06` ($Z$), set by `DATA` statements here and read by `ALEX06TAB` and [[getalex06.f#GETALEX06|`GETALEX06`]];
  - `/ALOT06/`: the table for one composition, `CAPALEX06(85, 19)`, initialized here to the first table ($X = 0$, $Z = 0$), and the composition and starting indices (`XE`, `ZE`, `IX`, `IT`, `ID`). `ALEX06TAB` rebuilds it for the envelope's composition, and `GETALEX06` interpolates in it.

**The tables.** From the header comments: $X$ = 0, 0.1, 0.2, 0.35, 0.5, 0.7, 0.8, 0.9 and $1-Z$; 16 values of $Z$ from 0 to 0.1; 85 values of $\log T$ from 2.7 to 4.5 (0.05 dex steps, 0.01 dex between 2.9 and 3.5); 19 values of $\log R$ from $-8$ to 1, with

$$R = \frac{\rho}{T_6^{\,3}} .$$

The tables at $X = 1-Z$ exist for 15 values of $Z$ only (none for $Z = 0.1$), so there are $8 \times 16 + 15 = 143$ compositions (`NUMXZ`), stored at index $(i_X - 1)\cdot 16 + i_Z$.

**The method.** For each composition, the routine reads the header ($X$, $Z$) and checks it against the grid; reads the $\log R$ row and checks it; then reads the 85 temperature rows in descending order of $T$, checking each $\log T$ against `TGR06`. A mismatch prints an error and stops the run.

## Questions for the experts

1. **A check that does not stop.** In the first loop (the eight $X$ values below $1-Z$), the `STOP` after a mismatch of $X$ or $Z$ is commented out, so the run goes on after printing "RUN STOPPED". In the second loop it does stop. Which is intended?
2. **Only 16 of 19 densities checked.** Both loops check `R0GRTAB(KK)` for `KK = 1, 16`, not up to `NUMD` = 19. Why are the last three values of $\log R$ not checked?
3. **Exact comparisons of reals.** The checks compare values read with `F9.6` or `F7.3` against `DATA` values with `.NE.`. This works when the decimal strings round to the same binary number, but a table written with a slightly different rounding would stop the run. Use a tolerance?
4. **Stale comment.** The comment on the storage index speaks of "15 sets of metal abundance with 7 sets of hydrogen" and of $Z = 0.1$ "already read in at X=0.9", while the code has 16 values of $Z$ and 9 of $X$.
5. **No `STATUS='OLD'`.** The file is opened without `STATUS`, so a wrong name creates an empty file and fails at the first read rather than at the open.
