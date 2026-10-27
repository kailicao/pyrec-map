## Explanation

**Purpose.** `TEMP_MOD` holds physics at each shell for rotational mixing: specific heat, mean molecular weight, a density derivative, and the radiative diffusivity and viscosity. Shared by 5 routines. It replaces `COMMON/TEMP/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.**
- `CP`, `SQDT` (`JSON` each): $c_P$ and $\partial\ln\rho/\partial\ln T$ (`QCP`, `QDT`), and `HAMU(JSON)`: the mean molecular weight of a fully ionized gas, set by [[physic.f#PHYSIC|`PHYSIC`]]. `CP` is read by [[viscos.f#VISCOS|`VISCOS`]], `HAMU` by [[getw.f#GETW|`GETW`]].
- `VISC(JSON)`: the viscosity, radiative plus molecular, and `THDIF(JSON)`: the radiative diffusivity $16\sigma T^3/(3\kappa\rho^2 c_P)$, set by `VISCOS`.
- All five are read by [[hpoint.f#HPOINT|`HPOINT`]] and [[midmod.f#MIDMOD|`MIDMOD`]], `HPOINT` saves them as the values at the start of the step, and `MIDMOD` interpolates between those and the current ones.

**Design.** A blanket `USE TEMP_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/TEMP/` as a module.
