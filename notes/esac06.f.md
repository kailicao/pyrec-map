## Explanation

**Purpose.** `ESAC06` is [[esac.f#ESAC|ESAC]] for the OPAL 2006 equation-of-state tables: it interpolates them in $X$, $T_6$ and $\rho$ and returns ten thermodynamic quantities. It is a copy of [[esac01.f#ESAC01|ESAC01]] adapted to the larger 2006 table.

**How it fits.**
- **Who calls it:** [[oeqos06.f#OEQOS06|OEQOS06]] (called from [[eqstat2.f#EQSTAT2|EQSTAT2]] when `LOPALE06` is set), [[rhoofp06.f#RHOOFP06|RHOOFP06]], and [[calcad.f#CALCAD|CALCAD]], which calls it directly for every point of the model and envelope (with `IORDER` = 9, `IRAD` = 1) when `LOPALE06` is set; its call for the atmosphere points is commented out.
- **What it calls:** [[readcoeos06.f#READCOEOS06|READCOEOS06]], [[quadeos06.f#QUADEOS06|QUADEOS06]], [[t6rinteos06.f#T6RINTEOS06|T6RINTEOS06]], [[gmass06.f#GMASS06|GMASS06]] and [[radsub06.f#RADSUB06|RADSUB06]].
- **Outputs:** in `/EEOS06/`: EOS(1) $P$, (2) $E$, (3) $S$, (4) $\partial E/\partial\rho|_T$, (5) $c_V$, (6) $\partial\ln P/\partial\ln\rho$, (7) $\partial\ln P/\partial\ln T$, (8) $\Gamma_1$, (9) $\Gamma_2/(\Gamma_2-1)$, (10) $\Gamma_3-1$.
- **COMMON blocks:** `/AEOS06/` (the tables), shared with `READCOEOS06`, `T6RINTEOS06`, `RHOOFP06` and [[eqbound06.f#EQBOUND06|EQBOUND06]]; `/AAEOS06/` and `/EEEOS06/` (workspace), with `READCOEOS06` and `T6RINTEOS06`; `/BEOS06/`, with `READCOEOS06`, `RADSUB06`, `RHOOFP06` and `EQBOUND06`, which reads `NTA` and `NRA` from it; `/BBEOS06/` (the indices), with `T6RINTEOS06` and `EQBOUND06`, which starts its search from `K3`, `L2`; `/EEOS06/` (the output), with `OEQOS06`, `RADSUB06`, `READCOEOS06`, `RHOOFP06`, `T6RINTEOS06` and `CALCAD`. `/LREADCO/` (`ITIME`) is shared with `ESAC` and `ESAC01`.

**The table.** 169 densities and 197 temperatures. Two DATA statements describe its irregular edge: `NTA(l)`, the lowest temperature index for each density, and `NRA(k)`, the highest density index for each temperature.

**The method.** As `ESAC01` (see [[esac.f|esac.f]] for the steps). Differences: `RADSUB06` takes `IRAD` as an argument, the error messages print their indices, and without radiation $c_V$ is EOS(5).

**KC's changes.** The unused argument `ZTAB` was removed (2025-05-31), and the elements of `/BEOS06/` were reordered (2025-05-30).

## Questions for the experts

1. **An argument that is always 1.** The code reads `if (irad .eq. 1) then call radsub06(irad,…) else eos(iri(5)) = …`. So `RADSUB06` is called only when `IRAD` = 1, and its `IRAD` argument is always 1. Is the argument needed?
2. **Edge tables in two places.** `NTA` and `NRA` are hard-coded here; if the table file changes, they must change too. Could `READCOEOS06` derive them from the file?
3. The questions on `ESAC` about the shared `ITIME` flag, the `ESK`/`ESK2` slip and the swapped `IP,IQ` in message 66 apply here too. Also, the check copied from `ESAC01` writes "iorder cannot exceed 9", though this table has ten quantities; the routine continues anyway.

### ESAC06

Interpolates the OPAL 2006 EOS tables in $X$, $T_6$, $\rho$ (as `ESAC01`); results in `/EEOS06/`. Also used by `CALCAD` for the adiabatic exponents of the whole model.
