## Explanation

**Purpose.** This file finds the convective and radiative regions of a model: the boundaries of each convection zone, without and with overshoot, the edge of the convective core (`JCORE`) and the base of the convective envelope (`JENV`), and the radiative regions between them. Its header stresses that overshoot here means "overmixing": overshoot shells are mixed with the convection zone but keep the radiative temperature gradient.

**How it fits.**
- **Inputs:** the arguments `LC` (convective or not, per shell, from [[coefft.f#COEFFT|COEFFT]] via the structure solution), `M`, and the model (`HCOMP`, `HD`, `HP`, `HR`, `HS`, `HT`), which only [[oversh.f#OVERSH|OVERSH]] uses; the overshoot switches `LOVSTC`, `LOVSTE`, `LOVSTM` (core, envelope, intermediate zones) in [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]]; the unit `ISHORT` from [[iounits_mod.f#IOUNITS_MOD|`IOUNITS_MOD`]].
- **Who calls it:** the main program ([[main.f#(file level)|main.f]]), [[mix.f#MIX|MIX]], [[getw.f#GETW|GETW]] and [[ovrot.f#OVROT|OVROT]].
- **What it calls:** [[oversh.f#OVERSH|OVERSH]], which moves the zone edges outward by the overshoot distance.
- **Outputs:** `MXZON0`, `NZONE0` (the zones without overshoot), `MXZONE`, `NZONE` (with overshoot, after merging zones that overlap), `MRZONE`, `NRZONE` (the radiative regions), `JCORE`, `JENV` (both before overshoot). [[mix.f#MIX|MIX]] uses the zones to treat burning in radiative and convective regions differently; [[ovrot.f#OVROT|OVROT]] (which sets the flags `LCZ` from them), [[rotmix.f#ROTMIX|ROTMIX]] and [[midmod.f#MIDMOD|MIDMOD]] also loop over the radiative regions; `JENV` is used throughout the code.

**The method.**
1. Scan the shells for runs of convective shells; a run of a single shell is ignored (the test `I1.NE.I-1`). At most 11 zones: as soon as the 11th is stored, the routine prints "TOO MANY MIX ZONES" (whether or not more follow) and stops the scan.
2. No zone: `JCORE = 1`, `JENV = M`, one radiative region. One zone covering the whole star: fully convective, `JCORE = JENV = 1`, `NRZONE = 0` (`MRZONE` is left as it was; every reader loops from 1 to `NRZONE`, so none reads it), and overshoot and merging are skipped.
3. `JCORE` is the top of a zone starting at shell 1; `JENV` the bottom of a zone ending at shell `M`.
4. If any overshoot switch is on, call OVERSH, then merge zones whose (overshot) edges now meet, with a message to `ISHORT`.
5. The radiative regions: below the first zone, between zones, above the last.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **An index error.** For a radiative region above the last convection zone, the code sets `MRZONE(1,2) = M` instead of `MRZONE(NRZONE,2) = M`. When that region is the only one (a convective core under a radiative envelope), the two are the same element and nothing goes wrong. When it is the second or a later one (a radiative surface and at least two radiative regions, e.g. a radiative core, a thin convection zone and a radiative surface), the top region's upper edge keeps an old value and the first region's upper edge becomes `M`. [[mix.f#MIX|MIX]] then burns the shells of the convection zones above the first region one by one, as radiative, before it treats each zone as a unit, and ROTMIX and MIDMOD treat those shells as radiative too (OVROT sets the convective flags after the radiative ones, so its `LCZ` comes out right). This looks like a bug. KC's check `I .GT. 0` in [[ovrot.f#OVROT|OVROT]] (2025-05-30, "to avoid runtime error") guards a loop over the same `MRZONE`, and may be related.
2. **The header's wording.** It says `JCORE` and `JENV` are "the edges of the surface and central convection zones respectively"; the code makes `JCORE` the core's edge and `JENV` the envelope's base (the reverse order).
3. **One-shell zones.** A single convective shell is treated as radiative. Is this a deliberate filter against noise in `LC`?

### CONVEC

Finds the convection zones (without and with overshoot, merging overlaps), the radiative regions between them, and `JCORE`, `JENV`.
