## Explanation

**Purpose.** Prepares the list of runs ("kind cards") for the automatic calibration of a solar model: it fills 48 runs, 16 repetitions of a three-run pattern, from the first three runs given by the user. The calibration itself (adjusting $X$ and the mixing length between repetitions) is done elsewhere, by [[chkcal.f#CHKCAL|`CHKCAL`]].

**How it fits.**
- **Who calls it:** the main program ([[main.f|`main.f`]]), when `LCALS` is true, before the loop over runs. It passes `FACAGE`, an age factor that is 1 except in Monte Carlo runs (`LMONTE`), where it is drawn per model.
- **Inputs and outputs, all through COMMON:** `/CKIND/` (`NUMRUN`, `RESCAL`, `NMODLS`, `IRESCA`, `LFIRST`), `/SETT/` (`ENDAGE`, `SETDT`, `LENDAG`, `LSETDT`), `/NEWXYM/` (`XENV0A`, `ZENV0A`, `CMIXLA`, `LSENV0A`, `SENV0A`), `/ZRAMP/` (`RSCLZC`, `RSCLZM1`, `RSCLZM2`), `/CALS2/` (`CALSOLAGE`, the solar age), `/CALSUN/` (`LSOL`, set to false). These are shared with [[parmin.f#PARMIN|`PARMIN`]] (which reads them), [[chkcal.f#CHKCAL|`CHKCAL`]], [[rscale.f#RSCALE|`RSCALE`]], [[starin.f#STARIN|`STARIN`]] and the main program.

**The method.**
- `NUMRUN` = 48; the composition and mixing length of run 1 are copied to runs 2–48.
- Runs 4, 7, …, 46 repeat run 1 (a new starting model with its rescaling; `LFIRST` true).
- Run 2 ends at $10^8$ yr × `FACAGE`, and run 3 at `CALSOLAGE` × `FACAGE`; both time steps `SETDT` are scaled by `FACAGE` too. Runs 5, 8, …, 47 repeat run 2, and runs 6, 9, …, 48 repeat run 3, each continuing from the previous model (`IRESCA` = 1, `LFIRST` false).

## Questions for the experts

1. **The new stop criteria are not copied.** `END_DCEN`, `END_XCEN` and `END_YCEN` (in `/SETT/`, "MHP 10/24 ADDED STOP CRITERIA") are not copied to the repeated runs, unlike `ENDAGE` and `SETDT`. A user who sets them for runs 2 or 3 would see them used only in the first repetition. Should they be copied?
2. **Stale comment.** The comment says "COPYING THE RELEVANT PARAMETERS FROM THE FIRST TWO RUNS TO THE NEXT SERIES OF 24 CALIBRATING RUNS"; the code (since "mhp 5/96") uses three runs and 48 in all.
3. **The hard-wired $10^8$ yr.** Run 2's end age is fixed at $10^8$ yr regardless of the input `ENDAGE(2)`. What is this run for (probably reaching the zero-age main sequence)? A namelist value might be clearer.
