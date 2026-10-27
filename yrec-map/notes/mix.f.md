## Explanation

**Purpose.** `MIX` updates the composition of a model over one time step: nuclear burning, mixing of convection zones, semiconvection, gravitational settling and deuterium burning. Its header gives the outline: (1) find the convection zones and the mixed regions with overshoot; (2) compute the burning rates for the given composition, density and temperature; (3) solve implicitly for the abundances in radiative regions; (4) solve for burning in each convection zone; (5) semiconvection if desired; (6) microscopic diffusion if desired. The header also says that `MIX` is called "prior to rezoning and on the third level of iteration in the Henyey portion".

**How it fits.**
- **Inputs:** the model (`HD`, `HL`, `HP`, `HR`, `HS` = $\log m$, `HS1` = $m$, `HS2` = shell masses, `HSTOT`, `HT`, `LC`, `M`), the composition `HCOMP(15,M)`, the step `DELTS` (s), the iteration level `ITLVL`, `TEFFL` and the mixing length `CMIXL`, passed on to `SCONVEC`. Parameters come from `NMLPAR_MOD`: `DPENV`, `LSEMIC`, the settling switches and limits (`LDIFY`, `XMIN`, `YMIN`, `DT_GS`, `LNEWDIF`), `TCUT`, the accretion settings (`LMDOT`, `DMDT0`, `COMPACC`) and `LEXCOM`, all set by [[parmin.f#PARMIN|PARMIN]].
- **Who calls it:** [[crrect.f#CRRECT|CRRECT]] and the main program in [[main.f|main.f]].
- **What it calls:** [[convec.f#CONVEC|CONVEC]] (zones), [[rates.f#RATES|RATES]] and [[deutrate.f#DEUTRATE|DEUTRATE]] (rates), [[kemcom.f#KEMCOM|KEMCOM]] (implicit burning), [[eqburn.f#EQBURN|EQBURN]] (explicit burning at `ITLVL = 1`), [[sconvec.f#SCONVEC|SCONVEC]] (semiconvection), [[microdiff.f#MICRODIFF|MICRODIFF]] or [[grsett.f#GRSETT|GRSETT]] (settling), and [[dburn.f#DBURN|DBURN]] (deuterium).
- **Outputs:** `HCOMP` in place; the time step in years `DDAGE`; the zone edges `JCORE`, `JENV`, `MXZONE`, `MXZON0`. The burning rates go to `HCOMPM` in `BURN_MOD`, which [[hpoint.f#HPOINT|HPOINT]] and [[rotmix.f#ROTMIX|ROTMIX]] read. The deuterium rate goes to `DRATE` in `DEUTER_MOD`. The mixed zones are printed to `ISHORT`.
- **Modules:** besides those above, `CONSTANTS_MOD` (`CLN`, `CGL`, `CSECYR`), `IOUNITS_MOD` (`ISHORT`) and `DIMENSIONS_MOD` (`JSON`).

**The method.**
1. **Deep mixing.** If `DPENV < 1` (and `ITLVL > 1`), every shell with $m \le \mathrm{DPENV}\,M_\ast$ is flagged convective in a copy of the flags (`LCC`) before `CONVEC` finds the zones; a commented-out variant used a fraction of the peak luminosity instead (MHP 1/95). Otherwise `LCC = LC`.
2. **Rates.** For every shell hotter than `TCUT(1)`, `RATES` gives the rates `HR1`–`HR13`, `HF1`, `HF2`, and `DEUTRATE` the deuterium rate if the surface (or accreted) deuterium exceeds $10^{-11}$. Cooler shells get zero rates.
3. **Implicit burning.** `KEMCOM` solves shell by shell in radiative zones (down to the `TCUT(1)` cutoff) and zone by zone in convective ones, which also homogenizes them.
4. **Explicit burning** (only `ITLVL = 1`): `EQBURN` gives hydrogen and helium burning rates assuming equilibrium ³He and CN abundances, which overwrite $X$, $Z$, ¹²C and ¹⁶O: $X \to X + \dot X\,\Delta t$, $Z \to Z - \dot Y\,\Delta t$, with $\Delta t$ = `DDAGE`$\times10^{-9}$ (Gyr).
5. **Semiconvection** (`LSEMIC`, `ITLVL > 1`): `SCONVEC`. Then, if `LSEMIC` or `ITLVL = 1`, each convection zone is mixed to its mass-weighted mean, $\bar X_k = \sum_j X_{k,j}\,\Delta m_j / \sum_j \Delta m_j$.
6. **Settling** (`LDIFY`): with $d\ln P/dr$ from hydrostatic equilibrium,
$$\frac{d\ln P}{dr} = -\frac{G\,m\,\rho}{r^2\,P}$$
(`HQPR`, from the logs and $\log G$ = `CGL`), and the helium settling time at the outer boundary (the first shell with $Y >$ `YMIN`, searching inward from `JENV`, the base of the surface convection zone), from Michaud et al. (1984) as the comment cites,
$$\tau = 4.348\times10^{21}\ \mathrm{yr}\;\frac{\Delta M/M_\ast}{T^{3/2}},$$
where $\Delta M/M_\ast$ is the mass fraction above that shell, the step is split into `NSTEP` substeps of at most `DT_GS`$\times\tau$, each running `MICRODIFF` (if `LNEWDIF`) or `GRSETT`.
7. **Clean-up.** Every abundance is clipped to $[0,1]$, $Z \le 1 - X - X_{^3\mathrm{He}}$, and $Y = 1 - X - Z - X_{^3\mathrm{He}}$.
8. **Deep mixing again:** `CONVEC` is called with the true flags `LC` to reset `JCORE` and `JENV`.
9. **Deuterium** (`LEXCOM`): `DBURN`, shell by shell in radiative zones and per convection zone.

**Design.** `MIX` switches settling off for the rest of the run (it sets `LDIFY = .FALSE.` in `NMLPAR_MOD`) once the central hydrogen falls below `XMIN`. A model without a surface convection zone gets only a warning ("diffusion not meaningful") and no settling.

**KC's changes.** 2025-05-31: unused arguments removed from the subroutine (`QDT`, `QDP`) and from the calls to `RATES`, `DEUTRATE`, `KEMCOM` and `EQBURN`.

**Changed since `rp_1`.** `CMIXL` is a new last argument (formerly `/CONST3/`), passed on to `SCONVEC`; COMMON blocks to modules, `IMPLICIT NONE`; the unused `/OLDMOD/`, `/COMP/`, `/THEAGE/`, `/NEWENG/` (and `/CTLIM/`, whose `TCUT` now comes from `NMLPAR_MOD`) are gone, which settles the former question 6.

## Questions for the experts

1. **The number of settling substeps.** `NSTEP = INT(DELTS/DTMAX)`, then `IF(MOD(DTMAX,DELTS).NE.0) NSTEP=NSTEP+1`. The arguments of `MOD` look swapped (the ceiling would test `MOD(DELTS,DTMAX)`), and when `DTMAX` is an exact multiple (two or more) of `DELTS`, `NSTEP` stays 0 and `DT = DELTS/0`. [[rotmix.f#ROTMIX|ROTMIX]] has the same line with `.OR.NSTEP.EQ.0` added. Should `MIX` get the same fix?
2. **`DPENV`: centre or surface?** The comment says "DPENV mixes the star from the surface to mass fraction DPENV, e.g. DPENV = 0.7 means the outer .3 of the star is mixed", but the code (and the next comment, "mix from center to a fixed mass fraction") flags the shells *inside* $\mathrm{DPENV}\,M_\ast$. Which is meant?
3. **Settling switched off for good.** `LDIFY = .FALSE.` in `NMLPAR_MOD` when $X_c <$ `XMIN` stops all settling, including that of metals and light elements, for the rest of the run, and `MICRODIFF` is reached only when `LDIFY` is true. Is metal or lithium settling without helium settling meant to be possible?
4. **Convection flags for settling.** `MIX` passes `LCC` (the flags before overshoot, or the deep-mixing flags) to `MICRODIFF`, while `ROTMIX` passes flags built from the mixed zones, overshoot included. Should the two agree?
5. **Units of `DT` in the burning steps.** The explicit and deuterium burning use `DT = DDAGE*1.0D-9` (Gyr). Are `EQBURN`'s rates and `DBURN` per Gyr? (The units are not stated here.)
