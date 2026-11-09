## Explanation

**Purpose.** Polynomial interpolation through `N` points by Neville's algorithm (the routine `POLINT` of Numerical Recipes, by its name and form): it returns the value `Y` at `X` and an error estimate `DY`, the last correction added.

**How it fits.**
- **Who calls it:** [[alsurfp.f#ALSURFP|ALSURFP]] (the Allard model atmospheres' surface pressures) and [[fpft.f#FPFT|FPFT]] (the rotational distortion factors).
- **Modules:** `IOUNITS_MOD`, for the unit `ISHORT` of its error message.
- **Limits:** at most 20 points (the arrays are fixed at 20, "for consistency with fpft", MHP 10/02).

**The method.** Starting from the nearest tabulated point, the tableau of differences $C_{i}$, $D_{i}$ is built column by column,
$$D_i \leftarrow \frac{(x_{i+j}-x)\,(C_{i+1}-D_i)}{x_i - x_{i+j}},\qquad C_i \leftarrow \frac{(x_i-x)\,(C_{i+1}-D_i)}{x_i - x_{i+j}},$$
and the path through it that stays closest to the centre adds one correction per column to $y$.

Two equal abscissas ($|x_i - x_{i+j}| < 10^{-20}$) stop the run (`STOP 1`) with a message to the terminal and to `ISHORT` giving the two abscissas, $x$ and `N`.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

**Changed since `a8a5950`.** The stop on two equal abscissas now writes a message with the values to the terminal and to the `.short` file (the routine now uses `IOUNITS_MOD`), and exits with status 1, the code for run-time errors, instead of a bare `STOP` (`KNOWN_ISSUES.md`, issue 38). This settles former question 1 (a stop without a message), which is removed.

