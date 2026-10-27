## Explanation

**Purpose.** "Model to equal" for the older settling routine [[grsett.f#GRSETT|GRSETT]]: it interpolates the diffusion coefficients and the abundances from the model points to an equally spaced grid in radius, at the grid points and at the midpoints. [[microdiff_mte.f#MICRODIFF_MTE|MICRODIFF_MTE]] is its newer counterpart, for [[microdiff.f#MICRODIFF|MICRODIFF]].

**How it fits.**
- **Inputs:** the coefficients `COD1`, `COD2` and their derivatives with respect to $X$, `QCOD1X`, `QCOD2X`, at the model points (from [[setup_grsett.f#SETUP_GRSETT|SETUP_GRSETT]]); the metal coefficients `COD1Z`, `COD2Z`, `QCOD1Z`, `QCOD2Z` (arguments, formerly `/GRAVSZ/`: SETUP_GRSETT fills them in arrays GRSETT owns); `HCOMP`, the radii `HRU` and masses `HS1` in Bahcall–Loeb units; `IBEGIN`, `IEND`, `M`.
- **Who calls it:** only [[grsett.f#GRSETT|GRSETT]].
- **What it calls:** [[interp.f#INTERP|INTERP]] (four-point Lagrange weights).
- **Outputs:** `NPT`, `DR`, the grid radii `ER`, and on the points and midpoints: masses (`EM`, `EM_H`), coefficients (`ECOD1`, `ECOD1_H`, `ECOD2_H`, `EQCOD1X_H`, `EQCOD2X_H`) and hydrogen (`EX`, `EX_H`). For metals (`LDIFZ`), the same in `GRAVEZ_MOD`, which [[lax_wendrof1.f#LAX_WENDROF1|LAX_WENDROF1]], [[lax_wendrof2.f#LAX_WENDROF2|LAX_WENDROF2]], GRSETT and [[equal_to_model.f#EQUAL_TO_MODEL|EQUAL_TO_MODEL]] read.
- **Modules:** `NMLPAR_MOD` (`LDIFZ`), `GRAVEZ_MOD` (written), `DIMENSIONS_MOD` (`JSON`).

**The method.** As in `MICRODIFF_MTE`: the number of points $N = \lceil (r_\mathrm{end}-r_\mathrm{begin})/\Delta r_\mathrm{min}\rceil$ (at least 2, at most `JSON`), here with $\Delta r_\mathrm{min}$ the smallest spacing over the whole region; the first midpoint by linear interpolation, the others by four-point Lagrange interpolation, $f(r) = \sum_{k=1}^4 w_k(r)\,f_{k_0+k-1}$; the end points take the model's values.

**KC's changes.** 2025-05-31: the unused arguments `HQPR` and `HTU` removed.

**Changed since `rp_1`.** The metal coefficients `COD1Z`, `COD2Z`, `QCOD1Z`, `QCOD2Z` are four new last arguments (formerly `/GRAVSZ/`); COMMON blocks to modules, `IMPLICIT NONE`. No question is settled.

## Questions for the experts

1. **The metals come from row 8.** `EZ` and `EZ_H` are interpolated from `HCOMP(8,·)`, while [[equal_to_model.f#EQUAL_TO_MODEL|EQUAL_TO_MODEL]] applies the change to `HCOMP(3,·)` ($Z$), and [[mix.f#MIX|MIX]] names row 8 ¹⁵N (`XN15`). Is row 8 a mistake for row 3? If so, the old routine's metal settling has been computed from the ¹⁵N profile.
2. **Unused derivative factors.** The "center derivative" block computes `FAC1`, `FAC2` and `DELR`, which are never used.
3. **The first midpoint's search.** As in `MICRODIFF_MTE`, the search runs over model indices `2..NPT` (bounded by the number of grid points) rather than `IBEGIN+1..IEND`.
4. **Midpoint radii lost.** `ER` first holds the midpoint radii and is then overwritten with the grid points' radii, so the caller never sees the midpoints' radii. Intended?
5. **A debugging line.** `IF(I-1 .EQ. 0) PRINT*, 'mte line 47'` cannot fire, and names the other file.
