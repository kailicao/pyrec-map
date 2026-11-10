## Explanation

**Purpose.** Rescales a starting model before a run, as asked by a "kind card" (one entry of the run's sequence, number `NK`): the hydrogen abundance $X$, the metallicity $Z$, the abundance of one other species, the total mass and, for horizontal-branch stars, the core mass. It also applies the "ZRAMP" option, a metallicity that changes linearly with mass in the core.

**How it fits.**
- **Who calls it:** [[starin.f#STARIN|`STARIN`]], once (the model is read and, if asked, its core extended first), when `IRESCA(NK)` is not 1.
- **Inputs:** the model (`HCOMP`, `HS` = $\log_{10} m$ in g, `HSTOT`, `HL`, `LC`, `M`, `SMASS` in solar masses) and, through modules, the targets: `RUNLOOP_MOD`'s `RESCAL(1..4, NK)` (new mass, $X$, $Z$, core mass; a negative or zero value means "no change"), and, in `NMLPAR_MOD`, `XNEWCP`, `INEWCP`, `LNEWCP`, `LREL` (one species to set) and `RSCLZC`, `RSCLZM1`, `RSCLZM2`, `LZRAMP` (the ramp), set by the namelist or by [[parmin.f#PARMIN|PARMIN]].
- **What it calls:** [[findsh.f#FINDSH|`FINDSH`]], to locate the hydrogen-burning shell (`JXBEG` to `JXEND`) in a horizontal-branch model.
- **Outputs:** `HCOMP`, `HS`, `HSTOT`, `SMASS` changed in place; in modules, `XNEW`, `ZNEW`, `ZENV`, `STOTAL` (`COMP_MOD`) and `XENV0`, `ZENV0` (`LABEL_MOD`, which [[wrthead.f#WRTHEAD|`WRTHEAD`]] and the output routines print).

**The method.**
1. **$X$.** Every shell's $X$ is multiplied by $X_\mathrm{new}/X_\mathrm{surf}$, capped at $X_\mathrm{new}$. `XENV` is deliberately not changed, since it fixes the mean molecular weight of the Yale equation of state from the first run (MHP 7/99). `XENV` and `ZENV` are the reference composition for which [[starin.f#STARIN|`STARIN`]] computes `AMUENV` (the sum of $X_i/A_i$ over the elements) and the number fractions `FXENV` of the elements used in the Saha ionization ([[eqsaha.f#EQSAHA|`EQSAHA`]]); in each shell, [[mu.f#MU|`MU`]] and [[eqstat2.f#EQSTAT2|`EQSTAT2`]] then correct these for the shell's $X - X_\mathrm{env}$ and $Z - Z_\mathrm{env}$ rather than recompute them, so changing `XENV` alone would make it disagree with `AMUENV` and `FXENV`.
2. **$Z$.** The same amount is added in every shell, $Z_j \to \max(0, Z_j + \Delta Z)$ with $\Delta Z = Z_\mathrm{new} - Z_\mathrm{surf}$, and species 5–11 (C12 through O18) are multiplied by $Z_j^\mathrm{new}/Z_j^\mathrm{old}$.

    > **Question** ([[#L123-L125]]; [[#L131-L133]]). **He3 and the $Z$ rescaling.** The comment says "THE CNO CYCLE ELEMENTS AND HE3 ARE MULTIPLIED BY THE RATIO," but the loop covers species 5–11 only; He3 is species 4 and is not scaled. Which is meant?

3. **One species** (`LNEWCP`, main sequence only): set to `XNEWCP` everywhere; with `LREL`, `XNEWCP` is first converted from the astronomers' scale, $X_\mathrm{sp} = 10^{\,\texttt{XNEWCP}-12}\,X_\mathrm{surf}$, into a local (`XTARG`), leaving `XNEWCP` as set.

    > **Question** ([[#L156-L171]]; [[nmlpar_mod.f#L109-L112]]). **One `XNEWCP` for all kind cards.** `XNEWCP` (and `INEWCP`, `LREL`) is one value for all kind cards, unlike the per-run `RESCAL`, so every rescaling card sets the same species to the same abundance. Is this intended?

4. **Mass, main sequence** (when the central $X > 10^{-10}$): every mass point is multiplied by $M_\mathrm{new}/M_\mathrm{old}$ (in the log, $\log m \to \log m + \log(M_\mathrm{new}/M_\mathrm{old})$); all other variables are kept.

    > **Question** ([[#L181-L192]]). **Mass rescaling without homology.** Step 4 multiplies every $m$ by $M_\mathrm{new}/M_\mathrm{old}$ and keeps $P$, $T$, $r$, $L$ at each point, so after a large change of mass the rescaled model is far from equilibrium, and the relaxation (`KINDRN` = 2) must absorb the difference. A student would expect a homologous first guess (on the main sequence, for example, $R \propto M^{0.8}$, $L \propto M^{3.5}$, with $P$ and $T$ scaled to match). Was such a scaling tried, and is the lack of it why the User Guide advises several rescalings in turn for large changes? It matters for how large a change one rescaling can make.

5. **Mass, horizontal branch.** Mass is added or removed outside the hydrogen shell, by stretching the mass coordinate above a fixed point $m_0$:
   $$m \to m_0 + s\,(m - m_0),\qquad s = \frac{M_\mathrm{new} - m_0}{M_\mathrm{old} - m_0}.$$
   If more than $0.01\,M_\odot$ lies outside the core, $m_0$ is the top of the shell ("old method"); otherwise the base of the shell ("new method").

    > **Question** ([[#L240]]). **The 0.01 solar-mass switch.** The choice between the two horizontal-branch methods depends on whether the mass outside the core exceeds $0.01\,M_\odot$, a hard-coded value. Where does it come from?

6. **Core mass, horizontal branch.** The core's points are multiplied by $M_\mathrm{core}^\mathrm{new}/M_\mathrm{core}^\mathrm{old}$, the shell's points shifted by the change $\Delta M_\mathrm{core}$ (so the shell's mass stays fixed), and the envelope squeezed or stretched so that the total mass is unchanged. The old and new masses are printed.
7. **$Y$** is reset everywhere to $1 - X - Z - X_\mathrm{He3}$.
8. **ZRAMP** (if `LZRAMP` and the three parameters are positive): with $f = m/M_*$, $Z$ is set to $Z_c$ (`RSCLZC`) for $f <$ `RSCLZM1`, and rises linearly to the surface $Z$ between `RSCLZM1` and `RSCLZM2`; $X$ absorbs the change, and species 5–11 are multiplied by $Z_\mathrm{new}/Z_\mathrm{old}$, as in step 2.

**For users** (from YREC's [User Guide](https://yrec.readthedocs.io/en/latest/userguide.html)). The targets are the control namelist's `RSCLM`, `RSCLX`, `RSCLZ` and `RSCLCM` for each run (copied by [[parmin.f#PARMIN|`PARMIN`]] into `RESCAL` for `KINDRN` = 2 or 3); a negative value means no rescaling. A typical job rescales a library model to the wanted mass, composition and mixing length with a few zero-time-step models, then evolves it; a large change, such as a solar-metallicity template turned into a very metal-poor star, may need several rescalings in turn. The User Guide also advises care, or a starting model made by a script, for core-helium-burning stars, where `RSCLM` stretches only the envelope, `RSCLCM` sets the helium core's mass and `RSCLX` acts on the envelope (the core has no hydrogen), as steps 1, 5 and 6 do. It does not say that zero also means "no change."

**Design.** Several unconditional `write(*,*)` lines ("Entering old method," "SENV," "Envelope") print to the terminal in the horizontal-branch mass rescaling; they look like debugging left on. Many others are commented out.

> **Question** ([[#L242-L245]]; [[#L288-L291]]). **Debug output.** Can these `write(*,*)` lines be removed, or put behind a debug flag?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/CKIND/` to `RUNLOOP_MOD`, `/COMP/` to `COMP_MOD`, `/LABEL/` to `LABEL_MOD`, `/NEWCMP/` and `/ZRAMP/` to `NMLPAR_MOD`, `/LUOUT/` to `IOUNITS_MOD`, the constants to `CONSTANTS_MOD`), the array size `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

**Changed since `a8a5950`.** The ZRAMP block scales species 5–11 by $Z_\mathrm{new}/Z_\mathrm{old}$ instead of $(Z_\mathrm{old} - Z_\mathrm{new})/Z_\mathrm{old}$ (settles former question 1); with `LREL`, the converted target goes into a local, `XTARG`, instead of overwriting `XNEWCP` (settles the first half of former question 3, whose second half is now question 2), and STARIN's first of its two calls is gone, so a reused model is no longer rescaled twice; $Z$ is rescaled only for `RESCAL(3,NK)` > 0, as for the mass and $X$, since the default `RSCLZ` = 0 used to set $Z = 0$; and the three stops on an impossible mass are `STOP 1` (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(not reached)** **The error message for one species names no species.** ([[#L175-L178]]; [[#L38]]) When the target abundance of the one species is 1 or more, format 1004 prints `ICOMP`, a local that is declared and never set (the species index is `INEWCP`), and ends "Z NOT RESCALED" whatever the species. Only the message is wrong: The abundance is left unchanged, as intended. Only with `LNEWCP` (a rescale card on the main sequence with a target $\ge 1$).

    **A possible fix:**

    ```diff
    --- a/src/rscale.f
    +++ b/src/rscale.f
    @@ -172,10 +172,13 @@
                 ELSE
     C  ERROR - RESCALED ABUNDANCE >100% - ABUNDANCE NOT CHANGED
     C               ACOMP = ANEWCP
    -               WRITE(ISHORT,1004)ICOMP,NK,XTARG
    +C 11/09/26 KC via Claude
    +C code changed to print the species index INEWCP, and to name the
    +C species, not Z, as the quantity not rescaled.
    +               WRITE(ISHORT,1004)INEWCP,NK,XTARG
      1004       FORMAT(1X,'ERROR IN SUBROUTINE RSCALE'/1X,'RESCALING OF ',
          *      'SPECIES ',I3,' IN KIND CARD # ',I3,' FAILED - DESIRED COMP',F9.6/1X,
    -     *      'GREATER THAN UNITY.  Z NOT RESCALED')
    +     *      'GREATER THAN UNITY.  SPECIES NOT RESCALED')
                 ENDIF
              ENDIF
     C  RESCALE STAR MASS BY MULTIPLYING ALL MASS POINTS IN THE STAR BY
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged). The block was not reached in the 34 cases run: The one case run that sets `LNEWCP` (`testsuite/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2`, `XNEWCP` = 1.5D-5) did not enter it, and in every YREC case that sets `LNEWCP` the target is 1.5D-5, below 1. No fix was run, since it changes only a message. What would reach it: a rescale card on a model with central hydrogen, with `LNEWCP` on and a target of 1 or more. Intent: none found.

2. **(not reached)** **The "new method" does not check the new total mass against the core.** ([[#L300-L305]]; [[#L310-L311]]; [[#L320-L322]]) The old method stops when the new envelope above the shell would be negative ([[#L250-L258]]), which is exactly when its scale factor would be negative. The new method checks only the old model (`CHKENV`, the old total minus the core), not the target: If `RESCAL(1,NK)` is at or below the core mass `COROLD`, `SFACTOR` is zero or negative, and `HS(I)` for `I` $\ge$ `JXBEG` becomes the log of a mass at or below the core's, or of a negative number (NaN), with no message. Only for a horizontal-branch model with less than $0.01\,M_\odot$ outside the core and a target total mass below its core mass, which is not a sensible input; so this is fragile code rather than a wrong result in practice.

    **A possible fix:**

    ```diff
    --- a/src/rscale.f
    +++ b/src/rscale.f
    @@ -297,7 +297,11 @@
     c            write(*,*)(10**HS(JXEND))/CMSUN,' end'
     c            write(*,*)(10**HS(M))/CMSUN,' M'
     c            write(*,*)(10**HSTOT)/CMSUN,' total'
    -            CHKENV = ((10**HSTOT)/CMSUN)-COROLD
    +C 11/09/26 KC via Claude
    +C code changed to check the new total mass as well as the old against
    +C the core, so that the scale factor below is positive, as the old
    +C method's check of ENVNEW makes it.
    +            CHKENV = DMIN1((10**HSTOT)/CMSUN,RESCAL(1,NK))-COROLD
                 IF(CHKENV.LE.0.0D0)THEN
                    WRITE(ISHORT,69)ENVOLD,ENVOLD+DENV,RESCAL(1,NK),SMASS
     C 10/30/26 MHP via Claude: bare STOP -> STOP 1, the run-time error code (issue 38).
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged). The "new method" was not taken in the 34 cases run, the horizontal-branch cases among them (`testsuite/Test_m0p95feh+0p0_GN93_TAHB`, `examples/run_from_zahb_to_tahb/ZAHB_m0p8feh+0p0_TAHB`). No fix was run, since it only turns the case into the existing stop. What would reach it: a horizontal-branch rescale card with less than $0.01\,M_\odot$ outside the core and a target total mass at or below the core mass. Intent: none found.
