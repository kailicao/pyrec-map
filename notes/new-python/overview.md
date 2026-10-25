# pyrec: the Python version

*Stage 2 of the overhaul, drafted by Claude (Oct 25, 2026) for Kaili Cao from his plan; nothing is translated yet. The stub tree, [[new/pyrec/__init__.py|`pyrec`]], is the target framework: the same classes and the same split as the [modern-Fortran design](../new-fortran/overview.md), as Python packages, with shells held as NumPy arrays and the hot loops marked for Numba. Each stub names the routines it replaces and links its Fortran counterpart page.*

## Why Python first

Compiled code is hard to debug: a wrong value in YREC today is found with print statements and a rebuild. KC's plan therefore goes through Python, where every array can be inspected between two lines, and keeps the Fortran frozen meanwhile, as the reference that every Python result is checked against. The route, in KC's words:

1. Fortran 77, old structure → Python (with Numba), old structure;
2. → Python, new structure (the framework of these stubs);
3. → modern Fortran, new structure (the [Fortran design](../new-fortran/overview.md)).

**Move 1: the translation.** The current code is translated routine by routine, keeping its structure, so that each Python routine has one Fortran original. Each routine is translated in one of two ways:

- **Plain Python,** for most routines (input, output, set-up, the driver, the run's logic). The COMMON blocks become state objects, one per block or group of blocks, held as attributes and passed along, close to the old structure.
- **A plain-Python wrapper and a Numba kernel,** for the numerics-heavy routines: the structure solver, the equation-of-state and opacity interpolation, nuclear burning, diffusion. The wrapper takes the arrays it needs from the state and passes them to an `@njit` kernel; kernels take and return arrays only, and never touch global state. Debugging still works with `NUMBA_DISABLE_JIT=1`, which runs the kernels as plain Python.

The reason for the split: Numba treats module globals as compile-time constants, so a COMMON block cannot become a mutable module global in Numba code; the kernels see the state only through their arguments.

**Move 2: the new structure.** The translated code is restructured step by step toward the framework of the stubs (one owner for each piece of state, one base class for each family of alternatives), each step checked against the step before it. The state objects of move 1 are the first draft of the classes: a block's variables move into the class that owns them, as the [COMMON-block map](../new-fortran/common-map.md) lays out.

**Move 3: modern Fortran.** Once pyrec is mature, its modules move to modern Fortran one by one, called from Python through F2PY, so that the code runs whole after each move. In KC's experience Numba is not even as fast as C, so this stage is expected to be needed for speed, not left optional.

## Conventions decided once

The translation meets the same Fortran idioms in every routine; each gets one convention, decided before the first routine and written down:

- **Indexing:** Fortran counts from 1, Python from 0. Either shift every index (and every loop bound and stored index, such as zone edges) at translation, or keep a dummy element 0 during move 1; shifting once is cleaner, keeping is safer for differential tests.
- **GOTO flow,** above all in `main.f`'s loops: into `while` loops, `break`, `continue` and early returns, with each label's role in a comment.
- **Column-major arrays:** `HCOMP(NSP, M)` keeps one shell contiguous in Fortran; in NumPy's row-major order, `(NSP, m)` keeps one species contiguous. Keep YREC's index order and accept the other memory layout, or transpose; the kernels' loops follow the choice.
- **Implicit typing:** every variable's type made explicit (names starting I–N are integers in Fortran 77), and single against double precision decided per variable.
- **COMMON blocks:** into state objects, passed explicitly; never module globals in Numba code (above).

## Testing

**Differential tests, routine by routine.** A structure-preserving translation lets each Python routine be checked against its Fortran original on the same inputs, by calling the frozen Fortran through F2PY. A routine is done when it agrees on its inputs from real runs and on edge cases.

**Bug for bug first.** Move 1 reproduces the Fortran, apparent bugs included, and marks each one found in Stage 1 (the questions on each file's page) with a comment. Each is fixed later, in its own commit, with its own benchmark change.

## Open questions

1. *[KC]* **Speed.** Python loops over shells would be perhaps 100–1000 times slower than Fortran; NumPy over shells and the Numba kernels close much of the gap while keeping debugging possible. How slow may pyrec be while it is developed (a model a minute? a track an hour?), and which kernels are profiled first?
2. *[KC]* **The benchmarks need a tolerance per quantity,** not identical output: Python and Numba change the order of floating-point operations, so results agree to round-off, not bit for bit. Each output quantity (log L, log Teff, the central values, the surface abundances, the ages) needs its own tolerance. The development branch's 298-case suite could serve, if that branch is the frozen version.
3. *[KC]* **Which version is frozen:** rp_1, as the notes describe it, or the development branch, which has removed nine obsolete options and turned each COMMON block into a module (whose modules F2PY wraps more easily)?
4. *[KC]* **Telling YREC's developers early,** before move 1 starts: the plan takes a frozen copy of the code they maintain as its reference, and move 3 would hand them a new code.
