## Explanation

**Purpose.** `ROTEN_MOD` holds the change of rotational kinetic energy at each shell over the step, a term of the energy equation. Shared by 3 routines. It replaces `COMMON/ROTEN/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.**
- `DEROT(JSON)`: $`(E_\mathrm{rot} - E_\mathrm{rot,old})/(\Delta t\,\Delta m)`$ at each shell ("7/92"), from `HKEROT`, `HKEROTO`, and `HS2` (with COEFFT's `DT` = 1/`DELTS`); set by [`COEFFT`](coefft.f.md#coefft) when `LROT` is set, which subtracts it from the luminosity equation. Written by [`PUTSTORE`](https://github.com/yreclab/yrec/blob/7be4133/src/putstore.f#L13-L360) and [`STITCH`](stitch.f.md#stitch) to the stored model.

**Design.** A blanket `USE ROTEN_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/ROTEN/` as a module.
