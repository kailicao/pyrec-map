## Explanation

**Purpose.** `YLLOC` prepares the OPAL92 opacity tables for interpolation in density ("spline coeff.", in [[yllo3d.f|yllo3d.f]]'s list): for each composition and temperature, it fits a natural cubic spline to $\log\kappa$ against $\log R$ with [[ysplin.f#YSPLIN|YSPLIN]] and stores the coefficients. With `L2Z` it does the same for the second table at another $Z$ (DBG 5/94).

**How it fits.**
- **Inputs:** COMMON `LLOT` (`OPACITY`, $\log\kappa$, with `NUMXM` compositions and `NUMTM` temperatures) and `GLLOT` (the grid of $\log R$, `GRHOT3`), and their second-table versions, filled by [[setllo.f#SETLLO|SETLLO]].
- **Who calls it:** only [[setllo.f#SETLLO|SETLLO]].
- **What it calls:** [[ysplin.f#YSPLIN|YSPLIN]].
- **Outputs:** COMMON `LINTPL` (`CFORD`, `NDS`, `NDD`) and `LINTPL2`, read by [[yllo2d.f#YLLO2D|YLLO2D]], [[yllo2d2.f#YLLO2D2|YLLO2D2]] and [[ll4th.f#LL4TH|LL4TH]].

**The method.** Entries at or below $-9.999$ mark missing values and are skipped; the run stops if the first valid density is not the table's first ("CHECK NDS"). Rows with one valid point or none get no spline.

## Questions for the experts

1. **Few points.** A row with 2 or 3 valid densities is passed to `YSPLIN`, which needs at least 4 (see [[ysplin.f|ysplin.f]]). Can such rows occur at the edges of the table?

### YLLOC

Spline coefficients of $\log\kappa$ in $\log R$ for each composition and temperature of the OPAL92 tables (and the second-$Z$ table).
