## Explanation

**Purpose.** The interface to the original OPAL equation of state ("implimented by YC, Feb. 21, 1995"): given $\log T$ and $\log P$, it returns the density and the thermodynamic derivatives that the structure equations need. [[oeqos01.f#OEQOS01|OEQOS01]] and [[oeqos06.f#OEQOS06|OEQOS06]] are the same interface for the 2001 and 2006 OPAL tables.

**How it fits.**
- **Inputs:** `T10` $=\log T$, `P10` $=\log P$, the hydrogen abundance `XC` and `Z`; the tables, read earlier by [[readco.f#READCO|READCO]] into the COMMON blocks of the table routines.
- **Who calls it:** [[eqstat2.f#EQSTAT2|EQSTAT2]], which selects the OPAL version.
- **What it calls:** [[rhoofp.f#RHOOFP|RHOOFP]] (density), [[esac.f#ESAC|ESAC]] (the table interpolation, `IORDER = 10`) and [[mu.f#MU|MU]].
- **Outputs:** $T$, $P$, $\rho$ (`D`) and $\log\rho$ (`D10`), `BETA`, `BETAI`, `BETA14`, `RMU`, `AMU`, `EMU`, `QDT`, `QDP`, `QCP`, `DELA`.
- **COMMON blocks:** `/E/` (`EOS(10)`, the result of `ESAC`; shared with ESAC, RADSUB, READCO, RHOOFP, T6RINTERP), `/CONST2/` (`CGAS`), `/LUOUT/`. `/COMP/`, `/CTLIM/`, `/CONST1/` and `/CCOUT2/` are declared but not used.

**The method.**
1. **Density.** From $T$ and $P$ (given as logs `T10`, `P10`), with $T_6 = T/10^6$ K and $P_{12} = P/10^{12}$ dyn cm⁻², the table routine finds $\rho(P, T, X)$ (`RHOOFP…`), with radiation included (`IRAD = 1`). A value $\le -998$ means failure.
2. **Thermodynamics.** The table routine `ESAC…` fills the array `EOS` at $(X, T_6, \rho)$. From it:
$$\texttt{QDP} = \left(\frac{\partial\ln\rho}{\partial\ln P}\right)_T = \frac{1}{\chi_\rho},\qquad \texttt{QDT} = \left(\frac{\partial\ln\rho}{\partial\ln T}\right)_P = -\frac{\chi_T}{\chi_\rho},$$
$$c_P = 10^{6}\,\frac{c_V\,\Gamma_1}{\chi_\rho}\ \ (\texttt{QCP};\ c_V\ \text{per}\ 10^6\ \mathrm{K}\ \text{in the table}),\qquad \nabla_\mathrm{ad} = \frac{\Gamma_2 - 1}{\Gamma_2}\ \ (\texttt{DELA}),$$
where $\chi_\rho = (\partial\ln P/\partial\ln\rho)_T$, $\chi_T = (\partial\ln P/\partial\ln T)_\rho$.
3. **Radiation.** $1-\beta = aT^4/(3P)$, coded as `BETA14` $= 2.521971383\times10^{-3}\,T_6^4/P_{12}$; `BETA` $=\beta$, `BETAI` $= 1/\beta$.
4. **Mean molecular weight.** `RMU` $= \beta P/(\rho T)$; [[mu.f#MU|MU]] gives the ion and electron terms `AMU` and `EMU`; if `EMU` $\le 0$, it is set to zero and `AMU` $=$ `RMU`$/\mathcal{R}$.

The entries used are documented in [[esac.f#ESAC|ESAC]]'s header: `EOS(5)` $c_V$, `EOS(6)` $\chi_\rho$, `EOS(7)` $\chi_T$, `EOS(8)` $\Gamma_1$, `EOS(9)` $\Gamma_2/(\Gamma_2-1)$; `EOS(1)` is the pressure in units of $10^{12}$ dyn cm⁻², which the pressure check below compares with $P_{12}$.

The alternate return (`RETURN 1`) tells the caller to fall back on another equation of state when the point is outside the table or the table fails.

**Range.** $0.005 \le T_6 \le 100$.

**KC's changes.** 2025-05-31: the unused argument `ZTAB` removed from the calls to `RHOOFP` and `ESAC`.

## Questions for the experts

1. **A stale header.** The file's index lists `MU`, `ESAC`, `T6RINTERP`, `READCO`, `QUAD`, `GMASS`, `RADSUB` and `RHOOFP`, which now live in files of their own, and the routine's banner reads "MEQOS".
2. **A hard stop.** If the table's pressure differs from the input by more than $5\times10^{-7}$ (relative), the run stops ("ERROR IN OEQOS PTOT"). In `OEQOS01` and `OEQOS06` this check is commented out. Should the three agree?
3. **`Z` not used.** `Z` is passed only to `MU` (`ZTAB = Z` is set but no longer passed on); the table routines take only $X$, $T_6$ and $\rho$, so the table is used at the $Z$ of the table file. Is the table file chosen for the run's $Z$ elsewhere?
