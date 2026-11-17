## Explanation

**Purpose.** "Model to equal" for the older settling routine [GRSETT](grsett.f.md#grsett): it interpolates the diffusion coefficients and the abundances from the model points to an equally spaced grid in radius, at the grid points and at the midpoints. [MICRODIFF_MTE](microdiff_mte.f.md#microdiff_mte) is its newer counterpart, for [MICRODIFF](microdiff.f.md#microdiff).

**How it fits.**
- **Inputs:** the coefficients `COD1`, `COD2` and their derivatives with respect to $`X`$, `QCOD1X`, `QCOD2X`, at the model points (from [SETUP_GRSETT](setup_grsett.f.md#setup_grsett)); the metal coefficients `COD1Z`, `COD2Z`, `QCOD1Z`, `QCOD2Z` (arguments, formerly `/GRAVSZ/`: SETUP_GRSETT fills them in arrays GRSETT owns); `HCOMP`, the radii `HRU` and masses `HS1` in Bahcall–Loeb units; `IBEGIN`, `IEND`, `M`.
- **Who calls it:** only [GRSETT](grsett.f.md#grsett).
- **What it calls:** [INTERP](interp.f.md#interp) (four-point Lagrange weights).
- **Outputs:** `NPT`, `DR`, the grid radii `ER`, and on the points and midpoints: masses (`EM`, `EM_H`), coefficients (`ECOD1`, `ECOD1_H`, `ECOD2_H`, `EQCOD1X_H`, `EQCOD2X_H`) and hydrogen (`EX`, `EX_H`). For metals (`LDIFZ`), the same in `GRAVEZ_MOD`, which [LAX_WENDROF1](lax_wendrof1.f.md#lax_wendrof1), [LAX_WENDROF2](lax_wendrof2.f.md#lax_wendrof2), GRSETT and [EQUAL_TO_MODEL](equal_to_model.f.md#equal_to_model) read.
- **Modules:** `NMLPAR_MOD` (`LDIFZ`), `GRAVEZ_MOD` (written), `DIMENSIONS_MOD` (`JSON`).

**The method.** As in `MICRODIFF_MTE`: the number of points $`N = \lceil (r_\mathrm{end}-r_\mathrm{begin})/\Delta r_\mathrm{min}\rceil`$ (at least 4, at most `JSON`), here with $`\Delta r_\mathrm{min}`$ the smallest spacing over the whole region; the first midpoint by linear interpolation, the others by four-point Lagrange interpolation, $`f(r) = \sum_{k=1}^4 w_k(r)\,f_{k_0+k-1}`$; the end points take the model's values. The midpoint search for the first midpoint runs over the wrong range of indices ([suspected bug 1](#b1)).

The metals' abundances on the grid, `EZ` and `EZ_H`, are interpolated from `HCOMP(8,·)` ($`^{15}\mathrm{N}`$ in [MIX](mix.f.md#mix)), not from $`Z`$ (`HCOMP(3,·)`); this does not change the result: `LAX_WENDROF1` overwrites `EZ_H(1..NPT-1)`, and `GRSETT` returns only the change `EZ - EZ_ORIG`, in which the starting values cancel, while the change itself comes from `COD1Z`, which `SETUP_GRSETT` computes from $`Z`$ (settled from the code, Nov 9, 2026: [line 108](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L108), [lines 189–190](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L189-L190), [line 209](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L209), [lines 260–261](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L260-L261), [line 271](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L271); [lax_wendrof1.f, lines 59–74](https://github.com/yreclab/yrec/blob/7be4133/src/lax_wendrof1.f#L59-L74); [grsett.f, lines 149–153](https://github.com/yreclab/yrec/blob/7be4133/src/grsett.f#L149-L153), [grsett.f, lines 259–265](https://github.com/yreclab/yrec/blob/7be4133/src/grsett.f#L259-L265); [setup_grsett.f, line 209](https://github.com/yreclab/yrec/blob/7be4133/src/setup_grsett.f#L209), [setup_grsett.f, line 311](https://github.com/yreclab/yrec/blob/7be4133/src/setup_grsett.f#L311)).

`ER` holds the midpoints' radii while the midpoints are interpolated, and is then overwritten with the grid points' radii ([lines 76–85](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L76-L85); [lines 195–198](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L195-L198)); the caller needs only the latter, for [EQUAL_TO_MODEL](equal_to_model.f.md#equal_to_model) (settled from the code, Nov 9, 2026: [grsett.f, lines 269–270](https://github.com/yreclab/yrec/blob/7be4133/src/grsett.f#L269-L270)). The "center derivative" block computes `FAC1`, `FAC2`, and `DELR` (from `DR1`, `DR2`), which nothing reads ([lines 110–125](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L110-L125): unused?); the line `IF(I-1 .EQ. 0) PRINT*, 'mte line 47'` cannot fire, since `I` starts at 2, and names the other file ([line 82](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L82): unused?); and the branch for `NPT .EQ. 2` ([lines 78–79](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L78-L79)) can no longer be taken, since `NPT` is at least 4 (unused?).

**Changed since `rp_1`.** The metal coefficients `COD1Z`, `COD2Z`, `QCOD1Z`, `QCOD2Z` are four new last arguments (formerly `/GRAVSZ/`); COMMON blocks to modules, `IMPLICIT NONE`. No question is settled.

**Changed since `a8a5950`.** The grid has at least 4 points, not 2: The four-point Lagrange stencils here and in [EQUAL_TO_MODEL](equal_to_model.f.md#equal_to_model) read `ER(K0..K0+3)`, so a 2- or 3-point grid read points never set, or `ER(-1)` and `ER(0)`.

## Bugs, by priority

1. **(not reached)** **The first midpoint's search runs over the wrong indices.** ([lines 91–97](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L91-L97)) The search for the model point above the first midpoint `ER(1)` runs over `IU = 2..NPT`: model indices from 2, bounded by the number of *equal-grid* points, rather than `IBEGIN+1..IEND`. Since `NPT` is at least `IEND - IBEGIN` (every model spacing in the range is at least `DRMIN`), the search finds the right point whenever `IBEGIN + 1 <= NPT`; when `IBEGIN` is larger (a large convective or hydrogen-exhausted core under a radiative zone of few, evenly spaced shells), `IU` falls back to `NPT`, and the first midpoint's mass, coefficients, and $`X`$ are extrapolated from two points far below it. Whether models reach this case was not traced. Only with `LDIFY` (off by default) and `LNEWDIF` false (the default).

    **A possible fix:**

    ```diff
    --- a/src/model_to_equal.f
    +++ b/src/model_to_equal.f
    @@ -88,10 +88,13 @@
     C  AT EQUALLY SPACED ZONE MIDPOINTS.
     C
     C  FIRST POINT : LINEAR INTERPOLATION BETWEEN STARTING POINT AND 2ND PT.
    -      DO 15 IU=2,NPT
    +C 11/09/26 KC via Claude
    +C code changed to search the model points of the settling range,
    +C not the indices 2..NPT of the equal grid.
    +      DO 15 IU=IBEGIN+1,IEND
              IF(HRU(IU).GE.ER(1))GOTO 17
        15 CONTINUE
    -      IU=NPT
    +      IU=IEND
        17 CONTINUE
           FX=(ER(1)-HRU(IU-1))/(HRU(IU)-HRU(IU-1))
           EM_H(1) = HS1(IU-1)+FX*(HS1(IU)-HS1(IU-1))
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): not reached in any of 34 runs (26 of YREC's cases, from $`0.04`$ to $`9\,M_\odot`$, with rotation, settling, and helium burning, and 8 made-up ones). These lines belong to the old settling routines (`LNEWDIF` false), which no case uses: Every case with settling sets `LNEWDIF` and `LDIFLI`, and the documentation lists `LNEWDIF` among the legacy options (`docs/source/namelist_physics.md`, line 285). Reaching them takes `LDIFY` or `LDIFZ` with `LNEWDIF` false and `LDIFLI` off, since `LDIFLI` forces `LNEWDIF` on ([parmin.f, lines 1239–1251](https://github.com/yreclab/yrec/blob/7be4133/src/parmin.f#L1239-L1251)), and a model whose `IBEGIN` exceeds `NPT`. The same search in the new routines ([microdiff_mte.f, suspected bug 1](microdiff_mte.f.md#b1)) never failed in the seven runs with settling. Intent: The comment "FIRST POINT : LINEAR INTERPOLATION BETWEEN STARTING POINT AND 2ND PT." ([line 90](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L90)) names the point above `IBEGIN`, which the search is meant to find.
