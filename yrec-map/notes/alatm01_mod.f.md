## Explanation

**Purpose.** `ALATM01_MOD` holds the Allard model-atmosphere table, shared by the four Allard routines. It replaces `COMMON/ALATM01/` (MHP via Claude, 10/14/26); the sizes `NGA` = 25 and `NTA` = 250 are private, since each user declares its own.

**What its variables hold, who sets them, who reads them.** All are set by [[alfilein.f#ALFILEIN|`ALFILEIN`]], which reads the table file:
- `TEFFLs(NTA)`, `GLs(NGA)`: the grid in $\log T_\mathrm{eff}$ and $\log g$, with their sizes `nTEFF`, `nGL`.
- `FeHs(NGA)`, `ALPHAs(NGA)`, with `nFeH`, `nALPHA`: the metallicities and $\alpha$-enhancements found in the file, used only within `ALFILEIN` to choose the table.
- `PLs`, `P100Ls`, `T100Ls` (`NTA` × `NGA`): $\log P$ where $T = T_\mathrm{eff}$, and $\log P$ and $\log T$ at $\tau = 100$ (for the option `LALTPTau100`).
- `LOldNextGen`: the file's format, set and not read elsewhere.

Read by [[altabinit.f#ALTABINIT|`ALTABINIT`]] (the table's limits), [[alprint.f#ALPRINT|`ALPRINT`]] and [[alsurfp.f#ALSURFP|`ALSURFP`]] (the interpolation).

**Changed since `rp_1`.** New file: `COMMON/ALATM01/` as a module.
