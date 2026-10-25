## Explanation

**Purpose.** `WRTLST` writes a converged model to a model file, in the MODEL2 format, which a later run can read back as its starting model ([[starin.f#STARIN|STARIN]] through [[getmodel2.f#GETMODEL2|GETMODEL2]]). Its comment: it writes the last converged model, and the stored models every `NPUNCH` models. Before writing, it turns the run's physics switches into the four header labels.

**How it fits.**
- **Inputs:** the model and its envelope triangle (arguments), the unit `IWRITE`, and the physics switches in COMMON blocks: `ATMOS` (`KTTAU`), `DEBHU` (`LDH`), `SCVEOS` (`LSCV`), `OPALEOS` (`LOPALE`, `LOPALE01`, `LOPALE06`), `NEWOPAC` (opacity tables), `NWLAOL` (`LPUREZ`), `I2O` (`COMPMIX`, the initial composition's code, carried from input to output), and `CWIND`, `DISK`, `DPMIX`, `GRAVST`, `GRAVS3`, `ROT`, `FLAG`, `CONST3`, whose values are written as they are.
- **Who calls it:** the main program [[main.f#(file level)|main.f]] (unit `ILAST`), [[wrtout.f#WRTOUT|WRTOUT]] (`ILAST`, and `IJLAST`), and [[wrtmonte.f#WRTMONTE|WRTMONTE]] (`IMONTE2`).
- **What it calls:** [[putmodel2.f#PUTMODEL2|PUTMODEL2]], which writes the file.
- **Outputs:** the model file on `IWRITE`; a line on `IOWR` and one on `ISHORT`. The unit `ILAST` is rewound, so it holds only the latest model.

**The labels.**
- **Atmosphere:** `KTTAU` 0–5 → `EDD` (Eddington), `KS`, `HRA`, `KUR` (Kurucz), `ALL` (Allard), `K/C` (Kurucz–Castelli).
- **Equation of state:** `SAHA`, plus `DH` (Debye–Hückel), `SCV`, and the OPAL tables (`OP`, `O1`, `O6`) in six-character combinations.
- **Low-temperature opacity** `ALOK`: `ALEX` or `KURZ`; **high-temperature** `HIK`: `OP95`, `OP92` or `LL89` (the last switch on wins).

**KC's changes.** The elements of COMMON `OPALEOS` were reordered (2025-05-30).

## Questions for the experts

1. **A lost label.** In the SCV branch, `IF (LOPALE06) EOS='SCV+O6'` sits inside `IF (LDH)` and is overwritten on the next line by `'SCV+DH'`; SCV with OPAL 2006 and without Debye–Hückel is labelled `SCV`. The line probably belongs before `IF (LDH)`.
2. **Unset atmosphere label.** If `KTTAU` is outside 0–5, `ATM` keeps its previous (`SAVE`d) or undefined value.
3. **A hard-coded unit.** The message's format depends on `IWRITE.EQ.11`; is unit 11 always `ILAST`?

### WRTLST

Sets the header labels for atmosphere, EOS and opacities, and writes the model to `IWRITE` in MODEL2 format through `PUTMODEL2`.
