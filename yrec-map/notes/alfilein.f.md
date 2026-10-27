## Explanation

**Purpose.** This file reads a table of model atmospheres by France Allard and collaborators (its comments name the 1999 NextGen format and a newer "Allard" format of 2007) and puts it into the arrays that the atmosphere lookup [[alsurfp.f#ALSURFP|ALSURFP]] uses. For each $\log T_\mathrm{eff}$ and $\log g$ the table gives $\log P$ at $T = T_\mathrm{eff}$, and, in the new format, $\log P$ and $\log T$ at $\tau = 100$.

**How it fits.**
- **Input:** the file named `FALLARD`, opened on unit `IOATMA`. Both come from the run's settings: `FALLARD` is an argument of [[parmin.f#PARMIN|PARMIN]] and [[setups.f#SETUPS|SETUPS]], `IOATMA` is in `IOUNITS_MOD`, and the requested metallicity and $\alpha$-enhancement (`ALATM_FeH`, `ALATM_Alpha`) are in `NMLPAR_MOD`, set by PARMIN.
- **Who calls it:** [[setups.f#SETUPS|SETUPS]], once at start-up, and only when `KTTAU = 4` (Allard atmospheres, which the comment there says are used instead of Kurucz below 10,000 K).
- **What it calls:** [[#SORT_SHELL|SORT_SHELL]] (in this file) and [[altabinit.f#ALTABINIT|ALTABINIT]], which checks the table and derives its limits.
- **Output:** `ALATM01_MOD` (the grid `TEFFLs`, `GLs`, `FeHs`, `ALPHAs` and the tables `PLs`, `P100Ls`, `T100Ls`, with their sizes), read by [[altabinit.f#ALTABINIT|ALTABINIT]], [[alprint.f#ALPRINT|ALPRINT]] and [[alsurfp.f#ALSURFP|ALSURFP]].
- **Modules:** `ALATM01_MOD` (ALTABINIT, ALPRINT, ALSURFP), `NMLPAR_MOD` for the requested [Fe/H] and $\alpha$ (formerly `/ALATM03/`), `IOUNITS_MOD` for the units (formerly `/LUOUT/` and `/ALATM03/`).

**The method.**
1. Fill every table entry with $-999$, the mark of an invalid entry.
2. Read the first record to decide the format: `3.50` in columns 4–7 means the old NextGen format, `ALLARD` in columns 4–9 the new one. Anything else stops the run.
3. **Old NextGen:** fixed sizes, 54 temperatures and 5 gravities; reads $\log g$, the temperatures and $\log P$ only. This format has no $\tau = 100$ values.
4. **New format:** one record per ($T_\mathrm{eff}$, $\log g$, [Fe/H], $\alpha$). The routine reads the file twice. The first pass keeps only the records with the requested [Fe/H] and $\alpha$ and collects the distinct $T_\mathrm{eff}$ and $\log g$ values, which it then sorts. The second pass places each record's three values at its indices, and stores $\log_{10} T_\mathrm{eff}$ in `TEFFLs`.
5. Call [[altabinit.f#ALTABINIT|ALTABINIT]].

Gaps in the grid (combinations of $T_\mathrm{eff}$ and $\log g$ absent from the file) keep the value $-999$; ALTABINIT then finds each row's valid range.

**Design.** Every error ends the run with `STOP 9999` after a message to the screen and to `ISHORT`. Some messages name other routines ("AtTabInit Pass 1 File Error"), and the closing comment says "END OF ALINITTAB", left from earlier names.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/ALATM01/`; `/ALATM03/` split between `NMLPAR_MOD` and `IOUNITS_MOD`; `/LUOUT/` to `IOUNITS_MOD`; `/ALATM04/`, which held only dummies, removed), `IMPLICIT NONE`; the `EXTERNAL sort_shell` line, which a misplaced column had made a continuation of the `/ALATM04/` declaration, is now a statement of its own. The misspelled flag of question 1 is now declared as a local `LOGICAL`, so the question stands.

## Questions for the experts

1. **A misspelled flag.** The old-format branch tests `LATMTPTau100`, but the flag in `NMLPAR_MOD` is `LALTPTau100`. The misspelled name is a separate local variable, declared `LOGICAL*4` and never set, so the intended check (stop if $\tau = 100$ values are requested from an old file) probably never fires. Should it test `LALTPTau100`?
2. **Loop bounds.** The checks for new [Fe/H] and $\alpha$ values loop `do i = 1,nGL` instead of `1,nFeH` and `1,nALPHA`, and compare with entries of `FeHs` and `ALPHAs` that were never initialized. Since only records with the requested [Fe/H] and $\alpha$ get this far, `nFeH` and `nALPHA` should stay 1; is anything lost?
3. **Two tolerances for [Fe/H] and $\alpha$.** The passes skip a record if $|\alpha - \alpha_\mathrm{req}| > 0$ (exact match), but the second pass then checks again with $10^{-6}$. [Fe/H] has two tolerances too: the first pass keeps a record when $|\Delta[\mathrm{Fe/H}]| \le 10^{-5}$, and the second drops it when $|\Delta| \ge 10^{-6}$, so a record in between adds its $T_\mathrm{eff}$ and $\log g$ to the grid but is never stored. Should the passes use one tolerance each?
4. **Old-format temperatures.** In the old format `TEFFLs` is read as given, while the new format converts $T_\mathrm{eff}$ to $\log_{10} T_\mathrm{eff}$. Are the old files already in $\log T_\mathrm{eff}$? [[alprint.f#ALPRINT|ALPRINT]] prints `10**TEFFLs` in both cases.

### ALFILEIN

Reads the Allard atmosphere file, old or new format, keeps the records with the requested [Fe/H] and $\alpha$, fills `ALATM01_MOD` and calls [[altabinit.f#ALTABINIT|ALTABINIT]]. Stops the run on any error.

### SORT_SHELL

Shell's sort from Numerical Recipes, ascending, in place, with the increments $1, 4, 13, 40, \dots$ ($h \to 3h + 1$).
