## Explanation

**Purpose.** Diffuses one species over one time step on the equally spaced grid, for [[microdiff.f#MICRODIFF|MICRODIFF]], and returns the change in its abundance. The comments describe the diffusion equation as two terms: one with $d\ln P/dr$ and the abundance gradient (solved explicitly, by the two-step Lax–Wendroff scheme of Numerical Recipes), and one with the second derivative of the abundance (solved implicitly).

**How it fits.**
- **Inputs:** the equal grid and midpoint variables from [[microdiff_mte.f#MICRODIFF_MTE|MICRODIFF_MTE]]: mass `EM`, radius `ER`, density, temperature, $d\ln P/dr$, $\nabla$ and the three-species abundances `ESPEC(3,·)`; the spacing `DR`; `DT` and `STOT` in Bahcall–Loeb units; and the species' weight `THEA`, charge `THEZ` and column `J` (1 for hydrogen, 3 for metals or a light element).
- **Who calls it:** only `MICRODIFF`, once per diffused species.
- **What it calls:** [[microdiff_cod.f#MICRODIFF_COD|MICRODIFF_COD]] (the coefficients, twice), [[lax_wendrof1.f#LAX_WENDROF1|LAX_WENDROF1]] and [[lax_wendrof2.f#LAX_WENDROF2|LAX_WENDROF2]] (the explicit term), [[get_imp_diffco.f#GET_IMP_DIFFCO|GET_IMP_DIFFCO]] (the matrix) and [[tridiag_gs.f#TRIDIAG_GS|TRIDIAG_GS]] (its solution).
- **Output:** `ESPEC(J,·)` is overwritten with the change $X^\mathrm{new}_i - X^\mathrm{old}_i$; `EDXDR` (the hydrogen concentration gradient, filled on the hydrogen call) is kept for later calls. A line per iteration goes to `ISHORT`, and a warning to `IOWR` and `ISHORT` if the iteration does not converge.
- **Modules:** `NMLPAR_MOD` (`GRTOL`, `NITER_GS`), `CONSTANTS_MOD` ($4\pi$, `C4PI`), `IOUNITS_MOD` (`ISHORT`, `IOWR`) and `DIMENSIONS_MOD` (`JSON`). The unused `/THEAGE/` of `rp_1` is no longer declared.

**The method.** Let $X_i$ be the abundance at grid point $i$ (radius $r_i$, mass $m_i$), and $X_{i+1/2}$ at the midpoints.
1. **Coefficients at the points.** `MICRODIFF_COD` gives the advective coefficient $C_{1,i}$ (`ECOD1`) and the diffusion coefficient $C_{2,i}$ (`ECOD2`).
2. **Lax–Wendroff, first half step** (`LAX_WENDROF1`), the change at the midpoints:
$$\Delta X_{i+1/2} = \frac{4\pi\,\Delta t}{2}\;\frac{C_{1,i+1} - C_{1,i}}{m_{i+1} - m_i},$$
where the first cell takes $C_{1,1} = 0$ and $m_1 = 0$, and the last cell $C_{1,N} = 0$ and $m_N =$ `STOT`, so the first and last cells reach to the centre and the surface.
3. **Coefficients at the midpoints**, from the half-step abundances $X_{i+1/2} + \Delta X_{i+1/2}$.
4. **Lax–Wendroff, full step** (`LAX_WENDROF2`), at the points:
$$X'_i = X_i + 4\pi\,\Delta t\;\frac{C_{1,i+1/2} - C_{1,i-1/2}}{m_{i+1/2} - m_{i-1/2}},$$
with $C_{1,1/2} = m_{1/2} = 0$ at the first point, and $C_{1,N+1/2} = 0$, $m_{N+1/2} =$ `STOT` at the last.
5. **The implicit term.** With $\alpha_i = 4\pi\,\Delta t / (\Delta r\, \Delta m_i)$ (`ALPHA`, where $\Delta m_i = m_{i+1/2} - m_{i-1/2}$, from the centre for $i=1$ and to `STOT` for $i=N$), `GET_IMP_DIFFCO` builds and `TRIDIAG_GS` solves
$$X_i - \alpha_i\left[C_{2,i+1/2}\,(X_{i+1}-X_i) - C_{2,i-1/2}\,(X_i - X_{i-1})\right] = X'_i .$$
The loop repeats until the largest change between iterations is below `GRTOL`, at most `NITER_GS` times.

    > **Question** ([[#L160-L174]]; [[get_imp_diffco.f#L20]]). **An iteration that cannot change anything.** Inside the loop, `GET_IMP_DIFFCO` corrects `ECOD2_H` by `EQCOD2X_H * ED_H`, but `EQCOD2X_H` is set to zero just before ("only used in GRSETT … retained for legacy"). So the matrix and the right-hand side `ED_PRIME` are the same in every iteration, and the second iteration always reproduces the first (its change is zero, below `GRTOL`). Is the loop (and the convergence test on `GRTOL`) still meaningful, or should the coefficients be recomputed from the new abundances?

    **The comments name the elements of an older use.** They speak of "the original run of light element mass fractions," "the new run of LI," and "the corrections to the hydrogen abundance" ([[#L82]]; [[#L172]]; [[#L176-L177]]), but `ED` is loaded from `ESPEC(J,·)` ([[#L80]]) for whichever species `J` the caller passes, so they could say "the diffused species."

6. **Result:** $\Delta X_i = X^\mathrm{new}_i - X_i$ in `ESPEC(J,·)`.

**Design.** The change rather than the new abundance is returned, as the comments explain, so that the interpolation back to the model grid adds less error. The first and last cells hold the masses of the convective core and envelope, whose changes [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] then applies to every point inside them.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html): `GRTOL` (default 1.0D-8) is the numerical tolerance on the abundance changes from diffusion, and `NITER_GS` (10) the largest number of iterations of the solver.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Bugs, by priority

1. **(never occurred)** **With `NITER_GS = 0`, the implicit term is skipped and the warning prints old values.** ([[#L152]]; [[#L178-L196]]) With `NITER_GS` = 0 the loop never runs: The implicit (diffusive) term is not applied at all, and the warning "MICRODIFF FAILED TO CONVERGE" prints `DXMAX` and `IMAX` left from an earlier call (all locals are `SAVE`d). Only with `NITER_GS` = 0 (the default is 10).

    **A possible fix:** reject `NITER_GS` < 1 where the namelist is read, or set `DXMAX = 0.0D0` and `IMAX = 0` before the loop so that the message is at least true.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The loop was entered at every settling call in the seven runs with settling (`testsuite/Test_solarGS98_dif`, `testsuite/Test_solarAAG21_dif`, `testsuite/Test_solarM22M_difkur`, `testsuite/Test_solarGS98_difrotmixper18p4d1p0`, `testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`, `testsuite/Test_m1p4feh+0p0GS98_dif_TAMS`, and `testsuite/Test_solarAAG21_dif` with a custom mixture), up to 18,515 times per run, always with `NITER_GS` = 10. Not reached: It needs `NITER_GS` = 0, and every case sets 10. No fix was run, since the page's fixes only stop the run or correct the message. Intent: none found.

2. **(harmless in the runs)** **The convergence test is one-sided.** ([[#L178-L190]]) `DXMAX` takes the largest *signed* change `ED(I)-ED_P(I)`, starting from zero, so negative changes are never seen, in the test or in the printed line. Correct today, since the second iteration reproduces the first (question 1); it would end the loop too early if the iterations changed anything.

    **A possible fix:**

    ```diff
    --- a/src/microdiff_run.f
    +++ b/src/microdiff_run.f
    @@ -177,8 +177,10 @@
     C  ENOUGH TO EXIT.
              DXMAX = 0.0D0
              IMAX = 0
    +C 11/09/26 KC via Claude
    +C code changed to test the size of the change, not its signed value.
              DO I = 1,NPT
    -            DX = ED(I)-ED_P(I)
    +            DX = ABS(ED(I)-ED_P(I))
                 IF(DX.GT.DXMAX)THEN
                    DXMAX = DX
                    IMAX = I
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The test ran in all seven runs with settling, 4,496 to 22,220 times per run, never more than two iterations a call. In 14 to 259 first iterations per run, the largest signed change was below `GRTOL` while the largest change in size, $2.0\times10^{-7}$ to $1.87\times10^{-6}$, was not, so the loop ended one iteration early. With the fix, `testsuite/Test_m1p4feh+0p0GS98_dif_TAMS` and `testsuite/Test_solarM22M_difkur` give identical tracks and stored models; the `.short` file differs beyond 2% (presumably its iteration lines; not checked). This agrees with the above: The second iteration repeats the first. Intent: none found.

3. **(cannot be reached)** **The midpoint change is shifted by one point.** ([[#L155-L157]]) `ED_H(I) = 0.5*(ED(I)+ED(I-1)-…)` for `I = 2..NPT` assigns to midpoint `I` the mean of points `I-1` and `I`, while in [[microdiff_mte.f#MICRODIFF_MTE|MICRODIFF_MTE]] midpoint `I` lies between points `I` and `I+1` ([[microdiff_mte.f#L85-L93]]); midpoint 1 keeps its value from `LAX_WENDROF1`. No effect today, since `EQCOD2X_H` is zero (question 1), but it would matter if `EQCOD2X_H` were used.

    **A possible fix:**

    ```diff
    --- a/src/microdiff_run.f
    +++ b/src/microdiff_run.f
    @@ -152,8 +152,11 @@
           DO 100 ITER=1,NITER_GS
     C  FIND CHANGE IN D AT THE ZONE MIDPOINTS, GIVEN CHANGE IN D AT
     C  THE ZONE CENTERS.
    -         DO I = 2,NPT
    -            ED_H(I) = 0.5D0*(ED(I)+ED(I-1)-ED_P(I)-ED_P(I-1))
    +C 11/09/26 KC via Claude
    +C code changed to put the change between points I and I+1 at
    +C midpoint I, as MICRODIFF_MTE places the midpoints.
    +         DO I = 1,NPT-1
    +            ED_H(I) = 0.5D0*(ED(I+1)+ED(I)-ED_P(I+1)-ED_P(I))
              ENDDO
     C  STORE CURRENT RUN OF ABUNDANCES IN VECTOR ED_P. THE ITERATION
     C  LOOP IS COMPLETED ONCE ED - ED_P IS EVERYWHERE LESS THAN THE TOLERANCE
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The midpoint changes were computed 4,496 to 22,220 times per run in all seven runs with settling, and `EQCOD2X_H` was zero every time. It cannot matter at 7be4133, since `EQCOD2X_H` is set to zero just before every use ([[#L162-L165]]); what remains is fragile code. The fix was not run. Intent: The comment there says `EQCOD2X_H` "IS ONLY USED IN GRSETT (OLD SETTLING ROUTINE), BUT RETAINED FOR LEGACY" ([[#L160-L161]]).

### MICRODIFF_RUN

One species, one step: explicit two-step Lax–Wendroff for the advective term, then an implicit tridiagonal solve for the diffusive term (equations above). Returns the change in abundance.
