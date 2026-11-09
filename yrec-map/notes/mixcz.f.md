## Explanation

**Purpose.** Homogenizes the composition of every convection zone (mass-weighted mean over the zone), then applies light clean-ups to the composition.

**How it fits.**
- **Inputs:** `HCOMP`, the shell masses `HS2`, the convection flags `LCZ` and `M`; `ZENVM` from `COMP_MOD`; `LEXCOM` from `NMLPAR_MOD`.
- **Who calls it:** the main program in [[main.f|main.f]], [[getw.f#GETW|GETW]] (twice) and [[seculr.f#SECULR|SECULR]]. From the main program, after the model has converged ("ENSURE CONVECTION ZONES ARE FULLY MIXED"), it mixes the formal convection zones (`LC`, without overshoot); from GETW and SECULR, the zones with overshoot built by [[ovrot.f#OVROT|OVROT]] (`LCZM`, `LCZ`).

    > **Question** ([[main.f#L977]]). **Mixing again after convergence, without overshoot.** In the corrector iterations [[mix.f#MIX|MIX]] (from [[crrect.f#CRRECT|CRRECT]]) has already homogenized the zones with overshoot, yet the main program calls `MIXCZ` once more after convergence, with the formal flags `LC`. Is the final mix needed because the zones moved during the iteration, and is it intended that overshoot regions are not re-mixed here?

- **Output:** `HCOMP` in place. It also writes `LCZ(M+1) = .FALSE.` as a sentinel.
- **Modules:** `COMP_MOD` (`ZENVM`), `NMLPAR_MOD` (`LEXCOM`) and `DIMENSIONS_MOD` (`JSON`). A convective turnover time calculation is commented out ("it is now passed in in the OVRTRN common block", G. Somers 3/17); the COMMON blocks `rp_1` declared for it (`/DEUTER/`, `/SCRTCH/`, `/CONST1/`, `/CONST2/`, `/ROT/`, `/MDPHY/`, `/OVRTRN/`) are no longer declared.

**The method.**
1. **Zones.** Runs of convective shells give up to 12 zones (`MXZONE`, pairs of first and last shell). Zones beyond the twelfth are not mixed, without a message (the scan stops once `J` passes 24, [[#L80-L82]]), where [[convec.f#CONVEC|CONVEC]] prints "TOO MANY MIX ZONES".
2. **Mixing.** In each zone (one shell is enough at the centre), every species $k$ (11, or 15 with `LEXCOM`) becomes
$$\bar X_k = \frac{\sum_j X_{k,j}\,\Delta m_j}{\sum_j \Delta m_j}.$$
3. **Clean-up,** at every shell: $X \ge 0$; $Z \le 1 - X$; and ¹⁶O (row 9) at least $0.99\times10^{-3}\,(Z - Z_\mathrm{env,m})$, where $Z_\mathrm{env,m}$ = `ZENVM` is the envelope's metal fraction other than the CNO elements (set by [[starin.f#STARIN|STARIN]]: "Z OTHER THAN CNO CYCLE ELEMENTS", `ZENV` times the mixture's non-CNO share), so $Z - Z_\mathrm{env,m}$ is the CNO part of $Z$ and the floor keeps ¹⁶O at least about 0.1% of the CNO mass.

    > **Question** ([[#L117-L122]]). **Helium after the clean-up.** $X$ is floored and $Z$ capped, but $Y$ is not recomputed (as [[mix.f#MIX|MIX]] does, [[mix.f#L473-L474]]), so $X+Y+Z+X_{^3\mathrm{He}}$ may differ from 1 afterwards. Is this restored elsewhere?

    > **Question** ([[#L121]]). **The oxygen floor.** `HCOMP(9,I) = MAX(HCOMP(9,I), 0.99D-3*(HCOMP(3,I)-ZENVM))`: What is this floor for, and where does $0.99\times10^{-3}$ come from? (Probably a guard for helium-burning regions, where $Z$ exceeds the envelope's; this is a guess.)

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (those of the commented-out turnover time dropped), `IMPLICIT NONE`.

## Bugs, by priority

1. **(d)** **The sentinel `LCZ(M+1)` is written past the model.** ([[#L65-L67]]) `LCZ(M+1) = .FALSE.` writes into the caller's array one element past the model, and the scan reads it; the arrays are declared `LCZ(JSON)`, so this is out of bounds when `M = JSON`, which [[hpoint.f#HPOINT|HPOINT]]'s check (`MNEW+NPT.GT.JSON`, [[hpoint.f#L401]]) allows. CONVEC does the same with `LC(M+1)` ([[convec.f#L87]]). Correct for every model with fewer than `JSON` = 5000 shells. Read from the code, not run. **A possible fix:** scan `I = 1,M` and, after the loop, close a zone still open at the surface (`IF(LCC)`, with `MXZONE(J+1) = M`), so that nothing past `M` is written or read.
