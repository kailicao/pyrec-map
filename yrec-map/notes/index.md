**What it is.** YREC, the Yale Rotating Evolution Code, at its development branch's commit 7be4133 (Nov 2, 2026; the map was written for 09c3b9b and moved on Oct 31 and Nov 9): 282 fixed-form Fortran files in `src/`, about one routine per file. 85 of them are modules (`*_mod.f`), which replaced the COMMON blocks of the release `rp_1` (where this site began): routines share data through the modules they `USE` (see the Modules page; every module variable is in the [Glossary](glossary.html), under its name in lower case) as much as through arguments, so a routine's modules matter as much as its calls. Since `rp_1`, the development branch has also removed legacy options (the MHD equation of state, the OPAL 1995 and 2001 equations of state, the Kurucz 1990, LAOL89 (all but its pure-metal table), Alexander 1995 and OPAL92 opacities, and the Monte Carlo loop), with 58 files, and fixed a number of bugs; each page's explanation ends with a "Changed since `rp_1`" line.

**Where to start.** [main.f](yrec-map/main.f.html) is the main program (it has no PROGRAM statement), and its page walks through the whole run. In order, it:

1. reads the run's settings and tables: [PARMIN](yrec-map/parmin.f.html), then [SETUPS](yrec-map/setups.f.html);
2. optionally sets up a calibration: of the Sun ([SETCAL](yrec-map/setcal.f.html)) or of a star of given $L$ and $T_\mathrm{eff}$ ([SETSCAL](yrec-map/setscal.f.html));
3. for each "kind card" (one run of the job), reads the starting model ([STARIN](yrec-map/starin.f.html)), writes the headers ([WRTHEAD](yrec-map/wrthead.f.html)) and sets the first time step ([HTIMER](yrec-map/htimer.f.html));
4. evolves it model by model. Each step: mass loss ([MASSLOSS](yrec-map/massloss.f.html)); mixing, burning and settling ([MIX](yrec-map/mix.f.html), with [KEMCOM](yrec-map/kemcom.f.html) and [GRSETT](yrec-map/grsett.f.html)); rezoning ([HPOINT](yrec-map/hpoint.f.html)); the structure, by four levels of the Henyey iteration ([CRRECT](yrec-map/crrect.f.html)), where a divergence ends the run (despite a comment about cutting the step, see main.f); convective mixing ([MIXCZ](yrec-map/mixcz.f.html)); rotation ([GETW](yrec-map/getw.f.html), [FPFT](yrec-map/fpft.f.html)); lithium burning ([LIRATE88](yrec-map/lirate88.f.html), [LIBURN](yrec-map/liburn.f.html)); the next time step (HTIMER); output ([WRTOUT](yrec-map/wrtout.f.html)); and the stop conditions. The composition is not among the Henyey unknowns: MIX changes it over the step with the current structure, the Henyey iteration then solves for $P$, $T$, $r$, $L$ with the composition fixed, and levels 3 and 4 redo the burning and mixing, from the start-of-step composition, with the new structure (an operator split; [CRRECT](yrec-map/crrect.f.html), step 2);
5. ends each kind card with [PUTSTORE](yrec-map/putstore.f.html) and the calibration checks ([CHKCAL](yrec-map/chkcal.f.html), [CHKSCAL](yrec-map/chkscal.f.html)).

**How a run goes.** (From YREC's documentation, [yrec.readthedocs.io](https://yrec.readthedocs.io/en/latest/), as the code does it.) One call, `yrec control.nml1 physics.nml2`, runs one job on one star. [PARMIN](yrec-map/parmin.f.html) reads the two namelists: the control namelist names the starting model, the tables and the output files (paths may use `{YREC_INPUT}`, `{YREC_START}`, `{YREC_OUTPUT}`, filled from environment variables) and lists the job's runs, the "kind cards"; the physics namelist chooses the physics (equation of state, opacities, atmosphere, nuclear rates, convection and overshoot, diffusion, rotation) and the numerical controls. [SETUPS](yrec-map/setups.f.html) reads the tables. Since YREC is a relaxation code, every job starts from a converged model, from the library in `input/models/` (most often one at the deuterium-burning birthline) or from an earlier job's `.last` file, read by [STARIN](yrec-map/starin.f.html).

Each kind card then rescales the model to the wanted mass, composition and mixing length ([RSCALE](yrec-map/rscale.f.html); with a zero time step, or with evolution for a pre-main-sequence model, which has no static solution unless deuterium burning carries its luminosity, see [main.f](yrec-map/main.f.html), step 3 of the evolution step), or evolves it, model by model, until a number of models, an age or a central abundance is reached.

After each model, [WRTOUT](yrec-map/wrtout.f.html) appends a line to the `.track` file (the global properties over time) and numerical details to `.short`, rewrites `.last` (the latest model, to restart from), and, as asked, writes snapshots of the structure to `.store` ([PUTSTORE](yrec-map/putstore.f.html)) and pulsation files ([WRTMOD](yrec-map/wrtmod.f.html)). A grid of stars is many such jobs, run by scripts or by the Python wrapper (`pip install yrec`), which runs the same executable. The test suite (`testsuite/`, run with pytest) runs a set of such jobs, solar models, brown dwarfs and stars of 0.1 to 9 $M_\odot$ evolved to various stages, and compares their outputs with stored reference outputs; it is how a change to the code is checked.

**The code's conventions.** Changes in the source carry a comment with their date and the author's initials ("MHP 10/24", "G. Somers 11/14", "KC 2025-05-31", and, for changes made with an AI assistant, "MHP via Claude"), which is why the pages list them. Variable names still follow the old implicit types (`A–H` and `O–Z` real, `I–N` integer, `L` logical), although every file now declares its types under `IMPLICIT NONE`. Character strings stay out of the modules, as they once stayed out of the COMMON blocks: file names are read and tied to unit numbers in PARMIN, and the few strings used elsewhere (the version, the mixture's name) are passed as arguments through the main program. The namelist variables live in two modules, [NMLPAR_MOD](yrec-map/nmlpar_mod.f.html) and [NMLBYPASS_MOD](yrec-map/nmlbypass_mod.f.html), with their defaults. A physics routine returns its derivatives with its value (an opacity with its derivatives in density and temperature, for example), so an alternative must return the same set.

## Reading this site


Each file's page has an outline in the margin, its text on the left, and the whole file's code on the right, which stays in view: the Fortran, re-indented by its loops and IF blocks (switch to "as in YREC" for the code as written), or its Python translation, whose blocks name the Fortran lines they translate. Every link to lines (in a question, a bug, a call) shows those lines in the code, and a ↗ beside it opens them on GitHub. Each routine's section gives the modules it uses (each linked to the module's page, which lists every unit using it), what calls it, and a flowchart of its calls in the order of the source, nested in boxes for its loops and branches; lines with a compiler's warning (gfortran) or a linter's finding (ruff, in the Python) are marked. Calls are found by reading the code, not by running it. Only `src/` is mapped; the `.f` files under `input/`, tools for the data tables, are left out. Many files carry changes marked "KC 20…" (Kaili Cao's), with the old lines kept as comments beside them, which is where they are read.

### A reading path

A route through the 15 topics of [Files by topic](#files-by-topic), for a newcomer who wants to read every page. Within each topic, read the files named here first, then the rest in the order their topic's table lists them (the routines, then the modules, which are short and best read beside the routines that use them).

1. **The main program and the run's control:** [[main.f]] first, its page walks through a whole run; then [[rscale.f]], and the calibrations [[setcal.f]] and [[chkcal.f]].
2. **Input:** [[parmin.f]] with [[nmlpar_mod.f]] (what every setting means), then [[setups.f]] and [[starin.f]].
3. **The structure equations and the Henyey solver:** [[crrect.f]], [[coefft.f]] (the four equations), then [[reduce.f]] and [[hsolve.f]].
4. **Atmospheres, the envelope and the boundary conditions:** [[surfbc.f]] (the envelope triangle), [[envint.f]], then [[qenv.f]] and [[qatm.f]].
5. **The equation of state:** [[eqstat.f]], [[eqstat2.f]] (the choice and blending of the tables), then [[eqsaha.f]].
6. **Opacities:** [[getopac.f]], then [[setupopac.f]] and [[getopal95.f]].
7. **Nuclear reactions, energy generation and neutrinos:** [[engeb.f]], [[rates.f]], [[kemcom.f]].
8. **Convection, overshoot and the mixing of composition:** [[mix.f]] (the composition over a step), [[convec.f]], [[tpgrad.f]] (mixing-length theory), [[oversh.f]], [[mixcz.f]].
9. **The time step and rezoning:** [[htimer.f]], [[hpoint.f]].
10. **Output:** [[wrtout.f]], [[wrthead.f]], [[putstore.f]].

This completes a run without rotation or diffusion. The remaining topics are options, each switched on by the namelists:

11. **Microscopic diffusion and settling:** [[grsett.f]] (the older treatment), then [[microdiff.f]] (the newer one) and [[thdiff.f]] (Burgers' equations).
12. **Rotation, the structure of a rotating star:** [[fpft.f]], [[shape.f]], [[momi.f]], [[getrot.f]].
13. **Rotation, angular-momentum transport and rotational mixing:** [[getw.f]] (the driver), [[midmod.f]], [[seculr.f]], [[vcirc.f]], [[codiff.f]].
14. **Angular-momentum loss and mass loss:** [[mwind.f]], [[gettau.f]] (the overturn time), [[massloss.f]], [[mdot.f]].
15. **Numerical utilities:** as the other pages call them; [[intrp2.f]], [[interp.f]] and [[osplin.f]] are the most used.

### What the explanations found


Each page has questions for the experts, placed where their context is, and, where the code seems wrong, suspected bugs graded by what they would do (wrong results first), each with a possible fix in the code's own style; each topic of [Files by topic](#files-by-topic) lists its suspected bugs and questions in tables of their own (being reorganized this way page by page, from Nov 9, 2026; the opacity pages are done). The development branch has already fixed several found at `rp_1` (for example, `MASSLOSS` called `MDOT` with one argument too many, and `SECULR`'s whole-domain option was never switched on). Some that remain: GRSETT's convergence test ignores negative changes, and its coefficient correction sits one midpoint off; in SNEUT, `cap-cap` stands where `cap*cap` is expected; VCIRC's restored μ-current option divides by the speed of light `CC`, which is never set; and the acoustic-depth output (CALCAD) never runs, since nothing sets its switch `LACOUT` (see `ACDPTH_MOD`).

**Found in passing.** Four CALLs name routines not in `src/`: `DERIV` (in MMID, a routine passed as an argument, QENV or QATM) and, in PARMIN, `GETARG`, `GETENV` and `SYSTEM` (compiler extensions for the command line, the environment and the shell).

### Where the overhaul stands


An overhaul goes in four stages: a documentation site for the old code (this part of the site); the documentation of a new code on the same site, with references to the old one; the new code, with benchmarks (same inputs, same outputs); and a paper. The first stage is complete for `rp_1`, where every file had an explanation with questions for the code's experts and every page went through one round of review and revision; a page's review findings, folded at its end, refer to `rp_1`. On Oct 27 every page was moved to 09c3b9b, each with its Python translation in the current structure (the [pyrec](https://github.com/kailicao/pyrec) repository): the translation is checked only by compiling it, and is to be tested routine by routine against the Fortran. On Oct 31 the pages moved to a8a5950, with YREC's public documentation, the YREC paper's notation, the files grouped by topic with a reading path, and the glossary. On Nov 9 they moved to 7be4133, after a round of bug fixes by YREC's developers; each page changed since ends with a "Changed since `a8a5950`" line. The second stage is drafted: [a new design](pyrec-map/overview.html), a high-level design on one page (Nov 9, 2026): a `Model` holding the star's state and its history, with its physics and numerical methods as families of callables, each a Python base class, in Python with Numba.

## Notation


The pages write the physics in the symbols of the YREC paper (Pinsonneault et al., "The YREC Stellar Evolution Code: Public Data Release", `YREC_Public_Data_Release_Paper_revised.pdf` in the repository's root), and the code's variables in code font. The paper names some quantities only in words; for those, marked *, the pages use the usual symbol. Many arrays hold logarithms (base 10) of the quantity, per shell. The code works in cgs, except that `HL` is in $L_\odot$ and is not a logarithm, `SMASS` is in $M_\odot$, the age `DAGE` is in Gyr and the step `DDAGE` in yr (`DELTS`, the same step, in s).

| Symbol | Meaning | Fortran names |
| --- | --- | --- |
| $m$* | mass coordinate (mass inside a shell); $M$ the total mass | `HS` ($\log m$), `HS1` ($m$, g), `HS2` (the shell's mass $\Delta m$, g); `HSTOT` ($\log M$), `SMASS` ($M/M_\odot$) |
| $r$, $R$ | radius of a shell; $R$ the star's radius | `HR` ($\log r$); `RL` ($\log R/R_\odot$) |
| $L$ | luminosity (at a shell, or the star's) | `HL` ($L/L_\odot$); `BL` ($\log L/L_\odot$) |
| $P$, $T$, $\rho$ | pressure, temperature, density | `HP`, `HT`, `HD` (their logarithms) |
| $T_\mathrm{eff}$ | effective temperature | `TEFFL` ($\log T_\mathrm{eff}$) |
| $\kappa$ | opacity (Rosseland mean) | `O`, `OL` ($\log\kappa$), with `QOD`, `QOT` its derivatives |
| $\nabla$, $\nabla_\mathrm{ad}$, $\nabla_\mathrm{rad}$ | actual, adiabatic and radiative temperature gradients, $d\ln T/d\ln P$ | `DEL`, `DELA`, `DELR` (from `TPGRAD`); per shell `SDEL(2,·)`, `SDEL(3,·)`, `SDEL(1,·)` |
| $H_p$ | pressure scale height | computed where needed (`HSUBP`, `TPGRAD`) |
| $X$, $Y$, $Z$ | mass fractions of hydrogen, helium and metals | `HCOMP(1,·)`, `HCOMP(2,·)`, `HCOMP(3,·)` (`HCOMP(4..15,·)` the tracked isotopes: ³He, CNO, ²H, ⁶Li, ⁷Li, ⁹Be); the envelope's `XENV`, `ZENV`, `YENV` |
| $\mu$ | mean molecular weight | `RMU` $=\mathcal{R}/\mu$ (the gas constant over $\mu$), with its terms `AMU` $=\mu_\mathrm{ion}^{-1}$ and `EMU` $=\mu_e^{-1}$ (in the equation of state) |
| $Q_{\rho T}$*, $Q_{\rho P}$* | $(\partial\ln\rho/\partial\ln T)_P$ and $(\partial\ln\rho/\partial\ln P)_T$; in Kippenhahn, Weigert & Weiss's notation $-\delta$ and $\alpha$ | `QDT`, `QDP` (their derivatives `QDTT`, `QDTP`) |
| $c_P$* | specific heat at constant pressure | `QCP` (its derivatives `QCPT`, `QCPP`) |
| $\beta$* | ratio of gas to total pressure, $P_\mathrm{gas}/P$ | `BETA`, `BETAI` ($1/\beta$), `BETA14` ($4(1-\beta)/\beta$ in the Yale equation of state) |
| $\eta$* | electron degeneracy parameter | `ETA` |
| $\epsilon$* | energy generation rate per gram ($\epsilon_\mathrm{nuc}$ nuclear, $\epsilon_\nu$ neutrino losses, $\epsilon_\mathrm{grav}$ gravitational) | `SESUM`, `SEG(1..7,·)`, `EPSM` |
| $\alpha$ | mixing-length parameter (the mixing length in units of $H_p$) | `CMIXL` (per kind card `CMIXLA`) |
| $\alpha_c$, $\alpha_e$, $\alpha_m$* | step overshoot of cores, envelopes and intermediate zones, in units of $H_p$ (the paper: "0.2 $H_p$") | `ALPHAC`, `ALPHAE`, `ALPHAM`; the limit by core size `BETAC` |
| $\Omega$ (the paper also $\omega$) | angular velocity | `OMEGA` |
| $j$*, $I$* | specific angular momentum and moment of inertia of a shell | `HJM`, `HI` |
| $\dot M$ | mass-loss rate | `DMDT` (in `MASSLOSS` and `MDOT`) |
| $\tau_\mathrm{cz}$, Ro | convective overturn time and Rossby number | `TAUCZ` |
| $f_c$ | efficiency of rotational mixing relative to angular-momentum transport | `FC` |
| $\tau$ | optical depth | in the atmosphere integration (`QATM`, `HRA`) |
| $S_0$ | astrophysical factor of a reaction at zero energy | the rate tables of `RATES` and `CROSS_MOD` |

## Files by topic


The 282 files, in 15 topics, in the order of the reading path (in [Reading this site](#reading-this-site)); within each topic the routines come first, in reading order, then the modules that hold its data.

**The main program and the run's control.** The main program, which runs the job kind card by kind card and model by model, with the rescaling of a starting model and the automatic calibrations of the Sun and of other stars. [[main.f]], [[runloop_mod.f]], [[rscale.f]], [[setcal.f]], [[chkcal.f]], [[setscal.f]], [[chkscal.f]], [[version.f]].

**Input: namelists, tables and the starting model.** Reading the two namelists and the tables, the run's settings and constants, and the starting model. [[parmin.f]], [[nmlpar_mod.f]], [[nmlbypass_mod.f]], [[remap.f]], [[setups.f]], [[iounits_mod.f]], [[constants_mod.f]], [[confac_mod.f]], [[dimensions_mod.f]], [[starin.f]], [[getmodel2.f]], [[getyrec7.f]].

**The structure equations and the Henyey solver.** The four equations of stellar structure, their coefficients at each shell, and the Henyey iteration that solves them. [[crrect.f]], [[coefft.f]], [[physic.f]], [[reduce.f]], [[hsolve.f]], [[oldmod_mod.f]], [[intvar_mod.f]], [[scrtch_mod.f]], [[ctol_mod.f]].

**Atmospheres, the envelope and the boundary conditions.** The outer boundary condition: the envelope triangle (envelopes integrated at three points around the model's $(\log T_\mathrm{eff}, \log L)$, whose values at the fitting point are fitted by a plane to give the outer boundary condition), the integration of the envelope and atmosphere, and the model-atmosphere tables. [[surfbc.f]], [[envint.f]], [[qenv.f]], [[qatm.f]], [[bsstep.f]], [[mmid.f]], [[ratext.f]], [[getnewenv.f]], [[hra.f]], [[surfp.f]], [[kcsurfp.f]], [[alfilein.f]], [[altabinit.f]], [[alsurfp.f]], [[alprint.f]], [[intpar_mod.f]], [[qenvmix_mod.f]], [[envprt_mod.f]], [[envstruct_mod.f]], [[atmprt_mod.f]], [[atmstruct_mod.f]], [[atmos_mod.f]], [[atmos2_mod.f]], [[atmos2c_mod.f]], [[fac_mod.f]], [[cenv_mod.f]], [[alatm01_mod.f]], [[alatm02_mod.f]], [[alatm05_mod.f]].

**The equation of state.** Pressure, density and the thermodynamic derivatives: the Yale equation of state, the SCV and OPAL 2006 tables, and the blending between them. [[eqstat.f]], [[eqstat2.f]], [[eqsaha.f]], [[eqrelv.f]], [[mu.f]], [[ifermi12.f]], [[zfermim12.f]], [[eqscve.f]], [[eqscvg.f]], [[setscv.f]], [[oeqos06.f]], [[esac06.f]], [[eqbound06.f]], [[t6rinteos06.f]], [[quadeos06.f]], [[radsub06.f]], [[rhoofp06.f]], [[gmass06.f]], [[readcoeos06.f]], [[debhu_mod.f]], [[ccr_mod.f]], [[scveos_mod.f]], [[aeos06_mod.f]], [[eeeos06_mod.f]], [[eos06misc_mod.f]].

**Opacities.** The radiative opacity from the OPAL 1995 and the low-temperature (Ferguson et al.) tables, LAOL89's pure-metal table (`FPUREZ`, used where $Z > 0.1$ and $\log T > 7$, in helium-burning cores; LAOL89's tables for mixtures are removed), and the conductive opacity. [[getopac.f]], [[setupopac.f]], [[surfopac.f]], [[getopal95.f]], [[ll95tbl.f]], [[op95xtab.f]], [[op95ztab.f]], [[op952d.f]], [[op953d.f]], [[op954d.f]], [[getalex06.f]], [[readalex06.f]], [[alex06tab.f]], [[gtpurz.f]], [[rdzlaol.f]], [[zsulaol.f]], [[condopacp.f]], [[condopacpint.f]], [[newopac_mod.f]], [[op95interp_mod.f]], [[llot95_mod.f]], [[llot95a_mod.f]], [[llot95e_mod.f]], [[alot06_mod.f]], [[alot06all_mod.f]], [[galot06_mod.f]], [[zlaol_mod.f]], [[zslaol_mod.f]].

**Nuclear reactions, energy generation and neutrinos.** Reaction rates, energy generation, the burning network, deuterium and the light elements, and neutrino losses. [[engeb.f]], [[rates.f]], [[kemcom.f]], [[eqburn.f]], [[dburn.f]], [[dburnm.f]], [[deutrate.f]], [[lirate88.f]], [[liburn.f]], [[liburn2.f]], [[neutrino.f]], [[nulosses.f]], [[sneut.f]], [[cross_mod.f]], [[fluxes_mod.f]], [[deuter_mod.f]], [[newrat_mod.f]], [[oldrat_mod.f]], [[prevcz_mod.f]].

**Convection, overshoot and the mixing of composition.** Where the model is convective, its temperature gradient, overshoot and semiconvection, and the change of composition over a step (burning and mixing of convection zones). [[mix.f]], [[convec.f]], [[tpgrad.f]], [[hsubp.f]], [[findsh.f]], [[oversh.f]], [[sconvec.f]], [[mixcz.f]], [[ovrot.f]], [[comp_mod.f]], [[comp2_mod.f]], [[dpmix_mod.f]], [[liov_mod.f]], [[pualpha_mod.f]].

**The time step and rezoning.** The choice of the next time step, and the redistribution of the mass points at the start of each step. [[htimer.f]], [[xtime.f]], [[ytime.f]], [[ptime.f]], [[entime.f]], [[wtime.f]], [[hpoint.f]], [[entrop_mod.f]].

**Output.** The output files: headers, the track and short output, stored models, model files and profiles for pulsation. [[wrthead.f]], [[wrtout.f]], [[wrtlst.f]], [[putstore.f]], [[stitch.f]], [[putmodel2.f]], [[putyrec7.f]], [[wrtmod.f]], [[wrtmil.f]], [[pindex.f]], [[pdist.f]], [[calcad.f]], [[acdpth_mod.f]], [[ccout_mod.f]], [[cent_mod.f]], [[label_mod.f]], [[pulse1_mod.f]], [[pulse2_mod.f]], [[sound_mod.f]].

**Microscopic diffusion and settling.** Gravitational settling and thermal diffusion of helium, metals and light elements: the older GRSETT treatment and the newer MICRODIFF. Settling is off by default (`LDIFY`); with it on, MICRODIFF needs `LNEWDIF` (also off by default, set by the test suite's settling cases), and GRSETT runs otherwise. [[grsett.f]], [[setup_grsett.f]], [[model_to_equal.f]], [[lax_wendrof1.f]], [[lax_wendrof2.f]], [[get_imp_diffco.f]], [[tridiag_gs.f]], [[equal_to_model.f]], [[microdiff.f]], [[microdiff_setup.f]], [[microdiff_mte.f]], [[microdiff_cod.f]], [[microdiff_run.f]], [[microdiff_etm.f]], [[thdiff.f]], [[gravez_mod.f]].

**Rotation: the structure of a rotating star.** The distortion of a rotating star, its moments of inertia and the form factors that correct the structure equations, and the rotation curve. [[fpft.f]], [[shape.f]], [[func.f]], [[qgauss.f]], [[trapzd.f]], [[getqua.f]], [[intmom.f]], [[momi.f]], [[getrot.f]], [[solid.f]], [[wczimp.f]], [[errmom_mod.f]], [[quadd_mod.f]], [[quadru_mod.f]].

**Rotation: angular-momentum transport and rotational mixing.** The internal rotation over a step: angular-momentum transport by rotational instabilities and the mixing of composition they drive. [[getw.f]], [[midmod.f]], [[seculr.f]], [[setupv.f]], [[vcirc.f]], [[codiff.f]], [[getfc.f]], [[viscos.f]], [[getgrid.f]], [[rotgrid.f]], [[dcoeft.f]], [[dadcoeft.f]], [[tridia.f]], [[eq2mod.f]], [[checkj.f]], [[mixgrid.f]], [[mixcom.f]], [[ccoeft.f]], [[ndifcom.f]], [[rotmix.f]], [[bursmix.f]], [[bsrotmix.f]], [[checkc.f]], [[egrid_mod.f]], [[egridder_mod.f]], [[difad_mod.f]], [[difad2_mod.f]], [[difad3_mod.f]], [[dwmax_mod.f]], [[oldrot_mod.f]], [[oldrot2_mod.f]], [[oldphy_mod.f]], [[mdphy_mod.f]], [[rotder_mod.f]], [[roten_mod.f]], [[taukh_mod.f]], [[temp_mod.f]], [[temp2_mod.f]], [[tridi_mod.f]], [[vfact_mod.f]].

**Angular-momentum loss and mass loss.** Magnetic braking by winds (with the convective overturn time it needs), disk locking, and mass loss or accretion. [[mwind.f]], [[cowind.f]], [[mcowind.f]], [[wind.f]], [[amcalc.f]], [[gettau.f]], [[taucal.f]], [[tauint.f]], [[tauintnew.f]], [[massloss.f]], [[mdot.f]], [[disk_mod.f]], [[ovrtrn_mod.f]], [[masschg2_mod.f]].

**Numerical utilities.** Interpolation, splines, quadrature and linear solvers, most of them from Numerical Recipes or published algorithms. [[interp.f]], [[inter3.f]], [[intrp2.f]], [[xrng4.f]], [[locate.f]], [[polint.f]], [[cspline.f]], [[splinc.f]], [[splinj.f]], [[splint.f]], [[splintd2.f]], [[kspline.f]], [[ksplint.f]], [[osplin.f]], [[meval.f]], [[spline.f]], [[cases.f]], [[choose.f]], [[search.f]], [[slopes.f]], [[splin_mod.f]], [[boole.f]], [[bandw.f]], [[ctridi.f]], [[simeqc.f]], [[ludcmp.f]], [[lubksb.f]].
