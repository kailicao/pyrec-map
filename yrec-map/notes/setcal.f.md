## Explanation

**Purpose.** Prepares the list of runs ("kind cards") for the automatic calibration of a solar model: it fills 48 runs, 16 repetitions of a three-run pattern, from the first three runs given by the user. The calibration itself (adjusting $X$ and the mixing length between repetitions; with $Z$ or $Z/X$ held fixed, setting $X$ sets the initial helium $Y = 1 - X - Z$, which is why the documentation speaks of calibrating the helium) is done elsewhere, by [[chkcal.f#CHKCAL|`CHKCAL`]].

**How it fits.**
- **Who calls it:** the main program ([[main.f|`main.f`]]), when `LCALS` is true, before the loop over runs. It passes `FACAGE`, an age factor, now always 1 (main.f sets `FACAGE = 1.0D0`, [[main.f#L369]]; it was drawn per model in the Monte Carlo option, removed since `rp_1`), and `LSOL`, a local of the main program that this routine sets to false (the flag `CHKCAL` sets when the calibration has converged).

    > **Question** ([[#L2]]; [[#L77-L82]]; [[main.f#L369]]). **`FACAGE` still an argument.** With the Monte Carlo option removed, main.f sets `FACAGE = 1.0D0` and nothing changes it, so the factor on the end ages and `SETDT` of runs 2 and 3 is always 1. Can the argument go, or is it kept for a planned use?

- **Inputs and outputs, through modules** (besides `LSOL`): `NMLPAR_MOD`, the namelist's per-run arrays (`NUMRUN`, `NMODLS`, `LFIRST`, `ENDAGE`, `SETDT`, `XENV0A`, `ZENV0A`, `CMIXLA`, `LSENV0A`, `SENV0A`, `RSCLZC`, `RSCLZM1`, `RSCLZM2`, and `CALSOLAGE`, the solar age), and `RUNLOOP_MOD` (`RESCAL`, `IRESCA`, `LENDAG`, `LSETDT`). These are shared with [[parmin.f#PARMIN|`PARMIN`]] (which reads them), [[chkcal.f#CHKCAL|`CHKCAL`]], [[rscale.f#RSCALE|`RSCALE`]], [[starin.f#STARIN|`STARIN`]] and the main program.

**The method.**
- `NUMRUN` = 48; the composition and mixing length of run 1 are copied to runs 2–48.

    The comment ([[#L52-L55]]) is stale: Since "mhp 5/96" ([[#L56]]) the code sets `NUMRUN` = 48 ([[#L57]]), not "THE MAXIMUM (50)," and copies the first three runs, not two, to runs 4–48, 15 further series of three (the loops at [[#L65]], [[#L83]], and [[#L92]], in steps of 3); its "24" fits the two-run pattern that [[setscal.f#SETSCAL|SETSCAL]] still uses ([[setscal.f#L112-L131]]).

    > **Question** ([[#L52-L55]]). **A stale comment.** Can the comment be brought up to date, to say that the first three runs are copied to the next 15 series of three (runs 4–48)?

- Runs 4, 7, …, 46 repeat run 1 (a new starting model with its rescaling; `LFIRST` true).
- Run 2 ends at $10^8$ yr × `FACAGE`, and run 3 at `CALSOLAGE` × `FACAGE`; both time steps `SETDT` are scaled by `FACAGE` too. Runs 5, 8, …, 47 repeat run 2, and runs 6, 9, …, 48 repeat run 3, each continuing from the previous model (`IRESCA` = 1, `LFIRST` false).

    > **Question** ([[#L76-L77]]). **The hard-wired $10^8$ yr.** Run 2's end age is fixed at $10^8$ yr regardless of the input `ENDAGE(2)` (the older line, [[#L78]], is commented out). What is this run for (probably reaching the zero-age main sequence)? Would a namelist value be clearer?

    The stop criteria `END_DCEN`, `END_XCEN`, and `END_YCEN` are not copied ([[#b1]]).


**From YREC's documentation.** [Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html) (Calibration): `LCALS` calibrates the solar helium abundance and mixing length automatically, to match the Sun's radius and luminosity at its age `CALSOLAGE` (default 4.57D9 yr; the documentation calls it a "tolerance"), within `TOLL` and `TOLR` (1.0D-5, 1.0D-4); with `LCALSOLZX`, $Z/X$ is held at `CALSOLZX` (0.02292, GS98), otherwise $Z$ is held fixed.

**Changed since `rp_1`.** `LSOL` is an argument (formerly in `/CALSUN/`, whose other members this routine never used); declarations only otherwise: COMMON blocks to modules, `IMPLICIT NONE`.

## Bugs, by priority

1. **(never occurred)** **The new stop criteria are not copied to the repeated runs.** ([[#L83-L100]]; [[nmlpar_mod.f#L261-L263]]; [[main.f#L1089-L1115]]) The loops that repeat runs 2 and 3 copy `ENDAGE`, `LENDAG`, `SETDT`, and `LSETDT`, but not `END_DCEN`, `END_XCEN`, and `END_YCEN` ("MHP 10/24 ADDED STOP CRITERIA," [[#L32]]), per-run arrays in `NMLPAR_MOD` ([[nmlpar_mod.f#L261-L263]]) that the main program reads for each run ([[main.f#L430-L459]]; [[main.f#L1089-L1115]]). What follows: In a calibration with such a stop set for run 2 or 3, only run 2 (or 3) itself stops at it; its repetitions, runs 5 to 47 (or 6 to 48), run to their end ages. [[setscal.f#SETSCAL|SETSCAL]] has the same omission ([[setscal.f#L131-L139]]). Only with `LCALS` and a stop criterion set for run 2 or 3.

    **A possible fix:**

    ```diff
    --- a/src/setcal.f
    +++ b/src/setcal.f
    @@ -88,6 +88,11 @@
              LENDAG(I) = LENDAG(2)
              SETDT(I) = SETDT(2)
              LSETDT(I) = LSETDT(2)
    +C 11/10/26 KC via Claude
    +C code changed to copy the stop criteria of run 2 too.
    +         END_DCEN(I) = END_DCEN(2)
    +         END_XCEN(I) = END_XCEN(2)
    +         END_YCEN(I) = END_YCEN(2)
           END DO
           DO I = 6,48,3
              IRESCA(I) = 1
    @@ -97,6 +102,11 @@
              LENDAG(I) = LENDAG(3)
              SETDT(I) = SETDT(3)
              LSETDT(I) = LSETDT(3)
    +C 11/10/26 KC via Claude
    +C code changed to copy the stop criteria of run 3 too.
    +         END_DCEN(I) = END_DCEN(3)
    +         END_XCEN(I) = END_XCEN(3)
    +         END_YCEN(I) = END_YCEN(3)
           END DO
           LSOL = .FALSE.
           RETURN
    ```

    **Checked by running YREC** (Nov 10, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): SETCAL ran once, in YREC's one calibration case, `examples/run_standard_solar_model/Test_solarcal_noGS_norot` (`NUMRUN` = 48 after it), and no `END_DCEN`, `END_XCEN`, or `END_YCEN` was set for run 2 or 3: A line counting any nonzero one never fired, so copying them would change nothing. The fix was not run. What would reach it: a calibration (`LCALS`) with one of these stops set for run 2 or 3, which no case of YREC's sets. Intent: none found.
