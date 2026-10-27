## Explanation

**Purpose.** Rescales a starting model before a run, as asked by a "kind card" (one entry of the run's sequence, number `NK`): the hydrogen abundance $X$, the metallicity $Z$, the abundance of one other species, the total mass and, for horizontal-branch stars, the core mass. It also applies the "ZRAMP" option, a metallicity that changes linearly with mass in the core.

**How it fits.**
- **Who calls it:** [[starin.f#STARIN|`STARIN`]], twice (for the two ways a model is read), when `IRESCA(NK)` is not 1.
- **Inputs:** the model (`HCOMP`, `HS` = $\log_{10} m$ in g, `HSTOT`, `HL`, `LC`, `M`, `SMASS` in solar masses) and, through modules, the targets: `RUNLOOP_MOD`'s `RESCAL(1..4, NK)` (new mass, $X$, $Z$, core mass; a negative or zero value means "no change", except for $Z$, where only a negative value does, so $Z = 0$ can be asked for), and, in `NMLPAR_MOD`, `XNEWCP`, `INEWCP`, `LNEWCP`, `LREL` (one species to set) and `RSCLZC`, `RSCLZM1`, `RSCLZM2`, `LZRAMP` (the ramp), set by the namelist or by [[parmin.f#PARMIN|PARMIN]].
- **What it calls:** [[findsh.f#FINDSH|`FINDSH`]], to locate the hydrogen-burning shell (`JXBEG` to `JXEND`) in a horizontal-branch model.
- **Outputs:** `HCOMP`, `HS`, `HSTOT`, `SMASS` changed in place; in modules, `XNEW`, `ZNEW`, `ZENV`, `STOTAL` (`COMP_MOD`) and `XENV0`, `ZENV0` (`LABEL_MOD`, which [[wrthead.f#WRTHEAD|`WRTHEAD`]] and the output routines print).

**The method.**
1. **$X$.** Every shell's $X$ is multiplied by $X_\mathrm{new}/X_\mathrm{surf}$, capped at $X_\mathrm{new}$. `XENV` is deliberately not changed, since it fixes the mean molecular weight of the Yale equation of state from the first run (MHP 7/99).
2. **$Z$.** The same amount is added in every shell, $Z_j \to \max(0, Z_j + \Delta Z)$ with $\Delta Z = Z_\mathrm{new} - Z_\mathrm{surf}$, and species 5–11 (C12 through O18) are multiplied by $Z_j^\mathrm{new}/Z_j^\mathrm{old}$.
3. **One species** (`LNEWCP`, main sequence only): set to `XNEWCP` everywhere; with `LREL`, `XNEWCP` is first converted from the astronomers' scale, $X_\mathrm{sp} = 10^{\,\texttt{XNEWCP}-12}\,X_\mathrm{surf}$.
4. **Mass, main sequence** (when the central $X > 10^{-10}$): every mass point is multiplied by $M_\mathrm{new}/M_\mathrm{old}$ (in the log, $\log m \to \log m + \log(M_\mathrm{new}/M_\mathrm{old})$); all other variables are kept.
5. **Mass, horizontal branch.** Mass is added or removed outside the hydrogen shell, by stretching the mass coordinate above a fixed point $m_0$:
   $$m \to m_0 + s\,(m - m_0),\qquad s = \frac{M_\mathrm{new} - m_0}{M_\mathrm{old} - m_0}.$$
   If more than $0.01\,M_\odot$ lies outside the core, $m_0$ is the top of the shell ("old method"); otherwise the base of the shell ("new method").
6. **Core mass, horizontal branch.** The core's points are multiplied by $M_\mathrm{core}^\mathrm{new}/M_\mathrm{core}^\mathrm{old}$, the shell's points shifted by the change $\Delta M_\mathrm{core}$ (so the shell's mass stays fixed), and the envelope squeezed or stretched so that the total mass is unchanged. The old and new masses are printed.
7. **$Y$** is reset everywhere to $1 - X - Z - X_\mathrm{He3}$.
8. **ZRAMP** (if `LZRAMP` and the three parameters are positive): with $f = m/M_*$, $Z$ is set to $Z_c$ (`RSCLZC`) for $f <$ `RSCLZM1`, and rises linearly to the surface $Z$ between `RSCLZM1` and `RSCLZM2`; $X$ absorbs the change, and species 5–11 are multiplied by a factor `ZFACT`.

**Design.** Several unconditional `write(*,*)` lines ("Entering old method", "SENV", "Envelope") print to the terminal in the horizontal-branch mass rescaling; they look like debugging left on. Many others are commented out.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/CKIND/` to `RUNLOOP_MOD`, `/COMP/` to `COMP_MOD`, `/LABEL/` to `LABEL_MOD`, `/NEWCMP/` and `/ZRAMP/` to `NMLPAR_MOD`, `/LUOUT/` to `IOUNITS_MOD`, the constants to `CONSTANTS_MOD`), the array size `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

## Questions for the experts

1. **The ZRAMP factor (apparent bug).** In the ZRAMP block, `ZFACT = (HCOMP(3,I)-RSCLZC(NK))/HCOMP(3,I)`, that is $(Z_\mathrm{old} - Z_\mathrm{new})/Z_\mathrm{old}$, the fractional change, not the ratio $Z_\mathrm{new}/Z_\mathrm{old}$ used in step 2. With it, the CNO species are scaled by about $1 - Z_c/Z$, and become negative when $Z_c > Z$. Was the ratio meant?
2. **The error message for one species.** Format 1004 prints `ICOMP`, which is never set (the species index is `INEWCP`), and ends "Z NOT RESCALED" for any species.
3. **`XNEWCP` converted in place.** With `LREL`, the value in `NMLPAR_MOD` is overwritten by the converted mass fraction. If `RSCALE` runs again in the same job (another kind card), the converted value is converted a second time. Also, `XNEWCP` is one value for all kind cards. Intended?
4. **He3 and the $Z$ rescaling.** The comment says "THE CNO CYCLE ELEMENTS AND HE3 ARE MULTIPLIED BY THE RATIO", but the loop covers species 5–11 only; He3 is species 4 and is not scaled. Which is meant?
5. **Debug output.** Remove or put behind a debug flag the unconditional `write(*,*)` lines in the horizontal-branch branch?
6. **The 0.01 solar-mass switch.** The choice between the two horizontal-branch methods depends on whether the mass outside the core exceeds $0.01\,M_\odot$, a hard-coded value. Where does it come from?
