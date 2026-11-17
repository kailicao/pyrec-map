## Explanation

**Purpose.** `DIFAD_MOD` holds the advective and diffusive coefficients of angular momentum transport on the even grid, used when transport is treated as diffusion plus advection (`LDIFAD`), shared by 4 routines. It replaces `COMMON/DIFAD/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](dimensions_mod.f.md#dimensions_mod).

**What its variables hold, who sets them, who reads them.**
- `ECOD3(JSON)`, `ECOD4(JSON)`: the advective and diffusive coefficients. [`ROTGRID`](rotgrid.f.md#rotgrid) interpolates them onto the even grid from `VESA`, `VESD` ([`DIFAD2_MOD`](difad2_mod.f.md#difad2_mod)), adds the composition diffusion coefficient to `ECOD4` and rescales both; [`DADCOEFT`](dadcoeft.f.md#dadcoeft) recomputes them in its iterations and builds its band matrix from them; [`DCOEFT`](dcoeft.f.md#dcoeft) reads them; [`CHECKJ`](checkj.f.md#checkj) prints them.

**Design.** A blanket `USE DIFAD_MOD`.

**Changed since `rp_1`.** New file: `COMMON/DIFAD/` as a module.
