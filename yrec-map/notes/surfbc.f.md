## Explanation

**Purpose.** `SURFBC` provides the outer boundary condition of the interior solution, by the "envelope triangle." Envelopes are integrated at three points around the model's $(\log T_\mathrm{eff}, \log L)$; each gives $\log P$, $\log T$ and $\log r_\mathrm{f}$, the radius at the fitting point. A plane through the three points then gives $\log r_\mathrm{f}$, $\log L$ and $\log T_\mathrm{eff}$ as linear functions of $\log P$ and $\log T$ at the fitting point, which the Henyey solution uses as its outer boundary. It also switches between atmosphere tables and the gray atmosphere as $T_\mathrm{eff}$ changes.

**The fitting point.** It is the interior's outermost mass point, at $\log(m_\mathrm{f}/M)$ = `SENV` (`SENV = HS(M) - HSTOT`, set in [[crrect.f#CRRECT|CRRECT]], [[hpoint.f#HPOINT|HPOINT]] and [[starin.f#STARIN|STARIN]]; the documentation's standard is $-10^{-4}$, so about $2\times10^{-4}$ of the mass lies outside it). The layers above it are not on the Henyey grid but are integrated as a static envelope by [[envint.f#ENVINT|ENVINT]]: the YREC paper (§2.2) explains that they hold little mass, typically one part in $10^4$ or less, but pressure and density fall steeply there, so leaving them out of the interior model is much faster, and the structure equations are more stable with a deeper fitting point. The outermost point has four unknowns ($\log P$, $\log T$, $\log r$, $L$); the plane fixes two relations among them, which are the two outer equations of the Henyey system in [[crrect.f#CRRECT|CRRECT]] (`HSRF`):
$$\log r = c_1\log P + c_2\log T + c_3, \qquad \log L = c_4\log P + c_5\log T + c_6,$$
where $c_1, \dots, c_6$ are `CFENV(1:6)` and $P$, $T$, $r$, $L$ are the outermost point's; after the solution, CRRECT sets $\log T_\mathrm{eff}$ from the third plane, `CFENV(7:9)`.

**How it fits.**
- **Inputs:** arguments from [[crrect.f#CRRECT|CRRECT]]: the current $\log T_\mathrm{eff}$ (`TEFFL`), $\log L/L_\odot$ (`BL`), the triangle (`TRIT`, `TRIL`, `FTRI`) and its envelopes' results (`PS`, `TS`, `RS`) from earlier calls, the surface $X$, $Z$, the rotation factors `FPL`, `FTL`, the pressure limit `PLIM`, and the mixing length `CMIXL` (passed on to `ENVINT`). The triangle's size `TRIDT`, `TRIDL`, the atmosphere choice (`KTTAU`, `KTTAU0`, `LTTAU`) and the spot parameters (`SPOTF`, `SPOTX`) come from [[nmlpar_mod.f|`NMLPAR_MOD`]]; the Allard table's upper limit `AL_TEFFLmax` from [[alatm05_mod.f|`ALATM05_MOD`]], set by [[altabinit.f#ALTABINIT|ALTABINIT]].
- **Who calls it:** only [[crrect.f#CRRECT|CRRECT]].
- **What it calls:** [[envint.f#ENVINT|ENVINT]] for each envelope to be recomputed.
- **Outputs:** `CFENV(1:9)`, the plane's coefficients, which `CRRECT` uses for the boundary equations and to update $T_\mathrm{eff}$; the triangle and `PS`, `TS`, `RS`; `LFLP` (true if an envelope was recomputed); a table of the triangle on `ISHORT`.
- **Modules:** [[nmlpar_mod.f|`NMLPAR_MOD`]] (the atmosphere flags, shared with [[envint.f#ENVINT|ENVINT]], [[parmin.f#PARMIN|PARMIN]], [[setups.f#SETUPS|SETUPS]] and others; this routine changes `KTTAU` and `LTTAU`), [[comp_mod.f|`COMP_MOD`]] (the total mass `STOTAL`), [[alatm05_mod.f|`ALATM05_MOD`]], [[constants_mod.f|`CONSTANTS_MOD`]], [[iounits_mod.f|`IOUNITS_MOD`]] (`ISHORT`), `JSON` from [[dimensions_mod.f|`DIMENSIONS_MOD`]].

**The method.**
1. **Atmosphere switch** (MHP 9/01, 06/13). With Kurucz tables (`KTTAU = 3`) above $\log T_\mathrm{eff} = 3.95$, or Allard tables (`KTTAU = 4`) above the table's maximum, the code switches to the gray atmosphere (`KTTAU = 0`), remembers it (`LTTAU`), and starts a new triangle; it switches back when $T_\mathrm{eff}$ drops below the limit again, and starts a new triangle then too, since the old vertices were integrated with the gray $T(\tau)$.

    > **Question** ([[#L83-L108]]). **The Kurucz–Castelli tables.** The switch to the gray atmosphere covers `KTTAU = 3` (Kurucz) and `4` (Allard), but not `KTTAU = 5` (Kurucz–Castelli, used by [[envint.f#ENVINT|ENVINT]] through `KCSURFP`), whose lookup extrapolates above the table's last temperature without a message. Does that table need no limit?

    > **Question** ([[#L84]]; [[#L110]]). **Hard-coded limit.** The gray switch for Kurucz tables is at $\log T_\mathrm{eff} = 3.95$, written in the code; should it come from the table's range, as for the Allard tables?

2. **A new triangle** (`LNEW`). With `LRESET` (from [[crrect.f#CRRECT|CRRECT]]) all three envelopes are recomputed without starting a new triangle; with `LNEW` the triangle is new too, and its vertices, with $T = \log T_\mathrm{eff}$, $L = \log L$,
   $$(T - \tfrac12\Delta T,\ L - \tfrac12\Delta L),\quad (T + \tfrac12\Delta T,\ L - \tfrac12\Delta L),\quad (T,\ L + \tfrac12\Delta L).$$
   Otherwise the code checks that the point lies inside the triangle: for each vertex $i$, with the other two $j$, $k$, the sign of
   $$f\left[(L_j - L_k)(T - T_j) + (T_k - T_j)(L - L_j)\right]$$
   ($f$ = `FTRI`, the orientation) must not be negative. If it is, vertex $i$ is replaced by $T_i \to T_j + T_k - T_i$, $L_i \to L_j + L_k - L_i$ (the triangle flips across that side, and its orientation changes), and the check repeats. After 1,000 reflections the run stops (`STOP 1`), with a message on the screen and `ISHORT`; the walk never ended for a degenerate triangle.

    > **Question** ([[#L138]]; [[#L144]]; [[#L167]]; [[#L172]]). **The tolerance `TRIERR`.** It is always zero, so the point must be strictly inside or on the triangle. Is the variable left from an older tolerance?

3. **New envelopes.** For each new vertex, `ENVINT` integrates at $L_i$ and $T_i$ (the vertex's $\log T_\mathrm{eff}$ is kept in the local `VTEFFL`), with $\log R = \tfrac12(\log L + \log L_\odot - 4\log T_\mathrm{eff} - \log 4\pi - \log\sigma)$ and $\log g = \log G + \log M - 2\log R$; for a spotted star whose outermost point is convective (`LC(M)`), at the ambient temperature $T_\mathrm{amb}$ of the unspotted surface,
   $$T_\mathrm{amb}^4 = \frac{T_\mathrm{eff}^4}{f x^4 + 1 - f},$$
   where $f$ is the spot filling factor (`SPOTF`) and $x = T_\mathrm{spot}/T_\mathrm{amb}$ (`SPOTX`), so that spots and ambient surface together radiate $\sigma T_\mathrm{eff}^4$ (the same formula as in [[starin.f|starin.f]]).
4. **The plane.** With $(P_i, T^\mathrm{f}_i)$ the fitting point's $\log P$ and $\log T$ of envelope $i$, each $Q \in \{\log r_\mathrm{f}, \log L, \log T_\mathrm{eff}\}$ is fitted exactly through the three envelopes:
   $$Q = c_1\,\log P + c_2\,\log T + c_3,$$
   with `CFENV(1:3)` for $\log r_\mathrm{f}$, the radius at the fitting point, `CFENV(4:6)` for $\log L$, `CFENV(7:9)` for $\log T_\mathrm{eff}$. A degenerate fit stops the run (`STOP 1`), with the three fitting points on the screen and `ISHORT`: two points at the same $\log T$ ($|T^\mathrm{f}_2 - T^\mathrm{f}_1| \le 10^{-10}|T^\mathrm{f}_3 - T^\mathrm{f}_1|$), or a pivot `DEN` below $10^{-10}$ of the differences it is made of (three points collinear in $(\log P, \log T)$); either gave infinite or NaN coefficients before.

    > **Question** ([[#L146-L154]]; [[#L253-L262]]). **The accuracy of the plane.** The boundary condition is linear in $\log P$ and $\log T$ across a triangle of $\Delta\log T_\mathrm{eff}$ = `TRIDT` = 0.01 and $\Delta\log L$ = `TRIDL` = 0.08 by default. What error in $R$ or $T_\mathrm{eff}$ does this linearization introduce, and was the default size tested against a smaller triangle, for instance in the solar calibration? A reader would expect the curvature of $\log r_\mathrm{f}$ with $T_\mathrm{eff}$ to matter most where the envelope's structure changes fast, such as near the onset of surface convection.

**Design.** `NUMENV` here is a local counter (`DATA NUMENV/0/`), not the envelope's point count in [[envstruct_mod.f|`ENVSTRUCT_MOD`]]. The comment "IF LNEW0, REDO ALL 3 ENVELOPES EVERY MODEL" refers to the caller; `LNEW0` is not used here.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) (Surface boundary conditions): the surface boundary condition is solved from three envelope models; `TRIDT` (default 0.01) is the spacing in $\log T_\mathrm{eff}$ between two of them, and `TRIDL` (0.08) the spacing in $\log L$ of the third, at their mean $T_\mathrm{eff}$. `KTTAU` selects the atmosphere (the documentation lists 0 Eddington, 1 Krishna Swamy, 3 Kurucz, 4 Allard).

**Changed since `rp_1`.** COMMON blocks to modules (the atmosphere flags, the triangle's size and the spot parameters now in `NMLPAR_MOD`), `IMPLICIT NONE`; a new argument `CMIXL`, the mixing length, passed on to `ENVINT`.

**Changed since `a8a5950`.** Each vertex is integrated at a local `VTEFFL`, so `TEFFL` no longer returns as the last vertex's temperature, which [[crrect.f#CRRECT|CRRECT]] had passed on to [[tpgrad.f#TPGRAD|TPGRAD]]'s depth-dependent spot contrast (settles former question 1); the switch back from the gray atmosphere starts a new triangle (settles former question 5); the reflection walk stops after 1,000 reflections, and a degenerate plane fit stops the run.

### SURFBC

The envelope triangle: keeps three envelope integrations around $(\log T_\mathrm{eff}, \log L)$, flips the triangle when the model leaves it, and fits the plane `CFENV` that gives $\log r_\mathrm{f}$, $\log L$ and $\log T_\mathrm{eff}$ from $\log P$ and $\log T$ at the fitting point.
