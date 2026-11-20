## Explanation

**Purpose.** `ATMOS_MOD` holds one number, `HRAS` $`= \mathrm{HRA}(\tfrac23)`$, the $`T(\tau)`$ relation at $`\tau = 2/3`$. It replaces `COMMON/ATMOS/` (MHP via Claude, 10/14/26).

**Who sets it, who reads it.** [`SETUPS`](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L16-L396) sets it once, from [`HRA`](hra.f.md#hra); [`QATM`](https://github.com/yreclab/yrec/blob/7be4133/src/qatm.f#L6-L125) uses $`\log T = \log T_\mathrm{eff} + \mathrm{HRA}(\tau) - \texttt{HRAS}`$, so that $`T = T_\mathrm{eff}`$ at $`\tau = 2/3`$; [`ENVINT`](envint.f.md#envint) uses it at $`\tau = 2/3`$ itself (with `KTTAU` = 2).

**Changed since `rp_1`.** New file: `COMMON/ATMOS/` as a module.
