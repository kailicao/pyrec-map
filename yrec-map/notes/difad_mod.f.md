## Explanation

**Purpose.** `DIFAD_MOD` holds the advective and diffusive coefficients of angular momentum transport on the even grid, used when transport is treated as diffusion plus advection (`LDIFAD`), shared by 4 routines. It replaces `COMMON/DIFAD/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]].

**What its variables hold, who sets them, who reads them.**
- `ECOD3(JSON)`, `ECOD4(JSON)`: the advective and diffusive coefficients. [[rotgrid.f#ROTGRID|`ROTGRID`]] interpolates them onto the even grid from `VESA`, `VESD` ([[difad2_mod.f#DIFAD2_MOD|`DIFAD2_MOD`]]), adds the composition diffusion coefficient to `ECOD4` and rescales both; [[dadcoeft.f#DADCOEFT|`DADCOEFT`]] recomputes them in its iterations and builds its band matrix from them; [[dcoeft.f#DCOEFT|`DCOEFT`]] reads them; [[checkj.f#CHECKJ|`CHECKJ`]] prints them.

**Design.** A blanket `USE DIFAD_MOD`.

**Changed since `rp_1`.** New file: `COMMON/DIFAD/` as a module.
