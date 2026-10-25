## Explanation

**Purpose.** `TRIDIA` solves the tridiagonal system of the implicit angular-momentum diffusion step (the Thomas algorithm), and returns the change of angular momentum at each point.

**How it fits.**
- **Inputs:** COMMON `TRIDI`, filled by [[dcoeft.f#DCOEFT|DCOEFT]] just before the call: the three diagonals `A`, `B`, `C`, the right-hand side `D` (by `DCOEFT`'s comment, the angular velocities at the start of the time step, the outermost one already reduced by the wind), and `GAMA(N)`, the wind term at the surface. The argument `EI` holds the points' moments of inertia (by `SECULR`'s use, probably).
- **Who calls it:** only [[seculr.f#SECULR|SECULR]].
- **Outputs:** `U` in `TRIDI`, the angular velocities at the end of the step; `DJ`, the change of angular momentum at each point; and `SUMDJ`, their sum. `SECULR` passes `DJ` to [[eq2mod.f#EQ2MOD|EQ2MOD]] to return to the model's grid.
- **COMMON blocks:** `TRIDI`, shared with `DCOEFT`, [[ccoeft.f#CCOEFT|CCOEFT]], [[ctridi.f#CTRIDI|CTRIDI]], [[getqua.f#GETQUA|GETQUA]] and [[mixcom.f#MIXCOM|MIXCOM]].

**The method.** Forward elimination and back substitution for $a_j u_{j-1} + b_j u_j + c_j u_{j+1} = d_j$; then
$$\Delta J_j = (\Omega_j^\mathrm{new} - \Omega_j^\mathrm{old})\,I_j,$$
with, at the surface, the wind term added: $\Delta J_N = \gamma_N + (\Omega_N^\mathrm{new} - \Omega_N^\mathrm{old})\,I_N$. A zero pivot stops the run ("#TRIDIA:SINGULAR MATRIX").

**KC's changes.** The unused argument `EJ` was removed (2025-05-31).

## Questions for the experts

1. **A no-op.** `FJ = 1 + (U(N)-U0(N))/U0(N)` and `U(N) = U0(N)*FJ` give back `U(N)` unchanged (up to rounding). Was something else meant?
2. **The wind term through `GAMA`.** The surface's wind loss reaches `TRIDIA` in `GAMA(N)`, the same array the elimination uses for its work, so it must be read first (as it is). A separate variable would be clearer.

### TRIDIA

Thomas algorithm for the implicit angular-momentum diffusion, returning each point's change of angular momentum and their sum.
