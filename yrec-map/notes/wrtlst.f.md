## Explanation

**Purpose.** `WRTLST` writes a converged model to a model file, in the MODEL2 format, which a later run can read back as its starting model ([[starin.f#STARIN|STARIN]] through [[getmodel2.f#GETMODEL2|GETMODEL2]]). Its comment: it writes the last converged model, and the stored models every `NPUNCH` models. Before writing, it turns the run's physics switches into the four header labels.

**How it fits.**
- **Inputs:** the model and its envelope triangle (arguments), the unit `IWRITE`, the mixing length `CMIXL` and `COMPMIX` (the initial composition's code, carried from input to output), both now arguments; and the physics switches in [[nmlpar_mod.f|`NMLPAR_MOD`]]: `KTTAU`, `LDH`, `LSCV`, `LOPALE06`, `LOPAL95` for the labels, and `LEXCOM`, `LROT`, `LDIFY`, `LDIFZ`, `LDISK`, `LINSTB`, `LJDOT0`, `LOVSTC`, `LOVSTE`, `LOVSTM`, `LPUREZ`, `LSEMIC`, `PDISK`, `TDISK`, `WMAX`, whose values are written as they are. The units `ILAST`, `IOWR`, `ISHORT` come from [[iounits_mod.f|`IOUNITS_MOD`]].
- **Who calls it:** the main program [[main.f#(file level)|main.f]] (unit `ILAST`) and [[wrtout.f#WRTOUT|WRTOUT]] (`ILAST`, and `IJLAST`).
- **What it calls:** [[putmodel2.f#PUTMODEL2|PUTMODEL2]], which writes the file.
- **Outputs:** the model file on `IWRITE`; a line on `IOWR` and one on `ISHORT`, which omits the age when `IWRITE` is 11, the unit number PARMIN gives `ILAST` ([[parmin.f#L658]]) (settled from the code, Nov 9, 2026: [[#L150-L156]]). The unit `ILAST` is rewound, so it holds only the latest model.

**The labels.**
- **Atmosphere:** `KTTAU` 0–5 → `EDD` (Eddington), `KS`, `HRA`, `KUR` (Kurucz), `ALL` (Allard), `K/C` (Kurucz–Castelli); any other value leaves `ATM` unset (bug 2).
- **Equation of state:** `SAHA`, plus `DH` (Debye–Hückel), `SCV`, and the OPAL 2006 tables (`O6`) in six-character combinations: `SAHA`, `SAH+DH`, `SCV`, `SCV+DH`, `SCDHO6`, `OPAL06`, `OP6+DH`; the seventh, `SCV+O6`, is never written (bug 1).
- **Low-temperature opacity** `ALOK`: always `NONE` now; **high-temperature** `HIK`: `OP95` or `NONE`.

**For users** (from YREC's [Quick Start](https://yrec.readthedocs.io/en/latest/quickstart.html)). Through the unit `ILAST`, this is the `.last` file (`FLAST` in the control namelist): the last converged model, in the same format as a starting model, so that a later job can start from it (`FFIRST`).

**Changed since `rp_1`.** COMMON blocks to modules, `IMPLICIT NONE`; `CMIXL` and `COMPMIX` (formerly COMMON `CONST3` and `I2O`) are now arguments; the labels of the removed options are gone (OPAL 1995 and 2001 EOS, Alexander 1995 and Kurucz 1990 low-temperature opacities, OPAL92 and LAOL89 high-temperature opacities); `WRTMONTE`, a former caller, is deleted.

## Bugs, by priority

1. **(never occurred)** **A lost label.** ([[#L110-L118]]) In the SCV branch, `IF (LOPALE06) EOS='SCV+O6'` sits inside `IF (LDH)` and is overwritten on the next line by `'SCV+DH'`, so SCV with OPAL 2006 and without Debye–Hückel is labelled `SCV`. What follows: a wrong equation-of-state label in the model file's flags line; GETMODEL2 reads the label back, but nothing acts on it. Only with `LSCV` and `LOPALE06` on and `LDH` off. [[putstore.f#PUTSTORE|PUTSTORE]] has the same lines ([[putstore.f#b1]]).

    **A possible fix:**

    ```diff
    --- a/src/wrtlst.f
    +++ b/src/wrtlst.f
    @@ -107,12 +107,15 @@
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

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Of 34 runs (26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones), the SCV branch ran at every model in 32, but never with `LOPALE06` on and `LDH` off: YREC's cases use SCV only with Debye–Hückel, and the documentation recommends `LDH` on (`docs/source/microphysics.md`, line 17). Not run: `LSCV` and `LOPALE06` on with `LDH` off. Intent: none found.

2. **(never occurred)** **Unset atmosphere label.** ([[#L93-L106]]) If `KTTAU` is outside 0–5, `ATM` keeps its value from the previous call (it is `SAVE`d) or, at the first call, is undefined, and that is written to the model file. Only with an invalid `KTTAU` (the default is 0); nothing checks its range.

    **A possible fix:**

    ```diff
    --- a/src/wrtlst.f
    +++ b/src/wrtlst.f
    @@ -103,6 +103,10 @@
     C JNT 06/14
           ELSEIF (KTTAU .EQ. 5) THEN
              ATM='K/C '
    +C 11/09/26 KC via Claude
    +C code changed to label an atmosphere option outside 0-5.
    +      ELSE
    +         ATM='UNK '
           ENDIF
     C Determine equation of state flag, EOS
           EOS='SAHA  '
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): WRTLST ran at every model in 33 runs, with `KTTAU` from 0 to 5 (5 in a made-up run: YREC's `testsuite/Test_solarGS98_kurucz` with `KTTAU` = 5 and the Castelli–Kurucz table, as `input/atmos/CastelliKurucz/README` asks), never outside 0–5. Not run: an invalid `KTTAU`, which nothing in YREC offers. Intent: none found.

### WRTLST

Sets the header labels for atmosphere, EOS and opacities, and writes the model to `IWRITE` in MODEL2 format through `PUTMODEL2`.
