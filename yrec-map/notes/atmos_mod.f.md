## Explanation

**Purpose.** `ATMOS_MOD` holds one number, `HRAS` $= \mathrm{HRA}(\tfrac23)$, the $T(\tau)$ relation at $\tau = 2/3$. It replaces `COMMON/ATMOS/` (MHP via Claude, 10/14/26).

**Who sets it, who reads it.** [[setups.f#SETUPS|`SETUPS`]] sets it once, from [[hra.f#HRA|`HRA`]]; [[envint.f#ENVINT|`ENVINT`]] and [[qatm.f#QATM|`QATM`]] use $\log T = \log T_\mathrm{eff} + \mathrm{HRA}(\tau) - \texttt{HRAS}$, so that $T = T_\mathrm{eff}$ at $\tau = 2/3$.

**Changed since `rp_1`.** New file: `COMMON/ATMOS/` as a module.
