## Explanation

**Purpose.** Diffuses one species over one time step on the equally spaced grid, for [[microdiff.f#MICRODIFF|MICRODIFF]], and returns the change in its abundance. The comments describe the diffusion equation as two terms: one with $d\ln P/dr$ and the abundance gradient (solved explicitly, by the two-step Lax–Wendroff scheme of Numerical Recipes), and one with the second derivative of the abundance (solved implicitly).

**How it fits.**
- **Inputs:** the equal grid and midpoint variables from [[microdiff_mte.f#MICRODIFF_MTE|MICRODIFF_MTE]]: mass `EM`, radius `ER`, density, temperature, $d\ln P/dr$, $\nabla$ and the three-species abundances `ESPEC(3,·)`; the spacing `DR`; `DT` and `STOT` in Bahcall–Loeb units; and the species' weight `THEA`, charge `THEZ` and column `J` (1 for hydrogen, 3 for metals or a light element).
- **Who calls it:** only `MICRODIFF`, once per diffused species.
- **What it calls:** [[microdiff_cod.f#MICRODIFF_COD|MICRODIFF_COD]] (the coefficients, twice), [[lax_wendrof1.f#LAX_WENDROF1|LAX_WENDROF1]] and [[lax_wendrof2.f#LAX_WENDROF2|LAX_WENDROF2]] (the explicit term), [[get_imp_diffco.f#GET_IMP_DIFFCO|GET_IMP_DIFFCO]] (the matrix) and [[tridiag_gs.f#TRIDIAG_GS|TRIDIAG_GS]] (its solution).
- **Output:** `ESPEC(J,·)` is overwritten with the change $X^\mathrm{new}_i - X^\mathrm{old}_i$; `EDXDR` (the hydrogen concentration gradient, filled on the hydrogen call) is kept for later calls. A line per iteration goes to `ISHORT`, and a warning to `IOWR` and `ISHORT` if the iteration does not converge.
- **COMMON blocks:** `/GRAVST/` (`GRTOL`, `NITER_GS`), `/CONST1/` ($4\pi$), `/LUOUT/`; `/THEAGE/` is declared but not used.

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
6. **Result:** $\Delta X_i = X^\mathrm{new}_i - X_i$ in `ESPEC(J,·)`.

**Design.** The change rather than the new abundance is returned, as the comments explain, so that the interpolation back to the model grid adds less error. The first and last cells hold the masses of the convective core and envelope, whose changes [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] then applies to every point inside them.

**KC's changes.** 2025-05-31: unused arguments `NLIGHT` and `CSLIGHT` removed.

## Questions for the experts

1. **An iteration that cannot change anything.** Inside the loop, `GET_IMP_DIFFCO` corrects `ECOD2_H` by `EQCOD2X_H * ED_H`, but `EQCOD2X_H` is set to zero just before ("only used in GRSETT … retained for legacy"). So the matrix and the right-hand side are the same in every iteration, and the second iteration always reproduces the first. Is the loop (and the convergence test on `GRTOL`) still meaningful, or should the coefficients be recomputed from the new abundances?
2. **The convergence test is one-sided.** `DXMAX` takes the largest *signed* change `ED(I)-ED_P(I)`, starting from zero; negative changes are never seen. Should it be the absolute value?
3. **The midpoint change.** `ED_H(I) = 0.5*(ED(I)+ED(I-1)-…)` for `I = 2..NPT` assigns to midpoint `I` the mean of points `I-1` and `I`, while in `MICRODIFF_MTE` midpoint `I` lies between points `I` and `I+1`. It has no effect now (see question 1), but would if `EQCOD2X_H` were used.
4. **A comment that names a different element.** The convergence comment speaks of "the corrections to the hydrogen abundance" and the solve of "the new run of Li"; the routine diffuses any species.

### MICRODIFF_RUN

One species, one step: explicit two-step Lax–Wendroff for the advective term, then an implicit tridiagonal solve for the diffusive term (equations above). Returns the change in abundance.
