## Explanation

**Purpose.** `SOUND_MOD` holds the adiabatic exponent $`\Gamma_1`$ at each shell and the switch for the sound-speed output ("MHP 7/96 … for solar model"). Shared by 5 routines. It replaces `COMMON/SOUND/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.**
- `GAM1(JSON)`: $`\Gamma_1 = \chi_\rho c_P/c_V`$ with $`\chi_\rho = 1/(\partial\ln\rho/\partial\ln P)`$ and $`c_V`$ from $`c_P`$ (`QCP`), computed by [`COEFFT`](coefft.f.md#coefft) at every shell ("JVS 01/11 always want gamma"). Read by [`WRTMOD`](wrtmod.f.md#wrtmod) (the pulsation model) and written to the stored model by [`PUTSTORE`](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L13-L360) and [`STITCH`](stitch.f.md#stitch).
- `LSOUND`: set by the [main program](main.f.md#file-level), false at the start of each run and true at the run's last model (the end age, or the end of the kind card); `WRTMOD` writes its sound-speed output only when it is set.

**Design.** A blanket `USE SOUND_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/SOUND/` as a module.
