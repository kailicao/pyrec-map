## Explanation

**Purpose.** Prepares the list of runs ("kind cards") for the automatic calibration of a solar model: it fills 48 runs, 16 repetitions of a three-run pattern, from the first three runs given by the user. The calibration itself (adjusting $X$ and the mixing length between repetitions; with $Z$ or $Z/X$ held fixed, setting $X$ sets the initial helium $Y = 1 - X - Z$, which is why the documentation speaks of calibrating the helium) is done elsewhere, by [[chkcal.f#CHKCAL|`CHKCAL`]].

**How it fits.**
- **Who calls it:** the main program ([[main.f|`main.f`]]), when `LCALS` is true, before the loop over runs. It passes `FACAGE`, an age factor, now always 1 (main.f sets `FACAGE = 1.0D0`, [[main.f#L369]]; it was drawn per model in the Monte Carlo option, removed since `rp_1`), and `LSOL`, a local of the main program that this routine sets to false (the flag `CHKCAL` sets when the calibration has converged).

    > **Question** ([[#L2]]; [[#L77-L82]]; [[main.f#L369]]). **`FACAGE` still an argument.** With the Monte Carlo option removed, main.f sets `FACAGE = 1.0D0` and nothing changes it, so the factor on the end ages and `SETDT` of runs 2 and 3 is always 1. Can the argument go, or is it kept for a planned use?

- **Inputs and outputs, through modules** (besides `LSOL`): `NMLPAR_MOD`, the namelist's per-run arrays (`NUMRUN`, `NMODLS`, `LFIRST`, `ENDAGE`, `SETDT`, `XENV0A`, `ZENV0A`, `CMIXLA`, `LSENV0A`, `SENV0A`, `RSCLZC`, `RSCLZM1`, `RSCLZM2`, and `CALSOLAGE`, the solar age), and `RUNLOOP_MOD` (`RESCAL`, `IRESCA`, `LENDAG`, `LSETDT`). These are shared with [[parmin.f#PARMIN|`PARMIN`]] (which reads them), [[chkcal.f#CHKCAL|`CHKCAL`]], [[rscale.f#RSCALE|`RSCALE`]], [[starin.f#STARIN|`STARIN`]] and the main program.

**The method.**
- `NUMRUN` = 48; the composition and mixing length of run 1 are copied to runs 2–48.

    > **Question** ([[#L52-L57]]). **A stale comment.** The comment says "COPYING THE RELEVANT PARAMETERS FROM THE FIRST TWO RUNS TO THE NEXT SERIES OF 24 CALIBRATING RUNS"; the code (since "mhp 5/96", [[#L56]]) uses three runs and 48 in all. Can the comment be brought up to date?

- Runs 4, 7, …, 46 repeat run 1 (a new starting model with its rescaling; `LFIRST` true).
- Run 2 ends at $10^8$ yr × `FACAGE`, and run 3 at `CALSOLAGE` × `FACAGE`; both time steps `SETDT` are scaled by `FACAGE` too. Runs 5, 8, …, 47 repeat run 2, and runs 6, 9, …, 48 repeat run 3, each continuing from the previous model (`IRESCA` = 1, `LFIRST` false).

    > **Question** ([[#L76-L77]]). **The hard-wired $10^8$ yr.** Run 2's end age is fixed at $10^8$ yr regardless of the input `ENDAGE(2)` (the older line, [[#L78]], is commented out). What is this run for (probably reaching the zero-age main sequence)? Would a namelist value be clearer?

    > **Question** ([[#L83-L100]]). **The new stop criteria are not copied.** `END_DCEN`, `END_XCEN` and `END_YCEN` ("MHP 10/24 ADDED STOP CRITERIA", [[#L32]]; per-run arrays in `NMLPAR_MOD`, [[nmlpar_mod.f#L261-L263]]) are not copied to the repeated runs, unlike `ENDAGE` and `SETDT`. A user who sets them for runs 2 or 3 would see them used only in the first repetition. Should they be copied?


**From YREC's documentation.** [Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html) (Calibration): `LCALS` calibrates the solar helium abundance and mixing length automatically, to match the Sun's radius and luminosity at its age `CALSOLAGE` (default 4.57D9 yr; the documentation calls it a "tolerance"), within `TOLL` and `TOLR` (1.0D-5, 1.0D-4); with `LCALSOLZX`, $Z/X$ is held at `CALSOLZX` (0.02292, GS98), otherwise $Z$ is held fixed.

**Changed since `rp_1`.** `LSOL` is an argument (formerly in `/CALSUN/`, whose other members this routine never used); declarations only otherwise: COMMON blocks to modules, `IMPLICIT NONE`.
