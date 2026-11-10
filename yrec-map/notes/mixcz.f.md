## Explanation

**Purpose.** Homogenizes the composition of every convection zone (mass-weighted mean over the zone), then applies light clean-ups to the composition.

**How it fits.**
- **Inputs:** `HCOMP`, the shell masses `HS2`, the convection flags `LCZ` and `M`; `ZENVM` from `COMP_MOD`; `LEXCOM` from `NMLPAR_MOD`.
- **Who calls it:** the main program in [[main.f|main.f]], [[getw.f#GETW|GETW]] (twice) and [[seculr.f#SECULR|SECULR]]. From the main program, after the model has converged ("ENSURE CONVECTION ZONES ARE FULLY MIXED"), it mixes the formal convection zones (`LC`, without overshoot); from GETW and SECULR, the zones with overshoot built by [[ovrot.f#OVROT|OVROT]] (`LCZM`, `LCZ`).

    > **Question** ([[main.f#L977]]). **Mixing again after convergence, without overshoot.** In the corrector iterations [[mix.f#MIX|MIX]] (from [[crrect.f#CRRECT|CRRECT]]) has already homogenized the zones with overshoot, yet the main program calls `MIXCZ` once more after convergence, with the formal flags `LC`. Is the final mix needed because the zones moved during the iteration, and is it intended that overshoot regions are not re-mixed here?

- **Output:** `HCOMP` in place. It also writes `LCZ(M+1) = .FALSE.` as a sentinel.
- **Modules:** `COMP_MOD` (`ZENVM`), `NMLPAR_MOD` (`LEXCOM`) and `DIMENSIONS_MOD` (`JSON`). A convective turnover time calculation is commented out ("it is now passed in in the OVRTRN common block," G. Somers 3/17); the COMMON blocks `rp_1` declared for it (`/DEUTER/`, `/SCRTCH/`, `/CONST1/`, `/CONST2/`, `/ROT/`, `/MDPHY/`, `/OVRTRN/`) are no longer declared.

**The method.**
1. **Zones.** Runs of convective shells give up to 12 zones (`MXZONE`, pairs of first and last shell). Zones beyond the twelfth are not mixed, without a message (the scan stops once `J` passes 24, [[#L80-L82]]), where [[convec.f#CONVEC|CONVEC]] prints "TOO MANY MIX ZONES."
2. **Mixing.** In each zone (one shell is enough at the centre), every species $k$ (11, or 15 with `LEXCOM`) becomes
$$\bar X_k = \frac{\sum_j X_{k,j}\,\Delta m_j}{\sum_j \Delta m_j}.$$
3. **Clean-up,** at every shell: $X \ge 0$; $Z \le 1 - X$; and ¹⁶O (row 9) at least $0.99\times10^{-3}\,(Z - Z_\mathrm{env,m})$, where $Z_\mathrm{env,m}$ = `ZENVM` is the envelope's metal fraction other than the CNO elements (set by [[starin.f#STARIN|STARIN]]: "Z OTHER THAN CNO CYCLE ELEMENTS," `ZENV` times the mixture's non-CNO share), so $Z - Z_\mathrm{env,m}$ is the CNO part of $Z$ and the floor keeps ¹⁶O at least about 0.1% of the CNO mass.

    $Y$ is not recomputed after the clamps ([[#b2]]).

    > **Question** ([[#L121]]). **The oxygen floor.** `HCOMP(9,I) = MAX(HCOMP(9,I), 0.99D-3*(HCOMP(3,I)-ZENVM))`: What is this floor for, and where does $0.99\times10^{-3}$ come from? (Probably a guard for helium-burning regions, where $Z$ exceeds the envelope's; this is a guess.)

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (those of the commented-out turnover time dropped), `IMPLICIT NONE`.

> **Question.** **The mass fractions' sum.** In `testsuite/Test_m1p4feh+0p0GS98_dif_TAMS`, $X + Y + Z + {}^3$He differed from 1 by up to $1.2\times10^{-3}$, while this routine's clamps (bug 2) never acted, so the clean-up here was not the cause. Where does the sum drift, and should the composition be renormalized somewhere? Seen while checking bug 2 by running YREC (Nov 10, 2026); its cause was not looked for.

## Bugs, by priority

1. **(never occurred)** **The sentinel `LCZ(M+1)` is written past the model.** ([[#L65-L67]]) `LCZ(M+1) = .FALSE.` writes into the caller's array one element past the model, and the scan reads it; the arrays are declared `LCZ(JSON)`, so this is out of bounds when `M = JSON`, which [[hpoint.f#HPOINT|HPOINT]]'s check (`MNEW+NPT.GT.JSON`, [[hpoint.f#L401]]) allows. CONVEC does the same with `LC(M+1)` ([[convec.f#L87]]). Correct for every model with fewer than `JSON` = 5000 shells.

    **A possible fix:** scan `I = 1,M` and, after the loop, close a zone still open at the surface (`IF(LCC)`, with `MXZONE(J+1) = M`), so that nothing past `M` is written or read.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The sentinel was written on every call in the 33 of 34 runs (26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones) that got past their start, at models of 349 to 3,455 shells, never at `JSON` = 5,000, so it never fell outside the array; a line at CONVEC's same sentinel ([[convec.f#L87]]) never found it outside either. It needs a model of 5,000 shells, which HPOINT allows but no case comes near.

2. **(never occurred)** **Helium is not recomputed after the clean-up.** ([[#L117-L122]]; [[mix.f#L473-L474]]) Loop 140 floors $X$ at 0 and caps $Z$ at $1 - X$ but leaves $Y$ as it was, whereas [[mix.f#MIX|MIX]]'s clean-up then sets $Y = 1 - X - Z - X_{^3\mathrm{He}}$ ([[mix.f#L473-L474]]; its cap on $Z$ also subtracts ³He). When a clamp acts, $X + Y + Z + X_{^3\mathrm{He}}$ then differs from 1. After a mass-weighted mean of fractions in range, a clamp can act only on a composition that was already out of range.

    **A possible fix:**

    ```diff
    --- a/src/mixcz.f
    +++ b/src/mixcz.f
    @@ -118,6 +118,9 @@
           DO 140 I = 1,M
              HCOMP(1,I) = DMAX1(HCOMP(1,I),0.0D0)
              HCOMP(3,I) = DMIN1(HCOMP(3,I),1.0D0-HCOMP(1,I))
    +C 11/10/26 KC via Claude
    +C code changed to recompute Y after the clamps, as MIX does.
    +         HCOMP(2,I) = 1.0D0-HCOMP(1,I)-HCOMP(3,I)-HCOMP(4,I)
              HCOMP(9,I) = DMAX1(HCOMP(9,I),0.99D-3*(HCOMP(3,I)-ZENVM))
       140 CONTINUE

    ```

    **Checked by running YREC** (Nov 10, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): MIXCZ was called 12,145 times in the five cases run (728 in `testsuite/Test_m1p0feh+0p0GS98_base_TAMS`, 266 in `testsuite/Test_m0p3feh+0p0GS98_base_ZAMS`, 820 in `testsuite/Test_m1p4feh+0p0GS98_dif_TAMS`, 9,000 in `testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`, and 1,331 in `examples/run_standard_solar_model/Test_solarcal_noGS_norot`), and neither clamp ever acted: No shell had $X < 0$ or $Z > 1 - X$. The sum $X + Y + Z + X_{^3\mathrm{He}}$ did differ from 1 by more than $10^{-12}$ at many shells, by up to $1.6\times10^{-5}$ in the 1 $M_\odot$ case and $1.2\times10^{-3}$ in the 1.4 $M_\odot$ case with diffusion, but not because of the clamps. The fix, which resets $Y$ at every shell and so removes those departures too, changes the results by about the size of the null change, not clearly beyond it: In the 1 $M_\odot$ case $\log L$ moves by up to 0.00006 dex and central $X$ by 0.000006, against 0.0004 and 0.00019 for a null change (nearly every opacity, all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$, times $1 + 10^{-10}$) on the same case, with 728 models in both; in the 1.4 $M_\odot$ case $\log L$ moves by up to 0.071 dex and central $X$ by 0.0040, against 0.057 and 0.0021 (1.2 and 1.9 times as much, from removing the sum's drift, the question above, since no clamp acted), with 820 models in both. What would reach it: a composition already out of range when MIXCZ is called. Intent: none found.
