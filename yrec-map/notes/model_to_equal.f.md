## Explanation

**Purpose.** "Model to equal" for the older settling routine [[grsett.f#GRSETT|GRSETT]]: it interpolates the diffusion coefficients and the abundances from the model points to an equally spaced grid in radius, at the grid points and at the midpoints. [[microdiff_mte.f#MICRODIFF_MTE|MICRODIFF_MTE]] is its newer counterpart, for [[microdiff.f#MICRODIFF|MICRODIFF]].

**How it fits.**
- **Inputs:** the coefficients `COD1`, `COD2` and their derivatives with respect to $X$, `QCOD1X`, `QCOD2X`, at the model points (from [[setup_grsett.f#SETUP_GRSETT|SETUP_GRSETT]]); the metal coefficients `COD1Z`, `COD2Z`, `QCOD1Z`, `QCOD2Z` (arguments, formerly `/GRAVSZ/`: SETUP_GRSETT fills them in arrays GRSETT owns); `HCOMP`, the radii `HRU` and masses `HS1` in Bahcall–Loeb units; `IBEGIN`, `IEND`, `M`.
- **Who calls it:** only [[grsett.f#GRSETT|GRSETT]].
- **What it calls:** [[interp.f#INTERP|INTERP]] (four-point Lagrange weights).
- **Outputs:** `NPT`, `DR`, the grid radii `ER`, and on the points and midpoints: masses (`EM`, `EM_H`), coefficients (`ECOD1`, `ECOD1_H`, `ECOD2_H`, `EQCOD1X_H`, `EQCOD2X_H`) and hydrogen (`EX`, `EX_H`). For metals (`LDIFZ`), the same in `GRAVEZ_MOD`, which [[lax_wendrof1.f#LAX_WENDROF1|LAX_WENDROF1]], [[lax_wendrof2.f#LAX_WENDROF2|LAX_WENDROF2]], GRSETT and [[equal_to_model.f#EQUAL_TO_MODEL|EQUAL_TO_MODEL]] read.
- **Modules:** `NMLPAR_MOD` (`LDIFZ`), `GRAVEZ_MOD` (written), `DIMENSIONS_MOD` (`JSON`).

**The method.** As in `MICRODIFF_MTE`: the number of points $N = \lceil (r_\mathrm{end}-r_\mathrm{begin})/\Delta r_\mathrm{min}\rceil$ (at least 4, at most `JSON`), here with $\Delta r_\mathrm{min}$ the smallest spacing over the whole region; the first midpoint by linear interpolation, the others by four-point Lagrange interpolation, $f(r) = \sum_{k=1}^4 w_k(r)\,f_{k_0+k-1}$; the end points take the model's values. The midpoint search for the first midpoint runs over the wrong range of indices ([[#b1]]).

The metals' abundances on the grid, `EZ` and `EZ_H`, are interpolated from `HCOMP(8,·)` (¹⁵N in [[mix.f#MIX|MIX]]), not from $Z$ (`HCOMP(3,·)`); this does not change the result: `LAX_WENDROF1` overwrites `EZ_H(1..NPT-1)`, and `GRSETT` returns only the change `EZ - EZ_ORIG`, in which the starting values cancel, while the change itself comes from `COD1Z`, which `SETUP_GRSETT` computes from $Z$ (settled from the code, Nov 9, 2026: [[#L108]], [[#L189-L190]], [[#L209]], [[#L260-L261]], [[#L271]]; [[lax_wendrof1.f#L59-L74]]; [[grsett.f#L149-L153]], [[grsett.f#L259-L265]]; [[setup_grsett.f#L209]], [[setup_grsett.f#L311]]).

`ER` holds the midpoints' radii while the midpoints are interpolated, and is then overwritten with the grid points' radii ([[#L76-L85]]; [[#L195-L198]]); the caller needs only the latter, for [[equal_to_model.f#EQUAL_TO_MODEL|EQUAL_TO_MODEL]] (settled from the code, Nov 9, 2026: [[grsett.f#L269-L270]]). The "center derivative" block computes `FAC1`, `FAC2`, and `DELR` (from `DR1`, `DR2`), which nothing reads ([[#L110-L125]]: unused?); the line `IF(I-1 .EQ. 0) PRINT*, 'mte line 47'` cannot fire, since `I` starts at 2, and names the other file ([[#L82]]: unused?); and the branch for `NPT .EQ. 2` ([[#L78-L79]]) can no longer be taken, since `NPT` is at least 4 (unused?).

**Changed since `rp_1`.** The metal coefficients `COD1Z`, `COD2Z`, `QCOD1Z`, `QCOD2Z` are four new last arguments (formerly `/GRAVSZ/`); COMMON blocks to modules, `IMPLICIT NONE`. No question is settled.

**Changed since `a8a5950`.** The grid has at least 4 points, not 2: The four-point Lagrange stencils here and in [[equal_to_model.f#EQUAL_TO_MODEL|EQUAL_TO_MODEL]] read `ER(K0..K0+3)`, so a 2- or 3-point grid read points never set, or `ER(-1)` and `ER(0)`.

## Bugs, by priority

1. **(a)** **The first midpoint's search runs over the wrong indices.** ([[#L91-L97]]) The search for the model point above the first midpoint `ER(1)` runs over `IU = 2..NPT`: model indices from 2, bounded by the number of *equal-grid* points, rather than `IBEGIN+1..IEND`. Since `NPT` is at least `IEND - IBEGIN` (every model spacing in the range is at least `DRMIN`), the search finds the right point whenever `IBEGIN + 1 <= NPT`; when `IBEGIN` is larger (a large convective or hydrogen-exhausted core under a radiative zone of few, evenly spaced shells), `IU` falls back to `NPT`, and the first midpoint's mass, coefficients, and $X$ are extrapolated from two points far below it. Whether models reach this case was not traced. Only with `LDIFY` (off by default) and `LNEWDIF` false (the default). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to search the model points of the settling range,
    C not the indices 2..NPT of the equal grid.
          DO 15 IU=IBEGIN+1,IEND
             IF(HRU(IU).GE.ER(1))GOTO 17
       15 CONTINUE
          IU=IEND
       17 CONTINUE
    ```
