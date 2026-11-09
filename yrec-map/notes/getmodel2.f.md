## Explanation

**Purpose.** `GETMODEL2` reads a stellar model stored in the "Model2" text format ("llp 4/16/03") into memory: the header (model number, mass, $T_\mathrm{eff}$, $L$, age), the physics flags of the run that wrote it, the luminosities by source, the envelope fitting data and the shell-by-shell structure and composition.

**How it fits.**
- **Who calls it:** only [[starin.f#STARIN|STARIN]], when the first record of the input model starts with `MOD2`; for the older YREC7 format (`NMOD`) it calls [[getyrec7.f#GETYREC7|GETYREC7]] instead.
- **Who writes the format:** [[putmodel2.f#PUTMODEL2|PUTMODEL2]] (and the format is mentioned in [[putstore.f#PUTSTORE|PUTSTORE]] and [[wrtlst.f#WRTLST|WRTLST]]).
- **Input:** the file on unit `IREAD`, rewound first.
- **Outputs (arguments):** the header values (`MODEL`, `M`, `SMASS`, `TEFFL`, `BL`, `HSTOT`, `DAGE`, `DDAGE`); the flags and names of the input physics (`EOS`, `ATM`, `ALOK`, `HIK`, `COMPMIX`, `LDIFY`, `LDIFZ`, `LROT`, …, and the disk-locking `TDISK`, `PDISK`, `WMAX`); the luminosities `TLUMX` (the three pp chains, CNO, helium burning, neutrinos, gravitational; converted to solar units if they exceed $10^{20}$, that is, if they were written in erg s$^{-1}$); the envelope triangle `TRIT`, `TRIL`, `PS`, `TS`, `RS`, `CFENV` and its orientation `FTRI` (±1: [[surfbc.f#SURFBC|SURFBC]] flips its sign each time it reflects a corner of the triangle, and uses it in its test of whether ($T_\mathrm{eff}$, $L$) lies inside; PUTMODEL2 writes the record numbers as −1, −2, −3 when it is negative, and GETMODEL2 reads the sign back); and per shell `HS`, `HR`, `HL`, `HP`, `HT`, `HD`, `OMEGA`, `LC` and 15 abundances `HCOMP`.

    > **Question** ([[#L75-L83]]). **Units guessed from size.** The luminosities are taken as erg s$^{-1}$ if any exceeds $10^{20}$, else as solar units. Could the format carry the unit instead?

- **Modules:** [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]] (formerly `/CONST/`), for $L_\odot$ (`CLSUN`).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Bugs, by priority

1. **(b)** **The number of shells is not checked.** ([[#L57-L58]], [[#L103-L106]]) The header record gives `M` and, in the same `READ`, stores `HS(M)`; the loop over the shells then fills `HS(1:M)` and the other arrays of `JSON` = 5000 elements. Nothing checks that 1 ≤ `M` ≤ `JSON`, so a damaged file, or a model of more than 5000 shells, writes outside the arrays (the default build has no bounds checks, `src/Makefile` line 132; `make devel` adds them). A read error or an end of file, which has no `END=` or `ERR=`, stops the run with the compiler's run-time message, which does not name the file. Read from the code, not run; any input model in this format takes this path. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to check the number of shells before it is used as an
    C index, as GETYREC7 checks the shells' masses.
          READ(IREAD,10) ATEMP,MODEL,M,SMASS,TEFFL,BL,HSTOT,DAGE,
         *   DDAGE,HS(1),HSM
          IF(M.LT.1 .OR. M.GT.JSON) THEN
             WRITE(*,*) 'GETMODEL2: NUMBER OF SHELLS ',M,
         *      ' OUTSIDE 1 TO ',JSON,'. RUN STOPPED'
             STOP 3
          ENDIF
          HS(M) = HSM
    ...
    ```

    with `HSM` declared `REAL*8`.

### GETMODEL2

Reads a Model2-format model file: header, physics flags, luminosities, envelope data and the shells.
