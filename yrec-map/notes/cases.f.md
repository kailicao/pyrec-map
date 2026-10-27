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

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

## Questions for the experts

1. **Division by zero.** Case 1 divides by $m_2 - m_1$ and cases 3–4 by $m_1$ and $m_2$. The caller presumably chooses `NCASE` to avoid these; this file does not check.

### CASES

Knots of a shape-preserving quadratic spline on one interval (McAllister and Roulier), for the four cases of their method.
