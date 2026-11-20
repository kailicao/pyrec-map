# A new design for YREC

*A high-level design (Nov 9, 2026), brought up to date with Kaili Cao's decisions of Nov 18, 2026: the structure the code is meant to have, kept in mind while the current code is mapped and debugged. It names responsibilities, not routines, so that bug fixes and small improvements to the Fortran leave it unchanged. Python with Numba is its scope; modern Fortran is mentioned at the end. The earlier, detailed design (modern-Fortran types, Python stubs, the COMMON-block map, Oct 25–31, 2026) is in this repository's history.*

**The pages of this design,** besides this overview:

- [State](state.md): what a run carries, each value under its descriptive name beside YREC's;
- [The families](families.md): each family's inputs and outputs;
- [Directions from MESA](directions.md): where each family could grow beyond YREC (none built);
- [The compiled tree](tree.md): what runs compiled, and what in plain Python;
- [Writing a Numba family](numba.md): how a family's hot paths are compiled;
- [The pilot: opacity](pilot-opacity.md): the first family, beside the code it wraps;
- [The families' names](names.md): each family's names beside YREC's.

## Goals

YREC's physics is mature and validated; what makes it hard to read, test, and extend is its structure: state shared through modules (COMMON blocks until recently), routines that set and read the same variables from far apart, and new physics added by editing those routines. The new structure should let an astronomer who does not read Fortran:

- **find each piece of physics** in one place, under the name of what it does;
- **replace it** with their own, in a few lines of Python, without touching the rest;
- **inspect any value** between two steps, or two lines, as Python allows, and **plot any array** (below, Looking inside);
- **trust the results,** because every piece is checked against the Fortran it replaces, bit for bit for the default physics;
- **run what astronomers run:** grids of models, settings that change along a track, and branches from a model.

One rule makes these possible: **everything that changes during a run lives in the model's data;** the physics and the numerical methods hold none of it. YREC keeps values between calls inside its routines (`SAVE`d locals, cached tables, ESAC06's growing `EOS(5)`); in the new structure every value a run carries has one home ([State](state.md)):

- **the `State`,** the star at one moment: arrays over the shells, scalars, and any value carried from one step to the next that changes later results;
- **a family's cache,** which the family can rebuild and which changes no result;
- **work arrays,** scratch space inside one computation.

**The test:** Copy a model in the middle of a run and run both copies on: They must match byte for byte.

## Two versions

pyrec comes in two versions:

1. **The Fortran-tracking pyrec,** the translation as it is: one Python module per Fortran file, Numba kernels, byte-identical to YREC on the 1 M☉ ZAMS case and the solar model (YREC's test-suite case `Test_solarGS98_base`).
2. **The object-oriented pyrec,** the design on these pages, committed with the first in one commit (Nov 19, 2026) as the package `pyrec_oop`. Once it no longer runs through the Fortran-tracking routines, it becomes pyrec's main branch, and the Fortran-tracking version moves to a branch of its own, relabeled "legacy" (a relabeling only).

This site shows both, cross-referenced: each family's section of [The families](families.md) names the Fortran-tracking routines its default wraps, and each file's page the family that wraps it (and is to replace it). The object-oriented version runs in pyrec as `pyrec_oop`, beside the Fortran-tracking path (`PYREC_FAMILIES=0`).

## The model

The central object is a `Model`: In a stellar code, a model is one star at one time, and `model()` advances it by one step. It holds the data (the star now, the star at the start of the step, and its history) and, as attributes, the callables that act on it, grouped in two bundles: the physics, and the numerical methods.

```text
Model                       # one star; model() advances it one step
├── config: Config          # from YAML: the run's settings and stopping conditions
├── state: State            # the current star: arrays over the shells (structure, composition,
│                           #   rotation) and scalars (age, mass, model number); state.copy()
├── start: State            # the state at the start of the step
├── history: History        # a table of per-step summaries, plus full snapshots now and then (NPZ)
├── controls: list          # callables run at the start of each step, which may change any setting
├── hooks: dict             # callables run between a step's stages (Looking inside)
├── stops: list             # the stopping conditions, checked at the end of each step
├── outputs: list           # callables writing the output at the end of each step
├── physics: Physics        # what the star is made of and how it behaves (each a base class; YREC's default)
│   ├── eos: EOSBase                 # EOS
│   ├── opacity: OpacityBase         # Opacity
│   ├── atmosphere: AtmosphereBase   # Atmosphere
│   ├── network: NetworkBase         # Network: reaction rates, energy generation, neutrinos
│   ├── convection: ConvectionBase   # Convection: mixing length, overshoot, semiconvection
│   ├── diffusion: DiffusionBase     # Diffusion: settling
│   ├── rotation: RotationBase       # Rotation: transport of angular momentum, rotational mixing
│   └── mass_loss: MassLossBase      # MassLoss: winds, braking, accretion
└── numerics: Numerics      # how the equations are solved
    ├── solver: SolverBase           # Solver: the Henyey iteration
    ├── timestep: TimestepBase       # Timestep: choosing the next step
    └── rezoner: RezonerBase         # Rezoner: placing the shells
```

- **Data and behavior apart.** `State` is plain data, arrays and scalars, so that copying it, saving it, and comparing it with the Fortran's are each one line. `Physics` and `Numerics` hold no state of the star; they are given it.
- **Physics and numerics apart,** because they change for different reasons: an astronomer swaps an opacity table, a numerical analyst the solver.
- **Each family is a base class** with a fixed set of inputs and outputs, for example the opacity's `point(log_density, log_temperature, x, z, ionization, data) -> (kappa, log_kappa, dlnkappa_dlnrho, dlnkappa_dlnt, status)` ([The families](families.md)); the base class's name ends in `Base` (`OpacityBase`), and YREC's default takes the plain name (`Opacity`). The local families (`eos`, `opacity`, `atmosphere`, `network`, `convection`), which the solver and the envelope call point by point, put their hot paths, the loops a run spends its time in, in compiled (Numba) static methods, so that a whole chain of families runs compiled ([Writing a Numba family](numba.md)); the stage families, called once a step, are plain Python calling compiled kernels ([The families](families.md), Two kinds of family). A family written in plain Python also works: It is installed with one assignment, `model.physics.opacity = MyOpacity(...)`, and pyrec warns that the run will be slower, since every compiled chain that calls it then runs in Python ([The compiled tree](tree.md) shows which).
- **The start of the step** is kept as a state of its own: YREC's operator split redoes the burning and mixing from the start-of-step composition once the structure is solved (levels 3 and 4 of [`CRRECT`](../../yrec-map/notes/crrect.f.md#crrect)), and a step that fails may be retried from it with a shorter step (below, One step).
- **The default of every family reproduces YREC,** bit for bit, each linked below to the routines it replaces.
- **Descriptive names,** each beside YREC's name (written in lower case in pyrec) for the variables the two share; the mapping is a table in the code, so that the glossary can show it ([State](state.md); [The families' names](names.md)). Each of YREC's variables has one descriptive name, the same in every table; a routine's arguments are mapped per routine, so that a YREC name meaning different quantities in different routines has one descriptive name for each.

## One step

`model()` does what one pass of [main.f](../../yrec-map/notes/main.f.md)'s model loop does today, in the same order, each stage through a family:

1. the controls, in order (below);
2. `start = state.copy()`, and whether the step ages the star (`timestep`);
3. mass loss or accretion (`mass_loss`), on a step that ages the star;
4. burning, mixing, and settling of the composition over the step, with the current structure (`convection`, whose mixing calls `network` and `diffusion` as YREC's MIX does), and the age advanced;
5. the shells placed (`rezoner`);
6. the structure solved for $`P`$, $`T`$, $`r`$, and $`L`$ at fixed composition, the burning and mixing redone with the new structure (`solver`, which calls `eos`, `opacity`, `atmosphere`, and `network`, and with rotation the `rotation` family, which YREC iterates with the structure);
7. the zones located, and the light elements burned (`rezoner`, `convection`, `network`);
8. the next step's length (`timestep`), the output, a summary row added to `history`, and the stopping conditions checked.

**A step that fails** to converge may be retried from `start` with a shorter step; the default reproduces YREC, which stops the run.

## Looking inside

Every array can be looked at and plotted:

- **A family on its own,** without a model: for example, the opacity on a grid of $`\rho`$ and $`T`$, called as the solver calls it, and plotted.
- **A model stopped at any step,** its `State` read and its profiles plotted, then run on.
- **Hooks between a step's stages** (`model.hooks`), callables run after any of the eight stages above, which may read the state, record it, or stop the run.

How memory is managed (views, copies, preallocated arrays) is chosen for speed, as long as all three work.

## The families

Each family against the home page's topics and the routines whose behavior its default reproduces (their pages give the code, the questions, and the suspected bugs); each family's inputs and outputs are on [The families](families.md).

| Family | Topic on the home page | Today's routines |
| --- | --- | --- |
| `eos` | The equation of state | [eqstat.f](../../yrec-map/notes/eqstat.f.md), [eqstat2.f](../../yrec-map/notes/eqstat2.f.md), [oeqos06.f](../../yrec-map/notes/oeqos06.f.md), [eqscve.f](../../yrec-map/notes/eqscve.f.md), [eqsaha.f](../../yrec-map/notes/eqsaha.f.md) |
| `opacity` | Opacities | [getopac.f](../../yrec-map/notes/getopac.f.md), [getopal95.f](../../yrec-map/notes/getopal95.f.md), [getalex06.f](../../yrec-map/notes/getalex06.f.md), [gtpurz.f](../../yrec-map/notes/gtpurz.f.md), [condopacpint.f](../../yrec-map/notes/condopacpint.f.md) |
| `atmosphere` | Atmospheres, the envelope, and the boundary conditions | [surfbc.f](../../yrec-map/notes/surfbc.f.md), [envint.f](../../yrec-map/notes/envint.f.md), [qatm.f](../../yrec-map/notes/qatm.f.md), [qenv.f](../../yrec-map/notes/qenv.f.md), [surfp.f](../../yrec-map/notes/surfp.f.md), [alsurfp.f](../../yrec-map/notes/alsurfp.f.md) |
| `network` | Nuclear reactions, energy generation, and neutrinos | [engeb.f](../../yrec-map/notes/engeb.f.md), [rates.f](../../yrec-map/notes/rates.f.md), [kemcom.f](../../yrec-map/notes/kemcom.f.md), [liburn.f](../../yrec-map/notes/liburn.f.md), [sneut.f](../../yrec-map/notes/sneut.f.md) |
| `convection` | Convection, overshoot, and the mixing of composition | [tpgrad.f](../../yrec-map/notes/tpgrad.f.md), [convec.f](../../yrec-map/notes/convec.f.md), [oversh.f](../../yrec-map/notes/oversh.f.md), [sconvec.f](../../yrec-map/notes/sconvec.f.md), [mix.f](../../yrec-map/notes/mix.f.md), [mixcz.f](../../yrec-map/notes/mixcz.f.md) |
| `diffusion` | Microscopic diffusion and settling | [microdiff.f](../../yrec-map/notes/microdiff.f.md), [grsett.f](../../yrec-map/notes/grsett.f.md) |
| `rotation` | Rotation (both topics) | [getrot.f](../../yrec-map/notes/getrot.f.md), [getw.f](../../yrec-map/notes/getw.f.md), [seculr.f](../../yrec-map/notes/seculr.f.md), [rotmix.f](../../yrec-map/notes/rotmix.f.md), [vcirc.f](../../yrec-map/notes/vcirc.f.md) |
| `mass_loss` | Angular-momentum loss and mass loss | [massloss.f](../../yrec-map/notes/massloss.f.md), [mdot.f](../../yrec-map/notes/mdot.f.md), [wind.f](../../yrec-map/notes/wind.f.md), [mwind.f](../../yrec-map/notes/mwind.f.md) |
| `solver` | The structure equations and the Henyey solver | [crrect.f](../../yrec-map/notes/crrect.f.md), [coefft.f](../../yrec-map/notes/coefft.f.md), [hsolve.f](../../yrec-map/notes/hsolve.f.md), [reduce.f](../../yrec-map/notes/reduce.f.md) |
| `timestep`, `rezoner` | The time step and rezoning | [htimer.f](../../yrec-map/notes/htimer.f.md), [ytime.f](../../yrec-map/notes/ytime.f.md), [xtime.f](../../yrec-map/notes/xtime.f.md), [hpoint.f](../../yrec-map/notes/hpoint.f.md), [findsh.f](../../yrec-map/notes/findsh.f.md), [getnewenv.f](../../yrec-map/notes/getnewenv.f.md) |
| `history`, input and output | Output; Input | [wrtout.f](../../yrec-map/notes/wrtout.f.md), [wrthead.f](../../yrec-map/notes/wrthead.f.md), [putstore.f](../../yrec-map/notes/putstore.f.md), [starin.f](../../yrec-map/notes/starin.f.md), [rscale.f](../../yrec-map/notes/rscale.f.md), [getyrec7.f](../../yrec-map/notes/getyrec7.f.md), [getmodel2.f](../../yrec-map/notes/getmodel2.f.md), [parmin.f](../../yrec-map/notes/parmin.f.md) |

The numerical utilities (splines, interpolation, quadrature, linear solvers) become a small library the families share, one routine where YREC has several.

**What is dropped:** whatever YREC's test suite does not cover; the coverage is measured later.

## Grids and calibrations

Above the model sit two small classes:

```text
Grid                 # many stars: one Model per point of the parameter grid
├── models: list[Model]
└── run()            # runs them, in parallel processes if asked, and gathers their histories
Calibration          # adjusts one model's parameters until it matches the Sun or a given star
```

- **A `Grid`** comes from a configuration in which some settings are lists (below). Its results are one table, one row per model and step, keyed by the grid's parameters. YREC's "kind cards," several runs in one job, are a small grid.
- **A `Calibration`** runs a model, compares it with its target, and adjusts the mixing length and helium until they match: the Sun, or a star of given $`L`$ and $`T_\mathrm{eff}`$, as [setcal.f](../../yrec-map/notes/setcal.f.md), [chkcal.f](../../yrec-map/notes/chkcal.f.md), [setscal.f](../../yrec-map/notes/setscal.f.md), and [chkscal.f](../../yrec-map/notes/chkscal.f.md) do today.

## Controls: settings that change along a track

`model.controls` is a list of plain callables; the model calls each at the start of every step, and each may change any setting or swap any family:

```python
def evolving_alpha(model):
    model.state.mixing_length = 1.8 + 0.1 * model.state.age   # the age in Gyr

model.controls.append(evolving_alpha)
```

A mixing length that evolves, an accretion rate that follows a disk (a mass-loss family whose `rate(state)` follows it; accretion is mass loss with the other sign), a switch turned on at the end of the main sequence: Each is a control. The values the controls set are written to the history, so that a run can be reproduced.

## Branching

`branch = model.copy()` copies the state, the start-of-step state, the configuration, the history, and the controls; the physics and numerics are shared, since they hold no state of the star. The branch is then changed (`branch.physics.rotation = ...`) and advanced on its own. A branch from a saved model is `Model.from_npz(path, config)`. Both rest on the rule above: A model's data is all that defines it, which the copy test checks.

## Configuration and files

- **Configuration in YAML,** one file per run: the settings of YREC's two namelists, grouped by family, with a converter from the namelists. **Any setting may be a single value or a list.** If every setting is a single value, the configuration describes one model (`Model`); each setting given as a list is an axis of a grid (`Grid`), its models every combination of the axes' values (or, if asked, the axes taken together, element by element). A setting that is itself a list (YREC's tolerances `HTOLER`, the time-step limits `ATIME`) is an axis only when given as a list of lists. One entry point, `pyrec.run(config)`, returns the model or the grid. The numbers YREC writes into its code today (limits, tolerances, switches; the earlier design's list is in this repository's history) become named settings with YREC's values as defaults.
- **Models in NPZ,** a dump of `State`, with converters both ways for YREC's model files (those [getyrec7.f](../../yrec-map/notes/getyrec7.f.md) and [getmodel2.f](../../yrec-map/notes/getmodel2.f.md) read, and the stored models of [putstore.f](../../yrec-map/notes/putstore.f.md)). The converters are also what lets each new piece be compared with the Fortran on the same model.
- **History** as a table (one row per step) written as YREC's track output is, plus NPZ snapshots at the steps the configuration asks for.
- **Tables** (opacities, equations of state, atmospheres) as binary copies (NPY) of YREC's text tables, kept outside the repository; pyrec's `npyio.py` writes and reads them. The time a conversion takes does not count against the run.

## Performance

**As fast as possible**. The driver, `Model` and its loop, is plain Python; every family's hot loops run in **Numba**, in kernels that fill arrays given to them and change nothing else, which is also what lets a family be tested on its own ([Writing a Numba family](numba.md)). Tables and models are read from NPY and NPZ, not text. The Fortran-tracking pyrec ran the 1 M☉ ZAMS case in 11.8–12.4 s on the NPY path against the Fortran's 11.4–12.4 s, run back to back on a busy machine (Nov 18, 2026; indicative); the object-oriented version is held to the same. A family in plain Python works, with a warning, and [The compiled tree](tree.md) shows what it slows down. JAX stays an option for a family other than the defaults: It could differentiate the physics for the Henyey solver's Jacobian, where YREC's hand-written derivatives hold several of today's suspected bugs ([condopacpint.f](../../yrec-map/notes/condopacpint.f.md), [engeb.f](../../yrec-map/notes/engeb.f.md); [`KNOWN_ISSUES.md`](https://github.com/yreclab/yrec/blob/7be4133/KNOWN_ISSUES.md), issue 40).

**Modern Fortran** stays possible: the same families as derived types with type-bound procedures, called from Python, for the families that need the speed once the Python is right.

## The route there

1. **The Python translation** in YREC's current structure (pyrec): one Python file per Fortran file, each routine beside its Fortran on this site, and the Fortran's apparent bugs reproduced and marked.
2. **Differential tests** against the Fortran at a frozen commit (7be4133 since Nov 9, 2026), routine by routine, then on whole models. They reached byte identity: Every recorded call agrees with the Fortran to the last bit, and the 1 M☉ run to the ZAMS and the solar model to 4.568 Gyr write byte-identical output (pyrec's README, Status). YREC's development branch brings a test suite of 298 cases and a rebaseline protocol ([`REBASELINE_PROTOCOL.md`](https://github.com/yreclab/yrec/blob/7be4133/REBASELINE_PROTOCOL.md)) for changes meant to change results.
3. **The new structure, family by family,** starting with the opacity ([The pilot: opacity](pilot-opacity.md)): Each family's default first wraps the translated routines, then replaces them. **Bit for bit:** After every step of the restructuring, the outputs stay byte-identical with the Fortran-tracking pyrec, and so with YREC, for the default families; a change of bits is a deliberate change of its own. Bug fixes the developers confirm come in commits of their own, each with its rebaseline.

**Where it stands.** In pyrec's `pyrec_oop`, every family is a base class with YREC's default, which wraps the Fortran-tracking pyrec's routines unchanged, and a `Model` drives each step of the 1 M☉ ZAMS case and of the solar model through the families, on a `State`: Every output file is byte-identical to YREC's, and a copy of the model taken after steps 1, 2, 3, 100, 200, or 267 and run on matches the original byte for byte ([State](state.md)). Warm, the run took 16.1–17.1 s against 15.3–16.0 s for the Fortran-tracking pyrec, the two Python versions run in turn on a loaded machine: at the edge of its noise (indicative, not a comparison with the Fortran). Not yet done: a run from a YAML configuration (the families still read YREC's namelists through pyrec's modules), the defaults replacing the routines they wrap, and a case with rotation, diffusion, and mass loss, which are wired but off in the ZAMS case.

## Open questions

Questions about pyrec's own design are Kaili Cao's, since he is pyrec's only developer; each is marked with his answer. Questions about YREC itself stay the team's.

1. *[KC]* **Retrying a failed step.** Today a model that fails to converge ends the run (`STARIN` stops; [main.f](../../yrec-map/notes/main.f.md)'s comment speaks of cutting the step). Should `model()` retry from `start` with a shorter step? *Settled:* It may retry; the default reproduces YREC and stops.
2. *[KC]* **What to drop:** code that never runs or is never called (marked "unused?" on the pages), unless an expert wants it back. *Settled:* Whatever YREC's test suite does not cover is dropped; the coverage is measured later.
3. *[Team]* **Two settling solvers:** keep [grsett.f](../../yrec-map/notes/grsett.f.md) ("retained for backwards compatability") beside [microdiff.f](../../yrec-map/notes/microdiff.f.md), or keep one?
4. *[KC]* **Names:** keep YREC's names (`HCOMP`, `HTOLER`, `ATIME`) in `State` and the configuration, as this site does with its glossary, or move to the "more intuitively named" ones that [remap.f](../../yrec-map/notes/remap.f.md) already accepts? *Settled:* descriptive names, mapped one to one to YREC's for the variables in both, the mapping a table in the code ([State](state.md)).
5. **Values kept between calls.** *[KC]* **Where they live.** *Settled:* in the `State` if they change later results, in a family's cache if it can rebuild them, in work arrays if they are scratch; a copy of a model run on must match the original byte for byte. *[Team]* Which of YREC's saved values (`SAVE`d locals, `DATA`-initialized state, cached tables) carry information from one step to the next, and so belong to the `State`, and which are caches a family can rebuild?
6. *[KC]* **Speed:** how slow may the Python be while it is developed (a model a minute? a track an hour?), and which families get Numba kernels first? *Settled:* as fast as possible; every family in Numba, and tables and models in NPY and NPZ (Performance, above).
