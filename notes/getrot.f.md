## Explanation

**Purpose.** `GETROT` turns a run of specific angular momentum $j(m)$ into a rotation curve $\Omega(m)$. Radiative shells are treated one at a time; each convection zone is given its rotation law as a whole. (Its comment calls it `GETW`, an older name.)

**How it fits.**
- **Who calls it:** [[checkj.f#CHECKJ|CHECKJ]], [[crrect.f#CRRECT|CRRECT]], [[getnewenv.f#GETNEWENV|GETNEWENV]], [[getw.f#GETW|GETW]], [[hpoint.f#HPOINT|HPOINT]] and [[midmod.f#MIDMOD|MIDMOD]].
- **Inputs:** `HJM` ($j$ per shell), `LCZ` (convective flags), the structure (`HD`, `HR`, `HS`, `HS2`), `M`.
- **What it calls:** [[solid.f#SOLID|SOLID]] (for a single radiative shell) and [[wczimp.f#WCZIMP|WCZIMP]] (for a convection zone; "JNT 09/25 for 05/15 call WCZIMP instead of WCZ").
- **Outputs:** `OMEGA`, `HI` (moments of inertia of the shells), `ETA2`, `QIW`, `R0`, filled by `SOLID` and `WCZIMP`; and `HJM`, which both rewrite as $j = I\Omega/\Delta m$, so that in a convection zone, where `WCZIMP` imposes the rotation law, $j$ is redistributed.

**The method.** Scanning outward: each radiative shell is passed to `SOLID` alone; a run of convective shells is collected and passed to `WCZIMP` when the next radiative shell (or the surface) is reached (but see question 2).

## Questions for the experts

1. **A stale name.** The comment begins "GETW takes the angular momentum distribution…"; the routine is `GETROT`, and `GETW` is another routine. Update the comment?
2. **A one-shell convective surface.** If only the last shell is convective (`LCZ(M)` true, `LCZ(M-1)` false), the loop marks the start of a convection zone at `I = M` and ends without calling `WCZIMP` or `SOLID` for it: `OMEGA(M)`, `HI(M)` and the rest keep the values they had before the call. The case `I.EQ.M` is reached only when the zone began below `M`. Should a zone that starts at `M` be treated too?

### GETROT

Converts $j(m)$ to $\Omega(m)$: `SOLID` for each radiative shell, `WCZIMP` for each convection zone.
