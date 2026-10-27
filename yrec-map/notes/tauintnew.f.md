## Explanation

**Purpose.** `TAUINTNEW` computes the convective overturn time scale $\tau_\mathrm{cz}$ (`TAUCZ`) and the radius of the base of the convection zone (`RBCZ`), by the method G. Somers introduced in 3/17. Its comment: search from the centre up for the base of the surface convection zone, and from the surface down; if both agree the zone is unique and the "old top-down sinkline method" is used; if not, several convective cells exist, and the crossing time of the lowest cell in the envelope is taken.

**How it fits.**
- **Inputs:** the full profile from [[gettau.f#GETTAU|GETTAU]] (interior and envelope; `M` points, of which `MINT` are interior shells): `HS1`, `LCZ`, `HR`, `HP`, `HD`, `HG`, `SVEL`, and `DEL1`, `DEL2`: for interior shells GETTAU passes `SDEL(1,·)` and `SDEL(3,·)`, the radiative and adiabatic gradients, but for the stitched envelope points `EDELS(1,·)` and `EDELS(2,·)`, the radiative and actual gradients.
- **Who calls it:** only [[gettau.f#GETTAU|GETTAU]], when `LNEWTCZ` is set; otherwise `GETTAU` calls [[tauint.f#TAUINT|TAUINT]].
- **What it calls:** [[kspline.f#KSPLINE|KSPLINE]] and [[ksplint.f#KSPLINT|KSPLINT]], a natural cubic spline through four points.
- **Outputs:** `TAUCZ` in [[ovrtrn_mod.f|`OVRTRN_MOD`]] (read by the mass-loss and rotation routines, by their names), and the argument `RBCZ` in solar radii.
- **Modules:** [[ovrtrn_mod.f|`OVRTRN_MOD`]] (`TAUCZ`), [[constants_mod.f|`CONSTANTS_MOD`]] (`CLN`, `CMSUN`, `CRSUN`), `JSON` from [[dimensions_mod.f|`DIMENSIONS_MOD`]].

**The method.**
1. **Find the zone.** From shell `IBEG` (first 1) upward: pass the convective core, if any (its top `JCORE`), then the first convective shell above a radiative region is `IMAX`. From the surface downward, the base of the outermost zone is `JMAX`: the first point `J` below a convective point `J+1` that is radiative, plus one, so that radiative points at the surface are passed over (JvS 02/2026; if no such point exists, `JMAX` = 1). A star with no such zone is radiative ($\tau_\mathrm{cz} = 0$); one convective throughout is fully convective.
2. **Reject false zones** and search again from above: a zone less than one decade in pressure above the core, $\log P(\mathrm{JCORE}) - \log P(\mathrm{IMAX}) < 1$ (unless the profile is the interior only); a zone fewer than 3 shells thick; in the interior-only case with two zones (`IJMAX` ≠ 0, `M = MINT`), `IMAX` is set to `JMAX`; and, at the end, a result $\tau_\mathrm{cz} > 10^{20}$.
3. **The base:** $r_b$ where $\nabla_1 - \nabla_2$ changes sign, by linear interpolation in $\log r$ (for a fully convective star, $\log r_b = 1$, a very small radius in cm).
4. **One zone** (`IMAX = JMAX`): go up from the base to where $r - r_b = H_P$, with $H_P = P/(\rho g)$. Around that point, four shells give $\delta_k = (r_k - r_b) - H_{P,k}$, and natural cubic splines in $\delta$ evaluated at $\delta = 0$ give $v$ and $H_P$; then
   $$\tau_\mathrm{cz} = \frac{H_P}{v}\bigg|_{\,r - r_b = H_P} .$$
5. **Several cells, or $r_b + H_P$ outside the star:** the lowest zone's top $r_t$ (again where $\nabla_1 - \nabla_2$ changes sign), its width $\Delta r = r_t - r_b$, and $v$ at its middle, $r_b + \Delta r/2$, from a four-point spline in $r$:
   $$\tau_\mathrm{cz} = \frac{\Delta r}{v(r_b + \Delta r/2)} .$$

**KC's changes.** Removed the unused arguments `HCOMP`, `HS2` and `HSTOT`, and the `RECURSIVE` attribute (2025-05-31); added the check `IMAX .GT. 0 .AND. JCORE .GT. 0` before using `HP(JCORE)` "to avoid runtime error" (2025-05-30); moved an `ENDIF` "to avoid block mismatch" (2025-05-31); reordered the elements of COMMON `ENVSTRUCT` (2025-05-30).

**Changed since `rp_1`.** COMMON blocks to modules, `IMPLICIT NONE` (the unused blocks dropped); the downward search for the base of the outermost zone now requires a convective point above the radiative one (JvS 02/2026), so a radiative layer at the surface no longer makes `JMAX` = `M`. No question is settled: question 6 concerns the upward search.

## Questions for the experts

1. **`JCORE` may be stale.** `JCORE` is set only when the upward search leaves a convective region that started at `IBEG`. When the search starts in a radiative shell, `JCORE` keeps its value from an earlier pass or call (`SAVE`). KC's check avoids an index of 0, but not a stale index. Should `JCORE` be reset at label 50?
2. **Restarts without a limit.** The searches restart with `GOTO 50` (thin zones, zones near the core, $\tau_\mathrm{cz} > 10^{20}$). Nothing stops `IBEG` from passing `M`, after which `LCZ(IBEG)` is read beyond the profile; and the 3-shell test reads `LCZ(IMAX+2)`, which can be beyond `M`. Can the loop fail to end?
3. **Indices near the top.** The four-point splines use shells up to `KK+1`; with `KK = K+1` and `K` near `M-1`, this can reach `M+1`.
4. **A fully convective star's $r_b$.** `RBCZ = 1.` is then `EXP(CLN*1)`, that is 10 cm, not 1 cm; harmless, but the comment and code disagree.
5. **Unused values.** `ENVRCL` (a radius from a spline) and `HSTOP`, `HSBOT`, `LCZSUR` (always true for a zone) are computed but not used for the result.
6. **A fully convective star loops forever.** The code reaches "fully convective" only when every point from `IBEG` to `M` is convective, and then sets `IMAX = 1`, `JCORE = 1`. When the envelope is stitched (`M` ≠ `MINT`), the near-core test `HP(1) - HP(1) < 1` always holds, so `IBEG = 2` and the search restarts, ending in the same state: an endless loop. And if the outermost points are radiative, the whole convective interior is taken as a convective core, and $\tau_\mathrm{cz} = 0$. How should a fully convective star be handled?
7. **Two kinds of gradient.** `DEL2` is the adiabatic gradient for interior shells but the actual gradient for the stitched envelope points, so the sign change of $\nabla_1 - \nabla_2$ means different things on the two sides of the fitting point. Intended?

### TAUINTNEW

The newer overturn time (G. Somers 3/17): finds the base of the main surface convection zone from both directions, then $H_P/v$ one pressure scale height above the base (by four-point splines), or the lowest cell's width over its central velocity; also returns the base's radius in solar units.
