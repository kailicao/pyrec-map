## Explanation

**Purpose.** `FINDEX` finds the interval of a sorted table that contains a value: given an increasing array `AX(1..NX)` and `X`, it returns `M` with `AX(M)` ≤ `X` < `AX(M+1)`. The header ("YCK 3/91") calls it part of the "interpolation package for Cox's and Kurucz's opacities", and lists the package's other two routines, [[intpol.f#INTPOL|INTPOL]] and [[ysplin.f#YSPLIN|YSPLIN]], which are in their own files.

**How it fits.**
- **Who calls it:** the opacity interpolators [[kurucz.f#KURUCZ|KURUCZ]], [[kurucz2.f#KURUCZ2|KURUCZ2]], [[ll4th.f#LL4TH|LL4TH]], [[yllo2d.f#YLLO2D|YLLO2D]], [[yllo2d2.f#YLLO2D2|YLLO2D2]], [[yllo3d.f#YLLO3D|YLLO3D]] and [[yllo3d2.f#YLLO3D2|YLLO3D2]].
- **Inputs and output:** `AX`, `NX`, `X`; `M` is both the starting guess (the last index found) and the result.

**The method.** A linear search from the guess `M` (reset to 1 if out of range), downward if `X` < `AX(M)`, upward otherwise. If `X` is below the table, `M` = −1; if above, `M` = −`NX`. `X` equal to the last value `AX(NX)` also gives −`NX`; YLLO3D and YLLO3D2 catch that case explicitly.

## Questions for the experts

1. **Out-of-range codes in KURUCZ.** LL4TH and the four YLLO routines test for a negative `M`; [[kurucz.f#KURUCZ|KURUCZ]] and [[kurucz2.f#KURUCZ2|KURUCZ2]] do not. They set `ITS = M2-2` (at least 1) and `ITF = M2+3`; above the temperature grid ($M_2 = -$`NUMTM`) `ITF` falls below `ITS` and the loop over temperatures does nothing. Can that happen, given the test on `DL` and `TL` that follows?

### FINDEX

Linear search from the last index for the table interval containing `X`; returns −1 below the table and −`NX` above it.
