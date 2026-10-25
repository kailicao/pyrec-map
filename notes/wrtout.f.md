## Explanation

**Purpose.** `WRTOUT` writes the output of each converged model: a summary block in the short output, one line (or block) per model in the track file, a line in the isochrone file, the last model for restarting, and, at the chosen intervals, the detailed profiles (through `PUTSTORE`, `WRTMOD`, `STITCH`). On the way it computes the summary quantities: convection-zone masses and the zone's base, the central conditions, the radius and gravity, neutrino capture rates, moments of inertia and rotation period.

**How it fits.**
- **Inputs:** the model and its run data through arguments (from the main program), and through COMMON blocks: the per-shell physics (`SCRTCH`), the neutrino fluxes (`FLUXES`, from [[engeb.f#ENGEB|ENGEB]]), the output switches (`CCOUT`, `CCOUT1`, `CCOUT2`, `CHRONE`, `TRACK`, `PULSE`, `ACDPTH`), the rotation totals and velocities (`ROT`, `TEMP2`, `ROTEN`), $\tau_\mathrm{cz}$ and $P_\mathrm{phot}$ (`OVRTRN`).
- **Who calls it:** the main program, [[main.f#(file level)|main.f]], after each model.
- **What it calls:** [[meqos.f#MEQOS|MEQOS]] or [[eqstat.f#EQSTAT|EQSTAT]] (central conditions), [[gettau.f#GETTAU|GETTAU]] (track version 0), [[wrtlst.f#WRTLST|WRTLST]] (the last model, `ILAST`; also `IJLAST`), [[putstore.f#PUTSTORE|PUTSTORE]], [[wrtmil.f#WRTMIL|WRTMIL]], [[wrtmod.f#WRTMOD|WRTMOD]], [[calcad.f#CALCAD|CALCAD]] (acoustic depths) and [[stitch.f#STITCH|STITCH]].
- **Outputs:** `ISHORT` (summary block), `ITRACK` (track; the header comes from [[wrthead.f#WRTHEAD|WRTHEAD]]), `IISO` (isochrone line), and the files written by the routines it calls. In COMMON `CENT`, it stores $\log T_c$, $\log P_c$, $\log\rho_c$ and the convection zone's base (`ENVLM`, `ENVR`), read by [[wrtmonte.f#WRTMONTE|WRTMONTE]]; in `FLUXES`, the Cl and Ga rates `CLSNU`, `GASNU`; in `OVRTRN`, `TAUCZ0` and `PPHOT0`.

**The method.**
1. **Luminosity terms** `TLUMX` (pp I–III, CNO, triple-α, He–C, gravity, neutrinos) are rescaled so that they sum to the surface luminosity (not during the helium flash).
2. **Radius and gravity:** $\log R = \tfrac12(\log L + \log L_\odot - \log 4\pi - \log\sigma - 4\log T_\mathrm{eff})$, $\log g = \log G + \log M - 2\log R$; $M_\mathrm{bol} = $ `CMBOL` $- 2.5\log(L/L_\odot)$.
3. **Central conditions**, extrapolated from shell 1 (mass $m_1$, radius $r_1$ from $m_1 = \tfrac{4\pi}{3}\rho_1 r_1^3$):
   $$P_c = P_1 + \tfrac12\,\frac{G m_1 \rho_1}{r_1},\qquad \log T_c = \log T_1 + \log\!\left(1 + \nabla_1\,\frac{P_c - P_1}{P_1}\right),$$
   then the equation of state gives $\beta$, $\eta$ there.
4. **Base of the surface convection zone:** where $\nabla_\mathrm{rad} - \nabla_\mathrm{ad}$ (`SDEL(1)` − `SDEL(3)`) changes sign between shells `JENV-1` and `JENV`, by linear interpolation; its mass above (`ENVLM`, $M_\odot$), radius ($R_\odot$), $T$, $\rho$, $P$, $\kappa$.
5. **Hydrogen shell** (`LSHELL`): masses at its middle, its total and the helium core's, and the temperature maximum (for the helium flash, the first maximum above $\log T = 7.98$).
6. **Neutrino detectors:** capture rates as linear combinations of the eight fluxes (pp, pep, hep, $^7$Be, $^8$B, $^{13}$N, $^{15}$O, $^{17}$F) with cross sections (from Bahcall's book, p. 207, table 8.2, by the comment) for $^7$Li, $^{37}$Cl, $^{71}$Ga, $^{81}$Br, $^{98}$Mo, $^{115}$In; and for the track, Cl and Ga in SNU with a second table (`CLSNUF`, `GASNUF`, "Neutrino Astrophysics p. 207", with $^{37}$Cl changes after Bahcall & Pinsonneault).
7. **Track** (`LTRACK`): the total moment of inertia (with rotation $\sum I_j$, otherwise $\sum \tfrac23 \Delta m_j r_j^2$), the surface zone's, the rotation period $P = 2\pi/\Omega_s$ in days and $v = \Omega_s R$ in km/s; then, by `ITRVER`, one line per model (0, after calling `GETTAU` for $\tau_\mathrm{cz}$ and $P_\mathrm{phot}$), or several lines (1, 2), or a short line (3).
8. **Isochrone line** (`LISO`): age in years, $L$ (erg/s), $R$ (cm), $T_\mathrm{eff}$, $g$, $Y_c$, and the helium core's mass in grams.
9. **Model files:** the last model to `ILAST` every time; the detailed output through `PUTSTORE` every `NPRTMOD` models if `LSTORE`; otherwise, with `LPULSE`, `WRTMIL` and `WRTMOD`; with `LACOUT`, acoustic depths through `CALCAD` and a second track line (format 1800); with `LSTCH`, the stitched profile.

**KC's changes.** Removed the unused argument `NKK` (2025-05-31), and adjusted the calls to `MEQOS`, `GETTAU`, `CALCAD` and `WRTMOD` to their shorter argument lists (2025-05-31); reordered the elements of COMMON `ACDPTH` (2025-05-30).

## Questions for the experts

1. **The convective core's radius.** `FX2 = (SDEL(3,JCORE+1)-SDEL(1,JCORE))/(SDEL(3,JCORE+1)-SDEL(1,JCORE))` is always 1 (or 0/0), and the next line uses `FX`, not `FX2`, which at that point is undefined or left from the previous model. `CORER` is then never used. Is this block (JVS 10/11) unfinished?
2. **Two tables of cross sections.** The $^{37}$Cl rate printed in the summary uses 1.09×10⁴ for $^8$B (`FL37CL`), the track's `CLSNU` 1.14×10⁴; the Ga values differ too (for example $^7$Be: 73.2 against 71.7). Which are current? And the summary line calls these rates "neutrino energies (1.E-36 erg)".
3. **Stale values in the track.** For `ITRVER` 1 and 2, `ROTP`, `ROTV` and `HICZ` are set only with rotation, but version 2 writes them always; `CLSNU` and `GASNU` in the `LACOUT` line (format 1800) are computed only when `LTRACK` is on; `ENVRL`, passed to `CALCAD`, is set only when the base of the convection zone is inside the model. Without these, the values come from earlier models.
4. **Two line formats in one track file.** With `LACOUT` and `ITRVER = 0`, each model writes a format-1499 line and a format-1800 line to `ITRACK`, with different columns (1800 has acoustic quantities in place of rotation ones, and `ICHECK`). Is the acoustic line meant for a separate file?
5. **`KSAHA` undefined.** The call to `EQSTAT` for the central conditions passes `KSAHA`, never set here.
6. **`FLUXTOT` zeroed.** For `ITRVER = 0` without `LSNU`, the fluxes in COMMON `FLUXES` are set to zero, which changes what later routines (such as `WRTMONTE`) read.
7. **Hard-coded values.** The helium flash's temperature threshold ($\log T = 7.98$), and the period's old cap of 9999 days still applied in version 0 (removed in version 1, MHP 8/25).
8. **Unused variable.** `LTSCAL` is set and never used.

### WRTOUT

All per-model output: summary, track and isochrone lines, the last model, and the detailed profiles at intervals; with the central conditions, the convection zone's base and the neutrino capture rates computed on the way.
