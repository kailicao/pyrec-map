## Explanation

**Purpose.** `TAUCAL` computes the convective overturn time scale $\tau_\mathrm{cz}$ (`TAUCZ`) near the base of the surface convection zone, for a convection zone that lies within the envelope (JVS 02/12). Its comments say the code was taken from `MIDMOD`, and that the routine is called only from `ENVINT`.

**How it fits.**
- **Inputs:** the envelope's profile, passed by [[envint.f#ENVINT|ENVINT]] as arguments: the shell masses `HS2`, unlogged masses `HS1`, convective flags `LCZ`, $\log r$ (`HR`), $\log P$ (`HP`), $\log\rho$ (`HD`), gravity `HG`, the convective velocity `SVEL`, and two temperature gradients `DEL1`, `DEL2` (`EDEL1` and `EDEL2` in `ENVINT`, copied from `EDELS(1,·)` and `EDELS(2,·)`, which [[stitch.f#STITCH|STITCH]]'s column list names the radiative and the actual gradient; their difference changes sign at the zone's edge).
- **Who calls it:** only [[envint.f#ENVINT|ENVINT]].
- **Output:** `TAUCZ` in `OVRTRN_MOD`, shared with [[gettau.f#GETTAU|GETTAU]], [[envint.f#ENVINT|ENVINT]], [[massloss.f#MASSLOSS|MASSLOSS]], [[getw.f#GETW|GETW]] and others (the wind and mass-loss routines, by their names).
- **Modules:** `OVRTRN_MOD`, `NMLPAR_MOD` (`LROT`) and `CONSTANTS_MOD`.

**The method.**
1. Going down from the surface, find the first convective shell, then the base of that zone, `IMAX`; note whether a second, deeper convective zone exists (`LTWOCZ`, its top `ICZTOP`); with two zones, `IMAX` ends at the base of the deeper one. For a single zone `ICZTOP` is not set (bug 1). The routine also sets `HSTOP`, `HSBOT` and `LCZSUR`, which nothing reads since the test on `LCZSUR` was commented out (JVS 10/11/13; unused?, [[#L106-L128]]); the test `(HSTOP-HSBOT)/CMSUN .GT. 0` would be true for any zone.
2. Locate the base $r_b$ where $\nabla_1 - \nabla_2$ changes sign, by linear interpolation between shells `IMAX-1` and `IMAX` (factor $f$), and the pressure scale height there,
   $$H_p = \frac{P}{\rho\,g},\qquad g = \frac{G m}{r^2}\ \text{(computed here only without rotation)},$$
   interpolated with the same $f$.
3. If the zone is thin, that is, with $r_\mathrm{top}$ the radius of shell `ICZTOP`,
   $$\left|1 - \frac{r_b + H_p - r_\mathrm{IMAX}}{r_\mathrm{top} - r_\mathrm{IMAX}}\right| < 0.5,$$
   so that the point $r_b + H_p$ lies between the zone's middle and half a width above its top, or there are two zones, the mass-weighted mean velocity over shells `IMAX` to `ICZTOP` is used:
   $$\bar v = \frac{\sum_j \Delta m_j\,\tfrac12 (v_j + v_{j+1})}{\sum_j \Delta m_j},\qquad \tau_\mathrm{cz} = \frac{|r_\mathrm{top} - r_\mathrm{IMAX}|}{\bar v}.$$

    > **Question** ([[#L148-L153]]). **`.AND.` became `.OR.`** The commented-out test required a thin zone *and* two zones; the active one takes either. Which is intended?

    > **Question** ([[#L159]]; [[#L139-L140]]). **Two widths.** In the averaging branch, the width is $r_\mathrm{top} - r_\mathrm{IMAX}$, from the shells, rather than from the interpolated base $r_b$ (`ENVR`). Is the shell's radius meant, or should the width start at $r_b$?

4. Otherwise (the original method), the velocity at one pressure scale height above the base, $v(r_b + H_p)$, by linear interpolation in $\log r$, gives
   $$\tau_\mathrm{cz} = \frac{H_p}{v(r_b + H_p)} .$$
5. ENVINT calls TAUCAL only with the old method (`LNEWTCZ` false; the default is true) and only when the envelope's deepest point is radiative and a point above it convective (`JENV` > 1, [[envint.f#L937-L971]]). So `LCZ(1)` is false: when a convective point lies below `M`, the loop leaves the zone and sets `IMAX` ≥ 2; when only the surface point `M` is convective (the loop starts at `M-1`), `LCZEX` stays false and `IMAX = M`. `IMAX` is thus always set in the call, `LALLCZ` is never set, and the branch `TAUCZ = 0` is not reached (settled from the code, Nov 9, 2026: [[#L87-L101]], [[#L122]], [[#L223-L224]]).

    > **Question** ([[#L120-L124]]; [[#L129-L144]]). **Only the surface point convective.** When only point `M` is convective, `IMAX = M`, and $\tau_\mathrm{cz}$ is computed from shells `M-1` and `M` as if a zone ended there: The search for $r_b + H_p$ then finds no shell (the loop from `IMAX+1` to `M` is empty), and `CVEL = SVEL(M)`. Should `TAUCZ` be 0 in that case?

**Design.** The routine prints "TauCal" to the screen at every call. A large commented-out block handled fully convective cases.

> **Question** ([[#L226]]). **A debugging print.** `print*, 'TauCal'` writes to the screen at every call. Is it left from debugging, and can it go?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/OVRTRN/` to `OVRTRN_MOD`, `/ROT/` to `NMLPAR_MOD`, the constants to `CONSTANTS_MOD`; the unused `/COMP/` and `/DEUTER/` dropped), the array size `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Bugs, by priority

1. **(a)** **`ICZTOP` is not set for a single zone.** ([[#L87-L98]]; [[#L152-L153]]; [[#L159-L163]]) `ICZTOP`, the top of the deeper zone, is set only when the loop finds two zones ([[#L94]]). But the test that chooses the averaging method evaluates `HR(ICZTOP)` for every zone ([[#L152-L153]]), and the averaging itself, which the first condition can select for a single zone, sums over shells `IMAX` to `ICZTOP` and takes the width from `HR(ICZTOP)`. For a single zone, `ICZTOP` keeps the value `SAVE`d from an earlier call with two zones, and is undefined if there was none (an index of 0 would read outside `HR`). What follows: The choice of method and, if averaging is chosen, `TAUCZ` depend on an earlier model's zone. Only with the old method (`LNEWTCZ` false; the default is true), when the envelope holds the zone's base. Read from the code, not run. **A possible fix:** take the top of a single zone as `ICZTOP`:

    ```fortran
                ELSE IF( LCZ(I) .AND. .NOT. LCZEX) THEN !First convective point from surface
                      LCZEX = .TRUE.
    C 11/09/26 KC via Claude
    C code changed to set ICZTOP for a single zone too: the thin-zone test
    C and the average below use it.  A second zone overwrites it.
                      ICZTOP = I
                ENDIF
    ```

### TAUCAL

The convective overturn time near the base of a surface convection zone within the envelope, $H_p/v$ one scale height above the base, or a zone's width over its mean velocity for thin or double zones.
