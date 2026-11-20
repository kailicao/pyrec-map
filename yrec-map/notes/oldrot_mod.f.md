## Explanation

**Purpose.** `OLDROT_MOD` holds the rotation of the model at the start of the step, on the new point distribution, shared by 6 routines. It replaces `COMMON/OLDROT/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/dimensions_mod.f#L38-L44). All members are arrays of `JSON`.

**What its variables hold, who sets them, who reads them.** [`HPOINT`](hpoint.f.md#hpoint) saves them after it has remapped the model ("store the old model structure for use in diffusion"):
- `WOLD`: $`\Omega`$ at the start of the step (also set by [`STARIN`](starin.f.md#starin)). Read by [`WTIME`](wtime.f.md#wtime) (the largest fractional change of $`\Omega`$, for the time step), [`CHECKJ`](checkj.f.md#checkj) (whether a gradient was positive before), [`GETW`](getw.f.md#getw) (the start of the first substep), and HPOINT.
- `HJX` ($`J/M`$, "MHP 10/91 J/M stored in HJX"), `R0X`, `ETA2X` (the rotational distortion terms): interpolated onto the new grid and copied back into `HJM`, `R0`, `ETA2` by HPOINT itself.
- `HGO`: gravity, read by [`MIDMOD`](https://github.com/yreclab/yrec/blob/7be4133/src/midmod.f#L2-L523) (interpolated to mid-step).
- `HIO`: the moment of inertia, saved by HPOINT ([hpoint.f, line 816](https://github.com/yreclab/yrec/blob/7be4133/src/hpoint.f#L816)); read nowhere: unused?

**Design.** A blanket `USE OLDROT_MOD`.

**Changed since `rp_1`.** New file: `COMMON/OLDROT/` as a module.
