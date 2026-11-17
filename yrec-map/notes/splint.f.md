## Explanation

**Purpose.** `SPLINT` evaluates a cubic spline at one point $`x`$, from the table $`(x_i, y_i)`$ and the second derivatives $`y''_i`$ computed beforehand: by [SPLINJ](splinj.f.md#splinj), or, for the opacity routine GTPURZ, by [CSPLINE](cspline.f.md#cspline) (computed there, or tabulated by ZSULAOL). The comments say it is taken from Numerical Recipes (Press et al., p. 89) and was changed from `REAL*4`, for the opacities, to `REAL*8` (MHP, 10/02).

The header's "OUTPUT OF SPLINE ABOVE" ([lines 7–10](https://github.com/yreclab/yrec/blob/7be4133/src/splint.f#L7-L10)) is Numerical Recipes' text: Its `spline` (with end slopes) is [CSPLINE](cspline.f.md#cspline) here, while `spline.f` is an unrelated quadratic spline. The second derivatives come from [SPLINJ](splinj.f.md#splinj) in BOOLE and CALCAD ([boole.f, lines 48–51](https://github.com/yreclab/yrec/blob/7be4133/src/boole.f#L48-L51); [calcad.f, lines 347–348](https://github.com/yreclab/yrec/blob/7be4133/src/calcad.f#L347-L348)) and from CSPLINE in GTPURZ, directly ([gtpurz.f, lines 115–116](https://github.com/yreclab/yrec/blob/7be4133/src/gtpurz.f#L115-L116)) and through the `ZSDORL` that ZSULAOL stores ([gtpurz.f, lines 78–82](https://github.com/yreclab/yrec/blob/7be4133/src/gtpurz.f#L78-L82); [zsulaol.f, lines 40–44](https://github.com/yreclab/yrec/blob/7be4133/src/zsulaol.f#L40-L44)).

> **Question** ([lines 7–10](https://github.com/yreclab/yrec/blob/7be4133/src/splint.f#L7-L10)). **The comment's reference.** Should the header name both `SPLINJ` and `CSPLINE` as the routines whose output `Y2A` is?

**How it fits.**
- **Who calls it:** [BOOLE](boole.f.md#boole), [CALCAD](calcad.f.md#calcad), and the low-temperature opacity routine [GTPURZ](gtpurz.f.md#gtpurz) (GTLAOL and GTLAOL2, and the table routine SULAOL, removed since `rp_1`, were the others).
- **Outputs:** the value `Y`, and the bracketing indices `KLO`, `KHI`.
- **Modules:** `IOUNITS_MOD`, for the unit `ISHORT` of its error message.

**The method.** A bisection finds $`x_\mathrm{lo} \le x \lt{} x_\mathrm{hi}`$ (`KLO`, `KHI`). With $`h = x_\mathrm{hi} - x_\mathrm{lo}`$, $`A = (x_\mathrm{hi} - x)/h`$ and $`B = 1 - A`$:

```math
y = A\,y_\mathrm{lo} + B\,y_\mathrm{hi} + \frac{h^2}{6}\left[(A^3 - A)\,y''_\mathrm{lo} + (B^3 - B)\,y''_\mathrm{hi}\right].
```

If two abscissas coincide ($`h = 0`$) it writes an error, with the abscissa and $`x`$, to the terminal and to `ISHORT`, and stops the run (`STOP 1`). Outside the table it extrapolates the end interval's cubic, without a warning.

**Design.** `KLO` and `KHI` are arguments but are reset on entry, so a caller's previous bracket is not used as a starting guess.

**Changed since `rp_1`.** Declarations only: `/LUOUT/` to `IOUNITS_MOD`, `IMPLICIT NONE`; two callers, GTLAOL and GTLAOL2, were removed with their files.

**Changed since `a8a5950`.** The stop on two equal abscissas now gives the abscissa and $`x`$ in its message, writes it to the terminal as well as the `.short` file, and exits with status 1, the code for run-time errors, instead of a bare `STOP` (`KNOWN_ISSUES.md`, issue 38).

### SPLINT

Cubic-spline interpolation at one point (equation above), with arrays sized `N`; stops the run when two table abscissas coincide.
