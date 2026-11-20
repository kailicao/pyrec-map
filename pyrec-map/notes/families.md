# The families

*Part of [A new design for YREC](overview.md). Each family is a base class with a fixed set of inputs and outputs; the local families put their hot paths in compiled (Numba) static methods ([Writing a Numba family](numba.md)), the stage families are plain Python calling compiled kernels (Two kinds of family, below), and a family in plain Python also works, with a warning ([The compiled tree](tree.md)). Each family's default reproduces YREC bit for bit; today every default wraps the Fortran-tracking pyrec's routines, unchanged.*

Each section gives the family's base class and default, its interface (inputs, outputs, and units), its stage methods, and the routines its default replaces (their pages show the Fortran beside the Fortran-tracking pyrec). Each family's names beside YREC's are in [The families' names](names.md); the directions in which a family could grow beyond YREC are in [Directions from MESA](directions.md).

## Two kinds of family

- **Local families** (`eos`, `opacity`, `atmosphere`, `network`, `convection`) are called point by point inside the compiled chains: the solver's loop over the shells (coefft's) and the envelope's integration (envint's). Their hot path is a **static method over one point** (`point`), which the chains call compiled. Each also evaluates arrays **without a model**, through `__call__` (for example the opacity on a grid of $`\rho`$ and $`T`$), and has `kernel_args()` (the settings and tables the kernel reads, as one named tuple), `kernel_args_out()` where the family keeps saved state (the opacity's and the network's: written back after the calls), `serves(...)` (whether `point` covers a call), and `plain(...)` (its own code for the calls `point` does not cover).
- **Stage families** (`diffusion`, `rotation`, `mass_loss`, `solver`, `timestep`, `rezoner`) are called by the step, stage by stage, on the `State`, which they change in place. They have no compiled static method of their own: Their defaults are plain Python calling pyrec's compiled kernels. The `network` and `convection` families also have stage methods.

**Units.** The local families take logarithms where YREC does, base 10, in cgs: log10 of $`\rho`$ in g cm⁻³, of $`T`$ in K, of $`P`$ in dyn cm⁻², of $`r`$ in cm; $`L`$ in L☉. Converting to linear values and back would change the last bits.

**Room for later physics.** No interface fixes YREC's own choices: A family's inputs carry the full composition and the state it needs, and its outputs include the derivatives the solver uses, so that another family can supply them its own way. Where the defaults' wrapping of pyrec still narrows an interface, the family's section says so.

## The physics

### `eos`: the equation of state

Base class `EOSBase`; default `EOS`. Replaces [eqstat.f](../../yrec-map/notes/eqstat.f.md), [eqstat2.f](../../yrec-map/notes/eqstat2.f.md), [oeqos06.f](../../yrec-map/notes/oeqos06.f.md), [eqscve.f](../../yrec-map/notes/eqscve.f.md), and [eqsaha.f](../../yrec-map/notes/eqsaha.f.md).

```python
EOS.point(log_temperature, log_pressure, log_density, x, z, composition, ionization,
          dlnrho_dlnt, dlnrho_dlnp, want_derivatives, in_atmosphere, saha_iterations,
          debye_x, debye_y, debye_z, scv_stencil_t, scv_stencil_p, opal_k3, opal_l2,
          saha_guess, data)                                   # -> 28 values
EOS()(log_pressure, log_temperature, x, z, saha_guess=None, want_derivatives=True,
      composition=None)                                       # -> EOSResult
```

- **Inputs.** $`\log T`$ and $`\log P`$ (YREC's EOS takes pressure, so there is no density input); starting values for $`\log\rho`$ and its two derivatives; X and Z; `composition`, the point's mass fractions in the `State`'s layout (X, Y, Z, then the tracked isotopes), there for families that blend EOSs over any composition (the default reads X and Z only); `derivatives`, whether to compute the second derivatives; the tables' search guesses; `saha_guess`, the Saha equations' starting guess, a `State` field read and set in place ([State](state.md)).
- **Outputs.** $`T`$, $`P`$, $`\log\rho`$ and $`\rho`$; $`\beta = P_\mathrm{gas}/P`$, $`1/\beta`$, and the radiation term; $`R/\mu`$, ions and free electrons per atomic mass unit, the degeneracy parameter $`\eta`$; the derivatives the solver uses: $`\partial\ln\rho/\partial\ln T`$, $`\partial\ln\rho/\partial\ln P`$, $`c_P`$ (erg g⁻¹ K⁻¹), $`\nabla_\mathrm{ad}`$, and their six second derivatives; then the ionization fractions (H⁺, He⁺, He⁺⁺), the iteration count, and the kernel's message flags.
- **The default.** `point` is pyrec's compiled EQSTAT2 kernel, unchanged but for the Saha guess, now an argument; the metal mixture is the envelope's, one per run, as in YREC (the default's choice, not the interface's). Without a model, the default on a grid of 91 × 141 points ($`\log T`$ 3.5–8.0 by a nominal $`\log\rho`$ −12 to 2, the pressures set from an ideal gas) takes about 6 µs a point compiled and agrees with pyrec point by point, byte for byte.
- **Narrower for now.** The envelope's chain knows only X and Z, and passes them as a composition; the four search guesses and the Debye-Hückel composition are passed one by one, as YREC does.

Directions (not implemented): [a blended EOS over any composition](directions.md#eos).

### `opacity`: opacities

Base class `OpacityBase`; default `Opacity`. Replaces [getopac.f](../../yrec-map/notes/getopac.f.md), [getopal95.f](../../yrec-map/notes/getopal95.f.md), [getalex06.f](../../yrec-map/notes/getalex06.f.md), [gtpurz.f](../../yrec-map/notes/gtpurz.f.md), and [condopacpint.f](../../yrec-map/notes/condopacpint.f.md). The first family built: [The pilot: opacity](pilot-opacity.md).

```python
Opacity.point(log_density, log_temperature, x, z, ionization, data)
    # -> (kappa, log_kappa, dlnkappa_dlnrho, dlnkappa_dlnt, status)
Opacity()(log_density, log_temperature, x, z, ionization=None)  # -> OpacityResult
```

- **Inputs.** $`\log\rho`$, $`\log T`$, X, Z, and the ionization fractions of H and He (`ionization`, fully ionized by default without a model), which the conductive opacity reads.
- **Outputs.** The Rosseland mean $`\kappa`$ (cm² g⁻¹) and $`\log\kappa`$, its derivatives $`\partial\ln\kappa/\partial\ln\rho`$ and $`\partial\ln\kappa/\partial\ln T`$, and a status, nonzero where the kernel leaves a point to `plain`.
- **The default.** The molecular tables of Ferguson et al. 2005 (YREC's ALEX06 tables) below `TMOLMAX` ($`\log T`$ = 4.1 by default), OPAL 1995 above `TMOLMIN` (4.0), a ramp in $`\log T`$ between, and Potekhin's conductive opacity (or the Hubbard-Lampe fit) added; `point` is pyrec's getopac kernel, unchanged. The surface tables interpolated to the surface's composition are `State` fields ([State](state.md), the copy test).

Directions (not implemented): [other opacity tables](directions.md#opacity).

### `atmosphere`: atmospheres, the envelope, and the boundary conditions

Base class `AtmosphereBase`; default `Atmosphere`. Replaces [surfbc.f](../../yrec-map/notes/surfbc.f.md), [envint.f](../../yrec-map/notes/envint.f.md), [qatm.f](../../yrec-map/notes/qatm.f.md), [qenv.f](../../yrec-map/notes/qenv.f.md), [surfp.f](../../yrec-map/notes/surfp.f.md), and [alsurfp.f](../../yrec-map/notes/alsurfp.f.md).

```python
Atmosphere.atmosphere_point(log_tau, integrated, slopes, distortion_fp, log_g, in_atmosphere,
                            want_derivatives, save_for_output, log_teff, x, z, cf, ci, ctx)
Atmosphere.envelope_point(log_pressure, integrated, slopes, luminosity, distortion_fp, distortion_ft,
                          in_atmosphere, want_derivatives, save_for_output, log_teff,
                          x, z, cf, ci, ctx)                  # -> stage: 0 when done, else where the kernel
                                                              #    stopped for the plain code (1-4)
Atmosphere()(log_luminosity, log_teff, log_total_mass, x, z, mixing_length, distortion_fp,
             distortion_ft, expected_fit_log_pressure, fit_point)
                                                              # -> (log P, log T, log r) at the fitting point
Atmosphere().boundary(state, x, z, distortion_fp, distortion_ft, expected_fit_log_pressure,
                      counters)                               # stage method: the solver's outer boundary
```

- **The hot path** is the integrand of the atmosphere's integration in $`\log\tau`$ (the right-hand side for $`\log P`$) and of the envelope's in $`\log P`$ (for $`\log(m/M)`$, $`\log T`$, and $`\log r`$), with YREC's calling convention: two small arrays of the integration's own values and counters, and the chain's context (the EOS's, the opacity's, and the convection's data). The default's integrands are pyrec's qatm and qenv kernels themselves; the EOS, opacity, and convection inside them are the installed families.
- **Without a model,** `__call__` gives the fitting point's $`\log P`$, $`\log T`$, and $`\log r`$ for a surface ($`L`$, $`T_\mathrm{eff}`$), and `atmosphere_derivatives`, `envelope_derivatives` the integrands on arrays of points.
- **Stage methods.** `boundary` (the solver's outer boundary condition: for the default, the envelope triangle and its plane fit, kept in the `State`) and `envelope_profile` (the envelope and atmosphere integrated again at fixed steps for the stored profile; the output module writes the lines).
- **What the solver needs** from any atmosphere family is the fitting point's $`\log P`$, $`\log T`$, and $`\log r`$ as functions of $`L`$ and $`T_\mathrm{eff}`$, with their derivatives. The $`T`$–$`\tau`$ relation, the model-atmosphere tables, the fitting mass, and the triangle are the default's, not the interface's.
- **Narrower for now.** The integrands' composition is X and Z only, their calling convention is the chain's, and `boundary` takes YREC's call counters.

Directions (not implemented): [other boundary conditions and starspots](directions.md#atmosphere).

### `network`: nuclear reactions, energy generation, and neutrinos

Base class `NetworkBase`; default `Network`. Replaces [engeb.f](../../yrec-map/notes/engeb.f.md), [rates.f](../../yrec-map/notes/rates.f.md), [kemcom.f](../../yrec-map/notes/kemcom.f.md), [liburn.f](../../yrec-map/notes/liburn.f.md), and [sneut.f](../../yrec-map/notes/sneut.f.md).

```python
Network.point(log_density, log_temperature, composition, shell, rates, data)
    # -> (epsilon_pp1, epsilon_pp2, epsilon_pp3, epsilon_cno, epsilon_triple_alpha, depsilon_dlnrho,
    #     depsilon_dlnt, epsilon, be7_mass_fraction, epsilon_alpha_capture, epsilon_neutrino, status)
Network.serves(log_temperature, data)                         # compiled too: the chains' fast-path test
Network()(log_density, log_temperature, composition)          # -> NetworkResult
```

- **Inputs.** $`\log\rho`$, $`\log T`$, the whole composition array (species by row; the family reads its own rows, `species`, at column `shell`), and the family's per-point rate arrays (`rate_names`), set at `shell`. The network's size and species are the family's data, not the base's constants.
- **Outputs.** The energy generation $`\epsilon`$ net of neutrinos (erg g⁻¹ s⁻¹), its derivatives in $`\ln\rho`$ and $`\ln T`$, its parts by branch (pp I–III, CNO, triple alpha, alpha captures), the neutrino losses, the ⁷Be mass fraction, and the rates.
- **Stage methods.** `burn` and `burn_deuterium` (the composition burned over the step), `light_elements_start` and `light_elements` (the light elements' rates at the start of the step and their burning after the structure), `light_elements_due`, and `save_start` (the start-of-step composition).
- **The default.** engeb's kernel, unchanged; its `SAVE`d scalars are the `State`'s `network_saved`. Without a model, 0.54–0.61 µs a point compiled where the kernel serves the point, and byte for byte with pyrec's engeb on a grid of 5,187 points at each of two compositions.
- **Narrower for now.** The solver's loop reads the network's 11 results by position and holds exactly 15 rate arrays, and the composition array has 15 species: fixed by the chain and the `State`'s layout today.

Directions (not implemented): [larger networks](directions.md#network).

### `convection`: convection, overshoot, and the mixing of composition

Base class `ConvectionBase`; default `Convection`. Replaces [tpgrad.f](../../yrec-map/notes/tpgrad.f.md), [convec.f](../../yrec-map/notes/convec.f.md), [oversh.f](../../yrec-map/notes/oversh.f.md), [sconvec.f](../../yrec-map/notes/sconvec.f.md), [mix.f](../../yrec-map/notes/mix.f.md), and [mixcz.f](../../yrec-map/notes/mixcz.f.md).

```python
Convection.point(log_temperature, temperature, log_pressure, pressure, density, log_radius, log_mass,
                 luminosity, kappa, <the EOS's and the opacity's derivatives>, nabla_ad, ...,
                 want_derivatives, distortion_fp, distortion_ft, mixing_length, overshoot_point, data)
    # -> (nabla, nabla_rad, dnabla_dlnt, dnabla_dlnp, dnabla_dlnr, convective_velocity, convective, status)
Convection()(want_derivatives, distortion_fp, distortion_ft, mixing_length, overshoot_point, log_teff,
             **inputs)                                        # -> ConvectionResult
```

- **Inputs.** The local state (24 values in YREC's order: $`T`$, $`P`$, $`\rho`$, $`r`$, $`m`$, $`L`$, $`\kappa`$, and the EOS's and the opacity's derivatives), the rotational distortion terms $`f_P`$, $`f_T`$, the mixing length $`\alpha`$, and the shell for the adiabatic-overshoot test.
- **Outputs.** The actual gradient $`\nabla`$, the radiative gradient $`\nabla_\mathrm{rad}`$, the derivatives of $`\nabla`$ (the solver's Jacobian), the convective velocity (cm s⁻¹), and whether the point is convective.
- **Stage methods.** `zones` (the convective and mixed zones, with overshoot), `mix` (the composition over the step: YREC's MIX, which also burns and settles through the installed network and diffusion families), `mix_zones` (the convection zones mixed fully), and `mixing_coefficients` (declared: diffusion coefficients each mixing process adds to; YREC's default mixes the zones instantly, so it gives none).
- **The default.** Böhm-Vitense's mixing-length theory as tpgrad.f has it; `point` is pyrec's tpgrad kernel, unchanged. The variant is the class's, not the signature's. Without a model, 0.2–0.5 µs a point on 2,192 points, byte for byte.
- **Narrower for now.** `point` takes no composition gradient and no previous velocity or time step.
- **Open.** The step calls only `convection.mix`, inside which YREC's MIX burns and settles: A convection family whose `mix` does not burn must call the network and diffusion itself. Whether the step should call them in MIX's order once MIX is restructured is open.

Directions (not implemented): [more convection and mixing](directions.md#convection).

### `diffusion`: microscopic diffusion and settling

Base class `DiffusionBase`; default `Diffusion`. Replaces [microdiff.f](../../yrec-map/notes/microdiff.f.md) and [grsett.f](../../yrec-map/notes/grsett.f.md).

```python
Diffusion()(state, start, timestep, mixing=None)   # the composition settled over the step, in place
Diffusion().coefficients(state)                    # its diffusion coefficients by interface, cm² s⁻¹
```

- **A stage family.** `timestep` in s; `mixing`, extra diffusion coefficients by interface (cm² s⁻¹) from other mixing, added to the family's own. The default is YREC's settling (on only with `LDIFY`, YREC's switch for helium settling), called inside MIX; it takes no extra coefficients yet (`mixing` must be `None`). Diffusion is off in the 1 M☉ ZAMS case, so the default is wired but not exercised by a run.

Directions (not implemented): [radiative levitation](directions.md#diffusion).

### `rotation`: rotation

Base class `RotationBase`; default `Rotation`. Replaces [getrot.f](../../yrec-map/notes/getrot.f.md), [getw.f](../../yrec-map/notes/getw.f.md), [seculr.f](../../yrec-map/notes/seculr.f.md), [rotmix.f](../../yrec-map/notes/rotmix.f.md), and [vcirc.f](../../yrec-map/notes/vcirc.f.md).

```python
Rotation()(state, start, timestep)        # Omega and j over the step, the mixing, the distortion terms
Rotation().torque(state)                  # the surface's angular-momentum loss, g cm² s⁻²
Rotation().mixing_coefficients(state)     # rotational mixing, cm² s⁻¹ by interface
```

- **A stage family.** The solver calls it inside its iteration, as YREC iterates structure and rotation. Transport, the surface's loss, and the mixing are separate methods, so that a family can change one alone; YREC's GETW does all three in one routine, so the default gives `torque` and `mixing_coefficients` only through its stage. The default uses two small modules: the shear's stability limit and the thermal diffusivity and viscosity (from YREC's PHYSIC and VISCOS). Rotation is off in the 1 M☉ ZAMS case.

Directions (not implemented): [rotation's structure and transport](directions.md#rotation).

### `mass_loss`: angular-momentum loss and mass loss

Base class `MassLossBase`; default `MassLoss`. Replaces [massloss.f](../../yrec-map/notes/massloss.f.md), [mdot.f](../../yrec-map/notes/mdot.f.md), [wind.f](../../yrec-map/notes/wind.f.md), and [mwind.f](../../yrec-map/notes/mwind.f.md).

```python
MassLoss()(state, timestep)   # -> the time step after mass loss, s; the State changed in place
MassLoss().rate(state)        # the signed mass change rate, g s⁻¹ (negative: loss; positive: accretion)
```

- **A stage family,** called on a step that ages the star. The recipe is the family's; YREC's MASSLOSS chooses and applies it in one routine, so the default gives `rate` only through its stage. It may shorten the step, as MASSLOSS may. Mass loss is off in the 1 M☉ ZAMS case (the stage is called, and returns at once).

Directions (not implemented): [mass-loss recipes and accretion](directions.md#mass-loss).

## The numerical methods

### `solver`: the structure equations and the Henyey solver

Base class `SolverBase`; default `Solver`. Replaces [crrect.f](../../yrec-map/notes/crrect.f.md), [coefft.f](../../yrec-map/notes/coefft.f.md), [hsolve.f](../../yrec-map/notes/hsolve.f.md), and [reduce.f](../../yrec-map/notes/reduce.f.md).

```python
Solver()(state, start, physics, timestep)   # -> SolveResult(converged, iterations, residuals, reason)
Solver().residuals(state)                   # the equations' residuals per shell
```

- **A stage family.** It solves for $`P`$, $`T`$, $`r`$, and $`L`$ at fixed composition over one step, in place, through CRRECT's four levels; its loop over the shells (coefft's) calls the local families' compiled kernels. `timestep` is in s, negative for a step that does not age the star (YREC's convention). Between iterations it calls the network's `light_elements_start`, the convection's `mix_zones`, and, with rotation, the rotation family.
- **Derivatives** come from the physics families' outputs, never from differentiating a family, so that a family may supply them its own way.
- **A failed solve** is returned (`converged` false), not raised; the model then retries from the start of the step with a shorter step or stops, and the default stops, as YREC does. `residuals` is declared; YREC's default does not provide it.

Directions (not implemented): [derivatives and diagnostics](directions.md#solver).

### `timestep`: the time step

Base class `TimestepBase`; default `Timestep`. Replaces [htimer.f](../../yrec-map/notes/htimer.f.md), [ytime.f](../../yrec-map/notes/ytime.f.md), and [xtime.f](../../yrec-map/notes/xtime.f.md).

```python
Timestep()(state, start)        # -> the next step, s
Timestep().ages(state)          # whether this step ages the star
Timestep().advance_age(state)   # the age advanced by the step
Timestep().counts_model(state)  # whether the step adds one to the model number
```

- **A stage family.** Its limits (YREC's `ATIME` and the rest) are its own configuration, not arguments. `ages` is false for a step at zero time (a rescaled model relaxed), which gates the mass-loss and composition stages; `counts_model` is false on a pure rescaling kind card (one of the runs YREC chains in one job), as in YREC; `advance_age` adds the step in years (3.1558 × 10⁷ s a year, YREC's) to the age in Gyr. The model's stopping conditions (the end age, the central abundances, the star calibration) sit beside it.

Directions (not implemented): [step retries](directions.md#timestep).

### `rezoner`: placing the shells

Base class `RezonerBase`; default `Rezoner`. Replaces [hpoint.f](../../yrec-map/notes/hpoint.f.md), [findsh.f](../../yrec-map/notes/findsh.f.md), and [getnewenv.f](../../yrec-map/notes/getnewenv.f.md).

```python
Rezoner()(state)                        # the shells placed, in place
Rezoner().locate_zones(state)           # the edges of the convective core, the surface convection zone,
                                        #   and the hydrogen shell
Rezoner().restore_fitting_point(state)  # the earlier fitting point restored after accretion
```

- **A stage family.** Its controls are its own configuration. `locate_zones` is FINDSH, whose outputs the time step and the rezoning read; `restore_fitting_point` does nothing unless the fitting point moved, so a rezoner without YREC's envelope fit need not provide it.

Directions (not implemented): [the mesh](directions.md#rezoner).
