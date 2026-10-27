## Explanation

**Purpose.** `VFACT_MOD` holds the factors at each interface from which the circulation velocities and the stability criteria of rotational mixing are computed; [[setupv.f#SETUPV|`SETUPV`]] sets them once per step and [[vcirc.f#VCIRC|`VCIRC`]] uses them. Shared by 2 routines. It replaces `COMMON/VFACT/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.** All are set by `SETUPV` (to 0 first, then at each interface); SETUPV's page gives the equations.
- `FACT1`, `FACT2` (`JSON` each): the Eddington–Sweet velocity, `VES` = `FACT1`·`FACT2`·$\omega^2$ ("Endal and Sofia paper II"), with `FACT6` of `TAUKH_MOD`; read by `VCIRC`, which also uses `FACT1` for the $\mu$ currents.
- `FACT3(JSON)`: $|H_T r|$, for the Goldreich–Schubert–Fricke velocity; read only in `VCIRC`'s commented-out lines.
- `FACT4(JSON)`: the "fictitious $\mu$ currents" (Kippenhahn, IAU 66); read by `VCIRC`.
- `FACT5(JSON)`: the Richardson criterion of the secular shear with $\mu$ gradients; read by `VCIRC`.
- `FACT7`, `FACT8` (`JSON` each): the terms of order $\mathrm{d}\omega/\mathrm{d}r$ (Zahn and Maeder 1998), computed only with `LDIFAD`; `FACT8` stays 0. Read by `VCIRC`.

**Design.** A blanket `USE VFACT_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/VFACT/` as a module.
