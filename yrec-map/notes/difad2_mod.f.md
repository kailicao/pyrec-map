## Explanation

**Purpose.** `DIFAD2_MOD` holds the advective and diffusive parts of the meridional circulation velocity at each shell, for the diffusion-plus-advection treatment of angular momentum (`LDIFAD`), shared by 3 routines. It replaces `COMMON/DIFAD2/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/dimensions_mod.f#L38-L44).

**What its variables hold, who sets them, who reads them.**
- `VESA(JSON)`, `VESD(JSON)`: the advective (signed) and diffusive parts, set by [`VCIRC`](vcirc.f.md#vcirc) (and rescaled there by the $`\mu`$-gradient factor); read by [`ROTGRID`](https://github.com/yreclab/yrec/blob/7be4133/src/rotgrid.f#L2-L285), which interpolates them into `ECOD3`, `ECOD4` ([`DIFAD_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/difad_mod.f#L19-L31)), and printed by [`CHECKJ`](checkj.f.md#checkj).
- `VESA0(JSON)`, `VESD0(JSON)`: their values from the previous call, saved and read by `VCIRC` alone.

**Design.** A blanket `USE DIFAD2_MOD`.

**Changed since `rp_1`.** New file: `COMMON/DIFAD2/` as a module.
