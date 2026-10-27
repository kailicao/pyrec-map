## Explanation

**Purpose.** Recomputes the auxiliary physics at every shell of a model: equation of state, opacity, temperature gradients and convection, mean molecular weight, then the thermal diffusivity and viscosity, and the largest angular velocity gradient that is stable against the shear instability. Its comment: "find actual and adiabatic temperature gradients, opacity, and mean molecular weight for all radiative shells" (the loop in fact covers all shells).

**How it fits.**
- **Inputs:** the model (`HCOMP`, `HD`, `HG` (gravity), `HL`, `HP`, `HR`, `HS`, `HT`, all logarithmic except `HL`, `HG` and `HCOMP`), the rotational distortion factors `FP`, `FT`, `M`, `TEFFL` and the mixing length `CMIXL` (a new argument, formerly in `/CONST3/`), passed on to `TPGRAD`; the envelope composition from `COMP_MOD` and `COMP2_MOD`; the switch `LDH` (`NMLPAR_MOD`), with the Debye–Hückel abundances it sets in `DEBHU_MOD`; `CLN` from `CONSTANTS_MOD`.
- **Who calls it:** [[getw.f#GETW|GETW]], [[hpoint.f#HPOINT|HPOINT]] and [[starin.f#STARIN|STARIN]].
- **What it calls:** [[eqstat.f#EQSTAT|EQSTAT]] (the general equation of state), [[getopac.f#GETOPAC|GETOPAC]], [[tpgrad.f#TPGRAD|TPGRAD]] (gradients and convective velocity), [[viscos.f#VISCOS|VISCOS]], and [[intrp2.f#INTRP2|INTRP2]].
- **Outputs (all through modules, except `LC`):**
  - `LC`, the convection flags (argument);
  - `SCRTCH_MOD`: `SDEL(1..3,·)` $= \nabla_\mathrm{rad}, \nabla, \nabla_\mathrm{ad}$, the opacity `SO`, the convective velocity `SVEL`;
  - `TEMP_MOD`: `CP`, `HAMU` (the mean molecular weight), `SQDT` ($(\partial\ln\rho/\partial\ln T)_P$), and through `VISCOS` `THDIF` and `VISC`;
  - `DWMAX_MOD`: `QWRMAX`, the critical $d\Omega/d\ln r$;
  - `DPMIX_MOD`: `IOVIM`, the current shell, for `TPGRAD`.
  These feed the rotational mixing and transport routines ([[midmod.f#MIDMOD|MIDMOD]] interpolates them in time), and [[microdiff_mte.f#MICRODIFF_MTE|MICRODIFF_MTE]] (for microscopic diffusion) reads `SDEL(2,·)`.

**The method.**
1. **Per shell:** the equation of state, always `EQSTAT` (with Debye–Hückel abundances set first when `LDH`), the opacity, and `TPGRAD`, without derivatives (`LDERIV = .FALSE.`).
2. **Mean molecular weight** of a fully ionized gas. With $A$ = 1.007825, 4.002603, 12 and 3.01603 for H, ⁴He, the metals (as carbon) and ³He,
$$\frac{1}{\mu_\mathrm{ion}} = \frac{1}{\mu_\mathrm{ion,env}} + \sum_k \frac{X_k - X_{k,\mathrm{env}}}{A_k},\qquad \frac{1}{\mu_e} = \frac{X}{A_\mathrm{H}} + 2\left(\frac{X_{^3\mathrm{He}}}{A_{^3\mathrm{He}}} + \frac{Y}{A_{^4\mathrm{He}}}\right) + \frac{Z}{2},\qquad \mu = \frac{\mu_\mathrm{ion}\,\mu_e}{\mu_\mathrm{ion}+\mu_e}.$$
3. **Shear stability** (Endal & Sofia 1978, ApJ 220, 279, as cited). At each interface between shells, with $\rho$, $P$, $\nabla$, $\nabla_\mathrm{ad}$ and $g$ interpolated to the midpoint in $\log m$ (four-point Lagrange),
$$\left(\frac{d\Omega}{d\ln r}\right)_\mathrm{max} = 2\sqrt{\frac{\rho}{P}\,g^2\,(\nabla_\mathrm{ad} - \nabla)}$$
where the root is real, and 0 otherwise. `QWRMAX(IM)` belongs to the interface between shells `IM-1` and `IM`; it is 0 where both shells are convective, and `QWRMAX(1)` is never set. $\rho$ and $P$ are interpolated in their logarithms (`HD`, `HP`), $g$ (`HG`, not logarithmic) and the gradients directly.

**Changed since `rp_1`.** The MHD equation of state is removed (`LMHD` and the call to `MEQOS`, removed since `rp_1`), so every shell uses `EQSTAT`; the mixing length `CMIXL` is a new argument, passed to `TPGRAD`; the write-only `/OPTAB/` settings (`IDT = 15`, `IDD = 5`) are gone; COMMON blocks to modules, `IMPLICIT NONE`. No question is settled.

**KC's changes.** 2025-05-31: the unused argument `LCZ` removed, and unused arguments removed from the calls to `MEQOS` and `VISCOS`.

## Questions for the experts

1. **`LC` overwritten.** `PHYSIC` resets the caller's convection flags `LC` from `TPGRAD`. Do all three callers expect this?
2. **Unused or unset.** `DWMAX_MOD`'s `QWRMX0` and the flag `LOCOND` are not used here; `KSAHA`, which EQSTAT updates (a counter of Saha-equation calls), is never initialized here.
3. **The comment's "radiative shells".** The loop covers all shells, convective ones included. Update the comment?
