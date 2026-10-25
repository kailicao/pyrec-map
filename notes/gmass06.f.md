## Explanation

**Purpose.** `GMASS06` is the version of [[gmass.f#GMASS|`GMASS`]] for the 2006 OPAL equation of state. Its code is identical to [[gmass01.f#GMASS01|`GMASS01`]] apart from its name: the mean mass per nucleus (without electrons), the number fractions of H, He, C, N, O, Ne, the particles per nucleus and the ground-state energy.

**How it fits.** Called only by [[esac06.f#ESAC06|`ESAC06`]]. No COMMON blocks, no calls.

**The method.** See [[gmass.f|`gmass.f`]] for the equations; here $\mathrm{GMASS06} = \sum_i A_i\,\mathrm{FRAC}_i$, without the electrons' mass.

## Questions for the experts

1. **Same as `GMASS01`.** The two files are identical apart from the name, including the ion energies. Were the 2006 tables meant to use other values?

### GMASS06

Same as `GMASS01`.
