## Explanation

**Purpose.** A helper for shape-preserving quadratic splines (D. F. McAllister and J. A. Roulier; coded by S. L. Dodd and M. Roulier). For one interval, it chooses which of four constructions ("cases") the spline needs, from the slopes at the two ends compared with the slope of the chord.

**How it fits.**
- **Inputs:** the end points $(p_1,p_2)$, $(q_1,q_2)$, the end slopes $m_1$, $m_2$, and a tolerance `EPS`.
- **Who calls it:** [[meval.f#MEVAL|MEVAL]] (itself called by [[osplin.f#OSPLIN|OSPLIN]]), which then calls [[cases.f#CASES|CASES]] with the result.
- **Output:** `NCASE`, 1 to 4.

**The method.** With the chord's slope $s = (q_2 - p_2)/(q_1 - p_1)$ ([[#L52]]):
- **Case 1:** the tangent lines at the ends meet between $p_1$ and $q_1$ (or one slope has the wrong sign and the other exceeds $(1+\epsilon)|s|$, or $s = 0$ with $m_1m_2 < 0$). When an end slope is within $\epsilon|s|$ of $s$, this test is skipped and the case is 2 or 3.
- **Case 2:** a knot at the midpoint $(p_1 + q_1)/2$: both tangents cross the midline, or both slopes have the sign opposite to $s$, or $s = 0$ with $m_1 m_2 \ge 0$.
- **Cases 3 and 4:** all three slopes have the same sign and one or both end slopes exceed about $2|s|$; case 4 puts two knots in the interval.

**Design.** "Modification by Marc Pinsonneault": if $m_1 = 0$ or $m_2 = 0$, case 2 is taken at once, to avoid a division by zero in CASES. Without it, a zero end slope would give case 1 or 2, never case 3 or 4 (the cases that divide by $m_1$, $m_2$): The modification changes only case 1 to case 2, when the other slope has the chord's sign and exceeds $|s|$ ([[#L77-L89]]). Case 2 then stays monotone as long as the other slope is at most $4|s|$ (the middle control value $w_2 = q_2 - m_2(q_1-p_1)/4$ must not pass $p_2$), and the slopes from [[slopes.f#SLOPES|SLOPES]], which OSPLIN always uses, are at most $2|s|$ (inside, the harmonic mean $2m_1m_2/(m_1+m_2)$ of the two chords; at the ends, at most twice the end chord's slope). So the modification keeps the spline monotone in every call YREC makes (settled from the code, Nov 9, 2026).

> **Question** ([[#L52]]). **Equal abscissas.** $s$ divides by $q_1 - p_1$ with no check. MEVAL's comment requires `XTAB` to be increasing ([[meval.f#L37-L38]]), and SLOPES would meet the same zero difference first, where `SAFEDIVIDE` returns 0 ([[slopes.f#L96]]). Can a caller pass a table with two equal abscissas?

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

### CHOOSE

Chooses the case (1–4) of the McAllister–Roulier shape-preserving quadratic spline for one interval, from the end slopes and the chord's slope.
