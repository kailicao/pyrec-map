## Explanation

**Purpose.** `GMASS01` is the version of [[gmass.f#GMASS|`GMASS`]] for the 2001 OPAL equation of state: the mean mass per nucleus of a fully ionized H, He, C, N, O, Ne mixture, its number fractions, particles per nucleus and ground-state energy.

**How it fits.** Called only by [[esac01.f#ESAC01|`ESAC01`]]. No COMMON blocks, no calls. Arguments as in `GMASS`.

**The method.** As in [[gmass.f#GMASS|`GMASS`]], with two differences: the ionization energies `EION` take other values, and the result leaves out the electrons' mass:

$$\mathrm{GMASS01} = \sum_{i} A_i\,\mathrm{FRAC}_i .$$

The variable `ANUME` (electrons per nucleus) is computed but not used.

## Questions for the experts

1. **Electron mass left out.** Unlike `GMASS`, the electrons' mass is not added (`gmass01=0D0` before the sum, and `ANUME` is unused). Intended?
2. **Near-duplicate code.** `gmass01.f` and `gmass06.f` are identical apart from the function name. Could one routine serve both EOS versions?

### GMASS01

Mean nuclear mass without electrons, with the OPAL 2001 ion energies.
