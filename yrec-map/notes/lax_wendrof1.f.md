## Explanation

**Purpose.** `LAX_WENDROF1` is the first (half) step of the two-step Lax–Wendroff scheme that [`GRSETT`](grsett.f.md#grsett) uses for the explicit, gravitational-settling term of the diffusion equation. It returns the change in the hydrogen abundance at the midpoints of an equally spaced radial grid over half a time step, and the same for the metals when metal diffusion is on.

**How it fits.**
- **Who calls it:** [`GRSETT`](grsett.f.md#grsett) (helium settling) and [`MICRODIFF_RUN`](microdiff_run.f.md#microdiff_run) (the microscopic-diffusion driver), each followed by [`LAX_WENDROF2`](lax_wendrof2.f.md#lax_wendrof2).
- **Arguments:** `DT` (time step, s), `ECOD1` (on the equal grid: the first term's coefficient, which [`SETUP_GRSETT`](setup_grsett.f.md#setup_grsett) builds as $`d\ln P/dr`$ times a function of $`X`$, so it acts as a flux), `EM` (the mass at each grid point), `NPT`, `STOT` (total mass), `LDOLI`; output `EX_H`.
- **Modules:** `CONSTANTS_MOD` ($`4\pi`$); `NMLPAR_MOD` (the switch `LDIFZ` for metal diffusion); `GRAVEZ_MOD`, the metals' arrays on the equal grid (`ECOD1Z` in, `EZ_H` out), shared with `GRSETT`, `LAX_WENDROF2`, [`MODEL_TO_EQUAL`](model_to_equal.f.md#model_to_equal) and [`EQUAL_TO_MODEL`](equal_to_model.f.md#equal_to_model).

**The method.** With $`F_i`$ = `ECOD1(I)`, $`m_i`$ = `EM(I)`, $`M`$ = `STOT`:

```math
\Delta X_{i+1/2} = \frac{\Delta t}{2}\,4\pi\,\frac{F_{i+1}-F_i}{m_{i+1}-m_i}\quad (i = 1..N-1),
```

stored in `EX_H(I)`, where at the centre ($`i = 1`$) the code takes $`F_1 = 0`$, $`m_1 = 0`$, and at the surface ($`i = N-1`$) $`F_N = 0`$, $`m_N = M`$: so the flux is taken as zero at the centre and at the surface. The same formulas, with `ECOD1Z` and `EZ_H`, are applied to the metals when `LDIFZ` is true and `LDOLI` is false.

Only the increment is computed, not the textbook half step's average of the neighbouring values, $`X_{j+1/2}^{n+1/2} = \tfrac12(X_j + X_{j+1}) + \Delta X_{j+1/2}`$: The average enters through the midpoint coefficients, which `MODEL_TO_EQUAL` interpolates from the current abundances, and `GRSETT` adds the increment by linearizing them, $`F_{i+1/2} + \Delta X_{i+1/2}\,\partial F/\partial X`$, which is $`F`$ at the half step's abundance to first order (settled from the code, Nov 9, 2026: [grsett.f, lines 173–185](https://github.com/yreclab/yrec/blob/7be4133/src/grsett.f#L173-L185); [model_to_equal.f, lines 157–170](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L157-L170)). The two boundary cells are not those of the midpoint grid: The central one spans the mass from 0 to `EM(2)`, and the surface one from `EM(NPT-1)` to `STOT`, so that each holds the reservoir beyond the grid's end (a convective core or envelope), to which `EQUAL_TO_MODEL` applies the change at the grid's end point (settled from the code, Nov 9, 2026: [lines 45–47](https://github.com/yreclab/yrec/blob/7be4133/src/lax_wendrof1.f#L45-L47), [lines 55–57](https://github.com/yreclab/yrec/blob/7be4133/src/lax_wendrof1.f#L55-L57); [equal_to_model.f, lines 42–44](https://github.com/yreclab/yrec/blob/7be4133/src/equal_to_model.f#L42-L44), [equal_to_model.f, lines 113–116](https://github.com/yreclab/yrec/blob/7be4133/src/equal_to_model.f#L113-L116)).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/CONST1/` to `CONSTANTS_MOD`, `LDIFZ` from `/GRAVS3/` to `NMLPAR_MOD`, `/GRAVEZ/` to `GRAVEZ_MOD`), `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

### LAX_WENDROF1

Half-step change of $`X`$ (and $`Z`$) from the difference of the settling fluxes (above).
