# Pages alex06tab.f to envint.f

Round 1, Oct 25, 2026, by Claude, against the code at YREC `rp_1`. Each finding gives its kind (wrong, missing, unclear, format), the text and the proposed fix; "Revised" says what was applied.

## alex06tab.f

1. Unclear. "for $N_X = 9$ values of $X$ (0 to 0.9, then a last set at $X = 1 - Z$)": the 9 are eight values 0 to 0.9 plus the set at $1-Z$ (`XXG06(9) = 1.0` stands for it). Fix: say so.

Otherwise checked against READALEX06 and GETALEX06: the grid, the indexing, the stencils and the three questions hold.

Revised: the nine values of $X$ explained (eight plus the set at $1-Z$, `XXG06(9) = 1.0`).

## alfilein.f

1. Missing. SETUPS calls ALFILEIN only when `KTTAU = 4` (Allard atmospheres; the comment there says they are used instead of Kurucz below 10,000 K). Fix: add to "Who calls it".
2. Wrong (incomplete). Question 3 speaks only of $\alpha$; [Fe/H] also has two tolerances: records are kept when $|\Delta[\mathrm{Fe/H}]| \le 10^{-5}$, then the second pass drops those with $|\Delta| \ge 10^{-6}$, so a record between the two is counted in pass 1 (its $T_\mathrm{eff}$, $\log g$ enter the grid) but never stored. Fix: widen the question.

Revised: the call under `KTTAU = 4` added; question 3 widened to [Fe/H].

## alprint.f

No change: correct.

## alsurfp.f

1. Missing. What the callers do with `LAlFail`: [[envint.f#ENVINT|ENVINT]] switches to a gray atmosphere (`KTTAU = 0`, `LTTAU = .TRUE.`); [[massloss.f#MASSLOSS|MASSLOSS]] ("experimental code … llp 06/15/2009") does not test it and uses `AT`, `AP` at once. Fix: state it under "How it fits", and make question 2 concrete (MASSLOSS).
2. Missing. The header comment says the print goes to `ISHORT` and `IMODPT`, and that a point outside the table ends the program; the code writes to `ISTOR`, and only stops below the table. Fix: add to question 3.

Revised: what ENVINT and MASSLOSS do with `LAlFail` added; questions 2 and 3 made concrete.

## altabinit.f

No change: correct (the format error of question 2 and the four widths of question 1 checked).

## alx8th.f

1. Unclear / settled. Question 1 asks whether any routine reads `IX`. None does: YALO3D only declares it, and ALXTBL only sets its DATA value. Fix: state this in the note, and turn the question into a design point (can `IX` be local?).
2. Missing. YALO3D uses table 8 only when its $X$ equals `XE` (within $10^{-8}$). Fix: one clause.

Revised: question 1 settled (YALO3D sets `IX` itself before each use; ALXTBL only gives it a DATA value) and turned into a design point; the `XE` test added.

## alxtbl.f

1. Wrong question. Question 2 (exact comparison of $X$, $Z$ read from the file with DATA values): a formatted read into REAL*8 and a `D0` constant both round the same decimal to the nearest double, so the test is reliable. Fix: drop it.
2. Missing question. The header says the routine generates entries "at either one or two fixed values of Z", but it builds one (`ZALEX1`); `ZALEX2` survives only in comments elsewhere. Fix: add as the new question 2.

Revised: question 2 replaced by the one on `ZALEX2`.

## alxztab.f

No change: correct (stencil boundaries checked: the last four tables are used from $Z \ge 0.06$).

## amcalc.f

1. Settled. Question 1 (units of `SMASS`): [[mdot.f#MDOT|MDOT]] updates it as `SMASS + DELM/CMSUN`, and COWIND's header says "stellar mass (solar units)". Fix: state it; drop the question.
2. Wrong question. Question 2 (mixed precision of `10.**BL`): `10.` is exact in single precision and is promoted to double before the power, so nothing is lost. Fix: drop it.

Revised: `SMASS` in solar masses stated; questions 1 and 2 dropped.

## bandw.f

1. Unclear. "A pivot smaller than $10^{-20}$ … stops the run (`STOP 999`), after printing the row": for the last row it stops without printing. Fix: a clause.

Revised: the clause on the last row added.

## blkdta000.f

No change: correct.

## boole.f

No change: correct.

## bsrotmix.f

1. Missing. The update of the stored differences: in Neville's step $c_j$ is replaced by the previous correction (`HCOMPI(K1) = HCOMPE` before the update). Fix: add to step 3.
2. Wrong. Question 2 says BSSTEP "reads its own [tolerance] from `/INTPAR/`"; BSSTEP gets `EPS` as an argument, from ENVINT, which takes it from `STOLR0` in `/INTPAR/`. Fix: reword.

Revised: the update of $c_j$ added; question 2 reworded.

## bsstep.f

1. Missing. The derivative routine `DERIV` is [[qatm.f#QATM|QATM]] (atmosphere) or [[qenv.f#QENV|QENV]] (envelope), passed by ENVINT. Fix: add.
2. Missing. `IMAX` and `NUSE` are also in the `PHYSICS` namelist, so a run can change them. Fix: add.
3. Wrong. Question 2 says the loop may hang; with the test on `X` (about 0.7) it stops once $H$ falls below about $10^{-16}X$. Fix: merge into question 1.

Revised: `DERIV` (QATM, QENV) and the namelist `IMAX`, `NUSE` added; question 2 merged into question 1.

## bursmix.f

1. Wrong. Steps 1 and 5 say $X$ and $Z$ are restored to "their values from the start of the routine"; these are the values the caller's full step already produced (the input `HCOMP`), not those at the start of the time step. Fix: reword; question 1 likewise.
2. Missing question. `HCOMPP` (the start-of-step composition in `/OLDMOD/`, read by CRRECT, KEMCOM and others) is overwritten during the substeps and left at the end-of-step composition, for all species, although the comment says it is overwritten "temporarily". GETW also overwrites `HCOMPP` for species 12–15 elsewhere. Is the end state intended?
3. Settled. Question 2 (`ECOD2`, `EM`, `IBEG`, `IEND`): NDIFCOM sets them (through MIXGRID) when `LOK` is true, and reads them as they are when `LOK` is false. Fix: make the question concrete on `LOK` (passed from GETW, set by SECULR).
4. Settled. Question 3: ROTMIX does gravitational settling (MICRODIFF or GRSETT, if `LDIFY`). Fix: state it; drop the question.
5. Missing. GETW calls BURSMIX only when `LINSTB`, not `LALLCZ` and `LBURS`. Fix: add.

Revised: the restored values reworded (steps 1 and 5, question 1); the `HCOMPP` question added; question 2 made concrete on `LOK`; settling in ROTMIX stated and question 3 dropped; the call conditions added.

## calcad.f

1. Missing. Question 1 (step sizes not restored): [[wrtmod.f#WRTMOD|WRTMOD]], whose code the comment says CALCAD copied, does restore them (`ATMBEG = ABEG0`, …). Fix: add, which sharpens the question.
2. Unclear. Question 7: `JENV = M` is also exactly the case in which no convection zone is found (`TCZ` needs `JENV < M`), so the spot correction applies only to stars for which `TCZ = 0`. Fix: say so.

Revised: WRTMOD's restore added to question 1; question 7 sharpened.

## cases.f

No change: correct.

## ccoeft.f

1. Wrong. "on an evenly spaced grid in radius": MIXCOM passes `DCHI` as `DR`, the spacing of the grid in the coordinate $\chi$ built by [[getgrid.f#GETGRID|GETGRID]] and [[mixgrid.f#MIXGRID|MIXGRID]]; the comments about radius and cm are older than that grid.
2. Wrong. The solver is [[ctridi.f#CTRIDI|CTRIDI]] (MIXCOM calls only that one), not "TRIDIA or CTRIDI".
3. Settled. The question on $4\pi\rho r^2$: [[codiff.f#CODIFF|CODIFF]] includes $4\pi$ in `COD2`, and MIXGRID multiplies the coefficient by $\rho r^2\,d\chi/dr$, so `COD` is $4\pi\rho r^2 D\,d\chi/dr$ and the scheme is the mass-conserving one. Fix: state it; replace the question with one on the outdated comments (radius, cm, "angular momentum" in the boundary comment).

Revised: the grid in $\chi$, the solver CTRIDI and the mass-conserving coefficient stated; the question replaced by one on the outdated comments.

## checkc.f

1. Wrong. "`AMUM` … read by CODIFF, GETW, MIXCZ and others": CODIFF does not read it. The readers are [[vcirc.f#VCIRC|VCIRC]], [[setupv.f#SETUPV|SETUPV]] (the $\mu$ gradient), [[getw.f#GETW|GETW]] and [[midmod.f#MIDMOD|MIDMOD]].
2. Missing. On the first anomaly that is not repaired, the routine jumps to the end: $\mu$ is not recomputed for that call. Fix: a clause.

Revised: the readers of `AMUM` corrected; the jump on an unrepaired anomaly added.

## checkj.f

No change: correct (the five tasks, the tolerances and the questions checked).

## codiff.f

1. Settled. Question 2: CHECKJ's print reads `HLE` (column "LENGTH"), but that print is switched off. Fix: reword.
2. Settled. Question 3: VCIRC sets `VMU = 0`; its comment says the $\mu$ terms were replaced by $(\nabla + \nabla_\mu - \nabla_\mathrm{ad})$ and `IMU` is kept "for later use". `FMU` and `IMU` are still namelist inputs, unused. Fix: state it; ask whether to remove them.
3. Settled. Question 4: no routine sets `COD(1)` or `COD2(1)`; the readers start at element 2 (MIXGRID from `COD2(IBEG+1)`). Fix: reword as a check.

Revised: questions 2, 3 and 4 reworded as settled.

## convec.f

1. Wrong. Question 1 says the index error (`MRZONE(1,2) = M` for the top radiative region) affects "stars with a convective core and a radiative envelope". In that case `NRZONE` is 1 when the line runs, so `MRZONE(1,2)` is the right element. The error bites only when the top region is the second or a later one (a radiative surface with at least two radiative regions, e.g. a radiative core, a thin convection zone and a radiative surface). Then the first region's top becomes `M`, so [[mix.f#MIX|MIX]] burns the shells of the zones above shell by shell (as radiative) before treating each zone as a unit, and ROTMIX and MIDMOD treat them as radiative too (OVROT, which sets the convective flags last, is not affected). Fix: say so; note that KC's 2025-05-30 check `I .GT. 0` in [[ovrot.f#OVROT|OVROT]] loops over the same `MRZONE` (possibly related).
2. Wrong. Question 2 is garbled ("`NZONE` is set, but `MXZON0` is"). On the fully convective path `NZONE`, `NZONE0` and `MXZON0` are all set (one zone, 1 to `M`); only `MRZONE` is left as it was, with `NRZONE = 0`, and overshoot and merging are skipped. All readers loop `1, NRZONE`, so nothing reads `MRZONE`. Fix: state it under the method; drop the question.
3. Missing. The readers of `MRZONE`, `NRZONE`: MIX, [[ovrot.f#OVROT|OVROT]] (sets `LCZ`), [[rotmix.f#ROTMIX|ROTMIX]] and [[midmod.f#MIDMOD|MIDMOD]]. Fix: add to the outputs.
4. Unclear. "more prints TOO MANY MIX ZONES": the message is printed as soon as the 11th zone is stored, whether or not more follow. Fix: reword.

Revised: question 1 corrected (when the index error bites, its effect on MIX, the possible link to KC's OVROT check); the fully convective path stated and question 2 dropped; the readers of `MRZONE` added; the zone limit reworded.

## crrect.f

1. Missing. The early return: if the boundary condition was recomputed (`LSBC`), the triangle did not flip (`LFLP` from SURFBC is false) and the model had converged at the previous level (`LFINI`), the routine returns before iterating. Fix: add as a step.
2. Missing. With `LDH` (`/DEBHU/`), the surface composition for the Debye–Hückel correction (`XXDH`, `YYDH`, `ZZDH`, `ZDH(1:3)`) is set from shell `M` before SURFBC. Fix: one clause in step 1.
3. Unclear / sharpened. Question 5 (local `JCORE`, `JENV`): `JENV` is also passed to [[coefft.f#COEFFT|COEFFT]], which uses it (with entropy terms and mass gain, `LMDOT` and `DMDT0 > 0`) to choose the shells whose $\log P$, $\log T$ changes get extra terms. At levels 1 and 2 MIX is not called, so COEFFT gets the value saved from an earlier call (SAVE), or an unset value at the first call. Fix: make the question concrete on this.
4. Missing. KC's changes: `MODEL` was also dropped from the call to COEFFT (2025-05-31). Fix: add.
5. Unclear. Question 2: "in the outer layers ($L > 1\,L_\odot$) … in the core": the switch is at $L = 1\,L_\odot$ (`HL` is in solar units), wherever that falls; in a star fainter than the Sun the test is absolute everywhere. Also the first shell enters with $|\delta L|$ alone. Fix: reword.
6. Missing. The residual test (question 3) prints `ITDONE+1` as the iteration count but returns without incrementing `ITDONE`. Minor; add to question 3.

Revised: the early return and the Debye–Hückel composition added to the method; question 5 made concrete on `JENV` in COEFFT; questions 2 and 3 sharpened; KC's change to the COEFFT call added.

## engeb.f

1. Wrong. "`QS0E`, `QQS0EE` and … `FO16`, `FC12` (`/CROSS/`, set in PARMIN from the namelist)": [[remap.f#REMAP|REMAP]] sets them (all 1, then, with `LNEWNUC`, from the namelist's cross-sections and their derivatives, relative to Solar Fusion I); PARMIN only declares `/CROSS/`. Fix: name REMAP.
2. Missing question. In the pp/CNO loop, `DRATT` differentiates the bracket $R_1$ without the factors `QS0E(I)`, `QQS0EE(I)` on the $Q_3$, $Q_4$, $Q_5$ terms, so with `LNEWNUC` and factors other than 1 the temperature derivative does not match the rate. Fix: add a question.
3. Missing (question 3). In reaction 8 ($^{13}$C($\alpha$,n)) the derivative terms `A2*(9.373*T9M1-1.5)` … lack the factor $T_9^{-3/2}$ that multiplies `A2`…`A5` in the rate. Fix: add to question 3.
4. Unclear. Question 8: "`SUM1` $\le 10^{-12}$ zeroes everything": it zeroes `PEP`, `PET` and the `EG` array (so the fluxes), but `SUM1` itself and the `DG` array (so `EPP1`, `ECN`, …) are kept. Fix: say so.
5. Missing. Step 5 does not state the deuterium cap: in the convective envelope (`IU` $\ge$ `JCZ`) and when `TAUCZ` $> 1$, the rate per unit $X$ is limited so that $r X \le (N_A/A_D)/\tau_\mathrm{cz}$. Fix: one sentence.
6. Missing (question 6). On the low-temperature path `RHO`, `T9` and the $^7$Be rates are also stale, and with `LSNU` they enter `FLUX(3)` and `BE7MASSFRACTION`. Fix: add a clause. (Checked: main.f skips shells with $\log T < 6$; the `IU` of question 7 is never set in main.f, line 388.)

Checked and right: the screening formulas, the eq. 3.14 rate form, the branchings, $Q$ values, `C21`, the Itoh-branch bug (question 1), the relative-derivative point (question 2), reaction 10's missing $T_9^{-2/3}$, the deuterium rate and derivative (question 4), and the MHP 5/90 comment (question 5).

Revised: REMAP named for `/CROSS/`; the deuterium cap added to step 5; questions 3, 6 and 8 sharpened; question 9 (`QS0E`, `QQS0EE` missing from `DRATT`) added.

## envint.f

1. Wrong. Question 1 says `ENVL` "is wrong after the reversal". Every entry of `ENVL` is set to `B` (the luminosity is constant in the envelope), so the broken swap changes nothing now; it would matter only if `ENVL` ever varied. Fix: say so; keep it as a latent bug.
2. Settled / sharpened. Question 2 (`ENVG`): [[taucal.f#TAUCAL|TAUCAL]] computes `HG` at the two points it needs from `HS1` when `LROT` is false; with rotation it uses `HG` as passed, and ENVINT's `ENVG` is never filled. Fix: make the question concrete on rotating models.
3. Settled. Question 3 (mixed mass units): TAUCAL uses `ENVS2` only as weights in an average of the convective velocity (`UMER/DENOM`), so its unit cancels; `ENVS1` (grams) is what enters $g$. Fix: state it; drop the question.
4. Missing. The step limit at `PLIM` applies only when `LSBC` is false (`LTEST`); and `PS(IE)`, `TS(IE)`, `RS(IE)` and `ESTORE`, `ISTORE` are set only when `LSBC` is true. Fix: add.
5. Missing. The gray start for Krishna Swamy uses $T^4 = \tfrac34 T_\mathrm{eff}^4 \times 0.550$ (the factor at $\tau \to 0$), not the Eddington one. Fix: a clause.
6. Minor. `LDERIV` is set by the pulsation test and then forced to `.TRUE.` just after (line 137). Fix: add to Design.

Revised: question 1 corrected (harmless now); question 2 made concrete on rotating models; question 3 settled and dropped (stated under the method); the `LSBC` conditions, the Krishna Swamy start and the forced `LDERIV` added.

## coefft.f

1. Unclear. "the energy fractions `SEG`": only `SEG(1:5)` are fractions of `SESUM` (the five nuclear terms); `SEG(6)` (neutrinos) and `SEG(7)` (gravothermal, `HHC`) are rates in erg g$^{-1}$ s$^{-1}$; with rotation `FRACNUC` $= (\mathtt{SESUM} - \mathtt{SEG(6)} - \mathtt{SEG(7)})/\mathtt{SESUM}$. Fix: say so.
2. Missing. The point index: COEFFT passes `IU = IM` to ENGEB, so here the rates `HR1`… are stored at the right point (unlike main.f's call, see [[engeb.f#ENGEB|ENGEB]] question 7). Fix: a clause.
3. Missing. `JENV` comes from CRRECT, which has it from MIX only at levels 3 and 4 (CRRECT's question 5). Also "points above `JENV`" is "at and above" (`IM` $\ge$ `JENV`). Fix: reword.

Otherwise checked: the structure equations and their derivatives, $\epsilon_\mathrm{grav}$, the central conditions, $\Gamma_1$, `TLUMX`, KC's changes and the five questions hold.

Revised: `SEG` and `FRACNUC` explained; the index `IU = IM` and where `JENV` comes from added.

## dburn.f

1. Wrong. Question 1 says DBURN's accretion weighting mixes units because `FMASSACC` is a fraction. It is not: [[mdot.f#MDOT|MDOT]] sets `FMASSACC = DELM`, with `DELM = DMDT*CMSUN*DELTS/CSECYR`, the accreted mass in grams (and `SMASS + DELM/CMSUN`). So DBURN weights grams by grams, as it should; the comment ("DMDT*DT/original CZ mass") is out of date, and it is [[dburnm.f#DBURNM|DBURNM]]'s weighting, `(XH2NO + XH2NA*FMASSA)/(1 + FMASSA)`, that treats a mass in grams as a fraction. Fix: rewrite question 1 (the outdated comment; the problem is in DBURNM).
2. Missing question. MDOT sets `FMASSACC` only when mass is gained (`DELM > 0`). The accretion branch of the burning (`LMDOT .AND. IEND.EQ.M`) does not test `DMDT0 > 0` (the zeroing test above it does), so with mass loss it mixes in a stale `FMASSACC` from an earlier accreting step (or 0). Fix: add.
3. Wrong. "Who calls it: MIX, for each radiative shell and each convection zone above the burning cut-off": MIX calls DBURN only with `LEXCOM` (the extended composition, 15 species); the cut-off `TCUT(1)` stops the loop over radiative shells, but every convection zone is passed. Fix: reword.
4. Minor. Step 2: on zeroing, the routine returns at once, leaving `X` and $^3$He as they are in `HCOMP`. Fix: a clause.

Revised: question 1 rewritten (`FMASSACC` is in grams; the comment is outdated and DBURNM's weighting is the suspect one); question 4 (accretion branch under mass loss) added; the call condition `LEXCOM` and the cut-off corrected; the early return stated.

## dburnm.f

1. Wrong. "the accreted fraction is $f_a$ = `FAC2*FMASSACC` … a weighting by fractions": `FMASSACC` is the accreted mass in grams ([[mdot.f#MDOT|MDOT]] sets it to `DELM`), so $f_a$ is a mass in grams, and $(X_{D,\mathrm{old}} + f_aX_{D,\mathrm{acc}})/(1+f_a)$ gives the accreted matter nearly all the weight; DBURN weights by the zone's mass `SUMM` instead. This looks like a bug. Fix: correct the method and make it a question of its own.
2. Settled. "`DTT = DT*1.0D-9/CSECYR`: from seconds to Gyr, probably": MIDMOD's `DT` is in seconds (`FAC2 = DT/DELTS`). Fix: drop "probably".
3. Missing. As in DBURN, the accretion branch does not test `DMDT0 > 0`. Fix: mention in question 1 (two copies).

Revised: the accretion weighting corrected in the method and made question 2 (an apparent bug); `DT` in seconds stated; the missing `DMDT0` test added to question 1.

## deutrate.f

1. Wrong. "MIX, for each point where deuterium exceeds $10^{-11}$": MIX tests the surface deuterium once (`HCOMP(12,M)`, or the larger of it and the accreted `COMPACC(12)` when accreting), then calls DEUTRATE for every point from the centre out until $T$ falls below `TCUT(1)`. Fix: reword.
2. Settled (probably). Question 2 (units of `TAUCZ`): [[taucal.f#TAUCAL|TAUCAL]] forms it as a length over a convective velocity (`CZWIDE/CVEAVG` or `PSCA/CVEL`), so it is in seconds if the code's CGS units hold, and the cap is consistent. Fix: state it with "probably"; keep a short check.
3. Unclear. The `###` summary says "per Gyr, probably", while the explanation derives it. Fix: drop "probably" there, keep the inference in the explanation.

Checked: the rate, the factor $N_A/2$, `C21`, the cap and question 1 hold; this is the same $T_9^{+2/3}$ as in ENGEB (its question 4).

Revised: the call condition corrected; question 2 answered with "probably" (seconds, from TAUCAL); "probably" dropped from the summary; the link to ENGEB's same power added.

## entime.f

No findings (the formula, the bounds, the inputs, the caller HTIMER and both questions checked).

No change

## chkcal.f

1. Unclear. "for the next three kind cards, the new $X$ (`RESCAL(2,·)`, `XENV0A`) … $Z$ (`RESCAL(3,·)`, `ZENV0A`)": `RESCAL` is set only for card $N+1$ (the rescaling card); `XENV0A`, `ZENV0A` and `CMIXLA` for $N+1$ to $N+3$. Fix: say so.
2. Missing (question 3). The convergence test uses $Z/X$ only when `LCALSOLZX` and `CALSOLZX > 0`; the update of $Z$ tests only `LCALSOLZX`, so a target of 0 would set $Z = 0$. (The default target is 0.02292, in PARMIN.) Fix: add a clause.

Otherwise checked: the convergence test, the Newton step and its formula, the derivatives, the call from main.f (`MOD(NK,3).EQ.0`) and the questions hold.

Revised: which cards get `RESCAL` and which the other values stated; question 3 extended to the `CALSOLZX > 0` test.

## chkscal.f

1. Missing question. `ALRI`, `BLI`, `AGEI` (the previous model) are set to start values only once, by [[setscal.f#SETSCAL|SETSCAL]] (`ALRI = 0`, called once before the kind cards), and are not updated at the crossing. The first comparison of each later run (its second model; main.f skips the first, only setting `TEFFI`, which nothing reads) is thus made against the model just before $R_*$ in the previous run. If the runs start with a radius above $R_*$ (pre-main sequence) and the earlier run crossed $R_*$ on the way up, a false crossing is found at once, and $L$ and the age are interpolated between two runs. Fix: add the question.

Otherwise checked: the radius formula, the crossing test, the interpolation, the found case, the first step and the secant step hold.

Revised: question 5 (the previous model carried across runs) added.

## choose.f

1. Missing. Case 1 is also taken when $s = 0$ and $m_1m_2 < 0$; and when an end slope is within `EPS` (relative) of $s$, the routine skips the "tangents meet" test and goes to case 2 or 3. Fix: add both.
2. Missing. MEVAL is called by [[osplin.f#OSPLIN|OSPLIN]]. Fix: name it, for the chain.

Otherwise checked: the cases, the modification and the two questions hold.

Revised: the two missing case-1 and tolerance rules added; OSPLIN named.

## condopacp.f

1. Settled. Question 1 (are CONDOPACPINT's limits inside the table?): the tables in `input/opacity/conductive/potekhin/` (`condall.d`, `condall06.d`) span exactly $3 \le \log T \le 9$, $-6 \le \log\rho \le 9.75$ (64 steps of 0.25) and $Z_\mathrm{ion}$ from 1 to 60, so the guards equal the table's edges. But HUNT returns $N$ for a value equal to the last grid value, so a point at exactly $\log T = 9$ or $\log\rho = 9.75$, which the guards (`.LE.`) let through, stops the run. Fix: state the ranges and turn the question into this edge case.
2. Unclear. HUNT "returns 0 or $N$ outside the table": also $N$ at the last value itself. Fix: add.

Revised: the table's ranges stated; question 1 turned into the edge case at the upper limits; HUNT's return at the last value added.

## condopacpint.f

1. Missing question. The extrapolation in step 3 also has the wrong sign of the step: `OCL = OCL + QODC*(-6.0D0-DL)` adds slope × $(-6 - \log\rho)$, while a linear extrapolation from $\log\rho = -6$ down to $\log\rho$ adds slope × $(\log\rho + 6)$. Together with question 1's sign, the extrapolated opacity is doubly suspect. Fix: add to question 1.
2. Missing. Step 3 is reached only for $\log T < 4$ (it needs $\log\rho < -6$ and $\log\rho - 3(\log T - 6) \ge 0$), and its $\partial\log\kappa/\partial\log T$ is hydrogen's alone at $\log\rho = -6$. Fix: a clause.
3. Missing. When `LCONDO` stays false, the routine leaves `OC` $= 10^{9.9998}$ and sets `QODC = QOTC = OC`; GETOPAC then either returns before using them ($\log T < 4.2$ or low density) or overwrites them with Hubbard–Lampe. Harmless; one clause.
4. Missing (link). The tables span exactly the guards' range; see CONDOPACP's question 1 for the upper edges. Fix: a pointer.

Revised: the reversed extrapolation step added to question 1; the region of step 3, its $T$ derivative, the fallback values and the pointer to CONDOPACP added.

## cowind.f

1. Settled. "they go to DADCOEFT as arguments, probably through MCOWIND's caller": [[seculr.f#SECULR|SECULR]] calls MCOWIND and passes `WIND1`, `WIND2` to [[dcoeft.f#DCOEFT|DCOEFT]] or [[dadcoeft.f#DADCOEFT|DADCOEFT]], where the surface boundary uses their mean, $-\tfrac12(\mathtt{WIND1}+\mathtt{WIND2})\,I$. Fix: state it.
2. Unclear. Step 2's $\log R$ omits $\log L_\odot$: `BL` is $\log L/L_\odot$, and the code adds `CLSUNL`. Fix: write $\log R = \tfrac12(\log(L/L_\odot) + \log L_\odot - \log 4\pi - \log\sigma - 4\log T_\mathrm{eff})$.

Revised: where `WIND1`, `WIND2` go (SECULR, DCOEFT, DADCOEFT) stated; the radius formula corrected.

## cspline.f

No findings (the recurrence, the natural-spline switch at $0.99\times10^{30}$, the five callers and the questions checked).

No change

## ctridi.f

1. Missing. `/TRIDI/` is shared with the angular-momentum solver as well: [[dcoeft.f#DCOEFT|DCOEFT]] fills the same arrays for [[tridia.f#TRIDIA|TRIDIA]] (and GETQUA uses them), so the block is reused between the two problems. Fix: one clause.
2. Missing (question 1). The first pivot $\beta_1 = b_1$ is not tested at all (the test starts at $j = 2$). Fix: add.

Revised: the shared use of `/TRIDI/` and the untested first pivot added.

## dadcoeft.f

1. Unclear. Step 7's "effective circulation velocity $V_\mathrm{tot}$": the mixing uses `VTOT2`, in which the term from `ECOD4` (which includes the shear and GSF coefficients) is replaced by its circulation part alone (`V1E`, from $E_{2a} + E_{2b}$; zero where `ECOD4` $\le 0$), so that shear and GSF are not counted twice. Fix: say so.
2. Minor. `/DEUTER/` is included but not used. Fix: add to the Design note.

Otherwise checked: the band layout, the coefficients `ECOD3`, `ECOD4`, the wind term (`FXX = DT/DT0`), the conservation rescaling, the cuts (`STOP 111` after 5), the `/PMMWIND/` question and the size limit hold.

Revised: `VTOT2` explained in step 7; the unused `/DEUTER/` noted.

## dcoeft.f

1. Wrong. "on the even grid in radius": [[rotgrid.f#ROTGRID|ROTGRID]] sets `DR = DCHI`, the spacing of the even grid in the coordinate $\chi$ (as for CCOEFT in round 1). Fix: say $\chi$.
2. Settled. Question 3 (geometric factors in `ECOD`): ROTGRID multiplies `ECOD` by $\rho r^2\,(d\chi/dr)$ and by $I/\Delta m$ of the shell (its comment: "product of $\rho r^4$ by $d\chi/dr$ … factor of $I/MR^2$"), with $4\pi$ already in CODIFF; with `LDIFAD` it also adds the composition coefficient `ECOD2` to `ECOD4`. Fix: state it; drop the question.
3. Missing. The advective terms are in conservative form (each interface's flux $\pm\tfrac12\Delta t\,\mathtt{ECOD3}_i(\Omega_{i-1}+\Omega_i)/I$ enters both neighbouring rows), with none beyond the centre and the surface. Fix: a clause.

Revised: the grid in $\chi$ stated; question 3 settled (ROTGRID's factors) and dropped; the conservative form of the advective terms added.
