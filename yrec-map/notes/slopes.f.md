## Explanation

**Purpose.** Computes the derivative at each node for the shape-preserving quadratic splines of McAllister and Roulier (coded by S. L. Dodd and M. Roulier, N.C. State University). Its comment: "the slopes provided will insure that an osculatory quadratic spline will have one additional knot between two adjacent points of interpolation. Convexity and monotonicity are preserved wherever these conditions are compatible with the data."

**How it fits.** Called by [[osplin.f#OSPLIN|`OSPLIN`]] before [[meval.f#MEVAL|`MEVAL`]] evaluates the spline (with [[search.f#SEARCH|`SEARCH`]]). It contains a second routine, [[#SAFEDIVIDE|`SAFEDIVIDE`]], added by KC. No COMMON blocks.

**The method.** At each interior node $i$, with the slopes $m_1$, $m_2$ of the chords to its two neighbors:
- if $m_1 m_2 \le 0$ (a local extremum or a flat chord), the derivative is 0;
- otherwise the chord with the larger slope is extended until it reaches the level of the far neighbor, at $\bar x$, and the derivative is the slope of the line from the node to the far neighbor's level at $\hat x$, the midpoint between $\bar x$ and the far node. For $|m_1| > |m_2|$:
  $$\bar x = x_i + \frac{y_{i+1} - y_i}{m_1},\qquad \hat x = \tfrac12(\bar x + x_{i+1}),\qquad y'_i = \frac{y_{i+1} - y_i}{\hat x - x_i}.$$

At each end node, the derivative is the slope from the midpoint of the end interval, where it takes the value of the line through the neighbor node with that node's derivative, to the end node. It is set to 0 if that would reverse the sign of the end chord, or to $2m$, twice the end chord's slope $m$, if the two chords nearest that end have opposite signs.

Two divisions go through `SAFEDIVIDE`, which returns 0 instead of dividing by zero: the slope $m_2$ in the loop ([[#L96]]) and the derivative at the last node ([[#L105]]).

> **Question** ([[#L96]]; [[#L105]]). **Where can the denominator be zero?** A zero denominator means two equal abscissae, which would make the spline ill-defined anyway; replacing the slope by 0 hides the problem, and a check in `OSPLIN` might be clearer. Which caller passes repeated $x$ values?

> **Question** ([[#L59-L61]]; [[#L93]]; [[#L116]]). **Unprotected divisions remain.** The first two chord slopes, $m_1$ in the loop, and the derivative at the first node are still plain divisions. Each difference of abscissas that the loop's $m_2$ protects is divided again, unprotected, as the next pass's $m_1$ ([[#L93]]), so a repeated abscissa still raises the exception unless it is the last pair, where [[choose.f#CHOOSE|CHOOSE]] may then divide by it ([[choose.f#L52]]). Should they be treated the same way, or should the check move to `OSPLIN`?

> **Question** ([[#L57-L61]]). **At least three points.** The routine reads `YTAB(3)` without checking `NUM` ≥ 3. Do all callers guarantee this?

**Changed since `rp_1`.** Declarations only: the array size `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE` in both routines.

### SLOPES

The derivatives at the nodes, as above. `MTAB` is declared `REAL*8` explicitly (under the implicit typing of `rp_1` its name would have made it an integer; now every name is declared).

### SAFEDIVIDE

Returns `NUMERATOR/DENOMINATOR`, or 0 when either is zero. Added by KC (2025-05-31) to avoid floating-point exceptions.
