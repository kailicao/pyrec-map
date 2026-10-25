# Page design.md

Round 1, Oct 25, 2026, by Claude, against the code at YREC `rp_1`. Each finding gives its kind (wrong, missing, unclear, format), the text and the proposed fix; "Revised" says what was applied.

For Kaili Cao. Page `notes/design.md` ("A new design"), checked also against the design brief, KC's coding guide and, for the claims about the other branches, `git show`/`git ls-tree` on `origin/development` and the other remote branches (nothing checked out).

## What was checked, and held

- **COMMON-block map (6.4).** A script over `callgraph.json` finds 243 distinct blocks; the map names each exactly once, with none missing and none extra. The counts in Section 1 hold: `/CONST1/` in 93 units, `/LUOUT/` in 88, `PARMIN` 86 blocks, `main.f` 60.
- **Routines replaced.** Every `[[file#unit]]` link resolves to a unit in the call graph, and every unit of the call graph is named on the page (`BLOCK_DATA` through `blkdta000.f`).
- **Code claims spot-checked and right:** `REDUCE` takes 39 arguments; `QUAD`'s 30 cache slots; `MIX` sets `LDIFY = .FALSE.`, `HTIMER` sets `LPTIME = .FALSE.`, `ENVINT` sets `KTTAU = 0`; `SECULR` tests `LCODM`, `CODM` without `/MAG/`; `LBURS = .FALSE.` in `GETW`; `ENGEB` called with the undefined `IU` in `main.f`; `STOP 9999` in `STARIN` and `ALFILEIN`; `/ALATM04/` holds only `DUMMY1`–`DUMMY4`; `GMASS01` and `GMASS06` differ only in name, case and a blank line; `PARMIN` is 1,461 lines; `GETW`'s substep count is the minimum of the two ceilings; `CRRECT`'s damping `FCORR = min(1, FCORR + FCORRI)`; `/QENVMIX/` is not in rp_1 (it is development's).
- **The other branches.** Dates and commit counts hold (development Oct 20, 246 ahead of rp_1; main Oct 11, 176; spotevol Sep 24, 162; yrec_2026_release Sep 16, 154; modern Apr 26, 2025, 41 ahead and 121 behind, all 41 by Kaili Cao; jvs0210 Oct 2, 2025, 0 ahead and 36 behind). On development: `F90_CONVERSION_PLAN.md`, `KNOWN_ISSUES.md`, `REBASELINE_PROTOCOL.md`, `rebaseline.py`, `wrappers/` exist; no `COMMON` statement is left in `src/` (issue 37, resolved Oct 20); all 284 `.f` files contain `IMPLICIT NONE`; the full suite is 298 cases, "about five hours", with a 17-case targeted set (plan, Validation protocol); the `CALL MDOT` mismatch was fixed in b3b0601; `docs/source/python_package.md` documents `pip install yrec` and `yrec.run_parallel`; `YREC_INPUT` is used. Issues 7 (QENV/QATM) and 11 (`ENVSTRUCT`, `ATMSTRUCT` held for output) say what the page says.
- **Style.** The conventions of the guide carry over sensibly (6.2): `init`/`run`/`clear`, `…Base` for private bases, `ierr` for errors, UPPERCASE parameters with the case-insensitivity caveat, hooks that do nothing in the base, one `Config` read once. The tree is at most 79 characters wide.

## Findings and proposed fixes

### Wrong

1. **A divergence does not cut the step today; it ends the run.** Sections 3.12 and 4 (step 5) say "`Track%run` cuts the step and tries again (label 15)". In rp_1, label 15 calls `STARIN` with `LARGE` set, and `STARIN` writes "MODEL FAILED TO CONVERGE" and `STOP`s (starin.f, lines 137–146), despite main.f's comment "STARIN called here for timestep cutting". (The main.f note, Steps 2, repeats the comment's claim; the starin.f note is right.) **Fix:** say that today a divergence ends the run; `Step%run` returns `STEP_DIVERGED`, and `Track%run` ends with that error, as today; cutting and retrying is a new behavior and goes into Section 8 (question 4).
2. **The `MDOT` mismatch is in `massloss.f`, not `main.f`.** Section 1: "[[main.f]] passes `MASSLOSS` one argument more than `MDOT` takes". `massloss.f` (line 176) calls `MDOT` with `BL` first; `MDOT` has no such argument. **Fix:** "`MASSLOSS` passes `MDOT` one argument (`BL`) more than it takes".
3. **"Every file declares `JSON = 5000`"** (Section 1, and Section 5 "in every file"): 123 of the 254 files do. **Fix:** "123 of the 254 files".
4. **`StarCalibr` checks every model, not a finished track.** `main.f` calls `CHKSCAL` inside the model loop (line 975, on even kind cards after the first model) and may end the track there (`GOTO 200`); only `CHKCAL` runs at the end of a track. Section 3.13 (`check` "from a finished track's TrackSummary") and Section 4 (step 5) say otherwise. **Fix:** give `CalibrBase` a hook `after_model(summary, done)` (the base does nothing), used by `StarCalibr`; step 4 of the data flow calls it.
5. **Layering: `ConvectionZones` cannot live in `convection.f90`.** Its methods take a `Star`, but `convection.f90` sits below `star.f90`, which needs `Mlt` from it. **Fix:** move `ConvectionZones` to a new module `zones.f90` just above `star.f90`; drop "Overshoot" from the tree (no such type is defined; `OVERSH` is part of `ConvectionZones%find`).
6. **Illegal Fortran in `Track`.** It has a component `run` (pointer to `Run`) and a type-bound procedure `run`; a binding name may not equal a component name. `Run`'s component `log` shadows the intrinsic `LOG` (the guide's Fix list: names that shadow builtins). **Fix:** `type(Run), pointer :: job`; `type(Logger) :: logger`.
7. **Development's open issues (Section 8, question 1).** "after its open issues 27 and 29 … are settled": issue 27 was resolved on Oct 20; only 29 (no explicit interfaces) is open. **Fix:** name issue 29 only.
8. **Module count.** "86 `_MOD` modules" (7.3): development's `src/` has 87 (`MODULE …_MOD`), since issue 37 added three after the plan's count and issue 26 added `DIMENSIONS_MOD`. Section 6.4: "moved every block into a module of its own" is loose: development first removed options and consolidated the blocks, then made each remaining block a module. **Fix:** say so, with 87.

### Missing

9. **Data flow (Section 4) skips parts of `main.f`'s run:** the copy of the first model to `ILAST` with `WRTLST` (He flash, `LKUTHE`); `PDIST` at the start of each step; `LIRATE88` at the start of a step (rates before the step); the `ITROT = 1, ITDIF1` loop that repeats level 4, `MIXCZ`, `GETW` and `FPFT` with the start-of-step composition and $j$ restored (rotation); `CONVEC` before the light elements; the second `FPFT` after `GETNEWENV`; the end-age floor after `HTIMER`; `WRTMONTE`; `KTTAU` and `LPTIME` restored after each solar-calibration cycle. **Fix:** add them to the steps.
10. **The Allard switch and calibrations.** `main.f` restores `KTTAU` after each solar-calibration cycle (`kttau = kttausv`), so the gray switch lasts for the rest of the run, or of the cycle. **Fix:** say so in 3.3.
11. **`Run` does not list its `UserPhysics`** though 6.5 says it holds one. **Fix:** add the component.
12. **Benchmarks (7.1):** development's test references are not under version control (issue 32, open), and on Oct 20 296 of 298 cases passed (issues 31, 36). **Fix:** the overhaul first freezes and archives its own reference set, and records the two failing cases.
13. **Migration testability (7.2, step 2):** once `Config` replaces `PARMIN`, the routines not yet converted still read the old blocks (or development's modules). **Fix:** `Config%derive` also fills them until their last reader is converted, so each step leaves a runnable code.
14. **What to drop (Section 8, question 5):** development already removed `WCZ`, `SPLINNR`, `SPLNR` (da1887a) and kept `PUTYREC7` at its developers' decision (issue 24); `LPMM` and `PMMWMAX` were removed from the namelists, and the suite guards against them (3.2 says they are "still accepted, with a warning"). **Fix:** say so in both places.

### Unclear

15. **Diagram:** `Track *-- Step` while `Track` has no `Step` component (a `Step` is made per step). **Fix:** `Track ..> Step`.

### Format

No problem: headings, links (all resolve) and math render.

## For other groups

- `notes/main.f.md`, Steps 2 and Questions: label 15 does not restore the model with a smaller step; `STARIN` stops when `LARGE` is set (finding 1). Its Design paragraph says `JSON = 5000` is "in every file": 123 of 254. Settled: the page now says so (step 2, and Design: "set in 123 of the 254 files").

## Revision

Revised: findings 1–15 applied to `notes/design.md` (Sections 1, 2, 3.2, 3.3, 3.12, 3.13, 3.15, 4, 5, 6.2, 6.4, 7.1, 7.2, 7.3, and Section 8's questions 1, 4 (now also asking whether a failed model should cut the step) and 5); site rebuilt (the file pages and the design page), with no link reported as pointing to nothing.
