## Explanation

**Purpose.** `STITCH` writes one model's full profile to the `.store` file, in an alternative format (JvS 08/25): the interior shells, then, if asked, the envelope and atmosphere "stitched" onto them, one line per point with 61 columns. Its comment lists the columns: model, shell, $\log m$ [g], $\log r$ [cm], $L/L_\odot$, $\log P$, $\log T$, $\log\rho$, $\Omega$ [rad/s], three flags for the point's kind, the 15 mass fractions, the opacity, gravity, the three temperature gradients, the convective velocity, $\Gamma_1$, ionisation fractions, $\beta$, $\eta$, the energy rates of each burning chain, neutrino and gravitational energy, $c_P$, $d\ln\rho/d\ln T$, and the rotation columns (51–61).

**How it fits.**
- **Inputs:** the model through the arguments (and the mixing length `CMIXL`, passed on to `ENVINT`), and the per-shell physics left in modules by earlier routines: [[scrtch_mod.f|`SCRTCH_MOD`]] (opacity `SO`, gradients `SDEL`, `SVEL`, ionisation `SFXION`, $\eta$ `SETA`, energy rates `SEG` and `SESUM`, `SCP`; filled by the physics routines such as [[physic.f#PHYSIC|PHYSIC]]), [[sound_mod.f|`SOUND_MOD`]] (`GAM1`), [[pulse1_mod.f|`PULSE1_MOD`]] (`PQDT`), [[roten_mod.f|`ROTEN_MOD`]] (`DEROT`) and [[temp2_mod.f|`TEMP2_MOD`]] (the circulation velocities `VES`, `VGSF`, `VSS`, written by [[vcirc.f#VCIRC|VCIRC]] among others).
- **Who calls it:** [[putstore.f#PUTSTORE|PUTSTORE]], and [[wrtout.f#WRTOUT|WRTOUT]] every `NPRTMOD` models when `LSTCH` is set.
- **What it calls:** [[envint.f#ENVINT|ENVINT]], to integrate the envelope (and atmosphere) again for output.
- **Output:** lines on the unit `ISTOR` ([[iounits_mod.f|`IOUNITS_MOD`]]).
- **Modules:** besides those above, [[envstruct_mod.f|`ENVSTRUCT_MOD`]] and [[atmstruct_mod.f|`ATMSTRUCT_MOD`]] (the envelope's and atmosphere's points, filled by `ENVINT`), [[nmlpar_mod.f|`NMLPAR_MOD`]] (the output steps `ATMSTP`, `ENVSTP`, the integration steps `ATMBEG` … `ENVMAX`, the switches `LSTENV`, `LSTATM`, the spot parameters and `LROT`), [[constants_mod.f|`CONSTANTS_MOD`]], `JSON` from [[dimensions_mod.f|`DIMENSIONS_MOD`]].

**The method.**
1. **Interior** (shells 1 to $M$): the gravity $g = G m / r^2$, and, with rotation, the shape quantities
   $$A = \frac{\Omega^2 r_0^3}{3\,G m}\,\frac{5}{2 + \eta_2},\qquad \frac{R_p}{R_e} = \frac{1 - A}{1 + A/2},$$
   with $r_0$ (`R0`) and $\eta_2$ (`ETA2`) from the rotation routines, and the total circulation velocity `VTOT = VES + VGSF + VSS`. Without rotation the 11 rotation columns are zeros.
2. **Envelope** (`LSTENV`): the integration steps are set to the fixed output steps `ATMSTP`, `ENVSTP` ("dropping a sinkline"), and `ENVINT` integrates from the surface, at $\log R = \tfrac12(\log L + \log L_\odot - 4\log T_\mathrm{eff} - \log 4\pi - \log\sigma)$ and $\log g = \log G + \log M - 2\log R$, down to the pressure of the last interior shell; for a spotted star at the ambient temperature (the formula in [[starin.f|starin.f]]). The envelope points get shell numbers $M+1, \dots$; $\Omega$ and the composition are those of the last interior shell; the burning and rotation columns are zero.
3. **Atmosphere** (`LSTATM`): the atmosphere's points, outermost last, with $r = R_\mathrm{env} + $ `ATMOR`, the total mass and the surface luminosity.

**Changed since `rp_1`.** COMMON blocks to modules, `IMPLICIT NONE` (the unused `OVRTRN` dropped); a new argument `CMIXL`, passed on to `ENVINT`; the formats of the lines (62, 63) now put a blank between the $\log P$, $\log T$, $\log\rho$ columns and between the six `F9.5` columns ($\Gamma_1$ to $\eta$), so that neighbouring values no longer run together.

## Questions for the experts

1. **The integration steps are not restored.** `STITCH` saves `ATMBEG`, `ATMMIN`, `ATMMAX`, `ENVBEG`, `ENVMIN`, `ENVMAX` into `ABEG0` … `EMAX0` and sets them to the output steps, but never restores them, so every later envelope integration of the run uses the output steps. ([[calcad.f#CALCAD|CALCAD]] does the same; [[starin.f#STARIN|STARIN]], [[wrtmod.f#WRTMOD|WRTMOD]] and [[getnewenv.f#GETNEWENV|GETNEWENV]] restore the steps they change.) Intended?
2. **β of the interior from the envelope's array.** Column 39 (BETA) for interior shell $I$ is `EBETAS(I)`, the envelope's array, while `SBETA(I)` in `SCRTCH` seems to be the interior's. A bug?
3. **`LPULPT` undefined.** `LPULPT` is passed to `ENVINT` but never set in `STITCH` (`CALCAD` sets its own to true). Is a value expected?
4. **Gravity of the atmosphere.** The atmosphere's lines write `SG`, which is left from the last envelope point (or interior shell when there is no envelope), not computed for each atmosphere point.
5. **Atmosphere without envelope.** With `LSTATM` but not `LSTENV`, the atmosphere's points are numbered and placed using `NUMENV` and `ENVR(NUMENV)` from whatever envelope integration ran last. And the atmosphere's luminosity column writes `B`, which is set (`B = DEXP(CLN*BL)`) only in the envelope branch, so it holds a value from an earlier call, or is undefined. Should the atmosphere require the envelope?
6. **Spot test.** The spotted-star branch tests `LC(M)` (the last shell convective), while [[starin.f#STARIN|STARIN]] and `CALCAD` test `JENV.EQ.M`. Same intent?

### STITCH

Writes one model's interior, envelope and atmosphere to `ISTOR` in the 61-column `.store` format, integrating the envelope again with `ENVINT` at fixed output steps.
