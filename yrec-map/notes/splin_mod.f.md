## Explanation

**Purpose.** `SPLIN_MOD` holds the work arrays of the interpolations by [`OSPLIN`](https://github.com/yreclab/yrec/blob/7be4133/src/osplin.f#L12-L50) (the shape-preserving spline) in the routines that move quantities between the model's grid and the even grid in $`\chi`$ of rotational mixing: the table (`XTAB`, `YTAB`) and the points of evaluation (`XVAL`) with the values found (`YVAL`). Shared by 4 routines. It replaces `COMMON/SPLIN/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.**
- `XTAB(JSON)`, `YTAB(JSON)`: the table to interpolate; `XVAL(JSON)`: the abscissas at which to evaluate; `YVAL(JSON)`: the values returned by `OSPLIN`. Each user fills them, calls `OSPLIN` with them as arguments, and reads the result before returning: [`EQ2MOD`](eq2mod.f.md#eq2mod), [`MIXCOM`](https://github.com/yreclab/yrec/blob/7be4133/src/mixcom.f#L2-L203), [`MIXGRID`](https://github.com/yreclab/yrec/blob/7be4133/src/mixgrid.f#L2-L167), and [`ROTGRID`](https://github.com/yreclab/yrec/blob/7be4133/src/rotgrid.f#L2-L285). `OSPLIN` itself does not use the module (its arguments have the same names).

**Design.** A blanket `USE SPLIN_MOD` in each routine. The arrays are scratch space: No value is passed from one routine to another through them.

**Changed since `rp_1`.** New file: `COMMON/SPLIN/` as a module.
