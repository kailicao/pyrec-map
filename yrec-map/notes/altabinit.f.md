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

1. **(never occurred)** **A format mismatch stops the run with a run-time error.** ([[#L119-L124]]) The "less than 4 rows" message writes two strings and an integer with format `910`, `(A,I3)`, which has only one `A`: the second string meets `I3`. With gfortran this is a run-time error ("Expected INTEGER for item 2"), so a table with fewer than 4 rows stops the run there, without the message, ALPRINT's table, and the exit status 3 meant for input errors. Only for a bad table.

    **A possible fix:**

    ```diff
    --- a/src/altabinit.f
    +++ b/src/altabinit.f
    @@ -120,7 +120,9 @@
              LBadTable = .true.
              write(ISHORT,910) 'ALTABINIT: Bad input Allard Table: ',
          x      'Less than 4 rows: nTeff = ',nTeff
    - 910         format(A,I3)
    +C 11/09/26 KC via Claude
    +C code changed to give format 910 the two strings it is written with.
    + 910         format(2A,I3)
           endif
           do i = 1, nTeff
              j1 = iGLmin(i)
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The test ran once, in `testsuite/Test_solarGS98_allard`, the only one of 34 runs (26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones; one of these, with `FCORE` = 1.0, stopped in its first second) with the Allard table, with 62 rows and 6 columns; the message was never written. Reading the code, a requested `ALATM_FeH` that is not in the table (for example $-0.25$ with `Nextgen2.all`, whose values run from 0 to $-4$) leaves no row and reaches it, after step 1 has read `TEFFLs(0)` and `TEFFLs(-1)` ([[#L63-L64]]); not run. No fix was run. Intent: none found.

2. **(never occurred)** **A row with no valid entry is read out of bounds.** ([[#L68-L84]]; [[#L92-L98]]) A row whose `PLs` are all at $-999$ never sets `iGLmin(i)`, `iGLmax(i)`, which keep 0 (or an earlier table's values); step 3 then reads `GLs(j1+1)` and `GLs(j2-1)`, `GLs(-1)` for an unset row, and step 4 (a) reads `PLs(i,0)`, before step 4 (b) rejects the row. A row with one valid entry, in the first column, reads `GLs(0)`. The table is rejected either way; the reads come first. Only for a bad table.

    **A possible fix:**

    ```diff
    --- a/src/altabinit.f
    +++ b/src/altabinit.f
    @@ -66,6 +66,12 @@
     C 2. For each row in GL, find the index of the smallest element (iGLmin) and the index of the
     C    largest element (iGLmax). There is one pair of these for each TEFFL.
           do i = 1, nTeff
    +C 11/09/26 KC via Claude
    +C code changed to give a row with no valid entry an empty range
    +C (iGLmin = 1, iGLmax = 0), which steps 3 and 4 (a) skip and step
    +C 4 (b) rejects.
    +         iGLmin(i) = 1
    +         iGLmax(i) = 0
              do j = 1, nGL
                 if(PLs(i,j) .gt. -998D0) then
                    iGLmin(i) = j
    @@ -92,6 +98,10 @@
           do i = 1, nTeff
              j1 = iGLmin(i)
              j2 = iGLmax(i)
    +C 11/09/26 KC via Claude
    +C code changed to skip a row with fewer than two valid entries, whose
    +C range in GL cannot be set; step 4 (b) rejects it.
    +         if(j2 .le. j1) cycle
              GLmin(i) = GLs(j1) - 4D0*(GLs(j1+1) - GLs(j1))
              if(GLmin(i) .lt. GLXmin) GLXmin = GLmin(i)
              GLmax(i) = GLs(j2) + (GLs(j2) - GLs(j2-1))
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Step 3 ran for each of the 62 rows of the table in `testsuite/Test_solarGS98_allard`, and no row had fewer than two valid entries. Every row of the three tables in `input/atmos/allard/` (`Nextgen2.all`, `AMES-Cond2.all`, and `AMES-Dusty2.all`, every [Fe/H]) holds at least four, read from the files; only a bad table, or the request of [[alfilein.f#b1]], would reach it, and neither was run. No fix was run. Intent: none found.

3. **(not reached)** **An empty table is read out of bounds.** ([[#L61-L64]]; [[#L119-L124]]; [[alfilein.f#L209-L213]]) When no record of the file has the requested `ALATM_FeH` and `ALATM_Alpha`, [[alfilein.f#ALFILEIN|ALFILEIN]] leaves `nTeff` at 0 ([[alfilein.f#L197]]) and calls ALTABINIT, whose step 1 reads `TEFFLs(0)` and `TEFFLs(-1)`, outside `TEFFLs(NTA)`, and `TEFFLs(1)` and `TEFFLs(2)`, never set for this table; with one matching row, it reads `TEFFLs(0)` and an unset `TEFFLs(2)`. Step 4 (b) rejects the table only later ([[#L119]]), and the run stops either way (under gfortran, through the format error of [[#b1]], which writes two strings with a format for one); nothing computed from the reads is used. Only with `KTTAU` = 4 and an [Fe/H] or $\alpha$ the file does not hold (no case sets `ALATM_FeH` or `ALATM_Alpha`; both default to 0, which every table holds).

    **A possible fix:**

    ```diff
    --- a/src/altabinit.f
    +++ b/src/altabinit.f
    @@ -54,6 +54,14 @@
     C it also retires the hazard behind the earlier alfilein.f fix, where a
     C mis-indented EXTERNAL was absorbed into this declaration and renamed
     C DUMMY4.
    +C 11/10/26 KC via Claude
    +C code changed to stop, before the range is set from TEFFLs, when the
    +C file holds fewer than 4 rows for the requested [Fe/H] and alpha.
    +      if(nTeff .lt. 4) then
    +         write(ISHORT,'(2A,I3)') 'ALTABINIT: Bad input Allard Table: ',
    +     x      'Less than 4 rows: nTeff = ',nTeff
    +         goto 9999
    +      endif
     
     C 1. Find the minimum (TEFFLmin) and maximum (TEFFLmax) permissable values of TEFFL. These are
     C    one row's width below the bottom and above the top of the table. Because the first level
    ```

    **Checked by running YREC** (Nov 10, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): ALTABINIT ran once in `testsuite/Test_solarGS98_allard`, with 62 rows and 6 columns, so the reads stayed inside the table: not reached. What would reach it: with `KTTAU` = 4, an `ALATM_FeH` absent from the file (with `Nextgen2.all`, for example $-0.3$ or $+0.3$; with `AMES-Dusty2.all`, anything but 0) or an `ALATM_Alpha` other than 0 (not run). The fix was not run, since the condition did not hold. Intent: none found.

### ALTABINIT

Derives each row's valid range in $\log g$ and the table's range in $\log T_\mathrm{eff}$ (`ALATM02_MOD`, `ALATM05_MOD`), checks the table, and stops the run (after [[alprint.f#ALPRINT|ALPRINT]]) if it is bad.
