## Explanation

**Purpose.** Chooses which shells of a model are printed (`ID(1..IDM)`): every `NPRTPT`-th shell, plus every shell of the hydrogen-burning shell when `LSHELL` is true. The first and last shells are always included.

**How it fits.**
- **Inputs:** the edges of the burning shell `JXBEG`, `JXEND`, the flag `LSHELL`, the number of shells `M`; `NPRTPT` from `/CCOUT1/` (set in [[parmin.f#PARMIN|PARMIN]]).
- **Who calls it:** only [[putstore.f#PUTSTORE|PUTSTORE]].
- **Outputs:** the list `ID` and its length `IDM`.

**The method.** Without a shell: $1, k, 2k, \dots, M$ with $k$ = `NPRTPT`. With a shell: the multiples of $k$ below `JXBEG`, every shell from `JXBEG` to `JXEND`, the multiples of $k$ above, and $M$.

## Questions for the experts

1. **`IEND` undefined.** In the `LSHELL` branch, if `NPRTPT` $\ge$ `JXBEG`, the first block is skipped and `IF(IEND .EQ. JXBEG)` reads `IEND` from an earlier call (`SAVE`), or undefined on the first. The result decides whether `JXBEG` is listed twice or not at all. Set `IEND = 0` first?
2. **`M` listed twice.** In the `LSHELL` branch, if `M` is a multiple of `NPRTPT`, the loop adds `M` and so does the final `ID(IDM) = M`; the general branch guards against this (`IF (IEND .EQ. M) IEND = IEND - NPRTPT`), the shell branch does not.
