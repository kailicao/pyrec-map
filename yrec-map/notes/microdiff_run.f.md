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

    > **Question** ([[#L82]]; [[#L172]]; [[#L176-L177]]). **Comments that name a different element.** The comments speak of "the original run of light element mass fractions", "the new run of LI" and "the corrections to the hydrogen abundance"; the routine diffuses any species. Should they say "the diffused species"?

6. **Result:** $\Delta X_i = X^\mathrm{new}_i - X_i$ in `ESPEC(J,·)`.

**Design.** The change rather than the new abundance is returned, as the comments explain, so that the interpolation back to the model grid adds less error. The first and last cells hold the masses of the convective core and envelope, whose changes [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] then applies to every point inside them.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html): `GRTOL` (default 1.0D-8) is the numerical tolerance on the abundance changes from diffusion, and `NITER_GS` (10) the largest number of iterations of the solver.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Bugs, by priority

1. **(c)** **With `NITER_GS = 0`, the implicit term is skipped and the warning prints old values.** ([[#L152]]; [[#L178-L196]]) With `NITER_GS` = 0 the loop never runs: The implicit (diffusive) term is not applied at all, and the warning "MICRODIFF FAILED TO CONVERGE" prints `DXMAX` and `IMAX` left from an earlier call (all locals are `SAVE`d). Only with `NITER_GS` = 0 (the default is 10). Read from the code, not run. **A possible fix:** reject `NITER_GS` < 1 where the namelist is read, or set `DXMAX = 0.0D0` and `IMAX = 0` before the loop so that the message is at least true.

2. **(d)** **The convergence test is one-sided.** ([[#L178-L190]]) `DXMAX` takes the largest *signed* change `ED(I)-ED_P(I)`, starting from zero, so negative changes are never seen, in the test or in the printed line. Correct today, since the second iteration reproduces the first (question 1); it would end the loop too early if the iterations changed anything. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to test the size of the change, not its signed value.
             DO I = 1,NPT
                DX = ABS(ED(I)-ED_P(I))
    ...
    ```

3. **(d)** **The midpoint change is shifted by one point.** ([[#L155-L157]]) `ED_H(I) = 0.5*(ED(I)+ED(I-1)-…)` for `I = 2..NPT` assigns to midpoint `I` the mean of points `I-1` and `I`, while in [[microdiff_mte.f#MICRODIFF_MTE|MICRODIFF_MTE]] midpoint `I` lies between points `I` and `I+1` ([[microdiff_mte.f#L85-L93]]); midpoint 1 keeps its value from `LAX_WENDROF1`. No effect today, since `EQCOD2X_H` is zero (question 1), but it would matter if `EQCOD2X_H` were used. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to put the change between points I and I+1 at
    C midpoint I, as MICRODIFF_MTE places the midpoints.
             DO I = 1,NPT-1
                ED_H(I) = 0.5D0*(ED(I+1)+ED(I)-ED_P(I+1)-ED_P(I))
             ENDDO
    ```

### MICRODIFF_RUN

One species, one step: explicit two-step Lax–Wendroff for the advective term, then an implicit tridiagonal solve for the diffusive term (equations above). Returns the change in abundance.
