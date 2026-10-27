# Settled during the explanations (for reviewers)

- **False function links from arrays** (Oct 25, 2026): `codemap.py` no longer links `NAME(…)` to a FUNCTION when the unit declares `NAME` as an array (DIMENSION, COMMON or a type statement). GETW's `QUAD` link is gone; notes that mention that false link (getw.f, vcirc.f, quad.f) should drop the remark. ESAC and T6RINTERP call the function QUAD for real (quadratic interpolation); those links are right.
