## Explanation

**Purpose.** `GETOPAC` is YREC's opacity routine: for a given $\rho$, $T$, $X$, $Z$ it combines the low-temperature (molecular) table and the interior table, ramps between them, handles metal-rich helium-burning cores, and adds conductive opacity. It returns $\kappa$ and its logarithmic derivatives.

**How it fits.**
- **Who calls it:** seven routines: [[coefft.f#COEFFT|COEFFT]], [[envint.f#ENVINT|ENVINT]], [[physic.f#PHYSIC|PHYSIC]], [[qatm.f#QATM|QATM]], [[qenv.f#QENV|QENV]], [[sconvec.f#SCONVEC|SCONVEC]] and [[starin.f#STARIN|STARIN]].
- **Inputs:** `DL`, `TL` ($\log\rho$, $\log T$), `X`, `Z`, and `FXION` (ionization fractions, passed on to the conductive opacity).

    > **Question** ([[#L192]]; [[condopacpint.f#L32-L40]]). **`FXION` used only by conduction.** Fine, but its meaning differs by equation of state (`EQSAHA` versus SCV); does `CONDOPACPINT` depend on which one supplied it?

- **What it calls:** the low-temperature table [[getalex06.f#GETALEX06|GETALEX06]] (the low-temperature tables of Ferguson et al. 2005, the code's `ALEX06`); the interior table [[getopal95.f#GETOPAL95|GETOPAL95]] (OPAL 1995); [[gtpurz.f#GTPURZ|GTPURZ]] (pure-metal table); and [[condopacpint.f#CONDOPACPINT|CONDOPACPINT]] (Potekhin conductive opacity).
- **Outputs:** `O` ($\kappa$), `OL` ($\log\kappa$), `QOD` $=\partial\log\kappa/\partial\log\rho$, `QOT` $=\partial\log\kappa/\partial\log T$.
- **Modules:** [[nmlpar_mod.f|NMLPAR_MOD]] (the namelist switches `LALEX06`, `LOPAL95`, `LPUREZ`, `LcondOpacP`, the ramp limits `TMOLMIN`, `TMOLMAX`, and the tolerance `OPTOL`, read by [[parmin.f#PARMIN|PARMIN]]); [[newopac_mod.f|NEWOPAC_MOD]] (`L2Z`, set by [[setupopac.f#SETUPOPAC|SETUPOPAC]] from `LZRAMP` or `LDIFZ`); [[comp_mod.f|COMP_MOD]] (`ZENV`); [[iounits_mod.f|IOUNITS_MOD]] (`ISHORT`, for the error messages).

**The method.**
1. **Molecular opacity** for $\log T \le$ `TMOLMAX`, from the Ferguson et al. (2005) tables (`LALEX06`); if they are not switched on, the run stops ("NO MOLECULAR OPACITY TABLE CHOSEN").
2. **Interior opacity**, unless $\log T <$ `TMOLMIN` (where the molecular value is used alone):
   - for $Z > 0.1$ and $\log T > 7.0$ (helium-burning cores), linear interpolation in $Z$ between OPAL 1995 at $Z_\mathrm{tab} = 0.1$ and the pure-metal table at $Z = 1$: $\log\kappa = \log\kappa_{Z=1} + (Z-1)\,\dfrac{\log\kappa_\mathrm{tab} - \log\kappa_{Z=1}}{Z_\mathrm{tab} - 1}$, and the derivatives likewise; the run stops if no pure-$Z$ table is loaded (`LPUREZ`) or if OPAL 1995 is not switched on;
   - the run stops if $Z > 0.12$ below that temperature, or if $Z$ differs from the envelope's `ZENV` beyond `OPTOL` with a single-$Z$ table (neither `L2Z` nor OPAL 1995, which interpolates in $Z$ itself; bug 2 below);
   - otherwise OPAL 1995; if it is not switched on, the run stops ("NO OPACITY TABLE CHOSEN").
3. **Ramp** for `TMOLMIN` ≤ $\log T \le$ `TMOLMAX`: with $w = (\log T - \mathrm{TMOLMIN})/(\mathrm{TMOLMAX} - \mathrm{TMOLMIN})$, $\kappa = w\,\kappa_\mathrm{int} + (1-w)\,\kappa_\mathrm{mol}$, and the derivatives likewise. The ramp is linear in $\kappa$, while the derivatives (of $\log\kappa$) are averaged with the same weights, so they are not exactly those of the ramped $\kappa$: The weights should be $w\,\kappa_\mathrm{int}/\kappa$ and $(1-w)\,\kappa_\mathrm{mol}/\kappa$, and the term $(\partial w/\partial\log T)(\kappa_\mathrm{int} - \kappa_\mathrm{mol})/\kappa$ is dropped. This is known, and affects the Jacobian only (settled from YREC's notes, Nov 9, 2026: `KNOWN_ISSUES.md`, issue 40, "Opacity ramp derivatives"; [[#L177-L181]]).
4. **Conduction.** Potekhin's opacity if `LcondOpacP` is set and it succeeds; otherwise, for $\log T \ge 4.2$ and $\log\rho \ge 2\log T - 13$, the fit to Hubbard & Lampe (1969) as coded (the code names no source for the fit; see the question below):
$$\log\kappa_c = \log(1 - 0.6X) - 14.6196 - (3.5853 + 0.1386\log\rho)\log\rho + (5.1324 - 0.3219\log T)\log T + 0.3901\log\rho\log T.$$
The two cuts leave out cool gas and gas of low density for its temperature ($\rho < 10^{-13}T^2$). The derivatives `QODC`, `QOTC` it receives from Potekhin's fit carry [[condopacpint.f#b1|CONDOPACPINT's suspected bugs 1 and 2]], and its extrapolation below $\log\rho = -6$ bugs 3 and 4.

    > **Question** ([[#L200-L211]]). **The conductive fit's source.** The fallback fit to Hubbard & Lampe (1969) has no reference in the code. Whose fit is it, and what range of $\rho$, $T$ was it made for? Are the cuts ($\log T \ge 4.2$, $\rho \ge 10^{-13}T^2$) meant to leave out gas where the electrons are far from degenerate and conduction is negligible next to radiation?

    > **Question** ([[#L190-L199]]). **Conduction where no table applies.** Below $\log T = 4.2$ or at low density the routine returns without conduction, which is fine; but when Potekhin is enabled and fails, Hubbard–Lampe is used without a message. Should the fallback be reported?

5. **Combination:** $1/\kappa = 1/\kappa_\mathrm{rad} + 1/\kappa_c$, and
$$\frac{\partial\log\kappa}{\partial\log\rho} = \frac{\kappa_c\,\partial\log\kappa_\mathrm{rad} + \kappa_\mathrm{rad}\,\partial\log\kappa_c}{\kappa_\mathrm{rad} + \kappa_c},$$
and the same in $\log T$.

**The tables' mixtures.** Each table is computed for one heavy-element mixture, named in its file (`FLIV95`, `FALEX06`): in the test suite `GS98.OP17` (OP, Grevesse & Sauval 1998, the YREC paper's base mixture), `GN93hz`, `AAG2021zx0.0187.tab` or `Magg22_met_zx0.0226.tab`, and `alexmol06gs98.tab` for the molecular table. The run's `XENV`, `ZENV` (and the equation of state's mixture) should match the tables', since the code only interpolates in $X$ and $Z$; the documentation (Control Options) recommends tying the CNO abundances "to preset mixtures used in opacity tables." The pure-metal table (`FPUREZ`) is `input/opacity/lanl/PURECO.DBGLAOL`, the table the User Guide names for helium burning ("Helium burning uses a different type of atomic opacity table"); so in a helium-burning core the step-2 interpolation runs from OPAL at $Z = 0.1$ to this table at $Z = 1$ (what mixture it holds is the question below).

> **Question** ([[#L109-L138]]). **OPAL's C/O-rich tables.** The YREC paper (§2.3.2) says OPAL's tables for carbon- and oxygen-rich mixtures (Iglesias & Rogers 1993) are used in helium-burning regions; the code instead interpolates in $Z$ between OPAL at $Z = 0.1$ and the table `PURECO.DBGLAOL` (step 2), which the tables' README describes as interpolating "between helium and a c/o mixture" (`input/opacity/atomic/README`, line 1): With what C/O ratio, and how does it interpolate between helium and C/O? Is the paper describing the older scheme, or is the C/O table meant to stand for it? A reader would ask how large the error in the core opacity of horizontal-branch and AGB models is when the C/O ratio of the core differs from the table's, and when $0.1 < Z < 1$ is reached by a straight line in $\log\kappa$.

**From YREC's documentation.** [Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html) (Input files) and [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) (Opacity options): `LALEX06` uses the molecular opacities of Ferguson et al. (2005) and `LOPAL95` the atomic opacities in OP/OPAL format (both recommended); `LPUREZ` adds the pure Y/Z table (`FPUREZ`); `LCONDOPACP` uses the updated conductive opacities. Below $\log T$ = `TMOLMIN` (default 4.0) only the molecular opacities are used, above `TMOLMAX` (4.1) only the atomic ones, with a ramp between. The code builds a 2D table for the surface abundances, useful in outer convection zones and the envelope, and switches to the full 3D/4D interpolation when $X$ or $Z$ differ from it by more than `OPTOL` (1.0D-8). `LOPAL95` has no default in `NMLPAR_MOD` (nor has `ZOPAL951`); the User Guide asks the user to set `LOPAL95 = .TRUE.` with the table's path; a namelist that omits it leaves it to the compiler (usually false), and the run then stops at a trap with status 3 (settled from the code and the documentation, Nov 9, 2026: `docs/source/userguide.md`, line 34; [[nmlpar_mod.f#L243]]; [[#L126-L130]], [[#L162-L166]]).

**Changed since `rp_1`.** The Alexander 1995, Kurucz 1990, OPAL 1992 and LAOL 1989 tables were removed, so OPAL 1995 is the only interior table and the Ferguson et al. (2005) tables (`ALEX06`) the only molecular ones; their two-$Z$ interpolations went with them, and so did the Kurucz failure path (the alternate return to label 100). New traps stop the run when no molecular table is chosen below `TMOLMAX`, and when no interior table is chosen in the helium-burning branch; this settles question 1 of `rp_1` (`ZIT` undefined in that branch), which is removed. The helium-burning branch now starts at $\log T > 7.0$ instead of 7.7 ("JCZ 211125," for semiconvection and overshoot horizontal-branch models), and the message for $Z > 0.12$ says $10^7$ K. COMMON blocks became modules (`NEWOPAC`, `NWLAOL` and `MISCOPAC` to `NMLPAR_MOD` and `NEWOPAC_MOD`; `OPTAB` removed), `IMPLICIT NONE`.

**Changed since `a8a5950`.** The stops now exit with a nonzero status instead of a bare `STOP` (`KNOWN_ISSUES.md`, issue 38): status 3, the code for input errors, when no molecular or interior table is chosen (three traps), and status 1, the code for run-time errors, when a helium-burning core needs the missing pure-$Z$ table and when $Z > 0.12$ or $Z$ leaves a single-$Z$ table.

## Bugs, by priority

1. **(not reached)** **A stale temperature in the pure-$Z$ trap's message.** ([[#L104-L114]]) Since the helium-burning branch starts at $\log T > 7.0$ ("JCZ 211125," line 107), the message for a missing pure-$Z$ table still says "Z>0.10 T > 5 X 10^7 K," and the comment above the test still speaks of "50 million K." A run that stops here with $10^7 < T < 5\times10^7$ K reports a temperature it has not reached. The trap fires only when `LPUREZ` is off (its default, [[nmlpar_mod.f#L244]]) and a core with $Z > 0.1$ passes $\log T = 7.0$.

    **A possible fix:**

    ```diff
    --- a/src/getopac.f
    +++ b/src/getopac.f
    @@ -108,7 +108,9 @@
     C     semiconvection+overshoot HB models, which can reach lower core temperatures
           IF((Z .GT. 0.1D0) .AND. (TL.GT.7.0D0)) THEN
              IF(.NOT.LPUREZ) THEN
    -            WRITE(ISHORT, *)' ERROR: Z>0.10 T > 5 X 10^7 K',
    +C 11/09/26 KC via Claude
    +C code changed to give the branch's threshold of 10^7 K in the message.
    +            WRITE(ISHORT, *)' ERROR: Z>0.10 T > 10^7 K',
          *        ' NEED PURE Z TABLE TO CONTINUE. Z,LOG T=',Z, TL
     C 10/30/26 MHP via Claude: bare STOP -> STOP 1, the run-time error code (issue 38).
                   STOP 1
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): not reached in any of 34 runs, 26 of YREC's cases (from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning) and 8 made-up ones (each one of YREC's cases with a few settings changed), of which one stopped in its first second. The trap needs `LPUREZ` off, and every one of YREC's cases sets it on; what would reach it: `LPUREZ` off, with a helium-burning core whose $Z$ passes 0.1 above $\log T = 7.0$. The fix only changes a message, so it was not run. Intent: The comment at line 142 shows the other message was updated with the threshold ("JCZ 211125 changed to 10^7 K in message"), but not this one.

2. **(not reached)** **The single-table test now only changes the stop.** ([[#L140-L141]], [[#L162-L166]]) The test `ABS(Z-ZENV) .GT. OPTOL .AND. .NOT.L2Z .AND. .NOT.LOPAL95` can be true only when OPAL 1995 is off, the one interior table left. Then a run whose $Z$ differs from `ZENV` stops with "OUTSIDE SINGLE TABLE USED" and status 1 (a run-time error), while the same run with $Z$ = `ZENV` stops at the final trap with "NO OPACITY TABLE CHOSEN" and status 3 (an input error), which is the true cause in both. `L2Z` is read nowhere else (set in [[setupopac.f#L64]]). Taken only when `LOPAL95` is off.

    **A possible fix:**

    ```diff
    --- a/src/getopac.f
    +++ b/src/getopac.f
    @@ -137,12 +137,13 @@
            SLOPE = (QOT-QOTZ)/(ZIT-1.0D0)
            QOT = QOTZ + (Z-1.0D0)*SLOPE
     C      ELSE
    -      ELSE IF((Z.GT.0.12D0) .OR. ((ABS(Z-ZENV) .GT. OPTOL)
    -     *      .AND..NOT.L2Z .AND. .NOT.LOPAL95))THEN
    +C 11/09/26 KC via Claude
    +C code changed to drop the single-table test, which can hold only when
    +C no interior table is chosen; the final trap then stops the run.
    +      ELSE IF(Z.GT.0.12D0)THEN
     C     JCZ 211125 changed to 10^7 K in message to reflect above change in logic.
              WRITE(ISHORT,*)' Z>0.12 T < 10^7 K',
    -     *   ' OUTSIDE OPAL OPACITY TABLE RANGE OR Z',
    -     *   ' OUTSIDE SINGLE TABLE USED.Z,ZENV,LOG T=',Z,ZENV,TL
    +     *   ' OUTSIDE OPAL OPACITY TABLE RANGE.Z,ZENV,LOG T=',Z,ZENV,TL
     C 10/30/26 MHP via Claude: bare STOP -> STOP 1, the run-time error code (issue 38).
              STOP 1
     C
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): not reached in any of the 34 runs; every one of YREC's cases sets `LOPAL95` on. What would reach it: `LOPAL95` off, which stops the run at the first interior point either way. The fix only changes which stop fires, so it was not run. Intent: none found.

### GETOPAC

Ramps and combines the molecular, interior, pure-metal and conductive opacities (method above).
