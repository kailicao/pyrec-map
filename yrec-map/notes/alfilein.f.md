## Explanation

**Purpose.** This file reads a table of model atmospheres by France Allard and collaborators (its comments name the 1999 NextGen format and a newer "Allard" format of 2007) and puts it into the arrays that the atmosphere lookup [[alsurfp.f#ALSURFP|ALSURFP]] uses. For each $\log T_\mathrm{eff}$ and $\log g$ the table gives $\log P$ at $T = T_\mathrm{eff}$, and, in the new format, $\log P$ and $\log T$ at $\tau = 100$.

**How it fits.**
- **Input:** the file named `FALLARD`, opened on unit `IOATMA`. Both come from the run's settings: `FALLARD` is an argument of [[parmin.f#PARMIN|PARMIN]] and [[setups.f#SETUPS|SETUPS]], `IOATMA` is in `IOUNITS_MOD`, and the requested metallicity and $\alpha$-enhancement (`ALATM_FeH`, `ALATM_Alpha`) are in `NMLPAR_MOD`, set by PARMIN.
- **Who calls it:** [[setups.f#SETUPS|SETUPS]], once at start-up, and only when `KTTAU = 4` (Allard atmospheres, which the comment there says are used instead of Kurucz below 10,000 K).
- **What it calls:** [[#SORT_SHELL|SORT_SHELL]] (in this file) and [[altabinit.f#ALTABINIT|ALTABINIT]], which checks the table and derives its limits.
- **Output:** `ALATM01_MOD` (the grid `TEFFLs`, `GLs`, `FeHs`, `ALPHAs` and the tables `PLs`, `P100Ls`, `T100Ls`, with their sizes), read by [[altabinit.f#ALTABINIT|ALTABINIT]], [[alprint.f#ALPRINT|ALPRINT]] and [[alsurfp.f#ALSURFP|ALSURFP]].
- **Modules:** `ALATM01_MOD` (ALTABINIT, ALPRINT, ALSURFP), `NMLPAR_MOD` for the requested [Fe/H] and $\alpha$ (formerly `/ALATM03/`) and the flag `LALTPTau100`, `IOUNITS_MOD` for the units (formerly `/LUOUT/` and `/ALATM03/`).

**The method.**
1. Fill every table entry with $-999$, the mark of an invalid entry.
2. Read the first record to decide the format: `3.50` in columns 4–7 means the old NextGen format, `ALLARD` in columns 4–9 the new one. Anything else stops the run.
3. **Old NextGen:** fixed sizes, 54 temperatures and 5 gravities; reads $\log g$, the temperatures and $\log P$ only. This format has no $\tau = 100$ values. The temperatures are stored as read, with no conversion: The old file in the repository, `input/atmos/allard/Nextgen.p00`, already gives $\log T_\mathrm{eff}$ (3.23044892 to 4.00000000, that is 1,700 to 10,000 K, the range its `@@README` names), so `TEFFLs` holds $\log T_\mathrm{eff}$ in both formats ([[#L173-L175]]; settled from the code and the input file, Nov 9, 2026).
4. **New format:** one record per ($T_\mathrm{eff}$, $\log g$, [Fe/H], $\alpha$). The routine reads the file twice. The first pass keeps only the records with the requested [Fe/H] and $\alpha$ and collects the distinct $T_\mathrm{eff}$ and $\log g$ values, which it then sorts. The second pass places each record's three values at its indices, and stores $\log_{10} T_\mathrm{eff}$ in `TEFFLs`.
5. Call [[altabinit.f#ALTABINIT|ALTABINIT]].

Gaps in the grid (combinations of $T_\mathrm{eff}$ and $\log g$ absent from the file) keep the value $-999$; ALTABINIT then finds each row's valid range.

**Design.** Every error ends the run with `STOP 3`, the exit status for input errors, after a message to the screen and to `ISHORT`. Some messages name other routines ("AtTabInit Pass 1 File Error"), and the closing comment says "END OF ALINITTAB," left from earlier names.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/ALATM01/`; `/ALATM03/` split between `NMLPAR_MOD` and `IOUNITS_MOD`; `/LUOUT/` to `IOUNITS_MOD`; `/ALATM04/`, which held only dummies, removed), `IMPLICIT NONE`; the `EXTERNAL sort_shell` line, which a misplaced column had made a continuation of the `/ALATM04/` declaration, is now a statement of its own. The misspelled flag of former question 1 was then declared as a local `LOGICAL`, so the question stands.

**Changed since `a8a5950`.** The old-format branch now tests the namelist flag `LALTPTau100` (from `NMLPAR_MOD`) instead of the misspelled, never-set local `LATMTPTau100`, so an old NextGen 1 file is refused when $\tau = 100$ values are requested (this settles former question 1). The error exit stops with `STOP 3`, the code for input errors, instead of `STOP 9999` (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(never occurred)** **Two tolerances for [Fe/H] and $\alpha$.** ([[#L209-L210]]; [[#L296-L297]]; [[#L326-L327]]) Both passes skip a record when $|\Delta[\mathrm{Fe/H}]| > 10^{-5}$ or $|\Delta\alpha| > 0$ (an exact match), measured from the requested `ALATM_FeH`, `ALATM_Alpha`; the second pass then drops the record again when $|\Delta[\mathrm{Fe/H}]| \ge 10^{-6}$ or $|\Delta\alpha| \ge 10^{-6}$. For $\alpha$ the second test changes nothing; for [Fe/H], a request between $10^{-6}$ and $10^{-5}$ from the file's value adds the records' $T_\mathrm{eff}$ and $\log g$ to the grid in the first pass, but stores none of them, so every entry stays at $-999$ and [[altabinit.f#ALTABINIT|ALTABINIT]] stops the run with "Bad input Allard Table," not with a message that names the [Fe/H]. Only with `KTTAU` = 4 and a requested [Fe/H] that is not exactly a value of the file (whose values have two decimals, format `915`).

    **A possible fix:**

    ```diff
    --- a/src/alfilein.f
    +++ b/src/alfilein.f
    @@ -323,8 +323,11 @@
     
     C we now verify that we have the correct FeH and Alpha
     
    -      if (DABS(FeH -ALATM_FeH) .ge. 1D-6)  goto 440     ! Wrong FeH, bypass item
    -      if (DABS(Alpha -ALATM_Alpha) .ge. 1D-6)  goto 440 ! Wrong Alpha, bypass item
    +C 11/09/26 KC via Claude
    +C code changed to drop the second test of FeH and Alpha, whose 1D-6
    +C dropped records that the test after label 410 (1D-5) had kept.
    +C     if (DABS(FeH -ALATM_FeH) .ge. 1D-6)  goto 440
    +C     if (DABS(Alpha -ALATM_Alpha) .ge. 1D-6)  goto 440
     
     
     C We now have the correct indices for our tables, i1 for the Teff-direction
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Of 34 runs (26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones; one of these, with `FCORE` = 1.0, stopped in its first second), only `testsuite/Test_solarGS98_allard` uses the Allard table (`Nextgen2.all`, `KTTAU` = 4). There the second test ran 316 times, each with [Fe/H] = 0 requested and found, and it never dropped a record. No case sets `ALATM_FeH` (the default is 0), and a value written as in the file reads to the same number as the file's two-decimal field, so the condition needs a request between $10^{-6}$ and $10^{-5}$ off a value of the file, which no case or document makes; it was not run. No fix was run. Intent: none found.

2. **(never occurred)** **Loop bounds for the new [Fe/H] and $\alpha$ values.** ([[#L248-L262]]) The checks for new [Fe/H] and $\alpha$ values loop `do i = 1,nGL` instead of `1,nFeH` and `1,nALPHA`, and so compare with entries of `FeHs` and `ALPHAs` that were never set. Harmless today: Only records within $10^{-5}$ of the requested [Fe/H] and with exactly the requested $\alpha$ get this far, and since the file's values have two decimals they are all equal to the first, found at `i` = 1; `nFeH` and `nALPHA` stay 1, and only [[alprint.f#ALPRINT|ALPRINT]] prints them. It would count wrong values once the filter let several [Fe/H] or $\alpha$ through.

    **A possible fix:**

    ```diff
    --- a/src/alfilein.f
    +++ b/src/alfilein.f
    @@ -246,7 +246,10 @@
     
     
     c Now check FeHs, increase counter if needed
    -      do i = 1,nGL  ! Skip out if any old FeH is a match
    +C 11/09/26 KC via Claude
    +C code changed to loop over the FeH and ALPHA values found so far,
    +C not over the GL values.
    +      do i = 1,nFeH  ! Skip out if any old FeH is a match
             if (DABS(FeH-FeHs(i)) .lt.1D-6) goto 314
           enddo
             nFeH = nFeH+1      ! count the next FeH
    @@ -254,7 +257,7 @@
      314  CONTINUE
     
     c Now check ALPHAs, increase counter if needed
    -      do i = 1,nGL  ! Skip out if any old ALPHA is a match
    +      do i = 1,nALPHA  ! Skip out if any old ALPHA is a match
             if (DABS(ALPHA-ALPHAs(i)) .lt.1D-6) goto 316
           enddo
             nALPHA = nALPHA+1      ! count the next ALPHA
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): In `testsuite/Test_solarGS98_allard`, the only Allard run, the two loops ran for 315 records, all with [Fe/H] = 0 and $\alpha$ = 0; the first entry matched every time, so no unset entry was compared. It would need records of several [Fe/H] or $\alpha$ to pass the filter, which no case or table does. No fix was run. Intent: none found.

### ALFILEIN

Reads the Allard atmosphere file, old or new format, keeps the records with the requested [Fe/H] and $\alpha$, fills `ALATM01_MOD` and calls [[altabinit.f#ALTABINIT|ALTABINIT]]. Stops the run on any error.

### SORT_SHELL

Shell's sort from Numerical Recipes, ascending, in place, with the increments $1, 4, 13, 40, \dots$ ($h \to 3h + 1$).
