## Explanation

**Purpose.** `GETGRID` builds the equally spaced grid on which the diffusion equations for rotational mixing and angular momentum transport are solved. The grid variable is the combination of $`\log m`$, $`L`$ and $`\log P`$ that [HPOINT](hpoint.f.md#hpoint) uses to place the model's points, with one difference: HPOINT scales $`\Delta_L`$ by the largest $`L`$ in the model, GETGRID by the surface $`L`$.

**How it fits.**
- **Who calls it:** [MIXGRID](mixgrid.f.md#mixgrid) and [ROTGRID](rotgrid.f.md#rotgrid), for one region (`IBEG..IEND`).
- **Inputs:** `HL` ($`L`$ in solar units), `HP` ($`\log P`$), `HS` ($`\log m`$).
- **What it calls:** [OSPLIN](osplin.f.md#osplin), a shape-preserving osculatory quadratic spline.
- **Outputs:** in [`EGRID_MOD`](egrid_mod.f.md#egrid_mod): `CHI` (the grid variable at the model points), `ECHI` (equally spaced values), `ES1` (their masses, in g), `DCHI`, `NTOT`. [EQ2MOD](eq2mod.f.md#eq2mod), [SECULR](seculr.f.md#seculr), [MIXCOM](mixcom.f.md#mixcom) and [CHECKJ](checkj.f.md#checkj) read them.
- **Modules:** [`NMLPAR_MOD`](nmlpar_mod.f.md#nmlpar_mod) gives the point-spacing tolerances `HPTTOL` (formerly in `/CTOL/`, set in [PARMIN](parmin.f.md#parmin)); `EGRID_MOD` (output); $`\ln 10`$ from [`CONSTANTS_MOD`](constants_mod.f.md#constants_mod).

**The method.** With the model's spacing criteria $`\Delta_m`$ = `HPTTOL(2)`, $`\Delta_L`$ = `HPTTOL(9)`$`\cdot L_\mathrm{surf}`$ (with $`L_\mathrm{surf}`$ = `HL(M)`), $`\Delta_P`$ = `HPTTOL(11)`,
```math
\chi_i = \frac{\log m_i}{\Delta_m} + \frac{L_i}{\Delta_L} - \frac{\log P_i}{\Delta_P}.
```
The equally spaced grid runs from $`\chi_1`$ to $`\chi_N`$ with $`N`$ = `NTOT` points, $`\Delta\chi = (\chi_N - \chi_1)/(N-1)`$, and $`\log m`$ is interpolated onto it with `OSPLIN`, then unlogged.

> **Question** ([lines 61–67](https://github.com/yreclab/yrec/blob/7be4133/src/getgrid.f#L61-L67)). **Number of points.** `NTOT` is set to the number of model points in the region (at least 3); the formula that set it from the range of $`\chi`$ ("modulus of final chi plus one," [lines 63–64](https://github.com/yreclab/yrec/blob/7be4133/src/getgrid.f#L63-L64)) is commented out. So the grid is equally spaced in $`\chi`$ but has as many points as the model. Is that the intended resolution?

> **Question** ([lines 57–60](https://github.com/yreclab/yrec/blob/7be4133/src/getgrid.f#L57-L60), [line 88](https://github.com/yreclab/yrec/blob/7be4133/src/getgrid.f#L88)). **Monotonic $`\chi`$.** `OSPLIN` interpolates in $`\chi`$, so it needs increasing abscissae. $`\chi`$ increases outward when $`\log P`$ decreases and $`L`$ does not drop sharply; can $`L`$ decrease enough (for example in a region with neutrino losses) to break this?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

### GETGRID

Equally spaced grid in $`\chi = \log m/\Delta_m + L/\Delta_L - \log P/\Delta_P`$, with the mass of each grid point by spline interpolation.
