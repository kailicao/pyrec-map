## Explanation

**Purpose.** This file integrates tabulated data with Boole's rule (5-point Newton–Cotes), after interpolating the data onto an even grid with a cubic spline. Its only use is the acoustic depth in [CALCAD](calcad.f.md#calcad), $`\int dr / c_s`$.

**How it fits.**
- **Inputs:** the arguments `X(N)` and `Y(N)`, and `NN`, the number of points of the even grid (it should be $`1 + 4p`$).
- **Who calls it:** [CALCAD](calcad.f.md#calcad), twice: over the whole star and from the base of the convection zone to the surface.
- **What it calls:** [SPLINJ](splinj.f.md#splinj) (the spline's second derivatives) and [SPLINT](splint.f.md#splint) (spline evaluation).
- **Output:** the integral in `S`.

**The method.**
1. Rescale: $`x' = 10^{-11} x`$, $`y' = 10^{7} y`$ (`SCALEX`, `SCALEY`; the comment says this brings the radius and the sound-speed vector to values near 1).

    > **Question** ([lines 34–35](https://github.com/yreclab/yrec/blob/7be4133/src/boole.f#L34-L35); [lines 41–45](https://github.com/yreclab/yrec/blob/7be4133/src/boole.f#L41-L45); [line 65](https://github.com/yreclab/yrec/blob/7be4133/src/boole.f#L65)). **Fixed scales.** The factors $`10^{-11}`$ and $`10^{7}`$ suit radii in $`\mathrm{cm}`$ and $`1/c_s`$ in $`\mathrm{s\,cm^{-1}}`$ of a star like the Sun. Since the result is scaled back, they only affect rounding; are they needed?

2. Fit a natural cubic spline to $`(x', y')`$ and evaluate it at `NN` evenly spaced points $`x'_k = x'_1 + (k-1)h`$, $`h = (x'_N - x'_1)/(NN-1)`$.
3. Apply Boole's rule to each group of 5 points:
   
   $$\displaystyle \int\_{x\_0}^{x\_4} f\\,dx \approx \frac{2h}{45}\left(7f\_0 + 32f\_1 + 12f\_2 + 32f\_3 + 7f\_4\right),$$
   
   over $`p = \lfloor (NN-1)/4 \rfloor`$ groups. If $`NN - 1`$ is not a multiple of 4, the last points would be left out without a message; CALCAD, the only caller, rounds $`NN - 1`$ up to a multiple of 4 in both calls ([calcad.f, lines 310–316](https://github.com/yreclab/yrec/blob/7be4133/src/calcad.f#L310-L316), [calcad.f, lines 375–381](https://github.com/yreclab/yrec/blob/7be4133/src/calcad.f#L375-L381)), except for a profile of at most 3 points ([calcad.f, suspected bug 7](calcad.f.md#b7)) (settled from the code, Nov 9, 2026).
4. Undo the scaling: $`S = S'/(10^{-11}\cdot 10^{7})`$.

The local arrays `XI`, `YI`, `XD`, `YD`, `D2X` have sizes set by the arguments `N` and `NN` (automatic arrays, standard in Fortran 90), and `H` and `S` are arrays of length 1 used as scalars ([lines 36–37](https://github.com/yreclab/yrec/blob/7be4133/src/boole.f#L36-L37)).

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE` with explicit declarations; `SCALEX` is now the double-precision `1D-11` (it was the single-precision `1e-11`, about $`4\times10^{-9}`$ off in relative terms), which changes only rounding, since the result is scaled back; the header comment now names `SPLINJ` and `SPLINT` (question 4 of `rp_1`, the header naming "numerical recipes SPLINE," is settled and removed).

### BOOLE

Spline-resamples $`(X, Y)`$ onto `NN` even points and integrates with Boole's rule; returns $`\int Y\,dX`$ in `S`.
