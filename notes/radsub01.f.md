## Explanation

**Purpose.** Adds radiation to the gas equation of state interpolated in the OPAL 2001 tables. The version for the older tables is [[radsub.f#RADSUB|`RADSUB`]], and for the 2006 tables [[radsub06.f#RADSUB06|`RADSUB06`]].

**How it fits.**
- **Who calls it:** [[esac01.f#ESAC01|`ESAC01`]], after the table interpolation, and only when its argument `irad` is 1. Otherwise `ESAC01` itself multiplies $c_V$ (`eos(iri(4))`) by `moles*aprop/tmass`.
- **COMMON:** `/EEOS/` (`ESACT`, `EOS(MV)`; shared with `ESAC01`, [[oeqos01.f#OEQOS01|`OEQOS01`]], [[readcoeos01.f#READCOEOS01|`READCOEOS01`]], [[rhoofp01.f#RHOOFP01|`RHOOFP01`]], [[t6rinteos01.f#T6RINTEOS01|`T6RINTEOS01`]]) and `/BEOS/` (`ZZ`, the index map `IRI`, `INDEX`, `NTA`; shared with `ESAC01`, `READCOEOS01`, `RHOOFP01`).
- **Output:** `EOS(IRI(1..9))` overwritten with the totals.

**The method.** The radiation terms $P_r$, $E_r$, $S_r$ and the totals $P$, $E$, $S$, $\chi_\rho$, $\chi_T$, $c_V$ are those of [[radsub.f#RADSUB|`RADSUB`]] (equations there). Note that the 2001 tables order the quantities differently: here `EOS(IRI(4))` is $c_V$, `IRI(5)` is $\chi_\rho$, `IRI(6)` is $\chi_T$, and `IRI(7..9)` are the three $\Gamma$s. The difference is in the $\Gamma$s: the code computes them twice from the same formulas, once without radiation and once with it, and adds only the difference to the tabulated values:

$$\Gamma_1 \leftarrow \Gamma_{1,\mathrm{tab}} + \bigl[\Gamma_1^{\mathrm{rad}} - \Gamma_1^{\mathrm{no\,rad}}\bigr],$$

and the same for `GAM2PT` and `GAM3PT`. The comment explains why: the computed $c_V$ "is not accurate enough" to give accurate $\Gamma$s directly (eq. 16.16 of Landau and Lifshitz). There is no `UNITF/UNITFOLD` rescaling here, unlike `RADSUB`.

**KC's changes.** The members of `/BEOS/` were reordered so that `ZZ` comes first (KC 2025-05-30); unused constants were removed from the declarations and `DATA` statement (KC 2025-05-31).

## Questions for the experts

1. **Different constants from RADSUB.** `APROP` is 83.14510 here and 83.1446304 in `RADSUB`, and the `UNITF/UNITFOLD` rescaling of `RADSUB` is absent. Are the 2001 tables already in the new units?
2. **Single-precision constants.** The `DATA` statement sets `sigmacc` and `aprop` with single-precision literals (`1.8914785e-3`, `83.14510`, no `D` exponent), although both are REAL*8 by the `IMPLICIT` statement, so they keep only about seven significant digits. [[radsub.f#RADSUB|`RADSUB`]] and [[radsub06.f#RADSUB06|`RADSUB06`]] write them with `D`. Should these be `D0` constants?
