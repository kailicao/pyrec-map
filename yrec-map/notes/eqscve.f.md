## Explanation

**Purpose.** `EQSCVE` interpolates the Saumon–Chabrier–Van Horn (SCV) equation of state in its table for the surface (envelope) composition. It returns the density, the thermodynamic derivatives and the ionization fractions of hydrogen and helium. For any other composition it hands the work to [[eqscvg.f#EQSCVG|EQSCVG]], which combines the pure-hydrogen, pure-helium and metal tables.

**How it fits.**
- **Who calls it:** only [[eqstat2.f#EQSTAT2|EQSTAT2]], when `LSCV` is set and $\log T <$ `TSCUT`, right after [[eqsaha.f#EQSAHA|EQSAHA]]. If the point is outside the table (`LCALC` false), the routine returns without touching its outputs, so the `EQSAHA` values stand.

    > **Question** ([[eqstat2.f#L181-L187]]; [[eqsaha.f#L194-L196]]). **Mixed EOS outputs.** When SCV succeeds, `EQSTAT2` keeps `RMU`, `EMU` and the second derivatives from `EQSAHA`, while the density comes from SCV. So $\mu$ is no longer consistent with $\rho = \beta P\mu/(\mathcal{R}T)$ (below the transition band, where `EQSTAT2` does not recompute `RMU`). `RMU` is read later by [[hsubp.f#L74]] and `EMU` by [[sconvec.f#L223]]. Is that intended?

- **Inputs:** `TL`, `T`, `P`, `BETA`, `X`, `Z`. It compares `X`, `Z` with `XENV`, `ZENV` from `/COMP/`.
- **What it calls:** [[kspline.f#KSPLINE|KSPLINE]] and [[ksplint.f#KSPLINT|KSPLINT]] (a four-point natural spline), [[interp.f#INTERP|INTERP]] (four-point Lagrange) and `EQSCVG`.
- **Outputs:** `DL`, `D`, `QDT`, `QDP`, `QCP`, `DELA`, `FXION`, `LCALC`.
- **Modules:** `SCVEOS_MOD` holds the tables (`TLOGX`, `TABLENV` for the envelope mixture, `TABLEX`, `TABLEY`, `TABLEZ`, `SMIX`, `NPTSX`) and the last indices `IDTSCV`, `IDP`; it is filled by [[setscv.f#SETSCV|SETSCV]] and used also by `EQSCVG` and [[setups.f#SETUPS|SETUPS]]. The flag `LSCV` is now in `NMLPAR_MOD`. `COMP_MOD` gives the envelope composition; `CONSTANTS_MOD` the constants.

**The method.**
1. The table is in $\log T$ and $\log P_\mathrm{gas}$, with $P_\mathrm{gas} = \beta P$. Out of table if $\log T$ is outside `TLOGX`, if $\log P_\mathrm{gas} < 4$, or if it is above the last pressure of the stencil's lowest-temperature row.
2. Find the 4×4 stencil (`IDTSCV`, `IDP`), starting from the last one. For each of the 4 temperatures, a natural spline in $\log P_\mathrm{gas}$ gives five quantities (columns 2–6 of `TABLENV`: $\log\rho$, $Q_{\rho T}$, $Q_{\rho P}$, $c_P$, $\partial U/\partial T$); a second spline in $\log T$ gives their values at the point. Column 5, the tabulated $c_P$ (`TEMPT(4)`, `QCP0`), is interpolated but never used, since step 4 rebuilds $c_P$ from $\partial U/\partial T$: unused? ([[#L384]]).

    > **Question** ([[#L102-L103]]; [[#L164-L166]]; [[#L407-L409]]). **One pressure grid for four temperatures.** The pressure abscissae are always taken from the row `IDTSCV` (the lowest temperature of the stencil), also for the other three rows. The ionization step (5) also uses `TABLENV`'s pressures for `TABLEX` and `TABLEY`; `TABLENV`'s pressures are `TABLEX`'s ([[setscv.f#L165]]). That is right only if every row of the tables has the same pressure grid. Is it so in the SCV tables?

3. **Smoothing at stencil changes.** When the point is within `TOLST` = 0.032 in $\log T$ (or `TOLSP` = 0.08 in $\log P$) of the edge of the middle interval, the routine also interpolates on the stencil shifted by one, and blends the two linearly (`FST`, `FSP`), so that the result does not jump when the stencil changes.
4. **Radiation.** The tables hold the gas alone. With $Q_{\rho P,0}$ and $Q_{\rho T,0}$ from the table,
$$Q_{\rho P} = \frac{Q_{\rho P,0}}{\beta},\qquad \chi_T = \beta\left(-\frac{Q_{\rho T,0}}{Q_{\rho P,0}}\right) + 4(1-\beta),\qquad Q_{\rho T} = -\chi_T\,Q_{\rho P},$$
$$\frac{\partial U}{\partial T} \mathrel{+}= \frac{4}{T}\cdot\frac{3P_\mathrm{rad}}{\rho},\qquad c_P = \frac{\partial U}{\partial T} - \frac{P}{\rho T}Q_{\rho T}\chi_T,\qquad \nabla_\mathrm{ad} = -\frac{P\,Q_{\rho T}}{\rho T\,c_P}.$$
5. **Ionization.** From the pure-hydrogen table `TABLEX` and the pure-helium table `TABLEY` (columns 2 and 3, Lagrange interpolation on the same stencil and pressure abscissae as `TABLENV`), the particle fractions of H$_2$, H, He and He$^+$; charge and particle conservation give the rest, and
$$x_{\mathrm{H}^+} = \frac{n_{\mathrm{H}^+}}{n_{\mathrm{H}_2} + n_\mathrm{H} + n_{\mathrm{H}^+}}, \quad x_{\mathrm{He}^+} = \frac{n_{\mathrm{He}^+}}{n_\mathrm{He} + n_{\mathrm{He}^+} + n_{\mathrm{He}^{++}}},$$
and likewise for He$^{++}$ (the code's formula for H$^+$; see bug 1).

    > **Question** ([[#L403-L425]]; [[#L162-L190]]). **Spline and Lagrange.** The thermodynamic quantities use splines, the ionization fractions Lagrange interpolation without the smoothing of step 3. Is the difference intended?

**Changed since `rp_1`.** Declarations (COMMON blocks to modules, `IMPLICIT NONE`); the saved temperature index `IDT` is renamed `IDTSCV` in `SCVEOS_MOD`, and the unused `/NMLPAR/` declaration is removed. The arithmetic is unchanged.

## Bugs, by priority

1. **(a)** **H$_2$ counted as one hydrogen nucleus.** ([[#L463]]; [[setscv.f#L58-L59]]) In step 5 the denominator `XTF_H2 + XTF_H1 + XTF_HP` counts each H$_2$ molecule once, but it holds two hydrogen nuclei, and the comment says the result is "the fraction XHP of hydrogen nuclei that are singly ionized" ([[#L460]]). `SETSCV` counts the nuclei with the factor 2 for the same table columns (its `1+3*TABLEX(I,J,2)+TABLEX(I,J,3)` is twice $2x_{\mathrm{H}_2} + x_\mathrm{H} + x_{\mathrm{H}^+}$). So `FXION(1)` is too large wherever H$_2$ is present; it is read by the conductive opacity ([[condopacpint.f#L39]]) and written to the outputs. Where H$_2$ is abundant, few H nuclei are ionized, so the absolute error is probably small; not traced. Only with `LSCV` (off by default, [[nmlpar_mod.f#L258]]). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to count the two hydrogen nuclei of each H2 molecule.
          XHP = XTF_HP / (2D0*XTF_H2 + XTF_H1 + XTF_HP)
    ```

### EQSCVE

SCV equation of state at the envelope composition: 2D spline interpolation with smoothing at stencil changes, radiation added, ionization fractions from the H and He tables (method above). Hands other compositions to `EQSCVG`.
