# A new design for YREC

*A high-level design (Nov 9, 2026): the structure the code is meant to have, kept in mind while the current code is mapped and debugged. It names responsibilities, not routines, so that bug fixes and small improvements to the Fortran leave it unchanged. Python with Numba is its scope; modern Fortran is mentioned at the end. The earlier, detailed design (modern-Fortran types, Python stubs, the COMMON-block map, Oct 25–31, 2026) is in this repository's history.*

## Goals

YREC's physics is mature and validated; what makes it hard to read, test, and extend is its structure: state shared through modules (COMMON blocks until recently), routines that set and read the same variables from far apart, and new physics added by editing those routines. The new structure should let an astronomer who does not read Fortran:

- **find each piece of physics** in one place, under the name of what it does;
- **replace it** with their own, in a few lines of Python, without touching the rest;
- **inspect any value** between two steps, or two lines, as Python allows;
- **trust the results,** because every piece is checked against the Fortran it replaces;
- **run what astronomers run:** grids of models, settings that change along a track, and branches from a model.

One rule makes these possible: **everything that changes during a run lives in the model's data;** the physics and the numerical methods hold none of it. YREC keeps values between calls inside its routines (`SAVE`d locals, cached tables, ESAC06's growing `EOS(5)`); in the new structure such a value belongs to the `State`, or to a cache its family can rebuild, so that copying a model copies everything that defines it.

## The model

The central object is a `Model`: In a stellar code, a model is one star at one time, and `model()` advances it by one step. It holds the data (the star now, the star at the start of the step, and its history) and, as attributes, the callables that act on it, grouped in two bundles: the physics, and the numerical methods.

```text
Model                       # one star; model() advances it one step
├── config: Config          # from YAML: the run's settings and stopping conditions
├── state: State            # the current star: arrays over the shells (structure, composition,
│                           #   rotation) and scalars (age, mass, model number); state.copy()
├── start: State            # the state at the start of the step
├── history: History        # a table of per-step summaries, plus full snapshots now and then (NPZ)
├── controls: list           # callables run at the start of each step, which may change any setting
├── physics: Physics        # what the star is made of and how it behaves
│   ├── eos: Eos
│   ├── opacity: Opacity
│   ├── atmosphere: Atmosphere
│   ├── network: Network         # reaction rates, energy generation, neutrinos
│   ├── convection: Convection   # mixing length, overshoot, semiconvection
│   ├── diffusion: Diffusion     # settling
│   ├── rotation: Rotation       # transport of angular momentum, rotational mixing
│   └── mass_loss: MassLoss      # winds, braking, accretion
└── numerics: Numerics      # how the equations are solved
    ├── solver: StructureSolver  # the Henyey iteration
    ├── timestep: TimeStep       # choosing the next step
    └── rezoner: Rezoner         # placing the shells
```

- **Data and behavior apart.** `State` is plain data, arrays and scalars, so that copying it, saving it, and comparing it with the Fortran's are each one line. `Physics` and `Numerics` hold no state of the star; they are given it.
- **Physics and numerics apart,** because they change for different reasons: an astronomer swaps an opacity table, a numerical analyst the solver.
- **Each family is a base class** with one `__call__` and a fixed set of inputs and outputs, for example `Opacity.__call__(rho, T, X, Z) -> (kappa, dlnkappa_dlnrho, dlnkappa_dlnT)`. A new piece of physics is a subclass, or any callable with the same signature (a `typing.Protocol`), so a plain function will do; it is installed with one assignment, `model.physics.opacity = MyOpacity(...)`. The base classes replace the hooks a Fortran code would need.
- **The start of the step** is kept as a state of its own: YREC's operator split redoes the burning and mixing from the start-of-step composition once the structure is solved (levels 3 and 4 of [[crrect.f#CRRECT|`CRRECT`]]), and a step that fails could be retried from it with a shorter step (today a divergence ends the run; an open question below).
- **The default of every family reproduces YREC,** each linked below to the routines it replaces.

## One step

`model()` does what one pass of [[main.f]]'s model loop does today, in the same order, each stage through a family:

1. the controls, in order (below);
2. `start = state.copy()`;
3. mass loss or accretion (`mass_loss`);
4. burning, mixing, and settling of the composition over the step, with the current structure (`network`, `convection`, `diffusion`);
5. the shells placed (`rezoner`);
6. the structure solved for $P$, $T$, $r$, and $L$ at fixed composition, the burning and mixing redone with the new structure (`solver`, which calls `eos`, `opacity`, `atmosphere`, and `network`);
7. rotation (`rotation`);
8. the next step's length (`timestep`), a summary row added to `history`, and the stopping conditions checked.

## The families

Each family against the home page's topics and the routines whose behavior its default reproduces (their pages give the code, the questions, and the suspected bugs).

| Family | Topic on the home page | Today's routines |
| --- | --- | --- |
| `eos` | The equation of state | [[eqstat.f]], [[eqstat2.f]], [[oeqos06.f]], [[eqscve.f]], [[eqsaha.f]] |
| `opacity` | Opacities | [[getopac.f]], [[getopal95.f]], [[getalex06.f]], [[gtpurz.f]], [[condopacpint.f]] |
| `atmosphere` | Atmospheres, the envelope, and the boundary conditions | [[surfbc.f]], [[envint.f]], [[qatm.f]], [[qenv.f]], [[surfp.f]], [[alsurfp.f]] |
| `network` | Nuclear reactions, energy generation, and neutrinos | [[engeb.f]], [[rates.f]], [[kemcom.f]], [[liburn.f]], [[sneut.f]] |
| `convection` | Convection, overshoot, and the mixing of composition | [[tpgrad.f]], [[convec.f]], [[oversh.f]], [[sconvec.f]], [[mix.f]], [[mixcz.f]] |
| `diffusion` | Microscopic diffusion and settling | [[microdiff.f]], [[grsett.f]] |
| `rotation` | Rotation (both topics) | [[getrot.f]], [[getw.f]], [[seculr.f]], [[rotmix.f]], [[vcirc.f]] |
| `mass_loss` | Angular-momentum loss and mass loss | [[massloss.f]], [[mdot.f]], [[wind.f]], [[mwind.f]] |
| `solver` | The structure equations and the Henyey solver | [[crrect.f]], [[coefft.f]], [[hsolve.f]], [[reduce.f]] |
| `timestep`, `rezoner` | The time step and rezoning | [[htimer.f]], [[ytime.f]], [[xtime.f]], [[hpoint.f]], [[getnewenv.f]] |
| `history`, input and output | Output; Input | [[wrtout.f]], [[wrthead.f]], [[putstore.f]], [[starin.f]], [[rscale.f]], [[getyrec7.f]], [[getmodel2.f]], [[parmin.f]] |

The numerical utilities (splines, interpolation, quadrature, linear solvers) become a small library the families share, one routine where YREC has several.

## Grids and calibrations

Above the model sit two small classes:

```text
Grid                 # many stars: one Model per point of the parameter grid
├── models: list[Model]
└── run()            # runs them, in parallel processes if asked, and gathers their histories
Calibration          # adjusts one model's parameters until it matches the Sun or a given star
```

- **A `Grid`** comes from a configuration in which some settings are lists (below). Its results are one table, one row per model and step, keyed by the grid's parameters. YREC's "kind cards", several runs in one job, are a small grid.
- **A `Calibration`** runs a model, compares it with its target, and adjusts the mixing length and helium until they match: the Sun, or a star of given $L$ and $T_\mathrm{eff}$, as [[setcal.f]], [[chkcal.f]], [[setscal.f]], and [[chkscal.f]] do today.

## Controls: settings that change along a track

`model.controls` is a list of plain callables; the model calls each at the start of every step, and each may change any setting or swap any family:

```python
def evolving_alpha(model):
    model.physics.convection.alpha = 1.8 + 0.1 * model.state.age / 1e9

model.controls.append(evolving_alpha)
```

A mixing length that evolves, an accretion rate that follows a disk (`model.physics.mass_loss.rate`; accretion is mass loss with the other sign), a switch turned on at the end of the main sequence: each is a control. The values the controls set are written to the history, so that a run can be reproduced.

## Branching

`branch = model.copy()` copies the state, the start-of-step state, the configuration, the history, and the controls; the physics and numerics are shared, since they hold no state of the star. The branch is then changed (`branch.physics.rotation = ...`) and advanced on its own. A branch from a saved model is `Model.from_npz(path, config)`. Both rest on the rule above: A model's data is all that defines it.

## Configuration and files

- **Configuration in YAML,** one file per run: the settings of YREC's two namelists, grouped by family, with a converter from the namelists. **Any setting may be a single value or a list.** If every setting is a single value, the configuration describes one model (`Model`); each setting given as a list is an axis of a grid (`Grid`), its models every combination of the axes' values (or, if asked, the axes taken together, element by element). A setting that is itself a list (YREC's tolerances `HTOLER`, the time-step limits `ATIME`) is an axis only when given as a list of lists. One entry point, `pyrec.run(config)`, returns the model or the grid. The numbers YREC writes into its code today (limits, tolerances, switches; the earlier design's list is in this repository's history) become named settings with YREC's values as defaults.
- **Models in NPZ,** a dump of `State`, with converters both ways for YREC's model files (those [[getyrec7.f]] and [[getmodel2.f]] read, and the stored models of [[putstore.f]]). The converters are also what lets each new piece be compared with the Fortran on the same model.
- **History** as a table (one row per step) written as YREC's track output is, plus NPZ snapshots at the steps the configuration asks for.

## Performance

The driver, `Model` and its loop, is plain Python. Each family is free to use whatever makes it fast; the default is **Numba**, in kernels that take and return arrays and change nothing else, which is also what lets a family be tested on its own. JAX is an option for a family that would gain from it: it could differentiate the physics for the Henyey solver's Jacobian, where YREC's hand-written derivatives hold several of today's suspected bugs ([[condopacpint.f]], [[engeb.f]]; `KNOWN_ISSUES.md`, issue 40).

**Modern Fortran** stays possible: the same families as derived types with type-bound procedures, called from Python, for the families that need the speed once the Python is right.

## The route there

1. **The Python translation** in YREC's current structure (pyrec): one Python file per Fortran file, each routine beside its Fortran on this site, and the Fortran's apparent bugs reproduced and marked.
2. **Differential tests** against the Fortran at a frozen commit (7be4133 since Nov 9, 2026), routine by routine, then on whole models through the NPZ converters; agreement to a tolerance per quantity, since Python and Numba reorder floating-point operations. YREC's development branch brings a test suite of 298 cases and a rebaseline protocol (`REBASELINE_PROTOCOL.md`) for changes meant to change results.
3. **The new structure, family by family:** each family's default first wraps the translated routines, then replaces them, with the tests passing after each step. Bug fixes the developers confirm come in commits of their own, each with its rebaseline.

## Open questions

1. *[Team]* **Retrying a failed step.** Today a model that fails to converge ends the run (`STARIN` stops; [[main.f]]'s comment speaks of cutting the step). Should `model()` retry from `start` with a shorter step?
2. *[Team]* **What to drop:** code that never runs or is never called (marked "unused?" on the pages), unless an expert wants it back.
3. *[Team]* **Two settling solvers:** keep [[grsett.f]] ("retained for backwards compatability") beside [[microdiff.f]], or keep one?
4. *[Team]* **Names:** keep YREC's names (`HCOMP`, `HTOLER`, `ATIME`) in `State` and the configuration, as this site does with its glossary, or move to the "more intuitively named" ones that [[remap.f]] already accepts?
5. *[Team]* **Values kept between calls:** which of YREC's saved values (`SAVE`d locals, `DATA`-initialized state, cached tables) carry information from one step to the next, and so belong to the `State`, and which are caches a family can rebuild?
6. *[KC]* **Speed:** how slow may the Python be while it is developed (a model a minute? a track an hour?), and which families get Numba kernels first?
7. *[KC]* **Working with YREC's developers:** when to tell them of the plan, and whether this design is proposed to them as the code's next stage.
