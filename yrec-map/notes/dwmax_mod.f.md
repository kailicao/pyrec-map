## Explanation

**Purpose.** `DWMAX_MOD` holds the critical rotation gradient for the shear instability at each shell, and its value at the start of the step, shared by [`PHYSIC`](https://github.com/yreclab/yrec/blob/7be4133/src/physic.f#L3-L191) and [`HPOINT`](hpoint.f.md#hpoint). It replaces `COMMON/DWMAX/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/dimensions_mod.f#L38-L44).

**What its variables hold, who sets them, who reads them.**
- `QWRMAX(JSON)`: the critical $`d\Omega/d\ln r`$ (Endal and Sofia [1978](https://ui.adsabs.harvard.edu/abs/1978ApJ...220..279E), as PHYSIC's comments cite), set by `PHYSIC` for the interface between shells `IM-1` and `IM`: 0 where both shells are convective or the root is not real ([physic.f, lines 155–186](https://github.com/yreclab/yrec/blob/7be4133/src/physic.f#L155-L186)). Read only by `HPOINT`, to copy it ([hpoint.f, line 855](https://github.com/yreclab/yrec/blob/7be4133/src/hpoint.f#L855)), so PHYSIC's computation reaches nothing (so also at `rp_1`): unused?
- `QWRMX0(JSON)`: the start-of-step copy, made by `HPOINT` when it saves the old model; read nowhere: unused?

**Design.** A blanket `USE DWMAX_MOD`. [`SECULR`](https://github.com/yreclab/yrec/blob/7be4133/src/seculr.f#L6-L532) has a local array of the same name, `QWRMAX`, which [`SETUPV`](https://github.com/yreclab/yrec/blob/7be4133/src/setupv.f#L3-L467) fills for the angular momentum transport; it is not this module's. At `rp_1`, [`MIDMOD`](https://github.com/yreclab/yrec/blob/7be4133/src/midmod.f#L2-L523) also declared the block without using it.

**Changed since `rp_1`.** New file: `COMMON/DWMAX/` as a module (MIDMOD's unused declaration dropped).
