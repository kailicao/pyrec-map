## Explanation

**Purpose.** Writes a stellar model in the older "YREC7" text format (LLP 4/16/03), which YREC can still read as a starting model. [[putmodel2.f#PUTMODEL2|PUTMODEL2]] writes the newer "MODEL2" format.

**How it fits.**
- **Inputs:** the model and its global quantities, as arguments (as for `PUTMODEL2`, without the physics labels). The comments "Last two lines are MODEL2 add-ons" ([[#L31]]) and "Any error messages go to LU ISHORT" ([[#L51]]) describe the argument list before `ISHORT` and the MODEL2 add-ons were removed from it ([[#L9-L10]]; [[#L28-L29]]).
- **Who calls it:** no routine in `src/` calls it. It is kept on purpose: `KNOWN_ISSUES.md` (issue 24, lines 1658–1666) records the developers' ruling to keep it, since its reader is live and the format may have legacy use, while fourteen other unreachable routines were removed (settled from YREC's public sources, Nov 9, 2026).
- **Who reads the format:** [[starin.f#STARIN|STARIN]] recognizes the leading `NMOD` and calls [[getyrec7.f#GETYREC7|GETYREC7]].
- **Output:** the file on unit `IWRITE`. The routine also changes two of the caller's arrays: `TLUMX` is converted to erg s⁻¹ in place when it is in solar units ([[#L71-L77]]), and `OMEGA` is floored at $10^{-59}$ ([[#L131]]).

**The format.** A header line `NMOD` (model number, shells, mass, $\log T_\mathrm{eff}$, $\log L$, $\log M$, age, step); a flags line (`LROT`, `LEXCOM`, `JCORE`, `JENV`, `CMIXL`); a `TLUMX` line (erg s⁻¹); three `ENV` lines; one line per shell ($\log m$, $\log r$, $L$, $\log P$, $\log T$, $\log\rho$, convection flag, and $X$ and $Z$ as integers in units of $10^{-6}$); the abundances 4–11 only from `JCORE` to `JENV` (each convection zone stores one composition); with `LEXCOM`, abundances 12–15 two shells per line; with `LROT`, $|\log_{10}\Omega|$, eight per line. For a fully convective star (`JENV` ≤ `JCORE`), two lines of abundances 4–11 are written, for `JCORE` and `JENV` ([[#L102-L104]]), although the comment says "write out 1 comp" ([[#L101]]); [[getyrec7.f#GETYREC7|GETYREC7]] reads two as well ([[getyrec7.f#L156-L157]]), so only the comment is wrong (settled from the code, Nov 9, 2026).

> **Question** ([[#L92-L93]]; [[#L131-L132]]). **Precision.** $X$ and $Z$ per shell are rounded to $10^{-6}$, and $\Omega$ is written as $|\log_{10}\Omega|$ with 7 decimals (the sign of $\log\Omega$ is lost if $\Omega > 1$ rad s⁻¹; GETYREC7 reads it back as $10^{-|\log_{10}\Omega|}$, [[getyrec7.f#L231-L236]]). Is this acceptable for a legacy format?

**Changed since `rp_1`.** Declarations only: `/CONST/` to `CONSTANTS_MOD`, `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Bugs, by priority

1. **(d)** **The flags record does not match its reader.** ([[#L65-L66]]; [[getyrec7.f#L104-L105]]) This routine writes the flags as `2(L1,1X),'F F ',2I4,F7.3`, four characters between the flags and `JCORE`; [[getyrec7.f#GETYREC7|GETYREC7]] reads them as `2(L1,1X),5X,2I4,F7.3`, skipping five, so every field it reads is shifted by one column. With Fortran's default treatment of blanks in input (ignored), the values still come back right while `JENV` < 1000 and `CMIXL` < 10; when `JENV` has four digits, its first digit is read as the last digit of `JCORE`, and `JENV` loses it. Only when a model written by PUTYREC7, which nothing in `src/` calls, is read back. Read from the code, not run. **A possible fix** (in the writer, since GETYREC7 presumably matches the files YREC7 itself wrote):

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to write five characters between the flags and JCORE,
    C as GETYREC7 reads them.
       30 FORMAT(2(L1,1X),'F F  ',2I4,F7.3)
    ```
