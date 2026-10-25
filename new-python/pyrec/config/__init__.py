"""Settings: the single source of a job's settings, read once and checked.

Modules
-------
settings : Config, its parts (dataclasses with __slots__), KindCard.

Counterpart: new-fortran/kernels.md
"""
from .settings import Config, KindCard
