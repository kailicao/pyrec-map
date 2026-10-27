## Explanation

**Purpose.** Inverts the OPAL 2006 equation of state: the density for a given $X$, $T_6$ and pressure. It follows the method of `RHOOFP` and `RHOOFP01`, the versions for the original and 2001 tables (both removed since `rp_1`), with a different treatment of radiation.

**How it fits.** Called by [[oeqos06.f#OEQOS06|`OEQOS06`]]; calls [[esac06.f#ESAC06|`ESAC06`]] for each trial density. Modules: `AEOS06_MOD` (tables and grids from [[readcoeos06.f#READCOEOS06|`READCOEOS06`]]) and `EOS06MISC_MOD` (`EOS`, the results of `ESAC06`, and `NRA`, the last density index at each temperature, set by a `DATA` statement in the module and also used by [[eqbound06.f#EQBOUND06|`EQBOUND06`]]). It returns the density, or $-999$.

**The method.**
1. Find the bracketing composition index `MLO` in `XA` and temperature index `KLO` in `T6LIST(1,·)`, by bisection.
2. Estimate the table's pressure range at that temperature from the first stored quantity, read as $P/(\rho T_6)$: $P_\mathrm{max} = \texttt{XZ}(\cdot,1,k,n_k)\,T_6\,\rho_{n_k}$ and $P_\mathrm{min} = \texttt{XZ}(\cdot,1,k,1)\,T_6\,\rho_1$, with $n_k$ = `NRA(KLO)`. If $P_\mathrm{gas} > 1.25\,P_\mathrm{max}$ or $P_\mathrm{gas} < P_\mathrm{min}$, it fails.
3. First guess $\rho_1 = \rho_{n_k} P_\mathrm{gas}/P_\mathrm{max}$; a second guess five times larger (capped at $\rho_{n_k}$) or five times smaller (floored at $10^{-14}$), depending on the side.
4. Up to 11 steps of the secant method, keeping a bracket (regula falsi):
   $$\rho_3 = \rho_1 + (\rho_2 - \rho_1)\,\frac{P_\mathrm{gas} - P_1}{P_2 - P_1}.$$

Failures (out of the table, no convergence, an error return from `ESAC06`) all return $-999$ silently; the messages are commented out.

**Differences from the removed `RHOOFP`.**
- **Radiation.** When `irad` is 1, the radiation pressure is subtracted first,
  $$P_\mathrm{gas} = P - \tfrac43\,\frac{\sigma}{c}\,T_6^4\quad(\text{in Mb}),$$
  and the search matches $P_\mathrm{gas}$ against `ESAC06` called with `irad` = 0 (gas only), with $P_\mathrm{min}$ and $P_\mathrm{max}$ also without radiation. The other two versions matched the total pressure instead.
- **The edge `NRA`** comes from `EOS06MISC_MOD`, not from a local `DATA` list.
- **Tolerance.** Convergence is $|P_3 - P|/P < 10^{-5}$, changed from $5\times10^{-8}$ "to prevent array value eos(5) from growing without bound and crashing the program during certain model runs" (MR 2025-10-10).

**KC's changes.** The unused argument `ZTAB` was removed from the function and its calls to `ESAC06` (KC 2025-05-31; one marker sits, probably by mistake, on the line computing `rhog3`); the members of `/BEOS06/` were reordered (KC 2025-05-30).

**Changed since `rp_1`.** The first-call switch (`ITIME` in `/LREADCO/`) and the call to `ESAC06` at a fixed point that forced the tables to be read are removed (the tables are now read once by `SETEOS06`, from `SETUPS`); `SIGMACC` is a double-precision constant (`1.8914785D-3`), which settles former question 3; `RHOOFP` and `RHOOFP01` are removed, which settles former question 2 (making the three versions agree); COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **The looser tolerance.** The 2025 change accepts a density whose pressure is off by up to $10^{-5}$ relative. Is that accurate enough for the hydrostatic solution, and is the underlying growth of `eos(5)` ($c_V$) understood?
