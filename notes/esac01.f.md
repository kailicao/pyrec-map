## Explanation

**Purpose.** `ESAC01` is [[esac.f#ESAC|ESAC]] for the OPAL 2001 equation-of-state tables: it interpolates them in $X$, $T_6$ and $\rho$ and returns the pressure, energy, entropy, specific heat and adiabatic exponents. The file carries long comments describing the table's layout.

**How it fits.**
- **Who calls it:** [[oeqos01.f#OEQOS01|OEQOS01]] (called from [[eqstat2.f#EQSTAT2|EQSTAT2]] when `LOPALE01` is set) and [[rhoofp01.f#RHOOFP01|RHOOFP01]].
- **Inputs, outputs, calls:** as `ESAC`, with the 2001 routines [[readcoeos01.f#READCOEOS01|READCOEOS01]], [[quadeos01.f#QUADEOS01|QUADEOS01]], [[t6rinteos01.f#T6RINTEOS01|T6RINTEOS01]], [[gmass01.f#GMASS01|GMASS01]] and [[radsub01.f#RADSUB01|RADSUB01]]. The output is in `/EEOS/`, with nine quantities (the 2001 table has no $\partial E/\partial\rho$): EOS(1) $P$, (2) $E$, (3) $S$, (4) $c_V$, (5) $\partial\ln P/\partial\ln\rho$, (6) $\partial\ln P/\partial\ln T$, (7) $\Gamma_1$, (8) $\Gamma_2/(\Gamma_2-1)$, (9) $\Gamma_3-1$.
- **COMMON blocks:** the 2001 counterparts of ESAC's blocks: `/AEOS/` (the tables), shared with `READCOEOS01`, `T6RINTEOS01`, `RHOOFP01` and [[eqbound01.f#EQBOUND01|EQBOUND01]]; `/AAEOS/` and `/EEEOS/` (workspace), with `READCOEOS01` and `T6RINTEOS01`; `/BEOS/`, with `READCOEOS01`, `RADSUB01` and `RHOOFP01`; `/BBEOS/` (the indices), with `T6RINTEOS01` only; `/EEOS/` (the output), with `OEQOS01`, `RADSUB01`, `READCOEOS01`, `RHOOFP01` and `T6RINTEOS01`. `/LREADCO/` (`ITIME`) is shared with `ESAC` and `ESAC06`.

**The table, per the comments.** Five $X$ values (0, 0.2, 0.4, 0.6, 0.8), 169 densities from $10^{-14}$ to $10^{7}$ g cm$^{-3}$, and up to 191 temperatures from $T_6 = 100$ down to 0.002. About 10% of the table, at high density and low temperature, is empty; `NTA(l)` gives, for each density, the index of the lowest temperature present (set by a DATA statement here).

**The method.** As `ESAC` (see [[esac.f|esac.f]]), with two guards added: the stencil is shrunk to 3 points (`IPU`, `IQU`) when it would pass the last temperature or density, and the empty-region sums loop over `MF..MF2` only. Without radiation, $c_V$ (here EOS(4)) is scaled by $nR/m$ with $R = 83.14511$.

**KC's changes.** The unused argument `ZTAB` was removed (2025-05-31), and the elements of `/BEOS/` were reordered (2025-05-30).

## Questions for the experts

1. **Two values of $R$.** `APROP` is 83.14511 here and 83.1446304 in `ESAC`. Which is meant (the second is the current CODATA value)?
2. **The format with no values.** `write (ISHORT,'(A, " ihi,ilo,imd",3i5)') ID` prints only `ID`; `ESAC06` adds the three indices.
3. The questions on `ESAC` about the shared `ITIME` flag, the `ESK`/`ESK2` slip (line 437) and the swapped `IP,IQ` in message 66 apply here too; `IORDER` above the limit again only writes a message. The table-end and $X < 10^{-6}$ problems of `ESAC` are fixed here.

### ESAC01

Interpolates the OPAL 2001 EOS tables in $X$, $T_6$, $\rho$ (as `ESAC`, with guards at the table's end); results in `/EEOS/`.
