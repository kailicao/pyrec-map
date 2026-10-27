## Explanation

**Purpose.** `WRTLST` writes a converged model to a model file, in the MODEL2 format, which a later run can read back as its starting model ([[starin.f#STARIN|STARIN]] through [[getmodel2.f#GETMODEL2|GETMODEL2]]). Its comment: it writes the last converged model, and the stored models every `NPUNCH` models. Before writing, it turns the run's physics switches into the four header labels.

**How it fits.**
- **Inputs:** the model and its envelope triangle (arguments), the unit `IWRITE`, the mixing length `CMIXL` and `COMPMIX` (the initial composition's code, carried from input to output), both now arguments; and the physics switches in [[nmlpar_mod.f|`NMLPAR_MOD`]]: `KTTAU`, `LDH`, `LSCV`, `LOPALE06`, `LOPAL95` for the labels, and `LEXCOM`, `LROT`, `LDIFY`, `LDIFZ`, `LDISK`, `LINSTB`, `LJDOT0`, `LOVSTC`, `LOVSTE`, `LOVSTM`, `LPUREZ`, `LSEMIC`, `PDISK`, `TDISK`, `WMAX`, whose values are written as they are. The units `ILAST`, `IOWR`, `ISHORT` come from [[iounits_mod.f|`IOUNITS_MOD`]].
- **Who calls it:** the main program [[main.f#(file level)|main.f]] (unit `ILAST`) and [[wrtout.f#WRTOUT|WRTOUT]] (`ILAST`, and `IJLAST`).
- **What it calls:** [[putmodel2.f#PUTMODEL2|PUTMODEL2]], which writes the file.
- **Outputs:** the model file on `IWRITE`; a line on `IOWR` and one on `ISHORT`. The unit `ILAST` is rewound, so it holds only the latest model.

**The labels.**
- **Atmosphere:** `KTTAU` 0–5 → `EDD` (Eddington), `KS`, `HRA`, `KUR` (Kurucz), `ALL` (Allard), `K/C` (Kurucz–Castelli).
- **Equation of state:** `SAHA`, plus `DH` (Debye–Hückel), `SCV`, and the OPAL 2006 tables (`O6`) in six-character combinations: `SAHA`, `SAH+DH`, `SCV`, `SCV+DH`, `SCDHO6`, `OPAL06`, `OP6+DH`.
- **Low-temperature opacity** `ALOK`: always `NONE` now; **high-temperature** `HIK`: `OP95` or `NONE`.

**KC's changes.** The elements of COMMON `OPALEOS` were reordered (2025-05-30); the block is no longer declared here.

**Changed since `rp_1`.** COMMON blocks to modules, `IMPLICIT NONE`; `CMIXL` and `COMPMIX` (formerly COMMON `CONST3` and `I2O`) are now arguments; the labels of the removed options are gone (OPAL 1995 and 2001 EOS, Alexander 1995 and Kurucz 1990 low-temperature opacities, OPAL92 and LAOL89 high-temperature opacities); `WRTMONTE`, a former caller, is deleted.

## Questions for the experts

1. **A lost label.** In the SCV branch, `IF (LOPALE06) EOS='SCV+O6'` sits inside `IF (LDH)` and is overwritten on the next line by `'SCV+DH'`; SCV with OPAL 2006 and without Debye–Hückel is labelled `SCV`. The line probably belongs before `IF (LDH)`.
2. **Unset atmosphere label.** If `KTTAU` is outside 0–5, `ATM` keeps its previous (`SAVE`d) or undefined value.
3. **A hard-coded unit.** The message's format depends on `IWRITE.EQ.11`; is unit 11 always `ILAST`?

### WRTLST

Sets the header labels for atmosphere, EOS and opacities, and writes the model to `IWRITE` in MODEL2 format through `PUTMODEL2`.
