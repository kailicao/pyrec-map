## Explanation

**Purpose.** Nuclear burning and gravitational settling for one step of the rotational-mixing loop. Its header comment lists the steps: (1) use [[kemcom.f#KEMCOM|`KEMCOM`]] to solve implicitly for the abundances in radiative regions, shell by shell; (2) solve for the burning in each convection zone as a whole. It then applies the settling of helium and renormalizes the composition.

**How it fits.**
- **Who calls it:** [[midmod.f#MIDMOD|`MIDMOD`]] (with the temperatures at the current time, `HTM`, "for thermodynamic consistency", MHP 6/00) and [[bursmix.f#BURSMIX|`BURSMIX`]], in their loops of substeps.
- **Inputs:** the step `DELTS` (s), the composition `HCOMP(15, ·)`, shell masses `HS2`, temperatures `HT` ($\log T$), and the zone lists `MRZONE` (radiative) and `MXZONE` (convective); for the settling, `HD`, `HS`, `HR`, `HP`, `HS1`, `HSTOT` and the convection flags `LC`.
- **The rates:** read from `/BURN/` (`HCOMPM(1..15, ·)`), where [[mix.f#MIX|`MIX`]] stored the output of [[rates.f#RATES|`RATES`]]: `HCOMPM(1..13)` are the rates `HR1`…`HR13`, `HCOMPM(14)` and `(15)` the branchings `HF1`, `HF2`.
- **What it calls:** `KEMCOM`, then either [[microdiff.f#MICRODIFF|`MICRODIFF`]] (when `LNEWDIF` is true, `/GRAVS4/`) or [[grsett.f#GRSETT|`GRSETT`]] (the older Bahcall–Loeb settling).
- **Output:** `HCOMP`, updated in place.
- **COMMON, other:** `/GRAVST/` (`LDIFY`, which this routine may switch off), `/GRAVS2/` (`DT_GS`, `XMIN`, `YMIN`), `/CTLIM/` (`TCUT(1)`), `/FLAG/` (`LEXCOM`: 15 species or 11), `/MDPHY/` (`DELM`), `/SCRTCH/` (`SDEL`, temporarily overwritten), `/CONST*/`.

**The method.**
1. **Burning.** For each radiative shell above the cut $\log T >$ `TCUT(1)` (the loop stops at the first shell below it, assuming $T$ falls outward), `KEMCOM` is called for the shell alone; for each convection zone, for the whole zone at once, which also homogenizes it. The step is passed in years, `DDAGE = DELTS/CSECYR`.
2. **Settling** (if `LDIFY`). It is skipped once the central hydrogen is below `XMIN` (and `LDIFY` is then switched off for good), if the star is fully convective, or if $Y <$ `YMIN` everywhere. It stops the run if there is no surface convection zone. The outer point `JMAX` is the top of the last radiative zone, moved down to the first shell with $Y >$ `YMIN`. The settling time there is taken from Michaud et al. (1984):
   $$t_\mathrm{settle} = 4.348\times10^{21}\;\frac{f_M}{T^{3/2}}\ \text{yr},\qquad f_M = \frac{M_* - m(\texttt{JMAX})}{M_*},$$
   with $T$ in K at `JMAX` (the code multiplies by `CSECYR` to get `TSCALE` in seconds, the unit of `DELTS`), and the step is divided into `NSTEP` substeps of at most `DT_GS` $\times\,t_\mathrm{settle}$. The pressure gradient passed to the settling routine is
   $$\frac{d\ln P}{dr} = -\frac{G m \rho}{P r^2}\quad(\texttt{HQPR}).$$
   During the settling, `SDEL(2,·)` holds `DELM` and is restored afterwards.
3. **Renormalization.** Every abundance is clipped to $[0, 1]$; $Z$ (`HCOMP(3)`) is capped at $1 - X - X_4$, and $Y$ is set to $1 - X - Z - X_4$, where $X_4$ is the fourth species, He3 (as [[starin.f#STARIN|`STARIN`]] fills it).

**KC's changes.** The unused argument `ITLVL` was removed (KC 2025-05-31), with the calls in `MIDMOD` and `BURSMIX`; the calls to `KEMCOM` drop `HR9`, `HR13` and `ITLVL` to match its new signature (KC 2025-05-31).

## Questions for the experts

1. **Unconditional debug output.** Two `write(69,*)` statements print `JMAX`, `FM`, `TSCALE`, `DTMAX`, `DELTS` and `NSTEP` to unit 69 at every call with settling. No routine opens unit 69, so this writes a file named by the compiler's default (for example `fort.69`). Leftover debugging?
2. **`MOD` with its arguments reversed.** `NSTEP = INT(DELTS/DTMAX)`, then one more substep `IF(MOD(DTMAX,DELTS).NE.0)`. To test whether `DELTS` is a multiple of `DTMAX`, it would be `MOD(DELTS,DTMAX)`. As written, whenever `DTMAX < DELTS` the test is always true, so one extra substep is always added. The same line is in [[mix.f#MIX|`MIX`]]. Intended?
3. **Message names the wrong routine.** The stop for "NO SURFACE CZ" says "STOPPED IN SUBROUTINE MIX" (copied from `MIX`).
4. **`HR9`, `HR13`, `HF2` are copied but not used.** The copies from `HCOMPM` remain after KC's change to the `KEMCOM` call. They could go.
5. **The burning loop exits at the first cool shell.** `GOTO 45` leaves both the shell loop and the zone loop, so any radiative zone listed after the first cool shell is skipped, even if it were hot (for example in a shell-burning star, if the zones were not ordered outward). Are `MRZONE` entries always ordered from the center out?
