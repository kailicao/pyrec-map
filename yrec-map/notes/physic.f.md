## Explanation

**Purpose.** Recomputes the auxiliary physics at every shell of a model: equation of state, opacity, temperature gradients and convection, mean molecular weight, then the thermal diffusivity and viscosity, and the largest angular velocity gradient that is stable against the shear instability. Its comment: "find actual and adiabatic temperature gradients, opacity, and mean molecular weight for all radiative shells" (the loop in fact covers all shells).

**The loop covers all shells.** The comment speaks of "ALL RADIATIVE SHELLS" ([lines 81–82](https://github.com/yreclab/yrec/blob/7be4133/src/physic.f#L81-L82)), but the loop `DO 30 IM = 1,M` ([line 86](https://github.com/yreclab/yrec/blob/7be4133/src/physic.f#L86)) skips no shell, convective ones included, so the comment could say "all shells."

**How it fits.**
- **Inputs:** the model (`HCOMP`, `HD`, `HG` (gravity), `HL`, `HP`, `HR`, `HS`, `HT`, all logarithmic except `HL`, `HG` and `HCOMP`), the rotational distortion factors `FP`, `FT`, `M`, `TEFFL` and the mixing length `CMIXL` (a new argument, formerly in `/CONST3/`), passed on to `TPGRAD`; the envelope composition from `COMP_MOD` and `COMP2_MOD`; the switch `LDH` (`NMLPAR_MOD`), with the Debye–Hückel abundances it sets in `DEBHU_MOD`; `CLN` from `CONSTANTS_MOD`.
- **Who calls it:** [GETW](getw.f.md#getw), [HPOINT](hpoint.f.md#hpoint) and [STARIN](starin.f.md#starin).
- **What it calls:** [EQSTAT](eqstat.f.md#eqstat) (the general equation of state), [GETOPAC](getopac.f.md#getopac), [TPGRAD](tpgrad.f.md#tpgrad) (gradients and convective velocity), [VISCOS](viscos.f.md#viscos), and [INTRP2](intrp2.f.md#intrp2).
- **Outputs (all through modules, except `LC`):**
  - `LC`, the convection flags (argument), overwritten from `TPGRAD` at every shell ([line 116](https://github.com/yreclab/yrec/blob/7be4133/src/physic.f#L116)). All three callers use the new flags right after the call (settled from the code, Nov 9, 2026): HPOINT calls PHYSIC, as its comment says, "to accurately locate the edges of convection zones" ([hpoint.f, lines 830–834](https://github.com/yreclab/yrec/blob/7be4133/src/hpoint.f#L830-L834)); STARIN passes `LC` to `OVROT` ([starin.f, lines 1031–1033](https://github.com/yreclab/yrec/blob/7be4133/src/starin.f#L1031-L1033)) and GETW to `GETTAU` ([getw.f, lines 240–244](https://github.com/yreclab/yrec/blob/7be4133/src/getw.f#L240-L244));
  - `SCRTCH_MOD`: `SDEL(1..3,·)` $`= \nabla_\mathrm{rad}, \nabla, \nabla_\mathrm{ad}`$, the opacity `SO`, the convective velocity `SVEL`;
  - `TEMP_MOD`: `CP`, `HAMU` (the mean molecular weight), `SQDT` ($`(\partial\ln\rho/\partial\ln T)_P`$), and through `VISCOS` `THDIF` and `VISC`;
  - `DWMAX_MOD`: `QWRMAX`, the critical $`d\Omega/d\ln r`$, which only HPOINT reads, to copy it into `QWRMX0`, which nothing reads ([hpoint.f, line 855](https://github.com/yreclab/yrec/blob/7be4133/src/hpoint.f#L855); unused?);
  - `DPMIX_MOD`: `IOVIM`, the current shell, for `TPGRAD`.
  These feed the rotational mixing and transport routines ([MIDMOD](midmod.f.md#midmod) interpolates them in time), and [MICRODIFF_MTE](microdiff_mte.f.md#microdiff_mte) (for microscopic diffusion) reads `SDEL(2,·)`.

**The method.**
1. **Per shell:** the equation of state, always `EQSTAT` (with Debye–Hückel abundances set first when `LDH`), the opacity, and `TPGRAD`, without derivatives (`LDERIV = .FALSE.`). The flag `LOCOND` is set to false and never read (unused?, [line 84](https://github.com/yreclab/yrec/blob/7be4133/src/physic.f#L84)); the counter of Saha-equation calls `KSAHA`, which EQSTAT updates, is never initialized or read here (unused?, [lines 108–110](https://github.com/yreclab/yrec/blob/7be4133/src/physic.f#L108-L110)).
2. **Mean molecular weight** of a fully ionized gas. With $`A`$ = 1.007825, 4.002603, 12 and 3.01603 for H, $`^4\mathrm{He}`$, the metals (as carbon) and $`^3\mathrm{He}`$,
   
   $$\displaystyle \frac{1}{\mu\_\mathrm{ion}} = \frac{1}{\mu\_\mathrm{ion,env}} + \sum\_k \frac{X\_k - X\_{k,\mathrm{env}}}{A\_k},\qquad \frac{1}{\mu\_e} = \frac{X}{A\_\mathrm{H}} + 2\left(\frac{X\_{^3\mathrm{He}}}{A\_{^3\mathrm{He}}} + \frac{Y}{A\_{^4\mathrm{He}}}\right) + \frac{Z}{2},\qquad \mu = \frac{\mu\_\mathrm{ion}\\,\mu\_e}{\mu\_\mathrm{ion}+\mu\_e}.$$
3. **Shear stability** (Endal & Sofia [1978](https://ui.adsabs.harvard.edu/abs/1978ApJ...220..279E), ApJ 220, 279, as cited). At each interface between shells, with $`\rho`$, $`P`$, $`\nabla`$, $`\nabla_\mathrm{ad}`$ and $`g`$ interpolated to the midpoint in $`\log m`$ (four-point Lagrange),
   
   $$\displaystyle \left(\frac{d\Omega}{d\ln r}\right)\_\mathrm{max} = 2\sqrt{\frac{\rho}{P}\\,g^2\\,(\nabla\_\mathrm{ad} - \nabla)}$$
   
   where the root is real, and 0 otherwise. `QWRMAX(IM)` belongs to the interface between shells `IM-1` and `IM`; it is 0 where both shells are convective, and `QWRMAX(1)` is never set. $`\rho`$ and $`P`$ are interpolated in their logarithms (`HD`, `HP`), $`g`$ (`HG`, not logarithmic) and the gradients directly.

**Changed since `rp_1`.** The MHD equation of state is removed (`LMHD` and the call to `MEQOS`, removed since `rp_1`), so every shell uses `EQSTAT`; the mixing length `CMIXL` is a new argument, passed to `TPGRAD`; the write-only `/OPTAB/` settings (`IDT = 15`, `IDD = 5`) are gone; COMMON blocks to modules, `IMPLICIT NONE`. No question is settled.
