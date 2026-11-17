## Explanation

**Purpose.** `DPMIX_MOD` holds the extent of the overshoot region below a convection zone and the index of the shell being computed, so that [`TPGRAD`](tpgrad.f.md#tpgrad) can use the adiabatic gradient there; shared by 6 routines. It replaces what is left of `COMMON/DPMIX/` (MHP via Claude, 10/14/26): the block's overshoot and semiconvection parameters (`DPENV`, `ALPHAC`, `ALPHAE`, `ALPHAM`, `BETAC`, `LOVSTC`, `LOVSTE`, `LOVSTM`, `LSEMIC`, `LADOV`, `LOVMAX`) are namelist variables now in [`NMLPAR_MOD`](nmlpar_mod.f.md#nmlpar_mod).

**What its variables hold, who sets them, who reads them.**
- `IOV1`, `IOV2` (`INTEGER*4`): the first and last shells of the overshoot region, set by [`OVERSH`](oversh.f.md#oversh) (−1 when there is none; "DBG 8/94 store position of overshoot for adiabatic extension").
- `IOVIM`: the shell for which the gradient is wanted, set just before the call by [`COEFFT`](coefft.f.md#coefft), [`PHYSIC`](physic.f.md#physic), [`QENV`](qenv.f.md#qenv) and [`STARIN`](starin.f.md#starin).
- All three are read only by `TPGRAD`: with `LADOV`, a radiative shell with `IOV1` $`\le`$ `IOVIM` $`\le`$ `IOV2` (and `IOVIM` $`\ne -1`$) takes $`\nabla = \nabla_\mathrm{ad}`$.

**Design.** A blanket `USE DPMIX_MOD`. The shell index reaches `TPGRAD` through the module rather than as an argument; `QENV`, which works in the envelope, sets it too.

**Changed since `rp_1`.** New file: `IOV1`, `IOV2`, `IOVIM` of `COMMON/DPMIX/` as a module; the block's parameters moved to `NMLPAR_MOD`.
