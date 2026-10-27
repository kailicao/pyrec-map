## Explanation

**Purpose.** `MASSLOSS` is the driver for mass loss or accretion in a step (MHP 10/01). It sets the rate $\dot M$ (constant, or from a Reimers formula), computes quantities of the convective envelope and of accreted matter, and calls [[mdot.f#MDOT|`MDOT`]] to change the model's mass. Sign convention: $\dot M > 0$ is a mass gain (accretion), $\dot M < 0$ a loss. Its header comment: "This is experimental code and valid for Allard atmospheres only" (llp 06/15/2009).

**How it fits.**
- **Who calls it:** the main program, [[main.f#(file level)|main.f]], in a step when `LAGE` is true (main.f:700–705), before the lithium burning of [[liburn.f#LIBURN|`LIBURN`]]; the main program sets `LNEWFIT` false just before the call.
- **Inputs:** `BL` ($\log L/L_\odot$), `DAGE` (Gyr), `DELTS` (s), the model (`HCOMP`, `HD`, `HP`, `HR`, `HS`, `HS1`, `HS2`, `HT`, `HJM`, `OMEGA`, `M`), `HSTOT` (log of the total mass in g), `SMASS` (mass in $M_\odot$), `TEFFL`, `JENV` (the base of the surface convection zone).
- **Outputs:** `LNEWFIT`, set true only for accretion; the main program then calls [[getnewenv.f#GETNEWENV|`GETNEWENV`]] to restore the earlier fitting point (main.f:1008). Through `MDOT`: the changed model, `DELTS`, `SMASS`, `HSTOT`, `LNEW`, `SENVOLD`. In `MASSCHG2_MOD`: `SACC` and `SCEN` (`MDOT` reads `SCEN`; [[coefft.f#COEFFT|`COEFFT`]] reads only `DLOGT` and `DLOGP`, which `MDOT` sets). In `DEUTER_MOD`: `JCZ`, the base of the convective envelope (or `M` if there is none).
- **Calls:** [[alsurfp.f#ALSURFP|`ALSURFP`]] (surface pressure from Allard atmospheres), [[eqstat.f#EQSTAT|`EQSTAT`]] (twice), [[mdot.f#MDOT|`MDOT`]].
- **Modules:** `NMLPAR_MOD` (the run's parameters, formerly in COMMON `MASSCHG`: `DMDT0`, `CREIM`, `LREIMER`, `LMDOT`, `COMPACC`; set in [[parmin.f#PARMIN|`PARMIN`]], defaults `DMDT0` = −1e−14 $M_\odot$/yr, `CREIM` = −4e−13, `LMDOT` and `LREIMER` false), `MASSCHG2_MOD`, `ATMPRT_MOD` (the surface point from `ALSURFP`), `OVRTRN_MOD` (`TAUCZ`, the convective turnover time; the comment at line 104 says it is computed in `MIXCZ`, but it is now set in [[taucal.f#TAUCAL|`TAUCAL`]] and [[tauint.f#TAUINT|`TAUINT`]]), `DEUTER_MOD`, `CONSTANTS_MOD` (the constants), and `DIMENSIONS_MOD` (`JSON`).

**The method.**
1. If mass change is off (`LMDOT` false), set `LNEWFIT` false and return. Otherwise $\dot M$ = `DMDT0` (in $M_\odot$/yr, as `MDOT` converts it).
2. Radius from $L = 4\pi R^2\sigma T_\mathrm{eff}^4$: $\log R = \tfrac12(\log L - \log 4\pi\sigma - 4\log T_\mathrm{eff})$, with $L$ in erg/s.
3. Reimers (`LREIMER`): $\dot M = \eta\,L/(g R)$ with $\eta$ = `CREIM` and $g = GM/R^2$, all in cgs (see question 3 on the units).
4. If there is a convective envelope (`JENV` < `M`), print `TAUCZ` (in years) and $R/R_\odot$, and set `JCZ` = `JENV`; otherwise set `TAUCZ` = 0 (in the shared block) and `JCZ` = `M`. The envelope's mass $M_\mathrm{cz}$ = `SUMDM` $= \sum_{j=\mathrm{JENV}}^{M}$ `HS2(j)`.
5. If $\dot M > 0$ (accretion), set `LNEWFIT` true, and with $e_\mathrm{acc} = f\,GM/R$ (`EACC0`; $f$ = `FACC` = 1), which the comments describe as the kinetic energy per gram of accreted matter (from the virial theorem):
   - over the convective envelope, the mass-weighted means of $e_\mathrm{acc}[1 + \tfrac12(R/r - 1)]$ (this mean overwrites `EACC`), of the thermal energy $P\beta/\rho$ (`ETHAV`), and of the entropy-like quantity
   $$s = \frac{P\beta}{\rho T}\left(\tfrac32\ln T - \ln\rho\right),\qquad \beta = 1 - \frac{aT^4}{3P}$$
   (`SCEN`; $a/3$ = `CA3`; $P\beta/(\rho T)$ = `RMU` is the gas constant over the mean molecular weight);
   - at the photosphere from `ALSURFP` and the EOS: `SACC`, the same $s$;
   - an alternative surface state "from Stahler 1988", with $\dot M$ in g/s: $P = \frac{\dot M}{4\pi}\sqrt{2f\,g/R^3}$, $T = \big(\tfrac34\,\dot M\,e_\mathrm{acc}/(4\pi R^2\sigma)\big)^{1/4}$ (with `EACC0`), its $s$ in `SACC2`;
   - finally `SCEN` is set to 0.
6. Call `MDOT` with $\dot M$, the mean $e_\mathrm{acc}$, the mean thermal energy, $M_\mathrm{cz}$ and `RMU`.

**Design.** It writes `TAUCZ` (in years) and $R/R_\odot$ to the terminal on every call with a convective envelope. Its locals are `SAVE`d.

**Changed since `rp_1`.** COMMON blocks to modules, `IMPLICIT NONE`; the unused `SCRTCH` dropped; the call to `MDOT` no longer passes `BL`, so its 23 arguments line up (settles former question 6); `MASSCHG2`'s order corrected to `…, DLOGP, DLOGT`, as in `MDOT` and `COEFFT` (settles former question 7).

## Questions for the experts

1. **Results that are thrown away.** `SCEN` is computed as the envelope's mean entropy and then set to 0 in both branches; `SACC2` is computed and not used (the lines using it are commented out); `LAlFail` from `ALSURFP` is not checked. What is the intended state?
2. **Allard atmospheres only.** `ALSURFP` is called whatever atmosphere the run uses. Should the routine check the atmosphere choice, or stop otherwise?
3. **Units of the Reimers rate (apparent bug).** `CREIM` multiplies $L/(gR) = LR/(GM)$ in cgs, which is in g/s: for the Sun $L_\odot R_\odot/(GM_\odot) \approx 2.0\times10^{18}$ g/s. `MDOT` reads the result as $M_\odot$/yr. With the default `CREIM` = −4e−13 (Reimers' coefficient for $L$, $R$, $M$ in solar units and $\dot M$ in $M_\odot$/yr), the Sun would lose about $8\times10^{5}\,M_\odot$/yr. Should $L$, $R$, $M$ be in solar units here, or `CREIM` include the conversion?
4. **A debug line.** The unconditional `WRITE(*,*) TAUCZ/CSECYR, RTOT/CRSUN` looks like debugging output.
5. **Arguments with no effect.** `MDOT` never uses the `RMU` it receives (it recomputes it at `JENV`), and uses `EACC` and `ETHAV` only for `ETHNEW` and `FAC`, which it does not use. For a loss the three are stale values from an earlier call (`SAVE`), or undefined on a first call. Can they be dropped from the interface?

### MASSLOSS

Sets $\dot M$ (constant or Reimers), computes the accretion energetics and entropies, and calls `MDOT` (above).
