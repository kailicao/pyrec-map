## Explanation

**Purpose.** `version.f` holds the version of YREC and the git commit it was built from, and its one routine `SETVERSION` hands them to the caller. The version, `YREC_VERSION` = `'202602'`, is written in the file; the commit's short hash, `GIT_HASH`, is given by the build (the Makefile passes `-DGIT_HASH`, with "-dirty" appended when `src/` has uncommitted changes, or "unknown" when git is missing; the file's own default is also `'unknown'`). Both are preprocessor macros (`#define`), so the file is compiled with the preprocessor (`-cpp`, `-fpp`).

**How it fits.**
- **Who calls it:** the [[main.f#(file level)|main program]], once at the start, with its own `YRECVER` (`CHARACTER*10`) and `GITHASH` (`CHARACTER*20`).
- **Outputs:** the two strings, which the main program passes to [[parmin.f#PARMIN|`PARMIN`]]. PARMIN prints the banner "Yale Rotating Evolution Code - YREC, v…" and writes a line "# YREC v… (…)" at the head of the output files (the stored models and the short and track files).

**Design.** The strings first went through a `COMMON/VERSION/`; since they are CHARACTER, "which does not belong in a COMMON block" (the comment), the main program now holds them and passes them as arguments (MHP via Claude, 10/13/26).

**For users** (from YREC's [Python Package](https://yrec.readthedocs.io/en/latest/python_package.html) page). The Fortran code's version is written `YYYYMM` (`202602`); the Python wrapper, which bundles a built executable and downloads the input tables and starting models on its first import, has versions `YYYY.MM.n` (the month not zero-padded, `n` the wrapper's own revision) and reports both this version and the git hash of the source it was built from (`yrec.__version__`, `yrec.__commit__`).

**Changed since `rp_1`.** New file (the version banner did not exist at `rp_1`): `SETVERSION` sets the version and git hash, passed as arguments since 10/13/26; `IMPLICIT NONE`.

### SETVERSION

Sets `YRECVER` to `YREC_VERSION` and `GITHASH` to `GIT_HASH`, padded with blanks to their declared lengths.
