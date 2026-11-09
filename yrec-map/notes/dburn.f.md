## Explanation

**Purpose.** This file burns deuterium over a time step in one shell or one mixed region (a convection zone), with the rate varying linearly from its start-of-step to its end-of-step value, and updates hydrogen and $^3$He accordingly. With mass accretion, it also burns the accreted deuterium in the surface convection zone.

**How it fits.**
- **Inputs:** the arguments `IBEGIN`, `IEND` (the shell or zone), `M`, `HS2` (the mass of each shell), `HCOMP`, `DT` (the time step; [[mix.f#MIX|MIX]] passes $\Delta t$ in Gyr, `DDAGE*1.0D-9`); the start-of-step composition `HCOMPP` ([[oldmod_mod.f#OLDMOD_MOD|`OLDMOD_MOD`]]); the rates `DRATE0`, `DRATE` ([[deuter_mod.f#DEUTER_MOD|`DEUTER_MOD`]], from [[deutrate.f#DEUTRATE|DEUTRATE]]) and `FMASSACC` (`DEUTER_MOD`, the mass accreted over the step in grams, set by [[mdot.f#MDOT|MDOT]] when mass is gained); the settings `LMDOT`, `DMDT0`, `COMPACC` ([[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]], formerly `/MASSCHG/`).
- **Who calls it:** [[mix.f#MIX|MIX]], only with `LEXCOM` (the extended composition, 15 species): for each radiative shell, from the centre out until $T$ falls below `TCUT(1)`, and for every convection zone.
- **Output:** `HCOMP` (species 1, 4 and 12: H, $^3$He, D) over the shell or zone.

**The method.**
1. For a zone, mass-weighted means of $X$, $X_D$, $X_3$ and of the rates, with the zone's mass `SUMM`; for a single shell, `SUMM` is the shell's own mass.
2. If $X_D$ (with the accreted D, at the surface) is below $10^{-11}$, set it to zero and return (leaving $X$ and $^3$He as they are).
3. Burn in `ISTEP` = $\lfloor r\Delta t/0.1\rfloor + 1$ substeps, the rate rising linearly, with $r_k$ the rate at the substep's midpoint:
$$X_D \leftarrow X_D\,e^{-2 r_k\,\Delta t/n}.$$
The code does not say what the factor 2 is for; `DRATE` is divided by the deuteron's mass `AMDEUT` ("Avagadros number divided by the mass of the deuteron in amu", [[deutrate.f#DEUTRATE|DEUTRATE]]), so the second question below asks.

    > **Question** ([[#L89-L94]]). **The substep size.** The comment says the burning per substep is limited to 0.5 in the natural log; the code limits $r\,\Delta t/n$ to 0.1, that is $2r\Delta t/n \le 0.2$. Is only the comment off, or was a coarser substep (0.25 for $r\Delta t/n$) meant?

    > **Question** ([[#L102]]; [[#L120-L122]]; [[deutrate.f#L62]]; [[deutrate.f#L81]]). **The factor 2 in the burning.** The substeps use $X_D \leftarrow X_D e^{-2r\Delta t}$. `DRATE` carries $N_A/A_D$ with $A_D \approx 2$, so $2\,$`DRATE` $\approx X\rho N_A\langle\sigma v\rangle$ per Gyr, which is the destruction rate per deuteron by protons: is that what the factor 2 is for? If so, $N_A/A_p$ with $A_p \approx 1$ would be the natural factor, and the 2 and `AMDEUT` differ slightly ($2/2.013553$); DBURNM uses the same factor.
4. Mass bookkeeping of D + p $\to$ $^3$He: with $\Delta X_D < 0$ the change of deuterium,
$$\Delta X = \tfrac12\,\Delta X_D, \qquad \Delta X_3 = -\tfrac32\,\Delta X_D.$$
5. **Accretion** (`LMDOT`, surface zone): matter accreted earlier in the step burns fully, new matter is exposed to half a substep's burning; then the zone's values are mass-weighted means of the old and the accreted matter.

    > **Question** ([[#L107-L109]]; [[mdot.f#L300-L321]]). **An outdated comment.** The comment defines `FMASSACC` as "DMDT*DT/original CZ mass" (a fraction), but [[mdot.f#MDOT|MDOT]] sets it to `DELM` = `DMDT*CMSUN*DELTS/CSECYR`, the accreted mass in grams. DBURN's means, weighted by `SUMM` (grams) and `FMASSACC`, are therefore consistent (and [[dburnm.f#DBURNM|DBURNM]]'s are since `a8a5950`). Should the comment say "the mass accreted over the step, in grams", here, in DBURNM ([[dburnm.f#L111-L112]]), and in LIBURN ([[liburn.f#L451]])?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`, and the unused `/CONST1/` gone.

**Changed since `a8a5950`.** For a single shell, the region mass `SUMM` is now set to the shell's own mass; before, the accretion blend used the value left from an earlier call (`SAVE`). This settles former question 2 and, with the fix of [[dburnm.f#DBURNM|DBURNM]]'s weighting, the second part of question 1; the later questions are renumbered.

## Bugs, by priority

1. **(d)** **`FMASSACC` is read under mass loss.** ([[#L75]]; [[#L106]]; [[#L128-L132]]) The accretion branch is taken whenever `LMDOT` is set and `IEND` = `M`, also with mass loss ($\dot M \le 0$), while the zeroing test above it checks `DMDT0 > 0` too. [[mdot.f#MDOT|MDOT]] sets `FMASSACC` only when mass is gained ([[mdot.f#L300]], [[mdot.f#L320]]), and [[deuter_mod.f#DEUTER_MOD|`DEUTER_MOD`]] gives it no initial value ([[deuter_mod.f#L30]]). In a run that only loses mass, the blend therefore uses a never-set `FMASSACC`: Compilers usually start module variables at zero, and with zero the branch gives the same result as the `ELSE` branch, so the code is correct in practice but rests on an unset variable. Only with `LMDOT` (off by default). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to take the accretion branch only when mass is gained,
    C as in the zeroing test above, since MDOT sets FMASSACC only then.
          IF(LMDOT .AND. IEND.EQ.M .AND. DMDT0.GT.0.0D0)THEN
    ```

### DBURN

Deuterium burning over the step in a shell or zone, with a linearly varying rate in substeps, the H and $^3$He bookkeeping, and accreted deuterium at the surface.
