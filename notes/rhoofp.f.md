## Explanation

**Purpose.** Inverts the OPAL equation of state (the original tables): given the hydrogen abundance $X$, the temperature $T_6$ and a pressure $P$, it finds the density $\rho$ such that $P(\rho, T_6, X) = P$. The versions for the 2001 and 2006 tables are [[rhoofp01.f#RHOOFP01|`RHOOFP01`]] and [[rhoofp06.f#RHOOFP06|`RHOOFP06`]].

**How it fits.**
- **Who calls it:** [[oeqos.f#OEQOS|`OEQOS`]], which works in pressure and temperature and needs the density.
- **What it calls:** [[esac.f#ESAC|`ESAC`]], for $P(\rho)$ at each trial density (its result is in `EOS(1)` of `/E/`). On the first use (`ITIME` in `/LREADCO/` not yet set), it first calls `ESAC` once at a fixed point ($X = 0.5$, $T_6 = 1$, $\rho = 0.001$) so that the tables get read.
- **COMMON:** `/A/` (the tables and grids `XZ`, `T6LIST`, `RHO`, `XA`, read by [[readco.f#READCO|`READCO`]]), `/B/`, `/E/`, `/LREADCO/`, `/LUOUT/`.
- **Output:** the function's value, $\rho$, or $-999$ when it fails. `OEQOS` tests for it (`R` $\le -998$) and then takes its error return (`RETURN 1`); [[oeqos01.f#OEQOS01|`OEQOS01`]] and [[oeqos06.f#OEQOS06|`OEQOS06`]] do the same with the other two versions.

**The method.**
1. Find the bracketing composition index `MLO` in `XA` and temperature index `KLO` in `T6LIST(1,·)`, by bisection.
2. Estimate the table's pressure range at that temperature from the first stored quantity, which this code treats as $P/(\rho T_6)$ (our reading of `XZ(…,1,…)*T6*RHO`):
   $$P_\mathrm{max} = \texttt{XZ}(\cdot,1,k,n_k)\,T_6\,\rho_{n_k} + I_\mathrm{rad}\,\tfrac43\tfrac{\sigma}{c}T_6^4,\qquad P_\mathrm{min} = \texttt{XZ}(\cdot,1,k,1)\,T_6\,\rho_1 + I_\mathrm{rad}\,\tfrac43\tfrac{\sigma}{c}T_6^4,$$
   with $n_k$ = `NRA(KLO)`, the last density index at that temperature. If $P > 1.25\,P_\mathrm{max}$ or $P < P_\mathrm{min}$, it fails.
3. First guess $\rho_1 = \rho_{n_k} P/P_\mathrm{max}$; a second guess five times larger (capped at $\rho_{n_k}$) or five times smaller (floored at $10^{-14}$), depending on the side.
4. Up to 11 steps of the secant method, keeping a bracket (regula falsi):
   $$\rho_3 = \rho_1 + (\rho_2 - \rho_1)\,\frac{P - P_1}{P_2 - P_1},$$
   until $|P_3 - P|/P < 5\times10^{-8}$.

The radiation pressure is not subtracted (`PR` = 0; the line that would compute it is commented out), and `ESAC` is called with `IRAD`, so $P$ is compared with the total pressure when `IRAD` is 1.

**Design.** Failures (out of the table, no convergence, an error return from `ESAC`) all return $-999$ silently; the messages are commented out. The edge `NRA` is a hard-coded `DATA` list, the same as `KRA` in [[readco.f#READCO|`READCO`]].

**KC's changes.** The unused argument `ZTAB` was removed from the function and from its calls to `ESAC` (KC 2025-05-31).

## Questions for the experts

1. **The extra factor 1.25.** The upper check allows $P$ up to $1.25\,P_\mathrm{max}$, beyond the table's edge, while the second guess is capped at the edge density. What happens in `ESAC` for $P$ between $P_\mathrm{max}$ and $1.25\,P_\mathrm{max}$?
2. **Few iterations, tight tolerance.** Eleven secant steps toward $5\times10^{-8}$; in [[rhoofp06.f#RHOOFP06|`RHOOFP06`]] the tolerance was relaxed to $10^{-5}$ in 2025 because of a crash. Should the same change be made here and in `RHOOFP01`?
