## Explanation

**Purpose.** `DIFAD2_MOD` holds the advective and diffusive parts of the meridional circulation velocity at each shell, for the diffusion-plus-advection treatment of angular momentum (`LDIFAD`), shared by 3 routines. It replaces `COMMON/DIFAD2/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]].

**What its variables hold, who sets them, who reads them.**
- `VESA(JSON)`, `VESD(JSON)`: the advective (signed) and diffusive parts, set by [[vcirc.f#VCIRC|`VCIRC`]] (and rescaled there by the μ-gradient factor); read by [[rotgrid.f#ROTGRID|`ROTGRID`]], which interpolates them into `ECOD3`, `ECOD4` ([[difad_mod.f#DIFAD_MOD|`DIFAD_MOD`]]), and printed by [[checkj.f#CHECKJ|`CHECKJ`]].
- `VESA0(JSON)`, `VESD0(JSON)`: their values from the previous call, saved and read by `VCIRC` alone.

**Design.** A blanket `USE DIFAD2_MOD`.

**Changed since `rp_1`.** New file: `COMMON/DIFAD2/` as a module.
