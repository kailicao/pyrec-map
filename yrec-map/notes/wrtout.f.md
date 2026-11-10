## Explanation

**Purpose.** `WRTOUT` writes the output of each converged model: a summary block in the short output, one line (or block) per model in the track file, the last model for restarting, and, at the chosen intervals, the detailed profiles (through `PUTSTORE`, which also calls `STITCH`, and `WRTMOD`). On the way it computes the summary quantities: convection-zone masses and the zone's base, the central conditions, the radius and gravity, neutrino capture rates, moments of inertia and rotation period.

**How it fits.**
- **Inputs:** the model and its run data through arguments (from the main program; `CMIXL`, `XMSOL` and `COMPMIX` are only passed on), and through modules: the per-shell physics (`SCRTCH_MOD`), the neutrino fluxes (`FLUXES_MOD`, from [[engeb.f#ENGEB|ENGEB]]), the output switches and options (`NMLPAR_MOD`: `LTRACK`, `ITRVER`, `LSTORE`, `NPRTMOD`, `LPULSE`, `LMILNE`, `LROT`, `LSNU`, `LKUTHE`; `ACDPTH_MOD`: `LACOUT`, `LADON`, `LJLAST`), the composition (`COMP_MOD`, `LABEL_MOD`), the constants (`CONSTANTS_MOD`), $\tau_\mathrm{cz}$ and $P_\mathrm{phot}$ (`OVRTRN_MOD`).
- **Who calls it:** the main program, [[main.f#(file level)|main.f]], after each model.
- **What it calls:** [[eqstat.f#EQSTAT|EQSTAT]] (central conditions), [[gettau.f#GETTAU|GETTAU]] (track version 0), [[wrtlst.f#WRTLST|WRTLST]] (the last model, `ILAST`; also `IJLAST`), [[putstore.f#PUTSTORE|PUTSTORE]], [[wrtmil.f#WRTMIL|WRTMIL]], [[wrtmod.f#WRTMOD|WRTMOD]] and [[calcad.f#CALCAD|CALCAD]] (acoustic depths).
- **Outputs:** `ISHORT` (summary block), `ITRACK` (track; the header comes from [[wrthead.f#WRTHEAD|WRTHEAD]]), and the files written by the routines it calls. In `CENT_MOD`, it stores $\log T_c$, $\log P_c$, $\log\rho_c$ and the convection zone's base (`CZsurf_M`, `CZsurf_R`, formerly `ENVLM`, `ENVR`), read by the main program for its `ISNU` output (WRTMONTE, which also read them, removed since `rp_1`); in `FLUXES_MOD`, the Cl and Ga rates `CLSNU`, `GASNU`; in `OVRTRN_MOD`, `TAUCZ0` and `PPHOT0`.

**The method.**
1. **Luminosity terms** `TLUMX` (pp I–III, CNO, triple-α, He–C, gravity, neutrinos) are rescaled so that they sum to the surface luminosity (not during the helium flash). The factor, $L$ divided by the unscaled sum, is not written out. (`LTSCAL`, set to false at [[#L176]], is never read: unused?)

    > **Question** ([[#L177-L185]]). **The unscaled luminosity sum.** The rescaling of `TLUMX` hides the mismatch between the sum of the sources and the surface luminosity. Is that mismatch the numerical error of the energy equation, or does it include terms the sum leaves out? How large is it typically, and could the factor be written to the track or the short output as a check of energy conservation?

2. **Radius and gravity:** $\log R = \tfrac12(\log L + \log L_\odot - \log 4\pi - \log\sigma - 4\log T_\mathrm{eff})$, $\log g = \log G + \log M - 2\log R$; $M_\mathrm{bol} = $ `CMBOL` $- 2.5\log(L/L_\odot)$. So $R$ is the radius that $L$ and $T_\mathrm{eff}$ define through $L = 4\pi R^2\sigma T_\mathrm{eff}^4$, not the outermost model point, which lies at the envelope's fitting point (`HR(M)`). $\log M$ here is `STOTAL`, the copy of `HSTOT` in `COMP_MOD`.

    > **Question** ([[#L223]]). **`CMBOL` = 4.79.** [[setups.f#SETUPS|SETUPS]] sets $M_{\mathrm{bol},\odot} = 4.79$; the IAU 2015 Resolution B2 nominal value is 4.74 (for $L_\odot = 3.828\times10^{33}$ erg/s), and with the code's own $L_\odot$ (`CLSUN` = $3.8515\times10^{33}$ erg/s) that zero point gives about 4.73. Is 4.79 an intended older convention, and should it follow the solar luminosity in use?

3. **Central conditions**, extrapolated from shell 1 (mass $m_1$, radius $r_1$ from $m_1 = \tfrac{4\pi}{3}\rho_1 r_1^3$):
   $$P_c = P_1 + \tfrac12\,\frac{G m_1 \rho_1}{r_1},\qquad \log T_c = \log T_1 + \log\!\left(1 + \nabla_1\,\frac{P_c - P_1}{P_1}\right),$$
   then the equation of state ([[eqstat.f#EQSTAT|EQSTAT]], with the Debye–Hückel composition set first when `LDH`) gives $\beta$, $\eta$ there. Its argument `KSAHA`, a counter that EQSAHA increments ([[eqsaha.f#L95]]), is passed unset; WRTOUT never reads it back, so its value does not matter (settled from the code, Nov 9, 2026: [[#L251-L253]]).
4. **Base of the surface convection zone:** where $\nabla_\mathrm{rad} - \nabla_\mathrm{ad}$ (`SDEL(1)` − `SDEL(3)`) changes sign between shells `JENV-1` and `JENV`, by linear interpolation; its mass above (`CZsurf_M`, $M_\odot$), radius (`CZsurf_R`, $R_\odot$), $T$, $\rho$, $P$, $\kappa$ (the locals `CZsurf_T`, `CZsurf_D`, `CZsurf_P`, `CZsurf_O`). The convective core's radius `CORER` (JVS 10/11, [[#L212-L221]]) is computed and never used (unused?, with `FX2` and `CORERL`): `FX2` is always 1 (or 0/0), and the radius is interpolated with `FX`, left at that point from the previous model's step 4.
5. **Hydrogen shell** (`LSHELL`): masses at its middle, its total and the helium core's, and the temperature maximum (for the helium flash, the first maximum above $\log T = 7.98$).

    > **Question** ([[#L382-L384]]). **The helium flash's threshold.** The temperature maximum during the helium flash is the first one above $\log T = 7.98$, a hard-coded value. Where does it come from, and should it be a setting?

6. **Neutrino detectors:** capture rates as linear combinations of the eight fluxes (pp, pep, hep, $^7$Be, $^8$B, $^{13}$N, $^{15}$O, $^{17}$F) with cross sections (from Bahcall's book, p. 207, table 8.2, by the comment) for $^7$Li, $^{37}$Cl, $^{71}$Ga, $^{81}$Br, $^{98}$Mo, $^{115}$In; and for the track, Cl and Ga in SNU with a second table (`CLSNUF`, `GASNUF`, "Neutrino Astrophysics p. 207," with $^{37}$Cl changes after Bahcall & Pinsonneault). The summary's labels give these rates and the fluxes in erg (bug 2).

    > **Question** ([[#L404-L413]]; [[#L165-L171]]). **Two tables of cross sections.** The $^{37}$Cl rate printed in the summary uses 1.09×10⁴ for $^8$B (`FL37CL`), the track's `CLSNU` 1.14×10⁴; the Ga values differ too (for example $^7$Be: 73.2 against 71.7). Which are current?

7. **Track** (`LTRACK`): the total moment of inertia (with rotation $\sum I_j$, otherwise $\sum \tfrac23 \Delta m_j r_j^2$), the surface zone's, the rotation period $P = 2\pi/\Omega_s$ in days and $v = \Omega_s R$ in km/s; then, by `ITRVER`, one line per model (0, after calling `GETTAU` for $\tau_\mathrm{cz}$ and $P_\mathrm{phot}$), or several lines (1, 2), or a short line (3). For version 0 without `LSNU`, the fluxes `FLUXTOT` are set to zero ([[#L459-L463]]); without `LSNU` they are never accumulated ([[coefft.f#L150-L155]]; [[coefft.f#L304-L309]]), and their other reader, the main program's `ISNU` output, runs only with `LSNU` ([[main.f#L1195]]), so this changes nothing read later (settled from the code, Nov 9, 2026). The headers that [[wrthead.f#WRTHEAD|WRTHEAD]] writes for versions 1–3 do not match these lines ([[wrthead.f#b1]]).

    > **Question** ([[#L470]]; [[#L596-L598]]). **The period's cap.** Version 0 still caps the rotation period at 9999 days, while versions 1 and 2 no longer do (MHP 8/25). Should version 0 follow?

8. **Model files:** the last model to `ILAST` every time; the detailed output through `PUTSTORE` every `NPRTMOD` models if `LSTORE` (with `LSTCH`, PUTSTORE also writes the stitched profile); otherwise, with `LPULSE`, `WRTMIL` and `WRTMOD`; with `LACOUT`, acoustic depths through `CALCAD` and a second track line (format 1800). `LACOUT` is in no namelist and nothing sets it, so this last branch never runs (see [[acdpth_mod.f#ACDPTH_MOD|`ACDPTH_MOD`]]).

    > **Question** ([[#L696-L725]]). **The acoustic-depth line.** If `LACOUT` is turned on, each model with `ITRVER = 0` writes a format-1499 line and a format-1800 line to `ITRACK`, with different columns (1800 has acoustic quantities in place of rotation ones, and `ICHECK`); the 1800 line writes `CLSNU`, `GASNU`, `SSS1`–`RRR3` and `TAUCZ`, which are set only with `LTRACK` ([[#L431-L644]]); and `CZsurf_RL`, passed to `CALCAD`, is set only when the base of the convection zone is inside the model ([[#L262-L278]]). Without these, the values come from earlier models. Is the acoustic line meant for a separate file, and should these values be computed for it?


**For users** (from YREC's [Quick Start](https://yrec.readthedocs.io/en/latest/quickstart.html), Understanding the output). The `.track` file is the run's history: one line per model of its global properties (age, luminosity, effective temperature, central temperature and pressure, and so on), not its interior structure, which goes to `.store`; `ITRVER` = 0, one line per model, is the format the test suite uses. The `.short` file holds the numerical details of each model (with `LRWSH`, the main program rewinds it so that only the last model's remain). The `.last` file, rewritten after every model, is the last converged model, readable by YREC as a starting model. The documentation's two deprecated outputs, `.full` and `.excomp`, are not written here: the light-element history that `.excomp` held is now in the track.

**From YREC's documentation.** [Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html) (Output): `NPRTMOD` writes the detailed structure every `NPRTMOD` models (negative: none of the intermediate ones, though the final model can still be written with `LSTPCH`); `LTRACK` writes the global properties to the `.track` file ("should almost always be on"); `ITRVER` chooses the track format, and the documentation strongly recommends 0 (one line per model), while the default is 1; `LRWSH` keeps only the last model's details in the `.short` file.

**Changed since `rp_1`.** The MHD equation of state removed (EQSTAT always); the isochrone output (`LISO`, unit `IISO`) removed; the call to STITCH removed, since PUTSTORE makes it (it ran twice per stored model); the new arguments `CMIXL`, `XMSOL` (formerly in `/CONST3/` and `/PULSE/`) and `COMPMIX` (formerly `/I2O/`), passed on to GETTAU, WRTLST, PUTSTORE, WRTMOD and CALCAD; `ENVLM`, `ENVR` renamed `CZsurf_M`, `CZsurf_R` (and the other `ENV…` locals `CZsurf_…`); the track's format 1499 writes `E17.8E3` in place of `E16.8`, for three-digit exponents (MCR 12/25); the commented-out JVS block on the zone outside the fitting point deleted; COMMON blocks to modules (many unused ones dropped), `IMPLICIT NONE`.

## Bugs, by priority

1. **(not reached)** **Track version 2 without rotation writes rotation values never set.** ([[#L594-L608]]; [[#L630-L634]]) In the branch for `ITRVER` 1 and 2, `ROTP`, `ROTV`, and `HICZ` are set only with `LROT`, but version 2 writes them always (format 1540). Without rotation they hold what an earlier call left, or, in a run that never set them, undefined values (zero with a compiler that zero-initializes `SAVE`d locals). `HICZ`, the surface zone's moment of inertia, is then not computed at all, while version 0 computes it without rotation ([[#L477-L485]]). Only with `ITRVER` = 2 (the default is 1) and `LROT` off.

    **A possible fix:**

    ```diff
    --- a/src/wrtout.f
    +++ b/src/wrtout.f
    @@ -592,6 +592,9 @@
          *        (HCOMP(I,M),I=1,3),HCOMP(3,M)/HCOMP(1,M)
      1520       FORMAT(1X,1P8E16.8,/,1X,1P8E16.8)
     C ROTATION I/O
    +C 11/09/26 KC via Claude
    +C code changed to set ROTP, ROTV and HICZ without rotation too, as
    +C for ITRVER = 0.
                 IF(LROT) THEN
     C MHP 8/25 removed limit on rotation period output
     C     ROTP = MIN(9999.0D0,0.5D0*C4PI/OMEGA(M)/8.64D4)
    @@ -605,6 +608,15 @@
                    ELSE
                       HICZ = 0.0D0
                    ENDIF
    +            ELSE
    +               ROTP = 0.0D0
    +               ROTV = 0.0D0
    +               HICZ = 0.0D0
    +               IF(JENV.LT.M)THEN
    +                  DO K = JENV,M
    +                     HICZ = HICZ + CC23*HS2(K)*EXP(2.0D0*CLN*HR(K))
    +                  END DO
    +               ENDIF
                 ENDIF
     C        Get location of bottom, middle, top of B burning shell.
                 IF(LSHELL) THEN
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): not reached in any of 34 runs (26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones): Every one of YREC's cases sets `ITRVER` = 0, as the documentation strongly recommends (`docs/source/namelist_control.md`, line 138). Not run: `ITRVER` = 2 without `LROT`. Intent: The branch for version 0 computes `HICZ` without rotation, with the comment "ADDED SURFACE CZ MOMENT OF INERTIA CALCULATION TO NON-ROTATING MODELS" ([[#L464-L466]]); this branch did not get the change.

2. **(wrong output)** **Checked by KC** (Nov 10, 2026). **The summary gives the neutrino fluxes and capture rates in erg.** ([[#L401-L403]]; [[#L423-L426]]) Format 160 labels the fluxes "1E10ERG/CM^2," and format 2160 the capture rates "NEUTRINO ENERGIES (1.E-36ERG)." The fluxes `FLUXTOT` are numbers of neutrinos, in units of $10^{10}$ cm⁻² s⁻¹ ([[engeb.f#ENGEB|ENGEB]], step 8), and a flux in these units times a cross section in $10^{-46}$ cm² (the $^8$B coefficient 1.09×10⁴ for $^{37}$Cl is $1.09\times10^{-42}$ cm²) is a capture rate in units of $10^{-36}$ per target atom per second, that is, in SNU, the unit the track gives the same sums ([[#L451-L458]]; `Cl_snu`, `Ga_snu` in [[wrthead.f#L138]]). What follows: wrong units in the `.short` file only; nothing reads them back. The lines are written for every model, with nonzero values only with `LSNU` (off by default).

    **A possible fix:**

    ```diff
    --- a/src/wrtout.f
    +++ b/src/wrtout.f
    @@ -399,7 +399,10 @@
           ENDIF
     C     PRINT OUT NEUTRINO RATES FROM ENGEB CALCULATION
           WRITE(ISHORT,160) (FLUXTOT(I),I=1,8)
    -  160 FORMAT(1X,'NEUTRINOS 1E10ERG/CM^2 PP,PEP,HEP,BE7,',
    +C 11/09/26 KC via Claude
    +C code changed to label the neutrino fluxes and capture rates in
    +C their units.
    +  160 FORMAT(1X,'NEUTRINOS 1E10/CM^2/S PP,PEP,HEP,BE7,',
          *  'B8,N13,O15,F17:', 1P8E9.2)
     C DBG 7/93 from Bahcall's book p 207 table 8.2
           FL7LI = 0.0D0*FLUXTOT(1)+665.0D0*FLUXTOT(2)+8.4D4*FLUXTOT(3)+
    @@ -421,7 +424,7 @@
          *        248.0D0*FLUXTOT(4)+2.5D4*FLUXTOT(5)+224.0D0*FLUXTOT(6)+
          *        355.0D0*FLUXTOT(7)+356.0D0*FLUXTOT(8)
           WRITE(ISHORT,2160) FL7LI,FL37CL,FL71GA,FL81BR,FL98MO,FL115IN
    - 2160 FORMAT(1X,'NEUTRINO ENERGIES (1.E-36ERG): 7Li=', 1PE9.2,
    + 2160 FORMAT(1X,'NEUTRINO CAPTURE RATES (SNU): 7Li=', 1PE9.2,
          * ' 37Cl=',1PE9.2,' 71Ga=',1PE9.2,' 81Br=',1PE9.2,' 98Mo=',
          * 1PE9.2, ' 115In=', 1PE9.2)
           FITMAS = HS1(M)/CMSUN
    ```

    **How the outputs show it.** In `examples/run_standard_solar_model/Test_solarcal_noGS_norot`, at the final model 449, the `.short` file gives "37Cl= 5.83E+00" and "71Ga= 1.19E+02" under "NEUTRINO ENERGIES (1.E-36ERG)" ([[#L423-L426]]). The `.track` gives the same sums as Cl_snu 6.027E+00 and Ga_snu 1.181E+02 ([[#L451-L458]]; [[#L558]]), as does the `.snu` file (6.027 and 118.101; [[main.f#L1212]]); they differ only by coefficients (the ⁸B term for ³⁷Cl is 1.09×10⁴ here, 1.14×10⁴ in `CLSNUF`). The fluxes the `.short` file labels "1E10ERG/CM^2" (6.05E+00 for pp; [[#L401-L403]]) are the `.track`'s pp_neut to F17_neut columns (6.049E+00 for pp): numbers of neutrinos.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The two lines were written at every model of the 33 runs that got past their start, with nonzero fluxes at nearly every model (the $^8$B flux up to 272, in units of $10^{10}$ cm⁻² s⁻¹). With the labels corrected, `examples/giant_differential_rotation/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2` and `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` have identical tracks and `.store` files; only their `.short` files differ, where the labels are. Intent: none found; the commented-out header of version 0 has the same "erg" ([[wrthead.f#L103]]).

### WRTOUT

All per-model output: summary, track and isochrone lines, the last model, and the detailed profiles at intervals; with the central conditions, the convection zone's base and the neutrino capture rates computed on the way.
