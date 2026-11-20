## Explanation

**Purpose.** `DIMENSIONS_MOD` holds `JSON` = 5000, the maximum number of shells in a model, the one structural array dimension shared by the whole code (MHP via Claude, 10/15/26). It replaces the statement `PARAMETER(JSON=5000)`, repeated in 108 files when the module was made (in 122 at `rp_1`); it is not a COMMON block.

**Who uses it.** 142 files: the routines that dimension arrays by the number of shells, and, since 10/20/26, the block modules sized on `JSON`, such as [`DEUTER_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/deuter_mod.f#L19-L33), which used to declare private copies (36 then, as the header says; 34 at 7be4133, `BURN_MOD` and `GRAB_MOD` having been removed since). The module must be compiled before them (the Makefile says so).

**Design.** The header explains what stays out: the dimensions of the input tables (such as `NUMT`, 70 for the OPAL95 opacities and 85 for the ALEX06 tables of Ferguson et al. [2005](https://ui.adsabs.harvard.edu/abs/2005ApJ...623..585F)) differ between tables and stay `PRIVATE` in each table's module, and scratch bounds such as `NMAX` stay local to their routines. A file that gains `USE DIMENSIONS_MOD` must drop its own `PARAMETER(JSON=5000)`.

**Changed since `rp_1`.** New file: the repeated `PARAMETER(JSON=5000)` as a module.
