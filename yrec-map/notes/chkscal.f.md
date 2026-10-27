## Explanation

**Purpose.** This file calibrates a track of another star (not the Sun) to a given radius and luminosity: it watches the track for the moment it crosses the target radius $R_*$, compares the luminosity there with the target $L_*$, and adjusts the hydrogen abundance $X$ (thus $Y$) for the next run until the track passes through $(R_*, L_*)$. Then it sets up a final run that stops at the age where the track reaches $R_*$.

**How it fits.**
- **Inputs:** the arguments `BL` ($\log L/L_\odot$), `TEFFL` ($\log T_\mathrm{eff}$), `DAGE` (age, Gyr), `NK` (kind card) and `ALRI` (the previous model's radius, kept by the main program and started by [[setscal.f#SETSCAL|SETSCAL]]); in [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] (set by [[parmin.f#PARMIN|PARMIN]]), the targets `SR` ($R_*/R_\odot$), `XLS` ($L_*/L_\odot$) and the tolerance `XLSTOL`; the previous model's `BLI`, `AGEI`, local variables kept by `SAVE`.
- **Who calls it:** the main program ([[main.f#(file level)|main.f]]), for even kind cards, when the option `LCALST` is on and the star has not yet been found (`LSTAR` false), from the second model on.
- **Outputs:** the arguments `LPASSR` (main.f then ends the run), `LSTAR` and `ALRI`; `BLR`, `AGER`, `BLRP` are saved locals; for the next kind cards, the new $X$ (`RESCAL(2,·)` in [[runloop_mod.f#RUNLOOP_MOD|`RUNLOOP_MOD`]], `XENV0A` in `NMLPAR_MOD`), or the stopping age (`LENDAG` in `RUNLOOP_MOD`, `ENDAGE` in `NMLPAR_MOD`). Lines to the screen and to `ITRACK`.

**The method.**
1. The radius from $L$ and $T_\mathrm{eff}$, in solar units:
$$\frac{R}{R_\odot} = \frac{\sqrt{L/(4\pi\sigma)}}{T_\mathrm{eff}^2\,R_\odot}.$$
If the track has not crossed $R_*$ since the previous model, store $L$, the age and $R$, and return.
2. At the crossing, interpolate linearly in $R$ between the two models for $\log L$ and the age at $R_*$.
3. If $|L/L_\odot - L_*/L_\odot| \le$ `XLSTOL`, the star is found: the next two kind cards run with the same $X$ and stop at that age (in years, $10^9 \times$ Gyr).
4. Otherwise, at the first pass (`NK = 2`) lower $X$ by 0.01 ("Y=Y+0.01"); afterwards take a secant step in $X$ against $\log L$:
$$X_\mathrm{new} = X + \frac{X - X_\mathrm{prev}}{\log L_R - \log L_{R,\mathrm{prev}}}\,\left(\log L_* - \log L_R\right).$$

**Changed since `rp_1`.** `/CALSTAR/` retired: `ALRI`, `LSTAR`, `LPASSR` are now arguments (owned by the main program), `BLI`, `AGEI`, `BLR`, `AGER`, `BLRP` saved locals, the targets in `NMLPAR_MOD`; COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **Linear or log radius.** The comments call `ALR` and `ALRI` "log(R/Rsun)", but the code computes $R/R_\odot$ itself; `SR` is described as $R/R_\odot$, so the comparison is consistent, and only the comments are wrong. The interpolation is thus linear in $R$.
2. **`LTEFF` unused.** The comments describe an option `LTEFF` to give the star's $T_\mathrm{eff}$ instead of its radius; this routine ignores it and always uses `SR`. Is it handled elsewhere (in SETSCAL, perhaps)?
3. **Two tolerances.** The test on $L$ is in linear units ($|L - L_*| \le$ `XLSTOL`), the secant step in $\log L$. Fine, but `XLSTOL` must be given in $L_\odot$.
4. **The first crossing only.** The comment "Check if track has passed through Teff the right number of times" has no code behind it: the first crossing of $R_*$ (in either direction) is used. For tracks that cross $R_*$ more than once (pre-main sequence, then main sequence), is the first crossing the right one?
5. **The previous model across runs.** `ALRI`, `BLI`, `AGEI` get start values only once, `ALRI` in [[setscal.f#SETSCAL|SETSCAL]] (`ALRI = 0`, called once before the kind cards), and are not updated at the crossing. The first comparison of each later run (at its second model: main.f skips the first, only setting `TEFFI`, which nothing reads) is thus made against the model just before $R_*$ in the previous run. If the runs start above $R_*$ (pre-main sequence) and the previous run crossed $R_*$ on the way up, a false crossing is found at once, and $L$ and the age are interpolated between two runs. Should `ALRI` be reset at the start of each run?

### CHKSCAL

Calibrates $X$ (thus $Y$) so that a track passes through a target $(R_*, L_*)$: detects the crossing of $R_*$, interpolates $L$ and the age there, and sets $X$ by a secant step, or sets the final run's stopping age.
