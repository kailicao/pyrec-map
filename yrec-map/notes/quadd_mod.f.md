## Explanation

**Purpose.** `QUADD_MOD` holds terms of the potential of a rotating star at each shell and the quadrupole correction factor of the meridional circulation. Shared by 3 routines. It replaces `COMMON/QUADD/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.**
- `PHISP`, `PHIROT`, `PHIDIS` (`JSON` each): the spherical potential $`GM/r`$, the rotational term $`\Omega^2 r^2`$ and the distortion term, computed by [`FPFT`](fpft.f.md#fpft) (under "OUTPUT DATA," [fpft.f, lines 93–98](https://github.com/yreclab/yrec/blob/7be4133/src/fpft.f#L93-L98)) and read by no routine, at `rp_1` too, where a fourth file declared the block (unused?).
- `RAT(JSON)`: the ratio of the corrected to the classical expression of the Eddington–Sweet circulation velocity (the quadrupole term, "as per Zahn ([1992](https://ui.adsabs.harvard.edu/abs/1992A%26A...265..115Z))"), set by [`VCIRC`](vcirc.f.md#vcirc) from `QUAD` and `GG` (`QUADRU_MOD`); read by `VCIRC` and written by [`CHECKJ`](checkj.f.md#checkj).

**Design.** A blanket `USE QUADD_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/QUADD/` as a module.
