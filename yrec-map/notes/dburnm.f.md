## Explanation

**Purpose.** The same deuterium burning as [[dburn.f#DBURN|DBURN]], for the substeps of a model in the middle of a time step: it is called by [[midmod.f#MIDMOD|MIDMOD]] with rates interpolated to the substep and with the accreted mass scaled to the substep's share ("unlike the routine called by MIX, the timestep here is only a portion of the total model DT"). Its header still says "DBURN."

**How it fits.**
- **Inputs:** as DBURN, plus `DRATEM`, `DRATEM0` (the rates at the end and start of the substep, interpolated in MIDMOD from `DRATE0`, `DRATE` with the fraction `FAC2`) and `FAC2` itself. `DT` is in seconds (MIDMOD's `FAC2 = DT/DELTS`), converted to Gyr with `DTT = DT*1.0D-9/CSECYR` (`CSECYR` from `CONSTANTS_MOD`, formerly `/CONST3/`). The other module data are DBURN's: `HCOMPP` from `OLDMOD_MOD`, `FMASSACC` from `DEUTER_MOD`, `LMDOT` and `COMPACC` from `NMLPAR_MOD`.
- **Who calls it:** [[midmod.f#MIDMOD|MIDMOD]].
- **Output:** `HCOMP` (H, $^3$He, D) over the shell or zone.

**The method.** As in DBURN: mass-weighted means over the zone, substeps with $X_D \leftarrow X_D e^{-2r_k\Delta t/n}$ (the factor 2 as in DBURN, whose question 2 asks what it is for, [[dburn.f#q2]]), then $\Delta X = \tfrac12\Delta X_D$ and $\Delta X_3 = -\tfrac32\Delta X_D$. The differences from DBURN:
- the threshold for zeroing deuterium is $10^{-14}$ (DBURN: $10^{-11}$) and does not include the accreted D;
- with accretion, the substep's share of the accreted matter is $f_a$ = `FAC2*FMASSACC`, in grams, since `FMASSACC` is the accreted mass ([[mdot.f#MDOT|MDOT]] sets it to `DELM`); with $M$ = `SUMM` the region's mass (for a single shell, its own mass), the new mean is weighted by mass, as in DBURN:
$$X_D = \frac{X_{D,\mathrm{old}}\,M + f_a X_{D,\mathrm{acc}}}{M + f_a}.$$

> **Question** ([[#L83]]; [[dburn.f#L75-L80]]; [[#L50]]). **Two copies.** DBURN and DBURNM share almost all their code but differ in the time unit of `DT` and in the zeroing test: $10^{-11}$ in DBURN, with the accreted D included at the surface, against $10^{-14}$ here, without it. Which test is right, and can the two become one routine in the overhaul? See also the questions on [[dburn.f#DBURN|DBURN]].

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`, and the unused `/CONST1/` gone.

**Changed since `a8a5950`.** The accretion blend is weighted by mass, $(X M + X_\mathrm{acc} f_a)/(M + f_a)$, as in DBURN; before, it divided by $1 + f_a$ with $f_a$ in grams, so any accretion replaced the region's D, H, and $^3$He by the accreted values. For a single shell, the region mass `SUMM` is now set to the shell's own mass (before, a value left from an earlier call). This settles former question 2.

## Bugs, by priority

1. **(not reached)** **`FMASSACC` is read under mass loss.** ([[#L109]]; [[#L140-L145]]) As in DBURN ([[dburn.f#b1]]): The accretion branch does not test `DMDT0 > 0`, so in a run that only loses mass it blends with an `FMASSACC` that [[mdot.f#MDOT|MDOT]] never set ([[mdot.f#L320]], [[deuter_mod.f#L30]]); with the usual zero start value the result is the same as without accretion. Only with `LMDOT` (off by default).

    **A possible fix:**

    ```diff
    --- a/src/dburnm.f
    +++ b/src/dburnm.f
    @@ -106,7 +106,10 @@
              R0 = R0 + DELRATE
           END DO
     C INCLUDE MASS ACCRETION FROM DEUTERIUM BURNING
    -      IF(LMDOT .AND. IEND.EQ.M)THEN
    +C 11/09/26 KC via Claude
    +C code changed to take the accretion branch only when mass is gained,
    +C since MDOT sets FMASSACC only then.
    +      IF(LMDOT .AND. IEND.EQ.M .AND. DMDT0.GT.0.0D0)THEN
     C ACCRETED MATTER IS EXPOSED TO BURNING FOR, ON
     C AVERAGE. 1/2 OF THE TIMESTEP.  FMASSACC IS
     C DEFINED AS DMDT*DT/ORIGINAL CZ MASS.
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached in any of 34 runs (26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones). DBURNM runs only in MIDMOD, which only GETW calls, in rotating runs, and the two made-up mass-loss runs (YREC's 3 $M_\odot$ main-sequence and 1 $M_\odot$ giant-branch cases with `LMDOT` and `LREIMER` on) do not rotate. Reaching it needs `LMDOT` with `LROT`, which no case of YREC's sets. In DBURN, where the same branch was taken under mass loss ([[dburn.f#b1]]), `FMASSACC` was 0 and the result unchanged.

### DBURNM

Deuterium burning over a substep in MIDMOD, with interpolated rates and the substep's share of accretion; otherwise as [[dburn.f#DBURN|DBURN]].
