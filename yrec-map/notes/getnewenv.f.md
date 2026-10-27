## Explanation

**Purpose.** `GETNEWENV` moves the outer fitting point of the interior model outward, by turning part of the envelope into new interior points, so that the envelope again holds the fraction of the mass it held before the step's mass change ($\log(m_\mathrm{fit}/M)$ = `SENVOLD`). Its header (MHP 07/02): "move the outer fitting point when the total mass is being decreased; add new points by dropping a sinkline from the surface down and including new points up to the desired envelope mass". It integrates the envelope once from the surface, then copies the points between the old and the new fitting point into the model.

**When it runs.** The main program calls it when [[massloss.f#MASSLOSS|MASSLOSS]] has set `LNEWFIT`, which it does whenever its rate `DMDT` is positive (massloss.f line 129), whichever rate applies: the constant `DMDT0` or the Reimers rate `CREIM`$\,L/(gR)$. [[mdot.f#MDOT|MDOT]] adds `DELM` = `DMDT`$\cdot\Delta t$ to the total mass, so a positive `DMDT` raises $M$ while the interior points keep their masses, and the envelope above the last point grows; main.f's comment reads "restore prior fitting point if mass accretion is being included". The defaults of both rates are negative (`DMDT0` = $-10^{-14}$, `CREIM` = $-4\times10^{-13}$, parmin.f), so with them the routine is not called; the header's "mass is being decreased" disagrees with this trigger (question 6).

**How it fits.**
- **Who calls it:** only the main program ([[main.f#(file level)|main.f]]), when `LNEWFIT` is set (above); it then calls [[fpft.f#FPFT|FPFT]] with its own `OMEGA`.
- **Inputs:** `SENVOLD` (the desired fitting point, below); the model arrays (`HCOMP`, `HD`, `HL`, `HP`, `HR`, `HS`, `HT`, `LC`, `M`), the surface `BL` ($\log L/L_\odot$) and `TEFFL`, the rotation arrays, and `CMIXL`, the mixing-length parameter, passed on to `ENVINT`.
- **What it calls:** [[envint.f#ENVINT|ENVINT]] (the envelope integration) and, for rotating models, [[getrot.f#GETROT|GETROT]].
- **Outputs:** the model with `M` increased and the new points filled; `HS1`, `HS2` (unlogged masses and shell masses) for the new points; for rotating models, `HJM`, `HI`, `ETA2`, `QIW`, `R0`, `HKEROT` (not `OMEGA`, which is local: question 2) and the totals `SJTOT`, `SKEROT`; `LNEW` = true; `SENV` in `COMP_MOD`. It prints the new points to standard output.
- **Modules:** `ENVSTRUCT_MOD` (the envelope solution `ENVP`, `ENVT`, `ENVS`, `ENVD`, `ENVR`, `ENVX`, `ENVZ`, `LCENV`, `NUMENV`, written by `ENVINT`); `NMLPAR_MOD` (the envelope step sizes `ENVMAX`, `ENVMIN`, `ENVBEG`, temporarily set to `HPTTOL(8)` and restored; the starspot parameters `SPOTF`, `SPOTX`; `LROT`, `WALPCZ`; `LEXCOM`); `COMP_MOD` (`STOTAL` = $\log M$, `SENV`); `DEBHU_MOD` (the Debye–Hückel composition, set here from the surface shell); `CONSTANTS_MOD`; `DIMENSIONS_MOD` (`JSON`).

**The method.**
1. **Surface quantities.** From $L = 4\pi R^2\sigma T_\mathrm{eff}^4$ and $g = GM/R^2$:
$$\log R = \tfrac12\left(\log\frac{L}{L_\odot} + \log L_\odot - 4\log T_\mathrm{eff} - \log 4\pi - \log\sigma\right), \qquad \log g = \log G + \log M - 2\log R.$$
With spots (fraction $f$ = `SPOTF`, temperature ratio $x$ = `SPOTX`) and a convective surface, the ambient temperature is $\log T_\mathrm{amb} = \log T_\mathrm{eff} - \tfrac14\log(f x^4 + 1 - f)$.
2. **Envelope integration** from the surface down to the current fitting point with `ENVINT`, at the spacing `HPTTOL(8)`, without rotational distortion ($f_P = f_T = 1$).
3. **Matching.** The envelope's first point is at the mass of the last interior point; the differences there in $\log P$, $\log\rho$, $\log T$, $\log r$ are added to all envelope points, and points closer than $10^{-10}$ in $\log m$ are dropped.
4. **New points.** Each envelope point below the new fitting point becomes an interior point, with $L$ held at its value at the old fitting point and the abundances other than $X$ and $Z$ copied from it. The last point is interpolated linearly in $\log m$ to the new fitting point.
5. **Shell masses.** $m = 10^{\log m}$, $\Delta m_j = \tfrac12(m_{j+1} - m_{j-1})$, and the last shell takes the rest of the star.
6. **Rotation.** The new points get, as a first guess, constant $j$ if $\alpha$ = `WALPCZ` $\le -2$, solid body if $\alpha \ge 0$, and otherwise $\Omega \propto r^{-\alpha}$ (PARMIN limits $\alpha$ to $[-2, 0]$; on the sign, question 7); with $I = \tfrac23 r^2$ and $j = \Omega I$. `GETROT` then finds the rotation law, and the totals $J = \sum j\,\Delta m$ and $E_\mathrm{rot} = \sum\tfrac12\Omega j\,\Delta m$ are recomputed.

`SENV` is the fitting point's $\log(m/M)$, as can be read from `HS = ENVS + STOTAL`; it is limited to at most $-10^{-12}$.

**KC's changes.** The unused argument `HG` was removed (2025-05-31), and the elements of `/ENVSTRUCT/` were reordered (2025-05-30; JvS added elements in 08/25).

**Changed since `rp_1`.** `CMIXL` is a new argument, passed on to `ENVINT` (it was in `/CONST3/`); COMMON blocks to modules (the namelist parameters from `/INTENV/`, `/CTOL/`, `/SPOTS/`, `/ROT/` and `/FLAG/` now come from `NMLPAR_MOD`; the unused `/ENVPRT/` dropped), `IMPLICIT NONE`. No question is settled.

## Questions for the experts

1. **A sign error.** When the new fitting point lies between the last interior point and the first envelope point, `HCOMP(1,J) = HCOMP(1,M)+FX*(HCOMP(1,M)-ENVX(JM))`, and the same for $Z$. Every other interpolation is $a + f(b - a)$; this one is $a + f(a - b)$. Should it be `ENVX(JM)-HCOMP(1,M)`?
2. **`OMEGA` is a local array.** `OMEGA` is not an argument: it is declared in `DIMENSION` and is local. In step 6, the solid-body and general cases read `OMEGA(MM)`, which is never set in this routine (it keeps whatever an earlier call left). So in those cases the new points' $j$ (`HJM(J) = OMEGA(MM)*HI(J)` or `OMEGA(J)*HI(J)`) comes from that stale value. Then `GETROT` overwrites `OMEGA` locally and the result is used only for $E_\mathrm{rot}$, while the main program goes on to call FPFT with its own `OMEGA`, which has no values for the new points. Should `OMEGA` be passed in and out?
3. **Constant luminosity.** The new points take $L$ of the old fitting point. Fine for a thin envelope; is it still right when much mass is shed at once?
4. **Output to standard output.** The routine writes to `*` rather than to the run's output units. Intended?
5. **Composition of new points.** $^3$He and the other species (rows 4…) are copied from the old fitting point rather than taken from the envelope integration. Intended?
6. **Header and trigger.** The header says the routine is for a decreasing total mass, but it runs only when `DMDT` > 0, which MDOT applies as a mass gain (`SMASS = SMASS + DELM/CMSUN`, mdot.f line 175); main.f's comment says accretion. With mass loss (`DMDT` < 0) MDOT instead compresses the convective-envelope shells and no points are added. Is the header out of date, or was the routine meant for mass loss too?
7. **The sign of `WALPCZ`.** The general case sets $\Omega = \Omega_{MM}(r/r_{MM})^{-\alpha}$ (lines 258, 260). WCZ uses $\Omega = C\,r^{\alpha}$, for which $\alpha = -2$ is constant $j$ and $\alpha = 0$ solid body, matching this routine's two end cases; with $r^{-\alpha}$, $-2 < \alpha < 0$ gives $\Omega$ rising outward, between neither. MDOT (line 145) uses the same $r^{-\alpha}$. Should it be $r^{+\alpha}$? (The question matters only once question 2 is fixed, since `OMEGA(MM)` is unset.)

### GETNEWENV

Moves the fitting point outward after mass loss: integrates the envelope from the surface, matches it to the last interior point, adds the envelope points as new shells, and resets rotation for them (method above).
