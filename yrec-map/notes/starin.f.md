## Explanation

**Purpose.** `STARIN` provides the starting model of each run of a job: it reads the initial stellar model from a file, or keeps the one in memory, then prepares it for evolution. Along the way it can change the model's composition, extend the model toward the centre, rescale it, move the envelope's fitting point, and it computes the shell masses, the rotation quantities, the surface composition and the first convection-zone quantities.

**How it fits.**
- **Inputs:** the model file on the unit `IFIRST` ([[iounits_mod.f|`IOUNITS_MOD`]]), opened by the set-up routines; its first four characters say its format, `NMOD` (YREC7) or `MOD2` (MODEL2). The run's mixing length `CMIXL` is an argument, and `COMPMIX` (the initial model's composition code, set by the readers) is passed through to them. The run's settings come through modules filled by [[parmin.f#PARMIN|PARMIN]] and [[setups.f#SETUPS|SETUPS]]: [[nmlpar_mod.f|`NMLPAR_MOD`]] (the namelist: `LFIRST`, `LCORE`, `MCORE`, `FCORE`, the mixture controls, `LROT`, `LWNEW`, `WNEW`, `HPTTOL`, the spot parameters, `VNEW`, `LSCV`, `LDH` and others), [[runloop_mod.f|`RUNLOOP_MOD`]] (`IRESCA`, per run `NK`), [[cenv_mod.f|`CENV_MOD`]] (`LSENV0`, `SENV0`), [[newopac_mod.f|`NEWOPAC_MOD`]] (`LLAOL`).
- **Who calls it:** the main program, [[main.f#(file level)|main.f]], at the start of each run (two calls).
- **What it calls:** the readers [[getyrec7.f#GETYREC7|GETYREC7]] and [[getmodel2.f#GETMODEL2|GETMODEL2]]; [[rscale.f#RSCALE|RSCALE]] (rescaling); for a new envelope base, the physics [[eqstat.f#EQSTAT|EQSTAT]], [[getopac.f#GETOPAC|GETOPAC]], [[tpgrad.f#TPGRAD|TPGRAD]] and the envelope integration [[envint.f#ENVINT|ENVINT]]; for rotation, [[fpft.f#FPFT|FPFT]] and [[momi.f#MOMI|MOMI]]; then [[surfopac.f#SURFOPAC|SURFOPAC]], [[setscv.f#SETSCV|SETSCV]], [[physic.f#PHYSIC|PHYSIC]], [[ovrot.f#OVROT|OVROT]] and [[gettau.f#GETTAU|GETTAU]].
- **Outputs:** the model in the arguments (`HS`, `HR`, `HL`, `HP`, `HT`, `HD`, `HCOMP`, `LC`, `OMEGA`, `M` and the rest), and many modules: the surface composition in [[comp_mod.f|`COMP_MOD`]] and [[comp2_mod.f|`COMP2_MOD`]] (`XENV`, `ZENV`, `ZENVM`, `AMUENV`, `FXENV`, `YENV`, `Y3ENV`), read by the equation of state and opacity routines; the previous model in [[oldmod_mod.f|`OLDMOD_MOD`]] (`HPO`, `HTO`, `HRO`, `HLO`, `TEFFLO`, the surface luminosity `HLSURO`), read by [[htimer.f#HTIMER|HTIMER]] and others to limit the time step, and the starting model's rotation convective flags `LCZO`, read by [[crrect.f#CRRECT|CRRECT]]; [[oldrot_mod.f|`OLDROT_MOD`]] (`WOLD`); and [[ovrtrn_mod.f|`OVRTRN_MOD`]] (`TAUCZ0`, `PPHOT0`, `FRACSTEP`).
- **Modules:** 16 of them; besides those above, [[constants_mod.f|`CONSTANTS_MOD`]], [[debhu_mod.f|`DEBHU_MOD`]] (the Debye–Hückel composition), [[dpmix_mod.f|`DPMIX_MOD`]] (`IOVIM`), [[nmlbypass_mod.f|`NMLBYPASS_MOD`]], `JSON` from [[dimensions_mod.f|`DIMENSIONS_MOD`]], and the envelope's [[envstruct_mod.f|`ENVSTRUCT_MOD`]] (filled by `ENVINT`, shared with [[stitch.f#STITCH|STITCH]], [[gettau.f#GETTAU|GETTAU]], [[tauint.f#TAUINT|TAUINT]] and others).

**The method, in order.**
1. **Stop on failure.** If `LARGE` is set (the previous model failed to converge), the run stops (exit status 1).
2. **Read or keep.** If `LFIRST(NK)` is false, the model in memory is kept, and the reading, the mixture change, and the core extension are skipped (the model is rescaled at step 5). Otherwise the format keyword decides the reader; another keyword stops the run (exit status 3). After reading: $\Delta t$ in seconds, `DELTS = CSECYR*DDAGE` (the step `DDAGE` is in years); for an evolved model (`MODEL > 0`), a warning if the model's mixing length differs from the run's by $2\times10^{-3}$ or more, or its "extended composition" switch differs (the run is no longer stopped, since 1/92; the warning prints an unset variable for the model's switch, bug 5). The envelope is always recomputed (`LNEW = .TRUE.`). If `LWNEW`, the model is set to solid-body rotation at `WNEW`; without rotation, the distortion factors `FP`, `FT` are 1.

    > **Question** ([[#L316-L337]]). **The mixing-length check.** A mismatch of mixing length or composition switch now only warns. Should the run still stop, as the commented-out `STOP` did?

3. **Change the mixture** (MHP 10/24), only for a model read from file, and only if it is chemically homogeneous (every species within $10^{-6}$ of its central value). With `LMIXTURE`, the C, N and O isotopes are scaled so that each element's share of $Z$ (`HCOMP(3,·)`) becomes `FRAC_C`, `FRAC_N`, `FRAC_O`:
   $$X_i \to X_i\,\frac{f_\mathrm{C}}{(X_{^{12}\mathrm{C}} + X_{^{13}\mathrm{C}})/Z}\quad (i = {}^{12}\mathrm{C}, {}^{13}\mathrm{C}),$$
   and likewise for N (indices 7–8) and O (9–11). With `LISOTOPE`, the ratios $^{12}$C/$^{13}$C = `R12_13` and $^{16}$O/$^{18}$O = `R16_18` are imposed at fixed sums, and $^3$He, $^2$H, $^6$Li, $^7$Li and $^9$Be are set to their `…_INI` values (the default `R16_18`: bug 3). `R14_15`, `R16_17`, `XB10_INI` and `XB11_INI` (in `NMLBYPASS_MOD`) are not applied: "AT PRESENT B10,B11,N15,O17 ARE NOT USED AND THUS NOT ALTERED" ([[#L439]]; unused?), and the documentation calls them placeholders. (The order of `HCOMP`'s 15 species, from the printed labels: X, Y, Z, $^3$He, $^{12}$C, $^{13}$C, $^{14}$N, $^{15}$N, $^{16}$O, $^{17}$O, $^{18}$O, $^2$H, $^6$Li, $^7$Li, $^9$Be.)
4. **Extend the core** (`LCORE`, for a model read from file; MHP 9/98, 9/14). If the extended model would exceed `JSON` points, the run stops (exit status 3). `MCORE` points are added inside the innermost shell (the old points are shifted outward, but not their densities: bug 1), spaced by `HPTTOL(2)` in $\log m$, with `MCORE = INT(DLOG10(FCORE)/HPTTOL(2))+1`; `FCORE` (a namelist variable) is then overwritten with `MCORE*HPTTOL(2)`, a log offset rather than the factor it was. Inward, at constant density $\rho_c$ (`HD(1)`), constant energy generation and constant $\nabla$:
   $$\log r = \tfrac13\left(\log m - \log\tfrac{4\pi}{3} - \log\rho_c\right),\qquad L = L_1\,\frac{m}{m_1},$$
   $$\frac{d\ln P}{d\ln m} = -\frac{G m^2}{4\pi r^4 P},\qquad \Delta\log T = \nabla\,\Delta\log P,$$
   with the pressure step taken at the midpoint (two evaluations), $\nabla$ from the first two old points (0/0 when `MCORE` = 1: bug 4), and the density from $\log\rho = \log P - \log T - $ const (`FACD`, fixed at the first old point; MHP 4/12 replaced a "broken" EOS call).
5. **Rescale** with `RSCALE` if `IRESCA(NK)` ≠ 1.
6. **Move the envelope's fitting point** (`LSENV0`), to `SENV0`, the log of the fitting point's mass fraction, $\log_{10}(m_\mathrm{fit}/M_\star)$ (as `SENV = HS(M) - HSTOT`): a small negative number, at most $-10^{-12}$ ("τ = 2/3"; a positive value is made negative, [[#L587-L591]]), which puts the fitting point a fraction $\approx 2\times10^{-12}$ of the mass below the surface. Nothing is done when the current `SENV` matches `SENV0` to within `SENVTOL` $= 100\,\epsilon\,|\texttt{HSTOT}|$ (100 units in the last place of `HSTOT`, about $7\times10^{-13}$, below the $10^{-12}$ minimum), since `SENV`, a difference of two log masses near 33, carries roundoff of order $10^{-14}$. For a deeper point, shells beyond it are dropped and the new last shell is interpolated linearly in $\log m$; if it lies between a convective and a radiative shell, the physics routines (`EQSTAT`, `GETOPAC`, `TPGRAD`) decide whether it is convective. For a shallower point (bug 2 for the interpolated last shell), an envelope is integrated with `ENVINT` from the surface (at the model's $L$ and $T_\mathrm{eff}$, or the spotted star's ambient temperature, below), shifted to match the last interior point, and its points down to the new fitting mass become interior shells (constant $L$), each with its envelope point's convective flag. With rotation the new shells rotate at the old surface rate, with $j = \tfrac23\,\Omega r^2$.

    > **Question** ([[#L587-L591]]). **The smallest envelope.** The User Guide says that `SENV0A` values above $-10^{-11}$ are set to $-10^{-11}$, which puts the fitting point at the atmosphere's boundary, and that the value must be negative; the code clamps at $-10^{-12}$ ("DBG 2/92," the comment saying $10^{-12}$ corresponds to $\tau = 2/3$), and turns a positive value into its negative, which is how the default `SENV0A` = $1.26\times10^{-4}$ in `NMLPAR_MOD` works. Which minimum is right, and should the documentation mention the sign change?

7. **Shell masses.** With $m_i = 10^{\texttt{HS}(i)}$ (`HS1`), each shell's mass `HS2` is
   $$\Delta m_i = \tfrac12\,(m_{i+1} - m_{i-1}),\quad \Delta m_1 = \tfrac12\,(m_2 + m_1),\quad \Delta m_M = M_\star - \tfrac12\,(m_{M-1} + m_M).$$
8. **Rotation.** `FPFT` and `MOMI` give the distortion and moments of inertia $I_i$; then $J_i = \Omega_i I_i$, $j_i = J_i/\Delta m_i$ (`HJM`), $K_i = \tfrac12 \Omega_i J_i$ (`HKEROT`), and the totals `SJTOT`, `SKEROT`, printed beside the previous ones.
9. **Surface composition** (first run only, `NK = 1`): from the relative mass fractions `V` of 12 elements (`VNEW` from the parameters unless the old `LLAOL` opacities are used), with H and He set from $X$ and $Y$, the number fractions $f_k = (V_k/A_k)/\sum_l (V_l/A_l)$ (`FXENV`, atomic weights `ATOMWT`), and $Z$ without C, N and O (`ZENVM`). With the mass fractions $X_k$ of all 12 elements, H and He included,
   $$\texttt{AMUENV} = \sum_{k=1}^{12} \frac{X_k}{A_k},$$
   the inverse mean atomic weight per ion (as [[checkc.f#CHECKC|CHECKC]]'s comment says; STARIN's own comment, [[#L920]], calls it the "MEAN ATOMIC WEIGHT OF SURFACE Z," which the code does not compute, [[#L932-L937]]). Then the surface opacity tables (`SURFOPAC`) and, with `LSCV`, the SCV equation of state (`SETSCV`).

    > **Question** ([[#L904]]). **The surface composition only for the first run.** This step, up to `SURFOPAC`, is skipped when `NK > 1` (`GOTO 630`), so a later run that reads a new model from file (or changes the mixture) keeps the first run's `XENV`, `ZENV`, `FXENV`. Intended?

10. **Save the old model** in `OLDMOD_MOD`/`OLDROT_MOD` (`TEFFLO = TEFFL` and `HLSURO = HL(M)` are set inside the loop over the shells, [[#L956-L969]], to the same effect as once before it), then compute the physics of all shells (`PHYSIC`), the convection and overshoot zones (`OVROT`, whose rotation convective flags `LCZ` are kept as `LCZO` for CRRECT, as [[hpoint.f#HPOINT|HPOINT]] keeps them after each rezone) and the convective turnover time and photospheric pressure (`GETTAU`), kept as `TAUCZ0`, `PPHOT0`; `FRACSTEP = 0.5`.

**Spots** (G. Somers 10/14). For a spotted star (`SPOTF` the covering fraction, `SPOTX` the spot-to-ambient temperature ratio), the envelope is integrated at the ambient temperature
$$\log T_\mathrm{amb} = \log T_\mathrm{eff} - \tfrac14 \log_{10}\!\left(f\,x^4 + 1 - f\right).$$

**Design.** Many paths print to the screen (`WRITE(*,…)`) as well as to `ISHORT`. Errors end the run with `STOP 1` (a failed model), `STOP 3` (bad input), or the bare `STOP 9999` or `STOP 9998` (too many points, coincident masses). A large commented-out block (G. Somers 8/17) computed the gradients of every shell; `PHYSIC` does that now. `FCORE` and `MCORE`, which the core extension overwrites, are namelist variables in `NMLPAR_MOD`.

**The starting models** (from YREC's [User Guide](https://yrec.readthedocs.io/en/latest/userguide.html)). The model read from `FFIRST` comes from a library of converged models, since YREC, a relaxation code, cannot start from nothing: `seed` models, the legacy pre-main-sequence models high on the Hayashi track (those ending in `.pms` far above the birthline, good for perturbing to new conditions; those in `.ahbl` at the deuterium-burning birthline, good for rotating models); `start` models, made from the seeds with the GS98 mixture, the OPAL 2006 equation of state, a gray atmosphere and OP with Alexander (2006) opacities, densely for solar metallicity (0.03 to 25 $M_\odot$) and sparsely for $Z$ = 0.001 to 0.06, the place to start for a large change of mass or composition; and `dbl` models, run to the deuterium-burning birthline (central D down by 1%), the recommended start for most work; a few terminal-age main-sequence models serve the test suite. The User Guide notes that the seeds' CNO abundances follow GS98 and must be adjusted by hand for another mixture; step 3 (the mixture controls) is the code's way to do it. With `LSENV0A`, the fitting point is moved to `SENV0A`, $\log_{10}$ of the mass fraction below it: $-10^{-4}$ is standard, $-10^{-7}$ a thin envelope (see the question at step 6).

**From YREC's documentation.** [Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html) (Mixtures) explains the composition controls that `STARIN` applies, only to a starting model read from `FFIRST` (`LFIRST`): `ISETMIX` = 0 leaves the CNO mixture alone, 1 uses the preset `AMIX` (`GS98`, `AAG21`, `M22P`, `M22M`; it is recommended to match the mixture of the opacity tables), 2 a custom one from `FRAC_C`, `FRAC_N`, `FRAC_O` (the fractions of the metals by mass in C, N, O; GS98: 0.172148, 0.050426, 0.468195). `ISETISO` does the same for the isotope ratios `R12_13` (C12/C13), `R16_18` (O16/O18) and the initial mass fractions `XH2_INI`, `XHE3_INI`, `XLI6_INI`, `XLI7_INI`, `XBE9_INI` of D, He3, Li6, Li7 and Be9, with `AISO = 'L21'` (Lodders 2021, the only preset); `R14_15`, `R16_17`, `XB10_INI`, `XB11_INI` are placeholders (N15, O17, B10, B11 are not followed). [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) adds: `LCORE` moves the central fitting point inward by a Taylor expansion, by the factor `FCORE` in mass; `MCORE` is obsolete as an input (STARIN computes it from `FCORE`); `LWNEW` turns a non-rotating model into one rotating uniformly at `WNEW` (rad/s; with disk locking it should equal the disk's rate, `PDISK`).

**Changed since `rp_1`.** COMMON blocks to modules, `IMPLICIT NONE` (unused blocks and the old opacity-table arrays dropped); new arguments `CMIXL` (formerly in COMMON) and `COMPMIX` (formerly COMMON `I2O`), with `CMIXL` passed on to `TPGRAD`, `ENVINT`, `PHYSIC` and `GETTAU`; the MHD equation of state is removed, and for a new last shell between a convective and a radiative one `EQSTAT` is now always called (the authors' fix of an unintended bug), which settles former question 1, so former questions 2–11 are now 1–10; the write-only `IDT`, `IDD` are gone.

**Changed since `09c3b9b`.** The fitting point is left alone when the requested `SENV0` equals the current `SENV` to within roundoff (`SENVTOL`, new), not only when the two are exactly equal: before, a request that differed by roundoff took the shallower-envelope branch, added a point with `FX` = 0 (a copy of point `M`), and `SPLINT` stopped on the duplicate abscissa (the authors' fix).

**Changed since `a8a5950`.** `QDT` and `QDP` are no longer arguments (now locals; MAIN only passed them on to CRRECT); a kept model is rescaled once, not twice (the `RSCALE` call before the jump to label 3000 is gone); a core extension past `JSON` now stops the run, which settles former question 1, so former questions 2–12 are now 1–11; the shift of the new envelope points now moves their convective flags `LCENV` too, which were read one point off; the saved point count `MO` is replaced by the surface luminosity `HLSURO`, for ENTIME's limit on the motion in the HR diagram; the starting model's rotation convective flags are saved in `LCZO` for CRRECT's call to GETROT; the stops now exit with status 1 (failed model) or 3 (bad input) (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(harmless in the runs)** **The densities are not shifted in the core extension.** ([[#L499-L510]], [[#L518]]) The loop that shifts the old points outward by `MCORE` moves `HS`, `HR`, `HL`, `HP`, `HT`, `LC`, `HCOMP` and `OMEGA`, but not `HD`. After it, `HD(MP1)`…`HD(M)` hold the densities of the old points of the same index, not of the points now stored there, and `HD(M+1)`…`HD(MN)` are never set. `FACD = HP(MP1)-HD(MP1)-HT(MP1)` then mixes the pressure and temperature of the old first point with the density of old point `MP1`, and every new core density ([[#L561]]) inherits the error; `HD(M)`, now unset, is read again when the fitting point is moved ([[#L625]], [[#L741]], [[#L785]]), and `PHYSIC` passes each `HD` on to `EQSTAT` ([[physic.f#L94]]). Taken whenever `LCORE` is true for a model read from file (default false; set in 110 of the repository's namelists, such as `testsuite/Test_solarGS98_base.nml2`).

    **A possible fix:**

    ```diff
    --- a/src/starin.f
    +++ b/src/starin.f
    @@ -496,12 +496,15 @@
               ENDIF
               DS = HPTTOL(2)
     c shift data for remaining points by the required number
    +C 11/09/26 KC via Claude
    +C code changed to shift the densities with the other quantities.
               DO I=M,1, -1
                  HS(I+MCORE) = HS(I)
                  HR(I+MCORE) = HR(I)
                  HL(I+MCORE) = HL(I)
                  HP(I+MCORE) = HP(I)
                  HT(I+MCORE) = HT(I)
    +             HD(I+MCORE) = HD(I)
                  LC(I+MCORE) = LC(I)
                  DO J=1, 15
                     HCOMP(J,I+MCORE) = HCOMP(J,I)
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The core was extended in 12 runs, 10 of YREC's cases (such as `testsuite/Test_solarGS98_SF3` and `examples/run_from_seed_to_start/m10000gs98z001000_prems`) and two made-up variants, by 26 to 101 points on models of 802 to 969 shells; in all 12, `HD(MP1)` differed from the density it should hold, `HD(1)` (the two from −3.191 to −1.566 and −3.190 to −1.565). With `HD` shifted, `testsuite/Test_solarAAG21_dif` and `testsuite/Test_solarGS98_allard` change about as much as with a null change (nearly every opacity, all with 3 <= log T <= 9 and -6 <= log rho <= 9.75, times 1 + 1e-10): $\log L$ by up to $8.2\times10^{-5}$ and $1.1\times10^{-4}$ dex, against $7.6\times10^{-5}$ and $1.4\times10^{-4}$; $\log T_c$ by up to $3.5\times10^{-5}$ and $4.0\times10^{-5}$, against $1.2\times10^{-5}$ and $3.7\times10^{-5}$; central $X$ by up to $8.7\times10^{-5}$ and $6.2\times10^{-5}$, against $4.0\times10^{-5}$ and $9.0\times10^{-5}$; the same numbers of models and end ages. Within the noise: The converging model does not keep the wrong starting densities in these runs, so what remains is fragile code. No comment explains why `HD` is left out of the shift.

2. **(not reached)** **A reversed sign in the envelope interpolation.** ([[#L790-L791]]) When a shallower fitting point falls between the last interior point and the first envelope point (`JM` = 1), the new shell gets `HCOMP(1,J) = HCOMP(1,M)+FX*(HCOMP(1,M)-ENVX(JM))`, and likewise for `HCOMP(3,J)`, while every other quantity on the neighboring lines, and the same interpolation between two envelope points ([[#L813-L814]]), uses `(new - old)`. $X$ and $Z$ of the new shell are then extrapolated away from the envelope's value instead of toward it. The error is zero when the envelope's $X$, $Z$ equal the last shell's, as they do when the envelope is integrated with the model's surface composition; it is not traced for a model whose last shell differs (after settling, for example). Taken with `LSENV0` and a shallower `SENV0` (default off).

    **A possible fix:**

    ```diff
    --- a/src/starin.f
    +++ b/src/starin.f
    @@ -787,8 +787,11 @@
                          HR(J) = HR(M)+FX*(ENVR(JM)-HR(M))
                          HS(J) = X1
                          HT(J) = HT(M)+FX*(ENVT(JM)-HT(M))
    -                     HCOMP(1,J) = HCOMP(1,M)+FX*(HCOMP(1,M)-ENVX(JM))
    -                     HCOMP(3,J) = HCOMP(3,M)+FX*(HCOMP(3,M)-ENVZ(JM))
    +C 11/09/26 KC via Claude
    +C code changed to interpolate X and Z toward the envelope point, as
    +C the other quantities are.
    +                     HCOMP(1,J) = HCOMP(1,M)+FX*(ENVX(JM)-HCOMP(1,M))
    +                     HCOMP(3,J) = HCOMP(3,M)+FX*(ENVZ(JM)-HCOMP(3,M))
                          DO K = 4,JEND
                             HCOMP(K,J) = HCOMP(K,M)
                          END DO
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached: The runs that ask for a small envelope mass, such as `examples/run_from_dbl_to_zams/Test_m0040_feh0_noGS_ZAMS` (`SENV0A` = −1.0D-7) and `Test_m0300_feh0_noGS_ZAMS` (−1.0D-5), never placed the new point between the last interior point and the first envelope point, so the fix was not run. What would reach it: a shallower fitting point that falls in that first interval (`JM` = 1), with a last shell whose $X$ or $Z$ differs from the envelope's. No comment explains the sign; the interpolation between envelope points ([[#L813-L814]]) has the other one.

3. **(harmless in the runs)** **The defaults of `R16_18` and `R16_17` look swapped.** ([[#L448-L449]]; [[nmlpar_mod.f#L232]], [[nmlbypass_mod.f#L105]]) STARIN splits oxygen with `R16_18` as $^{16}$O/$^{18}$O. Its default is 2693.0, close to the solar $^{16}$O/$^{17}$O ratio (the documentation, `namelist_control.md` lines 201–202, gives 2644 for Lodders 2025), while `R16_17`, which nothing reads, defaults to 471.4, close to $^{16}$O/$^{18}$O (the documentation: 468.2). With `ISETISO` = 1 and the preset `AISO = 'L21'` (the default, [[parmin.f#L509]]), which applies the defaults, the starting model gets about 5.7 times too little $^{18}$O (`SUM_O`/2694 instead of `SUM_O`/472.4). Off by default (`ISETISO` = 0), but taken by the 95 namelists in the repository that set `ISETISO = 1` (none sets `R16_18`), such as `testsuite/Test_solarAAG21_dif.nml1`.

    **A possible fix,** if the defaults are meant as Lodders (2021)'s values:

    ```diff
    --- a/src/nmlpar_mod.f
    +++ b/src/nmlpar_mod.f
    @@ -229,7 +229,9 @@
           REAL*8    :: FRAC_N = 0.050426D0
           REAL*8    :: FRAC_O = 0.468195D0
           REAL*8    :: R12_13 = 88.27D0
    -      REAL*8    :: R16_18 = 2693.0D0
    +C 11/09/26 KC via Claude
    +C code changed to give R16_18 the O16/O18 default (it held O16/O17's).
    +      REAL*8    :: R16_18 = 471.4D0
           REAL*8    :: XH2_INI = 2.781D-5
           REAL*8    :: XHE3_INI = 3.461D-5
           REAL*8    :: XLI6_INI = 7.187D-10
    --- a/src/nmlbypass_mod.f
    +++ b/src/nmlbypass_mod.f
    @@ -102,7 +102,7 @@
           INTEGER*4 :: ISETMIX = 0
           INTEGER*4 :: ISETISO = 0
           REAL*8    :: R14_15 = 411.9D0
    -      REAL*8    :: R16_17 = 471.4D0
    +      REAL*8    :: R16_17 = 2693.0D0
           REAL*8    :: ZXMIX = 0.02292D0
           REAL*8    :: XB10_INI = 1.002D-9
           REAL*8    :: XB11_INI = 4.405D-9
    ```

    in `NMLPAR_MOD`, and `R16_17 = 2693.0D0` in `NMLBYPASS_MOD`.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The split ran in `testsuite/Test_solarAAG21_dif` and `testsuite/Test_solarM22M_difkur`, both with `R16_18` = 2693 (the default) and `SUM_O` = 0.0088, so both start with the too-small $^{18}$O above. With 471.4 in its place (measurement only: a local copy in STARIN, not the module defaults the fix changes), both tracks change no more than with a null change (nearly every opacity, all with 3 <= log T <= 9 and -6 <= log rho <= 9.75, times 1 + 1e-10): $\log L$ by up to $2.2\times10^{-5}$ and $1.1\times10^{-5}$ dex, against $7.6\times10^{-5}$ and $1.7\times10^{-4}$; central $X$ by up to $9.1\times10^{-6}$ and $1.8\times10^{-5}$, against $4.0\times10^{-5}$ and $8.7\times10^{-6}$. Within the noise. The track does not carry $^{18}$O, so the harm the item names, the starting $^{18}$O itself, is not measured here. Intent: `namelist_control.md` (lines 201–202) gives 468.2 for $^{16}$O/$^{18}$O, which agrees with a swap.

4. **(stops the run)** **Checked by KC** (Nov 10, 2026). **0/0 with one core point.** ([[#L480]], [[#L515]], [[#L534]]) With `MCORE` = 1 (the default `FCORE` = 1.0 gives `INT(0)+1` = 1, as does any `FCORE` below $10^{\texttt{HPTTOL(2)}}$), the shift sets `HT(2) = HT(1)` and `HP(2) = HP(1)`, so `DEL = (HT(2)-HT(1))/(HP(2)-HP(1))` is 0/0: The new central temperature is NaN (or, in the `devel` build, which traps invalid operations, the run stops). With `MCORE` ≥ 2, points 1 and 2 are still the old first two points, and `DEL` is their gradient. Taken with `LCORE` and the default `FCORE`; every namelist in the repository that sets `LCORE` also sets `FCORE` = 10, which gives `MCORE` ≥ 26.

    **A possible fix,** which gives the same `DEL` whenever `MCORE` ≥ 2:

    ```diff
    --- a/src/starin.f
    +++ b/src/starin.f
    @@ -512,7 +512,10 @@
     C MARCH INWARD IN MASS FROM THE INNERMOST MODEL POINT.
     C ASSUME EPSILON=CONSTANT AND DEL=CONSTANT
               RHOC = HD(1)
    -          DEL = (HT(2)-HT(1))/(HP(2)-HP(1))
    +C 11/09/26 KC via Claude
    +C code changed to take DEL from the first two shifted points, so that
    +C it is not 0/0 when MCORE = 1.
    +          DEL = (HT(MP1+1)-HT(MP1))/(HP(MP1+1)-HP(MP1))
               HLC = HL(1)
     C MHP 4/12 FACTOR FOR ESTIMATING RHO FROM P AND T
               FACD = HP(MP1)-HD(MP1)-HT(MP1)
    ```

    **How the code itself shows it.** The comments state what `DEL` is: "`MARCH INWARD IN MASS FROM THE INNERMOST MODEL POINT.`", "`ASSUME EPSILON=CONSTANT AND DEL=CONSTANT`" ([[#L512-L513]]), and "`ASSUME DEL= CONSTANT IN THE CORE`" ([[#L533-L534]]), so `DEL` is the gradient at the old innermost point. After the shift that point sits at `MP1` ([[#L511]]), and most lines of the block read it there: `FACD` from `HP(MP1)` and `HT(MP1)` ([[#L518]]), `HS(MP1)` for the luminosity ([[#L524]]), and `LC(MP1)`, `OMEGA(MP1)`, and `HCOMP(J,MP1)` ([[#L532]], [[#L536]], [[#L539]]). `RHOC` and `HLC` still read index 1 (`HD(1)` and `HL(1)`, [[#L514]], [[#L516]]); `HD` is not shifted, and `HL(1)`, `HT(1)`, and `HP(1)` still hold the old innermost point only because the shift loop never writes index 1 ([[#L499-L510]]), while it writes index 2 from index 1 whenever `MCORE` = 1. The fix reads `DEL` at `MP1` and `MP1+1`, where its neighbors read their quantities.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): YREC's cases all set `FCORE` = 10 (26 to 101 core points in the 12 runs that extend the core), so `testsuite/Test_solarGS98_kurucz` was run with `FCORE` = 1.0, the code's default: The core grew by one point, `DEL` became 0/0, and the run stopped in its first second in TPGRAD ("TRIED TO TAKE SQUARE ROOT OF NEGATIVE NUMBER," with NaNs; `STOP 912`, exit status 144, that is 912 mod 256). The line counting the condition fired before the run stopped (its first hit, with `MCORE` = 1, is in the run's `probe.log`; its count was lost, since `STOP 912` ends the run before the counts are written). With `DEL` taken from the shifted points (the fix), the same case runs to its end (exit status 0, after 185 s). No comment says `MCORE` = 1 is excluded.

5. **(wrong output)** **Checked by KC** (Nov 10, 2026). **The warning prints an unset variable.** ([[#L328-L333]]; [[#L86]]) Format 1040 prints `LEXCP0` as the model's extended-composition switch, but `LEXCP0` is declared and never set; the model's value is `LEXCOM0`, which the test on the line above uses ("MHP 9/03 FIXED TYPO" fixed the test, not the `WRITE`). The message then shows whatever `LEXCP0` holds. Meant to be taken whenever an evolved model's mixing length or switch differs from the run's; with `LEXCOM` true, only when the switch differs (below).

    **A possible fix:**

    ```diff
    --- a/src/starin.f
    +++ b/src/starin.f
    @@ -83,7 +83,7 @@
           INTEGER I,IDUM,IKUT,IREAD,ISTORE,IXX,J,JCORE0,JEND,JENV,JENV0,JM,
          *       K,M,MM,MN,MODEL,MP1,MRZONE,MXZONE,NK,NRZONE,NZONE
           LOGICAL*4 LARGE,LATMO,LC,LCONV,LCZ,LDERIV,LDIFY0,LDIFZ0,LDISK0,
    -     *       LEXCOM0,LEXCP0,LINSTB0,LJDOT00,LMIXL,LNEW,LOCOND,LOVSTC0,
    +     *       LEXCOM0,LINSTB0,LJDOT00,LMIXL,LNEW,LOCOND,LOVSTC0,
          *       LOVSTE0,LOVSTM0,LPRT,LPULPT,LPUREZ0,LROT0,LSBC0,LSEMIC0
     
     C DBGLAOL
    @@ -324,9 +324,13 @@
     C mixing length to four sig digits.
            IF(CMIXL0.GT.0.0D0) LMIXL = (DABS(CMIXL-CMIXL0).LT.2.0D-3)
     C MHP 9/03 FIXED TYPO
    -       IF(.NOT.LMIXL .OR. LEXCOM0.NEQV.LEXCOM) THEN
    -          WRITE(ISHORT,1040) CMIXL,CMIXL0,LEXCOM,LEXCP0
    -          WRITE(IOWR,1040) CMIXL,CMIXL0,LEXCOM,LEXCP0
    +C 11/10/26 KC via Claude
    +C code changed to group the switch test, which .NEQV. otherwise
    +C applies to the whole .OR., and to print the model's switch LEXCOM0,
    +C not the unset LEXCP0.
    +       IF(.NOT.LMIXL .OR. (LEXCOM0.NEQV.LEXCOM)) THEN
    +          WRITE(ISHORT,1040) CMIXL,CMIXL0,LEXCOM,LEXCOM0
    +          WRITE(IOWR,1040) CMIXL,CMIXL0,LEXCOM,LEXCOM0
      1040       FORMAT(1X,'ERROR IN SUBROUTINE STARIN'/1X,'USER PARAMETERS',
          *      ' OF WRONG TYPE FOR INITIAL MODEL'/1X,'MIXING LENGTH - USER'
          *      ,' DESIRES',F7.3,' MODEL MIX LENGTH',F7.3/1X,
    ```

    and `LEXCP0` dropped from the declaration.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Not reached: The warning was printed in none of the 33 runs, and the line counting it never fired. The cause, found on Nov 10, 2026: The test itself ([[#L327]]). In Fortran `.NEQV.` binds more loosely than `.OR.`, so `.NOT.LMIXL .OR. LEXCOM0.NEQV.LEXCOM` reads as `(.NOT.LMIXL .OR. LEXCOM0) .NEQV. LEXCOM`; with `LEXCOM` true, as all 965 `.nml2` files in the repository set it, a wrong mixing length makes the left side true and the test false, so the warning is never printed for it (every other combination gives the intended answer). Lines counting the test in `examples/class_exercises/exercise_4/Grid_m4p0feh+0p0GS98_std25_TAMS` show it reached once, for model 32 of `startmodels/dbl_grid/m4000gs98z016492_Dbl.first`, with the model's mixing length 1.853 against the run's 1.708, and no warning. With the test written `.NOT.LMIXL .OR. (LEXCOM0.NEQV.LEXCOM)` and `LEXCOM0` printed, the same case prints the warning ("MIXING LENGTH - USER DESIRES  1.708 MODEL MIX LENGTH  1.853," "EXTENDED COMP-USER DESIRES T MODEL USED T"); its track and stored models are identical, and only the `.short` file differs, by the warning's lines. Only a message is wrong.

### STARIN

Reads or keeps the starting model and prepares it: mixture changes, core extension, rescaling, a new envelope fitting point, shell masses, rotation, surface composition, and the first convection-zone quantities (steps above).
