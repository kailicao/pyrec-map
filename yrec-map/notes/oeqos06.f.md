## Explanation

**Purpose.** The interface to the 2006 OPAL equation of state ("LLP, October 17, 2006"), with the same arguments and outputs as `OEQOS` and `OEQOS01` (removed since `rp_1`); it is now the only OPAL equation of state. Its inline comments document the entries of `EOS` it uses: `EOS(5)` is $c_V = dE/dT_6$ at constant volume, `EOS(6)` is $\partial\log P/\partial\log\rho$ at constant $T_6$, `EOS(7)` is $\partial\log P/\partial\log T_6$ at constant $\rho$, `EOS(8)` is $\Gamma_1$, and `EOS(9)` is $\Gamma_2/(\Gamma_2-1)$.

**How it fits.**
- **Inputs:** `T10` $=\log T$, `P10` $=\log P$, `XC`, `Z`; the tables read by [[readcoeos06.f#READCOEOS06|READCOEOS06]].
- **Who calls it:** [[eqstat2.f#EQSTAT2|EQSTAT2]].
- **What it calls:** [[rhoofp06.f#RHOOFP06|RHOOFP06]], [[esac06.f#ESAC06|ESAC06]] (`IORDER = 9`) and [[mu.f#MU|MU]].
- **Outputs:** $T$, $P$, $\log\rho$ and $\rho$, `BETA`, `BETAI`, `BETA14`, `RMU`, `AMU`, `EMU`, `QDT`, `QDP`, `QCP`, `DELA`, and the alternate return.
- **Modules:** `EOS06MISC_MOD` (the result `EOS(10)`, formerly `/EEOS06/`; shared with ESAC06, RADSUB06, READCOEOS06, RHOOFP06, T6RINTEOS06 and [[calcad.f#CALCAD|CALCAD]]), `CONSTANTS_MOD` (`CGAS`), `IOUNITS_MOD` (`ISHORT`). The unused `/COMP/`, `/CTLIM/`, `/CONST1/` and `/CCOUT2/` of `rp_1` are no longer declared. The parameters `MX`, `MV`, `NR`, `NT` (the table's dimensions, [[#L51]]) are declared but not used here (unused?), and `ZTAB` is set to `Z` ([[#L91]]) but no longer passed on (unused?).

**The method.**
1. **Density.** From $T$ and $P$ (given as logs `T10`, `P10`), with $T_6 = T/10^6$ K and $P_{12} = P/10^{12}$ dyn cm⁻², the table routine finds $\rho(P, T, X)$ (`RHOOFP…`), with radiation included (`IRAD = 1`). A value $\le -998$ means failure.
2. **Thermodynamics.** The table routine `ESAC…` fills the array `EOS` at $(X, T_6, \rho)$. From it:
$$\texttt{QDP} = \left(\frac{\partial\ln\rho}{\partial\ln P}\right)_T = \frac{1}{\chi_\rho},\qquad \texttt{QDT} = \left(\frac{\partial\ln\rho}{\partial\ln T}\right)_P = -\frac{\chi_T}{\chi_\rho},$$
$$c_P = 10^{6}\,\frac{c_V\,\Gamma_1}{\chi_\rho}\ \ (\texttt{QCP};\ c_V\ \text{per}\ 10^6\ \mathrm{K}\ \text{in the table}),\qquad \nabla_\mathrm{ad} = \frac{\Gamma_2 - 1}{\Gamma_2}\ \ (\texttt{DELA}),$$
where $\chi_\rho = (\partial\ln P/\partial\ln\rho)_T$, $\chi_T = (\partial\ln P/\partial\ln T)_\rho$.

    > **Question** ([[#L104-L109]]). **The pressure check.** The check that the table reproduces the input pressure, `EOS(1)` against `P12` to $5\times10^{-7}$, is commented out (as it was in `OEQOS01`, while `OEQOS` stopped on it; both removed since `rp_1`). Since RHOOFP06 now accepts a relative error of $10^{-5}$ ([[rhoofp06.f#L120]]), the check as written would stop runs whose density has converged within that tolerance. Is it left out on purpose, or should it come back as a warning with the looser tolerance?

3. **Radiation.** $1-\beta = aT^4/(3P)$, coded as `BETA14` $= 2.521971383\times10^{-3}\,T_6^4/P_{12}$; `BETA` $=\beta$, `BETAI` $= 1/\beta$.
4. **Mean molecular weight.** `RMU` $= \beta P/(\rho T)$; [[mu.f#MU|MU]] gives the ion and electron terms `AMU` and `EMU`; if `EMU` $\le 0$, it is set to zero and `AMU` $=$ `RMU`$/\mathcal{R}$.

The alternate return (`RETURN 1`) tells the caller to fall back on another equation of state when the point is outside the table or the table fails.

**Range.** $0.00187 \le T_6 \le 200$.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`; the unused parameters `IVARX`, `CNVS` and `ZERO` removed.
