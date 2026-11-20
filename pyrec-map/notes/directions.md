# Directions from MESA

*Part of [A new design for YREC](overview.md). The directions in which pyrec could grow beyond YREC, family by family, from a comparison with [MESA](https://mesastar.org/) (Modules for Experiments in Stellar Astrophysics): for each, what MESA does, what YREC does, and where pyrec's interfaces leave room. None is built: The defaults reproduce YREC, and these directions may be implemented later, by pyrec's developers or by its readers. No interface may rule one out ([The families](families.md)).*

**Sources.** MESA: its documentation for release r26.4.1 ([controls][ctl], [changelog][chl], [test suite][ts], [`auto_diff`][ad], [troubleshooting][trb]) and for `latest` ([EOS overview][eos], [changelog][chl-latest]), and its instrument papers, cited as MESA I to VI (references at the end). YREC: the release paper, Pinsonneault et al. 2026 ([arXiv:2603.25792][yp]), cited by section; its documentation at commit 7be4133 ([physics namelist][nml2], [control namelist][nml1], [microphysics][micro]) and its [`KNOWN_ISSUES.md`][ki]; this site's pages for the code. A MESA feature in `main` is unreleased as of Nov 18, 2026.

<a id="eos"></a>

## The equation of state (`eos`)

- **MESA** blends its components in order of precedence, CMS (experimental, off by default), Skye, PC, FreeEOS, OPAL/SCVH, and HELM, with an ideal-gas backstop ([EOS overview][eos]); MESA VI describes the default blend with Skye (its §4), which is on by default since r21.12.1.
- **YREC** recommends the OPAL 2005/2006 EOS (`LOPALE06`), uses SCV (Saumon et al. 1995) outside OPAL's table (`LSCV`), and keeps the Yale EOS (Saha, degeneracy from Fermi tables, Debye-Hückel) as a backup, whose semi-analytic derivatives serve the solution. The tie-breaker is OPAL > SCV > Yale, ramped near the tables' edges, where thermodynamic consistency is not preserved; OPAL's metal content is fixed per run, so settling cannot change it ([paper §2.3.1][yp]; [microphysics][micro]; [physics namelist][nml2]).
- **Room in pyrec.** The EOS's `point` takes the point's full composition, not only X and Z with one metal mixture per run, and returns every derivative the solver uses: A family blending several EOSs consistently over any composition fits the interface.

<a id="opacity"></a>

## Opacities (`opacity`)

- **MESA's** `kap` module gives radiative and conductive opacities ([home page][home]); OPLIB Type 1 tables were added in r24.08.1 ([changelog][chl]), and MESA VI updates the molecular, Compton, and conductive opacities.
- **YREC** has conductive opacities (Cassisi et al. 2007 in the paper; Potekhin's tables and routine in the code, [condopacp.f](../../yrec-map/notes/condopacp.f.md)), molecular opacities (Ferguson et al. 2005, YREC's ALEX06 tables, below $`\log T = 4.0`$), atomic ones (OP or OPAL, above 4.1, with a ramp between), and OPAL's C/O-rich tables for helium-burning regions, each table for a fixed heavy-element mixture ([paper §2.3.2][yp]; [getopac.f](../../yrec-map/notes/getopac.f.md)).
- **Room in pyrec.** The opacity's `point` takes X, Z, and the ionization, and its tables are the family's data: Another table set is another family.

<a id="atmosphere"></a>

## Atmospheres, the boundary, and starspots (`atmosphere`)

- **MESA** offers `atm_option` `T_tau`, `table`, `irradiated_grey`, `fixed_Teff`, `fixed_Tsurf`, `fixed_Psurf`, and `fixed_Psurf_and_Tsurf`. Its $`T`$–$`\tau`$ relations are Eddington, solar Hopf, Krishna Swamy, and Trampedach solar, and its tables `photosphere`, `tau_100` (the default), `tau_10`, `tau_1`, `tau_1m1`, `WD_tau_25`, and `DB_WD_tau_25` ([controls][ctl]). Starspots came in MESA VI, which implements YREC's SPOTS treatment and calls it "equivalent": the same filling factor and contrast, the boundary condition modified through a magnetic pressure, and the radiative gradient in the convection zone reduced, so that MESA's spots act in the interior too (MESA VI, §7.1).
- **YREC** has `KTTAU` 0 (Eddington gray), 1 (Krishna Swamy), 2 (the Harvard-Smithsonian reference atmosphere), 3 (Kurucz 1993), 4 (Allard and Hauschildt 1995; solar Z only), and 5 (Castelli and Kurucz 2003), the tables falling back to gray off their hot edge ([envint.f, lines 228–266][envint]); its outer fitting point lies well below the photosphere, with the envelope integrated at three ($`L`$, $`T_\mathrm{eff}`$) points, the "envelope triangle" ([paper §2.2, §2.3.6][yp]; [surfbc.f](../../yrec-map/notes/surfbc.f.md)). Its starspots block flux and modify the surface boundary condition, with the filling factor and contrast fixed for a run (`SPOTF`, `SPOTX`; [paper §2.5][yp]).
- **Room in pyrec.** What the solver needs from an atmosphere family is the fitting point's $`\log P`$, $`\log T`$, and $`\log r`$ as functions of $`L`$ and $`T_\mathrm{eff}`$, with their derivatives; the $`T`$–$`\tau`$ relation, the tables, the fitting mass, and the triangle are the default's own. A photosphere condition, an irradiated surface, or another table set is another family.

<a id="network"></a>

## Nuclear reactions and neutrinos (`network`)

- **MESA** has fully coupled networks "with hundreds of isotopes" (MESA III), weak rates on the fly (MESA III), operator-split burning (MESA VI), an `other_screening` hook (r21.12.1), and thermal neutrino losses in its `neu` module ([home page][home]).
- **YREC** has a fixed network: non-equilibrium burning of H, ³He, ⁴He, ¹²C, ¹³C, ¹⁴N, ¹⁶O, and ¹⁸O (the pp chain, CNO, triple alpha, and three alpha captures), pre-main-sequence deuterium burning, and ⁶Li, ⁷Li, and ⁹Be as trace species; weak screening by default, intermediate and strong available; thermal neutrino losses from Itoh et al. 1996, and solar neutrino fluxes ([paper §2.3.4][yp]; [engeb.f](../../yrec-map/notes/engeb.f.md); [sneut.f](../../yrec-map/notes/sneut.f.md)). It is not adaptive, and its high-mass runs end at core helium exhaustion.
- **Room in pyrec.** The network's size and species are the family's data (`species`, `rate_names`), and its `point` reads the composition array whole; a larger network, other rates, or other screening is a subclass with its own kernel.

<a id="convection"></a>

## Convection and mixing (`convection`)

- **MESA** offers `MLT_option` `Cox`, `ML1`, `ML2`, `Mihalas`, `Henyey`, `TDC` (time-dependent convection, the default in r26.4.1, introduced in MESA VI), and `none`, with the Ledoux criterion optional; overshoot schemes `exponential`, `step`, and `other`; semiconvection (Langer 1985) and thermohaline mixing (Kippenhahn; Traxler et al. 2011; Brown et al. 2013), both with the Ledoux criterion ([controls][ctl]; MESA II, IV, V, VI).
- **YREC** has Böhm-Vitense's MLT only, with the Schwarzschild criterion, and an option to take the adiabatic gradient in convective cores; step overshoot in pressure scale heights for cores, envelopes, and intermediate zones, as overmixing, with adiabatic overshoot as an experimental option. It has semiconvection after Castellani et al. 1971 (`LSEMIC`). Thermohaline mixing, MLT variants, exponential overshoot, and time-dependent convection are not in YREC ([paper §2.3.3][yp]; [tpgrad.f](../../yrec-map/notes/tpgrad.f.md); [oversh.f](../../yrec-map/notes/oversh.f.md); [sconvec.f](../../yrec-map/notes/sconvec.f.md)).
- **Room in pyrec.** The variant of the gradient is the class's, not the signature's; mixing enters as diffusion coefficients (`mixing_coefficients`) that overshoot, semiconvection, thermohaline mixing, and rotation can each add to. The gradient's `point` does not yet take a composition gradient (for the Ledoux criterion and thermohaline mixing) or the previous velocity and step (for time-dependent convection): an input each, to be added when such a family is written.

<a id="diffusion"></a>

## Diffusion and settling (`diffusion`)

- **MESA** has element diffusion (`do_element_diffusion`; MESA IV, coefficients in VI) and radiative levitation since MESA III, improved in V and VI ([controls][ctl]).
- **YREC** has settling and thermal diffusion (Burgers' equations as solved by Thoul et al. 1994) for helium, the metals as one group, and ⁶Li, ⁷Li, and ⁹Be (`LDIFY`, `LDIFZ`, `LDIFLI`); the paper names radiative levitation but says YREC includes settling and thermal diffusion only ([paper §2.4][yp]; [microdiff.f](../../yrec-map/notes/microdiff.f.md)).
- **Room in pyrec.** The diffusion stage takes the `State` whole and extra diffusion coefficients from other mixing, and gives its own (`coefficients`), so that a family with more species or radiative accelerations fits.

<a id="rotation"></a>

## Rotation (`rotation`)

- **MESA** treats shellular rotation; since MESA V its distortion factors are analytic fits to the Roche potential of a point mass, valid to about 0.9 of critical rotation. It transports angular momentum and composition by diffusion (MESA II), with a Spruit-Tayler dynamo term (`D_ST`; [controls][ctl]); angular-momentum-conserving remapping is in `main` ([changelog, latest][chl-latest]).
- **YREC** treats rotation in pseudo-2D: uniform rotation on equipotentials, whose shapes it solves with the potential's quadrupole term, and correction factors in the structure equations ([paper §2.6.2][yp]; [fpft.f](../../yrec-map/notes/fpft.f.md)); its transport covers meridional circulation, secular shear, and the GSF instability, with μ-gradient inhibition and a free mixing efficiency, and magnetic transport two ways, forced solid-body rotation and a constant extra diffusion ([paper §2.6.3, §2.6.5][yp]; [vcirc.f](../../yrec-map/notes/vcirc.f.md)). MESA's line of treatment descends from YREC's (Heger et al. 2000, from Pinsonneault et al. 1989).
- **Angular-momentum loss.** In MESA, a magnetic wind's torque is written by the user, through the `other_torque` hook; its test case `magnetic_braking` brakes a 15 M☉ star this way, after Weber and Davis 1967 ([magnetic_braking][mb]), and `accreted_material_j` adds the angular momentum that accreted mass carries ([accreted_material_j][amj]). YREC has three wind laws for low-mass stars, with saturation and Rossby scaling (Krishnamurthi et al. 1997; van Saders and Pinsonneault 2013, after Matt et al. 2012; a custom law), and disk locking for a set time at a set period ([paper §2.6.4][yp]; [nml2]).
- **Room in pyrec.** Transport, the surface's angular-momentum loss (`torque`), and the mixing (`mixing_coefficients`) are separate methods of the base class, so a family can change one alone.

<a id="mass-loss"></a>

## Mass loss and accretion (`mass_loss`)

- **MESA** offers the wind schemes `Reimers`, `Blocker`, `de Jager`, `van Loon`, `Nieuwenhuijzen`, `Vink`, `Dutch`, and `Bjorklund` (for hot winds, the red giant branch, and the AGB; [controls][ctl]); its accretion treatment improved in MESA III.
- **YREC's** mass loss is experimental and partly implemented: `LMDOT` with a constant rate (loss or gain) or a Reimers law ([physics namelist][nml2]; [massloss.f](../../yrec-map/notes/massloss.f.md); `KNOWN_ISSUES.md`, issue 12).
- **Room in pyrec.** The base class has the signed rate (`rate`: negative for winds, positive for accretion), which the stage applies; the recipe is the family's.

<a id="solver"></a>

## The solver: derivatives and diagnostics (`solver`)

- **MESA** solves structure and composition fully coupled (MESA I), with derivatives carried by its `auto_diff` types, generated in forward mode; assigning a derivative-carrying value to a plain real is not supported, "because we don't want to accidentally lose the derivative information" ([`auto_diff`][ad]). Residual plots are in `main` ([changelog, latest][chl-latest]). Energy conservation is central to MESA V and VI.
- **YREC** relaxes the four structure equations by Henyey's method, with the composition advanced apart, in up to four iteration levels; its derivatives are analytic, with numerical ones as a slow option; its notes record that the Jacobian and the EOS's second derivatives are not consistent (`KNOWN_ISSUES.md`, issue 40) and a period-2 limit cycle in the corrections (issue 41) ([paper §2.2, §2.3.5][yp]; [crrect.f](../../yrec-map/notes/crrect.f.md)). Its `.short` file logs each iteration's convergence; no global energy-conservation diagnostic was found.
- **Room in pyrec.** The solver takes its derivatives from the physics families' outputs, never by differentiating a family, so a family may supply them by automatic differentiation; `residuals` is declared for diagnostics, and a failed solve is returned, not raised.

<a id="timestep"></a>

## The time step and failed steps (`timestep`)

- **MESA** has "sophisticated timestep controls" (MESA I; `time_delta_coeff`, `varcontrol_target`), with soft and hard limits on changes, and retries and redos (`max_number_retries`; [controls][ctl]).
- **YREC** takes the most restrictive of several limits (burning, structure changes on the pre-main sequence, rotation, the growth per step; [paper §2.2][yp]; [htimer.f](../../yrec-map/notes/htimer.f.md)). It does not retry: A model that fails to converge stops the run ([starin.f, lines 227–235][starin]), and `KNOWN_ISSUES.md` notes that "A step retry at a smaller timestep after a failed solve would add robustness" (issue 40).
- **Room in pyrec.** The model may retry a failed step from the start of the step with a shorter step; the default stops, as YREC does.

<a id="rezoner"></a>

## The mesh (`rezoner`)

- **MESA** has an adaptive mesh (MESA I; `mesh_delta_coeff`, `max_allowed_nz`; [controls][ctl]).
- **YREC** rezones at the start of each step by limits on $`\Delta\log m`$, $`\Delta L`$, and $`\Delta\log P`$ in the envelope, at the base of the convection zone, and in the core, keeping the discontinuities in X, Z, and $`\Omega`$ ([paper §2.2][yp]; [hpoint.f](../../yrec-map/notes/hpoint.f.md)).
- **Room in pyrec.** The rezoner's controls are its own configuration, and the shells' number is the `State`'s.

<a id="numerics"></a>

## Numerics beyond the families

YREC is fast: On one thread its release paper measures it at about 8, 2, and 6 times faster than MESA r24.08.1 from the pre-main sequence to the ZAMS, from the ZAMS to the end of the main sequence, and from there to the tip of the red-giant branch, at similar mesh ([paper §3.1.1][yp]). Many of MESA's numerical choices buy robustness and stability at some cost in speed, so in pyrec each is weighed against what it costs a run.

- **Energy accounting.** Energy conservation, including during changes of mass, is central to MESA V and VI ([V][m5]; [VI][m6]). No global energy-conservation diagnostic was found in YREC. In pyrec it would be a diagnostic computed from the `State` after each step, an output beside the history.
- **Failed steps.** MESA removed its backups in r15140 ("MESA no longer has the concept of a 'backup'"; [changelog][chl]) and keeps retries and redos ([controls][ctl]). YREC stops the run when a model fails to converge ([The time step and failed steps](#timestep)).
- **Parallelism.** MESA runs one model on several threads with OpenMP (MESA I; its performance measured in MESA V), and its testing runs many cases side by side ([Wolf et al. 2023][mt]). The Fortran of YREC is single-threaded, and its Python package runs many models in parallel ([`python_package.md`][pyd]). pyrec keeps each model on one thread and runs many models side by side, so that the core-hours of a grid are saved; threads inside a model are a technique to try and report, not the default.
- **Reproducibility.** MESA III claimed "bit-for-bit consistency for all results across all the supported platforms" ([III][m3]); the testing paper finds most of MESA written to be bit-for-bit consistent across platforms, with checksums not yet tracked for some cases ([Wolf et al. 2023][mt-html]), and the MESA SDK gives a unified build (MESA II). YREC's tests compare outputs with references within a tolerance, and the references are not under version control (`KNOWN_ISSUES.md`, issue 32). pyrec's outputs are compared with YREC's byte for byte, and a copy of a model run on must match the original byte for byte ([The State](state.md)).

<a id="beyond"></a>

## Beyond the families

- **User hooks.** MESA has `run_star_extras` with `use_other_*` hooks ([controls][ctl]); YREC "was not designed with modular user inputs in mind" ([paper §1][yp]), and users edit the source. In pyrec, the step's stages, the hooks between them, the controls at the start of each step, and the retry are where a reader adds new physics without editing the framework ([the overview](overview.md), Looking inside).
- **Oscillation codes and photometry.** MESA links GYRE and ADIPLS, supporting the interfaces, not the packages ([troubleshooting][trb]; MESA II, III), and has synthetic photometry (`colors`) since r25.12.1 ([changelog][chl]). YREC writes its own pulsation files along the track ([pdist.f](../../yrec-map/notes/pdist.f.md)), with no GYRE or ADIPLS binding. In pyrec these would be outputs of the model, beside the history.
- **Binaries, hydrodynamics, and radial pulsation.** MESA has a `binary` module and implicit hydrodynamics with shocks (MESA III), a Riemann solver and STELLA coupling (MESA IV), and radial stellar pulsation, RSP (MESA V); none is in YREC, which is hydrostatic.
- **Evolutionary phases.** MESA evolves stars through the helium flash (MESA V), the AGB's thermal pulses (MESA I), to cooling white dwarfs (MESA IV), and to core collapse (MESA I, III). YREC ends a run at helium ignition in a degenerate core, making low-mass core-helium-burning models by rescaling instead (`KNOWN_ISSUES.md`, issue 33); the AGB is outside the domain it is optimized for, no white-dwarf case was found, and its high-mass runs end at core helium exhaustion ([paper §1.1, §3.3.2][yp]).

## References

MESA's instrument papers and its testing paper:

- MESA I: Paxton et al. 2011, ApJS 192, 3, [doi:10.1088/0067-0049/192/1/3][m1] ([ADS](https://ui.adsabs.harvard.edu/abs/2011ApJS..192....3P)).
- MESA II: Paxton et al. 2013, ApJS 208, 4, [doi:10.1088/0067-0049/208/1/4][m2] ([ADS](https://ui.adsabs.harvard.edu/abs/2013ApJS..208....4P)).
- MESA III: Paxton et al. 2015, ApJS 220, 15, [doi:10.1088/0067-0049/220/1/15][m3] ([ADS](https://ui.adsabs.harvard.edu/abs/2015ApJS..220...15P)).
- MESA IV: Paxton et al. 2018, ApJS 234, 34, [doi:10.3847/1538-4365/aaa5a8][m4] ([ADS](https://ui.adsabs.harvard.edu/abs/2018ApJS..234...34P)).
- MESA V: Paxton et al. 2019, ApJS 243, 10, [doi:10.3847/1538-4365/ab2241][m5] ([ADS](https://ui.adsabs.harvard.edu/abs/2019ApJS..243...10P)).
- MESA VI: Jermyn et al. 2023, ApJS 265, 15, [doi:10.3847/1538-4365/acae8d][m6] ([ADS](https://ui.adsabs.harvard.edu/abs/2023ApJS..265...15J)).
- Wolf, Schwab, Farmer, and Bauer 2023, "Testing Modules for Experiments in Stellar Astrophysics (MESA)," ApJS 269, 50, [doi:10.3847/1538-4365/acffbf][mt] ([ADS](https://ui.adsabs.harvard.edu/abs/2023ApJS..269...50W)).

YREC: Pinsonneault et al. 2026, "The YREC Stellar Evolution Code: Public Data Release," ApJ 1006, 220, [doi:10.3847/1538-4357/ae71cf][ypdoi], [arXiv:2603.25792][yp] ([ADS](https://ui.adsabs.harvard.edu/abs/2026ApJ..1006..220P)).

Compiled with AI assistance (Gemini's deep research, then Claude), each claim checked against the source cited; not vetted by YREC's or MESA's developers.

[m1]: https://doi.org/10.1088/0067-0049/192/1/3
[m2]: https://doi.org/10.1088/0067-0049/208/1/4
[m3]: https://doi.org/10.1088/0067-0049/220/1/15
[m4]: https://doi.org/10.3847/1538-4365/aaa5a8
[m5]: https://doi.org/10.3847/1538-4365/ab2241
[m6]: https://doi.org/10.3847/1538-4365/acae8d
[home]: https://mesastar.org/
[chl]: https://docs.mesastar.org/en/26.4.1/changelog.html
[chl-latest]: https://docs.mesastar.org/en/latest/changelog.html
[eos]: https://docs.mesastar.org/en/latest/eos/overview.html
[ctl]: https://docs.mesastar.org/en/26.4.1/reference/controls.html
[ts]: https://docs.mesastar.org/en/26.4.1/test_suite.html
[mb]: https://docs.mesastar.org/en/26.4.1/test_suite/magnetic_braking.html
[amj]: https://docs.mesastar.org/en/26.4.1/test_suite/accreted_material_j.html
[ad]: https://docs.mesastar.org/en/26.4.1/auto_diff/more_detail.html
[trb]: https://docs.mesastar.org/en/26.4.1/using_mesa/troubleshooting.html
[yp]: https://arxiv.org/abs/2603.25792
[ypdoi]: https://doi.org/10.3847/1538-4357/ae71cf
[nml1]: https://github.com/yreclab/yrec/blob/7be4133/docs/source/namelist_control.md
[nml2]: https://github.com/yreclab/yrec/blob/7be4133/docs/source/namelist_physics.md
[micro]: https://github.com/yreclab/yrec/blob/7be4133/docs/source/microphysics.md
[ki]: https://github.com/yreclab/yrec/blob/7be4133/KNOWN_ISSUES.md
[envint]: https://github.com/yreclab/yrec/blob/7be4133/src/envint.f#L228-L266
[starin]: https://github.com/yreclab/yrec/blob/7be4133/src/starin.f#L227-L235
[mt]: https://doi.org/10.3847/1538-4365/acffbf
[mt-html]: https://arxiv.org/html/2310.11618v1
[pyd]: https://github.com/yreclab/yrec/blob/7be4133/docs/source/python_package.md
