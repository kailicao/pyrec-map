## Explanation

**Purpose.** Adds radiation to the gas equation of state of the OPAL tables (the older, 1990s version), in the units of the OPAL code. It is the radiation step of [[esac.f#ESAC|`ESAC`]]; [[radsub01.f|`radsub01.f`]] and [[radsub06.f|`radsub06.f`]] are the versions for the OPAL 2001 and 2006 tables.

**How it fits.**
- **Who calls it:** [[esac.f#ESAC|`ESAC`]], after it has interpolated the gas-only quantities in the table, and only when its argument `IRAD` is 1. Otherwise `ESAC` itself multiplies $c_V$ (`EOS(IRI(5))`) by `MOLES*APROP/TMASS` and adds no radiation. `ESAC` is reached from [[eqstat2.f#EQSTAT2|`EQSTAT2`]] through [[oeqos.f#OEQOS|`OEQOS`]] when the old OPAL tables are chosen (`LOPALE`).
- **Inputs:** the arguments $T_6$ (`T6`, temperature in $10^6$ K), $\rho$ (`DENSITY`, g cm$^{-3}$), `MOLES` and `TMASS` (from `ESAC`, used for the heat capacity), and the gas values in `EOS(IRI(1..7))`.
- **COMMON:** `/E/` (`ESACT`, `EOS(10)`: the interpolated EOS quantities, shared with `ESAC`, [[oeqos.f#OEQOS|`OEQOS`]], [[readco.f#READCO|`READCO`]], [[rhoofp.f#RHOOFP|`RHOOFP`]] and [[t6rinterp.f#T6RINTERP|`T6RINTERP`]]), and `/B/` (`ZZ`, the index map `IRI`, `INDEX`, `NTA`; shared with `ESAC`, `READCO`, `RHOOFP` and `BLOCK_DATA`).
- **Output:** it overwrites `EOS(IRI(1..10))` in place with the totals (gas plus radiation), which `ESAC` returns and `OEQOS` uses.

**The method.** The code's units, from its comments: pressure in Mb ($10^{12}$ dyn cm$^{-2}$), energy per mass in Mb cm$^3$ g$^{-1}$, and $T_6$. With $\sigma/c$ in these units (`SIGMACC` $= 1.8914785\times10^{-3}$), the radiation terms are

$$P_r = \tfrac43\,\frac{\sigma}{c}\,T_6^4,\qquad E_r = \frac{3P_r}{\rho},\qquad S_r = \frac{4E_r}{3T_6}.$$

The totals, with "g" for the gas values in `EOS`:

$$P = P_g + P_r,\quad E = E_g + E_r,\quad S = S_g + S_r,\quad \chi_\rho = \chi_{\rho,g}\frac{P_g}{P},\quad \chi_T = \frac{P_g\,\chi_{T,g} + 4P_r}{P},$$

$$c_V = c_{V,g}\,\frac{N k}{M} + \frac{4E_r}{T_6},\qquad \Gamma_3 - 1 = \frac{P\chi_T}{c_V\,\rho\,T_6},\qquad \Gamma_1 = \chi_\rho + \chi_T(\Gamma_3-1),\qquad \frac{\Gamma_2}{\Gamma_2-1} = \frac{\Gamma_1}{\Gamma_3-1}.$$

Here $Nk/M$ is `MOLES*APROP/TMASS` (`APROP` $= 83.1446304$, the gas constant in Mb cm$^3$ per unit $T_6$, by the comment). In the code the last three are `GAM3PT`, `GAM1T` and `GAM2PT`; reading them as $\Gamma_3-1$ and $\Gamma_2/(\Gamma_2-1)$ is our inference from the formulas. The derivative of energy with density becomes $(\partial E/\partial\rho) - E_r/\rho$. Finally $P$ and $S$ are multiplied by `UNITF/UNITFOLD` $= 0.9648575/0.9652$, to convert from the old OPAL units to newer constants.

**KC's changes.** The unused constants `NA` and `K` were removed from the declarations and `DATA` statement (KC 2025-05-31).

## Questions for the experts

1. **Units fix applied to some quantities only.** `PT` and `ST` are multiplied by `REVISE = UNITF/UNITFOLD`, but `ET` and `DEDRHOAT` are not; the author's own comments ("MHP 10/02 EN is never used; should this be ET=ET*REVISE???", and the same for `DEDRHOA`) ask the same question. Should the energy and its derivative be rescaled too? Also, $\chi_\rho$, $\chi_T$ and the $\Gamma$s were computed with the unrescaled pressure.
2. **Direct $\Gamma$s.** Here the $\Gamma$s are computed directly from $c_V$. In [[radsub01.f#RADSUB01|`RADSUB01`]] and [[radsub06.f#RADSUB06|`RADSUB06`]], a comment says this $c_V$ "is not accurate enough", and those versions add only the radiation's difference to the tabulated $\Gamma$s. Should the older tables be treated the same way?
