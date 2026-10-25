## Explanation

**Purpose.** `YLLO2D2` is [[yllo2d.f|yllo2d.f]] for the second OPAL92 table, at a different $Z$ ("DBG 5/94 modified to use second opacity table at different Z"): the same method and equations, with the COMMON blocks `GLLOT2`, `LLOT2`, `LLOT42` and `LINTPL2`.

**How it fits.** Called by [[yllo3d2.f#YLLO3D2|YLLO3D2]] and [[ll4th.f#LL4TH|LL4TH]]; calls [[findex.f#FINDEX|FINDEX]] and [[intpol.f#INTPOL|INTPOL]]. Its coefficients come from [[ylloc.f#YLLOC|YLLOC]] (`CFORD2`) and `LL4TH` (`CFORD42`).

## Questions for the experts

1. **Duplicated code.** `YLLO2D` and `YLLO2D2` differ only in their COMMON blocks; passing the table as arguments would make one routine. Worth doing in the overhaul? (The stop message differs too, "OPAL95 2D2 CHECK NDSS", with the same mislabel as `YLLO2D`'s: these are OPAL92 tables.)

### YLLO2D2

`YLLO2D` for the second-$Z$ OPAL92 table.
