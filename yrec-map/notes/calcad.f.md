## Explanation

**Purpose.** This file computes acoustic depths: the sound travel time from the surface to the center, $t_\mathrm{norm}$, and from the surface to the base of the convection zone, $t_\mathrm{CZ}$. It joins the interior model and a fresh envelope integration into one profile, computes the sound speed at each point from the equation of state, and integrates $dr/c_s$.

**How it fits.**
- **Inputs:** the arguments, the interior model `HR`, `HD`, `HP`, `HT` ($\log r$, $\log\rho$, $\log P$, $\log T$), `HCOMP` (composition), `M` (last interior point), `JENV` (the base of the convection zone), `RCZL` ($\log r_\mathrm{CZ}/R_\odot$), `BL`, `TEFFL`, `FP`, `FT`, `HSTOT`, `DAGE` (the age), `CMIXL` (the mixing length, passed on to ENVINT).
- **Who calls it:** [[wrtout.f#WRTOUT|WRTOUT]], when the options `LACOUT` and `LADON` are on and the model has a convective envelope (`JENV > 1`).
- **What it calls:** [[envint.f#ENVINT|ENVINT]] (the envelope, which fills `/ENVSTRUCT/`); for the sound speed, [[esac06.f#ESAC06|ESAC06]] (OPAL 2006 EOS) or [[eqstat2.f#EQSTAT2|EQSTAT2]]; [[splinj.f#SPLINJ|SPLINJ]] and [[splint.f#SPLINT|SPLINT]] to interpolate at $r_\mathrm{CZ}$; [[boole.f#BOOLE|BOOLE]] to integrate.
- **Outputs:** in `/ACDPTH/`, `TNORM`, `TCZ`, `TAUCZN` $= t_\mathrm{CZ}/t_\mathrm{norm}$, `TATMOS` (always 0, see below) and `DELADJ` ($\nabla_\mathrm{ad}$ at each point). WRTOUT prints them in its output columns (its comment: columns 68–70). A line to `ISHORT` at every call; with `LCLCD`, the full profile to unit `ICLCD`.
- **Modules:** [[acdpth_mod.f#ACDPTH_MOD|`ACDPTH_MOD`]] (with ENVINT, [[getopal95.f#GETOPAL95|GETOPAL95]], the main program, PARMIN, WRTOUT; it also holds the output switches `LCLCD`, `LADON`, `LACOUT`); [[envstruct_mod.f#ENVSTRUCT_MOD|`ENVSTRUCT_MOD`]] (the envelope profile, filled by ENVINT); [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] (the integration step sizes `ATMBEG` … `ENVMAX` and `ATMSTP`, `ENVSTP`, the spot parameters `SPOTF`, `SPOTX`, and the switch `LOPALE06`); [[eos06misc_mod.f#EOS06MISC_MOD|`EOS06MISC_MOD`]] (ESAC06's output `EOS`); `COMP_MOD`, `CONSTANTS_MOD`, `IOUNITS_MOD` (the units `ISHORT`, `ICLCD`) and `DIMENSIONS_MOD`.

**The method.**
1. **The envelope.** Set the atmosphere and envelope step sizes to the fixed values `ATMSTP`, `ENVSTP`, then integrate the envelope with [[envint.f#ENVINT|ENVINT]] (with the model's mixing length `CMIXL`), from the surface to the interior's outer point, with
$$\log R = \tfrac12(\log L - \log 4\pi - \log\sigma - 4\log T_\mathrm{eff}), \qquad \log g = \log G + \log M - 2\log R.$$
For a spotted star (`SPOTF` $\ne 0$, `SPOTX` $\ne 1$) and only when `JENV = M`, the envelope uses the ambient temperature
$$\log T_\mathrm{amb} = \log T_\mathrm{eff} - \tfrac14\log_{10}\!\left(f_s x_s^4 + 1 - f_s\right),$$
with $f_s$ = `SPOTF` (the spot filling factor) and $x_s$ = `SPOTX` (probably the spot-to-ambient temperature ratio).
2. **One profile.** The interior points $1..M$, then envelope points $2..N_\mathrm{env}$, in linear units, $T$ in $10^6$ K.
3. **Sound speed.** With the OPAL 2006 EOS, $\Gamma_1$ = `EOS(8)` and $\nabla_\mathrm{ad} = 1/$`EOS(9)` (`EOS(9)` is $\Gamma_2/(\Gamma_2-1)$). Otherwise, from EQSTAT2's derivatives (`QDPJ`, `QDTJ`, probably $(\partial\ln\rho/\partial\ln P)_T$ and $(\partial\ln\rho/\partial\ln T)_P$) and $c_P$, by Cox and Giuli's chapter 9:
$$\chi_\rho = \frac{1}{\mathtt{QDP}}, \quad \chi_T = -\chi_\rho\,\mathtt{QDT}, \quad c_V = c_P - \frac{P}{\rho T}\frac{\chi_T^2}{\chi_\rho}, \quad \Gamma_1 = \frac{\chi_\rho\,c_P}{c_V}.$$
The code stores the inverse sound speed $1/c_s$, with $c_s = \sqrt{\Gamma_1 P/\rho}$.
4. **Integrate** with Boole's rule:
$$t_\mathrm{norm} = \int_0^{R} \frac{dr}{c_s}, \qquad t_\mathrm{CZ} = \int_{r_\mathrm{CZ}}^{R} \frac{dr}{c_s},$$
in seconds. For $t_\mathrm{CZ}$, the point just below $r_\mathrm{CZ}$ is replaced by $r_\mathrm{CZ}$ itself, with $1/c_s$ from a cubic spline through 7 neighboring points.
5. $\tau_\mathrm{CZ,n} = t_\mathrm{CZ}/t_\mathrm{norm}$.

The atmosphere's acoustic depth (`TATMOS`) was computed by a section now commented out, so it is always 0.

**Design.** The header lists `IACAT`, `IJLAST` and other output switches, some marked "obsolete?" (`IACAT` and the other unused unit numbers are no longer in the module). Many local variables and arrays remain from the commented-out sections.

**KC's changes.** 2025-05-30: elements of `/ACDPTH/` and `/OPALEOS/` reordered; integer declarations and two `WRITE` statements fixed for compiler warnings (from `Makefile.legacy`). 2025-05-31: the unused arguments `LPRT`, `NKK`, `DDAGE` removed, and `ZTAB` removed from the call to ESAC06.

**Changed since `rp_1`.** The new argument `CMIXL`, passed on to ENVINT; otherwise declarations only: COMMON blocks to modules, `IMPLICIT NONE`, unused blocks removed (among them a wrong `/LLOT95/` declaration that aliased `ZTAB` to an opacity value, harmless since nothing here reads it).

## Questions for the experts

1. **Step sizes not restored.** The routine saves `ATMBEG`, `ATMMIN`, `ATMMAX`, `ENVBEG`, `ENVMIN`, `ENVMAX` in `ABEG0` … `EMAX0`, sets them to `ATMSTP`/`ENVSTP` for its own envelope integration, and never restores them. Later envelope integrations in the same run then use the fixed steps. [[wrtmod.f#WRTMOD|WRTMOD]], whose code the comment says CALCAD copied, does restore them (`ATMBEG = ABEG0`, …). Is a restore missing at the end?
2. **The last point.** `K = M + NUMENV - 2` is passed to BOOLE as the number of points, but the profile has $M + N_\mathrm{env} - 1$ points, so the outermost point is left out of both integrals. Is this intended (the surface point having $c_s$ ill-defined)?
3. **The interior's $Z$.** `STARZ(I) = HCOMP(3,M)` for every interior point: the envelope's $Z$, not the local one. It is used only on the non-OPAL path (EQSTAT2). With diffusion, the interior $Z$ differs.
4. **EOS errors ignored.** ESAC06's alternate return `*999` jumps to the next statement, so a failed EOS call uses the `EOS` values of the previous point.
5. **`ICZ` may be stale.** If no pair of points brackets $r_\mathrm{CZ}$, `ICZ` keeps its value from an earlier call (`SAVE`), or is undefined at the first call. Also the 7-point stencil `ICZ-3 … ICZ+3` is not checked against the end of the profile.
6. **A short profile.** If `K ≤ 3`, `NN = 2` and BOOLE returns 0, so `TAUCZN` divides by zero.
7. **Spots only at `JENV = M`.** The ambient temperature is used only when `JENV = M`, which is also exactly the case in which no convection zone is found (`TCZ` needs `JENV < M`), so the spot correction applies only to stars for which `TCZ = 0`. Why that condition?
8. **Output format.** Format 67 has no space before "Acoustic depth of atmopshere" (also misspelled), and `TATMOS` is always 0. Should the atmosphere part be restored or removed?

### CALCAD

Integrates the envelope, joins it to the interior, computes $1/c_s$ from the EOS and integrates it with [[boole.f#BOOLE|BOOLE]] to get the acoustic depth of the star and of its convection zone (`TNORM`, `TCZ`, `TAUCZN` in `/ACDPTH/`).
