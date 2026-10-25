## Explanation

**Purpose.** Writes a verbose stellar model to the `.store` file (`ISTOR`), "either at specified ages, every NPRTMOD models, or at the end of runs". Its header (G. Somers 11/14) calls it "mostly a clone of wrtlst.f and putmodel2.f, combined". Since JvS 09/25 it has two formats: the older one (a MODEL2-style model followed by optional per-shell physics and rotation columns) and, with `LSTCH`, the "stitched" format, in which [[stitch.f#STITCH|STITCH]] writes interior, envelope and atmosphere points together.

**How it fits.**
- **Inputs:** the model as arguments (structure, composition, envelope data, luminosities `TLUMX`, rotation: `OMEGA`, `ETA2`, `R0`, `FP`, `FT`, `HJM`, `HI`); the physics flags from many COMMON blocks (`/ATMOS/`, `/OPALEOS/`, `/SCVEOS/`, `/DEBHU/`, `/NEWOPAC/`, `/NWLAOL/`, `/DPMIX/`, `/GRAVST/`, `/GRAVS3/`, `/DISK/`, `/CWIND/`, `/ROT/`, `/FLAG/`), the output switches in `/CCOUT/` (`LSTORE`, `LSTATM`, `LSTENV`, `LSTMOD`, `LSTPHYS`, `LSTROT`, `LSTCH`, `LPHHD`), the per-shell physics in `/SCRTCH/`, `/SOUND/` (`GAM1`), `/TEMP2/` (the rotational mixing velocities) and `/ROTEN/`, and the initial-mixture label `COMPMIX` in `/I2O/` (from [[starin.f#STARIN|STARIN]]).
- **Who calls it:** [[wrtout.f#WRTOUT|WRTOUT]] and the main program in [[main.f|main.f]].
- **What it calls:** [[stitch.f#STITCH|STITCH]] (new format), [[pindex.f#PINDEX|PINDEX]] (which shells to print), [[wrtmil.f#WRTMIL|WRTMIL]] and [[wrtmod.f#WRTMOD|WRTMOD]] (envelope and atmosphere, if `LSTATM` or `LSTENV`).
- **Output:** the `.store` file, opened by [[parmin.f#PARMIN|PARMIN]] (which also writes the old format's header key). Its `MOD2` blocks can serve as starting models ([[starin.f#STARIN|STARIN]] reads the `MOD2` format).

**The method.**
1. **Labels** for the physics: atmosphere (`EDD`, `KS`, `HRA`, `KUR`, `ALL` from `KTTAU`), equation of state (`SAHA`, `OPAL`, `SCV`, with `+DH` and the OPAL version), low-temperature opacity (`ALEX`, `KURZ`) and high-temperature opacity (`OP95`, `OP92`, `LL89`).
2. **Stitched format** (`LSTCH`): on the first call (`LPHHD`) a header key, the flags line and the column titles; then `STITCH`.
3. **Old format:** the `MOD2` header line, the flags, the `TLUMX` line (converted to erg s⁻¹ in place if the largest is $\le 10^{20}$, as in [[putmodel2.f#PUTMODEL2|PUTMODEL2]]), three `ENV` lines; then, with `LSTMOD`, one line per selected shell: the basic columns; with `LSTPHYS` opacity, gravity $g = Gm/r^2$, $\nabla_\mathrm{rad}$, $\nabla$, $\nabla_\mathrm{ad}$, convective velocity, $\Gamma_1$, `SBETA`, `SETA` and the energy generation terms; with `LSTROT` (and `LROT`) the distortion parameter and the ratio of polar to equatorial radius,
$$A = \frac{5}{3}\,\frac{\Omega^2 r_0^3}{G m\,(2+\eta_2)},\qquad \frac{R_p}{R_e} = \frac{1 - A}{1 + A/2},$$
then `FP`, `FT`, $j$, $I$, the rotational kinetic energy change, and the mixing velocities $v_\mathrm{ES}$, $v_\mathrm{GSF}$, $v_\mathrm{SS}$ and their sum. Missing groups are written as zeros.

**KC's changes.** 2025-05-30: `/OPALEOS/` reordered; 2025-05-31: unused arguments removed from the call to `WRTMOD`.

## Questions for the experts

1. **`PINDEX` gets undefined arguments.** `JXBEG`, `JXEND` and `LSHELL` are neither arguments nor in a COMMON block here, so they are undefined locals (zero or `.FALSE.` if the compiler zero-initializes). The burning-shell option of [[pindex.f#PINDEX|PINDEX]] can therefore never apply. Should they be passed in (as they were to `WRTMOD`, in the commented-out call)?
2. **`LMILNE` is undefined.** `IF(LMILNE) CALL WRTMIL(…)` uses `LMILNE`, which is in `/CCOUT2/`, not declared here; it is an undefined local logical, so `WRTMIL` is probably never called from here.
3. **The SCV + OPAL 2006 label.** In the `LSCV` branch, `IF (LOPALE06) EOS='SCV+O6'` sits inside `IF (LDH)`, where it is overwritten at once; without `LDH`, SCV with OPAL 2006 is labelled `SCV`. Move the line up one level?
4. **Atmosphere 5.** `KTTAU = 5` (Kurucz/Castelli, JNT 6/14) has no label, so `ATM` keeps its value from the previous call, or is undefined.
5. **Ionization fractions written as zeros.** The columns HII, HEII, HEIII are written as 0.0 (the line with `SFXION` is commented out). Intended?
6. **Column labels.** The old header names the fifth energy column "3HE" and the new one "TRIPLE_ALPHA". Which is `SEG(5,·)`?
7. **Duplicated code.** The labels, the `MOD2` header and the `TLUMX` conversion repeat [[putmodel2.f#PUTMODEL2|PUTMODEL2]] and `WRTLST`. A shared routine would keep them in step.
