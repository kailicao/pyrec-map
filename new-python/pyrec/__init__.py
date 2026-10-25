"""pyrec: YREC in Python, a stub design parallel to the modern-Fortran design.

The same classes and the same split as the Fortran design, as Python
packages layered by dependency (a lower package never imports a higher
one); shells are held as NumPy arrays, and hot loops are marked for Numba
(debug with ``NUMBA_DISABLE_JIT=1``). Bodies are ``...``: this is the target
framework, not code that runs.

Packages
--------
kernels : Constants, species indices, numerical kernels, ODE stepping, Logger.
config : Config and its parts; KindCard.
physics : Physics, PointState and the microphysics families.
star : Star, ShellPhysics, EnvelopeSolution, StepStart; ConvectionZones.
structure : EnvelopeIntegrator, SurfaceBC, StructureSolver, Rezoner.
timestep : StepCriterion family, TimeStepper.
composition : CompositionStep, Semiconvection, ChiGrid; settling.
rotation : RotationStep and its parts; MassLoss.
io : Model files, writers, analyses.
hooks : UserPhysics.
evolve : Run, Track, Step; calibrations.

Counterpart: new-fortran/overview.md, new-fortran/tunables.md, new-fortran/fortran.md, new-fortran/common-map.md

Replaces: main.f
"""
__version__ = "0.0.0"
