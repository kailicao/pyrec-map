## Explanation

**Purpose.** Chooses which shells of a model are printed (`ID(1..IDM)`): every `NPRTPT`-th shell, plus every shell of the hydrogen-burning shell when `LSHELL` is true. The first and last shells are always included.

**How it fits.**
- **Inputs:** the edges of the burning shell `JXBEG`, `JXEND`, the flag `LSHELL`, the number of shells `M`; `NPRTPT` from `NMLPAR_MOD` (formerly `/CCOUT1/`; set in [[parmin.f#PARMIN|PARMIN]]).
- **Who calls it:** only [[putstore.f#PUTSTORE|PUTSTORE]], which passes `LSHELL`, `JXBEG` and `JXEND` as locals it never sets ([[putstore.f#L262]]), so the `LSHELL` branch is not taken wherever the compiler zero-fills `SAVE`d locals (settled from the code, Nov 9, 2026).
- **Outputs:** the list `ID` and its length `IDM`.

**The method.** Without a shell: $1, k, 2k, \dots, M$ with $k$ = `NPRTPT`. With a shell: the multiples of $k$ below `JXBEG`, every shell from `JXBEG` to `JXEND`, the multiples of $k$ above, and $M$.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/CCOUT1/`, now gone, to `NMLPAR_MOD`; the unused `/CCOUT/` dropped), `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Bugs, by priority

1. **(d)** **`IEND` undefined.** ([[#L48-L56]]) In the `LSHELL` branch, if `NPRTPT` $\ge$ `JXBEG`, the first block is skipped and `IF(IEND .EQ. JXBEG)` reads `IEND` from an earlier call (`SAVE`), or undefined on the first. The result decides whether `JXBEG` is listed twice or not at all. Only if the `LSHELL` branch is taken (above). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to set IEND first, so that the test on JXBEG does not
    C read a value from an earlier call.
          ID(1) = 1
          IDM = 2
          IEND = 0
    ```

2. **(d)** **`M` listed twice.** ([[#L65-L72]]; [[#L83]]) In the `LSHELL` branch, if `M` is a multiple of `NPRTPT` (always, with the default `NPRTPT` = 1), the loop adds `M` and so does the final `ID(IDM) = M`; the general branch guards against this ([[#L77]]), the shell branch does not. PUTSTORE would then write the surface shell twice. Only if the `LSHELL` branch is taken (above). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to leave M to the final ID(IDM) = M, as the general
    C case does.
              IEND = INT(M/NPRTPT)*NPRTPT
              IF (IEND .EQ. M) IEND = IEND - NPRTPT
    ```
