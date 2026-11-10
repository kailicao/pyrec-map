## Explanation

**Purpose.** `ACDPTH_MOD` holds the acoustic-depth output: the results of [[calcad.f#CALCAD|`CALCAD`]] and the switches that decide at which ages it runs, shared by 6 routines. It replaces `COMMON/ACDPTH/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`. Five switches and the ages carry initial values, moved from PARMIN's `DATA` statements.

**What its variables hold, who sets them, who reads them.**
- `TAUCZN`, `TCZ`, `TNORM`, `TAUHE`, `WHE`, `TATMOS`: the acoustic depths computed by `CALCAD` (`TAUCZN` $= t_\mathrm{CZ}/t_\mathrm{norm}$; `TATMOS` is always 0 there); [[wrtout.f#WRTOUT|`WRTOUT`]] writes them, and resets `TAUCZN` to 0 when there is no convective envelope.
- `DELADJ(JSON)`: $\nabla_\mathrm{ad}$ at each point, set and read by `CALCAD`.
- `LACOUT`: the master switch, `.FALSE.`; read by the [[main.f#(file level)|main program]], [[parmin.f#PARMIN|`PARMIN`]] (the output file's name), [[getopal95.f#GETOPAL95|`GETOPAL95`]] and `WRTOUT`.
- `AGEOUT(5)`: the ages (Gyr) at which to write, 0.5, 1, 5, 10, 20; read by the main program.
- `LADON`, `LCLCD`, `LJLAST`, `LJWRT`: set by the main program from `LACOUT` and the age. `LADON` is read by `GETOPAL95` (four-point interpolation) and `WRTOUT`; `LCLCD` by `CALCAD` and [[envint.f#ENVINT|`ENVINT`]]; `LJLAST` by `WRTOUT`; `LJWRT` by the main program.
- `ACATMR`, `ACATMD`, `ACATMP`, `ACATMT` (`JSON` each) and `LAOLY`: set and read nowhere (unused?; [[#L44-L47]]; [[#L54]]).

**Design.** A blanket `USE ACDPTH_MOD` in each of the six routines. The module's header calls the initialized members namelist variables, but `LACOUT` is in no namelist and is set nowhere, so it stays `.FALSE.` and the acoustic-depth output never runs (so also at `rp_1`, where its default came from a `DATA` statement).

**Changed since `rp_1`.** New file: `COMMON/ACDPTH/` as a module, with the defaults of `AGEOUT`, `LCLCD`, `LJLAST`, `LJWRT` and `LACOUT` moved from PARMIN.

## Bugs, by priority

1. **(cannot be reached)** **A switch that cannot be turned on.** ([[#L20-L25]]; [[#L55]]) `LACOUT` is in no namelist and no routine sets it, so the acoustic-depth branch (CALCAD, the age outputs in the main program, [[main.f#L625-L655]], and GETOPAL95's four-point interpolation, [[getopal95.f#L254]]) is dead unless the source is edited, although the module's header calls the initialized members namelist variables.

    **A possible fix:** a choice for the developers: add `LACOUT` to a namelist (after the bugs on [[calcad.f#CALCAD|CALCAD]]'s page are checked), or remove the branch.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged; a module has no statements to count, so the lines sat in CALCAD, one of them at its every call): None of CALCAD's lines was reached in 34 runs: 26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones, so the acoustic-depth branch never ran, and it cannot be reached at 7be4133: A search of `src/` finds `LACOUT` only read ([[getopal95.f#L254]]; [[main.f#L625-L655]]; [[wrtout.f#L696]]; [[parmin.f#L834]]), and in no namelist group. Running the branch needs `LACOUT` set true in the source, which was not done here. Intent: The conversion plan knows the path is unexercised (`docs/archive/F90_CONVERSION_PLAN.md`: "the same kind of gap as `LADON`/`LACOUT` leaving the `ISOUND` write path unexercised"), but nothing says the switch was meant to be closed, and the header calls the initialized members namelist variables ([[#L23-L24]]).
