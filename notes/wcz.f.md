## Explanation

**Purpose.** `WCZ` sets the rotation of a convection zone (shells `ISTART`–`IEND`) while conserving its total angular momentum, by a law chosen with `WALPCZ` (COMMON `ROT`). It is no longer called: [[getrot.f#GETROT|GETROT]] and [[getw.f#GETW|GETW]] call [[wczimp.f#WCZIMP|WCZIMP]] instead ("JNT 09/25 for 05/15 call WCZIMP instead of WCZ"), which keeps these laws and adds others.

**How it fits.** Nobody calls it. It calls [[solid.f#SOLID|SOLID]]. COMMON blocks: `ROT` (`WALPCZ`) and `CONST1`.

**The method.** With $m_j$ = `HS2`, $j_j$ = `HJM`, $I_j$ = `HI` and $J = \sum m_j j_j$:
- **Solid body** if `WALPCZ` ≥ 0, or if the zone is not the surface one (`IEND < M`, JNT 2015/05/07): `SOLID` on the whole zone.
- **Constant specific angular momentum** if `WALPCZ` ≤ −2: $j = J/\sum m_j$ in every shell, then `SOLID` on each shell alone.
- **A power law** otherwise: $\Omega_j = \Omega_0\,r_j^{\alpha}$ with $\alpha$ = `WALPCZ` and
  $$\Omega_0 = \frac{J}{\sum_j r_j^{\alpha}\,I_j},$$
  then $j_j = \Omega_j I_j/m_j$ and `SOLID` on each shell.

## Questions for the experts

1. **Unused.** `WCZ` is replaced by `WCZIMP`; can it be removed?
2. **Positive exponents.** The power law is described for any `WALPCZ`, but `WALPCZ` ≥ 0 gives solid-body rotation, so only $-2 < \alpha < 0$ reaches it. ([[wczimp.f#WCZIMP|WCZIMP]] tests `WALPCZ .GT. 0`, so there $\alpha = 0$ reaches the power law, which is also solid body.)

### WCZ

Rotation law for a convection zone at fixed angular momentum: solid body, constant $j$, or $\Omega \propto r^{\alpha}$. Replaced by WCZIMP.
