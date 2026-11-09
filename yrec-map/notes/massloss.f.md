## Explanation

**Purpose.** `MASSLOSS` is the driver for mass loss or accretion in a step (MHP 10/01). It sets the rate $\dot M$ (constant, or from a Reimers formula), computes quantities of the convective envelope and of accreted matter, and calls [[mdot.f#MDOT|`MDOT`]] to change the model's mass. Sign convention: $\dot M > 0$ is a mass gain (accretion), $\dot M < 0$ a loss. Its header comment: "This is experimental code and valid for Allard atmospheres only" (llp 06/15/2009). `KNOWN_ISSUES.md` (issue 12) calls this section "experimental, partially implemented": The quantities it computes for physics "not wired up yet" are "not finished", not "dead". The entropies serve accretion: a commented-out line in [[mdot.f#MDOT|`MDOT`]] used `SACC - SCEN`, the entropy of the accreted matter relative to the envelope's (whether that difference was meant to decide if accretion expands the envelope is asked on MDOT's page). As the code stands, MDOT (its step 4) scales the expansion or contraction by the envelope's entropy `SCEN` alone, and `SCEN` set to 0 at the end of this routine switches the effect off.

> **Question** ([[#L6-L7]]; [[#L180-L182]]). **Allard atmospheres only.** `ALSURFP` is called whatever atmosphere the run uses. Should the routine check the atmosphere choice, or stop otherwise?

**How it fits.**
- **Who calls it:** the main program, [[main.f#(file level)|main.f]], in a step when `LAGE` is true (main.f:700–705), before the lithium burning of [[liburn.f#LIBURN|`LIBURN`]]; the main program sets `LNEWFIT` false just before the call.
- **Inputs:** `BL` ($\log L/L_\odot$), `DAGE` (Gyr), `DELTS` (s), the model (`HCOMP`, `HD`, `HP`, `HR`, `HS`, `HS1`, `HS2`, `HT`, `HJM`, `OMEGA`, `M`), `HSTOT` (log of the total mass in g), `SMASS` (mass in $M_\odot$), `TEFFL`, `JENV` (the base of the surface convection zone).
- **Outputs:** `LNEWFIT`, set true only for accretion; the main program then calls [[getnewenv.f#GETNEWENV|`GETNEWENV`]] to restore the earlier fitting point (main.f:1008). Through `MDOT`: the changed model, `DELTS`, `SMASS`, `HSTOT`, `LNEW`, `SENVOLD`. In `MASSCHG2_MOD`: `SACC` and `SCEN` (`MDOT` reads `SCEN`; [[coefft.f#COEFFT|`COEFFT`]] reads only `DLOGT` and `DLOGP`, which `MDOT` sets). In `DEUTER_MOD`: `JCZ`, the base of the convective envelope (or `M` if there is none).
- **Calls:** [[alsurfp.f#ALSURFP|`ALSURFP`]] (surface pressure from Allard atmospheres), [[eqstat.f#EQSTAT|`EQSTAT`]] (twice), [[mdot.f#MDOT|`MDOT`]].
- **Modules:** `NMLPAR_MOD` (the run's parameters, formerly in COMMON `MASSCHG`: `DMDT0`, `CREIM`, `LREIMER`, `LMDOT`, `COMPACC`; set in [[parmin.f#PARMIN|`PARMIN`]], defaults `DMDT0` = −1e−14 $M_\odot$/yr, `CREIM` = −4e−13, `LMDOT` and `LREIMER` false), `MASSCHG2_MOD`, `ATMPRT_MOD` (the surface point from `ALSURFP`), `OVRTRN_MOD` (`TAUCZ`, the convective turnover time; the comment at line 104 says it is computed in `MIXCZ`, but it is now set by [[gettau.f#GETTAU|`GETTAU`]], through [[tauintnew.f#TAUINTNEW|`TAUINTNEW`]] (the new method), [[tauint.f#TAUINT|`TAUINT`]] or [[taucal.f#TAUCAL|`TAUCAL`]]), `DEUTER_MOD`, `CONSTANTS_MOD` (the constants), and `DIMENSIONS_MOD` (`JSON`).

**The method.**
1. If mass change is off (`LMDOT` false), set `LNEWFIT` false and return. Otherwise $\dot M$ = `DMDT0` (in $M_\odot$/yr, as `MDOT` converts it).
2. Radius from $L = 4\pi R^2\sigma T_\mathrm{eff}^4$: $\log R = \tfrac12(\log L - \log 4\pi\sigma - 4\log T_\mathrm{eff})$, with $L$ in erg/s.
3. Reimers (`LREIMER`): $\dot M = \eta\,L/(g R)$ with $\eta$ = `CREIM` and $g = GM/R^2$, all in cgs (bug 1 on the units). The age in seconds, `AGETOT`, is computed and not used (unused?, [[#L97]]).
4. If there is a convective envelope (`JENV` < `M`), print `TAUCZ` (in years) and $R/R_\odot$ (labeled `MASSLOSS: TAUCZ (YR), R/RSUN`), and set `JCZ` = `JENV`; otherwise set `TAUCZ` = 0 (in the shared block) and `JCZ` = `M`. The envelope's mass $M_\mathrm{cz}$ = `SUMDM` $= \sum_{j=\mathrm{JENV}}^{M}$ `HS2(j)`.
5. If $\dot M > 0$ (accretion), set `LNEWFIT` true, and with $e_\mathrm{acc} = f\,GM/R$ (`EACC0`; $f$ = `FACC` = 1), which the comments describe as the kinetic energy per gram of accreted matter (from the virial theorem):
   - over the convective envelope, the mass-weighted means of $e_\mathrm{acc}[1 + \tfrac12(R/r - 1)]$ (this mean overwrites `EACC`), of the thermal energy $P\beta/\rho$ (`ETHAV`), and of the entropy-like quantity
   $$s = \frac{P\beta}{\rho T}\left(\tfrac32\ln T - \ln\rho\right),\qquad \beta = 1 - \frac{aT^4}{3P}$$
   (`SCEN`; $a/3$ = `CA3`; $P\beta/(\rho T)$ = `RMU` is the gas constant over the mean molecular weight);
   - at the photosphere from `ALSURFP` and the EOS: `SACC`, the same $s$, only if the lookup succeeded (`LAlFail` false); otherwise a message says that the accreted matter's entropy was not computed, and `SACC` keeps its earlier value;
   - an alternative surface state "from Stahler 1988", with $\dot M$ in g/s: $P = \frac{\dot M}{4\pi}\sqrt{2f\,g/R^3}$, $T = \big(\tfrac34\,\dot M\,e_\mathrm{acc}/(4\pi R^2\sigma)\big)^{1/4}$ (with `EACC0`), its $s$ in `SACC2`;
   - finally `SCEN` is set to 0 in both branches, so the envelope's mean entropy computed above is discarded, and `SACC2` is not used (unused?: The lines that used it are commented out, [[#L221-L224]]); the code is unfinished (issue 12 above; settled from YREC's notes, Nov 9, 2026: [[#L152-L177]], [[#L209-L227]]).
6. Call `MDOT` with $\dot M$, the mean $e_\mathrm{acc}$, the mean thermal energy, $M_\mathrm{cz}$, and `RMU`. MDOT recomputes `RMU` before using it, and uses `EACC` and `ETHAV` only for `ETHNEW` and `FAC`, which it does not use ([[mdot.f#L162-L174]]): The three arguments have no effect (unused?), so for a loss it does not matter that they are stale values from an earlier call (`SAVE`), or undefined on a first call.

**Design.** It writes `TAUCZ` (in years) and $R/R_\odot$ to the terminal on every call with a convective envelope. Its locals are `SAVE`d.

> **Question** ([[#L116-L117]]). **A debug line.** The unconditional write of `TAUCZ/CSECYR` and `RTOT/CRSUN` (labeled `MASSLOSS: TAUCZ (YR), R/RSUN` since `a8a5950`) looks like debugging output. Should it go, or move to the `.short` file?

**Changed since `rp_1`.** COMMON blocks to modules, `IMPLICIT NONE`; the unused `SCRTCH` dropped; the call to `MDOT` no longer passes `BL`, so its 23 arguments line up (settles former question 6); `MASSCHG2`'s order corrected to `…, DLOGP, DLOGT`, as in `MDOT` and `COEFFT` (settles former question 7).

**Changed since `a8a5950`.** `LAlFail` is now checked: after a failed `ALSURFP` lookup, the surface point (the previous lookup's `AT`, `AP`) is no longer used, and the accreted matter's entropy is skipped with a message, which settles that part of question 1; the diagnostic print of `TAUCZ` and $R/R_\odot$ is labeled, which question 4 now reflects.

## Bugs, by priority

1. **(a)** **The Reimers rate is in g/s, read as $M_\odot$/yr.** ([[#L100-L103]]; [[mdot.f#L111]]; [[mdot.f#L159]]) `DMDT = CREIM*10.0D0**(BL + CLSUNL)/GSURF/RTOT` is $\eta\,L/(gR) = \eta\,LR/(GM)$ with $L$, $R$, $M$ in cgs, a rate in g/s times $\eta$: for the Sun $L_\odot R_\odot/(GM_\odot) \approx 2.0\times10^{18}$ g/s. MDOT reads `DMDT` as $M_\odot$/yr (it multiplies by `CMSUN/CSECYR`). With the default `CREIM` = −4e−13, Reimers' coefficient for $L$, $R$, $M$ in solar units and $\dot M$ in $M_\odot$/yr, the Sun would lose about $8\times10^{5}\,M_\odot$/yr, and MDOT's step limits would cut the step accordingly. Only with `LMDOT` and `LREIMER` (both off by default). Read from the code, not run. **A possible fix:** Reimers' law in solar units:

    ```fortran
          IF(LDOMDOT .AND.LREIMER)THEN
    C 11/09/26 KC via Claude
    C code changed to evaluate the Reimers rate with L, R and M in solar
    C units, for which CREIM is defined, so that DMDT is in MSUN/YR.
             DMDT = CREIM*10.0D0**BL*(RTOT/CRSUN)/SMASS
          ENDIF
    ```

### MASSLOSS

Sets $\dot M$ (constant or Reimers), computes the accretion energetics and entropies, and calls `MDOT` (above).
