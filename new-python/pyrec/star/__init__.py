"""The model: one stellar model and the state its stages share.

Imports `kernels`, `config` and `physics`. Shells are NumPy arrays of
length m, centre first; ``hcomp`` is `(NSP, m)` as in YREC, so that one
species over all shells is contiguous in NumPy's row-major order (the
transposed choice of the Fortran design, which keeps one shell
contiguous), which is what the vectorized physics reads.

Modules
-------
model : Star, SurfaceComposition, ShellPhysics, EnvelopeSolution, StepStart.
zones : ConvectionZones.

Counterpart: new-fortran/star.md
"""
from .model import EnvelopeSolution, ShellPhysics, Star, StepStart
