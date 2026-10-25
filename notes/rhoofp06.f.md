## Explanation

**Purpose.** Inverts the OPAL 2006 equation of state: the density for a given $X$, $T_6$ and pressure. It follows [[rhoofp.f#RHOOFP|`RHOOFP`]] (method and equations there), with a different treatment of radiation.

**How it fits.** Called by [[oeqos06.f#OEQOS06|`OEQOS06`]]; calls [[esac06.f#ESAC06|`ESAC06`]] for each trial density. COMMON: `/AEOS06/` (tables and grids from [[readcoeos06.f#READCOEOS06|`READCOEOS06`]]), `/BEOS06/` (including `NRA`, the last density index at each temperature, set by a `DATA` statement in [[esac06.f#ESAC06|`ESAC06`]] and also used by [[eqbound06.f#EQBOUND06|`EQBOUND06`]]), `/EEOS06/`, `/LREADCO/`, `/LUOUT/`. It returns the density, or $-999$.

**Differences from `RHOOFP`.**
- **Radiation.** When `irad` is 1, the radiation pressure is subtracted first,
  $$P_\mathrm{gas} = P - \tfrac43\,\frac{\sigma}{c}\,T_6^4\quad(\text{in Mb}),$$
  and the search matches $P_\mathrm{gas}$ against `ESAC06` called with `irad` = 0 (gas only), with $P_\mathrm{min}$ and $P_\mathrm{max}$ also without radiation. The other two versions match the total pressure instead.
- **The edge `NRA`** comes from `/BEOS06/` (set in `ESAC06`), not from a local `DATA` list.
- **Tolerance.** Convergence is $|P_3 - P|/P < 10^{-5}$, changed from $5\times10^{-8}$ "to prevent array value eos(5) from growing without bound and crashing the program during certain model runs" (MR 2025-10-10).

**KC's changes.** The unused argument `ZTAB` was removed from the function and its calls to `ESAC06` (KC 2025-05-31; one marker sits, probably by mistake, on the line computing `rhog3`); the members of `/BEOS06/` were reordered (KC 2025-05-30).

## Questions for the experts

1. **The looser tolerance.** The 2025 change accepts a density whose pressure is off by up to $10^{-5}$ relative. Is that accurate enough for the hydrostatic solution, and is the underlying growth of `eos(5)` ($c_V$) understood?
2. **The `irad` = 0 path of the old versions.** Here radiation is removed before the search; in `RHOOFP` and `RHOOFP01` it is kept on both sides. Both are consistent, but should the three versions be made to agree, so that a change of table does not change the convergence behavior?
3. **A single-precision constant.** `sigmacc` is set by `data sigmacc/1.8914785e-3/`, a single-precision literal (no `D`), so the radiation pressure subtracted here carries only about seven significant digits; [[rhoofp01.f#RHOOFP01|`RHOOFP01`]] has the same `DATA` line, while [[rhoofp.f#RHOOFP|`RHOOFP`]] uses `1.8914785D-3`. Harmless at the present tolerance, but should it be a `D0` constant?
