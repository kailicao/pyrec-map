# The families' names

*Part of [A new design for YREC](overview.md). Each family module's table of names: the descriptive name the object-oriented pyrec uses, beside YREC's name, written in lower case as the Fortran-tracking pyrec writes it. The tables are part of the code (`NAMES` in each module) and are generated from it, as is [the `State`'s table](state.md) (The fields). A name that is also a `State` field's means the same quantity.*

A YREC name may be a setting (marked "(setting)"), an argument of the routine the family wraps, or a module variable; where one descriptive name stands for several YREC values, or for part of an array, the entry says which. The meanings and units of the arguments are on [The families](families.md), and those of the module variables in the site's glossary (linked at the top of every page).

**One name per variable.** Each of YREC's variables has one descriptive name, the same in every table: `latmo` is `in_atmosphere` in the EOS, the atmosphere, the solver, and the `State`. A routine's arguments are mapped per routine: Where one YREC name stands for different quantities in different routines, each quantity has its own name and the entry names the routine (`x0` is `log_tau` in QATM and `log_pressure` in QENV). An argument a routine reads and sets keeps one name (`dl` is `log_density` in the EOS, the starting guess on entry and the result on return). The converse need not hold across modules: A routine's argument and the model's array of the same quantity share a descriptive name (`log_density` is the EOS's `dl` and the `State`'s `hd`). The few names that are YREC's own are the usual symbols for their quantities (`x`, `z`, `beta`, `omega`).

Two small modules hold what YREC's PHYSIC computed, since PHYSIC itself is dropped: the mean molecular weight (`composition.py`) and the shear's stability limit with the thermal diffusivity and viscosity (`shear.py`, used by rotation).

## `EOS` (`pyrec_oop/eos.py`)

| Descriptive name | YREC name |
| --- | --- |
| `log_temperature` | tl |
| `log_pressure` | pl |
| `log_density` | dl |
| `x` | x |
| `z` | z |
| `composition` | hcomp(:, j) |
| `ionization` | fxion |
| `dlnrho_dlnt` | qdt |
| `dlnrho_dlnp` | qdp |
| `want_derivatives` | lderiv |
| `in_atmosphere` | latmo |
| `saha_iterations` | ksaha |
| `debye_x` | xxdh |
| `debye_y` | yydh |
| `debye_z` | zzdh |
| `scv_stencil_t` | idtscv |
| `scv_stencil_p` | idp |
| `opal_k3` | k3 |
| `opal_l2` | l2 |
| `saha_guess` | e, sahex1, sahex2 |
| `temperature` | t |
| `pressure` | p |
| `density` | d |
| `beta` | beta |
| `beta_inverse` | betai |
| `radiation_term` | beta14 |
| `gas_constant_over_mu` | rmu |
| `ions_per_mass` | amu |
| `electrons_per_mass` | emu |
| `degeneracy` | eta |
| `cp` | qcp |
| `nabla_ad` | dela |
| `d2lnrho_dlnt2` | qdtt |
| `d2lnrho_dlnt_dlnp` | qdtp |
| `dnabla_ad_dlnt` | qat |
| `dnabla_ad_dlnp` | qap |
| `dcp_dlnt` | qcpt |
| `dcp_dlnp` | qcpp |
| `messages` | (pyrec: the kernel's flags) |
| `opal_status` | (pyrec: esac06's status) |
| `opal_density` | (pyrec: esac06's last density) |
| `opal_t6` | (pyrec: esac06's last t6) |

## `Opacity` (`pyrec_oop/opacity.py`)

| Descriptive name | YREC name |
| --- | --- |
| `log_density` | dl |
| `log_temperature` | tl |
| `x` | x |
| `z` | z |
| `ionization` | fxion |
| `kappa` | o |
| `log_kappa` | ol |
| `dlnkappa_dlnrho` | qod |
| `dlnkappa_dlnt` | qot |

## `Atmosphere` (`pyrec_oop/atmosphere.py`)

| Descriptive name | YREC name |
| --- | --- |
| `log_tau` | x0 (qatm) |
| `log_pressure` | y(1) (qatm); x0 (qenv) |
| `log_mass_fraction` | y(1) (qenv) |
| `log_temperature` | y(2) (qenv) |
| `log_radius` | y(3) (qenv) |
| `integrated` | y |
| `slopes` | dydx |
| `luminosity` | b |
| `distortion_fp` | fpl |
| `distortion_ft` | ftl |
| `log_g` | gl |
| `in_atmosphere` | latmo |
| `want_derivatives` | lderiv |
| `save_for_output` | lsave |
| `log_teff` | teffl |
| `x` | x |
| `z` | z |
| `log_luminosity` | bl |
| `log_total_mass` | hstot |
| `mixing_length` | cmixl |
| `expected_fit_log_pressure` | plim |
| `fit_point` | ie |
| `pulsation_output` | lpulpt |

## `Network` (`pyrec_oop/network.py`)

| Descriptive name | YREC name |
| --- | --- |
| `log_density` | dl |
| `log_temperature` | tl |
| `composition` | hcomp (rows read: x 1, y 2, xhe3 4, xc12 5, xc13 6, xn14 7, xo16 9, xo18 11, xh2 12) |
| `shell` | iu |
| `rates` | hr1-hr13, hf1, hf2 |
| `epsilon_pp1` | epp1 |
| `epsilon_pp2` | epp2 |
| `epsilon_pp3` | epp3 |
| `epsilon_cno` | ecn |
| `epsilon_triple_alpha` | e3al |
| `depsilon_dlnrho` | pep |
| `depsilon_dlnt` | pet |
| `epsilon` | sum1 |
| `be7_mass_fraction` | be7massfraction |
| `epsilon_alpha_capture` | ealpca |
| `epsilon_neutrino` | enu |
| `timestep` | delts |
| `level` | itlvl |
| `step_years` | ddage |
| `saved` | engeb's SAVE (ssv_names) |

## `Convection` (`pyrec_oop/convection.py`)

| Descriptive name | YREC name |
| --- | --- |
| `log_temperature` | tl |
| `temperature` | t |
| `log_pressure` | pl |
| `pressure` | p |
| `density` | d |
| `log_radius` | rl |
| `log_mass` | sl |
| `luminosity` | b |
| `kappa` | o |
| `dlnrho_dlnt` | qdt |
| `dlnrho_dlnp` | qdp |
| `dlnkappa_dlnt` | qot |
| `dlnkappa_dlnrho` | qod |
| `cp` | qcp |
| `nabla_ad` | dela |
| `d2lnrho_dlnt2` | qdtt |
| `d2lnrho_dlnt_dlnp` | qdtp |
| `dnabla_ad_dlnt` | qat |
| `dnabla_ad_dlnp` | qap |
| `dnabla_dlnt` | qact |
| `dnabla_dlnp` | qacp |
| `dnabla_dlnr` | qacr |
| `dcp_dlnt` | qcpt |
| `dcp_dlnp` | qcpp |
| `want_derivatives` | lderiv |
| `distortion_fp` | fpl |
| `distortion_ft` | ftl |
| `mixing_length` | cmixl |
| `overshoot_point` | iovim |
| `nabla` | del |
| `nabla_rad` | delr |
| `convective_velocity` | vel |
| `convective` | lconv |
| `log_teff` | teffl |

## `Diffusion` (`pyrec_oop/diffusion.py`)

| Descriptive name | YREC name |
| --- | --- |
| `timestep` | delts |
| `composition` | hcomp |
| `log_density` | hd |
| `log_pressure` | hp |
| `log_radius` | hr |
| `log_mass` | hs |
| `shell_mass` | hs1 |
| `log_total_mass` | hstot |
| `log_temperature` | ht |
| `convective` | lc |
| `n_shells` | m |
| `envelope_base_shell` | jenv |

## `Rotation` (`pyrec_oop/rotation.py`)

| Descriptive name | YREC name |
| --- | --- |
| `log_luminosity` | bl |
| `timestep` | delts |
| `max_omega_change` | dwmax |
| `distortion_fp` | fp |
| `distortion_ft` | ft |
| `composition` | hcomp |
| `log_density` | hd |
| `specific_angular_momentum` | hjm |
| `luminosity` | hl |
| `log_pressure` | hp |
| `log_radius` | hr |
| `log_mass` | hs |
| `shell_mass` | hs1 |
| `mass_between_centers` | hs2 |
| `log_total_mass` | hstot |
| `log_temperature` | ht |
| `convective` | lc |
| `n_shells` | m |
| `mass` | smass |
| `log_teff` | teffl |
| `radau_eta2` | eta2 |
| `mean_gravity` | hg |
| `moment_of_inertia` | hi |
| `omega` | omega |
| `dinertia_domega` | qiw |
| `equivalent_radius` | r0 |
| `envelope_base_shell_start` | jenv0 |
| `mixing_length` | cmixl |
| `rotation_summary` | lprt0 |

## `MassLoss` (`pyrec_oop/mass_loss.py`)

| Descriptive name | YREC name |
| --- | --- |
| `log_luminosity` | bl |
| `age` | dage |
| `timestep` | delts |
| `composition` | hcomp |
| `log_density` | hd |
| `specific_angular_momentum` | hjm |
| `log_pressure` | hp |
| `log_radius` | hr |
| `log_mass` | hs |
| `shell_mass` | hs1 |
| `mass_between_centers` | hs2 |
| `log_total_mass` | hstot |
| `log_temperature` | ht |
| `envelope_base_shell` | jenv |
| `new_envelope` | lnew |
| `n_shells` | m |
| `omega` | omega |
| `mass` | smass |
| `log_teff` | teffl |
| `envelope_fit_mass_old` | senvold |
| `new_fitting_point` | lnewfit |

## `Solver` (`pyrec_oop/solver.py`)

| Descriptive name | YREC name |
| --- | --- |
| `iterations_level1` | niter1 (setting) |
| `iterations_level2` | niter2 (setting) |
| `iterations_level3` | niter3 (setting) |
| `iterations_level4` | niter4 (setting) |
| `correction_factor` | fcorr (ctol_mod), from fcorr0 and fcorri (settings) |
| `new_triangle_always` | lnew0 (setting) |
| `extrapolate_guess` | lnews (setting) |
| `rotation_iterations` | itdif1 (setting; set to 1 without rotation) |
| `timestep` | delts |
| `diverged` | large |
| `converged` | lfini |
| `iterations_done` | itdone |
| `surface_condition` | lsbc |
| `level` | itlvl |
| `iterations` | niter |
| `new_envelope` | lnew |
| `reset` | lreset |
| `envelope_triangle_size` | ftri |
| `store_index` | istore |
| `log_luminosity` | bl |
| `log_teff` | teffl |
| `in_atmosphere` | latmo |
| `want_derivatives` | lderiv |
| `mixed` | lmix |
| `conductive_opacity` | locond |
| `envelope_base_shell_start` | jenv0 |
| `max_omega_change` | dwmax |
| `rotation_summary` | lprt0 |

## `Timestep` (`pyrec_oop/timestep.py`)

| Descriptive name | YREC name |
| --- | --- |
| `timestep` | delts |
| `timestep_htimer` | deltsh |
| `timestep_previous` | delts0 |
| `step_years` | ddage |
| `max_omega_change` | dwmax |
| `core_shell` | jcore |
| `shell_middle` | jxmid |
| `shell_begin` | jxbeg |
| `kind_card` | nk |
| `age` | dage |
| `limits` | atime (setting) |
| `end_age` | endage (setting, per kind card) |
| `end_age_set` | lendag (runloop_mod, per kind card) |

## `Rezoner` (`pyrec_oop/rezoner.py`)

| Descriptive name | YREC name |
| --- | --- |
| `n_shells` | m |
| `reset` | lreset |
| `core_shell` | jcore |
| `envelope_base_shell` | jenv |
| `total_angular_momentum` | sjtot |
| `total_rotational_energy` | skerot |
| `rotational_energy_old` | hkeroto |
| `convective_zone_shell` | jcz (deuter_mod; not in State) |
| `helium_flash` | lkuthe (setting) |
| `rotation` | lrot (setting) |
| `shell_begin` | jxbeg |
| `shell_middle` | jxmid |
| `shell_end` | jxend |
| `burning_shell` | lshell |
| `new_fitting_point` | lnewfit |
| `envelope_fit_mass_old` | senvold |
| `new_envelope` | lnew |

## `pyrec_oop/profiles.py`

| Descriptive name | YREC name |
| --- | --- |
| `log_mass` | hs |
| `log_temperature` | ht |
| `log_pressure` | hp |
| `log_radius` | hr |
| `luminosity` | hl |
| `composition` | hcomp |
| `log_density` | hd |
| `distortion_fp` | fp |
| `distortion_ft` | ft |
| `mean_gravity` | hg |
| `convective` | lc |
| `n_shells` | m |
| `log_teff` | teffl |
| `mixing_length` | cmixl |
| `nabla_rad` | sdel(1, :) |
| `nabla` | sdel(2, :) |
| `nabla_ad` | sdel(3, :) |
| `kappa` | so |
| `cp` | cp |
| `dlnrho_dlnt` | sqdt |
| `convective_velocity` | svel |
| `mean_molecular_weight` | hamu |
| `shear_limit` | qwrmax |

## `pyrec_oop/composition.py`

| Descriptive name | YREC name |
| --- | --- |
| `composition` | hcomp |
| `n_shells` | m |
| `x_env` | xenv |
| `y_env` | yenv |
| `z_env` | zenv |
| `he3_env` | y3env |
| `inverse_mu_ion_env` | amuenv |
| `mean_molecular_weight` | hamu |
| `ATOMIC_WEIGHT` | atomwt |

## `pyrec_oop/shear.py`

| Descriptive name | YREC name |
| --- | --- |
| `log_mass` | hs |
| `log_pressure` | hp |
| `log_density` | hd |
| `mean_gravity` | hg |
| `convective` | lc |
| `nabla` | sdel(2, :) |
| `nabla_ad` | sdel(3, :) |
| `n_shells` | m |
| `shear_limit` | qwrmax |
| `thermal_diffusivity` | thdif |
| `viscosity` | visc |
