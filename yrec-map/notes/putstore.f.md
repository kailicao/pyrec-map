## Explanation

**Purpose.** Writes a verbose stellar model to the `.store` file (`ISTOR`), "either at specified ages, every NPRTMOD models, or at the end of runs". Its header (G. Somers 11/14) calls it "mostly a clone of wrtlst.f and putmodel2.f, combined". Since JvS 09/25 it has two formats: the older one (a MODEL2-style model followed by optional per-shell physics and rotation columns) and, with `LSTCH`, the "stitched" format, in which [[stitch.f#STITCH|STITCH]] writes interior, envelope and atmosphere points together.

**How it fits.**
- **Inputs:** the model as arguments (structure, composition, envelope data, luminosities `TLUMX`, rotation: `OMEGA`, `ETA2`, `R0`, `FP`, `FT`, `HJM`, `HI`), the mixing length `CMIXL`, `XMSOL` (passed on to `WRTMOD`) and the initial-mixture label `COMPMIX` (from [[starin.f#STARIN|STARIN]], through the main program); the physics flags and the output switches (`LSTORE`, `LSTATM`, `LSTENV`, `LSTMOD`, `LSTPHYS`, `LSTROT`, `LSTCH`, `LMILNE`) from [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]], and `LPHHD` from [[ccout_mod.f#CCOUT_MOD|`CCOUT_MOD`]]; the per-shell physics in [[scrtch_mod.f#SCRTCH_MOD|`SCRTCH_MOD`]], [[sound_mod.f#SOUND_MOD|`SOUND_MOD`]] (`GAM1`), [[temp2_mod.f#TEMP2_MOD|`TEMP2_MOD`]] (the rotational mixing velocities) and [[roten_mod.f#ROTEN_MOD|`ROTEN_MOD`]]; the constants from [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]] and the units from [[iounits_mod.f#IOUNITS_MOD|`IOUNITS_MOD`]].
- **Who calls it:** [[wrtout.f#WRTOUT|WRTOUT]] and the main program in [[main.f|main.f]].
- **What it calls:** [[stitch.f#STITCH|STITCH]] (new format), [[pindex.f#PINDEX|PINDEX]] (which shells to print), [[wrtmil.f#WRTMIL|WRTMIL]] (if also `LMILNE`) and [[wrtmod.f#WRTMOD|WRTMOD]] (envelope and atmosphere, if `LSTATM` or `LSTENV`).
- **Output:** the `.store` file, opened by [[parmin.f#PARMIN|PARMIN]] (which also writes the old format's header key). Its `MOD2` blocks can serve as starting models ([[starin.f#STARIN|STARIN]] reads the `MOD2` format).

**The method.**
1. **Labels** for the physics: atmosphere (`EDD`, `KS`, `HRA`, `KUR`, `ALL` from `KTTAU`), equation of state (`SAHA`, `OPAL06`, `SCV`, with `+DH` and OPAL 2006), low-temperature opacity (always `NONE`: the labels `ALEX` and `KURZ` went with the Alexander 1995 and Kurucz 1990 tables) and high-temperature opacity (`OP95`, or `NONE`).
2. **Stitched format** (`LSTCH`): on the first call (`LPHHD`) a header key, the flags line and the column titles; then `STITCH` (with `CMIXL`).
3. **Old format:** the `MOD2` header line, the flags, the `TLUMX` line (converted to erg s⁻¹ in place if the largest is $\le 10^{20}$, as in [[putmodel2.f#PUTMODEL2|PUTMODEL2]]), three `ENV` lines; then, with `LSTMOD`, one line per selected shell: the basic columns, led by the model number; with `LSTPHYS` opacity, gravity $g = Gm/r^2$, $\nabla_\mathrm{rad}$, $\nabla$, $\nabla_\mathrm{ad}$, convective velocity, $\Gamma_1$, `SBETA`, `SETA` and the energy generation terms; with `LSTROT` (and `LROT`) the distortion parameter and the ratio of polar to equatorial radius,
$$A = \frac{5}{3}\,\frac{\Omega^2 r_0^3}{G m\,(2+\eta_2)},\qquad \frac{R_p}{R_e} = \frac{1 - A}{1 + A/2},$$
then `FP`, `FT`, $j$, $I$, the rotational kinetic energy change, and the mixing velocities $v_\mathrm{ES}$, $v_\mathrm{GSF}$, $v_\mathrm{SS}$ and their sum. Missing groups are written as zeros.

**KC's changes.** 2025-05-30: `/OPALEOS/` reordered; 2025-05-31: unused arguments removed from the call to `WRTMOD`.

**Changed since `rp_1`.** `CMIXL`, `XMSOL` and `COMPMIX` are new arguments (`COMPMIX` was `/I2O/`, `CMIXL` was in `/CONST3/`), passed on: `CMIXL` to `STITCH`, both to `WRTMOD`; the labels of the removed options (the OPAL 1995 and 2001 equations of state, the OPAL92, LAOL89, Alexander 1995 and Kurucz 1990 opacities) are gone; each shell's line now starts with the model number, which fixes a crash (format 62 already expected it), and formats 62 and 63 put spaces between some columns; `LMILNE` now comes from `NMLPAR_MOD` (bug fix), so `WRTMIL` is called when it is set, which settles former question 2 (questions 3–7 are now 2–6); COMMON blocks to modules (eleven unused blocks dropped), `IMPLICIT NONE`. New question 7 (the low-temperature label).

## Questions for the experts

1. **`PINDEX` gets undefined arguments.** `JXBEG`, `JXEND` and `LSHELL` are neither arguments nor in a module here, so they are undefined locals (zero or `.FALSE.` if the compiler zero-initializes). The burning-shell option of [[pindex.f#PINDEX|PINDEX]] can therefore never apply. Should they be passed in (as they were to `WRTMOD`, in the commented-out call)?
2. **The SCV + OPAL 2006 label.** In the `LSCV` branch, `IF (LOPALE06) EOS='SCV+O6'` sits inside `IF (LDH)`, where it is overwritten at once; without `LDH`, SCV with OPAL 2006 is labelled `SCV`. Move the line up one level?
3. **Atmosphere 5.** `KTTAU = 5` (Kurucz/Castelli, JNT 6/14) has no label, so `ATM` keeps its value from the previous call, or is undefined.
4. **Ionization fractions written as zeros.** The columns HII, HEII, HEIII are written as 0.0 (the line with `SFXION` is commented out). Intended?
5. **Column labels.** The old header names the fifth energy column "3HE" and the new one "TRIPLE_ALPHA". Which is `SEG(5,·)`?
6. **Duplicated code.** The labels, the `MOD2` header and the `TLUMX` conversion repeat [[putmodel2.f#PUTMODEL2|PUTMODEL2]] and `WRTLST`. A shared routine would keep them in step.
7. **No low-temperature opacity label.** With the Alexander 1995 and Kurucz 1990 tables removed, `ALOK` is always `NONE`: the Ferguson et al. (2005) tables (`LALEX06`), the only low-temperature tables left, were never labelled. Should `LALEX06` set `ALOK` (for example to `AL06`)?
