## Explanation

**Purpose.** `MHDST1` reads one MHD table file (unformatted): a ZAMS table (`IDX` = 0: a lower and an upper part) or a centre table (`IDX` = 1: three tables at $X$, $X - \delta X$, $X + \delta X$, from which it also computes the derivatives with respect to $X$ of four variables).

**How it fits.** Called only by [[mhdst.f#MHDST|`MHDST`]], with the target arrays as arguments. Calls [[rabu.f#RABU|`RABU`]] (reads the composition: atomic weights, abundances, mass fractions, mean weight) and [[rtab.f#RTAB|`RTAB`]] (reads one table). COMMON: `CCOUT2` only (unused).

**The method.**
1. For each of the 1 (ZAMS) or 3 (centre) parts: read the header (number of variables, `IDX`, the shift code 0, −1, +1, and $\delta X$ = `DDX`), check it (stop if wrong), read the composition and the grid sizes, then the tables.
2. For a centre table: check that the three compositions differ by $\mp\delta X$ in $X$ and $\pm\delta X$ in $Y$ (within 5 % of $\delta X$) and agree in the metals, and that the temperature grids are identical; then copy the central table and add, by centred differences,
$$v_{21..24} = \frac{v(X+\delta X) - v(X-\delta X)}{2\,\delta X}$$
for $\log P$, $\log U$, $\nabla_\mathrm{ad}$ and $\log c_P$ (variables 2, 3, 8, 9, by its comment), with $v_{25}$ a placeholder (8888844444).

**KC's changes.** 2025-05-30: DO loops with shared or non-`CONTINUE` terminations rewritten (no change in behaviour intended).

## Questions for the experts

1. **Silent stops.** Every check ends in a bare `STOP` without a message (the formats explaining them are commented out), so a wrong or truncated table file stops the run with no hint of the cause. Restore the messages?
2. **Exact comparison of temperatures.** The three centre tables' temperature grids must be exactly equal (`.NE.` on reals); fine for tables written by the same program, fragile otherwise.

### MHDST1

Reads one MHD table file; for centre tables, checks the three compositions and forms the $X$-derivatives (above).
