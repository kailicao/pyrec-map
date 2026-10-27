## Explanation

**Purpose.** `HRA` evaluates a polynomial fit to the temperature–optical-depth relation of the Harvard Reference Atmosphere: it takes $\tau$ and returns $\log_{10} T$.

**How it fits.** Called by [[envint.f#ENVINT|`ENVINT`]], [[qatm.f#QATM|`QATM`]] and [[setups.f#SETUPS|`SETUPS`]], where the run uses this $T(\tau)$ relation for the atmosphere. `SETUPS` stores `HRAS` = `HRA(2/3)` (in [[atmos_mod.f#ATMOS_MOD|`ATMOS_MOD`]], formerly COMMON `ATMOS`), and `ENVINT` and `QATM` use $\log T = \log T_\mathrm{eff} + \mathrm{HRA}(\tau) - \texttt{HRAS}$, so the relation is normalised to $T = T_\mathrm{eff}$ at $\tau = 2/3$. No modules, no calls.

**The method.** With $t = \log_{10}\tau$,

$$\log_{10} T = \sum_{k=0}^{9} a_k\, t^k,$$

with $a_0 = 3.8115$, $a_1 = 0.14613$, … , $a_9 = 1.587\times10^{-6}$ (the constants in the code).

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

## Questions for the experts

1. **Range of validity.** The fit is a 9th-degree polynomial in $\log\tau$; over which range of $\tau$ was it fitted? Nothing stops callers from using it outside that range, where such a polynomial can diverge quickly.

### HRA

The polynomial above. The comment "speed this up by putting constants in variables" is an old note. The code sums explicit powers (`TL2`, `TL3`, …), not Horner's scheme; either is cheap.
