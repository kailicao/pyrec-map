## Explanation

**Purpose.** This file burns deuterium over a time step in one shell or one mixed region (a convection zone), with the rate varying linearly from its start-of-step to its end-of-step value, and updates hydrogen and $^3$He accordingly. With mass accretion, it also burns the accreted deuterium in the surface convection zone.

**How it fits.**
- **Inputs:** the arguments `IBEGIN`, `IEND` (the shell or zone), `M`, `HS2` (the mass of each shell), `HCOMP`, `DT` (the time step; [[mix.f#MIX|MIX]] passes $\Delta t$ in Gyr, `DDAGE*1.0D-9`); the start-of-step composition `HCOMPP` (`/OLDMOD/`); the rates `DRATE0`, `DRATE` (`/DEUTER/`, from [[deutrate.f#DEUTRATE|DEUTRATE]]) and `FMASSACC` (`/DEUTER/`, the mass accreted over the step in grams, set by [[mdot.f#MDOT|MDOT]] when mass is gained); `LMDOT`, `DMDT0`, `COMPACC` (`/MASSCHG/`).
- **Who calls it:** [[mix.f#MIX|MIX]], only with `LEXCOM` (the extended composition, 15 species): for each radiative shell, from the centre out until $T$ falls below `TCUT(1)`, and for every convection zone.
- **Output:** `HCOMP` (species 1, 4 and 12: H, $^3$He, D) over the shell or zone.

**The method.**
1. For a zone, mass-weighted means of $X$, $X_D$, $X_3$ and of the rates.
2. If $X_D$ (with the accreted D, at the surface) is below $10^{-11}$, set it to zero and return (leaving $X$ and $^3$He as they are).
3. Burn in `ISTEP` = $\lfloor r\Delta t/0.1\rfloor + 1$ substeps, the rate rising linearly, with $r_k$ the rate at the substep's midpoint:
$$X_D \leftarrow X_D\,e^{-2 r_k\,\Delta t/n}.$$
4. Mass bookkeeping of D + p $\to$ $^3$He: with $\Delta X_D < 0$ the change of deuterium,
$$\Delta X = \tfrac12\,\Delta X_D, \qquad \Delta X_3 = -\tfrac32\,\Delta X_D.$$
5. **Accretion** (`LMDOT`, surface zone): matter accreted earlier in the step burns fully, new matter is exposed to half a substep's burning; then the zone's values are mass-weighted means of the old and the accreted matter.

## Questions for the experts

1. **An outdated comment, and the weighting in DBURNM.** The comment defines `FMASSACC` as "DMDT*DT/original CZ mass" (a fraction), but [[mdot.f#MDOT|MDOT]] sets it to `DELM` = `DMDT*CMSUN*DELTS/CSECYR`, the accreted mass in grams. DBURN's means, weighted by `SUMM` (grams) and `FMASSACC`, are therefore consistent; [[dburnm.f#DBURNM|DBURNM]]'s, `(XH2NO + XH2NA*FMASSA)/(1 + FMASSA)`, treat that mass in grams as a fraction. The comment should be updated, and DBURNM checked.
2. **`SUMM` for one shell.** When `IBEGIN = IEND`, `SUMM` is never set, but the accretion branch uses it (if the surface zone is a single shell); it keeps a value from an earlier call (`SAVE`).
3. **The substep size.** The comment says the burning per substep is limited to 0.5 in the natural log; the code limits $r\,\Delta t/n$ to 0.1, that is $2r\Delta t/n \le 0.2$. Only the comment is off.
4. **Accretion branch under mass loss.** MDOT sets `FMASSACC` only when mass is gained. The zeroing test checks `DMDT0 > 0`, but the accretion branch of the burning (`LMDOT .AND. IEND.EQ.M`) does not, so with mass loss it mixes in a stale `FMASSACC` from an earlier accreting step (or 0). Should it test `DMDT0 > 0` too?

### DBURN

Deuterium burning over the step in a shell or zone, with a linearly varying rate in substeps, the H and $^3$He bookkeeping, and accreted deuterium at the surface.
