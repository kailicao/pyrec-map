## Explanation

**Purpose.** `EQ2MOD` maps a change in specific angular momentum, computed on an equally spaced grid, back onto the model's own mass points. It is the last step of the angular momentum transport by rotational instabilities: the diffusion equation is solved on the equally spaced grid for each unstable region, and this routine applies the result to the run of $j = J/M$ in the model.

**How it fits.**
- **Who calls it:** only [[seculr.f#SECULR|SECULR]], after it has solved the diffusion equation for one unstable region (shells `IBEG` to `IEND`).
- **Inputs:** the change `DJ` and the angular momentum `EJ` before redistribution, both on the equally spaced grid; the shell masses `HS2`; the convective flags `LCZ`; the total change `SUMDJ` across the grid.
- **What it calls:** [[osplin.f#OSPLIN|OSPLIN]], a shape-preserving osculatory quadratic spline (ACM Algorithm 574).
- **Output:** the array `HJM` (specific angular momentum at each model point), updated in place.
- **Modules:** [[egrid_mod.f#EGRID_MOD|`EGRID_MOD`]] (formerly `/EGRID/`) holds the grids: `CHI` (the model points' coordinate, $\chi = \log m/\Delta_m + L/\Delta_L - \log P/\Delta_P$, where $\Delta_m$ = `HPTTOL(2)`, $\Delta_L$ = `HPTTOL(9)`$\cdot L_\mathrm{surf}$, $\Delta_P$ = `HPTTOL(11)`, as [[getgrid.f#GETGRID|GETGRID]] forms it (its comment writes $L/(L_\mathrm{tot}\Delta L)$); here `CHI(1..NMOD)` are the region's points, from `IBEG` on), `ECHI` (the equally spaced points), `NTOT`; it is filled by [[getgrid.f#GETGRID|GETGRID]] and shared with `SECULR`, `ROTGRID`, `MIXGRID`, `MIXCOM` and `CHECKJ`. [[splin_mod.f#SPLIN_MOD|`SPLIN_MOD`]] (formerly `/SPLIN/`) is scratch space for the spline, shared with `MIXCOM`, `MIXGRID` and `ROTGRID`.

**The method.**
1. If a convection zone adjoins the region's first or last shell (whether or not that shell is itself convective), the region is extended (indices `I0`, `I1`) to the far edge of that zone, the test [[rotgrid.f#ROTGRID|ROTGRID]]'s sums use.
2. The fractional change $y = \Delta j / j$ (`DJ/EJ`) is interpolated with `OSPLIN` from the equally spaced points `ECHI` to the model points `CHI`, giving `YVAL`.
3. Each shell's $j$ is multiplied by $(1 + y_i)$. Shells in the extended convective parts take the value at the nearest edge (`YVAL(1)` or `YVAL(NMOD)`).

    > **Question** ([[#L100-L119]]). **The extended convective shells.** Shells outside `IBEG..IEND` but in the same convection zone get the edge value of $y$, so their $j$, and their $\Omega$, scale by one common factor. That keeps the zone in solid-body rotation only if it already was; the code does not check it. Is that assumption safe here?

4. Conservation check. With $m_i$ the shell mass (`HS2`),
$$S_J = \sum_i j_i m_i, \qquad S_{\Delta} = \sum_i y_i\, j_i m_i .$$
If $|S_\Delta - \Delta J| > 10^{-5}|\Delta J|$, where $\Delta J$ is `SUMDJ`, every shell from `I0` to `I1` is rescaled by
$$\frac{S_J + \Delta J}{S_J + S_\Delta},$$
so that the region's total angular momentum changes by exactly $\Delta J$. When $\Delta J = 0$ (no surface loss), any mismatch triggers the rescaling, which then conserves the region's angular momentum exactly; this is what the comment asks for ("CARE IS USED HERE BECAUSE DUMDJ SHOULD BE ZERO IN MODELS WITHOUT LOSS," where `DUMDJ` is `SUMDJ`; [[#L120-L124]], [[#L131-L136]]; settled from the code, Nov 9, 2026).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

**Changed since `a8a5950`.** The region is extended into a convection zone that adjoins its end shell even when that shell is radiative, as ROTGRID's sums already took that zone into the end cell; before, the zone's share of the change went to the end shell alone.

### EQ2MOD

Interpolates $\Delta j/j$ back to the model points, applies it, and rescales the region to conserve angular momentum (equations above).
