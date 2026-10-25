## Explanation

**Purpose.** Inverts the OPAL 2001 equation of state: the density for a given $X$, $T_6$ and pressure. It is the 2001 version of [[rhoofp.f#RHOOFP|`RHOOFP`]] and follows it line by line (method and equations there); the 2006 version is [[rhoofp06.f#RHOOFP06|`RHOOFP06`]].

**How it fits.** Called by [[oeqos01.f#OEQOS01|`OEQOS01`]]; calls [[esac01.f#ESAC01|`ESAC01`]] for each trial density. COMMON: `/AEOS/` (tables and grids from [[readcoeos01.f#READCOEOS01|`READCOEOS01`]]), `/BEOS/`, `/EEOS/` (`EOS(1)`, the pressure), `/LREADCO/`, `/LUOUT/`. It returns the density, or $-999$.

**Differences from `RHOOFP`.** The grid sizes (191 temperatures, 169 densities) and its own `DATA` list `NRA` of the last density at each temperature.

**KC's changes.** The unused argument `ZTAB` was removed from the function and from its calls to `ESAC01` (KC 2025-05-31); the members of `/BEOS/` were reordered (KC 2025-05-30).

## Questions for the experts

1. **Two edges that disagree.** `NRA` here and `KRA` in [[readcoeos01.f#READCOEOS01|`READCOEOS01`]] (the edge for the ramp in `EQBOUND01`) are meant to describe the same table, but they differ: `NRA` has `…,8*116,6*115,8*113,…` and `KRA` has `…,8*116,9*115,5*113,…`. At three temperatures the two disagree on the last density (115 against 113). Which is right? One list, computed from `NTA` or `ICYCUSE`, would avoid this.
2. **The tolerance.** $5\times10^{-8}$ here; [[rhoofp06.f#RHOOFP06|`RHOOFP06`]] was relaxed to $10^{-5}$ in 2025. Same change here?
