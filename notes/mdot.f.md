## Explanation

**Purpose.** `MDOT` applies a mass change (loss or accretion) to the model over a step: it limits the step so that not too much mass changes, removes mass from the surface convection zone or adds it at the surface, rescales the mass coordinates, the total mass and the shell masses, removes angular momentum with lost mass, and for accretion mixes the accreted composition into the convection zone. Sign convention: `DMDT` > 0 is a mass gain.

**How it fits.**
- **Who calls it:** only [[massloss.f#MASSLOSS|`MASSLOSS`]] (but with a shifted argument list: question 1).
- **Inputs and outputs (arguments):** `DELTS` (s, may be shortened), the model (`HCOMP`, `HD`, `HJM`, `HP`, `HR`, `HS`, `HS1`, `HS2`, `HT`, `OMEGA`, `M`, `JENV`), `HSTOT` and `SMASS` (updated), `DMDT` ($M_\odot$/yr), `RTOT`, `SUMDM` (the convection zone's mass, from `MASSLOSS`); `EACC`, `ETHAV` and `RMU` have no effect (see step 4); outputs `LNEW` (= true: recompute the surface boundary condition) and `SENVOLD` (the old `HS(M)` − `HSTOT`, for [[getnewenv.f#GETNEWENV|`GETNEWENV`]]).
- **COMMON blocks:** `MASSCHG` (`FCZDMDT`, `FTOTDMDT`, `COMPACC`, `LMDOT`), `MASSCHG2` (`SCEN`, `SMASS0`, `DLOGP`, `DLOGT`; with `MASSLOSS` and [[coefft.f#COEFFT|`COEFFT`]], which adds `DLOGT`, `DLOGP` to $\log T$, $\log P$ at and above `JENV` in its entropy terms when `LMDOT` and `DMDT0` > 0), `MASSCHG3` (the scaled solar wind), `DISK` (disk lifetime: `SAGE`, `TDISK`, `LDISK`), `COMP` (`STOTAL`, `SENV`), `DEUTER` (`FMASSACC`, read by [[liburn.f#LIBURN|`LIBURN`]], [[dburn.f#DBURN|`DBURN`]] and [[dburnm.f#DBURNM|`DBURNM`]]), `ROT` (`LROT`, `WALPCZ`), `FLAG`, the constants.

**The method.** Two masses of the convection zone appear: $M_\mathrm{cz}$ = `DMCZ` = `HS1(M)` − `HS1(JENV)` (or `HS1(M)` if `JENV` = 1), and $M'_\mathrm{cz}$ = `DMCZT` = `SUMDM`.
1. Optionally (`LSOLWIND` with rotation) $\dot M = \dot M_\odot\,\min\big((\Omega/\Omega_\odot)^2, (\Omega_\mathrm{max}/\Omega_\odot)^2\big)$, with $\dot M_\odot$ = `DMSUN`, $\Omega_\odot$ = `DMWSUN`, $\Omega_\mathrm{max}$ = `DMWMAX`.
2. Rate in g/s: $|\dot M|\,M_\odot/\mathrm{yr}$. Step limits: $\Delta t \le f_\mathrm{tot}M/|\dot M|$, $\Delta t \le f_\mathrm{cz}\,M_\mathrm{cz}/|\dot M|$ ($f_\mathrm{tot}$ = `FTOTDMDT`, $f_\mathrm{cz}$ = `FCZDMDT`), and at most half the mass outside the fitting point, $\tfrac12(10^{\texttt{HSTOT}} - 10^{\texttt{HS(M)}})/|\dot M|$. The comment speaks of adding mass, but this limit applies to loss as well. With a disk (`LDISK`) and accretion, the step ends at the disk's lifetime `TDISK` (Gyr), and `LMDOT` is then turned off.
3. $\Delta M = \dot M\,\Delta t$ (g).
4. **Accretion** ($\Delta M > 0$):
   - the new mean thermal energy $\bar e = (e_\mathrm{acc}\Delta M + \bar e_\mathrm{th}M'_\mathrm{cz})/(\Delta M + M'_\mathrm{cz})$ and `FAC` = $\log_{10}(\bar e/\bar e_\mathrm{th})$ are computed but not used (their use is commented out);
   - `RMU` = $P\beta/(\rho T)$ (the gas constant over $\mu$) is recomputed at `JENV`, and a scale factor $\Delta\ln E = (\Delta M/M_\mathrm{cz})\,s_\mathrm{cen}/(\mathcal{R}/\mu)$, with $s_\mathrm{cen}$ = `SCEN`, gives $\Delta\log r = \tfrac23\Delta\ln E/\ln 10$, $\Delta\log T = -\Delta\log r$, $\Delta\log P = -4\Delta\log r$ (the mass term `DLNM` is set to zero);
   - if `JENV` = 1 (fully convective), $\log r$, $\log P$, $\log T$ of every point change by these amounts; otherwise only $P$ and $T$ at `JENV`, and the radii above it are stretched about $r_\mathrm{b} = r_\mathrm{JENV}$: $r \leftarrow r_\mathrm{b} + 10^{\Delta\log r}(r - r_\mathrm{b})$.
   
   `MASSLOSS` sets `SCEN` = 0, so these changes are zero in practice.
5. **Angular momentum** (rotation, loss): the lost matter carries the surface's specific angular momentum, $\Delta J = \tfrac23 R^2\,\Omega_s\,\Delta M$ (solid-body zone, `WALPCZ` ≥ 0), or $j_s\Delta M$ (`WALPCZ` ≤ −2), or the same with $\Omega_s = \Omega_M (r_M/R)^{\texttt{WALPCZ}}$; the zone's specific angular momentum `HJM` is scaled by $(J_\mathrm{cz}+\Delta J)/J_\mathrm{cz}$, with $J_\mathrm{cz} = \sum$ `HJM`·`HS2` from `JENV` to `M`.
6. **Mass coordinates** (loss): points in the zone are compressed toward its base, $m_i \leftarrow m_\mathrm{b} + \frac{M_\mathrm{cz}+\Delta M}{M_\mathrm{cz}}(m_i - m_\mathrm{b})$. For accretion `HS1` is not changed: the gain goes to the outermost shell.
7. New total mass (`SMASS`, `SMASS0`, `HSTOT`, `STOTAL`), shell masses `HS2` from `JENV` to `M` − 1 as half the distance between neighbours, `HS2(M)` = $10^{\texttt{HSTOT}}$ − (`HS1(M)` + `HS1(M−1)`)/2, and `SENV`.
8. **Accretion:** elements 1–11 of the zone are mixed with the accreted composition `COMPACC`, $\bar x = (x_\mathrm{JENV}\,M'_\mathrm{cz} + x_\mathrm{acc}\Delta M)/(M'_\mathrm{cz}+\Delta M)$; `FMASSACC` = $\Delta M$.

**Design.** Several unconditional `WRITE(*,…)` lines report the step reduction, the angular momentum and the mass change.

**KC's changes.** 2025-05-30: the variables of COMMON `MASSCHG3` reordered (the logical `LSOLWIND` moved to the end).

## Questions for the experts

1. **The call does not match the interface.** `MASSLOSS` calls `MDOT(BL, DELTS, HCOMP, …, SENVOLD)` with 24 arguments, but `MDOT` is declared `MDOT(DELTS, HCOMP, …, SENVOLD)` with 23: every argument is shifted by one (`MDOT`'s `DELTS` receives `BL`, its `HCOMP` receives `DELTS`, and so on). `MDOT` would write the shortened step into `MASSLOSS`'s `BL`, `LNEW` = true into the integer `JENV`, the new mass into `RTOT` and `SENVOLD` into `SUMDM`. This has been so since the first commit of the repository. Any run with `LMDOT` true would misbehave; has mass loss been used with this version?
2. **`MASSCHG3` is set nowhere.** No other unit declares it (in `PARMIN` its declaration is commented out, and `LSOLWIND` is a local namelist variable there), so `LSOLWIND`, `DMSUN`, `DMWSUN`, `DMWMAX` are never set. The scaled solar wind therefore cannot be switched on.
3. **Inert code.** With `SCEN` = 0 and `DLNM` = 0, the structure changes of step 4 vanish, and `ETHNEW` and `FAC` are not used; so `EACC`, `ETHAV` and the `RMU` argument have no effect. Is the code kept for later work?
4. **Hard stop.** `IF(JENV.EQ.M) STOP911` (that is, `STOP 911`) ends the run with only the stop code 911 when there is no surface convection zone.
5. **Angular momentum of accreted matter.** For accretion `HJM` is not changed while `HS2(M)` grows, so the accreted matter implicitly takes the outer point's specific angular momentum. Intended?
6. **Out-of-bounds read (apparent bug).** The loop `DO I = JENV,M-1: HS2(I) = 0.5D0*(HS1(I+1)-HS1(I-1))` (lines 185–186) reads `HS1(0)` when `JENV` = 1, a case the routine handles elsewhere (lines 54 and 110). Should it start at `MAX(JENV,2)`, with the central shell treated apart?
7. **The sign of `WALPCZ`.** Line 145 sets $\Omega_\mathrm{surf} \propto r^{-\alpha}$ with $\alpha$ = `WALPCZ`, the opposite sign to [[wcz.f#WCZ|WCZ]]'s $\Omega = C\,r^{\alpha}$ (wcz.f line 58); see [[getnewenv.f#GETNEWENV|GETNEWENV]], question 7. Which sign is meant?

### MDOT

Step limit, mass removal or addition, angular-momentum loss, and mixing of accreted matter (above).
