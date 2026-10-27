## Explanation

**Purpose.** `ENVSTRUCT_MOD` holds the run of the envelope's structure, point by point, as stored by the envelope integration, shared by 7 routines. It replaces `COMMON/ENVSTRUCT/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]].

**What its variables hold, who sets them, who reads them.**
- `NUMENV` (`INTEGER*4`): the number of stored points.
- At each point (`JSON` each): `ENVP`, `ENVT`, `ENVD`, `ENVR` ($\log P$, $\log T$, $\log\rho$, $\log r$), `ENVS` ($\log(m/M_*)$), `ENVX`, `ENVZ` ($X$, $Z$), `ENVO` (opacity), `ENVL` (luminosity), `LCENV` (convective, `EVEL` > 0), `EVELS` (convective velocity), `EDELS(3,JSON)` (the three gradients), `EBETAS`, `EGAM1` ($\Gamma_1$), `EQCP`, `EQDT` (thermodynamic derivatives), `EFXIONS(3,JSON)` (ionization fractions).
- [[envint.f#ENVINT|`ENVINT`]] fills them from [[envprt_mod.f#ENVPRT_MOD|`ENVPRT_MOD`]], starting at the surface, and then reverses their order, so that point 1 is the bottom; it passes them to [[taucal.f#TAUCAL|`TAUCAL`]].
- [[getnewenv.f#GETNEWENV|`GETNEWENV`]] and [[starin.f#STARIN|`STARIN`]] shift the structure variables when the fitting point moves (points above the new interior mass kept, offset by the jump in each variable), and use them to add envelope points to the interior model.
- Read also by [[calcad.f#CALCAD|`CALCAD`]], [[gettau.f#GETTAU|`GETTAU`]], [[tauint.f#TAUINT|`TAUINT`]] (convective velocity beyond the interior) and [[stitch.f#STITCH|`STITCH`]] (which writes them out).

**Design.** A blanket `USE ENVSTRUCT_MOD`. At `rp_1`, `tauintnew.f` also declared the block; it no longer does.

**Changed since `rp_1`.** New file: `COMMON/ENVSTRUCT/` as a module.
