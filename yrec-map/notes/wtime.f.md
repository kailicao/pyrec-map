## Explanation

**Purpose.** `WTIME` limits the time step of a rotating model by the change of the angular velocity since the previous model: if $\Omega$ changed by more than the user's fraction `DTWIND` somewhere (the comment gives a default of 0.08; `NMLPAR_MOD` initializes it to 10), the step shrinks; if less, it grows. Which value a run uses: `DTWIND` is a namelist variable of [[parmin.f#PARMIN|PARMIN]], initialized to 10; [[remap.f#REMAP|REMAP]] replaces it with `TIME_DW_GLOBAL` (initialized to 0.08 in `NMLBYPASS_MOD`) only when `LNEWVARS` is set, and `LNEWVARS` is `.FALSE.` by default. A run that sets neither thus has `DTWIND` = 10, a tenfold change of $\Omega$ in one step, so that rotation almost never limits the step; with `LNEWVARS` it is 0.08, and it often does.

**How it fits.**
- **Inputs:** the previous step `DELTS`, `M`, the current `OMEGA`; through modules, the previous model's rates `WOLD` (`OLDROT_MOD`, saved by [[starin.f#STARIN|STARIN]] and the rotation routines), `DTWIND` (`NMLPAR_MOD`, read from the namelist by [[parmin.f#PARMIN|PARMIN]]; [[remap.f#REMAP|REMAP]] may reset it) and the step-change limit `ATIME(13)` (`NMLPAR_MOD`).
- **Who calls it:** only [[htimer.f#HTIMER|HTIMER]], which takes the smallest of its candidate steps.
- **Outputs:** `DELTSW`, the rotation-based step, and `DWMAX`, the largest relative change.

**The method.** The largest relative change over all shells,
$$\delta_\mathrm{max} = \max_i \frac{2\,|\Omega_i - \Omega_i^\mathrm{old}|}{\Omega_i + \Omega_i^\mathrm{old}},$$
gives $f = \delta_\mathrm{max}/$`DTWIND`, limited to $1/a \le f \le a$ with $a$ = `ATIME(13)` (MHP 10/14), and $\Delta t_\Omega = \Delta t/f$. If nothing changed ($f = 0$), $\Delta t_\Omega = 10^{20}$, so that rotation does not limit the step. The shell of the largest change is found (`IWMAX`) but not returned or read (unused?). The comment before the limiter, "restrict change in timestep to no more than a factor of ATIME(14)%," describes the commented-out line below it; REMAP now sets `ATIME(14)` from `TIME_DY_TOTAL`, a helium-burning limit of [[ytime.f#YTIME|YTIME]], and the code uses `ATIME(13)` (settled from the code, Nov 9, 2026: [[#L71-L77]]; [[remap.f#L276-L277]]).

**Changed since `rp_1`.** Declarations only: `COMMON/OLDROT/` to `OLDROT_MOD`, `/CT2/` and `/CTLIM/` to `NMLPAR_MOD` (where `DTWIND` now has the initial value 10), `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Bugs, by priority

1. **(never occurred)** **0/0 where $\Omega$ is zero.** ([[#L53-L62]]) The relative change $2|\Omega_i - \Omega_i^\mathrm{old}|/(\Omega_i + \Omega_i^\mathrm{old})$ is 0/0 in a shell where both are zero. In the first shell it makes `DWMAX` a NaN, and since every comparison with a NaN is false, `DWMAX` stays NaN, and so do `FAC` and `DELTSW` ([[#L63-L78]]); HTIMER's test `DELTSW.LT.1.0D0` does not catch it ([[htimer.f#L131]]), and `DWMAX` goes on to the rotational-mixing routines, which set their number of substeps from it. In any other shell the NaN is skipped. This needs `LROT` (off by default) and a model with $\Omega = 0$ at the center in two successive models, such as a rotating run started without rotation; with a floating-point trap on invalid operations, the run stops there.

    **A possible fix:**

    ```diff
    --- a/src/wtime.f
    +++ b/src/wtime.f
    @@ -50,10 +50,13 @@
     C   DWMAX : MAXIMUM FRACTIONAL CHANGE IN OMEGA.
     C
     
    -      II = 1
    -      DWMAX = 2.0D0*ABS(OMEGA(II)-WOLD(II))/(OMEGA(II)+WOLD(II))
    -      IWMAX = II
    -      DO 50 I = II+1,M
    +C 11/09/26 KC via Claude
    +C code changed to skip shells where OMEGA and WOLD are both zero, so
    +C that DWMAX is never 0/0.
    +      DWMAX = 0.0D0
    +      IWMAX = 1
    +      DO 50 I = 1,M
    +         IF(OMEGA(I)+WOLD(I).LE.0.0D0) GOTO 50
              TESTW=2.0D0*ABS(OMEGA(I)-WOLD(I))/(OMEGA(I)+WOLD(I))
              IF(TESTW.GT.DWMAX) THEN
                 DWMAX = TESTW
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): taken at every model in the five rotating runs of 34 runs (26 of YREC's cases, from 0.04 to 9 $M_\odot$, with rotation, settling, and helium burning, and 8 made-up ones), 547 to 1,854 times per run (`testsuite/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2`, `testsuite/Test_solarGS98_difrotmixper18p4d1p0`, `testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`, and `testsuite/Test_m2p0_feh+0p0_vzams150_IES1_TAMS` and `_IES2_TAMS`); $\Omega$ at the centre was $1.08\times10^{-7}$ to $4.9\times10^{-4}$ and never zero. Not reached: It needs a rotating run with no rotation at the centre, and every rotating case starts with `WNEW` > 0. The fix was not run. Intent: none found.

### WTIME

Rotation-based time step: $\Delta t/f$ with $f$ the largest relative change of $\Omega$ over `DTWIND`, limited by `ATIME(13)`.
