## Explanation

**Purpose.** Writes a stellar model to a text file in the "MODEL2" format (LLP 4/16/03), which YREC can read back as a starting model.

**How it fits.**
- **Inputs:** the model and its global quantities, as arguments: the header values (model number, number of shells `M`, mass, $\log T_\mathrm{eff}$, $\log L$, $\log M$, age, step, inner and outer $\log m$), the physics flags and labels (EOS, atmosphere, opacity, mixture strings), the luminosities by source `TLUMX`, the envelope data (`TRIT`, `TRIL`, `PS`, `TS`, `RS`, `CFENV`), and the shell arrays.
- **Who calls it:** [[wrtlst.f#WRTLST|WRTLST]], for the last model.
- **Who reads its output:** [[starin.f#STARIN|STARIN]], which recognizes the leading `MOD2 ` and calls [[getmodel2.f#GETMODEL2|GETMODEL2]].
- **Output:** the file on unit `IWRITE`; warnings to `ISHORT`.

**The format.** A header line (`MOD2 `, the number format chosen by the age's size); a line of physics flags; a `TLUMX` line of seven luminosities in erg s⁻¹ (pp chains I, II, III, CNO, helium burning, neutrinos, gravitational contraction, by GETYREC7's comment); three `ENV` lines (negative indices if `FTRI < 0`); column titles; then one line per shell: shell, $\log m$, $\log r$, $L$, $\log P$, $\log T$, $\log\rho$, $\Omega$ (unlogged, a change from YREC7 files), the convection flag, and the 15 abundances.

**Design.** If the largest of the luminosities is at most $10^{20}$, they are taken to be in solar units and multiplied by $L_\odot$, in place: the caller's `TLUMX` changes too.

## Questions for the experts

1. **Units guessed from size.** Deciding solar units versus erg s⁻¹ by comparing with $10^{20}$ works for stars, but changes the caller's array as a side effect. Could the caller pass the units instead?
2. **`TLUMX(8)` not written.** The eighth entry is the luminosity of $\alpha$ captures ([[coefft.f#COEFFT|COEFFT]] adds `ECA = EALPCA` to it; [[crrect.f#CRRECT|CRRECT]] counts it with helium burning, `TLUMX(5) + TLUMX(8)`), but only seven are checked, converted and written, so a model read back has no $\alpha$-capture luminosity. Should the format carry it?
