## Explanation

**Purpose.** The same deuterium burning as [[dburn.f#DBURN|DBURN]], for the substeps of a model in the middle of a time step: it is called by [[midmod.f#MIDMOD|MIDMOD]] with rates interpolated to the substep and with the accreted mass scaled to the substep's share ("unlike the routine called by MIX, the timestep here is only a portion of the total model DT"). Its header still says "DBURN".

**How it fits.**
- **Inputs:** as DBURN, plus `DRATEM`, `DRATEM0` (the rates at the end and start of the substep, interpolated in MIDMOD from `DRATE0`, `DRATE` with the fraction `FAC2`) and `FAC2` itself. `DT` is in seconds (MIDMOD's `FAC2 = DT/DELTS`), converted to Gyr with `DTT = DT*1.0D-9/CSECYR` (`CSECYR` from `CONSTANTS_MOD`, formerly `/CONST3/`). The other module data are DBURN's: `HCOMPP` from `OLDMOD_MOD`, `FMASSACC` from `DEUTER_MOD`, `LMDOT` and `COMPACC` from `NMLPAR_MOD`.
- **Who calls it:** [[midmod.f#MIDMOD|MIDMOD]].
- **Output:** `HCOMP` (H, $^3$He, D) over the shell or zone.

**The method.** As in DBURN: mass-weighted means over the zone, substeps with $X_D \leftarrow X_D e^{-2r_k\Delta t/n}$, then $\Delta X = \tfrac12\Delta X_D$ and $\Delta X_3 = -\tfrac32\Delta X_D$. The differences from DBURN:
- the threshold for zeroing deuterium is $10^{-14}$ (DBURN: $10^{-11}$) and does not include the accreted D;
- with accretion, the substep's share of the accreted matter is $f_a$ = `FAC2*FMASSACC`, and the new mean is
$$X_D = \frac{X_{D,\mathrm{old}} + f_a X_{D,\mathrm{acc}}}{1 + f_a},$$
written as a weighting by fractions. But `FMASSACC` is the accreted mass in grams ([[mdot.f#MDOT|MDOT]] sets it to `DELM`), so $f_a$ is in grams too (question 2).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`, and the unused `/CONST1/` gone.

## Questions for the experts

1. **Two copies.** DBURN and DBURNM share almost all their code but differ in the time unit of `DT`, the threshold ($10^{-11}$ against $10^{-14}$) and the accretion weighting; neither tests `DMDT0 > 0` in its accretion branch. Which behavior is right, and can the two become one routine in the overhaul? See also the questions on [[dburn.f#DBURN|DBURN]].
2. **The accretion weighting.** `FMASSA = FAC2*FMASSACC` is a mass in grams, yet the means divide by `1 + FMASSA`, as if it were a fraction of the zone's mass. The accreted matter then gets nearly all the weight, so $X_D$, $X$ and $^3$He of the surface zone jump towards the accreted values. DBURN weights by the zone's mass `SUMM` (grams) instead. This looks like a bug: should it be `(XH2NO*SUMM + XH2NA*FMASSA)/(SUMM + FMASSA)`?

### DBURNM

Deuterium burning over a substep in MIDMOD, with interpolated rates and the substep's share of accretion; otherwise as [[dburn.f#DBURN|DBURN]].
