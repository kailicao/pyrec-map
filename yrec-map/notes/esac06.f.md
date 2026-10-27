## Explanation

**Purpose.** `ESAC06` is `ESAC` (removed since `rp_1`) for the OPAL 2006 equation-of-state tables: it interpolates them in $X$, $T_6$ and $\rho$ and returns ten thermodynamic quantities. It is a copy of `ESAC01` (removed since `rp_1`) adapted to the larger 2006 table. The file also holds `SETEOS06`, the tables' one-time setup.

**How it fits.**
- **Who calls it:** [[oeqos06.f#OEQOS06|OEQOS06]] (called from [[eqstat2.f#EQSTAT2|EQSTAT2]] when `LOPALE06` is set), [[rhoofp06.f#RHOOFP06|RHOOFP06]], and [[calcad.f#CALCAD|CALCAD]], which calls it directly for every point of the model and envelope (with `IORDER` = 9, `IRAD` = 1) when `LOPALE06` is set; its call for the atmosphere points is commented out.
- **Who calls `SETEOS06`:** [[setups.f#SETUPS|SETUPS]], once, when `LOPALE06` is set (the table file is opened by [[parmin.f#PARMIN|PARMIN]]).
- **What it calls:** [[quadeos06.f#QUADEOS06|QUADEOS06]], [[t6rinteos06.f#T6RINTEOS06|T6RINTEOS06]], [[gmass06.f#GMASS06|GMASS06]] and [[radsub06.f#RADSUB06|RADSUB06]]; `SETEOS06` calls [[readcoeos06.f#READCOEOS06|READCOEOS06]].
- **Outputs:** in `EOS06MISC_MOD`'s `EOS`: EOS(1) $P$, (2) $E$, (3) $S$, (4) $\partial E/\partial\rho|_T$, (5) $c_V$, (6) $\partial\ln P/\partial\ln\rho$, (7) $\partial\ln P/\partial\ln T$, (8) $\Gamma_1$, (9) $\Gamma_2/(\Gamma_2-1)$, (10) $\Gamma_3-1$.
- **Modules:** `AEOS06_MOD` (the tables `XZ`, the grids `T6LIST`, `RHO`, `T6A`, `XA`, the X index `MF` and workspace; its member `M` is now `MIDX`), shared with `READCOEOS06`, `T6RINTEOS06`, `RHOOFP06` and [[eqbound06.f#EQBOUND06|EQBOUND06]]; `EEEOS06_MOD` (workspace `EPL`, `XX`), with `READCOEOS06` and `T6RINTEOS06`; `EOS06MISC_MOD`, which merges the former `/EEOS06/` (the output `EOS`, `ESACT`), `/AAEOS06/` (workspace), `/BEOS06/` (`ZZ`, `IRI`, `INDEX`, `NTA`, `NRA`) and `/BBEOS06/` (the indices `L1`…`K4`, `IP`, `IQ`), with `OEQOS06`, `RADSUB06`, `READCOEOS06`, `RHOOFP06`, `T6RINTEOS06`, `CALCAD` and `EQBOUND06` (which reads `NTA`, `NRA` and starts its search from `K3`, `L2`); `IOUNITS_MOD` (`ISHORT`).

**The table.** 169 densities and 197 temperatures. Two DATA statements, now in `EOS06MISC_MOD` (with `INDEX`; `XA` is in `AEOS06_MOD`), describe its irregular edge: `NTA(l)`, the lowest temperature index for each density, and `NRA(k)`, the highest density index for each temperature.

**The method.** As `ESAC01` and `ESAC`, whose steps were:
1. The tables are read once, before the first call, by `SETEOS06` (it maps `INDEX` into `IRI`, copies `XA` into `XX` and calls `READCOEOS06`); each call takes $Z$ from `ZZ(1)`. The run stops if the tables' $Z$ values differ (the check before label 66, and label 66 itself); only the two cases below use the alternate return.
2. Out of table (alternate return, label 62) if $T_6$ or $\rho$ is outside the grid.
3. Bisection for the indices in $X$ (`MF`…`MI`), $\rho$ (`L1`…`L4`) and $T_6$ (`K1`…`K4`).
4. Check that the stencil avoids the table's empty region, where `XZ` holds values above $10^{30}$, and choose a 3×3 or 4×4 stencil (`IP`, `IQ`). If the 3×3 stencil reaches the empty region but the 2×2 one does not, the stencil is moved back by one in both $T_6$ and $\rho$ and used as 3×3, without a new check; otherwise the routine returns "empty region" (label 65).
5. For each quantity, interpolate in $X$ with a quadratic through three tables (`QUADEOS06`; its first argument `IS` is 0 on the first point, so that it computes its abscissa factors, and 1 afterwards); between two overlapping quadratics, blend them linearly:
$$E = E_{\mathrm{low}}\,w + E_{\mathrm{high}}(1-w), \qquad w = (X_{MH} - X)/(X_{MH} - X_{MG}).$$
Then `T6RINTEOS06` interpolates in $T_6$ and $\rho$.
6. Pressure and energy are tabulated scaled: $P = \mathrm{EOS}(1)\cdot T_6\rho$ and $E = \mathrm{EOS}(2)\cdot T_6$. Without radiation, $c_V$, EOS(5), is scaled by $n\,R/m$, with $R = 83.14511$ (the gas constant in units of $10^{12}$ erg per mole per $10^6$ K) and the moles $n$ and mass $m$ from `GMASS06`; with radiation, `RADSUB06` (which takes `IRAD` as an argument) adds the radiation terms. The error messages print their indices.

**KC's changes.** The unused argument `ZTAB` was removed (2025-05-31), and the elements of `/BEOS06/` were reordered (2025-05-30).

**Changed since `rp_1`.** The one-time work (the `ITIME` switch in `/LREADCO/`, the table read, the `INDEX`/`XX` setup) moved to the new `SETEOS06`, called from `SETUPS`; the first-call check $X + Z \le 1$ (label 61) is dropped; the DATA for `XA`, `INDEX`, `NTA`, `NRA` moved into the modules; COMMON blocks to modules (four small ones merged into `EOS06MISC_MOD`, `M` renamed `MIDX`), `IMPLICIT NONE`. The question on the shared `ITIME` flag is settled (the flag is gone), and those on `ESAC` that applied here are now stated on this page.

## Questions for the experts

1. **An argument that is always 1.** The code reads `if (irad .eq. 1) then call radsub06(irad,…) else eos(iri(5)) = …`. So `RADSUB06` is called only when `IRAD` = 1, and its `IRAD` argument is always 1. Is the argument needed?
2. **Edge tables in two places.** `NTA` and `NRA` are hard-coded (in `EOS06MISC_MOD`); if the table file changes, they must change too. Could `READCOEOS06` derive them from the file?
3. **Wrong array checked.** In the second $X$ quadratic (loop 47) the warning tests `ESK` instead of `ESK2`.
4. **Messages.** The message at label 66 prints `IP,IQ` under the heading `IQ,IP`; the check copied from `ESAC01` writes "iorder cannot exceed 9", though this table has ten quantities, and the routine continues anyway.

### ESAC06

Interpolates the OPAL 2006 EOS tables in $X$, $T_6$, $\rho$ (as `ESAC01`); results in `EOS06MISC_MOD`'s `EOS`. Also used by `CALCAD` for the adiabatic exponents of the whole model.

### SETEOS06

The OPAL 2006 tables' one-time setup, moved out of `ESAC06`'s first call: maps `INDEX` into `IRI`, copies `XA` into `XX` and calls `READCOEOS06`. `SETUPS` calls it when `LOPALE06` is set.
