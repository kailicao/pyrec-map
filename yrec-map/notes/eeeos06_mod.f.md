## Explanation

**Purpose.** `EEEOS06_MOD` holds workspace of the OPAL 2006 equation-of-state interpolation: the table values of one quantity being interpolated, and the $X$ values of the tables. It replaces `COMMON/EEEOS06/` (MHP via Claude, 10/20/26). The table dimensions `MX` = 5, `NT` = 197, `NR` = 169 are `PRIVATE` copies, as in [[aeos06_mod.f#AEOS06_MOD|`AEOS06_MOD`]].

**What its variables hold, who sets them, who reads them.**
- `EPL(MX,NT,NR)`: for each $X$ index, the table values of the quantity being interpolated (`XZ(MIDX,IV,IT,IR)` of `AEOS06_MOD`), copied by [[esac06.f#ESAC06|`ESAC06`]] for each variable `IV` and read there in the interpolation.
- `XX(MX)`: the $X$ values of the five tables, copied from `XA` by [[esac06.f#SETEOS06|`SETEOS06`]]; read by `ESAC06` and by [[readcoeos06.f#READCOEOS06|`READCOEOS06`]], which forms the inverse spacings `DFSX` from them.
- [[t6rinteos06.f#T6RINTEOS06|`T6RINTEOS06`]] also uses the module but reads neither member.

**Design.** A blanket `USE EEEOS06_MOD`. `XX` duplicates `XA`.

**Changed since `rp_1`.** New file: `COMMON/EEEOS06/` as a module.
