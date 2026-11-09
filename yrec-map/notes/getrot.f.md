## Explanation

**Purpose.** `GETROT` turns a run of specific angular momentum $j(m)$ into a rotation curve $\Omega(m)$. Radiative shells are treated one at a time; each convection zone is given its rotation law as a whole. (Its comment calls it `GETW`, an older name.)

> **Question** ([[#L21-L23]]). **A stale name.** The comment begins "GETW takes the angular momentum distribution…"; the routine is `GETROT`, and `GETW` is another routine. Should the comment name `GETROT`?

**How it fits.**
- **Who calls it:** [[checkj.f#CHECKJ|CHECKJ]], [[crrect.f#CRRECT|CRRECT]], [[getnewenv.f#GETNEWENV|GETNEWENV]], [[getw.f#GETW|GETW]], [[hpoint.f#HPOINT|HPOINT]] and [[midmod.f#MIDMOD|MIDMOD]].
- **Inputs:** `HJM` ($j$ per shell), `LCZ` (convective flags), the structure (`HD`, `HR`, `HS`, `HS2`), `M`.
- **What it calls:** [[solid.f#SOLID|SOLID]] (for a single radiative shell) and [[wczimp.f#WCZIMP|WCZIMP]] (for a convection zone; "JNT 09/25 for 05/15 call WCZIMP instead of WCZ").
- **Outputs:** `OMEGA`, `HI` (moments of inertia of the shells), `ETA2`, `QIW`, `R0`, filled by `SOLID` and `WCZIMP`; and `HJM`, which both rewrite as $j = I\Omega/\Delta m$, so that in a convection zone, where `WCZIMP` imposes the rotation law, $j$ is redistributed.

**The method.** Scanning outward: each radiative shell is passed to `SOLID` alone, which finds the $\Omega$ for which $\Omega\,I(\Omega) = j\,\Delta m$, iterating SHAPE and MOMI, since the shell's moment of inertia depends on $\Omega$ through its distortion; a run of convective shells is collected and passed to `WCZIMP` when the next radiative shell (or the surface) is reached (but see [[#b1]]).

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`, and the array size `JSON` from `DIMENSIONS_MOD`.

## Bugs, by priority

1. **(a)** **A one-shell convective surface is never treated.** ([[#L33-L37]]; [[#L51-L58]]) If only the last shell is convective (`LCZ(M)` true, `LCZ(M-1)` false), the loop marks the start of a convection zone at `I = M` and ends without calling `WCZIMP` or `SOLID` for it; the case `I.EQ.M` is reached only when the zone began below `M`. What follows: `OMEGA(M)`, `HI(M)`, `ETA2(M)`, `R0(M)` and `QIW(M)` keep the values they had before the call, and are not those of the current `HJM(M)` and structure. Only with rotation (`LROT`, off by default), and only for a model whose surface convection zone is a single shell; whether such models occur was not checked. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to treat a convection zone that starts at the last
    C shell.
                ELSE
    C  CONVECTION ZONE START - SET LCONVZ TO T
                   LCONVZ = .TRUE.
                   JSTART = I
                   IF(I.EQ.M) THEN
                      JEND = M
                      CALL WCZIMP(HD,HJM,HR,HS,HS2,JSTART,JEND,ETA2,HI,
         *                 OMEGA,QIW,R0,M)
                   ENDIF
                ENDIF
    ```

### GETROT

Converts $j(m)$ to $\Omega(m)$: `SOLID` for each radiative shell, `WCZIMP` for each convection zone.
