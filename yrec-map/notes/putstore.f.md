## Explanation

**Purpose.** Writes a verbose stellar model to the `.store` file (`ISTOR`), "either at specified ages, every NPRTMOD models, or at the end of runs." Its header (G. Somers 11/14) calls it "mostly a clone of wrtlst.f and putmodel2.f, combined." Since JvS 09/25 it has two formats: the older one (a MODEL2-style model followed by optional per-shell physics and rotation columns) and, with `LSTCH`, the "stitched" format, in which [STITCH](stitch.f.md#stitch) writes interior, envelope and atmosphere points together.

**How it fits.**
- **Inputs:** the model as arguments (structure, composition, envelope data, luminosities `TLUMX`, rotation: `OMEGA`, `ETA2`, `R0`, `FP`, `FT`, `HJM`, `HI`), the mixing length `CMIXL`, `XMSOL` (passed on to `WRTMOD`) and the initial-mixture label `COMPMIX` (from [STARIN](starin.f.md#starin), through the main program); the physics flags and the output switches (`LSTORE`, `LSTATM`, `LSTENV`, `LSTMOD`, `LSTPHYS`, `LSTROT`, `LSTCH`, `LMILNE`) from [`NMLPAR_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/nmlpar_mod.f#L32-L279), and `LPHHD` from [`CCOUT_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/ccout_mod.f#L19-L26); the per-shell physics in [`SCRTCH_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/scrtch_mod.f#L19-L39), [`SOUND_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/sound_mod.f#L19-L31) (`GAM1`), [`TEMP2_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/temp2_mod.f#L19-L37) (the rotational mixing velocities) and [`ROTEN_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/roten_mod.f#L19-L30); the constants from [`CONSTANTS_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/constants_mod.f#L37-L75) and the units from [`IOUNITS_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/iounits_mod.f#L19-L54).
- **Who calls it:** [WRTOUT](wrtout.f.md#wrtout) and the main program in [main.f](main.f.md).
- **What it calls:** [STITCH](stitch.f.md#stitch) (new format), [PINDEX](https://github.com/yreclab/yrec/blob/7be4133/src/pindex.f#L6-L85) (which shells to print), [WRTMIL](wrtmil.f.md#wrtmil) (if also `LMILNE`) and [WRTMOD](wrtmod.f.md#wrtmod) (envelope and atmosphere, if `LSTATM` or `LSTENV`).
- **Output:** the `.store` file, opened by [PARMIN](https://github.com/yreclab/yrec/blob/7be4133/src/parmin.f#L16-L1489) (which also writes the old format's header key). Its `MOD2` blocks can serve as starting models ([STARIN](starin.f.md#starin) reads the `MOD2` format).

**The method.**
1. **Labels** for the physics: atmosphere (`EDD`, `KS`, `HRA`, `KUR`, `ALL` from `KTTAU`; `KTTAU` = 5 gets none, bug 2), equation of state (`SAHA`, `OPAL06`, `SCV`, with `+DH` and OPAL 2006; `SCV+O6` is never written, bug 1), low-temperature opacity (always `NONE`: the labels `ALEX` and `KURZ` went with the Alexander 1995 (the code's name for the tables of Alexander & Ferguson [1994](https://ui.adsabs.harvard.edu/abs/1994ApJ...437..879A)) and Kurucz 1990 (the code's name; probably the opacities of Kurucz [1991](https://ui.adsabs.harvard.edu/abs/1991ASIC..341..441K), “New Opacity Calculations”) tables) and high-temperature opacity (`OP95`, or `NONE`). The message for the label `' ? '` ([lines 176–180](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L176-L180)) is never written, since no branch sets that label (settled from the code, Nov 9, 2026).

    > **Question** ([lines 164–169](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L164-L169)). **No low-temperature opacity label.** With the Alexander 1995 and Kurucz 1990 tables removed, `ALOK` is always `NONE`: the Ferguson et al. ([2005](https://ui.adsabs.harvard.edu/abs/2005ApJ...623..585F)) tables (`LALEX06`), the only low-temperature tables left, were never labelled. Should `LALEX06` set `ALOK` (for example to `AL06`)?

2. **Stitched format** (`LSTCH`): on the first call (`LPHHD`) a header key, the flags line and the column titles; then `STITCH` (with `CMIXL`).
3. **Old format:** the `MOD2` header line, the flags, the `TLUMX` line (converted to $`\mathrm{erg\,s^{-1}}`$ in place if the largest is $`\le 10^{20}`$, as in [PUTMODEL2](https://github.com/yreclab/yrec/blob/7be4133/src/putmodel2.f#L7-L131), whose in-place conversion is [putmodel2.f, suspected bug 1](putmodel2.f.md#b1)), three `ENV` lines; then, with `LSTMOD`, one line per shell selected by [PINDEX](https://github.com/yreclab/yrec/blob/7be4133/src/pindex.f#L6-L85) (whose burning-shell arguments are never set, bug 3): the basic columns, led by the model number; with `LSTPHYS` opacity, gravity $`g = Gm/r^2`$, $`\nabla_\mathrm{rad}`$, $`\nabla`$, $`\nabla_\mathrm{ad}`$, convective velocity, $`\Gamma_1`$, `SBETA`, `SETA` and the energy generation terms; with `LSTROT` (and `LROT`) the distortion parameter and the ratio of polar to equatorial radius,
   
   $$\displaystyle A = \frac{5}{3}\\,\frac{\Omega^2 r\_0^3}{G m\\,(2+\eta\_2)},\qquad \frac{R\_p}{R\_e} = \frac{1 - A}{1 + A/2},$$
   
   where $`A`$ is the amplitude of the $`P_2`$ distortion of the level surface, $`r(\theta) = r_0\,[1 - A\,P_2(\cos\theta)]`$, in the Clairaut–Radau treatment of [FPFT](fpft.f.md#fpft) and [SHAPE](https://github.com/yreclab/yrec/blob/7be4133/src/shape.f#L2-L170) (Kippenhahn & Thomas [1970](https://ui.adsabs.harvard.edu/abs/1970stro.coll...20K)): $`P_2 = 1`$ at the pole and $`-\tfrac12`$ at the equator, hence $`r_0(1 - A)`$ and $`r_0(1 + A/2)`$; then `FP`, `FT`, $`j`$, $`I`$, the rotational kinetic energy change, and the mixing velocities $`v_\mathrm{ES}`$, $`v_\mathrm{GSF}`$, $`v_\mathrm{SS}`$ and their sum. Missing groups are written as zeros. The fifth energy column, `SEG(5,·)`, is the triple-$`\alpha`$ term: COEFFT stores in it `EG(5)`, ENGEB's `E3AL` ([coefft.f, lines 286–296](https://github.com/yreclab/yrec/blob/7be4133/src/coefft.f#L286-L296); [coefft.f, lines 433–435](https://github.com/yreclab/yrec/blob/7be4133/src/coefft.f#L433-L435); [engeb.f, lines 1125–1127](https://github.com/yreclab/yrec/blob/7be4133/src/engeb.f#L1125-L1127)), as the stitched header's "TRIPLE_ALPHA" says; the old header's "3HE" is wrong (bug 4) (settled from the code, Nov 9, 2026).

    > **Question** ([lines 307–312](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L307-L312)). **Ionization fractions written as zeros.** The columns HII, HEII, HEIII are written as 0.0 (the line with `SFXION` is commented out), although COEFFT fills `SFXION` for every shell ([coefft.f, line 450](https://github.com/yreclab/yrec/blob/7be4133/src/coefft.f#L450)) and [STITCH](stitch.f.md#stitch) writes it ([stitch.f, lines 117–120](https://github.com/yreclab/yrec/blob/7be4133/src/stitch.f#L117-L120)). Is that intended?

    > **Question** ([lines 133–174](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L133-L174); [lines 213–251](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L213-L251)). **Duplicated code.** The labels, the `MOD2` header, and the `TLUMX` conversion repeat [PUTMODEL2](https://github.com/yreclab/yrec/blob/7be4133/src/putmodel2.f#L7-L131) and [WRTLST](wrtlst.f.md#wrtlst), and the copies have already drifted (`KTTAU` = 5 is labelled in WRTLST, not here). Should one routine be shared?


**For users** (from YREC's [Quick Start](https://yrec.readthedocs.io/en/latest/quickstart.html)). This is the `.store` file (`FSTOR`): snapshots of the model's structure during the run. Which snapshots, and what they contain, the control namelist decides: `LSTORE` (`NPRTMOD`, every how many models; `NPRTPT`, every how many shells), `LSTPCH` (the final model), and `LSTATM`, `LSTENV`, `LSTPHYS`, `LSTROT` (the atmosphere, the envelope, the microphysics, the rotation), with `LSTCH` for the stitched format.

**From YREC's documentation.** [Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html) (Output):

| variable | meaning (documentation) |
| --- | --- |
| `LSTORE` | store model structures to the `.store` file at the chosen points (`LSTMOD` should be set the same; it may be redundant) |
| `LSTCH` | write interior, envelope and atmosphere in one consistent format (recommended) |
| `LSTATM`, `LSTENV` | add the atmosphere, the envelope; with both off nothing beyond the fitting point is written |
| `LSTPHYS` | add the microphysics ($`\epsilon`$, $`\kappa`$, …) |
| `LSTROT` | add the rotation data |
| `LSTPCH` | write the final model's details |

**Changed since `rp_1`.** `CMIXL`, `XMSOL` and `COMPMIX` are new arguments (`COMPMIX` was `/I2O/`, `CMIXL` was in `/CONST3/`), passed on: `CMIXL` to `STITCH`, both to `WRTMOD`; the labels of the removed options (the OPAL 1995 and 2001 equations of state, the OPAL92, LAOL89, Alexander 1995 and Kurucz 1990 opacities) are gone; each shell's line now starts with the model number, which fixes a crash (format 62 already expected it), and formats 62 and 63 put spaces between some columns; `LMILNE` now comes from `NMLPAR_MOD` (bug fix), so `WRTMIL` is called when it is set, which settles former question 2; COMMON blocks to modules (eleven unused blocks dropped), `IMPLICIT NONE`.

## Bugs, by priority

1. **(never occurred)** **The SCV + OPAL 2006 label is lost.** ([lines 149–157](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L149-L157)) In the `LSCV` branch, `IF (LOPALE06) EOS='SCV+O6'` sits inside `IF (LDH)`, where it is overwritten at once; without `LDH`, SCV with OPAL 2006 is labelled `SCV` in the flags line of both formats. Only with `LSCV` and `LOPALE06` on and `LDH` off. The same lines are in [WRTLST](wrtlst.f.md#wrtlst) ([wrtlst.f, suspected bug 1](wrtlst.f.md#b1)).

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

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The `LSCV` branch ran in 30 of 34 runs: 26 of YREC's cases, from a 0.04 $`M_\odot`$ brown dwarf and the solar models to 9 $`M_\odot`$, rotation, and helium burning, and 8 made-up ones, but the setting that goes wrong, SCV with OPAL 2006 and without `LDH`, held in none: YREC's cases that use SCV with OPAL 2006 also set `LDH`. Any of them with `LDH` off would reach it. The fix was not run. Intent: none found; the misplaced line is already in the first commit of the history (Apr 10, 2025), indented at the level of `IF (LDH)`, as if pasted one line low.

2. **(wrong output)** **Checked by KC** (Nov 10, 2026). **Atmosphere 5 has no label.** ([lines 135–145](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L135-L145)) `KTTAU = 5` (Kurucz/Castelli, JNT 6/14) has no branch, so `ATM` keeps its value from the previous call (it is `SAVE`d) or, at the first call, is undefined, and that is written to the `.store` file's flags line. WRTLST has the branch ([wrtlst.f, lines 103–105](https://github.com/yreclab/yrec/blob/7be4133/src/wrtlst.f#L103-L105)). Only with `KTTAU` = 5 (the default is 0) and `LSTORE`.

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

    **How the outputs show it.** In the made-up run (`testsuite/Test_solarGS98_kurucz` with `KTTAU` = 5 and `FATM` = `atmos/CastelliKurucz/atmk2004p00.tab`), the `.store` file's flags line, written once, at the first store (model 23; [lines 189–192](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L189-L192)), holds four NUL bytes in the ATM column, between "SCDHO6" and "NONE": `ATM` was never set. The `.last` file, written at the last model (1224) by WRTLST ([wrtlst.f, lines 103–105](https://github.com/yreclab/yrec/blob/7be4133/src/wrtlst.f#L103-L105)) through PUTMODEL2 ([putmodel2.f, line 80](https://github.com/yreclab/yrec/blob/7be4133/src/putmodel2.f#L80)), gives "K/C" in the same column.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): YREC's `testsuite/Test_solarGS98_kurucz`, run with `KTTAU` = 5 and `FATM` = `atmos/CastelliKurucz/atmk2004p00.tab`, as the README of those tables asks ("You NEED TO CHANGE KTTAU to 5," `input/atmos/CastelliKurucz/README`, line 15), reaches it at both of its stores (models 23 and 1000), so `ATM` was written without a value of its own. With the fix, the track is identical and the harness finds the `.store` file within 2%; the null change moves $`\log L`$ by up to $`0.000144\,\mathrm{dex}`$. The harm is the label, which the fix corrects. Intent: none found; [WRTLST](wrtlst.f.md#wrtlst) got the branch ("JNT 06/14"), and PUTSTORE, written later (G Somers, 11/14), lacks it.

3. **(never occurred)** **Checked by KC** (Nov 10, 2026). **`PINDEX` gets arguments that are never set.** ([lines 51–52](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L51-L52); [line 262](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L262)) `JXBEG`, `JXEND`, and `LSHELL` are neither arguments nor in a module here, so they are undefined locals (zero and `.FALSE.` with a compiler that zero-initializes `SAVE`d locals). The burning-shell option of [PINDEX](https://github.com/yreclab/yrec/blob/7be4133/src/pindex.f#L6-L85), which prints every shell of the hydrogen-burning shell ([pindex.f, lines 46–70](https://github.com/yreclab/yrec/blob/7be4133/src/pindex.f#L46-L70)), therefore never applies, and the old format prints only every `NPRTPT`-th shell there. Only in the old format (`LSTCH` off) with `LSTMOD`, and with `NPRTPT` above 1 (its default is 1, [nmlpar_mod.f, line 169](https://github.com/yreclab/yrec/blob/7be4133/src/nmlpar_mod.f#L169), kept by every case of YREC's that writes the old format).

    **A possible fix:** pass `LSHELL`, `JXBEG`, and `JXEND` to PUTSTORE as arguments, from WRTOUT (which has them as arguments) and from the main program (which sets them through FINDSH, [main.f, lines 578–579](https://github.com/yreclab/yrec/blob/7be4133/src/main.f#L578-L579)), as they were passed to WRTMOD in the commented-out call ([lines 344–346](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L344-L346)). The branch this reaches has two fragile points of its own ([pindex.f, suspected bug 1](pindex.f.md#b1); [pindex.f, suspected bug 2](pindex.f.md#b2)).

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): PINDEX got `JXBEG` = `JXEND` = 0 and `LSHELL` false at every call, in the 14 runs that write the old format. In 10 of them, the callers' `LSHELL` was true at a store, with the shell between points 26 and 2830. But no shell went unlisted: Every case of YREC's that writes the old format keeps `NPRTPT` at 1 (its default, [nmlpar_mod.f, line 169](https://github.com/yreclab/yrec/blob/7be4133/src/nmlpar_mod.f#L169)), and with 1, PINDEX's general branch lists every shell, 2 to $`M-1`$ and then $`M`$ ([pindex.f, lines 73–84](https://github.com/yreclab/yrec/blob/7be4133/src/pindex.f#L73-L84)); `testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS` lists all 748 shells of its model 921 once, and `testsuite/Test_m0p95feh+0p0_GN93_TAHB` all 3,268 and 3,425 shells of its models 0 and 943 (rechecked on Nov 10). The run with the fix differs, but not because of this bug: Its track is identical, and only the `.store` file changes beyond 2% (the null change moves $`\log L`$ by up to $`1.67\times10^{-7}\,\mathrm{dex}`$ in the first case). With `LSHELL` passed, PINDEX takes its shell branch, which with `NPRTPT` = 1 also lists every shell once (loops 10, 20, and 30, [pindex.f, lines 46–72](https://github.com/yreclab/yrec/blob/7be4133/src/pindex.f#L46-L72)) and then lists `M` a second time ([pindex.f, line 83](https://github.com/yreclab/yrec/blob/7be4133/src/pindex.f#L83)): That is PINDEX's own suspected bug, `M` listed twice ([pindex.f, suspected bug 2](pindex.f.md#b2)), which nothing reaches today and this fix would. So this fix should go with that one. The bug itself shows only with `NPRTPT` above 1, which no case of YREC's sets. Intent: The commented-out call to WRTMOD ([lines 344–346](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L344-L346)) passed these three; nothing says they were dropped on purpose.

4. **(wrong output)** **Checked by KC** (Nov 10, 2026). **The old header calls the triple-$`\alpha`$ column "3HE."** ([line 275](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L275); [line 309](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L309)) The fifth energy column, `SEG(5,I)`, is the triple-$`\alpha`$ term (Explanation, step 3), as the stitched format's header says ([line 208](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L208)). What follows: a misleading column name in the old `.store` format. Only with `LSTORE`, `LSTMOD`, and `LSTPHYS`, and `LSTCH` off.

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

    **How the outputs show it.** In `testsuite/Test_m0p95feh+0p0_GN93_TAHB`, at model 943, the `.store` file's column headed "3HE" ([line 275](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L275)) is 0.1000E+01 at the center, where the core burns helium. This column's fractions of E_NUC, summed over the masses of all 3,425 shells, give 3.083 $`L_\odot`$ (with the case's `CLSUN` of $`3.828 \times 10^{33}\,\mathrm{erg\,s^{-1}}`$), and the `.track` gives the same model's triple-$`\alpha`$ luminosity, 3a_lsun ([wrtout.f, line 558](https://github.com/yreclab/yrec/blob/7be4133/src/wrtout.f#L558)), as 3.08298493E+000. At model 0 the two are 16.16 and 1.61768489E+001. The column is the triple-$`\alpha`$ term, as the stitched header says ([line 208](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L208)).

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The header was written with the physics columns in the same 14 runs. With the fix, `examples/run_from_dbl_to_zams/Test_m0040_feh0_noGS_ZAMS` gives an identical track and a `.store` file within 2%, and `examples/run_standard_solar_model/Test_solarcal_noGS_norot` differs exactly as for the null change ($`\log L`$ by up to $`0.000322\,\mathrm{dex}`$): within the noise, as expected for a label. The harm is the label, which the fix corrects. Intent: none found; the stitched format's header names the column TRIPLE_ALPHA ([line 208](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L208)).
