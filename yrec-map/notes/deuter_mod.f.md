## Explanation

**Purpose.** `DEUTER_MOD` holds the deuterium burning rates, the mass accreted in the step and the base of the surface convection zone, shared by 11 routines. It replaces `COMMON/DEUTER/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](dimensions_mod.f.md#dimensions_mod).

**What its variables hold, who sets them, who reads them.**
- `DRATE(JSON)`: the deuterium burning rate at each shell, set by [`DEUTRATE`](deutrate.f.md#deutrate) (zeroed in [`MIX`](mix.f.md#mix)); read by [`DBURN`](dburn.f.md#dburn) and [`MIDMOD`](midmod.f.md#midmod).
- `DRATE0(JSON)`: the rate at the start of the step, copied from `DRATE` by `DEUTRATE` on the first iteration (`ITLVL` = 1) and remapped by [`HPOINT`](hpoint.f.md#hpoint) when points are added; read by `DBURN` and `MIDMOD`.
- `FMASSACC`: the mass accreted in the step (`DELM`), set by [`MDOT`](mdot.f.md#mdot); read by `DBURN`, [`DBURNM`](dburnm.f.md#dburnm) and [`LIBURN`](liburn.f.md#liburn), which mix the accreted material's deuterium and lithium into the convection zone.
- `JCZ`: the shell at the base of the surface convection zone (`JENV`), set by the [main program](main.f.md#file-level) and [`MASSLOSS`](massloss.f.md#massloss); read by `DEUTRATE`, which limits burning in the zone to the convective turnover time scale, and [`ENGEB`](engeb.f.md#engeb).

**Design.** A blanket `USE DEUTER_MOD`.

**Changed since `rp_1`.** New file: `COMMON/DEUTER/` as a module.
