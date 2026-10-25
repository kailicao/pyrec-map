## Explanation

**Purpose.** `EQSCVE` interpolates the Saumon–Chabrier–Van Horn (SCV) equation of state in its table for the surface (envelope) composition. It returns the density, the thermodynamic derivatives and the ionization fractions of hydrogen and helium. For any other composition it hands the work to [[eqscvg.f#EQSCVG|EQSCVG]], which combines the pure-hydrogen, pure-helium and metal tables.

**How it fits.**
- **Who calls it:** only [[eqstat2.f#EQSTAT2|EQSTAT2]], when `LSCV` is set and $\log T <$ `TSCUT`, right after [[eqsaha.f#EQSAHA|EQSAHA]]. If the point is outside the table (`LCALC` false), the routine returns without touching its outputs, so the `EQSAHA` values stand.
- **Inputs:** `TL`, `T`, `P`, `BETA`, `X`, `Z`. It compares `X`, `Z` with `XENV`, `ZENV` from `/COMP/`.
- **What it calls:** [[kspline.f#KSPLINE|KSPLINE]] and [[ksplint.f#KSPLINT|KSPLINT]] (a four-point natural spline), [[interp.f#INTERP|INTERP]] (four-point Lagrange) and `EQSCVG`.
- **Outputs:** `DL`, `D`, `QDT`, `QDP`, `QCP`, `DELA`, `FXION`, `LCALC`.
- **COMMON blocks:** `/SCVEOS/` holds the tables (`TLOGX`, `TABLENV` for the envelope mixture, `TABLEX`, `TABLEY`, `TABLEZ`, `SMIX`, `NPTSX`), the flag `LSCV` and the last indices `IDT`, `IDP`; it is filled by [[setscv.f#SETSCV|SETSCV]] and shared with `EQSCVG`, [[eqstat.f#EQSTAT|EQSTAT]], `EQSTAT2`, [[calcad.f#CALCAD|CALCAD]], `PARMIN`, `SETUPS`, `STARIN`, `PUTSTORE` and `WRTLST`. `/COMP/` gives the envelope composition.

**The method.**
1. The table is in $\log T$ and $\log P_\mathrm{gas}$, with $P_\mathrm{gas} = \beta P$. Out of table if $\log T$ is outside `TLOGX`, if $\log P_\mathrm{gas} < 4$, or if it is above the last pressure of the stencil's lowest-temperature row.
2. Find the 4×4 stencil (`IDT`, `IDP`), starting from the last one. For each of the 4 temperatures, a natural spline in $\log P_\mathrm{gas}$ gives five quantities (columns 2–6 of `TABLENV`: $\log\rho$, $Q_{\rho T}$, $Q_{\rho P}$, $c_P$, $\partial U/\partial T$); a second spline in $\log T$ gives their values at the point.
3. **Smoothing at stencil changes.** When the point is within `TOLST` = 0.032 in $\log T$ (or `TOLSP` = 0.08 in $\log P$) of the edge of the middle interval, the routine also interpolates on the stencil shifted by one, and blends the two linearly (`FST`, `FSP`), so that the result does not jump when the stencil changes.
4. **Radiation.** The tables hold the gas alone. With $Q_{\rho P,0}$ and $Q_{\rho T,0}$ from the table,
$$Q_{\rho P} = \frac{Q_{\rho P,0}}{\beta},\qquad \chi_T = \beta\left(-\frac{Q_{\rho T,0}}{Q_{\rho P,0}}\right) + 4(1-\beta),\qquad Q_{\rho T} = -\chi_T\,Q_{\rho P},$$
$$\frac{\partial U}{\partial T} \mathrel{+}= \frac{4}{T}\cdot\frac{3P_\mathrm{rad}}{\rho},\qquad c_P = \frac{\partial U}{\partial T} - \frac{P}{\rho T}Q_{\rho T}\chi_T,\qquad \nabla_\mathrm{ad} = -\frac{P\,Q_{\rho T}}{\rho T\,c_P}.$$
5. **Ionization.** From the pure-hydrogen table `TABLEX` and the pure-helium table `TABLEY` (columns 2 and 3, Lagrange interpolation on the same stencil and pressure abscissae as `TABLENV`), the particle fractions of H$_2$, H, He and He$^+$; charge and particle conservation give the rest, and
$$x_{\mathrm{H}^+} = \frac{n_{\mathrm{H}^+}}{n_{\mathrm{H}_2} + n_\mathrm{H} + n_{\mathrm{H}^+}}, \quad x_{\mathrm{He}^+} = \frac{n_{\mathrm{He}^+}}{n_\mathrm{He} + n_{\mathrm{He}^+} + n_{\mathrm{He}^{++}}},$$
and likewise for He$^{++}$.

**KC's changes.** Unused arguments (`PL`, `BETAI`, `BETA14`, `RMU`, `AMU`, `EMU`, `ETA`) and the unused array `ATOMWT` were removed (2025-05-31).

## Questions for the experts

1. **H$_2$ counted once.** In step 5, the denominator counts each H$_2$ molecule as one particle, but it holds two hydrogen nuclei. The comment says the result is "the fraction of hydrogen nuclei that are singly ionized". Should it be $2n_{\mathrm{H}_2}$?
2. **Mixed EOS outputs.** When SCV succeeds, `EQSTAT2` keeps `RMU`, `EMU` and the second derivatives from `EQSAHA`, while the density comes from SCV. So $\mu$ is no longer consistent with $\rho = \beta P\mu/(RT)$. Is that intended?
3. **One pressure grid for four temperatures.** The pressure abscissae are always taken from the row `IDT` (the lowest temperature of the stencil), also for the other three rows. The ionization step also uses `TABLENV`'s pressures for `TABLEX` and `TABLEY`. That is right only if every row of all three tables has the same pressure grid. Is it so in the SCV tables?
4. **Unused column.** $c_P$ from the table (`TEMPT(4)`, `QCP0`) is interpolated but never used; $c_P$ is rebuilt from $\partial U/\partial T$. Can the interpolation be dropped?
5. **Spline and Lagrange.** The thermodynamic quantities use splines, the ionization fractions Lagrange interpolation without the smoothing of step 3. Is the difference intended?

### EQSCVE

SCV equation of state at the envelope composition: 2D spline interpolation with smoothing at stencil changes, radiation added, ionization fractions from the H and He tables (method above). Hands other compositions to `EQSCVG`.
