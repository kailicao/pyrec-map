## Explanation

**Purpose.** The interface to the 2006 OPAL equation of state ("LLP, October 17, 2006"), with the same arguments and outputs as [[oeqos.f#OEQOS|OEQOS]] and [[oeqos01.f#OEQOS01|OEQOS01]]. Its inline comments document the entries of `EOS` it uses: `EOS(5)` is $c_V = dE/dT_6$ at constant volume, `EOS(6)` is $\partial\log P/\partial\log\rho$ at constant $T_6$, `EOS(7)` is $\partial\log P/\partial\log T_6$ at constant $\rho$, `EOS(8)` is $\Gamma_1$, and `EOS(9)` is $\Gamma_2/(\Gamma_2-1)$.

**How it fits.**
- **Inputs:** `T10` $=\log T$, `P10` $=\log P$, `XC`, `Z`; the tables read by [[readcoeos06.f#READCOEOS06|READCOEOS06]].
- **Who calls it:** [[eqstat2.f#EQSTAT2|EQSTAT2]].
- **What it calls:** [[rhoofp06.f#RHOOFP06|RHOOFP06]], [[esac06.f#ESAC06|ESAC06]] (`IORDER = 9`) and [[mu.f#MU|MU]].
- **Outputs:** as `OEQOS`.
- **COMMON blocks:** `/EEOS06/` (the result `EOS(10)`; shared with ESAC06, RADSUB06, READCOEOS06, RHOOFP06, T6RINTEOS06 and [[calcad.f#CALCAD|CALCAD]]), `/CONST2/`, `/LUOUT/`; `/COMP/`, `/CTLIM/`, `/CONST1/`, `/CCOUT2/` are declared but not used.

**The method.**
1. **Density.** From $T$ and $P$ (given as logs `T10`, `P10`), with $T_6 = T/10^6$ K and $P_{12} = P/10^{12}$ dyn cm⁻², the table routine finds $\rho(P, T, X)$ (`RHOOFP…`), with radiation included (`IRAD = 1`). A value $\le -998$ means failure.
2. **Thermodynamics.** The table routine `ESAC…` fills the array `EOS` at $(X, T_6, \rho)$. From it:
$$\texttt{QDP} = \left(\frac{\partial\ln\rho}{\partial\ln P}\right)_T = \frac{1}{\chi_\rho},\qquad \texttt{QDT} = \left(\frac{\partial\ln\rho}{\partial\ln T}\right)_P = -\frac{\chi_T}{\chi_\rho},$$
$$c_P = 10^{6}\,\frac{c_V\,\Gamma_1}{\chi_\rho}\ \ (\texttt{QCP};\ c_V\ \text{per}\ 10^6\ \mathrm{K}\ \text{in the table}),\qquad \nabla_\mathrm{ad} = \frac{\Gamma_2 - 1}{\Gamma_2}\ \ (\texttt{DELA}),$$
where $\chi_\rho = (\partial\ln P/\partial\ln\rho)_T$, $\chi_T = (\partial\ln P/\partial\ln T)_\rho$.
3. **Radiation.** $1-\beta = aT^4/(3P)$, coded as `BETA14` $= 2.521971383\times10^{-3}\,T_6^4/P_{12}$; `BETA` $=\beta$, `BETAI` $= 1/\beta$.
4. **Mean molecular weight.** `RMU` $= \beta P/(\rho T)$; [[mu.f#MU|MU]] gives the ion and electron terms `AMU` and `EMU`; if `EMU` $\le 0$, it is set to zero and `AMU` $=$ `RMU`$/\mathcal{R}$.

The alternate return (`RETURN 1`) tells the caller to fall back on another equation of state when the point is outside the table or the table fails.

**Range.** $0.00187 \le T_6 \le 200$.

**KC's changes.** 2025-05-31: the unused argument `ZTAB` removed from the calls to `RHOOFP06` and `ESAC06`.

## Questions for the experts

1. **The pressure check.** As in `OEQOS01`, the check that the table reproduces the input pressure is commented out, while `OEQOS` stops on it.
2. **Unused parameters.** `MX`, `NR`, `NT` (the table's dimensions; `NT = 197` here, 191 in `OEQOS01`), `IVARX`, `CNVS` and `ZERO` are declared but not used in this routine.
