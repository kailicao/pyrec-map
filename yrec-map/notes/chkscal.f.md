## Explanation

**Purpose.** This file calibrates a track of another star (not the Sun) to a given radius and luminosity: it watches the track for the moment it crosses the target radius $R_*$, compares the luminosity there with the target $L_*$, and adjusts the hydrogen abundance $X$ (thus $Y$) for the next run until the track passes through $(R_*, L_*)$. Then it sets up a final run that stops at the age where the track reaches $R_*$.

**How it fits.**
- **Inputs:** the arguments `BL` ($\log L/L_\odot$), `TEFFL` ($\log T_\mathrm{eff}$), `DAGE` (age, Gyr), `NK` (kind card) and `ALRI` (the previous model's radius, kept by the main program and started by [[setscal.f#SETSCAL|SETSCAL]]); in [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] (set by [[parmin.f#PARMIN|PARMIN]]), the targets `SR` ($R_*/R_\odot$; computed by [[setscal.f#SETSCAL|SETSCAL]] from `STEFF` when the option `LTEFF` gives the star's $T_\mathrm{eff}$ instead, so this routine needs only `SR`, settled from the code, Nov 9, 2026: [[setscal.f#L102-L106]]), `XLS` ($L_*/L_\odot$) and the tolerance `XLSTOL`; the previous model's `BLI`, `AGEI`, local variables kept by `SAVE`.
- **Who calls it:** the main program ([[main.f#(file level)|main.f]]), for even kind cards, when the option `LCALST` is on and the star has not yet been found (`LSTAR` false), from the second model on ([[main.f#L1117-L1123]]; the first model only sets `TEFFI`, which nothing reads: unused?).
- **Outputs:** the arguments `LPASSR` (main.f then ends the run), `LSTAR` and `ALRI`; `BLR`, `AGER`, `BLRP` are saved locals; for the next kind cards, the new $X$ (`RESCAL(2,·)` in [[runloop_mod.f#RUNLOOP_MOD|`RUNLOOP_MOD`]], `XENV0A` in `NMLPAR_MOD`), or the stopping age (`LENDAG` in `RUNLOOP_MOD`, `ENDAGE` in `NMLPAR_MOD`). Lines to the screen and to `ITRACK`.

**The method.**
1. The radius from $L$ and $T_\mathrm{eff}$, in solar units:
$$\frac{R}{R_\odot} = \frac{\sqrt{L/(4\pi\sigma)}}{T_\mathrm{eff}^2\,R_\odot}.$$
If the track has not crossed $R_*$ since the previous model, store $L$, the age and $R$, and return.

    > **Question** ([[#L81-L82]]; [[#L96]]). **Linear or log radius.** The comments call `ALR` and `ALRI` "log(R/Rsun)", but the code computes $R/R_\odot$ itself; `SR` is described as $R/R_\odot$, so the comparison is consistent and the interpolation is linear in $R$. Can the comments say $R/R_\odot$?

    > **Question** ([[#L97-L117]]). **The first crossing only.** The comment "Check if track has passed through Teff the right number of times" has no code behind it: The first crossing of $R_*$ (in either direction) is used. For tracks that cross $R_*$ more than once (pre-main sequence, then main sequence), is the first crossing the right one?
2. At the crossing, interpolate linearly in $R$ between the two models for $\log L$ and the age at $R_*$.
3. If $|L/L_\odot - L_*/L_\odot| \le$ `XLSTOL`, the star is found: the next two kind cards run with the same $X$ and stop at that age (in years, $10^9 \times$ Gyr). The test is in linear units, so `XLSTOL` is in $L_\odot$, while the secant step below works in $\log L$ (settled from the code, Nov 9, 2026: [[#L128]], [[#L168]]).
4. Otherwise, at the first pass (`NK = 2`) lower $X$ by 0.01 ("Y=Y+0.01"); afterwards take a secant step in $X$ against $\log L$:
$$X_\mathrm{new} = X + \frac{X - X_\mathrm{prev}}{\log L_R - \log L_{R,\mathrm{prev}}}\,\left(\log L_* - \log L_R\right).$$

**Changed since `rp_1`.** `/CALSTAR/` retired: `ALRI`, `LSTAR`, `LPASSR` are now arguments (owned by the main program), `BLI`, `AGEI`, `BLR`, `AGER`, `BLRP` saved locals, the targets in `NMLPAR_MOD`; COMMON blocks to modules, `IMPLICIT NONE`.

## Bugs, by priority

1. **(a)** **A false crossing at the start of a run that begins above $R_*$.** ([[#L97-L103]]; [[setscal.f#L107]]; [[main.f#L1119-L1123]]) `ALRI` starts at 0 ([[setscal.f#L107]]) and is not updated at a crossing ([[#L118-L178]] leave it as it was), and main.f's first call of each run is at its second model (the first only sets `TEFFI`). If that model's radius is above $R_*$ (a pre-main-sequence start with $R_*$ on the main sequence, say), the test `ALR.GT.SR.AND.ALRI.LE.SR` ([[#L98]]) holds at once: `LPASSR` ends the run at its second model, and $L$ and the age "at $R_*$" are interpolated between this model and `BLI`, `AGEI`, which are unset in the first run (saved locals with no `DATA`). Since `ALRI` stays 0, every later run stops the same way, and the secant step works on these values. When the track starts below $R_*$, the first comparison of each later run is made against the previous run's last stored model rather than the run's own, which is harmless as long as every run starts on the same side of $R_*$. Only with `LCALST` (off by default, [[nmlpar_mod.f#L160]]) and a track that starts above $R_*$; a track that starts below $R_*$ and expands through it is not affected. Read from the code, not run. **A possible fix** (in main.f, then here):

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to mark the first model of each run, so that CHKSCAL
    C starts its search from the run's own models.
                 IF(MODELN.EQ.1) THEN
                    TEFFI = 10.0D0**TEFFL
                    ALRI = -1.0D0
                 ELSE
    ...
    ```

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to store the first model of a run without testing it.
          ALR = SQRT((10.0D0**BL)*CLSUN/(C4PI*CSIG))/(TEFF*TEFF*CRSUN)
          IF(ALRI.LT.0.0D0) THEN
             BLI = BL
             AGEI = DAGE
             ALRI = ALR
             RETURN
          ENDIF
    ...
    ```

### CHKSCAL

Calibrates $X$ (thus $Y$) so that a track passes through a target $(R_*, L_*)$: detects the crossing of $R_*$, interpolates $L$ and the age there, and sets $X$ by a secant step, or sets the final run's stopping age.
