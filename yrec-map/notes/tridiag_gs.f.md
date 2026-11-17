## Explanation

**Purpose.** `TRIDIAG_GS` solves a tridiagonal system $`a_j x_{j-1} + b_j x_j + c_j x_{j+1} = e'_j`$, $`j = 1, \dots, n`$ (the Thomas algorithm), with the matrix and right-hand side as arguments. A zero pivot stops the run, with the message "#TRIDIA:SINGULAR MATRIX."

**How it fits.**
- **Who calls it:** [GRSETT](grsett.f.md#grsett) (the new run of $`X`$ in gravitational settling, by its comment) and [MICRODIFF_RUN](microdiff_run.f.md#microdiff_run) (the new run of Li).
- **Output:** the solution `EX`.
- **Modules:** `DIMENSIONS_MOD` (the array size `JSON`) only.

> **Question** ([lines 17–27](https://github.com/yreclab/yrec/blob/7be4133/src/tridiag_gs.f#L17-L27)). **The same algorithm four times.** [TRIDIA](tridia.f.md#tridia), [CTRIDI](ctridi.f.md#ctridi), [GETQUA](getqua.f.md#getqua), and `TRIDIAG_GS` each code the Thomas algorithm; this one is the only general version. Could the others call it?

**Changed since `rp_1`.** Declarations only: `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

### TRIDIAG_GS

The Thomas algorithm for a tridiagonal system, with arrays of size `JSON` (5000, from `DIMENSIONS_MOD`) as arguments.
