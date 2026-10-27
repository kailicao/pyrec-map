## Explanation

**Purpose.** `DEUTER_MOD` holds the deuterium burning rates, the mass accreted in the step and the base of the surface convection zone, shared by 11 routines. It replaces `COMMON/DEUTER/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]].

**What its variables hold, who sets them, who reads them.**
- `DRATE(JSON)`: the deuterium burning rate at each shell, set by [[deutrate.f#DEUTRATE|`DEUTRATE`]] (zeroed in [[mix.f#MIX|`MIX`]]); read by [[dburn.f#DBURN|`DBURN`]] and [[midmod.f#MIDMOD|`MIDMOD`]].
- `DRATE0(JSON)`: the rate at the start of the step, copied from `DRATE` by `DEUTRATE` on the first iteration (`ITLVL` = 1) and remapped by [[hpoint.f#HPOINT|`HPOINT`]] when points are added; read by `DBURN` and `MIDMOD`.
- `FMASSACC`: the mass accreted in the step (`DELM`), set by [[mdot.f#MDOT|`MDOT`]]; read by `DBURN`, [[dburnm.f#DBURNM|`DBURNM`]] and [[liburn.f#LIBURN|`LIBURN`]], which mix the accreted material's deuterium and lithium into the convection zone.
- `JCZ`: the shell at the base of the surface convection zone (`JENV`), set by the [[main.f#(file level)|main program]] and [[massloss.f#MASSLOSS|`MASSLOSS`]]; read by `DEUTRATE`, which limits burning in the zone to the convective turnover time scale, and [[engeb.f#ENGEB|`ENGEB`]].

**Design.** A blanket `USE DEUTER_MOD`.

**Changed since `rp_1`.** New file: `COMMON/DEUTER/` as a module.
