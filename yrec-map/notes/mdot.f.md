## Explanation

**Purpose.** `MDOT` applies a mass change (loss or accretion) to the model over a step: it limits the step so that not too much mass changes, removes mass from the surface convection zone or adds it at the surface, rescales the mass coordinates, the total mass and the shell masses, removes angular momentum with lost mass, and for accretion mixes the accreted composition into the convection zone. Sign convention: `DMDT` > 0 is a mass gain.

**How it fits.**
- **Who calls it:** only [[massloss.f#MASSLOSS|`MASSLOSS`]], when `LMDOT` is true.
- **Inputs and outputs (arguments):** `DELTS` (s, may be shortened), the model (`HCOMP`, `HD`, `HJM`, `HP`, `HR`, `HS`, `HS1`, `HS2`, `HT`, `OMEGA`, `M`, `JENV`), `HSTOT` and `SMASS` (updated), `DMDT` ($M_\odot$/yr), `RTOT`, `SUMDM` (the convection zone's mass, from `MASSLOSS`); `EACC`, `ETHAV` and `RMU` have no effect (unused?; see step 4); outputs `LNEW` (= true: recompute the surface boundary condition) and `SENVOLD` (the old `HS(M)` − `HSTOT`, for [[getnewenv.f#GETNEWENV|`GETNEWENV`]]).
- **Modules:** [[nmlpar_mod.f|`NMLPAR_MOD`]], the namelist variables (`FCZDMDT`, `FTOTDMDT`, `COMPACC`, `LMDOT`, `TDISK`, `LDISK`, `LROT`, `WALPCZ`, `LSOLWIND`); [[masschg2_mod.f|`MASSCHG2_MOD`]] (`SCEN`, `SMASS0`, `DLOGP`, `DLOGT`; with `MASSLOSS` and [[coefft.f#COEFFT|`COEFFT`]], which adds `DLOGT`, `DLOGP` to $\log T$, $\log P$ at and above `JENV` in its entropy terms when `LMDOT` and `DMDT0` > 0); [[disk_mod.f|`DISK_MOD`]] (the age `SAGE`, for the disk lifetime); [[comp_mod.f|`COMP_MOD`]] (`STOTAL`, `SENV`); [[deuter_mod.f|`DEUTER_MOD`]] (`FMASSACC`, read by [[liburn.f#LIBURN|`LIBURN`]], [[dburn.f#DBURN|`DBURN`]] and [[dburnm.f#DBURNM|`DBURNM`]]); [[constants_mod.f|`CONSTANTS_MOD`]]; `JSON` from [[dimensions_mod.f|`DIMENSIONS_MOD`]]. The solar-wind parameters `DMSUN`, `DMWSUN`, `DMWMAX` (formerly COMMON `MASSCHG3`) are now locals set to zero by DATA.

**The method.** Two masses of the convection zone appear: $M_\mathrm{cz}$ = `DMCZ` = `HS1(M)` − `HS1(JENV)` (or `HS1(M)` if `JENV` = 1), and $M'_\mathrm{cz}$ = `DMCZT` = `SUMDM`.
1. Optionally (`LSOLWIND` with rotation, and only if `DMWSUN` > 0) $\dot M = \dot M_\odot\,\min\big((\Omega/\Omega_\odot)^2, (\Omega_\mathrm{max}/\Omega_\odot)^2\big)$, with $\dot M_\odot$ = `DMSUN`, $\Omega_\odot$ = `DMWSUN`, $\Omega_\mathrm{max}$ = `DMWMAX`. Since these three are zero, the branch is inert; the guard on `DMWSUN` keeps it from dividing by zero now that `LSOLWIND` reaches this routine from the namelist.
2. Rate in g/s: $|\dot M|\,M_\odot/\mathrm{yr}$. Step limits: $\Delta t \le f_\mathrm{tot}M/|\dot M|$, $\Delta t \le f_\mathrm{cz}\,M_\mathrm{cz}/|\dot M|$ ($f_\mathrm{tot}$ = `FTOTDMDT`, $f_\mathrm{cz}$ = `FCZDMDT`; a zero rate sets neither), and at most half the mass outside the fitting point, $\tfrac12(10^{\texttt{HSTOT}} - 10^{\texttt{HS(M)}})/|\dot M|$. The comment speaks of adding mass, but this limit applies to loss as well. With a disk (`LDISK`) and accretion, the step ends at the disk's lifetime `TDISK` (Gyr), and `LMDOT` is then turned off (bug 1). A model without a surface convection zone (`JENV` = `M`) stops the run (bug 2).
3. $\Delta M = \dot M\,\Delta t$ (g).
4. **Accretion** ($\Delta M > 0$):
   - the new mean thermal energy $\bar e = (e_\mathrm{acc}\Delta M + \bar e_\mathrm{th}M'_\mathrm{cz})/(\Delta M + M'_\mathrm{cz})$ and `FAC` = $\log_{10}(\bar e/\bar e_\mathrm{th})$ are computed but not used (their use is commented out);
   - `RMU` = $P\beta/(\rho T)$ (the gas constant over $\mu$) is recomputed at `JENV`, and a scale factor $\Delta\ln E = (\Delta M/M_\mathrm{cz})\,s_\mathrm{cen}/(\mathcal{R}/\mu)$, with $s_\mathrm{cen}$ = `SCEN`, gives $\Delta\log r = \tfrac23\Delta\ln E/\ln 10$, $\Delta\log T = -\Delta\log r$, $\Delta\log P = -4\Delta\log r$ (homologous expansion of the envelope: $P \propto r^{-4}$, $T \propto r^{-1}$ at fixed $m$; the mass term `DLNM` is set to zero);
   - if `JENV` = 1 (fully convective), $\log r$, $\log P$, $\log T$ of every point change by these amounts; otherwise only $P$ and $T$ at `JENV`, and the radii above it are stretched about $r_\mathrm{b} = r_\mathrm{JENV}$: $r \leftarrow r_\mathrm{b} + 10^{\Delta\log r}(r - r_\mathrm{b})$.
   
   `MASSLOSS` sets `SCEN` = 0, so these changes are zero in practice: The code is kept for later work, as part of the experimental mass-loss section, "not finished," not "dead" (settled from `KNOWN_ISSUES.md`, issue 12, Nov 9, 2026).

    > **Question** ([[#L173-L174]]). **The form of the expansion.** A commented-out line scaled the expansion by `SACC - SCEN`, the entropy of the accreted matter relative to the envelope's; the active one by `SCEN` alone. An expansion scaled by `SCEN` alone depends on the units, since the entropy is defined only up to an additive constant (it contains $\ln T$ and $\ln\rho$ in cgs). When the code is revived, is `SACC - SCEN` the intended form?

5. **Angular momentum** (rotation, loss): the lost matter carries the surface's specific angular momentum, $\Delta J = \tfrac23 R^2\,\Omega_s\,\Delta M$ (solid-body zone, `WALPCZ` ≥ 0), or $j_s\Delta M$ (`WALPCZ` ≤ −2), or the same with $\Omega_s = \Omega_M (R/r_M)^{\texttt{WALPCZ}}$, the law $\Omega \propto r^{\texttt{WALPCZ}}$ that [[wczimp.f#WCZIMP|`WCZIMP`]] imposes; the zone's new angular momentum is $J_\mathrm{cz}+\Delta J$, with $J_\mathrm{cz} = \sum$ `HJM`·`HS2` from `JENV` to `M`. Its specific angular momentum `HJM` is scaled after step 7, once the new shell masses are known, by $(J_\mathrm{cz}+\Delta J)/\sum$ `HJM`·`HS2`, so that the zone holds exactly $J_\mathrm{cz}+\Delta J$.

    > **Question** ([[#L206]]; [[#L280]]). **Angular momentum of accreted matter.** For accretion `HJM` is not changed while `HS2(M)` grows, so the accreted matter implicitly takes the outer point's specific angular momentum. Is that intended?

6. **Mass coordinates** (loss): points in the zone are compressed toward its base, $m_i \leftarrow m_\mathrm{b} + \frac{M_\mathrm{cz}+\Delta M}{M_\mathrm{cz}}(m_i - m_\mathrm{b})$; in a fully convective star (`JENV` = 1), toward the center, $m_i \leftarrow \frac{M_\mathrm{cz}+\Delta M}{M_\mathrm{cz}}\,m_i$ for every point, consistent with $M_\mathrm{cz}$ = `HS1(M)` there. For accretion `HS1` is not changed: the gain goes to the outermost shell.

    > **Question** ([[#L240-L258]]; [[#L280]]). **All accreted mass in the last shell.** For accretion `HS1` is unchanged and the gain goes to `HS2(M)`, which over many steps grows unless rezoning redistributes it. The main program calls [[hpoint.f#HPOINT|HPOINT]] after every step (except in helium-flash runs, `LKUTHE`). Does its criterion split a growing outermost shell, so that the surface resolution survives long accretion?

7. New total mass (`SMASS`, `SMASS0`, `HSTOT`, `STOTAL`), shell masses `HS2` from `JENV` to `M` − 1 as half the distance between neighbours (for `JENV` = 1, `HS2(1)` = (`HS1(1)` + `HS1(2)`)/2, the innermost shell running from the center), `HS2(M)` = $10^{\texttt{HSTOT}}$ − (`HS1(M)` + `HS1(M−1)`)/2, and `SENV`.
8. **Accretion:** elements 1–11 of the zone are mixed with the accreted composition `COMPACC`, $\bar x = \big(\sum_j x_j\,\Delta m_j + x_\mathrm{acc}\Delta M\big)/\big(\sum_j \Delta m_j+\Delta M\big)$, summed over the zone's shells `JENV` to `M` with their masses before the accretion ($\Delta m_j$ = `HS2(J)`, less $\Delta M$ for `HS2(M)`), so that every species is conserved; `FMASSACC` = $\Delta M$.

**Design.** Several unconditional `WRITE(*,…)` lines report the step reduction, the angular momentum and the mass change.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) lists `LMDOT`, "experimental mass-loss module," and `LSOLWIND`, mass loss scaled to the solar wind, "not implemented," among the experimental options.

**Changed since `rp_1`.** COMMON blocks to modules, `IMPLICIT NONE`; `MASSCHG3` dropped (its three reals now zeroed locals, `LSOLWIND` from the namelist); the solar-wind branch guarded by `DMWSUN` > 0 (a bug fix: it would have given $\dot M$ = NaN). The call from `MASSLOSS` now matches the interface (fixed in massloss.f), which settles former question 1; former question 2 (`MASSCHG3` set nowhere) is settled by the authors' fix, which confirms it and keeps the option inert until the three parameters are given a source.

**Changed since `a8a5950`.** Five fixes in the experimental mass-change path: a zero rate no longer divides by zero in the step limits; the wind's surface rate now follows $\Omega \propto r^{\texttt{WALPCZ}}$, the law `WCZIMP` imposes (the old form had the ratio inverted), which settles former question 5; `HJM` is now scaled after the new shell masses are known, so that the zone loses exactly $\Delta J$, which settles former question 6; in a fully convective star the mass loss compresses the points about the center, and `HS2(1)` is (`HS1(1)` + `HS1(2)`)/2 instead of reading `HS1(0)`, which settles former question 4; accretion mixes the zone's mass-weighted abundances instead of the base shell's. Former question 7 is now 4.

## Bugs, by priority

1. **(not reached)** **Accretion past the disk's lifetime gives a negative step.** ([[#L146-L157]]; [[main.f#L981]]) With `LDISK` and accretion, `TEST = SAGE + 1.0d-9*DELTS/CSECYR` is the age at the end of the step, and when it exceeds `TDISK` the step is cut to `DELTS = (TDISK-SAGE)*1.0D9*CSECYR`. If `SAGE` already exceeds `TDISK`, this is negative: `DELM` = `DMDT*CMSUN*DELTS/CSECYR` is then negative, so the accretion is applied as a loss, and the main program goes on with a negative step (what it then does was not traced). The main program sets `SAGE = DAGE` only after the step's call to MASSLOSS ([[main.f#L981]]), so in the first step `SAGE` is unset (0 with zero-initialized storage), and from the second step on it is the model's age: a run that starts from a model older than `TDISK` reaches this. Only with `LMDOT`, `LDISK` (both off by default), and `DMDT0` > 0.

    **A possible fix:**

    ```diff
    --- a/src/mdot.f
    +++ b/src/mdot.f
    @@ -146,7 +146,13 @@
     C mhp 8/10 turn mass loss off when disk exhausted only when dm /dt > 0, e.g. accretion
           IF(LDISK .AND. DMDT.GT.0.0D0)THEN
              TEST = SAGE + 1.0d-9*DELTS/CSECYR
    -         IF(TEST.GT.TDISK)THEN
    +C 11/09/26 KC via Claude
    +C code changed to stop accreting, without a negative step, when the
    +C disk is already gone at the start of the step.
    +         IF(SAGE.GE.TDISK)THEN
    +            DMDT = 0.0D0
    +            LDONE = .TRUE.
    +         ELSE IF(TEST.GT.TDISK)THEN
                 DELTS = (TDISK-SAGE)*1.0D9*CSECYR
                 LDONE = .TRUE.
              ELSE
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached: No run had `LMDOT` with `LDISK` and accretion; the two made-up Reimers runs ([[massloss.f#b1]]) lose mass, so they skip this test. The fix was not run. What would reach it: `LMDOT`, `LDISK`, and `DMDT0` > 0, from a starting model older than `TDISK`. Intent: The comment above the test, "turn mass loss off when disk exhausted only when dm /dt > 0, e.g. accretion," means to end the accretion, not to reverse it.

2. **(stops the run)** **Checked by KC** (Nov 10, 2026). **A stop without a message when there is no surface convection zone.** ([[#L118]]; [[massloss.f#L106-L122]]) `IF(JENV.EQ.M) STOP911` (that is, `STOP 911`) ends the run with only the stop code 911, written nowhere else, when the model has no surface convection zone. MASSLOSS handles that case (it sets `TAUCZ` = 0 and `JCZ` = `M`) and then calls MDOT anyway, so a run with mass change on reaches the stop as soon as its envelope turns radiative. Only with `LMDOT` (off by default).

    **A possible fix:** say why the run stops (whether mass change should instead go on without a convection zone is the developers' choice):

    ```diff
    --- a/src/mdot.f
    +++ b/src/mdot.f
    @@ -115,7 +115,13 @@
     C      DMCZT = 10.0D0**HSTOT - HS1(JENV)
           DMCZT = SUMDM
     C COMPUTE MASS OF SURFACE CONVECTION ZONE BELOW FITTING POINT
    -      IF(JENV.EQ.M) STOP911
    +C 11/09/26 KC via Claude
    +C code changed to say why the run stops when there is no surface
    +C convection zone.
    +      IF(JENV.EQ.M) THEN
    +         WRITE(*,*)'MDOT: NO SURFACE CONVECTION ZONE; STOPPED'
    +         STOP 911
    +      ENDIF
           IF(JENV.GT.1) THEN
              DMCZ = HS1(M) - HS1(JENV)
           ELSE
    ```

    **How the code itself shows it.** MASSLOSS expects the case: When `JENV` equals `M`, it sets `TAUCZ = 0.0D0` and `JCZ = M` ([[massloss.f#L106-L122]]) rather than stopping, and MDOT's next lines handle the other end, a fully convective star, with `DMCZ = HS1(M)` ([[#L119-L123]]), but not this one. Elsewhere YREC meets a missing surface convection zone with a message: MIX writes "`NO SURFACE CZ - DIFFUSION NOT MEANINGFUL`" and goes on ("`DBG 2/92 CHANGED STOP TO JUST A WARNING MESSAGE, EXECUTION CONTINUES`", [[mix.f#L428-L433]]), and ROTMIX writes the same message before it stops with `STOP 1` ([[rotmix.f#L163-L170]]). Other run-time stops, such as CHECKJ's and WIND's, also write why first and use `STOP 1`, "`the run-time error code (issue 38)`" ([[checkj.f#L152-L159]]; [[wind.f#L72-L76]]); 911 is used as a stop code nowhere else in active code. The fix above keeps `STOP 911` and leaves two questions for the developers: Should this stop, too, use `STOP 1`, or should mass change go on without a convection zone, as diffusion does in MIX?

    **Checked by running YREC** (Nov 9, 2026, the 1 $M_\odot$ runs repeated on Nov 10 with a private start model; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The line ran at every MDOT call of the two made-up Reimers runs ([[massloss.f#b1]]), 8,341 and 920 times (`JENV` from 1 to 685, `M` from 368 to 957), and `JENV` = `M` never held: The wrong Reimers rate ruins those runs first. With the Reimers rate fixed, both end here, at `STOP 911` with no message (exit status 143, that is 911 mod 256): the 3 $M_\odot$ star at model 129 (0.0017 Gyr), the 1 $M_\odot$ star at model 6,599 (12.595 Gyr, 0.707 $M_\odot$). So a run with mass change that reaches this test ends with only the stop code. No fix was run, since the page's fix adds only a message. Intent: MDOT's header says the routine has never run, since every namelist sets `LMDOT` = .FALSE.

### MDOT

Step limit, mass removal or addition, angular-momentum loss, and mixing of accreted matter (above).
