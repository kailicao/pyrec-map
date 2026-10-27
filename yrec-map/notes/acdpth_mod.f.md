## Explanation

**Purpose.** `ACDPTH_MOD` holds the acoustic-depth output: the results of [[calcad.f#CALCAD|`CALCAD`]] and the switches that decide at which ages it runs, shared by 6 routines. It replaces `COMMON/ACDPTH/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`. Five switches and the ages carry initial values, moved from PARMIN's `DATA` statements.

**What its variables hold, who sets them, who reads them.**
- `TAUCZN`, `TCZ`, `TNORM`, `TAUHE`, `WHE`, `TATMOS`: the acoustic depths computed by `CALCAD` (`TAUCZN` $= t_\mathrm{CZ}/t_\mathrm{norm}$; `TATMOS` is always 0 there); [[wrtout.f#WRTOUT|`WRTOUT`]] writes them, and resets `TAUCZN` to 0 when there is no convective envelope.
- `DELADJ(JSON)`: $\nabla_\mathrm{ad}$ at each point, set and read by `CALCAD`.
- `LACOUT`: the master switch, `.FALSE.`; read by the [[main.f#(file level)|main program]], [[parmin.f#PARMIN|`PARMIN`]] (the output file's name), [[getopal95.f#GETOPAL95|`GETOPAL95`]] and `WRTOUT`.
- `AGEOUT(5)`: the ages (Gyr) at which to write, 0.5, 1, 5, 10, 20; read by the main program.
- `LADON`, `LCLCD`, `LJLAST`, `LJWRT`: set by the main program from `LACOUT` and the age. `LADON` is read by `GETOPAL95` (four-point interpolation) and `WRTOUT`; `LCLCD` by `CALCAD` and [[envint.f#ENVINT|`ENVINT`]]; `LJLAST` by `WRTOUT`; `LJWRT` by the main program.
- `ACATMR`, `ACATMD`, `ACATMP`, `ACATMT` (`JSON` each) and `LAOLY`: set and read nowhere.

**Design.** A blanket `USE ACDPTH_MOD` in each of the six routines. The module's header calls the initialized members namelist variables, but `LACOUT` is in no namelist and is set nowhere, so it stays `.FALSE.` and the acoustic-depth output never runs (so also at `rp_1`, where its default came from a `DATA` statement).

**Changed since `rp_1`.** New file: `COMMON/ACDPTH/` as a module, with the defaults of `AGEOUT`, `LCLCD`, `LJLAST`, `LJWRT` and `LACOUT` moved from PARMIN.

## Questions for the experts

1. **A switch that cannot be turned on.** `LACOUT` is in no namelist and no routine sets it, so the acoustic-depth branch (CALCAD, the age outputs) is dead unless the source is edited. Should it be added to a namelist, or the branch removed?
2. **Unused members.** `ACATMR`, `ACATMD`, `ACATMP`, `ACATMT` (four arrays of 5000) and `LAOLY` are used nowhere. Can they go?
