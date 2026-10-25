## Explanation

**Purpose.** `GETYREC7` reads a stellar model stored in the older YREC7 text format ("llp 4/16/03"; its header calls it `GETY7`) into memory. Since the YREC7 format lacks the physics flags of the newer Model2 format, it sets those to defaults ("?" strings, false flags).

**How it fits.**
- **Who calls it:** only [[starin.f#STARIN|STARIN]], when the input model's first record starts with `NMOD`; Model2 files (`MOD2`) go to [[getmodel2.f#GETMODEL2|GETMODEL2]], which returns the same arguments.
- **Who writes the format:** [[putyrec7.f#PUTYREC7|PUTYREC7]] (its formats match these), which nothing calls; so YREC7 files now come only from older codes.
- **Input:** the file on unit `IREAD`, rewound before and after.
- **Outputs (arguments):** the header (`MODEL`, `M`, `SMASS`, `TEFFL`, `BL`, `HSTOT`, `DAGE`, `DDAGE`), `LROT`, `LEXCOM`, `JCORE`, `JENV`, `CMIXL`, the luminosities `TLUMX` (converted to solar units if above $10^{20}$), the envelope triangle (`TRIT`, `TRIL`, `PS`, `TS`, `RS`, `CFENV`, `FTRI`), the shells (`HS`, `HR`, `HL`, `HP`, `HT`, `HD`, `LC`), `HCOMP` and `OMEGA`; plus the Model2-only items, set to defaults: the strings `ATM`, `EOS`, `HIK`, `ALOK` = "?", `COMPMIX` = "AG93", all flags false, `PDISK` = 7.2722×10$^{-6}$ rad s$^{-1}$ (a 10-day period), `TDISK` = 0, `WMAX` = 3×10$^{-4}$.
- **COMMON blocks:** `/CONST/`, for $L_\odot$.

**The format, as read.**
1. Each shell stores $X$ and $Z$ as integers in units of $10^{-6}$; $Y = 1 - X - Z - X(^3\mathrm{He})$ is recomputed. The run stops if a shell's $\log m$ is negative or above the total.
2. The other species (rows 4–11) are stored only from `JCORE` to `JENV`, the region between the convective core and envelope, and copied into the homogeneous core and envelope. With `LEXCOM`, the light elements (rows 12–15) follow the same pattern, two shells per record.
3. With `LROT`, $\Omega$ is stored as $-\log_{10}\Omega$; values of 58.9 or more mean $\Omega = 0$. If those records are missing, $\Omega$ is set to zero with a message.

## Questions for the experts

1. **Precision of $X$ and $Z$.** The format keeps $X$ and $Z$ to $10^{-6}$. Is that enough when models with diffusion are restarted from this format?
2. **Defaults that change physics.** `PDISK` and `WMAX` are set here to fixed values; if the namelist does not override them, a restart from a YREC7 model uses these. Are they the intended defaults?
3. **`ISHORT` still an argument.** In `GETMODEL2` KC removed the unused `ISHORT`; here it is used (for the error messages), so it stays. Fine; noted for consistency.
4. **A one-column offset.** PUTYREC7 writes the flags record as `2(L1,1X),'F F ',2I4,F7.3` (four characters between the flags and `JCORE`), but GETYREC7 reads it as `2(L1,1X),5X,2I4,F7.3`, skipping five. Each field is then read one column late; with blanks ignored this gives the right values while `JCORE` and `JENV` are below 1000, but with a four-digit `JENV` (up to `JSON` = 5000) the first digit of `JENV` ends up in `JCORE`. Which layout did YREC7 itself write?

### GETYREC7

Reads a YREC7-format model file (header, envelope data, shells, composition in compressed form, rotation) and sets the Model2-only items to defaults.
