## Explanation

**Purpose.** A thin wrapper, "modified by G. Newsham from codes of N. Itoh & F. Timmes (9/06)": it computes the composition's mean nucleon number $\bar A$ and charge $\bar Z$, and passes them to [[sneut.f#SNEUT|SNEUT]], which computes the neutrino losses. The header notes that only the carbon coefficients are used for bremsstrahlung losses ("the differences for other elements is slight"), and that the cutoff at $0.01\,T_\mathrm{Fermi}$ "is applicable for helium but will need to be amended for carbon and oxygen white dwarfs and cores of AGB stars".

**How it fits.**
- **Who calls it:** [[neutrino.f#NEUTRINO|NEUTRINO]].
- **What it calls:** [[#AZBAR|AZBAR]] and [[sneut.f#SNEUT|SNEUT]].
- **Outputs:** `SNU`, `DSNUDT`, `DSNUDD`. `SNEUT` also returns the derivatives with respect to $\bar A$ and $\bar Z$ (`DSNUDA`, `DSNUDZ`), which are dropped here.

**The method.** With mass fractions $X_i$, nucleon numbers $A_i$ and charges $Z_i$, the molar abundances $Y_i = X_i/A_i$ give
$$\bar A = \frac{1}{\sum_i Y_i},\qquad \bar Z = \bar A \sum_i Z_i\,Y_i .$$

## Questions for the experts

1. **The Fermi-temperature cutoff.** The header says the cutoff at $0.01\,T_\mathrm{Fermi}$ needs amending for C/O white dwarfs and AGB cores. Has this been done in `SNEUT`, or does it still limit the routine to helium cores?

### AZBAR

The mean nucleon number and charge of the mixture (equations above), from Timmes' code.
