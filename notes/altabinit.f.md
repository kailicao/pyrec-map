## Explanation

**Purpose.** This file checks the Allard atmosphere table that [[alfilein.f#ALFILEIN|ALFILEIN]] has just read and derives the limits that the lookup [[alsurfp.f#ALSURFP|ALSURFP]] needs: the range of $\log T_\mathrm{eff}$, and for each $T_\mathrm{eff}$ row the valid columns in $\log g$ and the allowed range of $\log g$, extrapolation included.

**How it fits.**
- **Who calls it:** [[alfilein.f#ALFILEIN|ALFILEIN]], at the end of reading.
- **What it calls:** [[alprint.f#ALPRINT|ALPRINT]], to print the table when it is bad.
- **Inputs:** `/ALATM01/` (the table).
- **Outputs:** `/ALATM02/` (`GLmin`, `GLmax`, `IGLmin`, `IGLmax`, `TEFFLmin`, `TEFFLmax`, `GLXmin`, `GLXmax`), read by ALSURFP and ALPRINT; `/ALATM05/` (`AL_TEFFLmin`, `AL_TEFFLmax`, the table's own first and last $\log T_\mathrm{eff}$), read by [[surfbc.f#SURFBC|SURFBC]] to decide when to switch away from Allard atmospheres.

**The method.** With $t_i$ the table's $\log T_\mathrm{eff}$ and $g_j$ its $\log g$ values:
1. $t_\mathrm{min} = t_1 - (t_2 - t_1)$ and $t_\mathrm{max} = t_n + (t_n - t_{n-1})$: one row's width beyond each end.
2. For each row $i$, the first and last valid columns $j_1(i)$, $j_2(i)$ (entries above $-998$).
3. The allowed range of $\log g$ in each row:
$$g_\mathrm{min}(i) = g_{j_1} - 4\,(g_{j_1+1} - g_{j_1}), \qquad g_\mathrm{max}(i) = g_{j_2} + (g_{j_2} - g_{j_2-1}),$$
and the extremes over all rows, `GLXmin` and `GLXmax`.
4. Validate: no invalid entry between $j_1$ and $j_2$ in any row, at least 4 rows, and at least 4 valid entries per row (4-point Lagrange interpolation needs them). Otherwise print the table and stop.

## Questions for the experts

1. **Four columns below.** The comments (here and in ALSURFP) say the allowed range extends one column's width beyond the table, but `GLmin` extends four widths below the lowest valid $\log g$ (`4D0*` in step 3). Which is meant? Extrapolating a 4-point Lagrange polynomial four steps out can be far off.
2. **A format mismatch.** The "less than 4 rows" message writes two strings and an integer with format `910`, `(A,I3)`, which has only one `A`. Most compilers would stop with a run-time format error at that point.
3. **Only $\log P$ is checked.** Validity is judged from `PLs` alone; `P100Ls` and `T100Ls` (used when the $\tau = 100$ option is on) are not checked for $-999$ entries.

### ALTABINIT

Derives each row's valid range in $\log g$ and the table's range in $\log T_\mathrm{eff}$ (`/ALATM02/`, `/ALATM05/`), checks the table, and stops the run (after [[alprint.f#ALPRINT|ALPRINT]]) if it is bad.
