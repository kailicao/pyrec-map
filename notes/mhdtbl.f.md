## Explanation

**Purpose.** `MHDTBL` opens the eight binary tables of the MHD equation of state, has [[mhdst.f#MHDST|MHDST]] read them, and closes them again. Its comment says the MHD equation of state "uses 3 ZAMS-type tables and optionally 5 center-type tables".

**How it fits.**
- **Inputs:** the eight file names `FMHD1`–`FMHD8`, passed as arguments (since MHP 8/25; earlier they came through the COMMON block `LUFNM`, now commented out). The unit numbers `IOMHD1`–`IOMHD8` come from `/MHD/`; [[parmin.f#PARMIN|PARMIN]] sets them to 40–47.
- **Who calls it:** [[setups.f#SETUPS|SETUPS]], at start-up, only when the flag `LMHD` (in `/MHD/`) is true.
- **What it calls:** [[mhdst.f#MHDST|MHDST]], which reads the tables into memory.
- **COMMON blocks:** `/MHD/` (the flag and unit numbers; shared with PARMIN, SETUPS, PHYSIC, QATM, QENV, STARIN, COEFFT, ENVINT, WRTOUT) and `/CCOUT2/` (debug flags, not used here).

**Design.** All eight files are opened with `STATUS='OLD'`, so all eight must exist, even though the comment calls five of them optional.

## Questions for the experts

1. **Optional tables.** The comment says five of the eight tables are optional, but `MHDTBL` opens all eight with `STATUS='OLD'`, so a missing file stops the run. Are the "center-type" tables in fact required now?
