## Explanation

**Purpose.** `WCZIMP` sets the rotation of a convection zone (shells `ISTART`–`IEND`) at fixed total angular momentum, as [[wcz.f|wcz.f]] did, and adds options to impose a rotation profile on the radiative interior below the surface convection zone (JNT, 2015/05/14, copied into this code 2025/09/03–04). `IMPJMOD` ("impose J model", [[parmin.f#PARMIN|PARMIN]]'s comment) chooses: 0, no effect; 1, solid-body rotation; 2, a solid-body core decoupled from the surface convection zone; 3, a solid-body core coupled to it.

**How it fits.**
- **Who calls it:** [[getrot.f#GETROT|GETROT]] and [[getw.f#GETW|GETW]] (in place of `WCZ` since 09/25).
- **What it calls:** [[solid.f#SOLID|SOLID]], for the zone, single shells, or the interior.
- **Inputs and outputs:** the arguments, as in [[solid.f|solid.f]]: `HJM`, `OMEGA`, `HI`, `QIW`, `ETA2`, `R0` are updated.
- **COMMON blocks:** `SBROT` (`LSOLID`, `IMPJMOD`, set by `PARMIN`; shared with `GETW`, `MIDMOD`, `SECULR`), `ROT` (`WALPCZ`), `CONST1`.

**The method.** With $m_j$ = `HS2`, $j_j$ = `HJM`, $I_j$ = `HI`, $\alpha$ = `WALPCZ`, $r_j = 10^{\texttt{HR}(j)}$:
- **Solid body** for the zone if $\alpha > 0$, `LSOLID`, `IMPJMOD = 1`, or the zone is not the surface one (`IEND < M`).
- **`IMPJMOD = 2`:** the zone follows $\Omega_j = \Omega_0 r_j^{\alpha}$ with $\Omega_0 = \sum_\mathrm{cz} m_j j_j / \sum_\mathrm{cz} r_j^{\alpha} I_j$; the interior (shells 1 to `ISTART-1`) is then made a solid body on its own, keeping its own angular momentum.
- **`IMPJMOD = 3`:** the interior and the zone share one angular momentum budget; the interior rotates at the rate of the zone's base:
  $$\Omega_0 = \frac{\sum_{j \le N} m_j j_j}{r_\mathrm{s}^{\alpha}\sum_{j \le \mathrm{s}} I_j + \sum_{\mathrm{s} < j \le N} r_j^{\alpha} I_j},$$
  with s = `ISTART` and $N$ = `IEND`; then $\Omega_j = \Omega_0 r_j^{\alpha}$ in the zone, $\Omega_j = \Omega_\mathrm{s}$ below it.
- **Constant specific angular momentum** if $\alpha \le -2$ (and `IMPJMOD = 0`), as in `WCZ`.
- **Otherwise the power law** for the zone alone, as in `WCZ`.
After each assignment, `SOLID` is called on single shells to make $\Omega$, $I$ and $j$ consistent.

## Questions for the experts

1. **The interior's moments of inertia.** In `IMPJMOD = 2` and `3`, the interior's $I_j$ are those in `HI` on entry (from the previous rotation), and only the final `SOLID` call updates them. Is one pass enough, or should the budget be iterated?
2. **`IMPJMOD = 3` and `SOLID`.** After the interior is set to $\Omega_\mathrm{s}$, `SOLID` is called on shells 1 to `ISTART-1`, which conserves their total angular momentum and may change $\Omega$ again. Does the interior stay at the base's rate?
3. **Dates in the comments.** The header says "copy of 2025/05/14", the next comments "2015/05/14"; `PARMIN` says "05/15". Which is the original date?
4. **$\alpha = 0$.** `WALPCZ = 0` (with `IMPJMOD = 0`) reaches the power-law branch, while [[wcz.f#WCZ|WCZ]] treated it as solid body; the result is the same rotation, computed shell by shell.

### WCZIMP

Rotation of a convection zone at fixed angular momentum (solid body, constant $j$, $\Omega \propto r^{\alpha}$), with options to impose solid-body rotation on the interior, decoupled from or coupled to the surface zone (`IMPJMOD`).
