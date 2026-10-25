## Explanation

**Purpose.** Reads the OPAL 2001 equation-of-state tables (five hydrogen abundances) into memory. It is the 2001 version of [[readco.f#READCO|`READCO`]]; the 2006 version is [[readcoeos06.f#READCOEOS06|`READCOEOS06`]].

**How it fits.**
- **Who calls it:** [[esac01.f#ESAC01|`ESAC01`]], on its first call.
- **Input:** the table file, opened on unit `IOPALE` by [[parmin.f#PARMIN|`PARMIN`]]; closed here at the end.
- **Outputs, through COMMON:** `/AEOS/` (the tables `XZ(5, 10, 191, 169)`, the grids and inverse spacings; shared with `ESAC01`, [[rhoofp01.f#RHOOFP01|`RHOOFP01`]], [[t6rinteos01.f#T6RINTEOS01|`T6RINTEOS01`]], [[eqbound01.f#EQBOUND01|`EQBOUND01`]]), `/BEOS/` (`ZZ`, read here; `IRI`, `INDEX`, `NTA` used), `/EEEEOS/` (per-composition headers, only here), and `/RMPOPEOS01/` (`RMX`, the table's highest density at each temperature, for the ramp in `EQBOUND01`, "mhp 7/2003").
- **Other COMMON:** `/OPALEOS/`, `/EEOS/`, `/EEEOS/` (`XX`), `/AAEOS/`, `/LUOUT/`.

**The method.** As in [[readco.f#READCO|`READCO`]] (see there for the inverse spacings), with 169 densities and 191 temperatures, nine quantities per row instead of ten (the tenth slot keeps the marker $10^{35}$, and [[esac01.f#ESAC01|`ESAC01`]] refuses `iorder` above 9, so it is never read), and `ZZ` read with more digits (`F12.9`). A zero temperature in the list stops the run with a message.

**KC's changes.** The members of `/BEOS/`, `/EEEEOS/` and `/OPALEOS/` were reordered (KC 2025-05-30); two `DO` loops that ended on an assignment (labels 12 and 13) were rewritten to end on `CONTINUE` (KC 2025-05-30).

## Questions for the experts

1. **`close (2)`.** Before reading, the routine closes unit 2, which it never opened. No other routine opens unit 2 explicitly. A leftover from when the file was opened here?
2. **`KRA` hard-coded.** The ramp's edge `KRA` is a `DATA` list of 191 indices, tied to this exact table. If the table were replaced, it would silently be wrong. Could it be computed from `NTA` or `ICYCUSE`?
