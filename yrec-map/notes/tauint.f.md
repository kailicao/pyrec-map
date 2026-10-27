## Explanation

**Purpose.** `TAUINT` computes the convective overturn time scale $\tau_\mathrm{cz}$ (`TAUCZ`) at the base of the surface convection zone, on the whole star's profile, interior and envelope joined (JVS 02/12, "snagged from MIDMOD"). It is the older method; [[tauintnew.f|tauintnew.f]] is the newer one (G. Somers 3/17).

**How it fits.**
- **Inputs:** the profile built by [[gettau.f#GETTAU|GETTAU]]: the interior shells only, since GETTAU stitches the envelope onto the profile only when `LCALCENV` and `LNEWTCZ` are both set, and calls TAUINT only when `LNEWTCZ` is false. `HS1` (mass), `LCZ`, `HR`, `HP`, `HD`, `HG`, `SVEL`, and `DEL1`, `DEL2`, which GETTAU takes from `SDEL(1,·)` and `SDEL(3,·)`, the radiative and adiabatic gradients; and, through `ENVSTRUCT_MOD`, the envelope from the last [[envint.f#ENVINT|ENVINT]] call.
- **Who calls it:** only [[gettau.f#GETTAU|GETTAU]], when `LNEWTCZ` is false and `TAUCZ` is still 0 after its ENVINT call (which sets it through TAUCAL when the top of the interior model is radiative).
- **Output:** `TAUCZ` in `OVRTRN_MOD`.
- **Modules:** `OVRTRN_MOD`, `ENVSTRUCT_MOD`, `NMLPAR_MOD` (`LROT`) and `CONSTANTS_MOD`.

**The method.** If the top shell or the one below it is convective, the zone's base `IMAX` is the lowest shell of the convective run from the surface.
- **Partly convective star:** as in [[taucal.f|taucal.f]], step 2 and 4: the base $r_b$ where $\nabla_1 - \nabla_2$ changes sign, $H_P = P/(\rho g)$ there, and
  $$\tau_\mathrm{cz} = \frac{H_P}{v(r_b + H_P)} ,$$
  with $v$ interpolated linearly in $\log r$. If $r_b + H_P$ lies beyond the profile, the envelope in `ENVSTRUCT_MOD` is searched for the first convective point above it ("stitch on the envelope for more room"; the profile holds the interior only, so TAUINT searches the envelope itself), and $v$ is interpolated between the last shell and that point.
- **Fully convective star:** the point where $H_P = r$, by linear interpolation of $H_P - r$; then $\tau_\mathrm{cz} = H_P/v$ there. If already $H_P \le r$ at the first shell, it takes $H_P \approx \sqrt{H_{P,1}\,r_1}$ and $v_1$ (the comment: "assume v constant inside and $H_P = k/r$" near the centre).
- **No surface zone:** $\tau_\mathrm{cz} = 0$.

**KC's changes.** The unused arguments `HCOMP`, `HS2` and `HSTOT` were removed (2025-05-31); the elements of COMMON `ENVSTRUCT` were reordered (2025-05-30).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/OVRTRN/` to `OVRTRN_MOD`, `/ENVSTRUCT/` to `ENVSTRUCT_MOD`, `/ROT/` to `NMLPAR_MOD`, the constants to `CONSTANTS_MOD`; the unused `/COMP/`, `/DEUTER/` and `/JTEST/` dropped, which settles the former question 3), the array size `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Questions for the experts

1. **The envelope interpolation.** Beyond the profile, $v$ is interpolated between the last shell `M` and envelope point `K`, with `FX = (RTESTL-HR(M))/(ENVR(K)-HR(M))`, skipping envelope points `2..K-1`, so a velocity profile with structure between the fitting point and point `K` is replaced by a straight line. Should the interpolation use the two envelope points that bracket $r_b + H_P$?
2. **The `LCZSUR` test.** `(HSTOP-HSBOT)/CMSUN .GT. 0` is true for any zone; is a minimum depth intended (the comment: "deep enough for angular momentum loss")?

### TAUINT

The older overturn time: $H_P/v$ one pressure scale height above the base of the surface convection zone, or at $H_P = r$ for a fully convective star.
