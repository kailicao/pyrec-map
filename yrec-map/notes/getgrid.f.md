## Explanation

**Purpose.** `GETGRID` builds the equally spaced grid on which the diffusion equations for rotational mixing and angular momentum transport are solved. The grid variable is the combination of $\log m$, $L$ and $\log P$ that [[hpoint.f#HPOINT|HPOINT]] uses to place the model's points, with one difference: HPOINT scales $\Delta_L$ by the largest $L$ in the model, GETGRID by the surface $L$.

**How it fits.**
- **Who calls it:** [[mixgrid.f#MIXGRID|MIXGRID]] and [[rotgrid.f#ROTGRID|ROTGRID]], for one region (`IBEG..IEND`).
- **Inputs:** `HL` ($L$ in solar units), `HP` ($\log P$), `HS` ($\log m$).
- **What it calls:** [[osplin.f#OSPLIN|OSPLIN]], a shape-preserving osculatory quadratic spline.
- **Outputs:** in [[egrid_mod.f#EGRID_MOD|`EGRID_MOD`]]: `CHI` (the grid variable at the model points), `ECHI` (equally spaced values), `ES1` (their masses, in g), `DCHI`, `NTOT`. [[eq2mod.f#EQ2MOD|EQ2MOD]], [[seculr.f#SECULR|SECULR]], [[mixcom.f#MIXCOM|MIXCOM]] and [[checkj.f#CHECKJ|CHECKJ]] read them.
- **Modules:** [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] gives the point-spacing tolerances `HPTTOL` (formerly in `/CTOL/`, set in [[parmin.f#PARMIN|PARMIN]]); `EGRID_MOD` (output); $\ln 10$ from [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]].

**The method.** With the model's spacing criteria $\Delta_m$ = `HPTTOL(2)`, $\Delta_L$ = `HPTTOL(9)`$\cdot L_\mathrm{surf}$ (with $L_\mathrm{surf}$ = `HL(M)`), $\Delta_P$ = `HPTTOL(11)`,
$$\chi_i = \frac{\log m_i}{\Delta_m} + \frac{L_i}{\Delta_L} - \frac{\log P_i}{\Delta_P}.$$
The equally spaced grid runs from $\chi_1$ to $\chi_N$ with $N$ = `NTOT` points, $\Delta\chi = (\chi_N - \chi_1)/(N-1)$, and $\log m$ is interpolated onto it with `OSPLIN`, then unlogged.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **Number of points.** `NTOT` is set to the number of model points in the region (at least 3); the formula that set it from the range of $\chi$ ("modulus of final chi plus one") is commented out. So the grid is equally spaced in $\chi$ but has as many points as the model. Is that the intended resolution?
2. **Monotonic $\chi$.** `OSPLIN` needs increasing abscissae. $\chi$ increases outward when $\log P$ decreases and $L$ does not drop sharply; can $L$ decrease enough (for example in a region with neutrino losses) to break this?

### GETGRID

Equally spaced grid in $\chi = \log m/\Delta_m + L/\Delta_L - \log P/\Delta_P$, with the mass of each grid point by spline interpolation.
