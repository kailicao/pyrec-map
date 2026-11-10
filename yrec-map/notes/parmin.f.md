## Explanation

**Purpose.** `PARMIN` reads a run's parameters and sets up its input and output. It holds the defaults of a few user parameters (most defaults are now initializers in the modules), reads the two namelist files (`CONTROL`, usually `yrec8.nml1`, and `PHYSICS`, usually `yrec8.nml2`), expands placeholders in file names, derives some parameters from others, opens most output files and several tables, writes the run's settings to the `.short` file, and interprets the "run cards" (the sequence of evolve and rescale steps). It is the code's single place of configuration.

**How it fits.**
- **Inputs:** the two namelist files, named on the command line (`GETARG(1)` and `GETARG(2)`; JVS 02/11) or defaulting to `yrec8.nml1` and `yrec8.nml2`; the code's version and git hash, `YRECVER` and `GITHASH` (arguments, from [[version.f#SETVERSION|SETVERSION]] through the main program; formerly `/VERSION/`); the environment variables `YREC_INPUT`, `YREC_START` and `YREC_OUTPUT`, if set. `GETARG`, `getenv` and `system` ([[#L758]], [[#L1527]], [[#L828]]) are compiler extensions; standard Fortran has `GET_COMMAND_ARGUMENT`, `GET_ENVIRONMENT_VARIABLE` and `EXECUTE_COMMAND_LINE`.
- **Who calls it:** the main program in [[main.f|main.f]], once, first.
- **What it calls:** [[#EXPAND_VALUE|EXPAND_VALUE]] (in this file), the shell through `system` (`mkdir -p` for the output folder), and [[remap.f#REMAP|REMAP]], which maps the newer, "more intuitively named" parameters (MHP 6/14, 10/14: `TIME_…`, `TOL_…`, `FLAG_…`) onto the older vectors `ATIME`, `HPTTOL` and the like.
- **Outputs:**
  - **Arguments:** 12 table file names (`FALEX06`, `FALLARD`, `FATM`, `FFERMI`, `FLIV95`, `FPATM`, `FPENV`, `FPMOD`, `FPUREZ`, `FSCVH`, `FSCVHE`, `FSCVZ`), which the main program passes on to [[setups.f#SETUPS|SETUPS]] and other set-up routines. Since MHP 8/25, file names travel as arguments rather than in COMMON blocks, "as character strings in common blocks can cause problems."
  - **Modules:** 11, almost all of them for the run's parameters. The namelists read straight into module variables: `NMLPAR_MOD` holds those the physics routines read, `NMLBYPASS_MOD` those that only set others (the cross sections, the `TIME_…` and `TOL_…` parameters for `REMAP`, the wind-law indices), and `CONSTANTS_MOD` (`CLSUN`, `CRSUN`, and `CLN`, `CC13`, `CC23`, `C_2` set here) and `INTPAR_MOD` (`STOLR0`, `IMAX`, `NUSE`) a few more. The others: `IOUNITS_MOD` (every unit number), `RUNLOOP_MOD` (the run cards: `RESCAL`, `IRESCA`, `LENDAG`, `LSETDT`), `COMP_MOD` (`ZENV`, bug 3), `CCOUT_MOD` (`LPHHD`), `ACDPTH_MOD` (`LACOUT`), `LABEL_MOD` and `NEWOPAC_MOD`. The site's `modules.html` lists every module and its users.
  - **Files opened:** the `.short` diagnostic file (`ISHORT`, unit 20), the stored models (`ISTOR`, with a header if `LSTORE`), the first model (`IFIRST`, read), the last model (`ILAST`), the per-shell file (`IMODPT`), and as switched on: the track, solar neutrinos, debugging, Milne variables (appended), pulsation files, the conductive opacities, the OPAL 2006 EOS table, the acoustic-depth file (`…calcad`, named after the `.short` file) and, always, the sound-speed file `FSOUND` (default `Csound.dat`, unit `ISOUND`), which WRTMOD writes when `LSOUND` is on. Before that it creates the output folder, the path of `FTRACK` up to its last `/`.
  - **Unit numbers:** fixed here, from `IOWR = 6` (the screen or status file) to 90 (`IALEX06`); for example the OPAL EOS table is 49, and `ISOUND` is 500.

**What it does, in order.**
1. **Defaults.** Most are now initializers in the modules (`NMLPAR_MOD`, `NMLBYPASS_MOD`, `CONSTANTS_MOD`, `INTPAR_MOD`); `PARMIN`'s own `DATA` keep those of the run cards, the mixture table, `ALFA`, `FK`, `WMAX_SUN`, `AWIND`, `FSOUND` and blank file names. Among the defaults, as their comments state: the cross sections of Solar Fusion II (Adelberger et al. 2011) and their derivatives (`S0_…`, `S0P_…`, `S0PP_…`); Li and Be destruction cross sections (Fowler et al. 1967, Rolfs & Kavanagh 1986, Fowler 1988); the GS98 CNO fractions and $Z/X = 0.02292$ and the Lodders et al. (2021) isotope ratios and light-element abundances; alternative mixtures `AAG21`, `M22P`, `M22M` (Asplund et al. 2021; Magg et al., given as 2021 in the comment); a G&N93 mixture `VNEW` for the envelope; $L_\odot = 3.8515\times10^{33}$ erg s⁻¹ and $R_\odot = 6.9598\times10^{10}$ cm; the burning cutoffs `TCUT`. The mixing length has no default any more: the old `CMIXL` $=1.4$ never reached the run, which takes `CMIXL = CMIXLA(NK)` in the main program for each run card.

    **The mixtures are Magg et al. (2022).** The comment cites `'M22M'` and `'M22P'` as "MAGG ET AL. 2021 (MET,PHOT) A&A 661,140" ([[#L515]]), but `input/opacity/atomic/README` cites "Magg et al. (2022)," as the names suggest. The comment's order (MET,PHOT) is also reversed against the `DATA`, which lists `'M22P'` ($Z/X = 0.0225$) third and `'M22M'` ($0.0226$) fourth ([[#L516-L517]]), and its list of supported mixtures, `'AAG21',M22M','M22P'`, lacks the quote before `M22M` ([[#L506]]).

2. **Namelists.** Both files are read and `REMAP` is called. Then `EXPAND_VALUE` expands a leading placeholder in each file name (bug 5), and the output folder is created (bug 4).

    > **Question** ([[#L380]], [[#L382]], [[#L387]], [[#L775]]). **Old entries that `REMAP` overwrites.** `DTDIF`, `DTWIND`, `HPTTOL` and `ATIME` are superseded by `REMAP`'s new parameters when those are used (`LNEWVARS`). Can the old entries be removed, or kept with a warning? (`LSOLWIND` now reaches [[mdot.f#MDOT|MDOT]] through `NMLPAR_MOD`, but MDOT's scaled solar wind stays inert: its constants `DMSUN`, `DMWSUN`, `DMWMAX` are zero, and a guard skips the branch; MDOT's page.)

3. **Derived settings.**
   - Li/Be cross sections given by the user (`LXLI6` and so on) become scale factors relative to the defaults, e.g. `SLI6 = XSLI6/5.5D3`.
   - Semiconvection together with any overshoot stops the run. Rotation (`LROT`) with the advection-diffusion transport of angular momentum (`LDIFAD`) stops it too: as the code's comment says, [[dadcoeft.f#DADCOEFT|`DADCOEFT`]] rebuilds its coefficients from equal-grid arrays that no routine sets, so the option is not implemented.

    > **Question** ([[#L980-L989]]). **Semiconvection with overshoot stops the run.** `LSEMIC` with any of `LOVSTC`, `LOVSTE`, `LOVSTM` prints "SEMI-CONVECTION AND OVERSHOOT FLAGS BOTH TURNED ON" and stops. Both act at the edge of a convective core, and a student would expect them to be combined (overshoot beyond a semiconvective zone). Is it that OVERSH and SCONVEC both rewrite the same boundary zone? A comment in GETOPAC (JCZ 211125) mentions "semiconvection+overshoot HB models," which this check forbids: is a combined treatment planned, or does that comment refer to another code?

   - **Rotation** (`LROT`): `WALPCZ` is limited to $[-2, 0]$; `LSOLID` forces `IMPJMOD = 1`. For the old wind law (`LMWIND` false), from the index $\alpha$ (`ALFA`), as the comments derive:
$$\dot J = f_K\, 2.036\times10^{33}\,(1.452\times10^{9})^{\alpha}\left(\frac{\dot M}{10^{-14}}\right)^{1-2\alpha/3}\Omega^{1+4\alpha/3}\left(\frac{R}{R_\odot}\right)^{2-\alpha}\left(\frac{M}{M_\odot}\right)^{-\alpha/3}.$$
     This is the Kawaler (1988) law (as the documentation names it); $\dot M$ is "in solar masses per year" (fixed at $2\times10^{-14}$ in [[cowind.f#COWIND|COWIND]] and [[wind.f#WIND|WIND]]) and $M$, $R$ relative to the Sun's, as their comments say.

    > **Question** ([[#L1028-L1040]]). **The units of the old wind law.** The comments give $\dot M$ in $M_\odot\,\mathrm{yr}^{-1}$ and $M$, $R$ in solar units, but not the units of $\Omega$ and $\dot J$. The rest of the code works in cgs, which suggests $\Omega$ in rad s⁻¹ and $\dot J$ in g cm² s⁻² (COWIND and WIND multiply by the step `DT`, so that they return a change of $J$ in g cm² s⁻¹): is that right?

     For the Matt et al. law (`LMWIND`), the indices $a, b, c, d, m$ (`PMMA`…`PMMM`), preset by `AWIND` ('K97': Krishnamurthi 1997, $m = \alpha/3$; 'V13': van Saders & Pinsonneault 2013, $m = 0.22$; 'CUS': from the namelist), give the exponents of $\dot J$, each quantity relative to the Sun:
$$a_\Omega = 1 + a - 2am + 4mb,\quad a_R = 2 + 5m - 4mc,\quad a_M = -m,\quad a_L = 1 - 2m,\quad a_P = 2md,\quad e_\mathrm{cen} = md,$$
     with $a_\tau = 0$ (the $\tau_\mathrm{cz}$ term is now applied in [[mwind.f#MWIND|MWIND]]), $c_2 = 0.0506$, `CONSTFACTOR` $= f_K\,J_\odot/\Omega_\odot^{a_\Omega}$, and, if `WMAX_SUN` $< 1000$, the saturation threshold $\Omega_\mathrm{sat} = $ `WMAX_SUN` $\times\,\Omega_\odot$.

    > **Question** ([[#L1062-L1073]], [[#L1097-L1098]]). **The exponent of $R$ in the Matt et al. law.** The comment's derivation gives $\dot J \propto R^{2+5m+4mbc}$, but the code (after JvS 09/25, "removed typo," which dropped a factor $b$) uses $a_R = 2 + 5m - 4mc$. For 'V13' ($c = 0$) the two agree. For 'K97' ($b = 1$, $c = 2$, $m = \alpha/3$) the code gives $2 - 3m = 2 - \alpha$, the exponent of the old law, while the comment would give $2 + 13m$; a custom law ('CUS') with $c \ne 0$ depends on the choice, and with $b \ne 1$ also on the dropped factor. Is the code's exponent the intended one, so that only the comment is stale?

   - **Composition changes:** a single species to rescale (`LNEWCP`, `ANEWCP`), a CNO mixture (`ISETMIX`, `AMIX`, with checks on a custom one) and isotope ratios (`ISETISO`, `AISO`), all applied later to the starting model by [[starin.f#STARIN|STARIN]] (the documentation's value 2 for a custom mixture does nothing: bug 2).
   - **Settling switches:** `LDIFZ` turns on `LDIFY` and `LTHOUL`; `LDIFLI` turns on `LNEWDIF`, `LDIFY`, `LDIFZ`, `LTHOUL`, turns off `LTHOULFIT`, and sets `ILAMBDA = 4`.
4. **Summary.** A line of tolerances and rotation settings is written first, right after the semiconvection and `LDIFAD` checks. After the derived settings, the `PHYSICS` and `CONTROL` namelists are written to `ISHORT` as read, and the output-only namelist `DERIVED` with the values derived above (the wind-law exponents, the settling switches, the mixture, `LREL`, …). Then the mixing lengths are checked: each `CMIXLA` entry the run uses (only `CMIXLA(1)` under solar calibration, `LCALS`, otherwise the first `NUMRUN`, at most 50) must be positive, or the run stops; so must the envelope triangle's size, `TRIDT` and `TRIDL`. Then the atmosphere choice (`KTTAU` 0–5), and the run's description with the version line (`# YREC v…`, also written at the head of the `.store` file and the track).
5. **Run cards** (`NUMRUN` cards, at most 50): `KINDRN = 1` evolves `NMODLS` models (to an age, a central D, X or Y, or with a fixed time step); `2` rescales the model (mass, $X$, $Z$, core mass) and relaxes it; `3` rescales and evolves. `LENDAG` and `LSETDT` are set only for evolve cards ([[#L1396-L1406]]), so the stop conditions (`ENDAGE`, `END_XCEN`, `END_YCEN`, …) are ignored on a rescale-and-evolve run: [[main.f#b1]], whose fix belongs here. The message of a rescale-and-evolve card is that of a rescale card (bug 1), and each card sets `ZENV` (bug 3).

**Design.** `PARMIN` is a 1,508-line routine that is mostly comments, declarations and data. A parameter now lives in one place, the module variable the namelist reads into. A few namelist entries are still unused (see the question at step 2).

**From YREC's documentation.** [Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html):
- **Placeholders.** `{YREC_INPUT}`, `{YREC_START}`, `{YREC_OUTPUT}` at the start of a path in the `CONTROL` namelist are replaced by the environment variable of that name, or by a default: the documentation gives `../../input`, `../../input/models` and `output` (in the working directory). `PARMIN` uses `../../startmodels` for `{YREC_START}` ([[#L1515-L1516]]), and the repository keeps its starting models in `startmodels/` (there is no `input/models/`), so the documentation's default and the "input/models" of the User Guide and the Quick Start are out of date (settled from the code and the repository, Nov 9, 2026).
- **File names.** `FFIRST` the starting model, `FLAST` the last converged model, `FSTOR` the snapshots, `FTRACK` global quantities against time, `FSHORT` the numerics of the run; `FMODPT`, `FSNU`, `FSCOMP` are "no longer used" (light elements are now in the track). Two of them are still opened and written: `FSNU` (opened with `LSNU`, [[#L946-L950]]) by the main program ([[main.f#L1209-L1229]]), and `FMODPT` (always opened, [[#L965]]) by PARMIN's description of the run ([[#L1364]]), [[wrtmod.f#L152]] and [[seculr.f#L486-L498]] (settled from the code, Nov 9, 2026). Table paths are on the pages of the routines that read them.
- **Read here only.** `KINDRN`, `RSCLM`, `RSCLX`, `RSCLZ`, `RSCLCM` (the run cards, below); `AMIX`, `AISO`, `ISETMIX`, `ISETISO` (the mixture, [[starin.f#STARIN|STARIN's page]]); `AWIND`, `FK`, `ALFA`, `WMAX_SUN` (the wind law, [[mwind.f#MWIND|MWIND's page]]; the Physics page lists `ALFA` as "Not used. Legacy exponent for Kawaler (1988) wind law," `namelist_physics.md` line 311, and the modules page calls `ALFA` and `FK` exponents, but `ALFA`, default 1.5, sets the old law's exponents and `CONSTFACTOR` when `LMWIND` is off, and `PMMM = ALFA/3` for `AWIND = 'K97'`, the default, [[#L1036-L1040]], [[#L1077]]; `FK` is a scale factor); `LXLI6`…`LXBE93` with `XSLI6`…`XSBE93`, manually set p+⁶Li, p+⁷Li and the three p+⁹Be cross sections (keV b; the documentation labels `LXBE92` and `LXBE93` as p+⁶Li channels, a slip for ⁹Be).
- **Run cards** (Run parameters & Kind cards): each card is a phase, `KINDRN(i)` = 1 evolve, 2 rescale (zero time step, main sequence or core helium burning), 3 rescale and evolve (pre-main sequence, which has no zero-time-step solution); `LFIRST(i)` starts from `FFIRST` rather than the previous phase's model; `RSCLM`, `RSCLCM`, `RSCLX`, `RSCLZ`, if positive, rescale to that mass, core mass (core helium burning only), $X$, $Z$; `CMIXLA(i)` is the mixing length to rescale to (or run with); `LSENV0A(i)` moves the outer fitting point to `SENV0A(i)`, which the Control page calls the log of the fractional envelope mass ($10^{-4}$ standard, $10^{-7}$ thin), but which is $\log_{10}(m_\mathrm{fit}/M_\star)$ of the fitting point, a small negative number (as the User Guide says: $-10^{-4}$ standard, about $2\times10^{-4}$ of the mass outside the fitting point; $-10^{-7}$ thin; STARIN negates a positive value; STARIN's page, step 6); `NMODLS(i)` stops after that many models (two for a first rescaling is recommended, then an evolve run); `ENDAGE`, `END_DCEN`, `END_XCEN`, `END_YCEN` stop at an age or a central D, $X$ or $Y$.

    > **Question** ([[starin.f#L586-L591]]). **`SENV0A` in the documentation.** The Control page calls `SENV0A(i)` "Log of fractional envelope fitting point mass. 1e-4 standard, 1e-7 thin," which reads as $\log$ of $10^{-4}$; the code (STARIN: `SENV = HS(M) - HSTOT`) and the User Guide make it $\log_{10}(m_\mathrm{fit}/M_\star)$, a small negative number ($-10^{-4}$ puts $1 - 10^{-10^{-4}} \approx 2.3\times10^{-4}$ of the mass outside the fitting point). STARIN negates a positive value, so the Control page's numbers work, but their meaning is not the one it gives. Also, STARIN's floor is $-10^{-12}$, while the User Guide says $-10^{-11}$. Should the two pages give the negative values, what they mean, and the same floor?


From the user documentation ([User Guide](https://yrec.readthedocs.io/en/latest/userguide.html), [Quick Start](https://yrec.readthedocs.io/en/latest/quickstart.html)):
- **Reading the namelists.** The two files are read in a fixed order, the first argument as `CONTROL` (unit `ISTAND`) and the second as `PHYSICS` (unit `IRUN`); the Python wrapper accepts them in either order, the program does not. They are opened by the names given, so a relative name is found from the working directory; the User Guide says both files should be in the executable's directory (`userguide.md`, line 23).

    **The namelists are looked for in the working directory.** PARMIN opens the two files by the names given (`OPEN(UNIT=ISTAND, FILE=YREC1, …)`, [[#L766-L767]]; by default `yrec8.nml1` and `yrec8.nml2`, [[#L758-L764]]), so a relative name is found from where the run starts, wherever the executable is; the User Guide could say "the working directory."

- **The output folder.** PARMIN now creates the folder of `FTRACK` (`mkdir -p`) before any output is opened, while the Quick Start still tells the user to `mkdir output` by hand, or the run fails; the step is no longer needed (bug 4 for the case of a name without `/`).

[Where Namelist Variables Live](https://yrec.readthedocs.io/en/latest/namelist_modules.html) gives the reasons for the modules' split (on [[nmlbypass_mod.f#NMLBYPASS_MOD|NMLBYPASS_MOD's page]]) and why `CHARACTER` variables are passed as arguments: in a COMMON block they force padding against numeric members, which compilers treat differently.

**Changed since `rp_1`.** The namelists read into modules (`NMLPAR_MOD`, `NMLBYPASS_MOD`), where most defaults now are; the removed options are gone (the MHD and OPAL 1995/2001 equations of state, the OPAL92, Kurucz 1990, LAOL89 and Alexander 1995 opacities, Monte Carlo, isochrones), and with them 15 file-name arguments; `YRECVER` and `GITHASH` are new arguments, printed and written as a version line; file names may start with a placeholder (`EXPAND_VALUE`, new), and the output folder is created; the sound-speed file is opened here; the hand-written summary tables are replaced by namelist echoes after `ISHORT` is opened, with a new `DERIVED` namelist; `TENV` is no longer set (ENVINT computes it); the default `CMIXL` is removed and `CMIXLA` is checked; `PMMM = 0.22` and `C_2 = 0.0506` are now double-precision constants; `LPMM`, `PMMWMAX`, `ZOPAL952` and `ZALEX2` are no longer namelist entries. Settled: the namelist dump before `OPEN(ISHORT)`, the printing slip in `TRIDT`, `TRIDL` and the stale "standard" values (old questions 1, 3, 4), and part of old question 6 (the unused entries; `LSOLWIND` now reaches MDOT).

**Changed since `09c3b9b`.** The `CONTROL` namelist gains `L_ZERODT_PREMS` (in [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]], used in main.f), so it is read and echoed to the `.short` file with the others.

**Changed since `a8a5950`.** Two new checks stop the run: `LROT` with `LDIFAD` (exit status 1), and a non-positive `TRIDT` or `TRIDL` (exit status 3; as the code's comment says, a zero size made [[surfbc.f#SURFBC|`SURFBC`]]'s reflection walk loop for ever). The stops on bad input (semiconvection with overshoot, a non-positive `CMIXLA`) now exit with status 3, the code for input errors (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(wrong output)** **Checked by KC** (Nov 10, 2026). **The wrong message for a rescale-and-evolve card.** ([[#L1476-L1480]]) A `KINDRN` = 3 card that starts from the previous run's model prints format 451, "RESCALE THE PREVIOUS RUN'S LAST MODEL.," the message of a rescale-only card; its own format 551 ("RESCALE & EVOLVE THE PREVIOUS RUN'S LAST MODEL.") is commented out. Only the screen and `.short` message is wrong.

    **A possible fix:**

    ```diff
    --- a/src/parmin.f
    +++ b/src/parmin.f
    @@ -1474,10 +1474,12 @@
       550          FORMAT(/1X,'RUN #',I3,
          1         '   RESCALE & EVOLVE THE INPUT MODEL: "FIRST MODEL".')
                 ELSE
    -               WRITE(IOWR,451) NKIND
    -               WRITE(ISHORT,451) NKIND
    -C   551          FORMAT(/1X,'RUN #',I3,
    -C      1         '   RESCALE & EVOLVE THE PREVIOUS RUN''S LAST MODEL.')
    +C 11/09/26 KC via Claude
    +C code changed to print the rescale-and-evolve message, format 551.
    +               WRITE(IOWR,551) NKIND
    +               WRITE(ISHORT,551) NKIND
    +  551          FORMAT(/1X,'RUN #',I3,
    +     1         '   RESCALE & EVOLVE THE PREVIOUS RUN''S LAST MODEL.')
                 END IF
                 WRITE(IOWR,452) NMODLS(NKIND),(RESCAL(I,NKIND),I = 1,4)
                 WRITE(ISHORT,452) NMODLS(NKIND),
    ```

    **How the outputs show it.** In `examples/run_from_seed_to_start/m10000gs98z001000_prems`, the `.short` file announces the second card as "RUN #  2   RESCALE THE PREVIOUS RUN'S LAST MODEL." ([[#L1478]]; line 422 of the file), the message of a card that only rescales. The same `.short` file and the `.track` ([[wrtout.f#L558]]) show that card's five models, 21 to 25, evolving at its new $Z$ = 0.001: Their ages rise from 5.31806807E-006 to 5.59249319E-006 Gyr, with steps of 52 to 88 years. The first card, also of kind 3, gets its own message, `RESCALE & EVOLVE THE INPUT MODEL: "FIRST MODEL".` ([[#L1473-L1475]]).

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Of YREC's cases with such a card, `examples/run_from_seed_to_start/m10000gs98z001000_prems` (its run 2) was run, and the wrong message was printed once. With format 551 restored, the track and `.store` are identical, and only `.short` changes, by the message. Intent: Format 551 is commented out with no reason given.

2. **(changes results, small)** **Checked by KC** (Nov 10, 2026). **`ISETMIX` = 2 and `ISETISO` = 2 do nothing.** ([[#L1141]], [[#L1149]], [[#L1193]], [[#L1196]]) The documentation (`namelist_control.md`, lines 173, 180, and 185) gives 2 as the custom mixture ("CNO enabled if `ISETMIX = 2`, Light elements if `ISETISO=2`"); the code takes a custom mixture only with `ISETMIX` = 1 and `AMIX = 'CUS'` (`ISETISO` = 1 and `AISO = 'CUS'`), and any other value of `ISETMIX`, `ISETISO` leaves the starting model's mixture alone without a message. No namelist in the repository sets either to 2.

    **A possible fix,** if the documentation's numbering is the intended one (otherwise, a correction of the documentation):

    ```diff
    --- a/src/parmin.f
    +++ b/src/parmin.f
    @@ -1138,7 +1138,11 @@
           ENDIF
           LMIXTURE = .FALSE.
           LISOTOPE = .FALSE.
    -      IF(ISETMIX.EQ.1)THEN
    +C 11/09/26 KC via Claude
    +C code changed to accept ISETMIX = 2 as the custom mixture, as the
    +C documentation describes it.
    +      IF(ISETMIX.EQ.2) AMIX = 'CUS'
    +      IF(ISETMIX.EQ.1 .OR. ISETMIX.EQ.2)THEN
     C IF DEFAULT MIX (GS98) CNOFRACS ARE ALREADY SET.
     C         IF(AMIX.EQ.'GS98')THEN
     C            LMIXTURE = .TRUE.
    @@ -1190,7 +1194,8 @@
          *        E12.4,' APPLIED TO STARTING MODEL.')
           ENDIF
     C     CHECK IF ISOTOPE RATIOS NEED TO BE ALTERED
    - 602  IF(ISETISO.EQ.1)THEN
    + 602  IF(ISETISO.EQ.2) AISO = 'CUS'
    +      IF(ISETISO.EQ.1 .OR. ISETISO.EQ.2)THEN
     C FOR A CUSTOM MIX,DISABLE IF THE SUM OF CNO MASS FRACTIONS EXCEEDS ONE
     C OR IF ANY MASS FRACTION IS NEGATIVE
              IF(AISO.EQ.'CUS')THEN
    ```

    **How the code itself shows it.** The code's own comments agree with the code, not with the documentation: MHP's comment of 10/24 gives both `ISETISO` and `ISETMIX` as "`(1=USED)`" and says "`AMIX AND AISO ARE STRINGS IDENTIFYING EITHER A PRESET MIXTURE OR A CUSTOM ONE ('CUS')`" ([[#L502-L505]]), and STARIN, which applies the mixture, says "`ISETMIX=1 -> CAN ADJUST CNO FRACTIONS ISETISO=1-> CHANGE ISOTOPE RATIOS`" ([[starin.f#L387]]). The shipped namelists side with the documentation: In 503 of them (in `testsuite/`, `examples/`, and `sample_cases/`), the comments on `ISETMIX` and `ISETISO` read "`0 = do not adjust 1 = use specified mixture (AMIX below) 2 = custom mixture`" (as in `testsuite/Test_solarGS98_SF3.nml1`, lines 10 and 13), and many add "`Custom mixture controls - CNO enabled if ISETMIX = 2, Light elements if ISETISO=2`" (line 111 there); none sets `AMIX = 'CUS'`. So the code and its comments use one numbering, and the documentation and the namelists' comments the other.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): No case of YREC sets either switch to 2, so `testsuite/Test_solarAAG21_dif` was run with `ISETMIX` = `ISETISO` = 2 and the case's own commented custom-mixture block switched on: The code ignored both, without a message. With the documentation's numbering (the fix), the custom mixture is applied, and the track changes on the pre-main sequence: $\log L$ by up to 0.0025 dex and $\log T_c$ by up to 0.0014 dex (near 0.00018 Gyr), against 0.00023 and 0.000037 dex with a null change (nearly every opacity, all with 3 <= log T <= 9 and -6 <= log rho <= 9.75, times 1 + 1e-10); central $X$ by up to $1.8\times10^{-5}$, within the noise ($3.9\times10^{-5}$). The run keeps its end age, 4.568 Gyr (1,201 models instead of 1,200). The effect is real, though small for this mixture. Intent: The code's comment allows only the default L21 or a custom mixture named by `AISO = 'CUS'` ("CURRENTLY THERE ARE ONLY 2 VALID OPTIONS"), so the documentation may be what is out of date (question below).

3. **(harmless in the runs)** **`ZENV` set from every run card.** ([[#L1486]]) The last line of the card loop, `IF(RESCAL(3,NKIND).GE.0.0D0) ZENV=RESCAL(3,NKIND)`, runs for every card, including evolve cards, where `RESCAL` is never set (zero), and for rescale cards with the default `RSCLZ = 0` ("0 = use current value"). So `ZENV` leaves `PARMIN` as the last card's `RSCLZ`, usually 0. STARIN sets `ZENV = ZNEW` in the first run ([[starin.f#L923]]), and RSCALE sets it whenever it changes $Z$ ([[rscale.f#L137-L139]]); in between, the first run's STARIN may call the physics with this `ZENV` when it moves the fitting point (`EQSTAT`, `GETOPAC`, `ENVINT`, [[starin.f#L641-L682]], [[starin.f#L686-L731]]; `GETOPAC` compares $Z$ with `ZENV`, [[getopac.f#L140]]).

    **A possible fix,** a choice for the developers: drop the line, since RSCALE sets `ZENV` when it rescales $Z$.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The line ran for every run card of all 33 runs, and in 32 of them it set `ZENV` = 0 from an evolve card. With the line dropped, `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` and the solar calibration `examples/run_standard_solar_model/Test_solarcal_noGS_norot` give identical tracks and `.store` files; only `.short` changes, within 2%. So STARIN's use of this `ZENV`, if any, changes nothing in these runs, and the item stays fragile code. No comment explains the line.

4. **(never occurred)** **No `/` in `FTRACK` leaves `LAST_SLASH_IDX` unset.** ([[#L815-L828]]) The loop that finds the last `/` sets `LAST_SLASH_IDX` only when there is one. A track file named without a folder leaves it at whatever the saved local holds (in practice 0 at the first call), and `mkdir -p ""` then fails with a message from the shell; another value would cut `FTRACK` at a wrong place.

    **A possible fix:**

    ```diff
    --- a/src/parmin.f
    +++ b/src/parmin.f
    @@ -815,6 +815,9 @@
     C Create output directory as specified in the FTRACK value of CONTROL
     C namelist if it doesn't already exist.
           ! find index of last '/' char. Use that to snip out the directory name.
    +C 11/09/26 KC via Claude
    +C code changed to create no folder when FTRACK names none.
    +      LAST_SLASH_IDX = 0
           DO I = LEN_TRIM(FTRACK), 1, -1
               IF (FTRACK(I:I) .EQ. '/') THEN
                   LAST_SLASH_IDX = I
    @@ -822,10 +825,12 @@
               ENDIF
           END DO
     1250  CONTINUE
    -      CMD = 'mkdir -p "' // FTRACK(1:LAST_SLASH_IDX) // '"'
    -      print *,"OUTPUT placed in :  ",FTRACK(1:LAST_SLASH_IDX)
    -      print *, ''
    -      CALL system(CMD)
    +      IF(LAST_SLASH_IDX.GT.0) THEN
    +         CMD = 'mkdir -p "' // FTRACK(1:LAST_SLASH_IDX) // '"'
    +         print *,"OUTPUT placed in :  ",FTRACK(1:LAST_SLASH_IDX)
    +         print *, ''
    +         CALL system(CMD)
    +      ENDIF
     
     
     C JVS 02/11 Acoustic depth/ Asteroseismic glitch output. Puts output
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The search ran once in each of the 33 runs, and every `FTRACK` named a folder (its last `/` at character 115 to 173), so `LAST_SLASH_IDX` was always set; the fix was not run. Four namelists of YREC name none: `sample_cases/Gyrochrones/rotevolin_m0p2per1p4`, `rotevolin_m0p25per2p2`, `rotevolin_m1p25per8p0`, and `rotevolin_m1p35per8p0` (`FTRACK = "rotevolin_m0p2per1p4.track"`, line 128 of the first); none of them was run, so what they do (whether `mkdir -p ""` fails) is not checked. No comment explains the missing initialization.

5. **(withdrawn)** **`EXPAND_VALUE` leaves the end of `TEMP` undefined.** ([[#L1527]], [[#L1533-L1538]]) Checked, and not a bug: `GETENV` is called before the test of whether the variable is set ([[#L1527]]), so in both branches, and when the variable is not set, gfortran's `GETENV` fills `TEMP` with blanks (checked with a small program built with the gfortran that builds YREC). In the default branch, `TEMP` is therefore already blank beyond the expanded name.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): not reached, since every run set all three variables. The statement rests on gfortran's behavior; a compiler that leaves the argument unchanged for an unset variable would bring the item back.

6. **(wrong output)** **Checked by KC** (Nov 10, 2026). **Long paths are cut to 256 characters without a word.** ([[#L1527-L1538]]; [[#L825-L828]]; [[pdist.f#L86-L111]]) Every file name is `CHARACTER*256` ([[#L80-L90]]), and `EXPAND_VALUE`, which replaces `{YREC_OUTPUT}` and the other placeholders by their environment variables, never checks the length: A longer result keeps its first 256 characters. Inputs then fail to open (`STATUS='OLD'`), but outputs are created under the shortened names (`STATUS='UNKNOWN'`), and names cut inside their shared stem coincide, so the track, short, store, and last files can land in one file. The `mkdir` command for the output folder ([[#L825]]) is cut the same way and its failure is ignored, and PDIST's pulsation names lose their model numbers (or, for a name of exactly 256 characters, their folder). Taken with an output folder longer than 182 characters for the repository's longest names; the default (`output`) is far below it.

    **A possible fix** (a stop; longer names would need every declaration changed, and the `mkdir` command and PDIST's names, up to 11 and 8 characters longer than the name, would need `CMD` and `COUT` lengthened too):

    ```diff
    --- a/src/parmin.f
    +++ b/src/parmin.f
    @@ -1503,7 +1503,7 @@
           CHARACTER*256 PHOLDERS(NUM_ENVVARS)
           CHARACTER*256 DEFAULTS(NUM_ENVVARS)
           CHARACTER*256 PHOLDER
    -      INTEGER STLEN1, STLEN2, PH_LEN, DEF_LEN
    +      INTEGER STLEN1, STLEN2, PH_LEN, DEF_LEN, NEWLEN
     C Each placeholder (env var name enclosed in curly braces) to be
     C supported for expansion in namelists, along with default value in the
     C case where the var is not defined in the execution environment.
    @@ -1527,6 +1527,19 @@
                 CALL getenv(PHOLDER(2:PH_LEN-1), TEMP)
                 STLEN1 = LEN_TRIM(TEMP)
                 STLEN2 = LEN_TRIM(NML_VAR)
    +C 11/10/26 KC via Claude
    +C code changed to stop when the expanded path does not fit in the 256
    +C characters of the name (or the variable itself fills them); it was
    +C cut short silently, and the run wrote to the shortened names.
    +            NEWLEN = DEF_LEN+STLEN2-PH_LEN
    +            IF (STLEN1 .NE. 0) NEWLEN = STLEN1+STLEN2-PH_LEN
    +            IF (NEWLEN .GT. LEN(NML_VAR) .OR.
    +     *          STLEN1 .EQ. LEN(TEMP)) THEN
    +               WRITE(*,*) 'EXPAND_VALUE: the path ', NML_VAR(1:STLEN2),
    +     *              ' expands to more than ', LEN(NML_VAR),
    +     *              ' characters'
    +               STOP 3
    +            END IF
                 IF (STLEN1 .NE. 0) THEN     ! If env var set
                     TEMP(STLEN1+1:STLEN1+STLEN2-PH_LEN) = NML_VAR(PH_LEN+1:STLEN2)
                     !print *,"Override: ",TEMP(1:LEN_TRIM(TEMP))
    ```

    **How the code itself shows it.** `TEMP(STLEN1+1:STLEN1+STLEN2-PH_LEN) = NML_VAR(PH_LEN+1:STLEN2)` ([[#L1531]]) writes beyond `TEMP`'s 256 characters whenever the sum exceeds 256, and `NML_VAR = TEMP` ([[#L1538]]) then cuts; `CALL getenv(PHOLDER(2:PH_LEN-1), TEMP)` ([[#L1527]]) already cuts a variable longer than 256. PDIST guards against nothing either: `IOCCOL = INDEX(FPMOD,' ')-1` ([[pdist.f#L86]]) is $-1$ for a name that fills all 256 characters.

    **Checked by reading the code** (Nov 10, 2026): `EXPAND_VALUE` expands 23 names ([[#L791-L813]]), and nothing in it or in its callers compares a name's length with 256. Built alone, with the case's flags and with `-fcheck=all`, the routine turned `{YREC_OUTPUT}/sample_cases/UpperMS/Sample_m9p0feh+0p0GS98_none_TAHB.track` with a 201-character `YREC_OUTPUT` into a name of 256 characters ending in `..._TAHB.`, with no message and no error in either build, and a separate test showed that gfortran lets two units open one file without an error. The longest output name after its placeholder in the repository's namelists is 74 characters (`FSCOMP` of `testsuite/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2.nml1`), so an output folder of more than 182 characters cuts some case's names. In the round of Nov 9, 2026, two fix runs lost their files this way, when the output path exceeded 256 characters. The fix, built into the routine alone, stops (`STOP 3`, with the message) for the 201-character folder and gives the full 241-character name for a 181-character one. Intent: none found (no comment on the length).

### EXPAND_VALUE

Replaces a placeholder at the start of a file name, `{YREC_INPUT}`, `{YREC_START}` or `{YREC_OUTPUT}`, by the value of the environment variable of that name, or, if it is not set, by a default: `../../input`, `../../startmodels` or `output`. A placeholder elsewhere in the name is left as it is (bug 5, withdrawn, for the default branch).
