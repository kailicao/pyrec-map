## Explanation

**Purpose.** Rational-function extrapolation to zero step size, for the Bulirsch–Stoer integrator. The comment says it is the same as `RZEXTR` of *Numerical Recipes* (p. 566).

**How it fits.** It is called by [[bsstep.f#BSSTEP|`BSSTEP`]] (the Bulirsch–Stoer step) and twice by [[liburn.f#LIBURN|`LIBURN`]] (light-element burning, with 3 variables and up to 7 previous estimates). It uses no COMMON blocks and calls nothing. Its arguments: `IEST` (the number of this estimate), `XEST` (the independent variable of the sequence, in practice the squared substep size), `YEST` (the `NV` estimates), and the outputs `YZ` (the extrapolated values) and `DY` (their error estimates).

**The method.** Each call adds one estimate $y(x_i)$ and evaluates the next diagonal of the rational extrapolation tableau, using at most `NUSE` earlier estimates. With $f_k = x_{i-k}/x_i$ (`FX`), it computes the correction terms by the recurrence of *Numerical Recipes*:

$$b = \frac{c - v}{f_k v - c},\qquad \Delta = c\,b,\qquad c \leftarrow f_k v\,b,$$

where $v$ is the previous diagonal's entry (`D(J,K)`) and $c$ the running term; the extrapolated value is $y_i + \sum\Delta$, and the last $\Delta$ is the error estimate. When $f_k v - c = 0$, it takes $\Delta = v$.

**Design.** The tableau `D` and the saved abscissae `X` persist between calls (`SAVE`), so the routine is stateful: it assumes the calls for one step come in order, `IEST` = 1, 2, …. Each caller runs its whole sequence inside one call of its own (the loop over `I` in `BSSTEP`, over `J` in `LIBURN`), and a call with `IEST` = 1 starts the tableau afresh, so the two callers do not disturb each other. The fixed sizes are `IMAX` = 11 estimates, `NMAX` = 15 variables and `NCOL` = 7 columns, with no check of `NV` or `NUSE` against them ([[#L11-L12]]): with the `PHYSICS` namelist's `IMAX` above 11 or `NUSE` above 7, BSSTEP's calls write past `X`, `D` and `FX` ([[bsstep.f#b2]]).

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.
