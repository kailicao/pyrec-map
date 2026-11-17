## Explanation

**Purpose.** `ATMOS_MOD` holds one number, `HRAS` $`= \mathrm{HRA}(\tfrac23)`$, the $`T(\tau)`$ relation at $`\tau = 2/3`$. It replaces `COMMON/ATMOS/` (MHP via Claude, 10/14/26).

**Who sets it, who reads it.** [`SETUPS`](setups.f.md#setups) sets it once, from [`HRA`](hra.f.md#hra); [`ENVINT`](envint.f.md#envint) and [`QATM`](qatm.f.md#qatm) use $`\log T = \log T_\mathrm{eff} + \mathrm{HRA}(\tau) - \texttt{HRAS}`$, so that $`T = T_\mathrm{eff}`$ at $`\tau = 2/3`$.

**Changed since `rp_1`.** New file: `COMMON/ATMOS/` as a module.
