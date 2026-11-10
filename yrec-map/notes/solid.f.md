## Explanation

**Purpose.** `SOLID` makes a range of shells, `JSTART` to `JEND`, rotate as a solid body while conserving their total angular momentum. Given each shell's angular momentum per unit mass, it returns the common rotation rate $\Omega$ and the shells' moments of inertia. Its comment adds that it also gives $r_0$ and $\eta_2$ (`R0`, `ETA2`), which [[fpft.f#FPFT|FPFT]] needs.

**How it fits.**
- **Inputs:** arguments only: the shells' masses (`HS2`, probably in grams, since the angular momentum is the sum of `HS2*HJM`), specific angular momenta `HJM`, the previous rates `OMEGA`, and the structure (`HD`, `HR`, `HS`), passed on to the shape routines.
- **Who calls it:** the rotation routines that impose solid-body rotation on a zone: [[checkj.f#CHECKJ|CHECKJ]], [[getrot.f#GETROT|GETROT]], [[midmod.f#MIDMOD|MIDMOD]], [[seculr.f#SECULR|SECULR]] and [[wczimp.f#WCZIMP|WCZIMP]] (for convection zones, by its name; WCZ, removed since `rp_1`, was another).
- **What it calls:** [[shape.f#SHAPE|SHAPE]] (the distortion of the shells, `ETA2` and `R0`) and [[momi.f#MOMI|MOMI]] (each shell's moment of inertia `HI` and `QIW`, which the comments call $dI/d\Omega$ but which is $\tfrac12\,\Omega\,dI/d\Omega$: [[#b2]]).
- **Outputs:** `OMEGA`, `HI`, `QIW`, `ETA2`, `R0` and an updated `HJM`, all through the arguments.
- **Modules:** `ERRMOM_MOD` (the tolerance `TOLERI`, $10^{-12}$, used only here and in [[checkj.f#CHECKJ|CHECKJ]]: CHECKJ saves it (`TOLER0 = TOLERI`), relaxes it to `MAX(DJOK*1.0D-2,TOLER0)` around its call to GETROT, and restores it); `DISK_MOD` (the age `SAGE`, shared with [[getw.f#GETW|GETW]], [[seculr.f#SECULR|SECULR]], [[mdot.f#MDOT|MDOT]] and others); `NMLPAR_MOD` (the disk-locking parameters: the locking time `TDISK`, the locked rate `PDISK` and the switch `LDISK`, namelist parameters read by [[parmin.f#PARMIN|PARMIN]]); `DIMENSIONS_MOD` (`JSON`).

**The method.** Let $m_j$ be `HS2(J)` and $j_j$ be `HJM(J)`. The target is the zone's total angular momentum,

$$J = \sum_{j=J_\mathrm{start}}^{J_\mathrm{end}} m_j\, j_j .$$

The first guess for $\Omega$ is the mean of the previous rates. With every shell at $\Omega$, `SHAPE` and `MOMI` give the moments of inertia $I_j(\Omega)$ and $I'_j$, taken as $dI_j/d\Omega$ (`QIW`, which is in fact $\tfrac12\,\Omega\,dI_j/d\Omega$; [[#b2]]). With $I = \sum I_j$ (`CZI`) and $I' = \sum I'_j$ (`CZQIW`), a Newton step solves $\Omega\, I(\Omega) = J$:

$$\Delta\Omega = \frac{J - \Omega I}{I + \Omega I'} ,$$

repeated until $|J - \Omega I|/J \le$ `TOLERI`, or 20 times ([[#L68-L95]]). Finally each shell's specific angular momentum is reset to $j_j = I_j\,\Omega / m_j$ ([[#L97-L99]]).

> **Question** ([[#L88-L95]]). **No warning after 20 steps.** When the Newton iteration has not converged after 20 steps, `SOLID` keeps the last guess silently. Should it report this?

**Disk locking.** For the surface convection zone (`JEND = M`, more than one shell), when `LDISK` is set and the age `SAGE` is at most `TDISK`, $\Omega$ is fixed to `PDISK` with no iteration, and the angular momentum follows from it ("MHP 9/94," [[#L58-L67]]).

**`PDISK` is an angular rate.** Under disk locking, `WGUESS = PDISK` ([[#L66]]), which is used as $\Omega$, and `NMLPAR_MOD`'s initial value `7.2722D-6` ([[nmlpar_mod.f#L210]]) is $2\pi/(10\ \mathrm{d})$ in rad/s, a rate for a period of 10 days. The comment calls it the "PERIOD AT WHICH LOCKING IS SET" ([[#L29-L30]]), and the Physics namelist page gives the unit rad/s but calls it a "Disk rotation period," so both could say "rate."

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) (Initializing rotation): `LDISK` enforces disk locking until the age `TDISK` (Gyr; $10^{-4}$, i.e. $10^5$ yr, is the deuterium birthline, and $10^{-4}$–$10^{-2}$ the recommended range), at the disk's rate `PDISK`. The documentation calls `PDISK` the "disk rotation period (rad/s)": it is an angular velocity, used as such here; the default 7.2722D-6 is a 10-day period, while the documentation suggests 8 days (9.0902D-6), the median for disked solar-mass stars in star-forming regions.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/ERRMOM/` to `ERRMOM_MOD`; `/DISK/` split between `DISK_MOD` (`SAGE`) and `NMLPAR_MOD` (`TDISK`, `PDISK`, `LDISK`); the unused `/LUOUT/` dropped), the array size `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`. One caller, WCZ, was removed with its file.

**Changed since `a8a5950`.** The file is unchanged, but [[errmom_mod.f#ERRMOM_MOD|`ERRMOM_MOD`]] now gives `TOLERI` the value $10^{-12}$, so the Newton loop stops once $|J - \Omega I|/J \le 10^{-12}$; this settles former question 1, and former questions 2–5 are now 1–4.

## Bugs, by priority

1. **(never occurred)** **A zone without angular momentum divides by zero.** ([[#L49-L57]]; [[#L86-L88]]) The convergence test `DABS(DELJ/CZJ)` divides by the zone's total angular momentum `CZJ`, which is zero for shells that do not rotate (`HJM` = 0). What follows: In the development build, which traps invalid operations and division by zero (`-ffpe-trap=invalid,zero,overflow` in `src/Makefile`), the run stops; in the release build the test gives `NaN` (when `DELJ` is 0 too, and the test is false) or infinity (the iteration then drives $\Omega$ towards 0 for its 20 steps). Only with rotation (`LROT`, off by default), for a zone with $j = 0$.

    **A possible fix:**

    ```diff
    --- a/src/solid.f
    +++ b/src/solid.f
    @@ -85,7 +85,10 @@
     C  ENOUGH.  IF NOT, CALCULATE DELTA OMEGA AND TRY AGAIN WITH A NEW WGUES
           DELJ = CZJ - CZJNEW
           IF(LOCK)GOTO 45
    -      IF(DABS(DELJ/CZJ).GT.TOLERI) THEN
    +C 11/09/26 KC via Claude
    +C code changed to test the angular momentum without dividing by CZJ,
    +C which is zero for a zone without rotation.
    +      IF(DABS(DELJ).GT.TOLERI*DABS(CZJ)) THEN
              IF(ICOUNT.LT.20) THEN
                 ICOUNT = ICOUNT + 1
                 DELW = DELJ/(CZI + WGUESS*CZQIW)
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The test ran in all five rotating test cases, from about 6.1 to 44.6 million times, and the zone's angular momentum was never zero, so no run reached the division. A rotating run with a zone that does not rotate would: an initial rotation of zero (`LWNEW` with `WNEW` = 0), or a start model without rotation; none of YREC's cases does this. Intent: none found.

2. **(harmless in the runs)** **`QIW` in the Newton step.** ([[#L91]]; [[momi.f#L84-L86]]; [[intmom.f#L28-L31]]) The step `DELW = DELJ/(CZI + WGUESS*CZQIW)` treats `QIW` as $dI/d\Omega$, as the comments say ([[#L78]]; [[momi.f#L50]]), but MOMI returns $A\,dI/dA = \tfrac12\,\Omega\,dI/d\Omega$ (since $A \propto \Omega^2$), so the denominator adds a term with units of $I$ s$^{-1}$; Newton's step for $\Omega I(\Omega) = J$ needs $I + \Omega\,dI/d\Omega = I + 2\,$`QIW`. What follows: The result is unchanged when the loop converges, since the test is on $J$; the missing term is of order $A$ relative to $I$, so the iteration, in effect a fixed-point one, still converges almost as fast as Newton's (its error shrinks by about $2\,$`QIW`$/I \approx 0.18(\eta_2+5)A$ per step, from INTMOM's leading term) for any $A$ in the method's range, but may need more of its 20 steps for a fast rotator. Only with rotation (`LROT`, off by default) and `WALPCZ` = 0 (the default; otherwise MOMI sets `QIW` to 0).

    **A possible fix** (or INTMOM could return $dI/d\Omega$, `QIWM`$\cdot 2/\Omega$):

    ```diff
    --- a/src/solid.f
    +++ b/src/solid.f
    @@ -88,7 +88,10 @@
           IF(DABS(DELJ/CZJ).GT.TOLERI) THEN
              IF(ICOUNT.LT.20) THEN
                 ICOUNT = ICOUNT + 1
    -            DELW = DELJ/(CZI + WGUESS*CZQIW)
    +C 11/09/26 KC via Claude
    +C code changed to use 2*QIW in the Newton step, since MOMI returns
    +C QIW = A*DI/DA = 0.5*OMEGA*DI/D(OMEGA).
    +            DELW = DELJ/(CZI + 2.0D0*CZQIW)
                 WGUESS = WGUESS + DELW
                 GOTO 20
              ENDIF
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The Newton step ran in all five rotating test cases (about 4.1 to 19.7 million times, at most 9 steps per solve). The missing term exceeded $10^{-3}\,I$ ($2\,$`QIW`$/I$ up to 0.059) in the three faster rotators, 2.1 to 7.2 million times; never in `testsuite/Test_solarGS98_difrotmixper18p4d1p0`, nor in `testsuite/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2`, which sets `WALPCZ` = $-2$ (`QIW` = 0). With the fix, both runs stay within the noise: in `testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS` $\log L$ moves by up to 0.00017 dex, against 0.00014 for a null change (nearly every opacity, all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$, times $1 + 10^{-10}$, on the same case), and in `testsuite/Test_m2p0_feh+0p0_vzams150_IES1_TAMS` every difference equals the null change's. As expected, the results do not change; the number of iterations was not counted.

### SOLID

Solid-body rotation of shells `JSTART`–`JEND` at fixed total angular momentum, by Newton iteration on $\Omega I(\Omega) = J$; or, under disk locking, at the fixed rate `PDISK`.
