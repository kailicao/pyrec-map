## Explanation

**Purpose.** `EQSCVG` evaluates the Saumon–Chabrier–Van Horn (SCV) equation of state for a general composition, by combining its pure-hydrogen, pure-helium and metal tables. The header calls them "the general abundance tables".

**How it fits.**
- **Who calls it:** only [[eqscve.f#EQSCVE|EQSCVE]], when $X$ or $Z$ differs from the envelope values by more than $10^{-5}$.
- **Inputs and outputs:** as for `EQSCVE`: `TL`, `T`, `P`, `BETA`, `X`, `Z` in; `DL`, `D`, `QDT`, `QDP`, `QCP`, `DELA`, `FXION`, `LCALC` out.
- **What it calls:** [[interp.f#INTERP|INTERP]], for four-point Lagrange weights and their derivative weights.
- **Modules:** `SCVEOS_MOD` (the tables `TABLEX`, `TABLEY`, `TABLEZ`, `SMIX`, the grid `TLOGX`, `TABLENV`'s pressure column, and the indices `IDTSCV`, `IDP`), shared with `EQSCVE`, [[eqstat2.f#EQSTAT2|EQSTAT2]] and the setup routines (see `eqscve.f`); `CONSTANTS_MOD` for `CLN`.

**The method.** All interpolation is four-point Lagrange in $\log P_\mathrm{gas}$ and $\log T$ (weights `FP`, `FT`; `FTD` are the weights of the $\log T$ derivative). The searches start from the indices `IDTSCV`, `IDP` left by the last call (of this routine or `EQSCVE`), which only costs time.

> **Question** ([[#L49-L112]]; [[eqscve.f#L83-L148]]). **No smoothing.** Unlike `EQSCVE`, there is no blending when the stencil changes, so the outputs can jump between stencils. Is that acceptable for non-envelope compositions?

> **Question** ([[#L75-L76]]; [[#L109-L112]]). **One pressure grid.** The pressure stencil and its abscissae are taken from `TABLENV`'s row `IDTSCV` and used for all four rows of `TABLEX`, `TABLEY`, `TABLEZ` and `SMIX`. Do all these tables share one pressure grid ([[eqscve.f#q2]])?
1. **Density** by additive volumes, with $\rho_X$, $\rho_Y$, $\rho_Z$ from the three tables (column 4 of `TABLEX`, `TABLEY`, `TABLEZ`):
$$\frac{1}{\rho} = \frac{X}{\rho_X} + \frac{Y}{\rho_Y} + \frac{Z}{\rho_Z}.$$
2. **Derivatives** as volume-weighted means, with weights $w_k = X_k\rho/\rho_k$:
$$Q_{\rho P,0} = \sum_k w_k Q_{\rho P,k}, \qquad Q_{\rho T,0} = \sum_k w_k Q_{\rho T,k}.$$
A comment line before the $Q_{\rho T}$ block ends with the stray string `zdiffOPEOSfinalewkop95zscv1.full`, probably a file name pasted by mistake ([[#L176]]).
3. **Specific heat** from the entropy: with $S = XS_X + YS_Y + S_\mathrm{mix}$ and the tabulated $\partial\ln S_k/\partial\ln T$,
$$c_{P,0} = XS_X\frac{\partial\ln S_X}{\partial\ln T} + YS_Y\frac{\partial\ln S_Y}{\partial\ln T} + S_\mathrm{mix}\frac{\partial\ln S_\mathrm{mix}}{\partial\ln T} + Z\left(\frac{\partial U_Z}{\partial T} + \frac{P_\mathrm{gas}Q_{\rho T,Z}^2}{Q_{\rho P,Z}\,\rho_Z T}\right),$$
then $\partial U/\partial T = c_{P,0} - P_\mathrm{gas}Q_{\rho T,0}^2/(Q_{\rho P,0}\,\rho T)$. The total entropy `S0` is computed but never read: unused? ([[#L234]]).

    > **Question** ([[#L218-L234]]; [[setscv.f#L53-L54]]; [[setscv.f#L90-L94]]). **The mixing entropy's composition.** `SMIX` is tabulated by `SETSCV` for the envelope's hydrogen fraction (`Y = 1.0D0-XENV`), but this routine serves compositions other than the envelope's. Is the envelope's $S_\mathrm{mix}$ meant to stand for the point's, and how large is the difference where $X$ differs most from `XENV`?
4. **Radiation** is added as in `EQSCVE`: $Q_{\rho P} = Q_{\rho P,0}/\beta$, $\chi_T = -\beta Q_{\rho T,0}/Q_{\rho P,0} + 4(1-\beta)$, $Q_{\rho T} = -\chi_T Q_{\rho P}$, $\partial U/\partial T \mathrel{+}= 12P_\mathrm{rad}/(\rho T)$, and
$$c_P = \frac{\partial U}{\partial T} + \frac{P\,Q_{\rho T}^2}{Q_{\rho P}\,\rho T},\qquad \nabla_\mathrm{ad} = -\frac{P\,Q_{\rho T}}{\rho T\,c_P}.$$
5. **Ionization fractions** as in `EQSCVE` (with its bug 1, see bug 1 below).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/SCVEOS/` to `SCVEOS_MOD`, where the index `IDT` is now `IDTSCV`; `/CONST1/`, `/CONST2/` to `CONSTANTS_MOD`), the unused `/COMP/` removed, `IMPLICIT NONE`.

## Bugs, by priority

1. **(a)** **H$_2$ counted as one hydrogen nucleus**, as in `EQSCVE` ([[eqscve.f#b1]]). ([[#L326]]) The denominator `XTF_H2 + XTF_H1 + XTF_HP` counts each H$_2$ molecule once, though it holds two hydrogen nuclei and the comment asks for "the fraction XHP of hydrogen nuclei that are singly ionized" ([[#L323]]), so `FXION(1)` is too large wherever H$_2$ is present. Only with `LSCV` (off by default, [[nmlpar_mod.f#L258]]), for compositions other than the envelope's. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to count the two hydrogen nuclei of each H2 molecule.
          XHP = XTF_HP / (2D0*XTF_H2 + XTF_H1 + XTF_HP)
    ```

2. **(d)** **The logarithm of a zero mixing entropy.** ([[#L231-L233]]; [[setscv.f#L70-L71]]) $\partial\ln S_\mathrm{mix}/\partial\ln T$ is taken from `LOG10` of the interpolated `SMIX` values at the four temperatures. `SETSCV` sets `SMIX` to 0 where the hydrogen or helium number density is zero, that is, for an envelope with `XENV` = 0 or 1; there `LOG10` returns $-\infty$ (or NaN for a negative value from the interpolation), and `QSMT`, then $c_P$ and $\nabla_\mathrm{ad}$, are not finite. Not reached for ordinary compositions. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to skip the mixing-entropy term where SMIX is not
    C positive.
          IF(MIN(TEMP(1,3),TEMP(2,3),TEMP(3,3),TEMP(4,3)).GT.0.0D0)THEN
             QSMT = FTD(1)*LOG10(TEMP(1,3)) + FTD(2)*LOG10(TEMP(2,3))
         *        + FTD(3)*LOG10(TEMP(3,3))
         *        + FTD(4)*LOG10(TEMP(4,3))
          ELSE
             QSMT = 0.0D0
          ENDIF
    ```

### EQSCVG

SCV equation of state for any $X$, $Z$ by additive volumes, with $c_P$ from the tabulated entropies (equations above).
