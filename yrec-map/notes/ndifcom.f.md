## Explanation

**Purpose.** Mixing of composition by rotationally induced instabilities, as part of angular momentum transport. Its comment: it "calculates the diffusion of composition due to angular momentum transport", by transforming to an equally spaced grid ("in radius", the comment says; the grid is in fact in the coordinate $\chi$ of [[getgrid.f#GETGRID|GETGRID]]), solving a diffusion equation and transforming back. It finds each unstable region and hands it to [[mixgrid.f#MIXGRID|MIXGRID]] (the grid) and [[mixcom.f#MIXCOM|MIXCOM]] (the solve).

**How it fits.**
- **Inputs:** the diffusion step `DT` (s); the mixing coefficients `COD2` at the model points; the transport velocities `HV` (a region is unstable where `HV > 0`); the model (`HD`, `HL`, `HP`, `HR`, `HS`, `HS1`, `HS2`, `HSTOT`); the convection flags `LCZ` (overshoot included); the search range `IMIN..IMAX`; the flag `LOK` (final iteration); and the species range `JBEG..JEND`.
- **Who calls it:** [[seculr.f#SECULR|SECULR]] (the angular momentum transport) and [[bursmix.f#BURSMIX|BURSMIX]] (burning and mixing).
- **What it calls:** [[mixgrid.f#MIXGRID|MIXGRID]] and [[mixcom.f#MIXCOM|MIXCOM]].
- **Outputs:** `HCOMP` updated in place; `IBEG`, `IEND`, `ECOD2` and `EM` for the last region (kept for the next call).
- **Modules:** only `DIMENSIONS_MOD` (`JSON`); the grid is shared between `MIXGRID` and `MIXCOM` through `EGRID_MOD`.

**The method.**
- **Before the last iteration** (`LOK = F`): `MIXCOM` is called once for the region found earlier (`IBEG..IEND`, with its grid), so that the comments' aim, the change of the $\mu$ gradient caused by mixing, can be found. The comment says only H, ⁴He and ³He are mixed then; which species are mixed is set by the caller through `JBEG..JEND`.
- **On the last iteration** (`LOK = T`): it scans `IMIN..IMAX` for runs of interfaces with `HV > 0`. Each run, from the zone below its first such interface (`IBEG`) to the zone above its last (`IEND`), gets its own grid from `MIXGRID` and its own solve in `MIXCOM`. A region of only two zones (`LDUM2`) is skipped.

**KC's changes.** 2025-05-31: the unused argument `NTOT` removed.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`, `JSON` from `DIMENSIONS_MOD`.

## Questions for the experts

1. **The species mixed.** The comments say that before the last iteration only H, ⁴He and ³He are mixed, and on the last only species heavier than ⁴He. The routine itself does not choose: `JBEG..JEND` come from the caller. [[seculr.f#SECULR|SECULR]] matches the comments (rows 1–4, then rows 5–11 or 5–15); [[bursmix.f#BURSMIX|BURSMIX]] passes rows 4 to 11 (or 15) on every call. Is that intended for BURSMIX?
2. **Regions skipped.** A region of only two zones (one unstable interface) is skipped entirely, so no composition is mixed across a single unstable interface. Intended?
3. **Only the last region before the final call.** The header says the grid of the last region solved "[is] used initially, and then the program checks for additional unstable regions interior to that", but with `LOK = F` only that one region is mixed and nothing else is checked; other unstable regions are mixed only on the final call. Intended?

### NDIFCOM

Finds each run of unstable interfaces (`HV > 0`) between `IMIN` and `IMAX` and mixes its composition (on the final call), or mixes the last region again (before it).
