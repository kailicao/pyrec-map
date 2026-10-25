## Explanation

**Purpose.** Polynomial interpolation through `N` points by Neville's algorithm (the routine `POLINT` of Numerical Recipes, by its name and form): it returns the value `Y` at `X` and an error estimate `DY`, the last correction added.

**How it fits.**
- **Who calls it:** [[alsurfp.f#ALSURFP|ALSURFP]] (the Allard model atmospheres' surface pressures) and [[fpft.f#FPFT|FPFT]] (the rotational distortion factors).
- **Limits:** at most 20 points (the arrays are fixed at 20, "for consistency with fpft", MHP 10/02).

**The method.** Starting from the nearest tabulated point, the tableau of differences $C_{i}$, $D_{i}$ is built column by column,
$$D_i \leftarrow \frac{(x_{i+j}-x)\,(C_{i+1}-D_i)}{x_i - x_{i+j}},\qquad C_i \leftarrow \frac{(x_i-x)\,(C_{i+1}-D_i)}{x_i - x_{i+j}},$$
and the path through it that stays closest to the centre adds one correction per column to $y$.

## Questions for the experts

1. **A silent stop.** Two equal abscissas stop the run (`STOP`) without a message, which is hard to trace in a long run. Add a message?
