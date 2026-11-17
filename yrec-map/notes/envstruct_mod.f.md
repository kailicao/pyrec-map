## Explanation

**Purpose.** `ENVSTRUCT_MOD` holds the run of the envelope's structure, point by point, as stored by the envelope integration, shared by 7 routines. It replaces `COMMON/ENVSTRUCT/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](dimensions_mod.f.md#dimensions_mod).

**What its variables hold, who sets them, who reads them.**
- `NUMENV` (`INTEGER*4`): the number of stored points.
- At each point (`JSON` each): `ENVP`, `ENVT`, `ENVD`, `ENVR` ($`\log P`$, $`\log T`$, $`\log\rho`$, $`\log r`$), `ENVS` ($`\log(m/M_*)`$), `ENVX`, `ENVZ` ($`X`$, $`Z`$), `ENVO` (opacity), `ENVL` (luminosity), `LCENV` (convective, `EVEL` > 0), `EVELS` (convective velocity), `EDELS(3,JSON)` (the three gradients), `EBETAS`, `EGAM1` ($`\Gamma_1`$), `EQCP`, `EQDT` (thermodynamic derivatives), `EFXIONS(3,JSON)` (ionization fractions).
- [`ENVINT`](envint.f.md#envint) fills them from [`ENVPRT_MOD`](envprt_mod.f.md#envprt_mod), starting at the surface, and then reverses their order, so that point 1 is the bottom; it passes them to [`TAUCAL`](taucal.f.md#taucal).
- [`GETNEWENV`](getnewenv.f.md#getnewenv) and [`STARIN`](starin.f.md#starin) shift the structure variables when the fitting point moves (points above the new interior mass kept, offset by the jump in each variable), and use them to add envelope points to the interior model.
- Read also by [`CALCAD`](calcad.f.md#calcad), [`GETTAU`](gettau.f.md#gettau), [`TAUINT`](tauint.f.md#tauint) (convective velocity beyond the interior) and [`STITCH`](stitch.f.md#stitch) (which writes them out).

**Design.** A blanket `USE ENVSTRUCT_MOD`. At `rp_1`, `tauintnew.f` also declared the block; it no longer does.

**Changed since `rp_1`.** New file: `COMMON/ENVSTRUCT/` as a module.
