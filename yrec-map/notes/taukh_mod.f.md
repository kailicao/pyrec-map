## Explanation

**Purpose.** `TAUKH_MOD` holds factors at each interface of the rotating model that [[setupv.f#SETUPV|`SETUPV`]] computes once per step from the structure and [[vcirc.f#VCIRC|`VCIRC`]] uses to compute the circulation velocities (the name, from "Kelvin–Helmholtz", is older than its content). Shared by 2 routines. It replaces `COMMON/TAUKH/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.** All are set by `SETUPV` at each interface (all but `FACT6` to 0 first, at every shell); SETUPV's page gives the equations.
- `FACT6(JSON)`: the term of the Eddington–Sweet velocity in the derivative of $\Omega^2 r^2$ (`VCIRC`: `VES` $= |\mathtt{FACT1}\,(\mathtt{FACT2}\,\mathtt{RAT}\,\omega^2 + \mathtt{FACT6}\,\mathrm{d}V)|$).
- `FES1`, `FES2`, `FES3` (`JSON` each): the Zahn-type terms of the circulation; read by SETUPV itself and by `VCIRC`.
- `FGSFK(JSON)`: the factor of the Goldreich–Schubert–Fricke velocity that `VCIRC` uses; `FGSFJ(JSON)`: the factor of an earlier form, used only in `VCIRC`'s commented-out lines.

**Design.** A blanket `USE TAUKH_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/TAUKH/` as a module.
