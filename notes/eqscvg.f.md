## Explanation

**Purpose.** `EQSCVG` evaluates the Saumon–Chabrier–Van Horn (SCV) equation of state for a general composition, by combining its pure-hydrogen, pure-helium and metal tables. The header calls them "the general abundance tables".

**How it fits.**
- **Who calls it:** only [[eqscve.f#EQSCVE|EQSCVE]], when $X$ or $Z$ differs from the envelope values by more than $10^{-5}$.
- **Inputs and outputs:** as for `EQSCVE`: `TL`, `T`, `P`, `BETA`, `X`, `Z` in; `DL`, `D`, `QDT`, `QDP`, `QCP`, `DELA`, `FXION`, `LCALC` out.
- **What it calls:** [[interp.f#INTERP|INTERP]], for four-point Lagrange weights and their derivative weights.
- **COMMON blocks:** `/SCVEOS/` (the tables `TABLEX`, `TABLEY`, `TABLEZ`, `SMIX`, the grid `TLOGX`, `TABLENV`'s pressure column, and the indices `IDT`, `IDP`), shared with `EQSCVE`, [[eqstat2.f#EQSTAT2|EQSTAT2]] and the setup routines (see `eqscve.f`). `/COMP/` is declared but not used here.

**The method.** All interpolation is four-point Lagrange in $\log P_\mathrm{gas}$ and $\log T$ (weights `FP`, `FT`; `FTD` are the weights of the $\log T$ derivative).
1. **Density** by additive volumes, with $\rho_X$, $\rho_Y$, $\rho_Z$ from the three tables (column 4 of `TABLEX`, `TABLEY`, `TABLEZ`):
$$\frac{1}{\rho} = \frac{X}{\rho_X} + \frac{Y}{\rho_Y} + \frac{Z}{\rho_Z}.$$
2. **Derivatives** as volume-weighted means, with weights $w_k = X_k\rho/\rho_k$:
$$Q_{\rho P,0} = \sum_k w_k Q_{\rho P,k}, \qquad Q_{\rho T,0} = \sum_k w_k Q_{\rho T,k}.$$
3. **Specific heat** from the entropy: with $S = XS_X + YS_Y + S_\mathrm{mix}$ and the tabulated $\partial\ln S_k/\partial\ln T$,
$$c_{P,0} = XS_X\frac{\partial\ln S_X}{\partial\ln T} + YS_Y\frac{\partial\ln S_Y}{\partial\ln T} + S_\mathrm{mix}\frac{\partial\ln S_\mathrm{mix}}{\partial\ln T} + Z\left(\frac{\partial U_Z}{\partial T} + \frac{P_\mathrm{gas}Q_{\rho T,Z}^2}{Q_{\rho P,Z}\,\rho_Z T}\right),$$
then $\partial U/\partial T = c_{P,0} - P_\mathrm{gas}Q_{\rho T,0}^2/(Q_{\rho P,0}\,\rho T)$.
4. **Radiation** is added as in `EQSCVE`: $Q_{\rho P} = Q_{\rho P,0}/\beta$, $\chi_T = -\beta Q_{\rho T,0}/Q_{\rho P,0} + 4(1-\beta)$, $Q_{\rho T} = -\chi_T Q_{\rho P}$, $\partial U/\partial T \mathrel{+}= 12P_\mathrm{rad}/(\rho T)$, and
$$c_P = \frac{\partial U}{\partial T} + \frac{P\,Q_{\rho T}^2}{Q_{\rho P}\,\rho T},\qquad \nabla_\mathrm{ad} = -\frac{P\,Q_{\rho T}}{\rho T\,c_P}.$$
5. **Ionization fractions** as in `EQSCVE`.

**KC's changes.** Unused arguments and the array `ATOMWT` were removed (2025-05-31).

## Questions for the experts

1. **H$_2$ counted once** in the hydrogen ionization fraction, as in `EQSCVE` (question 1 there).
2. **No smoothing.** Unlike `EQSCVE`, there is no blending when the stencil changes, so the outputs can jump between stencils. Is that acceptable for non-envelope compositions?
3. **One pressure grid.** The searches start from the indices `IDT`, `IDP` left by the last call (of this routine or `EQSCVE`), which only costs time. But the pressure stencil and its abscissae are taken from `TABLENV`'s row `IDT` and used for all four rows of `TABLEX`, `TABLEY`, `TABLEZ` and `SMIX`. Do all these tables share one pressure grid? (Question 3 in `EQSCVE`.)
4. **A stray string.** A comment line before the $Q_{\rho T}$ block ends with `zdiffOPEOSfinalewkop95zscv1.full`, probably a file name pasted by mistake.
5. **Logarithm of $S_\mathrm{mix}$.** $\partial\ln S_\mathrm{mix}/\partial\ln T$ is taken from $\log_{10}$ of the interpolated `SMIX` values; it fails if `SMIX` is zero or negative anywhere in the stencil. Can it be?

### EQSCVG

SCV equation of state for any $X$, $Z$ by additive volumes, with $c_P$ from the tabulated entropies (equations above).
