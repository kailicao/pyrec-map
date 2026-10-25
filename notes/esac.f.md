## Explanation

**Purpose.** `ESAC` interpolates the OPAL 1995 equation-of-state tables in hydrogen abundance $X$, temperature $T_6$ and density $\rho$, and returns the pressure, energy, specific heat and adiabatic exponents. Its header (from the OPAL distribution) describes the scheme: quadratic interpolation in $X$, then in $\rho$ and $T_6$, "smoothed by mixing overlapping quadratics".

**How it fits.**
- **Who calls it:** [[oeqos.f#OEQOS|OEQOS]] (the YREC wrapper for OPAL 1995, called from [[eqstat2.f#EQSTAT2|EQSTAT2]]) and [[rhoofp.f#RHOOFP|RHOOFP]] (which inverts $P(\rho)$ to find $\rho$).
- **Inputs:** `XH` ($X$), `T6` ($T/10^6$ K), `R` ($\rho$ in g cm$^{-3}$), `IORDER` (how many quantities to compute), `IRAD` (1 to add radiation).
- **What it calls:** [[readco.f#READCO|READCO]] (reads the tables, on the first call only), [[quad.f#QUAD|QUAD]] (quadratic interpolation in $X$), [[t6rinterp.f#T6RINTERP|T6RINTERP]] (the 2D interpolation in $T_6$, $\rho$), [[gmass.f#GMASS|GMASS]] (moles and mass of the mixture) and [[radsub.f#RADSUB|RADSUB]] (radiation).
- **Outputs:** in `/E/`: `EOS(1..10)`, with (per the header) EOS(1) pressure in Mbar, EOS(2) energy in $10^{12}$ erg g$^{-1}$, EOS(5) $c_V$, EOS(6) $\partial\ln P/\partial\ln\rho|_T$, EOS(7) $\partial\ln P/\partial\ln T|_\rho$, EOS(8) $\Gamma_1$, EOS(9) $\Gamma_2/(\Gamma_2-1)$, EOS(10) $\Gamma_3 - 1$. EOS(2)–(4) are marked "YCK NO USE". Alternate return 1 if the point is outside the table or in its empty region.
- **COMMON blocks:** `/A/` (the tables `XZ`, the grids `T6LIST`, `RHO`, `T6A`, `XA`, and workspace), shared with `READCO`, `RHOOFP`, `T6RINTERP`, `BLOCK_DATA` and [[eqbound.f#EQBOUND|EQBOUND]]; `/AA/` (workspace), with `READCO`, `T6RINTERP`, `BLOCK_DATA`; `/B/` (`ZZ`, `INDEX`, `IRI`, `NTA`), with `READCO`, `RADSUB`, `RHOOFP`, `BLOCK_DATA`; `/BB/` (the indices `L1`…`K4`, `IP`, `IQ`), with `T6RINTERP` only; `/E/` (the output), with `OEQOS`, `RADSUB`, `READCO`, `RHOOFP`, `T6RINTERP`; `/EE/` (workspace), with `READCO` and `T6RINTERP`. `/LREADCO/` holds `ITIME`, the "already initialized" flag, shared with [[esac01.f#ESAC01|ESAC01]], [[esac06.f#ESAC06|ESAC06]] and the `RHOOFP*` routines.

**The method.**
1. On the first call (`ITIME` ≠ 12345678), read the tables and check that $X + Z \le 1$; if not, the run stops. It also stops (label 66 and the check before it) if the tables' $Z$ values differ; only the two cases below use the alternate return.
2. Out of table (alternate return) if $T_6$ or $\rho$ is outside the grid.
3. Bisection for the indices in $X$ (`MF`…`MI`), $\rho$ (`L1`…`L4`) and $T_6$ (`K1`…`K4`).
4. Check that the stencil avoids the table's empty region, where `XZ` holds values above $10^{30}$, and choose a 3×3 or 4×4 stencil (`IP`, `IQ`). If the 3×3 stencil reaches the empty region but the 2×2 one does not, the stencil is moved back by one in both $T_6$ and $\rho$ and used as 3×3, without a new check; otherwise the routine returns "empty region".
5. For each quantity, interpolate in $X$ with a quadratic through three tables (`QUAD`; its first argument `IS` is 0 on the first point, so that it computes its abscissa factors, and 1 afterwards, so that it reuses them); between two overlapping quadratics, blend them linearly:
$$E = E_{\mathrm{low}}\,w + E_{\mathrm{high}}(1-w), \qquad w = (X_{MH} - X)/(X_{MH} - X_{MG}).$$
Then `T6RINTERP` interpolates in $T_6$ and $\rho$.
6. Pressure and energy are tabulated scaled: $P = \mathrm{EOS}(1)\cdot T_6\rho$ and $E = \mathrm{EOS}(2)\cdot T_6$. Without radiation, $c_V$ is scaled by $n\,R/m$, with $R = 83.1446$ (the gas constant in units of $10^{12}$ erg per mole per $10^6$ K) and the moles $n$ and mass $m$ from `GMASS`; with radiation, `RADSUB` adds the radiation terms.

**KC's changes.** The unused argument `ZTAB` was removed (2025-05-31).

## Questions for the experts

1. **Stencil past the table end.** The empty-region check loops `DO M=MF,MF+3`. With `MF` = 3 and five $X$ tables, it reads `XZ(6,…)`, past the first dimension. `ESAC01` and `ESAC06` loop `M=MF,MF2` instead and also guard `K4`, `L4` against the table's end. Should `ESAC` get the same fixes?
2. **A shared initialization flag.** `ITIME` in `/LREADCO/` is shared by the three OPAL families. If two families were active in one run, only the first would read its tables. [[parmin.f#PARMIN|PARMIN]] allows only one at a time, so this is safe today; is that restriction relied on?
3. **Wrong array checked.** In the second $X$ quadratic (loop 47) the warning tests `ESK` instead of `ESK2`. The same slip is in `ESAC01` and `ESAC06`.
4. **Messages.** The format `IHI,ILO,IMD` has no values to print; the message at label 66 prints `IP,IQ` under the heading `IQ,IP`; `IORDER > 10` writes a message but continues.
5. **Header vs code.** The header says "R=RHO/T6\*\*3", but `R` is the density itself. Unused locals: `XXI`, `RI`, `BLANK`.
6. **Hydrogen-free mixtures.** For $X < 10^{-6}$ the code sets `MH=1` twice (lines 134–135), where `ESAC01` and `ESAC06` set `MF=1` and `MH=1`. `MF` then keeps its bisection value, 0, so the code reads `XZ(0,…)`, `EPL(0,…)` and `ZZ(0)`, outside the arrays. Should the first line read `MF=1`?

### ESAC

Interpolates the OPAL 1995 EOS tables in $X$, $T_6$, $\rho$ (method above); results in `/E/`, alternate return outside the table.
