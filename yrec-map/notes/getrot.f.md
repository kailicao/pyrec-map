## Explanation

**Purpose.** `GETROT` turns a run of specific angular momentum $j(m)$ into a rotation curve $\Omega(m)$. Radiative shells are treated one at a time; each convection zone is given its rotation law as a whole. (Its comment calls it `GETW`, an older name.)

**The comment names another routine.** It begins "GETW TAKES THE ANGULAR MOMENTUM DISTRIBUTION…" ([[#L21-L23]]), but the routine is `GETROT`, and [[getw.f#GETW|`GETW`]] is another routine, so the comment should name `GETROT`.

**How it fits.**
- **Who calls it:** [[checkj.f#CHECKJ|CHECKJ]], [[crrect.f#CRRECT|CRRECT]], [[getnewenv.f#GETNEWENV|GETNEWENV]], [[getw.f#GETW|GETW]], [[hpoint.f#HPOINT|HPOINT]] and [[midmod.f#MIDMOD|MIDMOD]].
- **Inputs:** `HJM` ($j$ per shell), `LCZ` (convective flags), the structure (`HD`, `HR`, `HS`, `HS2`), `M`.
- **What it calls:** [[solid.f#SOLID|SOLID]] (for a single radiative shell) and [[wczimp.f#WCZIMP|WCZIMP]] (for a convection zone; "JNT 09/25 for 05/15 call WCZIMP instead of WCZ").
- **Outputs:** `OMEGA`, `HI` (moments of inertia of the shells), `ETA2`, `QIW`, `R0`, filled by `SOLID` and `WCZIMP`; and `HJM`, which both rewrite as $j = I\Omega/\Delta m$, so that in a convection zone, where `WCZIMP` imposes the rotation law, $j$ is redistributed.

**The method.** Scanning outward: each radiative shell is passed to `SOLID` alone, which finds the $\Omega$ for which $\Omega\,I(\Omega) = j\,\Delta m$, iterating SHAPE and MOMI, since the shell's moment of inertia depends on $\Omega$ through its distortion; a run of convective shells is collected and passed to `WCZIMP` when the next radiative shell (or the surface) is reached (but see [[#b1]]).

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`, and the array size `JSON` from `DIMENSIONS_MOD`.

## Bugs, by priority

1. **(never occurred)** **A one-shell convective surface is never treated.** ([[#L33-L37]]; [[#L51-L58]]) If only the last shell is convective (`LCZ(M)` true, `LCZ(M-1)` false), the loop marks the start of a convection zone at `I = M` and ends without calling `WCZIMP` or `SOLID` for it; the case `I.EQ.M` is reached only when the zone began below `M`. What follows: `OMEGA(M)`, `HI(M)`, `ETA2(M)`, `R0(M)` and `QIW(M)` keep the values they had before the call, and are not those of the current `HJM(M)` and structure. Only with rotation (`LROT`, off by default), and only for a model whose surface convection zone is a single shell.

    **A possible fix:**

    ```diff
    --- a/src/getrot.f
    +++ b/src/getrot.f
    @@ -30,10 +30,18 @@
                    JEND = I
                    CALL SOLID(HD,HJM,HR,HS,HS2,JSTART,JEND,ETA2,HI,OMEGA,
          *          QIW,R0,M)
    +C 11/09/26 KC via Claude
    +C code changed to treat a convection zone that starts at the last
    +C shell.
                 ELSE
     C  CONVECTION ZONE START - SET LCONVZ TO T
                    LCONVZ = .TRUE.
                    JSTART = I
    +               IF(I.EQ.M) THEN
    +                  JEND = M
    +                  CALL WCZIMP(HD,HJM,HR,HS,HS2,JSTART,JEND,ETA2,HI,
    +     *                 OMEGA,QIW,R0,M)
    +               ENDIF
                 ENDIF
              ELSE IF(.NOT.LCZ(I)) THEN
     C  THE PREVIOUS SHELL WAS CONVECTIVE.  IF THIS ONE IS RADIATIVE, ENFORCE
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): A convection zone started in all five rotating test cases (from 6,703 times in `testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS` to 27,038 in `testsuite/Test_solarGS98_difrotmixper18p4d1p0`), at shells 1 to 928 in models of 350 to 1,070 shells, but never at the last shell: No model had a single-shell surface convection zone, not even in the 2 and 3 $M_\odot$ cases, so no run reached the bug. It needs a rotating model whose surface convection zone is a single shell; none of YREC's cases was found to have one. Intent: none found; the special case ([[#L51-L58]]) covers only a zone that began below the surface.

### GETROT

Converts $j(m)$ to $\Omega(m)$: `SOLID` for each radiative shell, `WCZIMP` for each convection zone.
