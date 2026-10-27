# Language and style

*In Python: `pyrec`, under Python below.*

## 6.1 The language

| Option | For | Against |
| --- | --- | --- |
| **Modern Fortran** (2008, with `iso_c_binding` and `iso_fortran_env`): modules, derived types, type-bound procedures, `abstract` types, `allocatable` arrays | Keeps the validated physics line by line; the compilers YREC already uses (`gfortran`, Intel `ifx`) support it; the refactoring can go one routine at a time, checked against the benchmarks at each step; YREC's users read Fortran | No interactive use; a user who adds physics must compile |
| **A Python interface** over the compiled library | Runs, grids and calibrations from Python and Jupyter; NumPy views of the model; user physics in Python at the step level | Needs a library with no `STOP` and no global state first; per-point callbacks into Python would be slow |
| **Rewrite in Python** (NumPy and Numba) | One language | Some 44,000 lines of validated physics to rewrite and revalidate; not proposed |

**KC's decision (Oct 25, 2026), which may change with feedback:** the route goes through Python after all, as [the Python version's overview](overview.md) describes: Fortran 77 to Python in the old structure, then Python in the new structure, then modern Fortran in the new structure, the last needed for speed. The table and the proposal below are the first sketch's reasoning, kept for the comparison.

**Proposal (first sketch): both, in that order.** The core becomes modern Fortran by refactoring, not rewriting ([Section 7](overview.md)); the Python interface comes once the core has no `STOP` and no global state, since that is what lets a Python process hold a run (or two) in memory and survive an error. This matches the plan's "possibly a Python interface" on KC's Research Directions: the Fortran design is complete without it, and nothing in it has to change when it comes.

## 6.2 KC's style in Fortran

The guide is written for Python. Its conventions carry over as follows; where Fortran has no counterpart, the choice made is stated.

| The guide (Python) | In this design (Fortran) |
| --- | --- |
| One package per method; modules layered by dependency | One library, `yrec`; modules from `kinds` to `evolve` ([Section 2](overview.md)). The compiler forbids circular `use`, so the layering is enforced |
| A module docstring lists its contents | A header comment of `!!` lines listing types and procedures, in the format FORD (a Fortran documentation generator) renders |
| NumPy-style docstrings with shapes and dtypes | `!!` lines after each procedure's header: arguments with shape, kind and unit, e.g. `!! hcomp : (NSP, m), real(dp), mass fractions`. Shapes follow Fortran's column-major order |
| Type hints everywhere | `implicit none` in every module; every argument declared with `intent` |
| UPPERCASE tunable numbers, as class attributes | Module-level `parameter`s in UPPERCASE for fixed values; components with default initialization, in UPPERCASE, for values a driver may change. **Fortran is case-insensitive**: `CMIXL` and `cmixl` are the same name, so case is only a visual signal, and a constant cannot share its name with a variable; constants take a suffix where needed (`CMIXL_DEFAULT`) |
| `__init__` stores, `__call__` runs, `clear()` frees | `init` (or a structure constructor) stores, `run` runs, `clear` deallocates. Fortran has no `__call__`; `run` is the name throughout. Finalizers (`final`) are not relied on, because compilers have differed in when they call them |
| A private base class (`_LAKernel`) | An `abstract` type named `…Base` with `deferred` procedures (Fortran names cannot begin with an underscore); `private` components and procedures mark internals |
| Children reach settings through their parent | A `pointer` component to the parent (`track%job%cfg`); the parent is declared `target`. One `Config`, never copied, read-only after `derive` |
| `setup()` classmethods for class-wide settings | `Physics%setup` and the `init` of each type; there is no class-wide state, so two runs can live in one process |
| Hooks that do nothing in the base class | Non-deferred type-bound procedures whose body is empty, documented "a hook for extended types; the base type does nothing" ([Section 6.5](hooks.md)) |
| Errors name the setting that failed; `ValueError`, not `assert` | Every procedure that can fail returns `ierr` (0 for success) and sets a message naming the setting (`"KTTAU: 6 is not an atmosphere"`); no `STOP` in the library; internal invariants checked under a debug build |
| `logging` instead of `print`, a fixed timing format | `Logger` with levels (`debug`, `info`, `warning`); `system_clock` timings in one fixed format; the routines that now write to the terminal at every call log at `debug` |
| Dispatch on formats with `match` | `select case` on a setting in one factory function per family; `select type` only where a type must be recovered |
| Named columns, not magic indices | Named integer parameters: `I_H1`, `I_HE4`, ... ([Section 3.1](kernels.md)) |
| Derived quantities are properties | Type-bound functions: `star%radius()`, `star%tc()` |
| Numba kernels fill preallocated arrays | `pure` or `elemental` procedures with `intent(inout)` arrays, in `numerics` |
| `__slots__` against misspelled settings | A namelist already rejects an unknown name |
| The configuration written into the output | `Config%write_namelists` into the `.short` file and the model files' headers, defaults included |
| Package data with the package | Tables found through `YREC_INPUT` (already used by the development branch), never through paths relative to the working directory |
| pytest regression and analytic checks | The test suite of reference runs ([Section 7.1](overview.md)), plus unit tests of the kernels on cases with exact answers (splines on cubics, the tridiagonal solver, Bulirsch–Stoer on $y' = y$) |
| Personal style: short statements on one line | Kept where it reads as one thought: `if (ierr /= 0) return`, `tr => self%track  ! Shortcut.` |

## 6.3 The Python interface

Two kinds exist, and YREC already has the first. The development branch documents a `yrec` Python package (`pip install yrec`; `yrec.model.Model(nml1, nml2).run()`, `yrec.run_parallel`) and keeps grid tools in `wrappers/`; both write namelists, run the executable and read its output files. That stays as it is and needs nothing from the overhaul, except that the namelists and output files stay compatible.

The second kind runs YREC in the Python process. `capi.f90` exports a small set of `bind(C)` procedures on opaque handles: `yrec_run_new(nml1, nml2, ierr)`, `yrec_track_start`, `yrec_step(handle, ierr)`, `yrec_star_get(handle, name, array)`, `yrec_run_free`. `python/yrec/_capi.py` declares them with `ctypes`, and `star.py` wraps the model's arrays as NumPy views without copying. With it, a Python driver can step a track, inspect or change the model between steps, and run calibrations with SciPy's root finders, as KC's mesa\_apokasc drivers do around MESA. This design chose `ctypes` over `f2py`, because `f2py` does not wrap derived types or type-bound procedures, which the design's interface is made of. The Python side follows the guide as written. [Section 8](overview.md) asks whether the second kind is wanted, and by whom.
