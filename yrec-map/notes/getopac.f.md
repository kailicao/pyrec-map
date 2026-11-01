## Explanation

**Purpose.** `GETOPAC` is YREC's opacity routine: for a given $\rho$, $T$, $X$, $Z$ it combines the low-temperature (molecular) table and the interior table, ramps between them, handles metal-rich helium-burning cores, and adds conductive opacity. It returns $\kappa$ and its logarithmic derivatives.

**How it fits.**
- **Who calls it:** seven routines: [[coefft.f#COEFFT|COEFFT]], [[envint.f#ENVINT|ENVINT]], [[physic.f#PHYSIC|PHYSIC]], [[qatm.f#QATM|QATM]], [[qenv.f#QENV|QENV]], [[sconvec.f#SCONVEC|SCONVEC]] and [[starin.f#STARIN|STARIN]].
- **Inputs:** `DL`, `TL` ($\log\rho$, $\log T$), `X`, `Z`, and `FXION` (ionization fractions, passed on to the conductive opacity).
- **What it calls:** the low-temperature table [[getalex06.f#GETALEX06|GETALEX06]] (the low-temperature tables of Ferguson et al. 2005, the code's `ALEX06`); the interior table [[getopal95.f#GETOPAL95|GETOPAL95]] (OPAL 1995); [[gtpurz.f#GTPURZ|GTPURZ]] (pure-metal table); and [[condopacpint.f#CONDOPACPINT|CONDOPACPINT]] (Potekhin conductive opacity).
- **Outputs:** `O` ($\kappa$), `OL` ($\log\kappa$), `QOD` $=\partial\log\kappa/\partial\log\rho$, `QOT` $=\partial\log\kappa/\partial\log T$.
- **Modules:** [[nmlpar_mod.f|NMLPAR_MOD]] (the namelist switches `LALEX06`, `LOPAL95`, `LPUREZ`, `LcondOpacP`, the ramp limits `TMOLMIN`, `TMOLMAX`, and the tolerance `OPTOL`, read by [[parmin.f#PARMIN|PARMIN]]); [[newopac_mod.f|NEWOPAC_MOD]] (`L2Z`, set by [[setupopac.f#SETUPOPAC|SETUPOPAC]] from `LZRAMP` or `LDIFZ`); [[comp_mod.f|COMP_MOD]] (`ZENV`); [[iounits_mod.f|IOUNITS_MOD]] (`ISHORT`, for the error messages).

**The method.**
1. **Molecular opacity** for $\log T \le$ `TMOLMAX`, from the Ferguson et al. (2005) tables (`LALEX06`); if they are not switched on, the run stops ("NO MOLECULAR OPACITY TABLE CHOSEN").
2. **Interior opacity**, unless $\log T <$ `TMOLMIN` (where the molecular value is used alone):
   - for $Z > 0.1$ and $\log T > 7.0$ (helium-burning cores), linear interpolation in $Z$ between OPAL 1995 at $Z_\mathrm{tab} = 0.1$ and the pure-metal table at $Z = 1$: $\log\kappa = \log\kappa_{Z=1} + (Z-1)\,\dfrac{\log\kappa_\mathrm{tab} - \log\kappa_{Z=1}}{Z_\mathrm{tab} - 1}$, and the derivatives likewise; the run stops if no pure-$Z$ table is loaded (`LPUREZ`) or if OPAL 1995 is not switched on;
   - the run stops if $Z > 0.12$ below that temperature, or if $Z$ differs from the envelope's `ZENV` beyond `OPTOL` with a single-$Z$ table (neither `L2Z` nor OPAL 1995, which interpolates in $Z$ itself);
   - otherwise OPAL 1995; if it is not switched on, the run stops ("NO OPACITY TABLE CHOSEN").
3. **Ramp** for `TMOLMIN` ≤ $\log T \le$ `TMOLMAX`: with $w = (\log T - \mathrm{TMOLMIN})/(\mathrm{TMOLMAX} - \mathrm{TMOLMIN})$, $\kappa = w\,\kappa_\mathrm{int} + (1-w)\,\kappa_\mathrm{mol}$, and the derivatives likewise.
4. **Conduction.** Potekhin's opacity if `LcondOpacP` is set and it succeeds; otherwise, for $\log T \ge 4.2$ and $\log\rho \ge 2\log T - 13$, the fit to Hubbard & Lampe (1969) as coded (the code names no source for the fit; question 7):
$$\log\kappa_c = \log(1 - 0.6X) - 14.6196 - (3.5853 + 0.1386\log\rho)\log\rho + (5.1324 - 0.3219\log T)\log T + 0.3901\log\rho\log T.$$
The two cuts leave out cool gas and gas of low density for its temperature ($\rho < 10^{-13}T^2$); why there is question 7.
5. **Combination:** $1/\kappa = 1/\kappa_\mathrm{rad} + 1/\kappa_c$, and
$$\frac{\partial\log\kappa}{\partial\log\rho} = \frac{\kappa_c\,\partial\log\kappa_\mathrm{rad} + \kappa_\mathrm{rad}\,\partial\log\kappa_c}{\kappa_\mathrm{rad} + \kappa_c},$$
and the same in $\log T$.

**The tables' mixtures.** Each table is computed for one heavy-element mixture, named in its file (`FLIV95`, `FALEX06`): in the test suite `GS98.OP17` (OP, Grevesse & Sauval 1998, the YREC paper's base mixture), `GN93hz`, `AAG2021zx0.0187.tab` or `Magg22_met_zx0.0226.tab`, and `alexmol06gs98.tab` for the molecular table. The run's `XENV`, `ZENV` (and the equation of state's mixture) should match the tables', since the code only interpolates in $X$ and $Z$; the documentation (Control Options) recommends tying the CNO abundances "to preset mixtures used in opacity tables". The pure-metal table (`FPUREZ`) is `input/opacity/lanl/PURECO.DBGLAOL`, the table the User Guide names for helium burning ("Helium burning uses a different type of atomic opacity table"); so in a helium-burning core the step-2 interpolation runs from OPAL at $Z = 0.1$ to this table at $Z = 1$ (what mixture it holds is question 8).

**From YREC's documentation.** [Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html) (Input files) and [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) (Opacity options): `LALEX06` uses the molecular opacities of Ferguson et al. (2005) and `LOPAL95` the atomic opacities in OP/OPAL format (both recommended); `LPUREZ` adds the pure Y/Z table (`FPUREZ`); `LCONDOPACP` uses the updated conductive opacities. Below $\log T$ = `TMOLMIN` (default 4.0) only the molecular opacities are used, above `TMOLMAX` (4.1) only the atomic ones, with a ramp between. The code builds a 2D table for the surface abundances, useful in outer convection zones and the envelope, and switches to the full 3D/4D interpolation when $X$ or $Z$ differ from it by more than `OPTOL` (1.0D-8).

**Changed since `rp_1`.** The Alexander 1995, Kurucz 1990, OPAL 1992 and LAOL 1989 tables were removed, so OPAL 1995 is the only interior table and the Ferguson et al. (2005) tables (`ALEX06`) the only molecular ones; their two-$Z$ interpolations went with them, and so did the Kurucz failure path (the alternate return to label 100). New traps stop the run when no molecular table is chosen below `TMOLMAX`, and when no interior table is chosen in the helium-burning branch; this settles question 1 of `rp_1` (`ZIT` undefined in that branch), which is removed. The helium-burning branch now starts at $\log T > 7.0$ instead of 7.7 ("JCZ 211125", for semiconvection and overshoot horizontal-branch models), and the message for $Z > 0.12$ says $10^7$ K. COMMON blocks became modules (`NEWOPAC`, `NWLAOL` and `MISCOPAC` to `NMLPAR_MOD` and `NEWOPAC_MOD`; `OPTAB` removed), `IMPLICIT NONE`.

## Questions for the experts

1. **Ramp in $\kappa$, not $\log\kappa$.** The ramp is linear in $\kappa$, while the derivatives (which are of $\log\kappa$) are averaged with the same weights. The derivatives are then not exactly those of the ramped $\kappa$. Acceptable?
2. **Conduction where no table applies.** Below $\log T = 4.2$ or at low density the routine returns without conduction, which is fine; but when Potekhin is enabled and fails, Hubbard–Lampe is used without a message. Should the fallback be reported?
3. **`FXION` used only by conduction.** Fine, but its meaning differs by equation of state (`EQSAHA` versus SCV); does `CONDOPACPINT` depend on which one supplied it?
4. **A stale message.** With the threshold now at $\log T > 7.0$, the pure-$Z$ error still says "Z>0.10 T > 5 X 10^7 K", and the comment above the test still speaks of "50 million K". Update both to $10^7$ K?
5. **`L2Z` and `OPTOL` with OPAL 1995 only.** The single-table test `ABS(Z-ZENV) .GT. OPTOL .AND. .NOT.L2Z .AND. .NOT.LOPAL95` can now be true only when OPAL 1995 is off, and then the run stops at the final trap anyway. Is the test, and `L2Z` here, still needed?
6. **`LOPAL95` has no default.** It is declared in `NMLPAR_MOD` without an initial value (as are `ZOPAL951` and the store switches `LSTATM`, `LSTENV`, `LSTMOD`, `LSTPHYS`, `LSTROT`), so a namelist that omits it leaves it to the compiler (usually false). The documentation recommends it on. Should it get an explicit default?
7. **The conductive fit's source.** The fallback fit to Hubbard & Lampe (1969) has no reference in the code. Whose fit is it, and what range of $\rho$, $T$ was it made for? Are the cuts ($\log T \ge 4.2$, $\rho \ge 10^{-13}T^2$) meant to leave out gas where the electrons are far from degenerate and conduction is negligible next to radiation?
8. **OPAL's C/O-rich tables.** The YREC paper (§2.3.2) says OPAL's tables for carbon- and oxygen-rich mixtures (Iglesias & Rogers 1993) are used in helium-burning regions; the code instead interpolates in $Z$ between OPAL at $Z = 0.1$ and the table `PURECO.DBGLAOL` (step 2), whose name suggests a C/O mixture: is it one, and with what C/O ratio, or does it interpolate between helium and C/O? Is the paper describing the older scheme, or is the C/O table meant to stand for it? A reader would ask how large the error in the core opacity of horizontal-branch and AGB models is when the C/O ratio of the core differs from the table's, and when $0.1 < Z < 1$ is reached by a straight line in $\log\kappa$.


### GETOPAC

Ramps and combines the molecular, interior, pure-metal and conductive opacities (method above).
