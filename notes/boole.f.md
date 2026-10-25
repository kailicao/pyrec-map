## Explanation

**Purpose.** This file integrates tabulated data with Boole's rule (5-point Newton–Cotes), after interpolating the data onto an even grid with a cubic spline. Its only use is the acoustic depth in [[calcad.f#CALCAD|CALCAD]], $\int dr / c_s$.

**How it fits.**
- **Inputs:** the arguments `X(N)` and `Y(N)`, and `NN`, the number of points of the even grid (it should be $1 + 4p$).
- **Who calls it:** [[calcad.f#CALCAD|CALCAD]], twice: over the whole star and from the base of the convection zone to the surface.
- **What it calls:** [[splinj.f#SPLINJ|SPLINJ]] (the spline's second derivatives) and [[splint.f#SPLINT|SPLINT]] (spline evaluation).
- **Output:** the integral in `S`.

**The method.**
1. Rescale: $x' = 10^{-11} x$, $y' = 10^{7} y$ (`SCALEX`, `SCALEY`; the comment says this brings the radius and the sound-speed vector to values near 1).
2. Fit a natural cubic spline to $(x', y')$ and evaluate it at `NN` evenly spaced points $x'_k = x'_1 + (k-1)h$, $h = (x'_N - x'_1)/(NN-1)$.
3. Apply Boole's rule to each group of 5 points:
$$\int_{x_0}^{x_4} f\,dx \approx \frac{2h}{45}\left(7f_0 + 32f_1 + 12f_2 + 32f_3 + 7f_4\right),$$
over $p = \lfloor (NN-1)/4 \rfloor$ groups.
4. Undo the scaling: $S = S'/(10^{-11}\cdot 10^{7})$.

## Questions for the experts

1. **Leftover points.** If $NN - 1$ is not a multiple of 4, the last points are silently left out. CALCAD always passes a valid `NN`, but nothing checks it here.
2. **Fixed scales.** The factors $10^{-11}$ and $10^{7}$ suit radii in cm and $1/c_s$ in s cm$^{-1}$ of a star like the Sun. Since the result is scaled back, they only affect rounding; are they needed?
3. **Fortran 77.** The local arrays `XI`, `YI`, `XD`, `YD`, `D2X` have sizes set by arguments (automatic arrays), and `H` and `S` are arrays of length 1 used as scalars. These need a Fortran 90 compiler; worth tidying in the overhaul.
4. **The header.** It names "numerical recipes SPLINE (renamed splinnr)", but the code calls `SPLINJ`.

### BOOLE

Spline-resamples $(X, Y)$ onto `NN` even points and integrates with Boole's rule; returns $\int Y\,dX$ in `S`.
