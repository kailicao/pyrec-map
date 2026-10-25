## Explanation

**Purpose.** Writes a stellar model in the older "YREC7" text format (LLP 4/16/03), which YREC can still read as a starting model. [[putmodel2.f#PUTMODEL2|PUTMODEL2]] writes the newer "MODEL2" format.

**How it fits.**
- **Inputs:** the model and its global quantities, as arguments (as for `PUTMODEL2`, without the physics labels).
- **Who calls it:** no routine in `src/` calls it.
- **Who reads the format:** [[starin.f#STARIN|STARIN]] recognizes the leading `NMOD` and calls [[getyrec7.f#GETYREC7|GETYREC7]].
- **Output:** the file on unit `IWRITE`.

**The format.** A header line `NMOD` (model number, shells, mass, $\log T_\mathrm{eff}$, $\log L$, $\log M$, age, step); a flags line (`LROT`, `LEXCOM`, `JCORE`, `JENV`, `CMIXL`); a `TLUMX` line (erg s⁻¹); three `ENV` lines; one line per shell ($\log m$, $\log r$, $L$, $\log P$, $\log T$, $\log\rho$, convection flag, and $X$ and $Z$ as integers in units of $10^{-6}$); the abundances 4–11 only from `JCORE` to `JENV` (each convection zone stores one composition); with `LEXCOM`, abundances 12–15 two shells per line; with `LROT`, $|\log_{10}\Omega|$, eight per line.

**KC's changes.** 2025-05-31: the unused argument `ISHORT` and the MODEL2 add-ons (labels and flags) removed from the argument list.

## Questions for the experts

1. **Precision.** $X$ and $Z$ per shell are rounded to $10^{-6}$, and $\Omega$ is written as $|\log_{10}\Omega|$ with 7 decimals (the sign of $\log\Omega$ is lost if $\Omega > 1$ rad s⁻¹). Acceptable for a legacy format?
2. **Side effects.** `OMEGA` is floored at $10^{-59}$ and `TLUMX` converted to erg s⁻¹ in the caller's arrays.
3. **The fully convective case.** The comment says "if star is fully convective, write out 1 comp", but two lines are written (for `JCORE` and `JENV`); [[getyrec7.f#GETYREC7|GETYREC7]] reads two as well, so only the comment is wrong.
4. **The flags record does not match its reader.** This routine writes the flags as `2(L1,1X),'F F ',2I4,F7.3`, four characters between the flags and `JCORE`; [[getyrec7.f#GETYREC7|GETYREC7]] reads them as `2(L1,1X),5X,2I4,F7.3`, skipping five. Read back, `JCORE`, `JENV` and `CMIXL` are shifted by one column. One of the two formats needs to change (GETYREC7 presumably matches the files YREC7 itself wrote).
5. **Stale comments.** "Last two lines are MODEL2 add-ons" and "Any error messages go to LU ISHORT" describe the argument list before KC's change of 2025-05-31.
6. **Still needed?** No routine calls `PUTYREC7`. Can it be removed, or is it called from outside `src/`?
