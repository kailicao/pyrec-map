"""The run: the job, its tracks and their steps; calibrations.

The top of the layering; imports every other package.

Modules
-------
calibr : TrackSummary, CalibrBase, SolarCalibr, StarCalibr, MonteCarlo.
run : Run, Track, Step.

Counterpart: new-fortran/run.md
"""
from .run import Run
