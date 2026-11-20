## Explanation

**Purpose.** `EGRIDDER_MOD` holds the coefficients of the higher-derivative terms of the diffusion-plus-advection treatment of angular momentum (`LDIFAD`), shared by [`SETUPV`](https://github.com/yreclab/yrec/blob/7be4133/src/setupv.f#L3-L467), [`VCIRC`](vcirc.f.md#vcirc), and [`DADCOEFT`](dadcoeft.f.md#dadcoeft). It replaces `COMMON/EGRIDDER/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/dimensions_mod.f#L38-L44).

**What its variables hold, who sets them, who reads them.**
- `QQCOD(JSON)`: $`\tfrac23\,r^4/(G\,m)`$-type factors at each shell (`CC23*RM**4/CG/HS3`), set by `SETUPV`; `VCIRC` multiplies them by $`\Omega`$ (`WM`) into `EQQCOD`.
- `EQQCOD(JSON)`: read by `DADCOEFT` as the coefficients of its $`d^2\Omega/dr^2`$ rows.
- `QQQCOD(JSON)`: factors set by `SETUPV` (`HTM`, `HTP`, [setupv.f, line 410](https://github.com/yreclab/yrec/blob/7be4133/src/setupv.f#L410), [setupv.f, line 435](https://github.com/yreclab/yrec/blob/7be4133/src/setupv.f#L435)); read nowhere: unused?
- `EQQQCOD(JSON)`: read by `DADCOEFT` as the coefficients of its $`d^3\Omega/dr^3`$ rows ([dadcoeft.f, lines 371–373](https://github.com/yreclab/yrec/blob/7be4133/src/dadcoeft.f#L371-L373)), but set by no routine (so at `rp_1` too), so those coefficients are zero. This gap is part of [DADCOEFT's suspected bug 1](dadcoeft.f.md#b1), whose possible fix names `QQQCOD` as the model-grid version to map onto the even grid (only with `LDIFAD`, off by default).

**Design.** A blanket `USE EGRIDDER_MOD`. The pairs mirror each other: `VCIRC` turns `QQCOD` into `EQQCOD`, but nothing turns `QQQCOD` into `EQQQCOD`, the same gap as in [`DIFAD3_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/difad3_mod.f#L19-L50).

**Changed since `rp_1`.** New file: `COMMON/EGRIDDER/` as a module.
