## Explanation

**Purpose.** `WRTHEAD` writes the header lines of the output files at the start of each run of a job: a line describing the run in the main output, and the track file's column header.

**How it fits.**
- **Inputs:** the arguments, the stellar mass `SMASS` (solar masses), the mixing length `CMIXL` and the run index `NK`; and through modules: the run's kind `IRESCA(NK)` (`RUNLOOP_MOD`, formerly `CKIND`), its number of models `NMODLS(NK)` and `LFIRST(NK)` (`NMLPAR_MOD`, namelist settings), the initial $X$ and $Z$ (`XENV0`, `ZENV0` in `LABEL_MOD`), the namelist switch `LTRACK` and the track format's version `ITRVER` (`NMLPAR_MOD`, `ITRVER` 1 by default; read by [[parmin.f#PARMIN|PARMIN]]), and the units `IOWR`, `ITRACK` (`IOUNITS_MOD`).
- **Who calls it:** the main program, [[main.f#(file level)|main.f]], once per run.
- **Outputs:** a line on `IOWR` ("RUN= … EVOLVE", "RESCALE" or "RESCALE&EVOLVE"); with `LTRACK`, for a run that reads its starting model (`LFIRST(NK)`), a version line and the column names on `ITRACK`. The data lines under these headers are written by [[wrtout.f#WRTOUT|WRTOUT]], which must match them.

**Design.** The column names depend on `ITRVER`: 0, one long line of names (G. Somers 11/14); 1, a description in comment lines (except two lines of format 1505, " Neutrinos …" and '    "        " cont: …', which do not start with `#`); 2, the same plus the rotation columns (whose line, format 1510, does not start with `#` either); 3, a short list.

**Changed since `rp_1`.** `CMIXL` and `NK` are now arguments (from the main program) instead of COMMON members; the isochrone header (the `LISO` option, on `IISO`) is removed with the option; declarations: COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **The comment and the active code.** For `ITRVER = 0`, the comment says "Uncomment the following block if desired", but the block that follows is commented out and a second version (format 1504) is active. Which is current?
2. **The column line is not a comment.** In format 1504, the line of column names does not start with `#`, unlike the lines around it, so a reader that skips `#` lines reads it as data. Intended, as a header row? The same holds for two lines of format 1505 (" Neutrinos …" and '    "        " cont: …', `ITRVER` = 1 and 2) and the rotation line of format 1510 (`ITRVER` = 2).
3. **Matching `WRTOUT`.** The headers must agree with the data `WRTOUT` writes, but nothing checks it: a change to one needs a change to the other and to `ITRVER` (the comment asks for this).

### WRTHEAD

Writes the run line and the track file's header (by version `ITRVER`).
