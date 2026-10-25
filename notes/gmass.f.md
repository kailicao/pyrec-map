## Explanation

**Purpose.** `GMASS` returns the mean mass per nucleus (in atomic mass units) of a fully ionized mixture of H, He, C, N, O and Ne, given the hydrogen and metal mass fractions $X$ and $Z$. On the way it returns the number fractions of the six elements, the number of free particles per nucleus, and the mixture's ground-state energy, which the equation of state needs.

**How it fits.**
- **Who calls it:** only [[esac.f#ESAC|`ESAC`]], the OPAL equation-of-state interface. Two near copies serve the other EOS versions: [[gmass01.f|`gmass01.f`]] (for `ESAC01`) and [[gmass06.f|`gmass06.f`]] (for `ESAC06`).
- **Arguments:** inputs `X`, `Z`; outputs `AMOLES`, `EGROUND`, `FRACZ`, `FRAC(1..6)` and the function value. No COMMON blocks, no calls.
- **Outputs used by:** `ESAC`, which passes `AMOLES` and the mean mass (its `TMASS`) to [[radsub.f#RADSUB|`RADSUB`]] and uses them to scale one of its interpolated quantities.

**The method.** The metals are split in fixed number proportions $x_\mathrm{C} = 0.2471$, $x_\mathrm{N} = 0.0621$, $x_\mathrm{O} = 0.5284$, $x_\mathrm{Ne} = 0.1624$ (`XC`, `XN`, `XO`, `XNE`). With atomic masses $A_i$ (`AMAS`), the number of moles per gram of each species is

$$n_\mathrm{H} = \frac{X}{A_\mathrm{H}},\quad n_\mathrm{He} = \frac{1-X-Z}{A_\mathrm{He}},\quad n_k = f_Z\,x_k,\quad f_Z = \frac{Z}{\sum_k x_k A_k}\ (k = \mathrm{C,N,O,Ne}),$$

and the number fractions are $\mathrm{FRAC}_i = n_i/\sum_j n_j$, stored in the order Ne, O, N, C, He, H (indices 1 to 6). With $Z_i$ the nuclear charges (`ANUM`) and $E_i$ the ground-state energies of the ions (`EION`, units not stated in the code),

$$\mathrm{AMOLES} = \sum_i (1+Z_i)\,\mathrm{FRAC}_i,\qquad \mathrm{EGROUND} = \sum_i E_i\,\mathrm{FRAC}_i,$$

$$\mathrm{GMASS} = (\mathrm{AMOLES}-1)\,m_e + \sum_i A_i\,\mathrm{FRAC}_i ,$$

where $\mathrm{AMOLES}-1$ is the number of electrons per nucleus and $m_e = 0.00054858$ amu.

## Questions for the experts

1. **Electron mass.** `GMASS` adds the electrons' mass, while `GMASS01` and `GMASS06` start the sum from zero and leave it out. Which is intended for each EOS version?
2. **Ionization energies.** `EION` here differs slightly from the values in `gmass01.f` and `gmass06.f` (e.g. −3388.637 against −3394.874 for Ne). Which source does each set come from?

### GMASS

The mean nuclear mass with electrons; equations above. The metal mixture (C, N, O, Ne proportions) is fixed in the code, not taken from the run's mixture.
