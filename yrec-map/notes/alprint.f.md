## Explanation

**Purpose.** A diagnostic print of the Allard atmosphere table: its sizes, its limits, and the three tables ($\log P$ at $T_\mathrm{eff}$, $\log P$ and $\log T$ at $\tau = 100$), one row per $T_\mathrm{eff}$, with each row's valid range in $\log g$.

**How it fits.**
- **Who calls it:** only [[altabinit.f#ALTABINIT|ALTABINIT]], and only when it finds the table bad, just before the run stops.
- **Inputs:** `ALATM01_MOD` (filled by [[alfilein.f#ALFILEIN|ALFILEIN]]) and `ALATM02_MOD` (filled by ALTABINIT).
- **Output:** text to unit `ISHORT` (from `IOUNITS_MOD`).

**Design.** Besides printing, it recomputes `TEFFLmin` and `TEFFLmax` in `ALATM02_MOD`, with the same formulas as ALTABINIT, so it has a (harmless) side effect.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/ALATM01/`, `/ALATM02/`, `/LUOUT/` to `IOUNITS_MOD`; the unused `/ALATM03/` and `/ALATM04/` dropped, though a stray declaration of `LALTPTau100` remains), `IMPLICIT NONE`.

## Questions for the experts

1. **Side effect.** ALPRINT writes `TEFFLmin` and `TEFFLmax` into `ALATM02_MOD`. Is this left over from a time when ALTABINIT did not set them?

### ALPRINT

Prints the Allard table and its auxiliary limits to `ISHORT`.
