## Explanation

**Purpose.** `QUADD_MOD` holds terms of the potential of a rotating star at each shell and the quadrupole correction factor of the meridional circulation. Shared by 3 routines. It replaces `COMMON/QUADD/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.**
- `PHISP`, `PHIROT`, `PHIDIS` (`JSON` each): the spherical potential $GM/r$, the rotational term $\Omega^2 r^2$ and the distortion term, computed by [[fpft.f#FPFT|`FPFT`]] (under "OUTPUT DATA") and read by no routine.
- `RAT(JSON)`: the ratio of the corrected to the classical expression of the Eddington–Sweet circulation velocity (the quadrupole term, "as per Zahn (1992)"), set by [[vcirc.f#VCIRC|`VCIRC`]] from `QUAD` and `GG` (`QUADRU_MOD`); read by `VCIRC` and written by [[checkj.f#CHECKJ|`CHECKJ`]].

**Design.** A blanket `USE QUADD_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/QUADD/` as a module.

## Questions for the experts

1. **Unused arrays.** `PHISP`, `PHIROT` and `PHIDIS` are computed by FPFT and read nowhere (at `rp_1` too, where a fourth file declared the block). Are they meant for an output that was dropped, or can they go?
