## Explanation

**Purpose.** Adds radiation, optionally, to the gas equation of state interpolated in the OPAL 2006 tables. The older versions are [[radsub.f#RADSUB|`RADSUB`]] and [[radsub01.f#RADSUB01|`RADSUB01`]].

**How it fits.**
- **Who calls it:** [[esac06.f#ESAC06|`ESAC06`]], only when its argument `irad` is 1, and it passes `irad` on.
- **COMMON:** `/EEOS06/` (`ESACT`, `EOS(MV)`; shared with `ESAC06`, [[oeqos06.f#OEQOS06|`OEQOS06`]], [[readcoeos06.f#READCOEOS06|`READCOEOS06`]], [[rhoofp06.f#RHOOFP06|`RHOOFP06`]], [[t6rinteos06.f#T6RINTEOS06|`T6RINTEOS06`]] and [[calcad.f#CALCAD|`CALCAD`]]) and `/BEOS06/` (`ZZ`, `IRI`, `INDEX`, `NTA`, `NRA`; shared with `ESAC06`, `READCOEOS06`, `RHOOFP06` and [[eqbound06.f#EQBOUND06|`EQBOUND06`]]).
- **Output:** `EOS(IRI(1..9))` overwritten.

**The method.** As in [[radsub01.f#RADSUB01|`RADSUB01`]] (equations in [[radsub.f#RADSUB|`RADSUB`]]), with the 2006 order of quantities: `IRI(4)` is $\partial E/\partial\rho$, `IRI(5)` is $c_V$, `IRI(6)` is $\chi_\rho$, `IRI(7)` is $\chi_T$, `IRI(8..10)` the $\Gamma$s. With `irad` $\ne 0$, the radiation terms are added, $\partial E/\partial\rho$ becomes $\partial E_g/\partial\rho - E_r/\rho$, and the differences (with minus without radiation) are added to $\Gamma_1$ and to `GAM2PT`. With `irad` $= 0$, the routine only rewrites the gas values, with $c_V$ multiplied by $Nk/M$ (`molenak/tmass`).

**KC's changes.** The members of `/BEOS06/` were reordered so that `ZZ` comes first (KC 2025-05-30); unused constants were removed from the declarations and `DATA` statement (KC 2025-05-31).

## Questions for the experts

1. **$\Gamma_3$ not corrected.** The line that would add the radiation's difference to `eos(iri(10))` ($\Gamma_3$) is commented out, while `RADSUB01` corrects all three $\Gamma$s. Is this deliberate?
2. **The `irad = 0` branch.** `ESAC06` calls this routine only when `irad` is 1, so the branch for `irad = 0` never runs. Is it kept for another caller, or can it be removed?
