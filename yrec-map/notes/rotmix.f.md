## Explanation

**Purpose.** Nuclear burning and gravitational settling for one step of the rotational-mixing loop. Its header comment lists the steps: (1) use [[kemcom.f#KEMCOM|`KEMCOM`]] to solve implicitly for the abundances in radiative regions, shell by shell; (2) solve for the burning in each convection zone as a whole. It then applies the settling of helium and renormalizes the composition.

**How it fits.**
- **Who calls it:** [[midmod.f#MIDMOD|`MIDMOD`]] (with the temperatures at the current time, `HTM`, "for thermodynamic consistency", MHP 6/00) and [[bursmix.f#BURSMIX|`BURSMIX`]], in their loops of substeps.
- **Inputs:** the step `DELTS` (s), the composition `HCOMP(15, ·)`, shell masses `HS2`, temperatures `HT` ($\log T$), densities `HD` (also used for the rates), and the zone lists `MRZONE` (radiative) and `MXZONE` (convective); for the settling, `HS`, `HR`, `HP`, `HS1`, `HSTOT` and the convection flags `LC`. The zone lists come from [[convec.f#CONVEC|CONVEC]], whose end of the surface radiative zone is misplaced ([[convec.f#b1]]).
- **The rates:** computed here by [[rates.f#RATES|`RATES`]] on the model passed in (`HD`, `HT`, and the substep's own composition), as [[mix.f#MIX|`MIX`]] does: the rates `HR1`…`HR13` and the branchings `HF1`, `HF2`, set to zero in shells with $\log T \le$ `TCUT(1)`.
- **What it calls:** `RATES`, `KEMCOM`, then either [[microdiff.f#MICRODIFF|`MICRODIFF`]] (when `LNEWDIF` is true) or [[grsett.f#GRSETT|`GRSETT`]] (the older Bahcall–Loeb settling).
- **Output:** `HCOMP`, updated in place.
- **Modules, other:** `NMLPAR_MOD` (the namelist parameters `LDIFY`, which this routine may switch off, `DT_GS`, `XMIN`, `YMIN`, `LNEWDIF`, `TCUT(1)` and `LEXCOM`: 15 species or 11), `MDPHY_MOD` (`DELM`), `SCRTCH_MOD` (`SDEL`, temporarily overwritten), `CONSTANTS_MOD`, `IOUNITS_MOD` (`ISHORT`), `DIMENSIONS_MOD` (`JSON`).

**The method.**
1. **Burning.** For each radiative shell above the cut $\log T >$ `TCUT(1)` (the loop stops at the first shell below it, assuming $T$ falls outward), `KEMCOM` is called for the shell alone; for each convection zone, for the whole zone at once, which also homogenizes it. The step is passed in years, `DDAGE = DELTS/CSECYR`.

    > **Question** ([[#L118-L130]]). **The burning loop exits at the first cool shell.** `GOTO 45` leaves both the shell loop and the zone loop, so any radiative zone listed after the first cool shell is skipped, even if it were hot (for example in a shell-burning star, if the zones were not ordered outward). Are `MRZONE` entries always ordered from the center out?

2. **Settling** (if `LDIFY`). It is skipped once the central hydrogen is below `XMIN` (and `LDIFY` is then switched off for good), if the star is fully convective, or if $Y <$ `YMIN` everywhere. It stops the run (exit status 1) if there is no surface convection zone. The outer point `JMAX` is the top of the last radiative zone; the comment says it is moved down to the first shell with $Y >$ `YMIN`, but the search moves only `J`, so `JMAX` stays the top of the last radiative zone (suspected bug 1). The settling time there is taken from Michaud et al. (1984):
   $$t_\mathrm{settle} = 4.348\times10^{21}\;\frac{f_M}{T^{3/2}}\ \text{yr},\qquad f_M = \frac{M_* - m(\texttt{JMAX})}{M_*},$$
   with $T$ in K at `JMAX` (the code multiplies by `CSECYR` to get `TSCALE` in seconds, the unit of `DELTS`), and the step is divided into `NSTEP` substeps of at most `DT_GS` $\times\,t_\mathrm{settle}$ (one more than `INT(DELTS/DTMAX)` unless `DELTS` is an exact multiple of `DTMAX`). The pressure gradient passed to the settling routine is
   $$\frac{d\ln P}{dr} = -\frac{G m \rho}{P r^2}\quad(\texttt{HQPR}).$$
   During the settling, `SDEL(2,·)` holds `DELM` and is restored afterwards.
3. **Renormalization.** Every abundance is clipped to $[0, 1]$; $Z$ (`HCOMP(3)`) is capped at $1 - X - X_3$, and $Y$ is set to $1 - X - Z - X_3$, where $X_3$ is ³He, the fourth species `HCOMP(4,·)` (as [[starin.f#STARIN|`STARIN`]] fills it).

**Changed since `rp_1`.** The two debug writes to unit 69 are commented out (settles former question 1); COMMON blocks to modules (the unused `/CTLIM/` dropped), `IMPLICIT NONE`.

**Changed since `a8a5950`.** The rates are computed by `RATES` on the model passed in, instead of copied from `HCOMPM` in `BURN_MOD` (removed since `a8a5950`), which held the rates `MIX` found on the previous Newton iterate's end-of-step structure, so that the midpoint substep from `MIDMOD` burned with end-of-step rates (this settles former question 3, since the copies are gone); the substep count tests `MOD(DELTS,DTMAX)` (this settles former question 1); the stop for no surface convection zone exits with status 1, the code for run-time errors (`KNOWN_ISSUES.md`, issue 38). The later questions are renumbered.

## Bugs, by priority

1. **(c)** **The outer point for the settling step is not moved down.** ([[#L156-L160]]; [[#L174-L180]]; [[#L191-L194]]) The comment says the outer boundary is the surface convection zone or "the first point where the helium abundance rises above" `YMIN`. Loop 140 finds that point as `J`, but `JMAX` is never set to it, so `FM` and `TSCALE`, and with them the number of settling substeps, are always taken at the top of the last radiative zone. Where $Y \le$ `YMIN` there, the step limit is set at a point the comment means to skip. Only with `LDIFY` (off by default); the settling itself does not use `JMAX`. Read from the code, not run. **A possible fix:**

    ```fortran
      150    CONTINUE
    C 11/09/26 KC via Claude
    C code changed to move the outer point down to the first shell with
    C Y > YMIN, as the comment above says.
             JMAX = J
             STOT=EXP(CLN*HSTOT)
    ```

2. **(c)** **The stop message names the wrong routine.** ([[#L163-L169]]) The stop for no surface convection zone prints "STOPPED IN SUBROUTINE MIX" (copied from `MIX`), though it stops in ROTMIX. Only with `LDIFY` (off by default). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to name ROTMIX in the stop message.
      911       FORMAT(1X,'NO SURFACE CZ - DIFFUSION NOT MEANINGFUL'/
         *             'STOPPED IN SUBROUTINE ROTMIX')
    ```
