## Explanation

**Purpose.** A helper for shape-preserving quadratic splines, from the package by D. F. McAllister and J. A. Roulier (coded by S. L. Dodd and M. Roulier, N.C. State University, per its header). Given two data points and the slopes there, it computes the knots of the quadratic spline on that interval.

**How it fits.**
- **Inputs:** the end points $(p_1, p_2)$ and $(q_1, q_2)$, the slopes $m_1$ and $m_2$ there, and `NCASE` (1 to 4), which fixes the number and place of the knots.
- **Who calls it:** [[meval.f#MEVAL|MEVAL]], which evaluates the spline.
- **Outputs:** the knots $(v_1,v_2)$, $(w_1,w_2)$, $(z_1,z_2)$, and for case 4 also $(y_1,y_2)$ and $(e_1,e_2)$.
- No COMMON blocks.

**The method.** Each case builds the spline from straight segments of the given slopes through the end points. In case 1, for example, the two tangent lines meet at
$$z_1 = \frac{p_2 - q_2 + m_2 q_1 - m_1 p_1}{m_2 - m_1},$$
and the knots are the midpoints $v = \tfrac12(p + z)$, $w = \tfrac12(z + q)$. Cases 2–4 place the middle knot at the interval's midpoint or at auxiliary points ($c_1 = p_1 + (q_2 - p_2)/m_1$ and $d_1 = q_1 + (p_2 - q_2)/m_2$), as the slopes require.

The divisions are safe for the cases [[choose.f#CHOOSE|CHOOSE]] picks, as long as $q_1 \ne p_1$: case 1 divides by $m_2 - m_1$ ([[#L55]]), and CHOOSE picks it only when the two slopes differ (opposite signs, or the same sign with $|s|$ strictly between $|m_1|$ and $|m_2|$, [[choose.f#L59-L61]], [[choose.f#L82-L89]], [[choose.f#L131-L143]]); cases 3 and 4 divide by $m_1$ and $m_2$ ([[#L74-L75]]), which CHOOSE rules out as zero ([[choose.f#L57]]), by $h_1 - p_1 = 2(q_2 - p_2)/m_1$, nonzero since $s \ne 0$ there, and in case 3 by $\bar m_2 - \bar m_1 = (m_2 - m_1)/2$ ([[#L84]]), nonzero since one slope exceeds $2|s|$ and the other does not exceed $(2-\epsilon)|s|$ (settled from the code, Nov 9, 2026).

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

### CASES

Knots of a shape-preserving quadratic spline on one interval (McAllister and Roulier), for the four cases of their method.
