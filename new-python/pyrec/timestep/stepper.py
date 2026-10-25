"""Step criteria and the time stepper.

Classes
-------
StepCriterion : Base of the family; a user's own criterion is a subclass.
StructureCriterion : PTIME, ATIME(8-11).
HydrogenCriterion : XTIME.
HeliumCriterion : YTIME.
RotationCriterion : WTIME, DTWIND.
SurfaceCriterion : ENTIME (the triangle).
TimeStepper : The next step and the criterion that set it.

Counterpart: new-fortran/timestep.md
"""
from __future__ import annotations

from ..config import KindCard
from ..star import Star, StepStart


class StepCriterion:
    """Base of the step criteria.

    Methods
    -------
    dt_max : Largest step allowed.
    name : For the .short file.
    """

    DT_NOLIMIT = 1.0e20  # [s] "No limit" (HTIMER).

    def dt_max(self, star: Star, start: StepStart, dt_old: float) -> float:
        """Largest step allowed [s]; ``DT_NOLIMIT`` if the criterion does not apply.

        This is a hook for derived classes. The base class does nothing.
        """
        ...

    @property
    def name(self) -> str:
        """The class name, for the .short file."""
        ...


class StructureCriterion(StepCriterion):
    """Changes of structure per step.

    Replaces: ptime.f#PTIME
    """


class HydrogenCriterion(StepCriterion):
    """Change of central hydrogen per step.

    Replaces: xtime.f#XTIME
    """


class HeliumCriterion(StepCriterion):
    """Change of central helium per step, and the helium flash.

    Replaces: ytime.f#YTIME
    """

    LOGRHOC_FLASH = 5.0  # log rho_c at and above which the flash criterion applies (YTIME).
    C_YTIME = 1.0e15  # Scale of YTIME's criterion.
    Y_FLOOR = 1.0e-22  # Floor on Y (YTIME).


class RotationCriterion(StepCriterion):
    """Change of rotation per step.

    Replaces: wtime.f#WTIME
    """


class SurfaceCriterion(StepCriterion):
    """Keeps (Teff, L) inside the envelope triangle.

    Replaces: entime.f#ENTIME
    """


class TimeStepper:
    """The next step, as the most restrictive criterion, limited in growth by ATIME(13).

    Attributes
    ----------
    criteria : list[StepCriterion]
    use_structure : bool
        LPTIME; switched off by the stepper, reset per calibration cycle.
    """

    FINAL_STEP_FRAC = 1.0e-3  # Floor of the final step before ENDAGE, as a fraction of the age (main.f).
    L_NOBURN = 1.0e-34  # [Lsun] "No burning" (HTIMER).

    def next_dt(self, star: Star, start: StepStart, card: KindCard, dt_old: float) -> tuple[float, str]:
        """The step [s] and the name of the criterion that set it.

        Replaces: htimer.f#HTIMER
        """
        ...
