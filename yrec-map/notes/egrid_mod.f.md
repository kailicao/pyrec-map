## Explanation

**Purpose.** `EGRID_MOD` holds the evenly spaced grid on which angular momentum transport and rotational mixing are solved: the grid variable $`\chi`$ at the model's shells and at the even points, the even points' masses, the spacing and their number. Shared by 7 routines. It replaces `COMMON/EGRID/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](dimensions_mod.f.md#dimensions_mod).

**What its variables hold, who sets them, who reads them.** All are set by [`GETGRID`](getgrid.f.md#getgrid) for the region `IBEG`…`IEND`:
- `CHI(JSON)`: $`\chi = \log m/\Delta_m + L/\Delta_L - \log P/\Delta_P`$ at each shell of the region, where $`\Delta_m`$ = `HPTTOL(2)`, $`\Delta_L`$ = `HPTTOL(9)`$`\cdot L_\mathrm{surf}`$ and $`\Delta_P`$ = `HPTTOL(11)`, the mesh tolerances ([GETGRID](getgrid.f.md#getgrid)).
- `NTOT` (`INTEGER*4`): the number of even points, the number of shells in the region but at least 3.
- `DCHI`: the spacing, $`(\chi_\mathrm{last} - \chi_1)/(\mathtt{NTOT}-1)`$.
- `ECHI(JSON)`: $`\chi`$ at the even points, from `CHI(1)` in steps of `DCHI`.
- `ES1(JSON)`: the mass (g) at the even points, interpolated in $`\log m`$ by [`OSPLIN`](osplin.f.md#osplin).
- Read by [`ROTGRID`](rotgrid.f.md#rotgrid) and [`MIXGRID`](mixgrid.f.md#mixgrid), which interpolate quantities between the two grids, [`MIXCOM`](mixcom.f.md#mixcom), [`EQ2MOD`](eq2mod.f.md#eq2mod), [`SECULR`](seculr.f.md#seculr) (which passes `NTOT` to the solvers) and [`CHECKJ`](checkj.f.md#checkj) (printing).

**Design.** A blanket `USE EGRID_MOD`. At `rp_1`, SECULR named the third member `EQS1`, harmless with COMMON's storage association.

**Changed since `rp_1`.** New file: `COMMON/EGRID/` as a module.
