## Explanation

**Purpose.** Builds the equation-of-state table for the envelope's mixture from the SCV (Saumon–Chabrier–Van Horn, by the common block's name `SCVEOS`, "MHP 5/97") tables of pure hydrogen, pure helium and metals, which [[setups.f#SETUPS|`SETUPS`]] has read. It adds the entropy of mixing, and computes by finite differences the derivatives the structure equations need. (The header comment, "evaluate the EOS with the new tables and call eqstat … and compare", describes an earlier purpose; the routine calls neither.)

**How it fits.**
- **Who calls it:** [[starin.f#STARIN|`STARIN`]], once the starting model's envelope composition is known.
- **Inputs, through COMMON:** `/SCVEOS/` (the tables `TABLEX` (hydrogen), `TABLEY` (helium), `TABLEZ` (metals) on a grid of temperatures `TLOGX(63)` and up to 76 pressures `NPTSX(I)`), and `/COMP/` (`XENV`, `ZENV`).
- **What it calls:** [[inter3.f#INTER3|`INTER3`]], three-point Lagrange interpolation weights (`FT`) and their derivatives (`FTD`).
- **Outputs, through COMMON `/SCVEOS/`:** column 12 of `TABLEX` and `TABLEY`, `SMIX` (the entropy of mixing), and `TABLENV(63, 76, 12)`, the mixture's table. It is read by [[eqscve.f#EQSCVE|`EQSCVE`]] and [[eqscvg.f#EQSCVG|`EQSCVG`]], through [[eqstat.f#EQSTAT|`EQSTAT`]], when `LSCV` is true.

**The method.** The table columns are used, in the code's notation, as $\log P$ (1), the ionization fractions (2, 3), $\log\rho$ (4), $\log S$ (5), $\partial\ln\rho/\partial\ln T$ (7), $\partial\ln\rho/\partial\ln P$ (8) and $\partial\ln S/\partial\ln T$ (9); we read this from the formulas.

1. **$dU/dT$ of each pure table** (column 12), from the two expressions for $c_P$ in the comments,
   $$c_P = S\left(\frac{\partial\ln S}{\partial\ln T}\right)_P = \frac{dU}{dT} + \frac{P}{\rho T}\,\frac{(\partial\ln\rho/\partial\ln T)^2}{\partial\ln\rho/\partial\ln P}.$$
2. **Entropy of mixing.** With $Y = 1 - X$ (`XENV`), the mixture's density $\rho_\mathrm{mix} = 1/((1-Y)/\rho_X + Y/\rho_Y)$, the number densities of hydrogen and helium particles and of their electrons from the ionization fractions, and $\beta = (m_H/m_{He})\,Y/(1-Y)$, $\gamma$ the ratio of particles per nucleus, the code computes
   $$S_\mathrm{mix} = \frac{k}{m_H}\,\frac{2(1-Y)}{1+x_2+3x_1}\left[\ln(1+\beta\gamma) - \frac{n_{e,H}}{n}\ln(1+\delta) + \beta\gamma\ln\Bigl(1+\frac{1}{\beta\gamma}\Bigr) - \frac{n_{e,He}}{n}\ln\Bigl(1+\frac1\delta\Bigr)\right],$$
   with $n$ = `TNUM` the sum of the hydrogen and helium number densities (`HNUM` + `HENUM`), $n_{e,H}$, $n_{e,He}$ their electron number densities (`HNUME`, `HENUME`, each floored at 1), $\delta$ (`DE`) the ratio of electrons from helium to those from hydrogen, scaled by $\beta\gamma$ (the last term uses `DEI`, which is $1/\delta$ when both are positive); $x_1$, $x_2$ are `TABLEX(I,J,2)` and `(I,J,3)`. Constants: $m_H$ = `CMH`, $m_{He}$ = `CMHE` (g), $k$ = `CBOLTZ` (erg K$^{-1}$). This is the code's formula; its source is not cited.
3. **The mixture at each $(T, P)$**, with $X$, $Y = 1 - X - Z$, $Z$ from `/COMP/`: densities add as volumes,
   $$\frac1\rho = \frac{X}{\rho_X} + \frac{Y}{\rho_Y} + \frac{Z}{\rho_Z},\qquad \frac{\partial\ln\rho}{\partial\ln P} = \sum_k X_k\frac{\rho}{\rho_k}\left(\frac{\partial\ln\rho}{\partial\ln P}\right)_k,$$
   and the same for $\partial\ln\rho/\partial\ln T$; the entropy is $S = X S_X + Y S_Y + S_\mathrm{mix}$, and $c_P$ follows, with the metals' term added. Stored: `TABLENV(·,·,1..6)` = $\log P$, $\log\rho$, $\partial\ln\rho/\partial\ln T$, $\partial\ln\rho/\partial\ln P$, $c_P$, $dU/dT$.
4. **Derivatives,** by three-point Lagrange differentiation in $\ln T$ and $\ln P$: of $\partial\ln\rho/\partial\ln T$ in $\ln P$ and $\ln T$, of $\partial\ln P/\partial\ln\rho$ in $\ln\rho$, of $\ln c_P$ in $\ln T$, and of $dU/dT$ in $\ln P$ and $\ln T$; stored in columns 7–12.

**KC's changes.** The unused array `ATOMWT` and its `DATA` statement were removed (KC 2025-05-31).

## Questions for the experts

1. **A fix that is undone.** In the derivatives of $dU/dT$ in temperature, the loop sets `QR(K) = TABLENV(ii,jj,6)` with `jj = min(NPTSX(ii),j)` (protection against neighbor rows with fewer pressures), and the next line overwrites it with `QR(K) = TABLENV(IDT+K-1,J,6)`. The second line should probably be removed.
2. **The same protection is missing elsewhere.** `QDTT` (from `TABLENV(IDT..IDT+2, J, 3)`) and `QSMIXT` (from `SMIX(IDT..IDT+2, J)`) also read neighbor temperature rows at index `J`, which may exceed their `NPTSX`. Use `min(NPTSX(ii),j)` there too?
3. **Radiation pressure computed, then not used.** `PRAD` $= a T^4/3$ is added to `P` and `PL`, and the comments describe the corrections for radiation, but `TABLENV(I,J,1)` stores the gas pressure from `TABLEX`, and `PL`, `QPT0` are never used. Where does the code add radiation for the SCV tables (perhaps in `EQSCVE`)?
4. **$Y$ in the entropy of mixing ignores $Z$.** In step 2, $Y = 1 - $ `XENV`, while step 3 uses $Y = 1 - X - Z$. Intended (mixing of hydrogen and helium only)?
5. **Comment versus code.** The list before the derivative loop names "D LN DEL(AD)/D LN P" and "…/D LN T", but the code computes derivatives of $dU/dT$ (`QAP`, `QAT`). The comment "READ IN EQUATION OF STATE TABLES FOR HYDROGEN AND HELIUM" also stands over a loop that reads nothing (the reading is in `SETUPS`). And `QCPP` ($\partial\ln c_P/\partial\ln P$, in the comment's list) is computed but not stored; is it needed downstream?
