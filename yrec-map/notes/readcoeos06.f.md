## Explanation

**Purpose.** Reads the OPAL 2006 equation-of-state tables (five hydrogen abundances) into memory. It follows `READCOEOS01` (removed since `rp_1`, with the OPAL 2001 equation of state) closely; see also `READCO` (removed since `rp_1`, with the OPAL 1995 equation of state).

**How it fits.**
- **Who calls it:** [[esac06.f#SETEOS06|`SETEOS06`]], once at set-up (from [[setups.f#SETUPS|`SETUPS`]]).
- **Input:** the file on unit `IOPALE` (from [[iounits_mod.f#IOUNITS_MOD|`IOUNITS_MOD`]]), opened by [[parmin.f#PARMIN|`PARMIN`]]; closed here. The `close (2)` before the reading ([[#L95]]), as in `READCOEOS01`, closes a unit that no part of YREC opens (no unit number in `IOUNITS_MOD` or `PARMIN` is 2), so it does nothing (unused?).
- **Outputs, through modules:** [[aeos06_mod.f#AEOS06_MOD|`AEOS06_MOD`]] (the tables `XZ(5, 10, 197, 169)`, grids, inverse spacings; shared with `ESAC06`, [[rhoofp06.f#RHOOFP06|`RHOOFP06`]], [[t6rinteos06.f#T6RINTEOS06|`T6RINTEOS06`]], [[eqbound06.f#EQBOUND06|`EQBOUND06`]]; its `MIDX`, formerly `M`, is the loop index over the compositions here) and [[eos06misc_mod.f#EOS06MISC_MOD|`EOS06MISC_MOD`]] (`ZZ` read here; `INDEX`, `NTA` used; `EOS(1..10)` set to 1 on the first call). The per-composition headers and the extra columns `AMU_M`, `ALOGNE`, formerly `/EEEEOS06/`, are saved local arrays; `AMU_M` and `ALOGNE` are read nowhere (unused?), nor is the array `ALOGR` ([[#L64]], unused?).
- **Other modules:** [[eeeos06_mod.f#EEEOS06_MOD|`EEEOS06_MOD`]] (`XX`, for the inverse spacings `DFSX`); `ISHORT` from `IOUNITS_MOD`.

**The method.** As in `READCOEOS01`, with 197 temperatures, and rows that hold $T_6$, a mean molecular weight (`AMU_M`), $\log n_e$ (`ALOGNE`, by its name) and nine quantities. Unlike the 2001 version, it does not set up the ramp's edge `RMX`; `EQBOUND06` uses `NRA` in `/BEOS06/` (now in `EOS06MISC_MOD`) instead.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/BEOS06/`, `/EEOS06/` and `/AAEOS06/` merged into `EOS06MISC_MOD`; `/EEEEOS06/` made local arrays, with `SAVE`; `/OPALEOS/` dropped with the OPAL 1995 and 2001 equations of state), `IMPLICIT NONE`; `AEOS06`'s `M` renamed `MIDX`.

## Bugs, by priority

1. **(c)** **The 2006 tables called "OEOS96" in a message.** ([[#L114-L118]]) When a density row of the file has fewer temperatures than `NTA` requires, the run stops with "Problem with OEOS96 data files", naming the 1996 tables. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to name the 2006 tables in the message.
             write (ISHORT,'("Problem with OEOS06 data files: X=",f6.4,
         X         " density=",e14.4)') xin(midx), rhogr(midx,jcs)
    ```

2. **(d)** **`ALOGNE` read into one element.** ([[#L124-L126]]; [[#L81]], [[#L89]]) The data read is `alogNe(jcs,j)`, but the loop variable is `i`: `j` is left from the initialization loops (11 after them), so every row writes to `alogNe(jcs,11)`, and `ALOGNE` holds only the last value read for each density. `ALOGNE` is read nowhere, so the results are not changed today. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to read ALOGNE into the row of the loop.
          read (IOPALE,'(f11.6,1x,f6.4,e11.4,2e13.6,2e11.3,5f10.6)')
         x t6list(jcs,i),amu_M(jcs,i),alogNe(jcs,i),
         x (xz(midx,index(iv),i,jcs),iv=1,9)
    ```
