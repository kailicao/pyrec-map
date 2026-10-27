## Explanation

**Purpose.** `DPMIX_MOD` holds the extent of the overshoot region below a convection zone and the index of the shell being computed, so that [[tpgrad.f#TPGRAD|`TPGRAD`]] can use the adiabatic gradient there; shared by 6 routines. It replaces what is left of `COMMON/DPMIX/` (MHP via Claude, 10/14/26): the block's overshoot and semiconvection parameters (`DPENV`, `ALPHAC`, `ALPHAE`, `ALPHAM`, `BETAC`, `LOVSTC`, `LOVSTE`, `LOVSTM`, `LSEMIC`, `LADOV`, `LOVMAX`) are namelist variables now in [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]].

**What its variables hold, who sets them, who reads them.**
- `IOV1`, `IOV2` (`INTEGER*4`): the first and last shells of the overshoot region, set by [[oversh.f#OVERSH|`OVERSH`]] (−1 when there is none; "DBG 8/94 store position of overshoot for adiabatic extension").
- `IOVIM`: the shell for which the gradient is wanted, set just before the call by [[coefft.f#COEFFT|`COEFFT`]], [[physic.f#PHYSIC|`PHYSIC`]], [[qenv.f#QENV|`QENV`]] and [[starin.f#STARIN|`STARIN`]].
- All three are read only by `TPGRAD`: with `LADOV`, a radiative shell with `IOV1` ≤ `IOVIM` ≤ `IOV2` (and `IOVIM` ≠ −1) takes $\nabla = \nabla_\mathrm{ad}$.

**Design.** A blanket `USE DPMIX_MOD`. The shell index reaches `TPGRAD` through the module rather than as an argument; `QENV`, which works in the envelope, sets it too.

**Changed since `rp_1`.** New file: `IOV1`, `IOV2`, `IOVIM` of `COMMON/DPMIX/` as a module; the block's parameters moved to `NMLPAR_MOD`.
