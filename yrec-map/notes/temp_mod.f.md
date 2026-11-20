## Explanation

**Purpose.** `TEMP_MOD` holds physics at each shell for rotational mixing: specific heat, mean molecular weight, a density derivative, and the radiative diffusivity and viscosity. Shared by 5 routines. It replaces `COMMON/TEMP/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.**
- `CP`, `SQDT` (`JSON` each): $`c_P`$ and $`\partial\ln\rho/\partial\ln T`$ (`QCP`, `QDT`), and `HAMU(JSON)`: the mean molecular weight of a fully ionized gas, set by [`PHYSIC`](https://github.com/yreclab/yrec/blob/7be4133/src/physic.f#L3-L191). `CP` is read by [`VISCOS`](viscos.f.md#viscos), `HAMU` by [`GETW`](getw.f.md#getw).
- `VISC(JSON)`: the viscosity, radiative plus molecular, and `THDIF(JSON)`: the radiative diffusivity $`16\sigma T^3/(3\kappa\rho^2 c_P)`$, set by `VISCOS`.
- All five are read by [`HPOINT`](hpoint.f.md#hpoint) and [`MIDMOD`](https://github.com/yreclab/yrec/blob/7be4133/src/midmod.f#L2-L523): `HPOINT` saves them as the values at the start of the step, and `MIDMOD` interpolates between those and the current ones.

**Design.** A blanket `USE TEMP_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/TEMP/` as a module.
