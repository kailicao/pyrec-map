## Explanation

**Purpose.** `KURUCZ` interpolates in Kurucz's low-temperature opacity tables (1990): it returns $\kappa$, $\log\kappa$ and the derivatives $\partial\log\kappa/\partial\log\rho$ and $\partial\log\kappa/\partial\log T$ at a given $\log\rho$, $\log T$, by cubic splines (YCK's code, by the shared style with [[intpol.f#INTPOL|`INTPOL`]]).

**How it fits.**
- **Who calls it:** only [[getopac.f#GETOPAC|`GETOPAC`]], for the atmosphere and outer envelope when the run selects the Kurucz tables (`LKUR90`). It uses an alternate return (`*`): `RETURN 1` sends `GETOPAC` to its label 100, where it falls back to the interior tables. With two metallicities (`L2Z`), `GETOPAC` also calls [[kurucz2.f#KURUCZ2|`KURUCZ2`]] and interpolates linearly in $Z$.
- **Inputs:** `DL`, `TL`; in COMMON, the temperature grid `GKRZ`, the table `KRZ` (densities `RHO` for each temperature row; `NUMTM` rows) and the density-spline coefficients `INTPL2` (`CFORD`, with the start `NDS` and length `NDD` of the valid range on each row). `GKRZ` and `KRZ` are filled by [[setkrz.f#SETKRZ|`SETKRZ`]], `INTPL2` by [[ykoeff.f#YKOEFF|`YKOEFF`]].
- **Calls:** [[findex.f#FINDEX|`FINDEX`]] (grid index) and [[intpol.f#INTPOL|`INTPOL`]] (spline in $T$).
- **COMMON blocks:** `GKRZ`, `KRZ` (with `SETKRZ`, `YKOEFF`), `INTPL2` (with `YKOEFF`), `KIPM` (its own saved indices), `LUOUT`.

**The method.**
1. If not ($\log\rho \le -3$ and $\log T \le 4.1$), take the alternate return: the table is used only in that corner.
2. On up to six temperature rows around $\log T$, find the density interval containing $\log\rho$ and evaluate the stored cubic and its derivative:
$$\log\kappa_j = ((c_4\Delta + c_3)\Delta + c_2)\Delta + c_1,\qquad \left.\frac{\partial\log\kappa}{\partial\log\rho}\right|_j = (3c_4\Delta + 2c_3)\Delta + c_2,$$
with $\Delta = \log\rho - \log\rho_k$. Rows where $\log\rho$ is outside the tabulated range are skipped.
3. If three or fewer rows remain, retry with all rows; if still too few, stop.
4. If $\log T$ is outside the rows found, take the alternate return.
5. Spline both $\log\kappa_j$ and the density derivatives in $\log T$ with `INTPOL`; the spline's slope gives `QOTF`.

## Questions for the experts

1. **The hard-coded corner.** `KURUCZ` returns to `GETOPAC` unless $\log\rho \le -3$ and $\log T \le 4.1$. The limits are written into the code rather than taken from the table that was read; are they right for every Kurucz table the code may use? (`KURUCZ2` has no such test, but `GETOPAC` calls it only after `KURUCZ` has passed it, so the two agree in practice.)
2. **Comments on the derivatives.** The header says `QODF` and `QOTF` are derivatives "of O wrt D/T" and are "estimated by numerical differentiation"; the code takes analytic spline derivatives of $\log\kappa$ with respect to $\log\rho$ and $\log T$ (as the later comments say).
3. **DATA on COMMON variables.** `DATA M1,M2,M3/1,1,1/` initializes variables of the COMMON block `KIPM` inside a subroutine, which standard Fortran allows only in BLOCK DATA. `M1` and the array `OPACITY` are unused here.

### KURUCZ

Spline in $\log\rho$ on each temperature row, then in $\log T$ (above), with an alternate return outside the table's corner.
