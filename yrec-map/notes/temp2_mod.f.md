## Explanation

**Purpose.** `TEMP2_MOD` holds the velocities of rotational mixing at each interface, computed by [`VCIRC`](vcirc.f.md#vcirc) and turned into diffusion coefficients by [`CODIFF`](codiff.f.md#codiff). Shared by 5 routines. It replaces `COMMON/TEMP2/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.**
- `VES`, `VGSF`, `VSS`, `VMU` (`JSON` each): the Eddington–Sweet circulation, the Goldreich–Schubert–Fricke, the secular-shear, and the $`\mu`$-current velocities, set by `VCIRC` (to 0 first). Read by `CODIFF` (the coefficients `COD`, from the sum `VES` + `VGSF` + `VSS`, and `COD2`, from a weighted sum, or with `LVFC` from `COD` times `VFC`), [`CHECKJ`](checkj.f.md#checkj) (which writes them), and, except `VMU`, by [`PUTSTORE`](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L13-L360) and [`STITCH`](stitch.f.md#stitch) (the stored model).
- `VES0`, `VGSF0`, `VSS0`: the previous iteration's `VES`, `VGSF`, `VSS`, saved by `VCIRC` from the second iteration on, which then averages old and new values; `CHECKJ` writes `VES0` and `VGSF0`.
- `HLE(JSON)`: a length scale, set to 0 at every interface by `CODIFF` (its assignments `HLE(I) = RMID(I)` are commented out); `CHECKJ` writes it as "LENGTH."

**Design.** A blanket `USE TEMP2_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/TEMP2/` as a module.
