## Explanation

**Purpose.** `COMP_MOD` holds the composition of the envelope and the star's total and envelope masses, shared by 23 routines. It replaces `COMMON/COMP/` (MHP via Claude, 10/14/26), with the same names and types (`REAL*8` throughout) and an explicit `SAVE`.

**What its variables hold, who sets them, who reads them.**
- `XENV`, `ZENV`: the envelope's $X$ and $Z$. [[starin.f#STARIN|`STARIN`]] sets them from `XNEW`, `ZNEW`; [[rscale.f#RSCALE|`RSCALE`]] and [[parmin.f#PARMIN|`PARMIN`]] may reset `ZENV`. Read by the equation of state ([[eqstat2.f#EQSTAT2|`EQSTAT2`]], [[eqscve.f#EQSCVE|`EQSCVE`]], [[setscv.f#SETSCV|`SETSCV`]]), [[mu.f#MU|`MU`]], [[physic.f#PHYSIC|`PHYSIC`]], [[getopac.f#GETOPAC|`GETOPAC`]] (`ZENV`), [[checkc.f#CHECKC|`CHECKC`]] and [[wrtmil.f#WRTMIL|`WRTMIL`]].
- `ZENVM`: "Z other than CNO cycle elements" (STARIN's comment): `ZENV` times the share of the metals' relative mass fractions left after removing `V(6)`, `V(8)`, `V(9)`; set in `STARIN`, read by [[mixcz.f#MIXCZ|`MIXCZ`]].
- `AMUENV`, `FXENV(12)`: set in `STARIN` from the envelope's mass fractions $X_i$ and atomic weights $A_i$ of the twelve species: $\mathtt{AMUENV} = \sum_i X_i/A_i$, the inverse mean molecular weight per ion (as PHYSIC's comment says), and `FXENV(I)` $= (X_i/A_i)/\mathtt{AMUENV}$, the number fractions. Read by `MU`, `EQSTAT2` (which passes `FXENV` on to the Saha solver), `PHYSIC` and `CHECKC`, which correct `AMUENV` for the local $X$ and $Z$.
- `XNEW`, `ZNEW`: the surface $X$ and $Z$ for which the surface opacity table was last made. Set in `STARIN`, `RSCALE` and [[hpoint.f#HPOINT|`HPOINT`]] (which calls [[surfopac.f#SURFOPAC|`SURFOPAC`]] when the surface $X$ has changed by more than $10^{-8}$); read by [[crrect.f#CRRECT|`CRRECT`]] and [[wrtout.f#WRTOUT|`WRTOUT`]].
- `STOTAL`: $\log M_*$, set from `HSTOT` in `STARIN`, `RSCALE` and [[mdot.f#MDOT|`MDOT`]]; read by the envelope and surface routines ([[qenv.f#QENV|`QENV`]], [[surfbc.f#SURFBC|`SURFBC`]], [[getnewenv.f#GETNEWENV|`GETNEWENV`]]), [[calcad.f#CALCAD|`CALCAD`]], `MIXCZ` and the output routines.
- `SENV`: $\log(m/M_*)$ at the fitting point between the interior model and the envelope. Set in `STARIN`, `HPOINT` (when outer points are added or removed), `MDOT`, `GETNEWENV` and `CRRECT`; read by [[envint.f#ENVINT|`ENVINT`]], which integrates the envelope down to it.

**Design.** A blanket `USE COMP_MOD` in each routine, the convention of the conversion: all 23 files declared the block identically, so the module brings in exactly the names the block made global. The header says `SAVE` is explicit because module variables are saved implicitly only from Fortran 2008, which the Intel compiler it names predates.

**Changed since `rp_1`.** New file: `COMMON/COMP/` as a module.

## Questions for the experts

1. **A comment that contradicts the code.** STARIN's comment calls `AMUENV` the "mean atomic weight of surface Z", but the code computes $\sum_i X_i/A_i$ over all twelve species, hydrogen and helium included, the inverse mean molecular weight per ion that PHYSIC's comment names. The comment in STARIN could be corrected.
