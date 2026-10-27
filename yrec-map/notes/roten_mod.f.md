## Explanation

**Purpose.** `ROTEN_MOD` holds the change of rotational kinetic energy at each shell over the step, a term of the energy equation. Shared by 3 routines. It replaces `COMMON/ROTEN/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.**
- `DEROT(JSON)`: $\Delta t\,(E_\mathrm{rot} - E_\mathrm{rot,old})/\Delta m$ at each shell ("7/92"), from `HKEROT`, `HKEROTO` and `HS2`; set by [[coefft.f#COEFFT|`COEFFT`]] when `LROT` is set, which subtracts it from the luminosity equation. Written by [[putstore.f#PUTSTORE|`PUTSTORE`]] and [[stitch.f#STITCH|`STITCH`]] to the stored model.

**Design.** A blanket `USE ROTEN_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/ROTEN/` as a module.
