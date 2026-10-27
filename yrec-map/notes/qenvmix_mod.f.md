## Explanation

**Purpose.** `QENVMIX_MOD` relays the mixing-length parameter from [[envint.f#ENVINT|`ENVINT`]] to [[qenv.f#QENV|`QENV`]]. Shared by 2 routines. It replaces no `rp_1` block: at `rp_1`, [[tpgrad.f#TPGRAD|`TPGRAD`]] read `CMIXL` from `COMMON/CONST3/`; since `CMIXL` became an argument (9/24/26), QENV must pass it on to `TPGRAD`, but QENV's argument list cannot change, since it is also called as the `DERIV` callback of [[bsstep.f#BSSTEP|`BSSTEP`]] and [[mmid.f#MMID|`MMID`]] (QENV's comment). The relay was a `COMMON/QENVMIX/` first, then this module (MHP via Claude, 10/14/26).

**What its variables hold, who sets them, who reads them.**
- `CMIXLQ`: the mixing-length parameter $\alpha$, set to `ENVINT`'s argument `CMIXL` on every entry to `ENVINT`; read by `QENV`, which passes it to `TPGRAD`.

**Changed since `rp_1`.** New file: a module for `CMIXL`, formerly read from `COMMON/CONST3/`.
