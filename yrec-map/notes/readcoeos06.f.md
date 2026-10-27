## Explanation

**Purpose.** Reads the OPAL 2006 equation-of-state tables (five hydrogen abundances) into memory. It follows `READCOEOS01` (removed since `rp_1`, with the OPAL 2001 equation of state) closely; see also `READCO` (removed since `rp_1`, with the OPAL 1995 equation of state).

**How it fits.**
- **Who calls it:** [[esac06.f#ESAC06|`ESAC06`]], on its first call.
- **Input:** the file on unit `IOPALE` (from [[iounits_mod.f#IOUNITS_MOD|`IOUNITS_MOD`]]), opened by [[parmin.f#PARMIN|`PARMIN`]]; closed here.
- **Outputs, through modules:** [[aeos06_mod.f#AEOS06_MOD|`AEOS06_MOD`]] (the tables `XZ(5, 10, 197, 169)`, grids, inverse spacings; shared with `ESAC06`, [[rhoofp06.f#RHOOFP06|`RHOOFP06`]], [[t6rinteos06.f#T6RINTEOS06|`T6RINTEOS06`]], [[eqbound06.f#EQBOUND06|`EQBOUND06`]]; its `MIDX`, formerly `M`, is the loop index over the compositions here) and [[eos06misc_mod.f#EOS06MISC_MOD|`EOS06MISC_MOD`]] (`ZZ` read here; `INDEX`, `NTA` used; `EOS(1..10)` set to 1 on the first call). The per-composition headers and the extra columns `AMU_M`, `ALOGNE`, formerly `/EEEEOS06/`, are saved local arrays.
- **Other modules:** [[eeeos06_mod.f#EEEOS06_MOD|`EEEOS06_MOD`]] (`XX`, for the inverse spacings `DFSX`); `ISHORT` from `IOUNITS_MOD`.

**The method.** As in `READCOEOS01`, with 197 temperatures, and rows that hold $T_6$, a mean molecular weight (`AMU_M`), $\log n_e$ (`ALOGNE`, by its name) and nine quantities. Unlike the 2001 version, it does not set up the ramp's edge `RMX`; `EQBOUND06` uses `NRA` in `/BEOS06/` instead.

**KC's changes.** The members of `/BEOS06/`, `/EEEEOS06/` and `/OPALEOS/` were reordered (KC 2025-05-30); two `DO` loops that ended on an assignment (labels 12 and 13) were rewritten to end on `CONTINUE` (KC 2025-05-30).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/BEOS06/`, `/EEOS06/` and `/AAEOS06/` merged into `EOS06MISC_MOD`; `/EEEEOS06/` made local arrays, with `SAVE`; `/OPALEOS/` dropped with the OPAL 1995 and 2001 equations of state), `IMPLICIT NONE`; `AEOS06`'s `M` renamed `MIDX`.

## Questions for the experts

1. **A wrong index.** The data read is `alogne(jcs,j)`, but `j` is not the loop variable (that is `i`): `j` is left over from an earlier loop (11 after the first call's initialization). So every row writes to the same element, and `ALOGNE` holds only the last value read. `ALOGNE` and `AMU_M` are used nowhere else, so the bug has no effect today; it should read `alogne(jcs,i)`.
2. **`close (2)`.** As in `READCOEOS01`, unit 2 is closed though never opened. Leftover?
3. **Message typos.** The error message says "oeos96 data files" (for the 2006 tables).
