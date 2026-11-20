# State: what a run carries

*Part of [A new design for YREC](overview.md). Every value a run carries has one home: the `State`, a family's cache, or work arrays. This page lists the `State`'s fields, each under its descriptive name beside YREC's, and says what the copy test found.*

## The three homes

- **`State`:** the star at one moment: arrays over the shells, scalars, and any value carried from one step to the next that changes later results. `state.copy()` copies it whole, `state.differences(other)` lists the fields that differ byte for byte, and `state.to_npz(path)` and `State.from_npz(path)` save and load it exactly.
- **A family's cache:** tables read once, interpolation coefficients, the tables' search guesses, values kept to save time; the family can rebuild it, and it changes no result.
- **Work arrays:** scratch space inside one computation, preallocated and passed to the kernels ([Writing a Numba family](numba.md)); nothing in them outlives the call.

**The copy test.** Copy a model in the middle of a run and run both copies on: They must match byte for byte. A value that breaks the test lives in the wrong home: It changes results, so it belongs to the `State`.

## The copy test on the 1 M☉ ZAMS case

The run's driver does the test when asked (`PYREC_COPY_AT=k`): After step $`k`$ of the run's 268, it copies the model; the original runs on to the end of its kind card's loop (a kind card is one of the runs YREC chains in one job), and its output files, screen text, and `State` are kept; the output files are put back as they were at the copy, the copy takes the original's place, and the run goes on with it. When the copy reaches the original's last step, the two are compared: every output file and the screen byte for byte, and the `State` field by field.

**What it found.** The test ran after steps 1, 2, 3, 100, 200, and 267, and the copy now matches the original byte for byte at each, with every output file as YREC's. Getting there moved two kinds of value into the `State`:

- **A setting the run writes.** After steps 100 and 200 the copy first failed (it crashed at step 100's copy, and stopped early at step 200's). Putting back the one value `LPTIME` made it identical: [HTIMER](../../yrec-map/notes/htimer.f.md) turns off its structure criterion for good near the ZAMS by setting `LPTIME`, a namelist setting, so the setting is part of the star's history. It is now the field `structure_timestep_on`; the configuration holds its starting value.
- **Tables with a tolerance.** After step 3 the copy differed. The surface opacity tables interpolated to the surface composition are rebuilt only when X or Z moves by more than a tolerance ([getalex06.f](../../yrec-map/notes/getalex06.f.md): 10⁻⁸; [getopal95.f](../../yrec-map/notes/getopal95.f.md): 10⁻⁴), so a table built at an earlier step serves later points, and its bits carry from step to step. The molecular table with its X and Z, and the OPAL table with its X, are now `State` fields (`molecular_opacity_table`, `molecular_table_x`, `molecular_table_z`, `surface_opal_table`, `surface_opal_table_x`); neither half alone made the copy identical.

Two carried values were already in the `State`: eqsaha's starting guess for the Saha equations, `saha_guess` (each EOS call starts its Newton iteration from the last call's result, which changes results), and the network's saved scalars, `network_saved` (engeb's `SAVE`d values, read only below `TCUT(1)`).

**Shared arrays.** While the default families wrap the Fortran-tracking pyrec, the running model's `State` is a view of pyrec's own arrays: Its arrays are the very arrays pyrec's routines and kernels read, and its scalars are copied into pyrec's modules before each stage and back after it. Some of those arrays are also held inside the kernels' data tuples (eqsaha's guess is one), so a copy or a restore writes values into the arrays in place and never replaces an array: Replacing one would cut it off from the tuples that hold it. After every stage the model checks that each `State` array is still pyrec's.

**Its reach.** The test covers the 1 M☉ ZAMS case only, in which rotation, diffusion, and mass loss are off. Whether the values below stay where they are on a case with those on is open.

## Names

The object-oriented pyrec uses descriptive names, each beside YREC's name, written in lower case as the Fortran-tracking pyrec writes it. The mapping is a table in the code, so that this page, [the families' names](names.md), and the site's glossary (linked at the top of every page) can show it. There is one table for the `State` (below) and one per family module, and each of YREC's variables has one descriptive name across all of them (`latmo` is `in_atmosphere` here, in the EOS, and in the solver); a routine's arguments are mapped per routine, as [the families' names](names.md) explains.

## The fields

All 153 fields, generated from the `State` class's metadata. Shapes are YREC's, JSON being YREC's largest number of shells (its array dimension; the shells in use are `n_shells`); pyrec's arrays keep one unused element at index 0 and the same index order, so that the default families wrap pyrec unchanged. The role says what a field is: `star` (the star at this moment), `old` (YREC's start-of-step copies), `carried` (a value carried from step to step that changes later results), `work` (the solver's scratch, kept for now), or `run` (the run's bookkeeping, which may move to the model or the configuration). The last column says what is not yet checked about a field. The `work` and `run` fields sit in the `State` while the defaults wrap pyrec's routines; whether they move to the solver's work arrays and to the model or the configuration is open.

| Descriptive name | YREC name | Meaning | Units | Shape | Role | Not yet checked |
| --- | --- | --- | --- | --- | --- | --- |
| `log_mass` | `hs` | mass inside each shell | log10 g | (JSON) | star |  |
| `luminosity` | `hl` | luminosity at each shell | L_sun | (JSON) | star | units from oldmod_mod.hlo/hlsuro (L/L_sun); to check |
| `log_radius` | `hr` | radius of each shell | log10 cm | (JSON) | star |  |
| `log_pressure` | `hp` | pressure | log10 dyn cm^-2 | (JSON) | star |  |
| `log_temperature` | `ht` | temperature | log10 K | (JSON) | star |  |
| `log_density` | `hd` | density | log10 g cm^-3 | (JSON) | star |  |
| `convective` | `lc` | whether each shell is convective |  | (JSON) | star |  |
| `composition` | `hcomp` | X, Y, Z, then the tracked isotopes (HCOMP(K, J)) | mass fraction | (15, JSON) | star |  |
| `shell_mass` | `hs1` | mass of each shell (unlogged) | g | (JSON) | star |  |
| `mass_between_centers` | `hs2` | mass between shell centers | g | (JSON) | star |  |
| `omega` | `omega` | angular velocity | rad s^-1 | (JSON) | star |  |
| `moment_of_inertia` | `hi` | moment of inertia of each shell | g cm^2 | (JSON) | star |  |
| `specific_angular_momentum` | `hjm` | j of each shell | cm^2 s^-1 | (JSON) | star |  |
| `rotational_energy` | `hkerot` | rotational kinetic energy of each shell | erg | (JSON) | star | units not checked |
| `rotational_energy_old` | `hkeroto` | the same at the start of the step | erg | (JSON) | old | units not checked |
| `distortion_fp` | `fp` | distortion term f_P (FPFT) |  | (JSON) | star |  |
| `distortion_ft` | `ft` | distortion term f_T (FPFT) |  | (JSON) | star |  |
| `equivalent_radius` | `r0` | radius r_0 of each equipotential | cm | (JSON) | star |  |
| `radau_eta2` | `eta2` | eta_2 from Radau's equation |  | (JSON) | star |  |
| `dinertia_domega` | `qiw` | dI / dOmega of each shell (GETROT, MOMI) |  | (JSON) | star | units not checked |
| `mean_gravity` | `hg` | mean gravity <g> on the equipotential | cm s^-2 | (JSON) | star |  |
| `angular_momentum_start_iteration` | `hjm0` | start-of-step j for the structure-rotation iteration | cm^2 s^-1 | (JSON) | old | a copy of start? (formerly COMMON/ORIGSTART/) |
| `composition_start_iteration` | `hcompp0` | start-of-step composition for that iteration | mass fraction | (15, JSON) | old | a copy of start? (formerly COMMON/ORIGSTART/) |
| `luminosity_by_source` | `tlumx` | luminosities by source (pp I-III, CNO, ...) | L_sun | (8) | star | units not checked |
| `envelope_triangle_log_l` | `tril` | envelope triangle: log L | log10 L_sun | (3) | star |  |
| `envelope_triangle_log_teff` | `trit` | envelope triangle: log Teff | log10 K | (3) | star |  |
| `envelope_triangle_log_p` | `ps` | envelope triangle: P at the fit | log10 dyn cm^-2 | (3) | star |  |
| `envelope_triangle_log_t` | `ts` | envelope triangle: T at the fit | log10 K | (3) | star |  |
| `envelope_triangle_log_r` | `rs` | envelope triangle: r at the fit | log10 cm | (3) | star |  |
| `envelope_fit_coefficients` | `cfenv` | the envelope's fit coefficients |  | (9) | star |  |
| `starin_v` | `v` | STARIN's V |  | (12) | run | meaning not checked |
| `mixed_zones` | `mxzone` | mixed zones (bottom, top) | shell index | (12, 2) | star |  |
| `mixed_zones_old` | `mxzon0` | mixed zones before | shell index | (12, 2) | old |  |
| `radiative_zones` | `mrzone` | radiative zones | shell index | (13, 2) | star |  |
| `henyey_c` | `hhc` | CRRECT's work array |  | (JSON) | work |  |
| `henyey_a` | `hha` | CRRECT's work array |  | (4, 2, JSON) | work |  |
| `henyey_b` | `hhb` | CRRECT's work array |  | (4, JSON) | work |  |
| `first_guess_log_p_rate` | `hpp` | CRRECT's work array (log P) |  | (JSON) | work | read by step_store_rates: carried? |
| `first_guess_log_t_rate` | `htt` | CRRECT's work array (log T) |  | (JSON) | work | read by step_store_rates: carried? |
| `max_correction` | `hmax` | CRRECT's largest corrections |  | (4) | work |  |
| `max_correction_shell` | `nhmax` | where they are | shell index | (4) | work |  |
| `stored_energies` | `estore` | CRRECT's ESTORE |  | (4) | work | meaning not checked |
| `surface_values` | `hsrf` | CRRECT's HSRF |  | (6) | work | meaning not checked |
| `log_luminosity` | `bl` | surface luminosity | log10 L_sun |  | star |  |
| `log_teff` | `teffl` | effective temperature | log10 K |  | star |  |
| `mass` | `smass` | total mass | M_sun |  | star |  |
| `log_total_mass` | `hstot` | total mass | log10 g |  | star |  |
| `age` | `dage` | age | Gyr |  | star |  |
| `step_years` | `ddage` | the step | yr |  | star |  |
| `timestep` | `delts` | the time step | s |  | star |  |
| `timestep_htimer` | `deltsh` | HTIMER's time step | s |  | star |  |
| `timestep_previous` | `delts0` | the previous time step | s |  | star |  |
| `envelope_triangle_size` | `ftri` | the envelope triangle size |  |  | star | meaning not checked |
| `max_omega_change` | `dwmax` | largest change of Omega (HTIMER) |  |  | star | units |
| `log_g` | `gl` | surface gravity (WRTOUT: CGL + STOTAL - 2 RL) | log10 cm s^-2 |  | star |  |
| `total_angular_momentum` | `sjtot` | total angular momentum | g cm^2 s^-1 |  | star |  |
| `total_rotational_energy` | `skerot` | total rotational kinetic energy | erg |  | star |  |
| `envelope_fit_mass_old` | `senvold` | the previous fitting point | log10(m/M) |  | carried |  |
| `convective_velocity` | `vel` | convective velocity at STARIN's last TPGRAD call (the surface shell) | cm s^-1 |  | star |  |
| `mixing_length` | `cmixl` | mixing length alpha | pressure scale heights |  | star |  |
| `mass_for_output` | `xmsol` | the mass kept for the output | M_sun |  | run |  |
| `n_shells` | `m` | number of shells in use |  |  | star |  |
| `model_number` | `model` | the model number |  |  | star |  |
| `core_shell` | `jcore` | H-burning shell / core edge | shell index |  | star | meaning per FINDSH |
| `envelope_base_shell` | `jenv` | base of the surface convection zone | shell index |  | star |  |
| `envelope_base_shell_start` | `jenv0` | the same at the step start | shell index |  | old |  |
| `shell_begin` | `jxbeg` | H-burning shell: inner edge | shell index |  | star |  |
| `shell_end` | `jxend` | H-burning shell: outer edge | shell index |  | star |  |
| `shell_middle` | `jxmid` | H-burning shell: middle | shell index |  | star |  |
| `n_radiative_zones` | `nrzone` | CONVEC's radiative zones |  |  | star |  |
| `n_mixed_zones` | `nzone` | CONVEC's mixed zones |  |  | star |  |
| `n_mixed_zones_old` | `nzone0` | the same before |  |  | old |  |
| `iterations_done` | `itdone` | CRRECT's iterations done |  |  | work |  |
| `starin_ikut` | `ikut` | STARIN's IKUT |  |  | work | meaning not checked; name provisional |
| `store_index` | `istore` | CRRECT's ISTORE |  |  | work | meaning not checked |
| `in_atmosphere` | `latmo` | CRRECT's flag (whether an EOS call is in the atmosphere) |  |  | work |  |
| `want_derivatives` | `lderiv` | CRRECT's flag (whether derivatives are wanted) |  |  | work |  |
| `mixed` | `lmix` | CRRECT's flag |  |  | work |  |
| `conductive_opacity` | `locond` | CRRECT's flag |  |  | work |  |
| `new_envelope` | `lnew` | a new envelope triangle is needed |  |  | star |  |
| `burning_shell` | `lshell` | a H-burning shell exists |  |  | star |  |
| `new_fitting_point` | `lnewfit` | the fitting point moved (accretion) |  |  | star |  |
| `rotation_summary` | `lprt0` | rotation summary printed |  |  | run |  |
| `diverged` | `large` | the iteration diverged |  |  | star |  |
| `reset` | `lreset` | HPOINT's reset flag |  |  | star |  |
| `kind_card` | `nk` | the kind card |  |  | run |  |
| `pass_number` | `modeln` | the pass of its model loop |  |  | run |  |
| `next_output_age` | `nao` | the next of the ages AGEOUT |  |  | run |  |
| `computed` | `lpunch` | a model was calculated |  |  | run |  |
| `pulse_output` | `lsavpu` | LPULSE as read |  |  | run |  |
| `star_calibration` | `lstar` | the star calibration's flag |  |  | run |  |
| `star_matched` | `lpassr` | the star is matched |  |  | run |  |
| `star_calibration_alpha` | `alri` | the star calibration's value |  |  | run |  |
| `pulse_last_l` | `pol1` | PDIST's last point |  |  | run |  |
| `pulse_last_t` | `pot1` | PDIST's last point |  |  | run |  |
| `pulse_last_age` | `poa1` | PDIST's last point |  |  | run |  |
| `pulse_length` | `polen` | PDIST's last point |  |  | run |  |
| `mixture_name` | `compmix` | the mixture's name |  |  | run |  |
| `old_log_pressure` | `hpo` | old log P | log10 dyn cm^-2 | (JSON) | old |  |
| `old_log_temperature` | `hto` | old log T | log10 K | (JSON) | old |  |
| `old_log_radius` | `hro` | old log r | log10 cm | (JSON) | old |  |
| `old_luminosity` | `hlo` | old L | L_sun | (JSON) | old |  |
| `old_log_density` | `hdo` | old log rho (also HPOINT scratch) | log10 g cm^-3 | (JSON) | old |  |
| `old_composition` | `hcompp` | old composition | mass fraction | (15, JSON) | old |  |
| `old_log_mass` | `hss` | old mass coordinates | log10 g | (JSON) | old | units not stated in the glossary |
| `old_convective` | `lco` | old convective flags |  | (JSON) | old |  |
| `old_convective_rotation` | `lczo` | old convective flags for GETROT |  | (JSON) | old | what it flags, as against lco |
| `old_log_teff` | `tefflo` | old log Teff | log10 K |  | old |  |
| `old_surface_luminosity` | `hlsuro` | old surface L | L_sun |  | old |  |
| `old_omega` | `wold` | old Omega | rad s^-1 | (JSON) | old |  |
| `old_specific_angular_momentum` | `hjx` | old j | cm^2 s^-1 | (JSON) | old |  |
| `old_moment_of_inertia` | `hio` | old I (read nowhere) | g cm^2 | (JSON) | old |  |
| `old_mean_gravity` | `hgo` | old <g> | cm s^-2 | (JSON) | old |  |
| `old_equivalent_radius` | `r0x` | old r_0 | cm | (JSON) | old |  |
| `old_radau_eta2` | `eta2x` | old eta_2 |  | (JSON) | old |  |
| `old_li6_rate` | `rli60` | old 6Li proton-capture rate | s^-1 | (JSON) | old |  |
| `old_li7_rate` | `rli70` | old 7Li rate | s^-1 | (JSON) | old |  |
| `old_be9_rate` | `rbe90` | old 9Be rate | s^-1 | (JSON) | old |  |
| `old_deuterium_rate` | `drate0` | old deuterium burning rate | s^-1 | (JSON) | old | units not checked |
| `log_t_rate` | `htt0` | d log T / dt over the last step | s^-1 | (JSON) | carried |  |
| `log_p_rate` | `hpp0` | d log P / dt | s^-1 | (JSON) | carried |  |
| `luminosity_rate` | `hll0` | relative dL / dt | s^-1 | (JSON) | carried |  |
| `log_r_rate` | `hrr0` | d log r / dt | s^-1 | (JSON) | carried |  |
| `cz_base_radius_start` | `rbase0` | convection-zone base at the step start | cm |  | carried |  |
| `li6_burning_old` | `bli6old` | CZ-averaged 6Li rate, previous step | ln s^-1 |  | carried |  |
| `li7_burning_old` | `bli7old` | the same for 7Li | ln s^-1 |  | carried |  |
| `be9_burning_old` | `bbe9old` | the same for 9Be | ln s^-1 |  | carried |  |
| `light_burning_stored` | `lbliold` | the three hold end-of-step rates |  |  | carried |  |
| `envelope_base_shell_end` | `jenvos` | the envelope's base at the step end | shell index |  | carried |  |
| `overturn_time` | `taucz` | convective overturn time | s |  | carried |  |
| `overturn_time_start` | `taucz0` | the same at the step start | s |  | carried |  |
| `log_p_photosphere` | `pphot` | photospheric P | log10 dyn cm^-2 |  | carried |  |
| `log_p_photosphere_start` | `pphot0` | the same at the step start | log10 dyn cm^-2 |  | carried |  |
| `wind_step_fraction` | `fracstep` | fraction of the step for the wind |  |  | carried |  |
| `overshoot_start` | `pscal0` | overshoot distance at the step start | cm |  | carried |  |
| `overshoot_end` | `pscal1` | overshoot distance at the step end | cm |  | carried |  |
| `envelope_fit_mass` | `senv` | the envelope fitting point | log10(m/M) |  | carried |  |
| `log_total_mass_comp` | `stotal` | log M (COMP_MOD copy of hstot) | log10 g |  | carried | duplicate of log_total_mass? |
| `surface_x_table` | `xnew` | surface X of the current surface opacity table | mass fraction |  | carried | a cache of the opacity family? |
| `surface_z_table` | `znew` | surface Z of the same | mass fraction |  | carried | a cache of the opacity family? |
| `age_total` | `sage` | total age for disk locking | Gyr |  | carried | duplicate of age? |
| `saha_guess` | `e`, `sahex1`, `sahex2` | Saha's starting guess: electrons per atom, He+ and He++ fractions (eqsaha.f's SAVE'd E, SAHEX1, SAHEX2; pyrec's eqsaha.sv, the kernels' ssv) |  | (3) | carried |  |
| `structure_timestep_on` | `lptime` | whether HTIMER's structure criterion (PTIME) is on (the setting LPTIME, switched off for good near the ZAMS) |  |  | carried |  |
| `molecular_opacity_table` | `capalex06` | Ferguson et al. 2005 (ALEX06) molecular log kappa at (molecular_table_x, molecular_table_z) (ALEX06TAB) | log10 cm^2 g^-1 | (85, 19) | carried |  |
| `molecular_table_x` | `xe` | the X of molecular_opacity_table | mass fraction |  | carried |  |
| `molecular_table_z` | `ze` | the Z of molecular_opacity_table | mass fraction |  | carried |  |
| `surface_opal_table` | `cappae` | OPAL 1995 log kappa at X = surface_opal_table_x, Z = ZTAB (OP95XTAB) | log10 cm^2 g^-1 | (70, 19) | carried |  |
| `surface_opal_table_x` | `xop95` | the X of surface_opal_table | mass fraction |  | carried |  |
| `network_saved` | `ssv` | engeb's SAVE'd scalars (F1-F4, RHO, T9, T9M1, T9M12, T9M13, T9M23, T9P13, TM1, XXL8, Z58, Z28, BE7PROTON, BE7ELECTRON, CONVERT) |  | (18) | carried | read only below TCUT(1) (stale there: the suspected bug on engeb.f's page); changes the neutrino-flux output when TCUT(1) > 6 |
| `mean_molecular_weight` | `hamu` | mean molecular weight, fully ionized (PHYSIC) |  | (JSON) | star |  |
| `thermal_diffusivity` | `thdif` | radiative thermal diffusivity (VISCOS) | cm^2 s^-1 | (JSON) | star | units not checked |
| `viscosity` | `visc` | kinematic viscosity (VISCOS) | cm^2 s^-1 | (JSON) | star | units not checked |
| `shear_limit` | `qwrmax` | largest dOmega/dln r stable against shear (PHYSIC) | rad s^-1 | (JSON) | star | units not checked |

## The caches

What the defaults keep as caches, each rebuilt by its family or shown not to change results:

- **The tables** (opacity, EOS, atmosphere), read once at the setup into pyrec's modules, and passed to the kernels as data (`kernel_args()`).
- **The tables' search guesses:** the EOS's SCV stencil (`IDTSCV`, `IDP`) and OPAL's `K3`, `L2`; the opacity's table indices (`IT`, `ID`), getopal95's, and condopacp's guesses. Resetting the EOS's at every point changed no result, and the copy test left all of them unrestored with the copy identical.
- **Each family's settings,** read from the run's settings (still pyrec's modules, filled from YREC's namelists) into the kernels' data.

## Values YREC keeps between calls

YREC's `SAVE`d locals, `DATA`-initialized state, and cached tables, as placed so far:

| Value | Home | Why |
| --- | --- | --- |
| eqsaha's `E`, `SAHEX1`, `SAHEX2` | `State` (`saha_guess`) | the next call's starting guess; it changes results |
| engeb's `SAVE`d scalars | `State` (`network_saved`) | read below `TCUT(1)`, where they can change the neutrino-flux output |
| `LPTIME` | `State` (`structure_timestep_on`) | a setting HTIMER writes; the copy test |
| alot06's and llot95e's surface tables, with their X and Z | `State` | rebuilt only past a tolerance; the copy test |
| the tables' search guesses (EOS, opacity) | cache | the EOS's reset at every point with no change; the copy test |
| eqstat2's saved Saha derivatives, its number fractions | work arrays | set before they are read, in the same call |
| engeb's `SAVE`d arrays; mix's and coefft's rate arrays; `ctol_mod`'s `FCORR` | work arrays | set before they are read at each call |
| envint's `SAVE`s (`TAUP`, `OP`, `DP`, the step counts) | pyrec's modules, for now | the copy test left them unrestored with the copy identical; they feed later calls and printed counts (suspected bugs 3 and 4 on [envint.f](../../yrec-map/notes/envint.f.md)'s page) |
| `deuter_mod`'s `JCZ`; hpoint's, htimer's, ptime's, and getnewenv's `SAVE`d arrays; the output modules' | pyrec's modules, for now | the copy test left them unrestored with the copy identical |

The values in the last two rows changed no result on the ZAMS case; where each finally lives, and whether the test is rerun on a case with rotation, diffusion, and mass loss before that is settled, is open. Which of YREC's saved values carry information in the runs the test has not covered stays question 5 of [the overview](overview.md).
