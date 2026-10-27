## Explanation

**Purpose.** Solves a tridiagonal linear system by the Thomas algorithm (Numerical Recipes' `TRIDAG`, per its comment), for the new abundance of a species after rotational mixing.

**How it fits.**
- **Inputs:** `N`, and the coefficients `A`, `B`, `C` and right-hand side `D` in [[tridi_mod.f#TRIDI_MOD|`TRIDI_MOD`]], set by [[ccoeft.f#CCOEFT|CCOEFT]].
- **Who calls it:** [[mixcom.f#MIXCOM|MIXCOM]].
- **Output:** the solution `U` in `TRIDI_MOD` (`GAMA` is a work array there). The same module serves the angular-momentum problem: [[dcoeft.f#DCOEFT|DCOEFT]] fills it for [[tridia.f#TRIDIA|TRIDIA]], and GETQUA also uses it.

**The method.** For $a_j u_{j-1} + b_j u_j + c_j u_{j+1} = d_j$: forward elimination with $\beta_1 = b_1$, $\gamma_j = c_{j-1}/\beta_{j-1}$, $\beta_j = b_j - a_j\gamma_j$, $u_j = (d_j - a_j u_{j-1})/\beta_j$; then back substitution $u_j \leftarrow u_j - \gamma_{j+1}u_{j+1}$. No pivoting; a zero $\beta$ stops the run (with the message "TRIDIA: singular matrix").

**Design.** [[tridia.f#TRIDIA|TRIDIA]] is the same solver with extra bookkeeping of the change in angular momentum; this copy is for composition.

**Changed since `rp_1`.** Declarations only: `/TRIDI/` to `TRIDI_MOD`, `IMPLICIT NONE`.

## Questions for the experts

1. **Exact zero test.** Only $\beta = 0$ exactly is caught, and only from $j = 2$ ($\beta_1 = b_1$ is not tested); a tiny $\beta$ passes. The diffusion matrices from CCOEFT are diagonally dominant, so this should not arise.

### CTRIDI

Thomas algorithm for the tridiagonal system in `TRIDI_MOD`; the solution goes to `U`.
