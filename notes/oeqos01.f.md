## Explanation

**Purpose.** The interface to the 2001 OPAL equation of state ("LLP, August 10, 2003"), with the same arguments and outputs as [[oeqos.f#OEQOS|OEQOS]] (the original OPAL tables) and [[oeqos06.f#OEQOS06|OEQOS06]] (the 2006 tables).

**How it fits.**
- **Inputs:** `T10` $=\log T$, `P10` $=\log P$, `XC`, `Z`; the tables read by [[readcoeos01.f#READCOEOS01|READCOEOS01]].
- **Who calls it:** [[eqstat2.f#EQSTAT2|EQSTAT2]].
- **What it calls:** [[rhoofp01.f#RHOOFP01|RHOOFP01]], [[esac01.f#ESAC01|ESAC01]] (`IORDER = 9`, "all 1st and 2nd order data") and [[mu.f#MU|MU]].
- **Outputs:** as `OEQOS`.
- **COMMON blocks:** `/EEOS/` (the result `EOS(10)`; shared with ESAC01, RADSUB01, READCOEOS01, RHOOFP01, T6RINTEOS01), `/CONST2/`, `/LUOUT/`; `/COMP/`, `/CTLIM/`, `/CONST1/`, `/CCOUT2/` are declared but not used.

**The method.**
1. **Density.** From $T$ and $P$ (given as logs `T10`, `P10`), with $T_6 = T/10^6$ K and $P_{12} = P/10^{12}$ dyn cm⁻², the table routine finds $\rho(P, T, X)$ (`RHOOFP…`), with radiation included (`IRAD = 1`). A value $\le -998$ means failure.
2. **Thermodynamics.** The table routine `ESAC…` fills the array `EOS` at $(X, T_6, \rho)$. From it:
$$\texttt{QDP} = \left(\frac{\partial\ln\rho}{\partial\ln P}\right)_T = \frac{1}{\chi_\rho},\qquad \texttt{QDT} = \left(\frac{\partial\ln\rho}{\partial\ln T}\right)_P = -\frac{\chi_T}{\chi_\rho},$$
$$c_P = 10^{6}\,\frac{c_V\,\Gamma_1}{\chi_\rho}\ \ (\texttt{QCP};\ c_V\ \text{per}\ 10^6\ \mathrm{K}\ \text{in the table}),\qquad \nabla_\mathrm{ad} = \frac{\Gamma_2 - 1}{\Gamma_2}\ \ (\texttt{DELA}),$$
where $\chi_\rho = (\partial\ln P/\partial\ln\rho)_T$, $\chi_T = (\partial\ln P/\partial\ln T)_\rho$.
3. **Radiation.** $1-\beta = aT^4/(3P)$, coded as `BETA14` $= 2.521971383\times10^{-3}\,T_6^4/P_{12}$; `BETA` $=\beta$, `BETAI` $= 1/\beta$.
4. **Mean molecular weight.** `RMU` $= \beta P/(\rho T)$; [[mu.f#MU|MU]] gives the ion and electron terms `AMU` and `EMU`; if `EMU` $\le 0$, it is set to zero and `AMU` $=$ `RMU`$/\mathcal{R}$.

The alternate return (`RETURN 1`) tells the caller to fall back on another equation of state when the point is outside the table or the table fails.

**Indices.** In this version the entries of `EOS` sit one place lower than in the other two: $\chi_\rho$ is `EOS(5)`, $\chi_T$ `EOS(6)`, $c_V$ `EOS(4)`, $\Gamma_1$ `EOS(7)` and $\Gamma_2/(\Gamma_2-1)$ `EOS(8)`; the lines with the other indices are kept as comments. [[esac01.f#ESAC01|ESAC01]]'s header documents this order (its list has no $dE/d\rho$ entry, which is `EOS(4)` in [[esac.f#ESAC|ESAC]] and [[esac06.f#ESAC06|ESAC06]]).

**Range.** $0.002 \le T_6 \le 100$.

**KC's changes.** 2025-05-31: the unused argument `ZTAB` removed from the calls to `RHOOFP01` and `ESAC01`.

## Questions for the experts

1. **The shifted indices.** `OEQOS01` reads `EOS(4)`–`EOS(8)` where `OEQOS` and `OEQOS06` read `EOS(5)`–`EOS(9)`, as `ESAC01`'s header documents for the 2001 tables. Has this order been checked against the 2001 tables' own documentation?
2. **The pressure check.** The check that the table reproduces the input pressure, a hard stop in `OEQOS`, is commented out here. Intended?
