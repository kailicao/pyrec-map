## Explanation

**Purpose.** `YLLO3D2` is [[yllo3d.f|yllo3d.f]] for the second OPAL92 table at a different $Z$ ("DBG 5/94 opacity at different Z"): the same method and equations, with the COMMON blocks `GLLOT2`, `LLOT2`, `LLOT42` and `KIPMLL2` (used by no other routine), calling [[yllo2d2.f#YLLO2D2|YLLO2D2]].

**How it fits.** Called by [[getopac.f#GETOPAC|GETOPAC]] after `YLLO3D` when `L2Z` is true (with `LOPAL92`): `GETOPAC` then interpolates $\log\kappa$ and both derivatives linearly in $Z$ between the two tables (`ZOPAL1`, `ZOPAL2`); calls [[findex.f#FINDEX|FINDEX]] and `YLLO2D2`.

## Questions for the experts

1. **No initial indices.** Unlike `YLLO3D`, the COMMON `KIPMLL2` has no `DATA`; The indices `M12`, `M22`, `M32` are starting guesses for `FINDEX` (`M32` through `YLLO2D2`), so they are read before they are first set. `FINDEX` resets a guess outside the grid to 1, so this is harmless, but the two routines should agree.

### YLLO3D2

`YLLO3D` for the second-$Z$ OPAL92 table.
