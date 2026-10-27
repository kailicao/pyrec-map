## Explanation

**Purpose.** `GMASS06` is the version of `GMASS` for the 2006 OPAL equation of state. At `rp_1` its code was identical to `GMASS01` apart from its name; `GMASS` and `GMASS01`, for the older tables, are removed since `rp_1`. It returns the mean mass per nucleus (without electrons), and sets the number fractions of H, He, C, N, O, Ne, the particles per nucleus and the ground-state energy.

**How it fits.** Called only by [[esac06.f#ESAC06|`ESAC06`]]. No COMMON blocks or modules, no calls.

**The method.** The metals are split in fixed number proportions $x_\mathrm{C} = 0.2471$, $x_\mathrm{N} = 0.0621$, $x_\mathrm{O} = 0.5284$, $x_\mathrm{Ne} = 0.1624$ (`XC`, `XN`, `XO`, `XNE`). With atomic masses $A_i$ (`AMAS`), the number of moles per gram of each species is

$$n_\mathrm{H} = \frac{X}{A_\mathrm{H}},\quad n_\mathrm{He} = \frac{1-X-Z}{A_\mathrm{He}},\quad n_k = f_Z\,x_k,\quad f_Z = \frac{Z}{\sum_k x_k A_k}\ (k = \mathrm{C,N,O,Ne}),$$

and the number fractions are $\mathrm{FRAC}_i = n_i/\sum_j n_j$, stored in the order Ne, O, N, C, He, H (indices 1 to 6). With $Z_i$ the nuclear charges (`ANUM`) and $E_i$ the ground-state energies of the ions (`EION`, units not stated in the code),

$$\mathrm{AMOLES} = \sum_i (1+Z_i)\,\mathrm{FRAC}_i,\qquad \mathrm{EGROUND} = \sum_i E_i\,\mathrm{FRAC}_i,\qquad \mathrm{GMASS06} = \sum_i A_i\,\mathrm{FRAC}_i,$$

without the electrons' mass (which `GMASS` added). `FRACZ` returns $f_Z$.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`. `GMASS` and `GMASS01`, which the method referred to, are removed, so their equations are given here.

## Questions for the experts

1. **Values inherited from `GMASS01`.** The code was identical to `GMASS01` (for the 2001 tables, removed since `rp_1`) apart from the name, including the ion energies. Were the 2006 tables meant to use other values?

### GMASS06

Mean mass per nucleus, number fractions, particles per nucleus and ground-state energy for a fixed metal mixture (method above).
