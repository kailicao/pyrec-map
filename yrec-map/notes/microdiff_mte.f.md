## Explanation

**Purpose.** "Model to equal": interpolates the model's variables onto an equally spaced grid in radius, at the grid points and at the midpoints between them, for [[microdiff.f#MICRODIFF|MICRODIFF]].

**How it fits.**
- **Inputs:** from [[microdiff_setup.f#MICRODIFF_SETUP|MICRODIFF_SETUP]]: the radii `HRU` (units of $R_\odot$), `IBEGIN`, `IEND`, and the density `ODEN` and temperature `OTEM`; and the composition `HCOMP`, `HQPR`, `HS1` and $\nabla$ (`SDEL(2,·)` in `SCRTCH_MOD`).
- **Who calls it:** only `MICRODIFF`.
- **What it calls:** [[interp.f#INTERP|INTERP]], for the four-point Lagrange weights.
- **Outputs:** `NPT`, `DR`, and on the grid points (`E…`) and midpoints (`E…_H`): the mass $m$, $\rho$, $T$, $d\ln P/dr$, $\nabla$, $X$, $Y$, $Z$ and the light elements; these go to [[microdiff_run.f#MICRODIFF_RUN|MICRODIFF_RUN]]. The radius, mass and $d\ln P/dr$ are in the Bahcall–Loeb units of `MICRODIFF_SETUP`; $\rho$ and $T$ are in cgs units (g cm⁻³, K).
- **Modules:** `SCRTCH_MOD` (read: `SDEL`), `NMLPAR_MOD` (`LDIFLI`), `DIMENSIONS_MOD` (`JSON`).

**The method.**
1. **Spacing.** $\Delta r_\mathrm{min}$ is the smallest model spacing among the 20 points below `IEND` (the base of the surface convection zone). The number of points is
$$N = \left\lceil \frac{r_\mathrm{end} - r_\mathrm{begin}}{\Delta r_\mathrm{min}} \right\rceil,\quad N \ge 2,\quad N \le 5000\ (\mathrm{JSON}),\qquad \Delta r = \frac{r_\mathrm{end} - r_\mathrm{begin}}{N-1}.$$
2. **Midpoints.** $r_{i+1/2} = r_\mathrm{begin} + (i - \tfrac12)\Delta r$ for $i = 1,\dots,N-1$. The first is found by linear interpolation; the others by four-point Lagrange interpolation over the four model points around them, $f(r) = \sum_{k=1}^{4} w_k(r)\, f_{k_0+k-1}$.
3. **Grid points.** $r_i = r_\mathrm{begin} + (i-1)\Delta r$. The first and last take the model's values at `IBEGIN` and `IEND`; the others use the same four-point interpolation.

**KC's changes.** 2025-05-30: `CSLIGHT` declared `INTEGER` (fixing `-Wconversion`); 2025-05-31: unused arguments `HTU` and `LC` removed.

**Changed since `rp_1`.** The cap on `NPT` is now `JSON` itself (the same 5000) rather than a repeated literal; the authors' comment says the name `HALFJSON` is presumably left from an earlier cap of `JSON/2`, which settles the former question 3; COMMON blocks to modules (the unused `/GRAVS3/` is gone), `IMPLICIT NONE`.

## Questions for the experts

1. **The first midpoint's search.** The search for the model point above the first midpoint runs over `IU = 2..NPT`: model indices from 2, bounded by the number of *equal-grid* points, rather than `IBEGIN+1..IEND`. When `NPT` is smaller than the model index needed (a coarse equal grid, or a large `IBEGIN`), `IU` falls back to `NPT`, and the "interpolation" extrapolates from the wrong pair of points. A bug?
2. **Where the spacing is measured.** $\Delta r_\mathrm{min}$ is measured only over the 20 points below the surface convection zone ("ID THE MINIMUM SPACING IN THE 20 LAYERS BELOW THE SURFACE CZ"). Deeper regions with finer model spacing are then under-resolved. Intended?
3. **A debugging line.** `IF(I-1 .EQ. 0) PRINT*, 'mte line 47'` can never fire inside `DO 10 I = 2,NPT-1`.
4. **Interpolated composition.** Four-point Lagrange interpolation of $X$, $Y$, $Z$ near steep gradients can overshoot (negative or above one). Is that guarded anywhere? (Only changes are mapped back, which limits the harm.)
5. **The grid is coarser than the comment says.** The comment asks for "the minimum number of equally spaced grid points such that DR <= DRMIN", but `NPT` $=\lceil \Delta r_\mathrm{tot}/\Delta r_\mathrm{min}\rceil$ points make `NPT-1` intervals, so `DR` $= \Delta r_\mathrm{tot}/(N-1)$ is larger than $\Delta r_\mathrm{min}$ (up to twice as large when $N = 2$). Should `NPT` be one more?
