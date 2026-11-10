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

1. **(never occurred)** **The number of shells is not checked.** ([[#L57-L58]], [[#L103-L106]]) The header record gives `M` and, in the same `READ`, stores `HS(M)`; the loop over the shells then fills `HS(1:M)` and the other arrays of `JSON` = 5000 elements. Nothing checks that 1 ≤ `M` ≤ `JSON`, so a damaged file, or a model of more than 5000 shells, writes outside the arrays (the default build has no bounds checks, `src/Makefile` line 132; `make devel` adds them). A read error or an end of file, which has no `END=` or `ERR=`, stops the run with the compiler's run-time message, which does not name the file.

    **A possible fix:**

    ```diff
    --- a/src/getmodel2.f
    +++ b/src/getmodel2.f
    @@ -24,8 +24,8 @@
     C explicit declarations.
           IMPLICIT NONE
           REAL*8 BL,CCCMAX,CFENV,CMIXL,DAGE,DDAGE,FTRI,HCOMP,HD,HL,HP,HR,HS,
    -     *       HSTOT,HT,OMEGA,PDISK,PS,RS,SMASS,TDISK,TEFFL,TLUMX,TRIL,
    -     *       TRIT,TS,WMAX
    +     *       HSM,HSTOT,HT,OMEGA,PDISK,PS,RS,SMASS,TDISK,TEFFL,TLUMX,
    +     *       TRIL,TRIT,TS,WMAX
           INTEGER I,IO,IREAD,J,JCORE,JENV,K,M,MODEL
           LOGICAL*4 LC,LDIFY,LDIFZ,LDISK,LEXCOM,LINSTB,LJDOT0,LOVSTC,LOVSTE,
          *       LOVSTM,LPUREZ,LROT,LSEMIC
    @@ -54,8 +54,17 @@
           REWIND(IREAD)
     
     C get the header record
    +C 11/09/26 KC via Claude
    +C code changed to check the number of shells before it is used as an
    +C index, as GETYREC7 checks the shells' masses.
           READ(IREAD,10) ATEMP,MODEL,M,SMASS,TEFFL,BL,HSTOT,DAGE,
    -     *   DDAGE,HS(1),HS(M)
    +     *   DDAGE,HS(1),HSM
    +      IF(M.LT.1 .OR. M.GT.JSON) THEN
    +         WRITE(*,*) 'GETMODEL2: NUMBER OF SHELLS ',M,
    +     *      ' OUTSIDE 1 TO ',JSON,'. RUN STOPPED'
    +         STOP 3
    +      ENDIF
    +      HS(M) = HSM
      10   FORMAT(A5,2I8,5F16.12,1PE18.10,0P2F16.12)
     
     C Get the flags describing the input physics and the information that
    ```

    with `HSM` declared `REAL*8`.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The header was read in all 33 runs (YREC's cases, and the made-up variants of them used for other pages), once each, three times in the solar calibration `examples/run_standard_solar_model/Test_solarcal_noGS_norot`, with `M` from 441 to 2,118 shells and model numbers from −3 to 852. `M` never left 1 to `JSON`, so no run wrote outside the arrays, and the fix was not run. What would reach it: a damaged model file, or one of more than 5,000 shells; nothing stops such a file before the arrays are overrun. Any input model in this format takes this path. No comment says the check was left out on purpose.

### GETMODEL2

Reads a Model2-format model file: header, physics flags, luminosities, envelope data and the shells.
