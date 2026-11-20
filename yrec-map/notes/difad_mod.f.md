## Explanation

**Purpose.** `DIFAD_MOD` holds the advective and diffusive coefficients of angular momentum transport on the even grid, used when transport is treated as diffusion plus advection (`LDIFAD`), shared by 4 routines. It replaces `COMMON/DIFAD/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/dimensions_mod.f#L38-L44).

**What its variables hold, who sets them, who reads them.**
- `ECOD3(JSON)`, `ECOD4(JSON)`: the advective and diffusive coefficients. [`ROTGRID`](https://github.com/yreclab/yrec/blob/7be4133/src/rotgrid.f#L2-L285) interpolates them onto the even grid from `VESA`, `VESD` ([`DIFAD2_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/difad2_mod.f#L19-L33)), adds the composition diffusion coefficient to `ECOD4`, and rescales both; [`DADCOEFT`](dadcoeft.f.md#dadcoeft) recomputes them in its iterations and builds its band matrix from them; [`DCOEFT`](dcoeft.f.md#dcoeft) reads them; [`CHECKJ`](checkj.f.md#checkj) prints them.

**Design.** A blanket `USE DIFAD_MOD`.

**Changed since `rp_1`.** New file: `COMMON/DIFAD/` as a module.
