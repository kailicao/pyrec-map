## Explanation

**Purpose.** `GETMODEL2` reads a stellar model stored in the "Model2" text format ("llp 4/16/03") into memory: the header (model number, mass, $T_\mathrm{eff}$, $L$, age), the physics flags of the run that wrote it, the luminosities by source, the envelope fitting data and the shell-by-shell structure and composition.

**How it fits.**
- **Who calls it:** only [[starin.f#STARIN|STARIN]], when the first record of the input model starts with `MOD2`; for the older YREC7 format (`NMOD`) it calls [[getyrec7.f#GETYREC7|GETYREC7]] instead.
- **Who writes the format:** [[putmodel2.f#PUTMODEL2|PUTMODEL2]] (and the format is mentioned in [[putstore.f#PUTSTORE|PUTSTORE]] and [[wrtlst.f#WRTLST|WRTLST]]).
- **Input:** the file on unit `IREAD`, rewound first.
- **Outputs (arguments):** the header values (`MODEL`, `M`, `SMASS`, `TEFFL`, `BL`, `HSTOT`, `DAGE`, `DDAGE`); the flags and names of the input physics (`EOS`, `ATM`, `ALOK`, `HIK`, `COMPMIX`, `LDIFY`, `LDIFZ`, `LROT`, …, and the disk-locking `TDISK`, `PDISK`, `WMAX`); the luminosities `TLUMX` (the three pp chains, CNO, helium burning, neutrinos, gravitational; converted to solar units if they exceed $10^{20}$, that is, if they were written in erg s$^{-1}$); the envelope triangle `TRIT`, `TRIL`, `PS`, `TS`, `RS`, `CFENV` and its orientation `FTRI` (±1: [[surfbc.f#SURFBC|SURFBC]] flips its sign each time it reflects a corner of the triangle, and uses it in its test of whether ($T_\mathrm{eff}$, $L$) lies inside; PUTMODEL2 writes the record numbers as −1, −2, −3 when it is negative, and GETMODEL2 reads the sign back); and per shell `HS`, `HR`, `HL`, `HP`, `HT`, `HD`, `OMEGA`, `LC` and 15 abundances `HCOMP`.
- **Modules:** [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]] (formerly `/CONST/`), for $L_\odot$ (`CLSUN`).

**KC's changes.** The unused argument `ISHORT` was removed (2025-05-31).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **Units guessed from size.** The luminosities are taken as erg s$^{-1}$ if any exceeds $10^{20}$, else as solar units. Could the format carry the unit instead?
2. **No checks.** There is no check that `M` ≤ `JSON` (5000), although the header record already stores `HS(M)` as it reads `M`, nor on read errors. Add them?

### GETMODEL2

Reads a Model2-format model file: header, physics flags, luminosities, envelope data and the shells.
