## Explanation

**Purpose.** `NMLBYPASS_MOD` holds the 83 namelist variables that serve only to set other quantities, or are kept for later development: none is read by the physics routines. It is used by [[parmin.f#PARMIN|`PARMIN`]], [[remap.f#REMAP|`REMAP`]] and [[starin.f#STARIN|`STARIN`]]. It replaces `COMMON/NMLBYPASS/` (MHP via Claude, 10/14/26), which had gathered `COMMON/NEWPARAM/`, `/NEWCROSS/` and `/XSECT/` and 18 derivation-only members of other blocks (`/PMMWIND/`, `/NEWMX/`, `/VMULT/`, `/CCOUT1/`, `/ENVGEN/`, and `LNEWNUC` of `/CROSS/`), so that [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] holds only what the physics reads.

**What its variables hold, who sets them, who reads them.** All are in PARMIN's `PHYSICS` namelist, except `NPENV`, `ISETMIX`, `ISETISO`, `R14_15`, `R16_17`, `ZXMIX`, `XB10_INI` and `XB11_INI`, which are in `CONTROL`. All but `NPENV` carry initial values, moved from PARMIN's `DATA` statements.
- `LNEWVARS` and the tolerances `TOL_DM_MIN`, `TOL_DM_MAX`, `TOL_DL_MAX`, `TOL_DP_*`, `TOL_DX_MAX`, `TOL_DZ_MAX`, `TOL_CZBASE_FINE_WIDTH`, `FLAG_DX`, `FLAG_DZ`, `FLAG_DW`, `TIME_*` and `LSTRUCT_TIME`: "more intuitive variable names" for the mesh and time-step tolerances; with `LNEWVARS`, `REMAP` copies them into `HPTTOL`, `ATIME`, `LPTIME`, `DTWIND` and `DTDIF` (in `NMLPAR_MOD`).
- `LNEWNUC` and the S-factors `S0_*`, with their first and second derivatives `S0P_*`, `S0PP_*` (pp chain, CNO cycle, Be7, hep, and the N15+p branches): with `LNEWNUC`, `REMAP` turns them into the rate factors `SSTANDARD` (in `NMLPAR_MOD`) and `QS0E`, `QQS0EE`, `FC12`, `FO16` ([[cross_mod.f#CROSS_MOD|`CROSS_MOD`]]).
- `XSLI6`, `XSLI7`, `XSBE91`–`XSBE93` with their switches `LXLI6`–`LXBE93`: the light-element cross sections (keV b); PARMIN turns each one switched on into the factor `SLI6`, …, `SBE93` relative to the default.
- `ISETMIX`, `ISETISO`, `ZXMIX`, `R14_15`, `R16_17`, `XB10_INI`, `XB11_INI`: the heavy-element mixture and isotope ratios that PARMIN applies to the starting model ("MHP 10/24 added heavy element mixture controls"); PARMIN sets `ZXMIX` from the chosen mixture.
- `PMMA`–`PMMM`, `PMMJD`: the exponents and constant of the wind law (reset by PARMIN for the presets of `AWIND`), from which PARMIN derives the factors of [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] (`EXMD`, `EXW`, `CONSTFACTOR`, …); `FO`: written to the `.short` file only; `NPENV`: a print interval, 9999 when not positive.
- `LENVG` and `PMMMD` are read nowhere.

**Design.** A blanket `USE NMLBYPASS_MOD` in the three routines; STARIN uses none of the members, and declares the module so that its isotope code can reach them later (the conversion's commit message says so).

**Changed since `rp_1`.** New file: the derivation-only namelist variables of six COMMON blocks as one module, with their defaults moved from PARMIN's `DATA` statements.

## Questions for the experts

1. **Unused inputs.** `LENVG` (removed from every input file as dead) and `PMMMD` are read nowhere, and `FO` is only written out. Can they leave the namelist?
