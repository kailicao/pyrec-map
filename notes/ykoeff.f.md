## Explanation

**Purpose.** `YKOEFF` (YCK 3/91) prepares the Kurucz opacity tables for interpolation in density: for each temperature, it fits a natural cubic spline to $\log\kappa$ as a function of the density variable (`RHO`), with [[ysplin.f#YSPLIN|YSPLIN]], and stores the four coefficients per interval. With `L2Z`, it does the same for the second table, at another $Z$ (DBG 12/95).

**How it fits.**
- **Inputs:** COMMON `KRZ` (`OPACITY`, `RHO`, `NUMTM` temperatures; and `KRZ2`), filled by [[setkrz.f#SETKRZ|SETKRZ]].
- **Who calls it:** only [[setkrz.f#SETKRZ|SETKRZ]], after reading the tables.
- **What it calls:** [[ysplin.f#YSPLIN|YSPLIN]].
- **Outputs:** COMMON `INTPL2` (`CFORD`, the coefficients, 4 per density point; `NDS`, the first valid density; `NDD`, the number of valid densities) and `INTPL22`, read by [[kurucz.f#KURUCZ|KURUCZ]] and [[kurucz2.f#KURUCZ2|KURUCZ2]].

**The method.** Entries with $\kappa \le 0$ are missing and skipped. The run stops if the first valid density is not the first of the table, or if fewer than 25 remain ("ERROR KURUCZ OPACITY NDS/NDD").

## Questions for the experts

1. **Short error messages.** The second table's stops print only `' NDS2'` and `' NDD2'`. A message naming the table and the temperature would help.

### YKOEFF

Spline coefficients of $\log\kappa$ in density for each temperature of the Kurucz tables (and the second-$Z$ table).
