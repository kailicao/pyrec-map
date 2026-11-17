## Explanation

**Purpose.** `DIFAD3_MOD` holds the Zahn-type factors of the diffusion-plus-advection treatment of angular momentum (`LDIFAD`), shared by [`SETUPV`](setupv.f.md#setupv), [`VCIRC`](vcirc.f.md#vcirc) and [`DADCOEFT`](dadcoeft.f.md#dadcoeft). It replaces `COMMON/DIFAD3/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](dimensions_mod.f.md#dimensions_mod). All 21 members are arrays of `JSON`.

**What its variables hold, who sets them, who reads them.**
- `FACD2`, `FACD3`: factors set by `SETUPV`, from which `VCIRC` forms `VESD2`, `VESD3` (`0.2*FACD*WM`, then rescaled by the $`\mu`$-gradient factor); `VESD2`, `VESD3` are read nowhere else.
- `FV0`, `FV1A`, `FV1B`, `FV2A`, `FV2B`: set by `SETUPV` (`FV2B` with the `FACT7` term added); `VCIRC` rescales `FV0`. `FV1A`–`FV2B` are read nowhere: unused? (So are `VESD2`, `VESD3` above.)
- `DSS`, `DGSF`: $`r\,|v_\mathrm{SS}|`$ and $`r\,|v_\mathrm{GSF}|`$, set by `VCIRC`, read nowhere: unused?
- `EV0`, `EV1A`, `EV1B`, `EV2A`, `EV2B`, `ECOD5`, `ECOD6`, `FGEOM`, `ESS`, `EGSF`: read by `DADCOEFT` to build its coefficients (`ESS`, `EGSF` rescaled in place there), but set by no routine, so they keep their initial values (zero in practice, though a module variable without an initializer is formally undefined). The coefficients `ECOD3`, `ECOD4` that DADCOEFT computes from them are then zero ([dadcoeft.f, lines 244–269](https://github.com/yreclab/yrec/blob/7be4133/src/dadcoeft.f#L244-L269)), and DADCOEFT divides by `FGEOM` ([dadcoeft.f, lines 592–597](https://github.com/yreclab/yrec/blob/7be4133/src/dadcoeft.f#L592-L597)). This is [DADCOEFT's suspected bug 1](dadcoeft.f.md#b1) (only with `LDIFAD`, off by default), whose possible fix takes them for the even-grid versions of the `FV*`, `DSS`, and `DGSF` on the model's grid; `VESD2` and `VESD3` may be missing inputs too, and `FGEOM` a geometric factor still to be computed.

**Design.** A blanket `USE DIFAD3_MOD`. The block looks like a half-finished link between the factors SETUPV computes (`FV*`) and those DADCOEFT reads (`EV*`), which differ only in their first letter.

**Changed since `rp_1`.** New file: `COMMON/DIFAD3/` as a module.
