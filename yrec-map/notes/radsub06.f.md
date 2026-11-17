## Explanation

**Purpose.** Adds radiation, optionally, to the gas equation of state interpolated in the OPAL 2006 tables. The older versions were `RADSUB` and `RADSUB01` (both removed since `rp_1`).

**How it fits.**
- **Who calls it:** [`ESAC06`](esac06.f.md#esac06), only when its argument `irad` is 1, and it passes `irad` on ([esac06.f, lines 481–485](https://github.com/yreclab/yrec/blob/7be4133/src/esac06.f#L481-L485)); so `irad` is always 1 here, and the branch for `irad` $`= 0`$ never runs (unused?).
- **Modules:** `EOS06MISC_MOD`, which merges the former `/EEOS06/` (`ESACT`, `EOS(MV)`) and `/BEOS06/` (`ZZ`, `IRI`, `INDEX`, `NTA`, `NRA`) with two other blocks; shared with `ESAC06`, [`OEQOS06`](oeqos06.f.md#oeqos06), [`READCOEOS06`](readcoeos06.f.md#readcoeos06), [`RHOOFP06`](rhoofp06.f.md#rhoofp06), [`T6RINTEOS06`](t6rinteos06.f.md#t6rinteos06), [`CALCAD`](calcad.f.md#calcad) and [`EQBOUND06`](eqbound06.f.md#eqbound06). This routine uses `EOS` and `IRI` only.
- **Output:** `EOS(IRI(1..9))` overwritten.

**The method.** As in `RADSUB01` (equations in `RADSUB`; both removed since `rp_1`), with the 2006 order of quantities: `IRI(4)` is $`\partial E/\partial\rho`$, `IRI(5)` is $`c_V`$, `IRI(6)` is $`\chi_\rho`$, `IRI(7)` is $`\chi_T`$, `IRI(8..10)` the $`\Gamma`$s. With `irad` $`\ne 0`$, the radiation terms are added, $`\partial E/\partial\rho`$ becomes $`\partial E_g/\partial\rho - E_r/\rho`$, and the differences (with minus without radiation) are added to $`\Gamma_1`$ and to `GAM2PT`. The line that would add the difference to `eos(iri(10))` ($`\Gamma_3`$, [line 102](https://github.com/yreclab/yrec/blob/7be4133/src/radsub06.f#L102)) is commented out, while `RADSUB01` corrected all three $`\Gamma`$s; it has nothing to correct, since `EOS(10)` is never interpolated (the tables hold nine quantities, [readcoeos06.f, lines 124–126](https://github.com/yreclab/yrec/blob/7be4133/src/readcoeos06.f#L124-L126)) and nothing reads it (settled from the code, Nov 9, 2026). With `irad` $`= 0`$, the routine only rewrites the gas values, with $`c_V`$ multiplied by $`Nk/M`$ (`molenak/tmass`).

**Changed since `rp_1`.** Declarations only: `/EEOS06/` and `/BEOS06/` to `EOS06MISC_MOD`, `IMPLICIT NONE`.
