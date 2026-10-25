## Explanation

**Purpose.** `TRIDIAG_GS` solves a tridiagonal system $a_j x_{j-1} + b_j x_j + c_j x_{j+1} = e'_j$, $j = 1, \dots, n$ (the Thomas algorithm), with the matrix and right-hand side as arguments. A zero pivot stops the run, with the message "#TRIDIA:SINGULAR MATRIX".

**How it fits.**
- **Who calls it:** [[grsett.f#GRSETT|GRSETT]] (the new run of $X$ in gravitational settling, by its comment) and [[microdiff_run.f#MICRODIFF_RUN|MICRODIFF_RUN]] (the new run of Li).
- **Output:** the solution `EX`.
- **COMMON blocks:** none.

## Questions for the experts

1. **The same algorithm four times.** [[tridia.f#TRIDIA|TRIDIA]], `CTRIDI`, `GETQUA` and `TRIDIAG_GS` each code the Thomas algorithm; this one is the only general version. Could the others call it?

### TRIDIAG_GS

The Thomas algorithm for a tridiagonal system, with arrays of size 5000 as arguments.
