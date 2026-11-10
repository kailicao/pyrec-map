## Explanation

**Purpose.** `GETYREC7` reads a stellar model stored in the older YREC7 text format ("llp 4/16/03"; its header calls it `GETY7`) into memory. Since the YREC7 format lacks the physics flags of the newer Model2 format, it sets those to defaults ("?" strings, false flags).

**How it fits.**
- **Who calls it:** only [[starin.f#STARIN|STARIN]], when the input model's first record starts with `NMOD`; Model2 files (`MOD2`) go to [[getmodel2.f#GETMODEL2|GETMODEL2]], which returns the same arguments.
- **Who writes the format:** [[putyrec7.f#PUTYREC7|PUTYREC7]] (its formats match these), which nothing calls; so YREC7 files now come only from older codes.
- **Input:** the file on unit `IREAD`, rewound before and after; `ISHORT`, the unit of its error messages ([[#L140-L141]], [[#L249]]), so that, unlike in `GETMODEL2`, this argument is used.
- **Outputs (arguments):** the header (`MODEL`, `M`, `SMASS`, `TEFFL`, `BL`, `HSTOT`, `DAGE`, `DDAGE`), `LROT`, `LEXCOM`, `JCORE`, `JENV`, `CMIXL`, the luminosities `TLUMX` (converted to solar units if above $10^{20}$), the envelope triangle (`TRIT`, `TRIL`, `PS`, `TS`, `RS`, `CFENV`, `FTRI`), the shells (`HS`, `HR`, `HL`, `HP`, `HT`, `HD`, `LC`), `HCOMP` and `OMEGA`; plus the Model2-only items, set to defaults: the strings `ATM`, `EOS`, `HIK`, `ALOK` = "?," `COMPMIX` = "AG93," all flags false, `PDISK` = 7.2722×10$^{-6}$ rad s$^{-1}$ (a 10-day period), `TDISK` = 0, `WMAX` = 3×10$^{-4}$ ([[#L86-L89]]). These three do not change the run's physics: STARIN receives them in its locals `PDISK0`, `TDISK0`, `WMAX0` ([[starin.f#L280-L285]]), which it never reads (unused?), and the namelist's `PDISK`, `TDISK`, `WMAX` are untouched (settled from the code, Nov 9, 2026).
- **Modules:** [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]] (formerly `/CONST/`), for $L_\odot$.

**The format, as read.**
1. Each shell stores $X$ and $Z$ as integers in units of $10^{-6}$; $Y = 1 - X - Z - X(^3\mathrm{He})$ is recomputed. The run stops (exit status 3, an input error) if a shell's $\log m$ is negative or above the total.

    > **Question** ([[#L148-L149]]). **Precision of $X$ and $Z$.** The format keeps $X$ and $Z$ to $10^{-6}$. Is that enough when models with diffusion are restarted from this format?

2. The other species (rows 4–11) are stored only from `JCORE` to `JENV`, the region between the convective core and envelope, and copied into the homogeneous core and envelope. With `LEXCOM`, the light elements (rows 12–15) follow the same pattern, two shells per record.
3. With `LROT`, $\Omega$ is stored as $-\log_{10}\Omega$; values of 58.9 or more mean $\Omega = 0$. If those records are missing, $\Omega$ is set to zero with a message.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

**Changed since `a8a5950`.** The stop on a bad shell mass now exits with status 3, the code for input errors (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(not reached)** **The flags record is read one column late.** ([[#L104-L105]]; [[putyrec7.f#L65-L66]]) PUTYREC7 writes the record as `2(L1,1X),'F F ',2I4,F7.3`, four characters between the flags and `JCORE`, and the YREC7 starting models in `startmodels/seed/` have the same layout (`F T F F    1   1  1.735`); GETYREC7 reads it as `2(L1,1X),5X,2I4,F7.3`, skipping five. Each field is then read one column late: `JCORE` from columns 10–13, which hold its last three digits and the first column of `JENV`; `JENV` from columns 14–17, its last three digits and the first column of `CMIXL`. With blanks ignored, the values come out right while `JCORE` and `JENV` are below 1000 (all 41 YREC7 files in the repository have at most 391 shells); with a four-digit `JENV` (`M` may reach `JSON` = 5000) its first digit is appended to `JCORE` and lost from `JENV`.

    **A possible fix:**

    ```diff
    --- a/src/getyrec7.f
    +++ b/src/getyrec7.f
    @@ -102,7 +102,10 @@
     C Get the flags describing the input physics and the information that
     C is stored in the model (rotating or not?, extendec compotition, etc.)
           READ(IREAD,30) LROT,LEXCOM,JCORE,JENV,CMIXL
    - 30   FORMAT(2(L1,1X),5X,2I4,F7.3)
    +C 11/09/26 KC via Claude
    +C code changed to skip the four columns PUTYREC7 writes ('F F ')
    +C between the flags and JCORE, not five.
    + 30   FORMAT(2(L1,1X),4X,2I4,F7.3)
     
     C get the LUMINOSITIES---PP(1-2-3)-CNO-HE-NU-GRAV
           READ(IREAD,40) (TLUMX(J),J=1,7)
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached: None of the 33 runs started from a YREC7 file (the `NMOD` seeds in `startmodels/seed/`, which the cases of `examples/run_from_seed_to_start/` and `examples/run_rotation_to_RG/` read). The fix was not run. With those seeds the values would come out right, as above; what would reach the misreading is a YREC7 file with a four-digit `JENV`. No comment says the fifth column is meant; PUTYREC7 writes four.

### GETYREC7

Reads a YREC7-format model file (header, envelope data, shells, composition in compressed form, rotation) and sets the Model2-only items to defaults.
