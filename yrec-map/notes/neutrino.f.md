## Explanation

**Purpose.** The entry point of the neutrino-loss routines added by Grant Newsham (9/06). It sets up a four-species composition (hydrogen, helium, ¹²C, ¹⁶O) and returns the neutrino energy-loss rate `SNU` with its derivatives with respect to temperature and density, `DSNUDT` and `DSNUDD`.

**How it fits.**
- **Inputs:** $T$ (K) and $\rho$ (g cm⁻³), unlogged; $X$, $Y$; `ZC` and `ZO`, which [[engeb.f#ENGEB|ENGEB]] sets to ¹²C + ¹³C and ¹⁶O + ¹⁸O.
- **Who calls it:** only [[engeb.f#ENGEB|ENGEB]], when `LNULOS1` is set and $\log T$ is above the cutoff `TCUT(5)`. ENGEB uses $-$`SNU` as the loss and turns the derivatives into logarithmic ones.
- **What it calls:** [[nulosses.f#NULOSSES|NULOSSES]].
- **Outputs:** `SNU`, `DSNUDT`, `DSNUDD`. The units are those of [[sneut.f#SNEUT|SNEUT]] (probably erg g⁻¹ s⁻¹, as in the Timmes codes it comes from; not stated here).
- **Modules:** none.

**The method.** Nuclei with $(A, Z)$ = (1, 1), (4, 2), (12, 6), (16, 8), mass fractions $(X, Y, X_\mathrm{C}, X_\mathrm{O})$; everything else is done in `NULOSSES`.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

## Questions for the experts

1. **Metals other than C and O.** Neon, nitrogen, iron and the rest of $Z$ are left out, so the four mass fractions sum to less than one, and [[nulosses.f#AZBAR|AZBAR]] does not renormalize them: $\bar A = 1/\sum_i X_i/A_i$ is then too large by the factor $1/\sum_i X_i$, and so is $\bar Z$. Should the fractions be renormalized, or the missing metals added (for example as ¹⁶O)?
