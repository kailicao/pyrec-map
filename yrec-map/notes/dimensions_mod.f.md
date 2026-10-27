## Explanation

**Purpose.** `DIMENSIONS_MOD` holds `JSON` = 5000, the maximum number of shells in a model, the one structural array dimension shared by the whole code (MHP via Claude, 10/15/26). It replaces the statement `PARAMETER(JSON=5000)` that 108 files repeated at `rp_1`; it is not a COMMON block.

**Who uses it.** 144 files: the routines that dimension arrays by the number of shells, and, since 10/20/26, the 36 block modules sized on `JSON` (such as [[deuter_mod.f#DEUTER_MOD|`DEUTER_MOD`]]), which used to declare private copies. The module must be compiled before them (the Makefile says so).

**Design.** The header explains what stays out: the dimensions of the input tables (such as `NUMT`, 70 for the OPAL95 opacities and 85 for Alexander 2006) differ between tables and stay `PRIVATE` in each table's module, and scratch bounds such as `NMAX` stay local to their routines. A file that gains `USE DIMENSIONS_MOD` must drop its own `PARAMETER(JSON=5000)`.

**Changed since `rp_1`.** New file: the repeated `PARAMETER(JSON=5000)` as a module.
