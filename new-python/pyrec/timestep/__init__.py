"""The time step: the most restrictive of several criteria, limited in growth.

Imports `config` and `star`.

Modules
-------
stepper : StepCriterion family, TimeStepper.

Counterpart: new-fortran/timestep.md
"""
from .stepper import StepCriterion, TimeStepper
