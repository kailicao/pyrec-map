## Explanation

**Purpose.** This file checks the Allard atmosphere table that [[alfilein.f#ALFILEIN|ALFILEIN]] has just read and derives the limits that the lookup [[alsurfp.f#ALSURFP|ALSURFP]] needs: the range of $\log T_\mathrm{eff}$, and for each $T_\mathrm{eff}$ row the valid columns in $\log g$ and the allowed range of $\log g$, extrapolation included.

**How it fits.**
- **Who calls it:** [[alfilein.f#ALFILEIN|ALFILEIN]], at the end of reading.
- **What it calls:** [[alprint.f#ALPRINT|ALPRINT]], to print the table when it is bad.
- **Inputs:** `ALATM01_MOD` (the table).
- **Outputs:** `ALATM02_MOD` (`GLmin`, `GLmax`, `IGLmin`, `IGLmax`, `TEFFLmin`, `TEFFLmax`, `GLXmin`, `GLXmax`), read by ALSURFP and ALPRINT; `ALATM05_MOD` (`AL_TEFFLmin`, `AL_TEFFLmax`, the table's own first and last $\log T_\mathrm{eff}$), read by [[surfbc.f#SURFBC|SURFBC]] to decide when to switch away from Allard atmospheres.

**The method.** With $t_i$ the table's $\log T_\mathrm{eff}$ and $g_j$ its $\log g$ values:
1. $t_\mathrm{min} = t_1 - (t_2 - t_1)$ and $t_\mathrm{max} = t_n + (t_n - t_{n-1})$: one row's width beyond each end.
2. For each row $i$, the first and last valid columns $j_1(i)$, $j_2(i)$ (entries above $-998$).
3. The allowed range of $\log g$ in each row:
$$g_\mathrm{min}(i) = g_{j_1} - 4\,(g_{j_1+1} - g_{j_1}), \qquad g_\mathrm{max}(i) = g_{j_2} + (g_{j_2} - g_{j_2-1}),$$
and the extremes over all rows, `GLXmin` and `GLXmax`.

    > **Question** ([[#L86-L95]]). **Four columns below.** The comments (here and in ALSURFP, [[alsurfp.f#L13-L16]]) say the allowed range extends one column's width beyond the table, but `GLmin` extends four widths below the lowest valid $\log g$ (`4D0*` in step 3). Which is meant? Extrapolating a 4-point Lagrange polynomial four steps out can be far off.

4. Validate: no invalid entry between $j_1$ and $j_2$ in any row, at least 4 rows, and at least 4 valid entries per row (4-point Lagrange interpolation needs them). Otherwise print the table and stop. Only `PLs` is checked, which is enough: [[alfilein.f#ALFILEIN|ALFILEIN]] fills `P100Ls` and `T100Ls` from the same record as `PLs` ([[alfilein.f#L334-L337]]), and refuses an old-format file, which has no $\tau = 100$ values, when `LALTPTau100` asks for them ([[alfilein.f#L156-L164]]) (settled from the code, Nov 9, 2026).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/ALATM01/`, `/ALATM02/`, `/ALATM05/`, `/LUOUT/` to `IOUNITS_MOD`; the unused `/ALATM03/` and `/ALATM04/` dropped, though a stray declaration of `LALTPTau100` remains, unused? ([[#L41]])), `IMPLICIT NONE`.

**Changed since `a8a5950`.** The stop on a bad table now exits with status 3, the code for input errors, instead of a bare `STOP` (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(c)** **A format mismatch stops the run with a run-time error.** ([[#L119-L124]]) The "less than 4 rows" message writes two strings and an integer with format `910`, `(A,I3)`, which has only one `A`: the second string meets `I3`. With gfortran this is a run-time error ("Expected INTEGER for item 2"), so a table with fewer than 4 rows stops the run there, without the message, ALPRINT's table, and the exit status 3 meant for input errors. Only for a bad table. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to give format 910 the two strings it is written with.
     910         format(2A,I3)
    ```

2. **(d)** **A row with no valid entry is read out of bounds.** ([[#L68-L84]]; [[#L92-L98]]) A row whose `PLs` are all at $-999$ never sets `iGLmin(i)`, `iGLmax(i)`, which keep 0 (or an earlier table's values); step 3 then reads `GLs(j1+1)` and `GLs(j2-1)`, `GLs(-1)` for an unset row, and step 4 (a) reads `PLs(i,0)`, before step 4 (b) rejects the row. A row with one valid entry, in the first column, reads `GLs(0)`. The table is rejected either way; the reads come first. Only for a bad table. Read from the code, not run. **A possible fix:**

    ```fortran
          do i = 1, nTeff
    C 11/09/26 KC via Claude
    C code changed to give a row with no valid entry an empty range
    C (iGLmin = 1, iGLmax = 0), which steps 3 and 4 (a) skip and step
    C 4 (b) rejects.
             iGLmin(i) = 1
             iGLmax(i) = 0
             do j = 1, nGL
    ...
          do i = 1, nTeff
             j1 = iGLmin(i)
             j2 = iGLmax(i)
    C 11/09/26 KC via Claude
    C code changed to skip a row with fewer than two valid entries, whose
    C range in GL cannot be set; step 4 (b) rejects it.
             if(j2 .le. j1) cycle
    ...
    ```

### ALTABINIT

Derives each row's valid range in $\log g$ and the table's range in $\log T_\mathrm{eff}$ (`ALATM02_MOD`, `ALATM05_MOD`), checks the table, and stops the run (after [[alprint.f#ALPRINT|ALPRINT]]) if it is bad.
