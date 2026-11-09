## Explanation

**Purpose.** `WRTHEAD` writes the header lines of the output files at the start of each run of a job: a line describing the run in the main output, and the track file's column header.

**How it fits.**
- **Inputs:** the arguments, the stellar mass `SMASS` (solar masses), the mixing length `CMIXL` and the run index `NK`; and through modules: the run's kind `IRESCA(NK)` (`RUNLOOP_MOD`, formerly `CKIND`), its number of models `NMODLS(NK)` and `LFIRST(NK)` (`NMLPAR_MOD`, namelist settings), the initial $X$ and $Z$ (`XENV0`, `ZENV0` in `LABEL_MOD`), the namelist switch `LTRACK` and the track format's version `ITRVER` (`NMLPAR_MOD`, `ITRVER` 1 by default; read by [[parmin.f#PARMIN|PARMIN]]), and the units `IOWR`, `ITRACK` (`IOUNITS_MOD`).
- **Who calls it:** the main program, [[main.f#(file level)|main.f]], once per run.
- **Outputs:** a line on `IOWR` ("RUN= … EVOLVE", "RESCALE" or "RESCALE&EVOLVE"); with `LTRACK`, for a run that reads its starting model (`LFIRST(NK)`), a version line and the column names on `ITRACK`. The data lines under these headers are written by [[wrtout.f#WRTOUT|WRTOUT]], which must match them.

**Design.** The column names depend on `ITRVER`: 0, one long line of names (G. Somers 11/14); 1, a description in comment lines (except two lines of format 1505, " Neutrinos …" and '    "        " cont: …', which do not start with `#`); 2, the same plus the rotation columns (whose line, format 1510, does not start with `#` either); 3, a short list. For `ITRVER` = 0 the 83 names of format 1504 match, in number and order, the 83 values that [[wrtout.f#WRTOUT|WRTOUT]] writes with format 1499; nothing in the code checks this, and the comment asks that `ITRVER` change whenever the track file does ([[#L89-L90]]) (settled from the code, Nov 9, 2026: [[#L131-L148]]; [[wrtout.f#L558-L568]]). The headers of versions 1–3 do not match their data (bug 1).

> **Question** ([[#L112-L114]]; [[#L115-L131]]). **The comment and the active code.** For `ITRVER = 0`, the comment says "Uncomment the following block if desired", but the block that follows is commented out and a second version (format 1504) is active. Which is current, and can the comment and the commented-out format go?

> **Question** ([[#L131-L148]]). **The column line is not a comment.** In format 1504, the line of column names does not start with `#`, unlike the lines around it, so a reader that skips `#` lines reads it as data. Is it intended, as a header row for readers that take the column names from the file?

**For users** (from YREC's [User Guide](https://yrec.readthedocs.io/en/latest/userguide.html)). The track file is the run's history, one line per model with `ITRVER` = 0, the format recommended. The two lines of `DESCRIP` in the control namelist, the run's description, head the track file too, but [[parmin.f#PARMIN|`PARMIN`]] writes them, before this header.

**From YREC's documentation.** [Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html): `ITRVER` chooses the format of the `.track` file; 0 (one line per model) is strongly recommended, though the default is 1.

**Changed since `rp_1`.** `CMIXL` and `NK` are now arguments (from the main program) instead of COMMON members; the isochrone header (the `LISO` option, on `IISO`) is removed with the option; declarations: COMMON blocks to modules, `IMPLICIT NONE`.

## Bugs, by priority

1. **(c)** **The headers of track versions 1, 2, and 3 do not match the data.** ([[#L152-L176]]; [[wrtout.f#L570-L641]]) For `ITRVER` = 1 (the default) and 2, WRTOUT writes for each model: a first line of 14 values whose last five are the base of the convection zone (`CZsurf_R`, `CZsurf_T`, `CZsurf_D`, `CZsurf_P`, `CZsurf_O`; [[wrtout.f#L570-L572]]), which format 1505 does not name; a central line whose ninth value is the total moment of inertia `HITOT` ([[wrtout.f#L573-L575]]), not named; a neutrino line of the Cl and Ga rates and 10 fluxes ([[wrtout.f#L587-L588]]), where the header names 8 fluxes and no rates; and a second surface line of H2, Li6, Li7, Be9, X, Y, Z, and Z/X ([[wrtout.f#L591-L593]]), where the header names the first four. For version 2 the rotation line has nine values (`SJTOT`, `SKEROT`, `HITOT`, `HICZ`, Ω at the surface and center, `ROTP`, `ROTV`, `TAUCZ`; [[wrtout.f#L632-L634]]), where format 1510 names four. For version 3 the tenth value is `CZsurf_R` ([[wrtout.f#L639-L641]]), where format 1515 says "% Grav Energy" (the line that computed it is commented out, [[wrtout.f#L637-L638]]). And three header lines do not start with `#` ([[#L158-L159]]; [[#L164]]; [[#L171]]), so a reader that skips `#` lines takes them for data. What follows: a user who reads a track of version 1, 2, or 3 by its header assigns columns wrongly; the run itself is not affected. On by default (`LTRACK` true and `ITRVER` 1: [[nmlpar_mod.f#L59]]; [[nmlpar_mod.f#L142]]), though the documentation recommends version 0. Read from the code, not run. **A possible fix** (the comment at [[#L89-L90]] may also call for a new `ITRVER`):

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to make the headers of ITRVER = 1, 2 and 3 name the
    C columns WRTOUT writes, each line starting with '#'.
     1505       FORMAT(
         1'# Model #, shells, AGE, log(L/Lsun), log(R/Rsun), log(g),',
         1' log(Teff), Mconv. core, Mconv. env.; CZ base: R, T, Rho,',
         1' P, kappa',/,
         2'# Central: log(T), log(RHO), log(P), BETA, ETA, X, Y, Z,',
         2' total I',/,
         3'# Luminosity: ppI, ppII, ppIII, CNO, triple-alpha,',
         3' He-C, gravity, neutrinos (old)',/,
         3'# Cl SNU, Ga SNU, Neutrinos (1E10/CM^2/S at earth): pp,',
         3' pep, hep, Be7, B8, N13, O15, F17, diag1, diag2',/,
         4'# Central Abundances: He3, C12, C13, N14, N15, O16,',
         4' O17, O18',/,
         5'# Surface Abundances: He3, C12, C13, N14, N15, O16,',
         5' O17,O18',/,
         6'#    "        " cont: H2, Li6, Li7, Be9, X, Y, Z, Z/X',/,
         7'# H shell loc: mass frac-base, midpoint, top; radius frac-',
         7'base, midpoint, top')
    ...
     1510       FORMAT(
         1'# Jtot, K.E. Rotation, total I, CZ I, OMEGAsurf,',
         1' OMEGAcenter, Prot (days), Vrot (km/s), TauCZ (s)')
    ...
     1515       FORMAT(
         1'#Model #, shells, AGE, log(L/Lsun), log(R/Rsun), log(g),',
         1' log(Teff), Mconv. core, Mconv. env., R CZ base, X env')
    ```

### WRTHEAD

Writes the run line and the track file's header (by version `ITRVER`).
