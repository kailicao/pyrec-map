## Explanation

**Purpose.** `TAUCAL` computes the convective overturn time scale $\tau_\mathrm{cz}$ (`TAUCZ`) near the base of the surface convection zone, for a convection zone that lies within the envelope (JVS 02/12). Its comments say the code was taken from `MIDMOD`, and that the routine is called only from `ENVINT`.

**How it fits.**
- **Inputs:** the envelope's profile, passed by [[envint.f#ENVINT|ENVINT]] as arguments: the shell masses `HS2`, unlogged masses `HS1`, convective flags `LCZ`, $\log r$ (`HR`), $\log P$ (`HP`), $\log\rho$ (`HD`), gravity `HG`, the convective velocity `SVEL`, and two temperature gradients `DEL1`, `DEL2` (`EDEL1` and `EDEL2` in `ENVINT`, copied from `EDELS(1,·)` and `EDELS(2,·)`, which [[stitch.f#STITCH|STITCH]]'s column list names the radiative and the actual gradient; their difference changes sign at the zone's edge).
- **Who calls it:** only [[envint.f#ENVINT|ENVINT]].
- **Output:** `TAUCZ` in `OVRTRN_MOD`, shared with [[gettau.f#GETTAU|GETTAU]], [[envint.f#ENVINT|ENVINT]], [[massloss.f#MASSLOSS|MASSLOSS]], [[getw.f#GETW|GETW]] and others (the wind and mass-loss routines, by their names).
- **Modules:** `OVRTRN_MOD`, `NMLPAR_MOD` (`LROT`) and `CONSTANTS_MOD`.

**The method.**
1. Going down from the surface, find the first convective shell, then the base of that zone, `IMAX`; note whether a second, deeper convective zone exists (`LTWOCZ`, its top `ICZTOP`).
2. Locate the base $r_b$ where $\nabla_1 - \nabla_2$ changes sign, by linear interpolation between shells `IMAX-1` and `IMAX` (factor $f$), and the pressure scale height there,
   $$H_P = \frac{P}{\rho\,g},\qquad g = \frac{G m}{r^2}\ \text{(computed here only without rotation)},$$
   interpolated with the same $f$.
3. If the zone is thin, that is, with $r_\mathrm{top}$ the radius of shell `ICZTOP`,
   $$\left|1 - \frac{r_b + H_P - r_\mathrm{IMAX}}{r_\mathrm{top} - r_\mathrm{IMAX}}\right| < 0.5,$$
   so that the point $r_b + H_P$ lies between the zone's middle and half a width above its top, or there are two zones, the mass-weighted mean velocity over shells `IMAX` to `ICZTOP` is used:
   $$\bar v = \frac{\sum_j \Delta m_j\,\tfrac12 (v_j + v_{j+1})}{\sum_j \Delta m_j},\qquad \tau_\mathrm{cz} = \frac{|r_\mathrm{top} - r_\mathrm{IMAX}|}{\bar v}.$$
4. Otherwise (the original method), the velocity at one pressure scale height above the base, $v(r_b + H_P)$, by linear interpolation in $\log r$, gives
   $$\tau_\mathrm{cz} = \frac{H_P}{v(r_b + H_P)} .$$
5. With no convective zone the code sets `IMAX = M` and, unless `LALLCZ` is set, computes $\tau_\mathrm{cz}$ at the surface anyway (from shells `M-1` and `M`). $\tau_\mathrm{cz} = 0$ only when `LALLCZ` is set, by the test `IMAX .LT. 1`, which depends on a value of `IMAX` left from an earlier call (question 1).

**Design.** The routine prints "TauCal" to the screen at every call. A large commented-out block handled fully convective cases.

**KC's changes.** The unused arguments `HCOMP` and `MINT` were removed (2025-05-31).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/OVRTRN/` to `OVRTRN_MOD`, `/ROT/` to `NMLPAR_MOD`, the constants to `CONSTANTS_MOD`; the unused `/COMP/` and `/DEUTER/` dropped), the array size `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Questions for the experts

1. **`IMAX` and `ICZTOP` may be undefined.** `IMAX` is set only when the loop leaves a convective zone; otherwise it keeps the value `SAVE`d from an earlier call, and the test `IMAX .LT. 1` (for a zone reaching the bottom) relies on that. `ICZTOP` is set only when there are two zones, but the averaging branch also runs for one thin zone (the first condition), and then uses `ICZTOP` undefined.
2. **`.AND.` became `.OR.`** The commented-out test required a thin zone *and* two zones; the active one takes either. Which is intended?
3. **A debugging print.** `print*, 'TauCal'` writes to the screen at every call.
4. **Two widths.** In the averaging branch, the width is $r_\mathrm{top} - r_\mathrm{IMAX}$, from the shells, rather than from the interpolated base $r_b$.
5. **`LCZSUR`.** The test `(HSTOP-HSBOT)/CMSUN .GT. 0` is true for any zone, and `LCZSUR` is no longer used (its test was commented out, JVS 10/11/13).
6. **No convective zone, but a turnover time.** Without a convective zone (`LCZEX` false), `IMAX = M`, and unless `LALLCZ` happens to be set, $\tau_\mathrm{cz}$ is computed from the surface shells `M-1` and `M` as if a zone ended there. Should `TAUCZ` be 0 in that case?

### TAUCAL

The convective overturn time near the base of a surface convection zone within the envelope, $H_P/v$ one scale height above the base, or a zone's width over its mean velocity for thin or double zones.
