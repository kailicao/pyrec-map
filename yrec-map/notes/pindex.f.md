## Explanation

**Purpose.** Chooses which shells of a model are printed (`ID(1..IDM)`): every `NPRTPT`-th shell, plus every shell of the hydrogen-burning shell when `LSHELL` is true. The first and last shells are always included.

**How it fits.**
- **Inputs:** the edges of the burning shell `JXBEG`, `JXEND`, the flag `LSHELL`, the number of shells `M`; `NPRTPT` from `NMLPAR_MOD` (formerly `/CCOUT1/`; set in [[parmin.f#PARMIN|PARMIN]]).
- **Who calls it:** only [[putstore.f#PUTSTORE|PUTSTORE]], which passes `LSHELL`, `JXBEG` and `JXEND` as locals it never sets ([[putstore.f#L262]]), so the `LSHELL` branch is not taken wherever the compiler zero-fills `SAVE`d locals (settled from the code, Nov 9, 2026).
- **Outputs:** the list `ID` and its length `IDM`.

**The method.** Without a shell: $1, k, 2k, \dots, M$ with $k$ = `NPRTPT`. With a shell: the multiples of $k$ below `JXBEG`, every shell from `JXBEG` to `JXEND`, the multiples of $k$ above, and $M$.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/CCOUT1/`, now gone, to `NMLPAR_MOD`; the unused `/CCOUT/` dropped), `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Bugs, by priority

1. **(cannot be reached)** **`IEND` undefined.** ([[#L48-L56]]) In the `LSHELL` branch, if `NPRTPT` $\ge$ `JXBEG`, the first block is skipped and `IF(IEND .EQ. JXBEG)` reads `IEND` from an earlier call (`SAVE`), or undefined on the first. The result decides whether `JXBEG` is listed twice or not at all. Only if the `LSHELL` branch is taken (above).

    **A possible fix:**

    ```diff
    --- a/src/pindex.f
    +++ b/src/pindex.f
    @@ -41,8 +41,12 @@
     
     C  ID IS THE ARRAY OF THE SHELLS TO BE PRINTED OUT;
     C  I.E. IF SHELLS 1,3,5,..TO BE PRINTED ID(1)=1,ID(2)=3,..
    +C 11/09/26 KC via Claude
    +C code changed to set IEND first, so that the test on JXBEG does not
    +C read a value from an earlier call.
           ID(1) = 1
           IDM = 2
    +      IEND = 0
           IF(LSHELL) THEN
     C  PRINT OUT EVERY ZONE IN H-BURNING SHELL
            IF(NPRTPT.LT.JXBEG) THEN
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in any of 34 runs: 26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones. It cannot be reached at 7be4133: PINDEX's only caller, PUTSTORE, passes its own `LSHELL`, which nothing sets ([[putstore.f#b3]]); in the runs it was false at every call. With PUTSTORE's bug fixed, the branch would run at each old-format store after the core's hydrogen is exhausted, but these runs hold no counts from PINDEX with that fix. The fix was not run. Intent: none found.

2. **(cannot be reached)** **`M` listed twice.** ([[#L65-L72]]; [[#L83]]) In the `LSHELL` branch, if `M` is a multiple of `NPRTPT` (always, with the default `NPRTPT` = 1), the loop adds `M` and so does the final `ID(IDM) = M`; the general branch guards against this ([[#L77]]), the shell branch does not. PUTSTORE would then write the surface shell twice. Only if the `LSHELL` branch is taken (above).

    **A possible fix:**

    ```diff
    --- a/src/pindex.f
    +++ b/src/pindex.f
    @@ -64,7 +64,11 @@
        20    CONTINUE
            IF(NPRTPT.LT.M) THEN
               IBEG = INT(JXEND/NPRTPT+1)*NPRTPT
    +C 11/09/26 KC via Claude
    +C code changed to leave M to the final ID(IDM) = M, as the general
    +C case does.
               IEND = INT(M/NPRTPT)*NPRTPT
    +          IF (IEND .EQ. M) IEND = IEND - NPRTPT
               DO 30 J = IBEG,IEND,NPRTPT
                  ID(IDM) = J
                  IDM = IDM + 1
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in the same 34 runs. It cannot be reached at 7be4133: PINDEX's only caller, PUTSTORE, passes its own `LSHELL`, which nothing sets ([[putstore.f#b3]]); in the runs it was false at every call. With PUTSTORE's bug fixed, the branch would run at each old-format store after the core's hydrogen is exhausted, but these runs hold no counts from PINDEX with that fix. With `NPRTPT` = 1, the default and the value in YREC's cases, it would then hold at every such store. The run of PUTSTORE's fix agrees: In `testsuite/Test_m0p95feh+0p0_GN93_TAHB` and `testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS` the `.store` file changed beyond 2% while the track stayed identical, as `M` written twice would make it (an inference from the code; the stored models were not compared line by line). The fix was not run. Intent: none found; the general branch guards against it ([[#L77]]).
