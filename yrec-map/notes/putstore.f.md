## Explanation

**Purpose.** Writes a verbose stellar model to the `.store` file (`ISTOR`), "either at specified ages, every NPRTMOD models, or at the end of runs." Its header (G. Somers 11/14) calls it "mostly a clone of wrtlst.f and putmodel2.f, combined." Since JvS 09/25 it has two formats: the older one (a MODEL2-style model followed by optional per-shell physics and rotation columns) and, with `LSTCH`, the "stitched" format, in which [[stitch.f#STITCH|STITCH]] writes interior, envelope and atmosphere points together.

**How it fits.**
- **Inputs:** the model as arguments (structure, composition, envelope data, luminosities `TLUMX`, rotation: `OMEGA`, `ETA2`, `R0`, `FP`, `FT`, `HJM`, `HI`), the mixing length `CMIXL`, `XMSOL` (passed on to `WRTMOD`) and the initial-mixture label `COMPMIX` (from [[starin.f#STARIN|STARIN]], through the main program); the physics flags and the output switches (`LSTORE`, `LSTATM`, `LSTENV`, `LSTMOD`, `LSTPHYS`, `LSTROT`, `LSTCH`, `LMILNE`) from [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]], and `LPHHD` from [[ccout_mod.f#CCOUT_MOD|`CCOUT_MOD`]]; the per-shell physics in [[scrtch_mod.f#SCRTCH_MOD|`SCRTCH_MOD`]], [[sound_mod.f#SOUND_MOD|`SOUND_MOD`]] (`GAM1`), [[temp2_mod.f#TEMP2_MOD|`TEMP2_MOD`]] (the rotational mixing velocities) and [[roten_mod.f#ROTEN_MOD|`ROTEN_MOD`]]; the constants from [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]] and the units from [[iounits_mod.f#IOUNITS_MOD|`IOUNITS_MOD`]].
- **Who calls it:** [[wrtout.f#WRTOUT|WRTOUT]] and the main program in [[main.f|main.f]].
- **What it calls:** [[stitch.f#STITCH|STITCH]] (new format), [[pindex.f#PINDEX|PINDEX]] (which shells to print), [[wrtmil.f#WRTMIL|WRTMIL]] (if also `LMILNE`) and [[wrtmod.f#WRTMOD|WRTMOD]] (envelope and atmosphere, if `LSTATM` or `LSTENV`).
- **Output:** the `.store` file, opened by [[parmin.f#PARMIN|PARMIN]] (which also writes the old format's header key). Its `MOD2` blocks can serve as starting models ([[starin.f#STARIN|STARIN]] reads the `MOD2` format).

**The method.**
1. **Labels** for the physics: atmosphere (`EDD`, `KS`, `HRA`, `KUR`, `ALL` from `KTTAU`; `KTTAU` = 5 gets none, bug 2), equation of state (`SAHA`, `OPAL06`, `SCV`, with `+DH` and OPAL 2006; `SCV+O6` is never written, bug 1), low-temperature opacity (always `NONE`: the labels `ALEX` and `KURZ` went with the Alexander 1995 and Kurucz 1990 tables) and high-temperature opacity (`OP95`, or `NONE`). The message for the label `' ? '` ([[#L176-L180]]) is never written, since no branch sets that label (settled from the code, Nov 9, 2026).

    > **Question** ([[#L164-L169]]). **No low-temperature opacity label.** With the Alexander 1995 and Kurucz 1990 tables removed, `ALOK` is always `NONE`: the Ferguson et al. (2005) tables (`LALEX06`), the only low-temperature tables left, were never labelled. Should `LALEX06` set `ALOK` (for example to `AL06`)?

2. **Stitched format** (`LSTCH`): on the first call (`LPHHD`) a header key, the flags line and the column titles; then `STITCH` (with `CMIXL`).
3. **Old format:** the `MOD2` header line, the flags, the `TLUMX` line (converted to erg s⁻¹ in place if the largest is $\le 10^{20}$, as in [[putmodel2.f#PUTMODEL2|PUTMODEL2]], whose in-place conversion is [[putmodel2.f#b1]]), three `ENV` lines; then, with `LSTMOD`, one line per shell selected by [[pindex.f#PINDEX|PINDEX]] (whose burning-shell arguments are never set, bug 3): the basic columns, led by the model number; with `LSTPHYS` opacity, gravity $g = Gm/r^2$, $\nabla_\mathrm{rad}$, $\nabla$, $\nabla_\mathrm{ad}$, convective velocity, $\Gamma_1$, `SBETA`, `SETA` and the energy generation terms; with `LSTROT` (and `LROT`) the distortion parameter and the ratio of polar to equatorial radius,
$$A = \frac{5}{3}\,\frac{\Omega^2 r_0^3}{G m\,(2+\eta_2)},\qquad \frac{R_p}{R_e} = \frac{1 - A}{1 + A/2},$$
where $A$ is the amplitude of the $P_2$ distortion of the level surface, $r(\theta) = r_0\,[1 - A\,P_2(\cos\theta)]$, in the Clairaut–Radau treatment of [[fpft.f#FPFT|FPFT]] and [[shape.f#SHAPE|SHAPE]] (Kippenhahn & Thomas 1970): $P_2 = 1$ at the pole and $-\tfrac12$ at the equator, hence $r_0(1 - A)$ and $r_0(1 + A/2)$; then `FP`, `FT`, $j$, $I$, the rotational kinetic energy change, and the mixing velocities $v_\mathrm{ES}$, $v_\mathrm{GSF}$, $v_\mathrm{SS}$ and their sum. Missing groups are written as zeros. The fifth energy column, `SEG(5,·)`, is the triple-α term: COEFFT stores in it `EG(5)`, ENGEB's `E3AL` ([[coefft.f#L286-L296]]; [[coefft.f#L433-L435]]; [[engeb.f#L1125-L1127]]), as the stitched header's "TRIPLE_ALPHA" says; the old header's "3HE" is wrong (bug 4) (settled from the code, Nov 9, 2026).

    > **Question** ([[#L307-L312]]). **Ionization fractions written as zeros.** The columns HII, HEII, HEIII are written as 0.0 (the line with `SFXION` is commented out), although COEFFT fills `SFXION` for every shell ([[coefft.f#L450]]) and [[stitch.f#STITCH|STITCH]] writes it ([[stitch.f#L117-L120]]). Is that intended?

    > **Question** ([[#L133-L174]]; [[#L213-L251]]). **Duplicated code.** The labels, the `MOD2` header, and the `TLUMX` conversion repeat [[putmodel2.f#PUTMODEL2|PUTMODEL2]] and [[wrtlst.f#WRTLST|WRTLST]], and the copies have already drifted (`KTTAU` = 5 is labelled in WRTLST, not here). Should one routine be shared?


**For users** (from YREC's [Quick Start](https://yrec.readthedocs.io/en/latest/quickstart.html)). This is the `.store` file (`FSTOR`): snapshots of the model's structure during the run. Which snapshots, and what they contain, the control namelist decides: `LSTORE` (`NPRTMOD`, every how many models; `NPRTPT`, every how many shells), `LSTPCH` (the final model), and `LSTATM`, `LSTENV`, `LSTPHYS`, `LSTROT` (the atmosphere, the envelope, the microphysics, the rotation), with `LSTCH` for the stitched format.

**From YREC's documentation.** [Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html) (Output):

| variable | meaning (documentation) |
| --- | --- |
| `LSTORE` | store model structures to the `.store` file at the chosen points (`LSTMOD` should be set the same; it may be redundant) |
| `LSTCH` | write interior, envelope and atmosphere in one consistent format (recommended) |
| `LSTATM`, `LSTENV` | add the atmosphere, the envelope; with both off nothing beyond the fitting point is written |
| `LSTPHYS` | add the microphysics ($\epsilon$, $\kappa$, …) |
| `LSTROT` | add the rotation data |
| `LSTPCH` | write the final model's details |

**Changed since `rp_1`.** `CMIXL`, `XMSOL` and `COMPMIX` are new arguments (`COMPMIX` was `/I2O/`, `CMIXL` was in `/CONST3/`), passed on: `CMIXL` to `STITCH`, both to `WRTMOD`; the labels of the removed options (the OPAL 1995 and 2001 equations of state, the OPAL92, LAOL89, Alexander 1995 and Kurucz 1990 opacities) are gone; each shell's line now starts with the model number, which fixes a crash (format 62 already expected it), and formats 62 and 63 put spaces between some columns; `LMILNE` now comes from `NMLPAR_MOD` (bug fix), so `WRTMIL` is called when it is set, which settles former question 2; COMMON blocks to modules (eleven unused blocks dropped), `IMPLICIT NONE`.

## Bugs, by priority

1. **(never occurred)** **The SCV + OPAL 2006 label is lost.** ([[#L149-L157]]) In the `LSCV` branch, `IF (LOPALE06) EOS='SCV+O6'` sits inside `IF (LDH)`, where it is overwritten at once; without `LDH`, SCV with OPAL 2006 is labelled `SCV` in the flags line of both formats. Only with `LSCV` and `LOPALE06` on and `LDH` off. The same lines are in [[wrtlst.f#WRTLST|WRTLST]] ([[wrtlst.f#b1]]).

    **A possible fix:**

    ```diff
    --- a/src/putstore.f
    +++ b/src/putstore.f
    @@ -146,12 +146,15 @@
     C Determine equation of state flag, EOS
           EOS='SAHA  '
           IF (LDH) EOS='SAH+DH'
    +C 11/09/26 KC via Claude
    +C code changed to label SCV with OPAL 2006 and without Debye-Huckel
    +C SCV+O6; the test sat inside IF (LDH), where it was overwritten.
           IF (LSCV) THEN
              EOS='SCV   '
     C 9/24/26 MHP via Claude
     C code changed to remove the OPAL 1995/2001 equations of state
    -         IF (LDH) THEN
              IF (LOPALE06) EOS='SCV+O6'
    +         IF (LDH) THEN
                 EOS='SCV+DH'
                 IF (LOPALE06) EOS='SCDHO6'
              ENDIF
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The `LSCV` branch ran in 30 of 34 runs: 26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones, but the setting that goes wrong, SCV with OPAL 2006 and without `LDH`, held in none: YREC's cases that use SCV with OPAL 2006 also set `LDH`. Any of them with `LDH` off would reach it. The fix was not run. Intent: none found; the misplaced line is already in the first commit of the history (Apr 10, 2025), indented at the level of `IF (LDH)`, as if pasted one line low.

2. **(wrong output)** **Checked by KC** (Nov 10, 2026). **Atmosphere 5 has no label.** ([[#L135-L145]]) `KTTAU = 5` (Kurucz/Castelli, JNT 6/14) has no branch, so `ATM` keeps its value from the previous call (it is `SAVE`d) or, at the first call, is undefined, and that is written to the `.store` file's flags line. WRTLST has the branch ([[wrtlst.f#L103-L105]]). Only with `KTTAU` = 5 (the default is 0) and `LSTORE`.

    **A possible fix:**

    ```diff
    --- a/src/putstore.f
    +++ b/src/putstore.f
    @@ -142,6 +142,10 @@
              ATM='KUR '
           ELSEIF (KTTAU .EQ. 4) THEN
              ATM='ALL '
    +C 11/09/26 KC via Claude
    +C code changed to label the Kurucz/Castelli atmosphere, as WRTLST does.
    +      ELSEIF (KTTAU .EQ. 5) THEN
    +         ATM='K/C '
           ENDIF
     C Determine equation of state flag, EOS
           EOS='SAHA  '
    ```

    **How the outputs show it.** In the made-up run (`testsuite/Test_solarGS98_kurucz` with `KTTAU` = 5 and `FATM` = `atmos/CastelliKurucz/atmk2004p00.tab`), the `.store` file's flags line, written once, at the first store (model 23; [[#L189-L192]]), holds four NUL bytes in the ATM column, between "SCDHO6" and "NONE": `ATM` was never set. The `.last` file, written at the last model (1224) by WRTLST ([[wrtlst.f#L103-L105]]) through PUTMODEL2 ([[putmodel2.f#L80]]), gives "K/C" in the same column.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): YREC's `testsuite/Test_solarGS98_kurucz`, run with `KTTAU` = 5 and `FATM` = `atmos/CastelliKurucz/atmk2004p00.tab`, as the README of those tables asks ("You NEED TO CHANGE KTTAU to 5," `input/atmos/CastelliKurucz/README`, line 15), reaches it at both of its stores (models 23 and 1000), so `ATM` was written without a value of its own. With the fix, the track is identical and the harness finds the `.store` file within 2%; the null change moves $\log L$ by up to 0.000144 dex. The harm is the label, which the fix corrects. Intent: none found; [[wrtlst.f#WRTLST|WRTLST]] got the branch ("JNT 06/14"), and PUTSTORE, written later (G Somers, 11/14), lacks it.

3. **(never occurred)** **Checked by KC** (Nov 10, 2026). **`PINDEX` gets arguments that are never set.** ([[#L51-L52]]; [[#L262]]) `JXBEG`, `JXEND`, and `LSHELL` are neither arguments nor in a module here, so they are undefined locals (zero and `.FALSE.` with a compiler that zero-initializes `SAVE`d locals). The burning-shell option of [[pindex.f#PINDEX|PINDEX]], which prints every shell of the hydrogen-burning shell ([[pindex.f#L46-L70]]), therefore never applies, and the old format prints only every `NPRTPT`-th shell there. Only in the old format (`LSTCH` off) with `LSTMOD`, and with `NPRTPT` above 1 (its default is 1, [[nmlpar_mod.f#L169]], kept by every case of YREC's that writes the old format).

    **A possible fix:** pass `LSHELL`, `JXBEG`, and `JXEND` to PUTSTORE as arguments, from WRTOUT (which has them as arguments) and from the main program (which sets them through FINDSH, [[main.f#L578-L579]]), as they were passed to WRTMOD in the commented-out call ([[#L344-L346]]). The branch this reaches has two fragile points of its own ([[pindex.f#b1]]; [[pindex.f#b2]]).

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): PINDEX got `JXBEG` = `JXEND` = 0 and `LSHELL` false at every call, in the 14 runs that write the old format. In 10 of them, the callers' `LSHELL` was true at a store, with the shell between points 26 and 2830. But no shell went unlisted: Every case of YREC's that writes the old format keeps `NPRTPT` at 1 (its default, [[nmlpar_mod.f#L169]]), and with 1, PINDEX's general branch lists every shell, 2 to M−1 and then M ([[pindex.f#L73-L84]]); `testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS` lists all 748 shells of its model 921 once, and `testsuite/Test_m0p95feh+0p0_GN93_TAHB` all 3,268 and 3,425 shells of its models 0 and 943 (rechecked on Nov 10). The run with the fix differs, but not because of this bug: Its track is identical, and only the `.store` file changes beyond 2% (the null change moves $\log L$ by up to 1.67e-7 dex in the first case). With `LSHELL` passed, PINDEX takes its shell branch, which with `NPRTPT` = 1 also lists every shell once (loops 10, 20, and 30, [[pindex.f#L46-L72]]) and then lists `M` a second time ([[pindex.f#L83]]): That is PINDEX's own suspected bug, `M` listed twice ([[pindex.f#b2]]), which nothing reaches today and this fix would. So this fix should go with that one. The bug itself shows only with `NPRTPT` above 1, which no case of YREC's sets. Intent: The commented-out call to WRTMOD ([[#L344-L346]]) passed these three; nothing says they were dropped on purpose.

4. **(wrong output)** **Checked by KC** (Nov 10, 2026). **The old header calls the triple-α column "3HE."** ([[#L275]]; [[#L309]]) The fifth energy column, `SEG(5,I)`, is the triple-α term (Explanation, step 3), as the stitched format's header says ([[#L208]]). What follows: a misleading column name in the old `.store` format. Only with `LSTORE`, `LSTMOD`, and `LSTPHYS`, and `LSTCH` off.

    **A possible fix:**

    ```diff
    --- a/src/putstore.f
    +++ b/src/putstore.f
    @@ -272,7 +272,10 @@
          1'    O17             O18             H2              Li6             Li7',
          1'             Be9           OPAC       GRAV        DELR        DEL      ',
          1'   DELA       V_CONV     GAM1      HII     HEII     HEIII    BETA      ',
    -     1'ETA       PPI         PPII       PPIII        CNO         3HE         ',
    +C 11/09/26 KC via Claude
    +C code changed to name the fifth energy column for the triple-alpha
    +C term it holds, as FORMAT 1014 does.
    +     1'ETA       PPI         PPII       PPIII        CNO         3ALPHA      ',
          1'E_NUC        E_NEU       E_GRAV          A           RP/RE           FP',
          1'            FT           J/M          MOMENT        DEL_KE       V_ES ',
          1'      V_GSF      V_SS       VTOT   ',/)
    ```

    **How the outputs show it.** In `testsuite/Test_m0p95feh+0p0_GN93_TAHB`, at model 943, the `.store` file's column headed "3HE" ([[#L275]]) is 0.1000E+01 at the center, where the core burns helium. This column's fractions of E_NUC, summed over the masses of all 3,425 shells, give 3.083 $L_\odot$ (with the case's `CLSUN` of 3.828×10³³ erg s⁻¹), and the `.track` gives the same model's triple-α luminosity, 3a_lsun ([[wrtout.f#L558]]), as 3.08298493E+000. At model 0 the two are 16.16 and 1.61768489E+001. The column is the triple-α term, as the stitched header says ([[#L208]]).

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The header was written with the physics columns in the same 14 runs. With the fix, `examples/run_from_dbl_to_zams/Test_m0040_feh0_noGS_ZAMS` gives an identical track and a `.store` file within 2%, and `examples/run_standard_solar_model/Test_solarcal_noGS_norot` differs exactly as for the null change ($\log L$ by up to 0.000322 dex): within the noise, as expected for a label. The harm is the label, which the fix corrects. Intent: none found; the stitched format's header names the column TRIPLE_ALPHA ([[#L208]]).
