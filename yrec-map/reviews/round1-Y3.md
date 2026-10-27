# Pages gmass.f to mhdst1.f, and index.md

Round 1, Oct 25, 2026, by Claude, against the code at YREC `rp_1`. Each finding gives its kind (wrong, missing, unclear, format), the text and the proposed fix; "Revised" says what was applied.

Following the review brief; checked also against `callgraph.json` and with `grep`. This is the only round, so there are no earlier findings to check.

## gmass.f

1. **Wrong.** Question 3: "`EION` and `AMAS` are dimensioned 7, `EION(7)` is never set; … `ANUM`, `EION` could be dimensioned 6." `ANUM` is already dimensioned 6, and `AMAS(7)` is used (hydrogen). Only `EION(7)` (and the caller's `FRAC(7)`) are unused, which is trivial. Fix: drop the question.
2. **Missing.** What `ESAC` does with the results. Fix: one line: `ESAC` passes `AMOLES` and the mean mass `TMASS` to `RADSUB` and uses them to scale its tabulated quantity.

Revised: question 3 dropped; the line on what `ESAC` does with `AMOLES` and `TMASS` added.

## gmass01.f

Checked: the values of `EION`, the sum without electrons, the caller (`ESAC01`, which declares `moles` as `REAL*8`). Nothing to fix.

No change.

## gmass06.f

Checked: identical to `gmass01.f` apart from the name. Nothing to fix.

No change.

## grsett.f

1. **Missing question (apparent bug).** In the implicit loop, `EX_H(I)` for `I = 2..NPT` is the change at the midpoint between points `I-1` and `I`, but [[get_imp_diffco.f]] adds `EQCOD2X_H(I)*EX_H(I)` to `ECOD2_H(I)`, the coefficient at the midpoint between points `I` and `I+1` (as its matrix shows: `A(I)` uses `ECOD2_H(I-1)`, `C(I)` uses `ECOD2_H(I)`). So the correction is applied one midpoint off, and `ECOD2_H(1)` gets the stale `EX_H(1)` left by `LAX_WENDROF1`. Fix: add a question.
2. **Missing.** The implicit system's coefficients, as an equation. Fix: give $(1+\alpha_i(D_{i-1/2}+D_{i+1/2}))X_i - \alpha_i D_{i-1/2}X_{i-1} - \alpha_i D_{i+1/2}X_{i+1} = X'_i$ with $D$ = `ECOD2_H`.

Revised: question 4 (the correction one midpoint off) and the implicit system as an equation added.

## gtlaol.f

1. **Wrong.** "`TOLLAOL` is 10 by default (`PARMIN`), so $\delta \approx 2.30$". `TOLLAOL` is only a namelist variable read by `PARMIN`; no file in `src/` (nor the docs or examples) gives it a value. Fix: say it has no default in the code, so it must be set in the namelist; if left at zero, `LOG(0)` would make the margin $-\infty$ (or fail). Rephrase question 1 accordingly.

Revised: `TOLLAOL` has no default in the code; method and question 1 rephrased.

## gtlaol2.f

Checked: line-for-line copy of `GTLAOL` on `NWLAOL2`/`SLAOL2`; `SLAOL` and `ZRAMP` unused; caller `GETOPAC` with the linear $Z$ interpolation. Nothing to fix.

No change.

## gtpurz.f

1. **Unclear.** "when $Z$ is above the range of the normal tables". `GETOPAC` calls it when $Z > 0.1$ and $\log T > 7.7$ (the comment: Z > 0.10, T > 5 × 10⁷ K), and interpolates linearly in $Z$ between the normal table at `ZIT` and $Z = 1$. Fix: state the condition.

Revised: the calling condition ($Z > 0.1$, $\log T > 7.7$) and the linear interpolation in $Z$ stated.

## hpoint.f

1. **Wrong.** Question 2: "the loop jumps past the convection-zone, overshoot and fine-zoning flags". The convection-zone edges and the H-shell base are flagged before the loop; only the overshoot base `JOS` and the fine-zoning base `JFINE` are skipped. Fix: correct the question.
2. **Wrong.** "25 blocks in all": HPOINT declares 24. Fix: 24.
3. **Wrong.** `ENTROP` described as "the previous step's $T$, $P$, $L$, $r$": it holds their rates of change (`HTT0` = $d\log T/dt$, …), which main.f uses for the first guess. Fix.
4. **Unclear.** `OLDMOD`: after HPOINT, `HPO`, `HTO`, `HRO`, `HLO`, `HDO`, `HSS` hold the start-of-step model on the new grid (they are the `OSPLIN` outputs). Fix: say so.
5. **Missing question (apparent bug).** `MO = M` is set before the rezoning (old number of points), while `HLO` ends on the new grid with `MNEW` points. [[entime.f#ENTIME|`ENTIME`]] (called by `HTIMER` when `LTRIST`) reads `HLO(MO)` as the previous surface luminosity, which is the surface only if the number of points did not change. Fix: add a question (set `MO = MNEW` after the rezoning?).
6. **Missing question.** The overshoot base is found where $\log_{10}P - \log_{10}P_\mathrm{env} >$ `ALPHAE`, so `ALPHAE` is used as a depth in $\log_{10}P$, while main.f uses it as a fraction of $H_P$ (an overshoot of $\alpha H_P$ is $\Delta\ln P \approx \alpha$, i.e. $\Delta\log_{10}P \approx 0.43\alpha$). Fix: add a question.

Revised: all six findings applied (questions 2, 6, 7; 24 blocks; `ENTROP` as rates of change; `OLDMOD` on the new grid).

## hra.f

1. **Wrong.** "the code is already a plain Horner-like sum": it sums explicit powers (`TL2`, `TL3`, …), not Horner's scheme. Fix: say so.
2. **Missing.** How callers use it: `SETUPS` stores `HRAS = HRA(2/3)`, and `ENVINT`, `QATM` use $\log T = \log T_\mathrm{eff} + \mathrm{HRA}(\tau) - \mathrm{HRAS}$, i.e. the relation is normalised to $T = T_\mathrm{eff}$ at $\tau = 2/3$. Fix: add.

Revised: explicit powers, not Horner; the normalisation through `HRAS` at $\tau = 2/3$ added.

## hsolve.f

Checked the 2×2 surface system and the back-substitution line by line; correct. Nothing to fix.

No change.

## hsubp.f

1. **Wrong.** "the EOS call … has no effect on the result": `EQSTAT` returns `DL` (log density from $P$, $T$, $X$, $Z$; it is an output argument, set by `EQSTAT2`), and `PSCAHE` uses that `DL`, not `HD(JEDGE)`. So $\rho$ in $H_P$ is the EOS density. Fix: correct the method and question 1.

Revised: $\rho$ in $H_P$ is the EOS density (`DL`); method and question 1 corrected.

## lax_wendrof1.f

1. **Unclear (format).** The notation $\Delta X^{(i)}_{1/2}$ mixes index and midpoint. Fix: write $\Delta X_{i+1/2}$, with $F_1 = 0$, $m_1 = 0$ at the centre and $F_N = 0$, $m_N \to M$ at the surface.

Revised: notation $\Delta X_{i+1/2}$ with the boundary values.

## lax_wendrof2.f

Checked. Nothing to fix.

No change.

## main.f

1. **Wrong.** "main.f declares about 80 of them": it declares 60. Fix.
2. **Wrong.** "`ENTROP` (… with `HPOINT`, `CRRECT`)": `ENTROP` is shared with `HPOINT` only. Fix.
3. **Wrong.** Question 3: `GL` is set by `WRTOUT` (`GL = CGL + STOTAL - RL - RL`), and `LMIX`, `LOCOND`, `LATMO`, `LDERIV` are set by `COEFFT` (through `CRRECT`) before use; `QDT`, `QDP` are set by `STARIN`. Only `ZTOX` remains: in the Monte Carlo failure branch it is written before any assignment on the first pass (later passes see the previous value, through `SAVE`). Fix: reduce the question to `ZTOX` (and add that the failure branch prints `TCENTER`, `PCENTER`, `DCENTER` as logs, unlike the success branch).
4. **Wrong (small).** Step 13: "at least $10^{-3}$ of the age". `DELTS = MAX(DELTS0, 1.0D-3*DAGE*CSECYR)` with `DAGE` in Gyr gives $10^{-3}\times$ (age in Gyr) years, i.e. $10^{-12}$ of the age. Fix: describe what the code computes and add a question (units slip?).
5. **Missing question.** For He-flash runs the copy of the starting model to `ILAST` (`WRTLST`, comment: "timestep cutting requires a model stored in ILAST or it will crash") runs only if `LPUNCH`, which is false on the first kind card (and after `PUTSTORE`), and it passes `JCORE` before `FINDSH` has set it. Fix: add.
6. **Missing.** Step 3: `LAGE` also needs `MODEL ≥ 0`. Step 11 says rotational mixing "which `GETW` handles": this is a fact (GETW calls `LIRATE88`, `LIBURN`, `LIBURN2`), so cite it. The `ITROT` loop includes `MIXCZ` and the convergence test, not only level 4 and rotation. `CHKSCAL`'s success (`LPASSR`) jumps to label 200, skipping `PUTSTORE`. `TEFFI` is set and never used. Fix: add these.
7. **Missing.** The radius for the solar calibration: $\log(R/R_\odot) = \tfrac12[\log(L/L_\odot) + \log L_\odot - \log 4\pi - \log\sigma - 4\log T_\mathrm{eff}] - \log R_\odot$ (`RLL`). Fix: add the equation.
8. **Unclear.** "up to 15" calibration cycles: the counter starts at 1 and the loop ends when it reaches 15. Fix: say so. Question 6: `FZDIF` is a copy of `FHE`, so the one settling factor read is applied to metals only; `ZX(NN)` is read but only written out. Fix: add to the question.
Also checked: "now 5000, in every file" holds (the only "JSON=2000" is the comment itself).

Revised: all eight findings applied (60 blocks; `ENTROP` with `HPOINT` only; question 3 reduced to `ZTOX`; step 13 and question 7 on the floor; question 8 on `ILAST`; step 3, step 11, the `ITROT` loop, `CHKSCAL`, `TEFFI`; the `RLL` equation; `ICONV` and question 6).

## htimer.f

1. **Wrong.** Outputs: "`DELTSH` (= `DELTS`)". On the relaxation branch (`DELTS` < 0) `DELTSH` is not set (unless the final-age cut applies). Fix: say so.
2. **Missing.** `CT3`: `LPTIME` defaults to true in `PARMIN` (namelist), is reset by `REMAP` from `LSTRUCT_TIME`, and is read by `XTIME` and `YTIME`. Fix: add.
3. **Missing.** `SETT` also holds `END_DCEN`, `END_XCEN`, `END_YCEN` (stop criteria for central abundances, MHP 10/24), which is why the age cut tests `ENDAGE(NK)` > 0 as well as `LENDAG(NK)`. Fix: add.

Checked otherwise: the branches, the minimum, the 1 s guards, the `ENTIME` condition, the call sites in main.f (lines 464, 912; `DABS` at 908, negative step at 683), KC's changes. Questions are real.

Revised: findings 1–3 applied.

## kemcom.f

1. **Wrong.** Output: "`HCOMP` (elements 1–7, 9, 11, and 3 in one case)". Element 3 ($Z$) is always written: reset to $1-X-{}^3\mathrm{He}-Y$, or set to the zone's start-of-step mean `XSUM(3)`. Fix: say so.
2. **Unclear.** "If $X < 5\times10^{-7}$ at the zone's top": the test is on the previous model's $X$ (`HCOMPP(1,IEND)`), not the new one. Fix: say so.

Checked otherwise: all seven residuals and the 49 Jacobian entries against lines 138–203 (factors $A_k$, signs, column-major layout, diagonal at 1, 9, …, 49), the zeroing and diagonal shortcut, the convergence test, ¹⁸O, the callers (`MIX`, `ROTMIX`), `BURTOL` (shared with `PARMIN` only), the `HCOMPP` writers. Questions are real; question 5 (undivided step when the matrix is diagonal) looks like a real bug if the shortcut is ever taken with $J_{kk}$ far from 1.

Revised: findings 1–2 applied.

## ifermi12.f

No findings. Checked the formulas, the coefficients' use and the callers.

No change

## inter3.f

No findings. Checked the formulas, the coefficients' use and the callers.

No change

## interp.f

No findings. Checked the formulas, the coefficients' use and the callers.

No change

## intmom.f

No findings. Checked the series, `MOMI`'s arguments (`CON` = $5/(3G)$, `R0R`, `A`) and question 2 against `SOLID` line 62 (`DELW = DELJ/(CZI + WGUESS*CZQIW)`); the question stands.

No change

## intpol.f

No findings. Checked the interval search, the evaluation, the bounds and the callers.

No change

## intpt.f

1. **Unclear.** Method step 1: "the first temperature index `IT(1)` below `TL`". The loop leaves `IT(1)` at the *last* grid temperature below `TL`. Fix: say so, and give the clamp (`NT`−3).

Checked otherwise: the pressure brackets, the five `LIR` calls, the early `RETURN`, KC's changes. Questions 1–3 are real.

Revised: finding 1 applied.

## intrp2.f

No findings. Checked the formulas and the callers.

No change

## kspline.f

No findings. Checked the formulas and the callers.

No change

## ksplint.f

No findings. Checked the formulas and the callers.

No change

## kcsurfp.f

1. **Missing (question).** When a temperature's highest gravities are missing in the table (`IMINMAX2(J)` < `NGC`, set by `SETUPS`), the general search covers $\log g$ only up to `ATMGLC(IMINMAX2(J)-1)` (line 96); a $\log g$ between that and `ATMGLC(NGC-1)` falls through to the lowest four valid gravities, and one above `ATMGLC(NGC-1)` uses the top four entries, missing ones included (line 78). Fix: add as question 4.

Checked otherwise: the range check, the temperature and gravity branches (linear, `INTER3`, splines), `KP`/`JP`, and the COMMON sharers (`ATMPRT`: `ALSURFP`, `ENVINT`, `QATM`, `MASSLOSS`, `SURFP`; `ATMOS2C`: `ENVINT`, `PARMIN`, `SETUPS`; `FAC`: `SETUPS`, `SURFP`).

Revised: question 4 added.

## kurucz.f

1. **Wrong.** Question 1: "with two tables the second can be used where the first is not". `GETOPAC` (lines 48–50) calls `KURUCZ2` only after `KURUCZ` returned normally; `KURUCZ`'s `RETURN 1` jumps to label 100 past the call. So the missing test in `KURUCZ2` has no effect. Fix: rewrite the question as one on the hard-coded corner.

Checked otherwise: the row search, the cubic and its derivative, the retry, the alternate returns, the `INTPOL` calls, the COMMON sharers (`GKRZ`, `KRZ`: `SETKRZ`, `YKOEFF`; `INTPL2`: `YKOEFF`).

Revised: question 1 rewritten.

## kurucz2.f

1. **Wrong.** Same as `KURUCZ`'s finding 1: the missing corner test does not matter, since `GETOPAC` calls `KURUCZ2` only after `KURUCZ` passed it. The code otherwise differs from `KURUCZ` only in the COMMON names (checked by `diff`). Fix: say so in the method; drop question 1; keep the duplication question.

Revised: method, questions and `###` note corrected.

## liburn.f

1. **Wrong.** Step 3: "All points from the deeper of the two bases to the surface get the result." The loop runs from `MAXJ` = max(`JENV`, `JENV0`), the shallower base (line 411 of the file). Fix: "shallower" (question 3 already has it right).
2. **Wrong.** Step 2 and question 5: the loop exits where "a rate" is below $10^{-32}$; only the ⁹Be rate (start or end) is tested, and points with all three abundances below $10^{-24}$ are skipped. Fix.
3. **Missing (apparent bug).** Step 4: `DMASS = HSBEG - HSEND` is negative for a retreating zone (`HS1` = $10^{HS}$ grows outward), so `FRAD` lies in [−1, 0] and the rate extrapolates past the zone's rate. Also, with the sign fixed, the radiative rate gets the weight that the comment gives to the time spent in the zone. Same lines in `LIBURN2`. Fix: give $f$ explicitly; add question 7.
4. **Missing.** The bottom point's adjusted rates (`RLI6(JENV)` etc.) are left in `NEWRAT`; only `HS2(JENV)` is restored. `GETW` and `BURSMIX` copy them to `OLDRAT`. Fix: say so; add question 8.

Checked otherwise: the base offset, overshoot, substeps and `RATEXT`, the zone averages, accretion, `SAFEDIVEXP`, the COMMON sharers, the callers (main.f line 891, `GETW` line 350). Question 2 (`HRO` in line 107) is real. See also question 5, which affects the rates `LIBURN` uses.

Revised: findings 1–4 applied.

## lirate88.f

1. **Missing (apparent bug).** End-of-step rates seem never to be computed. main.f stores the starting model in `OLDMOD`, then `J` = 1 (main.f line 673, "beginning of the time step") fills `NEWRAT` from the same starting model, and `J` = 2 (line 889, "end of the time step") fills `OLDRAT` from `OLDMOD`. `GETW` (line 342) also calls `J` = 2 "at the end". The callers' comments fit the code only if the branches were swapped. Fix: add question 5.
2. **Missing.** The ⁶Li fit also differs from the commented old line in the $T_9^{5/3}$ coefficient (0.006 → 0.005), not mentioned. Fix: add to question 4.

Checked otherwise: the ⁷Li formula ($T_{9a}$, exponent 5/6), the scale factors, $\rho X$, the temperature cut and the zeroing.

Revised: questions 4 and 5.

## liburn2.f

1. **Unclear.** "skipping points with a rate below $10^{-32}$": only the ⁹Be rate is tested. Fix.
2. **Missing.** The `FRAD` sign problem and the unrestored bottom-point rates (see `liburn.f`, findings 3–4) are in the same lines here (282–291, 203). Fix: add to question 3.
3. **Unclear.** Question 2 suggests a difference from `LIBURN`; `LIBURN` also leaves its last loop at such a point. Fix: say so.

Checked otherwise: the geometric-mean rate (radiative and zone), the 30 cut, the callers and the COMMON blocks.

Revised: findings 1–3 applied.

## lir.f

1. **Unclear.** "Called by `INTPT` (twice …)": two call sites, but five calls per `INTPT` call (four rows in pressure, one in temperature). Fix.
2. **Unclear.** "the weight of the node nearest `Z`": the code corrects `A(K)` with `K` = 3 (the first node beyond `Z`) except near the ends; "closest" is the comment's word. Fix: say which node.

Checked otherwise: the scan, the on-node copy, the cubic weights, the linear branch, the silent error returns, KC's changes (the block IFs keep the arithmetic IFs' branches). `LIR1` has no caller.

Revised: findings 1–2 applied.

## ll4th.f

1. **Missing.** Callers: `SURFOPAC` calls `LL4TH` only when `LOPAL92` is set, and is itself called by `STARIN` as well as `HPOINT` (when the surface $X$ changes by more than $10^{-8}$). Fix.
2. **Unclear.** "`NEWOPAC` … shared by 17 units": 18 units declare it, so 17 others. Fix.

Checked otherwise: the $X$ index and clamp, the linear interpolation in $X$, the `NDSS` check, the spline per row, `ZENV4` = `ZOPAL1` (and `ZENV42` = `ZOPAL2`), the readers of `LLOT4`/`LLOT42` (`YLLO2D`, `YLLO3D` and their `2` versions). Questions are real.

Revised: findings 1–2 applied.

## ll95tbl.f

1. **Wrong.** Question 1: "the other 16 units": `NEWOPAC` is declared in 18 units, so 17 others, all with the 17-item layout (checked). Fix.
2. **Unclear.** Question 3: the `READ` of the $\log R$ line has `END=1000`, which closes the file and builds the table; only the header loop and the rows use `END=9999`. Fix: say so.

Checked otherwise: the table counts (8 × 13 + 10 + 12 = 126), the corner rows 58–70 and the filler, `NZ`, `NUMXM`. Question 2 holds: the $X = 1-Z$ tables of $Z$ = 0.06 and 0.08 land in slots 110 and 119, the slots of the next metallicity's $X = 0$ table, and overwrite them (an apparent bug).

Revised: findings 1–2 applied.

## massloss.f

1. **Wrong.** Output: "`LNEWFIT` (true when mass changes)". The routine sets `LNEWFIT` true only when `DMDT` > 0 (a mass gain, massloss.f:85–86); for a loss it leaves the value the main program set (false, main.f:588). Fix: "true only for accretion; the main program then calls [[getnewenv.f#GETNEWENV|`GETNEWENV`]] to restore the earlier fitting point (main.f:896)".
2. **Wrong.** "in COMMON `MASSCHG2`, the entropies `SACC`, `SCEN` (read by `COEFFT` and `MDOT`)". `COEFFT` reads only `DLOGT` and `DLOGP` from that block (and uses `SCEN` only in a commented-out line); `MDOT` reads `SCEN`. Fix accordingly.
3. **Wrong.** "`TAUCZ`, the convective turnover time, computed in `MIXCZ`". The comment at line 60 says so, but `MIXCZ` no longer computes it (its own comment, mixcz.f:101); it is set in [[taucal.f#TAUCAL|`TAUCAL`]] and [[tauint.f#TAUINT|`TAUINT`]]. `MASSLOSS` only prints it, and sets it to 0 in the shared block when there is no convective envelope. Fix: say so.
4. **Wrong.** `SENVOLD` listed as an input; it is an output (set by `MDOT`, then used by `GETNEWENV`). Fix.
5. **Missing.** The default values (`PARMIN`): `DMDT0` = −1e−14 (a loss; $\dot M > 0$ is a gain), `CREIM` = −4e−13, `LMDOT` and `LREIMER` false. And when it is called: only when `LAGE` is true (main.f:581–591). Fix: add.
6. **Missing (apparent bug, sharpens question 3).** The Reimers branch applies `CREIM` to $L/(gR)$ in cgs, which for the Sun is $L_\odot R_\odot/(GM_\odot) \approx 2.0\times10^{18}$ g/s, and `MDOT` reads the result as $M_\odot$/yr. With the default `CREIM` = −4e−13 (Reimers' coefficient in solar units and $M_\odot$/yr), the Sun would lose about $8\times10^{5}\,M_\odot$/yr. Fix: rewrite question 3 with these numbers.
7. **Wrong (question 5).** "Does `MDOT` use `RMU` only for accretion?" `MDOT` never uses the `RMU` it receives: it recomputes it at `JENV` before use. Likewise `EACC` and `ETHAV` feed only `ETHNEW` and `FAC`, which `MDOT` does not use. For a loss these three are stale (`SAVE`) or, on a first call, undefined, which is then harmless. Fix: replace question 5 by this point.
8. **Unclear.** Step 4's "virial-type energy per gram"; the code's comment speaks of the kinetic energy per gram of accreted matter. Also `EACC` is overwritten by the envelope mean, while the Stahler temperature uses the first value (`EACC0`). Fix: use the comment's words; name `EACC0`.
9. **Unclear (question 6).** Fine as is, but say the argument list has been shifted since the repository's first commit (checked: 6cd5673). Fix: one clause.

Revised: items 1–9 applied (outputs, `MASSCHG2` readers, `TAUCZ`'s source, defaults, the call condition, the Reimers units with numbers, question 5 replaced, `EACC0`).

## mdot.f

1. **Wrong.** Step 2: "(accretion) at most half the mass outside the fitting point". The limit applies whenever `RATE` > 0, and `RATE` = $|\dot M|$, so it applies to loss as well (mdot.f:66–69), though its comment says "add". Fix.
2. **Wrong.** Step 4 says the correction "changes $\log r$, $\log T$, $\log P$ of the zone". Only for a fully convective model (`JENV` = 1) are all points shifted; otherwise only $T$ and $P$ at `JENV` change, and the radii above `JENV` are stretched about $r_\mathrm{b}$ by $10^{\Delta\log r}$. Fix: say so; add that `DLOGP`, `DLOGT` go to `COEFFT` through `MASSCHG2` (its entropy terms, for points at or above `JENV`, when `LMDOT` and `DMDT0` > 0).
3. **Missing.** In step 4 the code also computes the new mean thermal energy $\bar e = (e_\mathrm{acc}\Delta M + \bar e_\mathrm{th} M_\mathrm{cz})/(\Delta M + M_\mathrm{cz})$ and `FAC` = $\log(\bar e/\bar e_\mathrm{th})$, both unused (their use is commented out); the `RMU` argument is overwritten before use. Fix: add to step 4 and to question 3.
4. **Missing.** For accretion the mass coordinates `HS1` are not changed: the gain goes into the outer shell's mass `HS2(M)` = $10^{\texttt{HSTOT}}$ − midpoint. Fix: add to steps 6–7.
5. **Missing question (apparent bug).** The shell-mass loop `DO I = JENV,M-1: HS2(I) = 0.5*(HS1(I+1)-HS1(I-1))` reads `HS1(0)`, out of bounds, when `JENV` = 1 (mdot.f:185–186), a case the routine handles elsewhere (lines 54, 110). Fix: add a question.
6. **Unclear.** Step 8 writes $M_\mathrm{cz}$ for two different masses: the step limit uses `DMCZ` = `HS1(M)` − `HS1(JENV)`, the mixing uses `DMCZT` = `SUMDM` (the sum of `HS2` from `JENV` to `M`, from `MASSLOSS`). Fix: name them.
7. **Unclear (question 4).** "without a message": `STOP911` is `STOP 911` (blanks do not count in fixed form), which prints the code 911. Fix: "with only the stop code 911".
8. **Wrong (question 5).** "Accretion adds mass but no angular momentum." `HJM` (specific angular momentum) is kept while `HS2(M)` grows, so the accreted mass takes the outer point's specific angular momentum. Fix: rephrase as a question on that implicit choice.
9. **Missing.** Question 1 should note that, through the shift, `MDOT` would write the shortened step into `MASSLOSS`'s `BL`, `LNEW` = true into the integer `JENV`, the new mass into `RTOT` and `SENVOLD` into `SUMDM`. Fix: one sentence.

Revised: items 1–9 applied.

## locate.f

Checked: the bisection, the two 1 % tolerances, the callers (`ALSURFP`, `GTLAOL`, `GTLAOL2`, `GTPURZ`), and the question on the tolerances (it holds for zero or negative end values and for descending arrays). Nothing to fix.

No change.

## lubksb.f

Checked: forward substitution with the permutation and the skipped leading zeros, back-substitution, the caller (`THDIFF`). Nothing to fix.

No change.

## ludcmp.f

1. **Missing.** The hard stop: a row of zeros ends the run with `STOP 'Singular matrix.'` (ludcmp.f:36). Fix: add to the method.

Revised: the stop added to the method.

## mcowind.f

Checked: the switch to `COWIND`, the saturation and Rossby scaling, the coefficient, the centrifugal factor (both $f$ terms, with $R$ in cm), the torque and the `WIND2` averaging; the four questions hold (`GL` is a local never set).
1. **Unclear.** "With the extra field scaling (`LBSCALE`)" reads as independent of the Rossby scaling; the code applies it only inside `IF(LROSSBY)`. Fix: say so.
2. **Missing.** COMMON `DEUTER` is declared but not used. Fix: one clause.

Revised: both applied.

## meqos.f

Checked: the conversions from `VARMHD` (the equations), $\beta$, `RMU` and the stop on $\mu$, the unused COMMON blocks, KC's changes, the questions.
1. **Wrong.** "where the run uses the MHD tables and the point is inside them". All seven callers test only `LMHD` (a namelist switch of `PARMIN`, default false), never the range. Fix: say so, and point to `mhdpx.f`'s question 1.

Revised: the callers' condition corrected.

## mhdpx.f

1. **Unclear (question 1).** It asks whether the callers check the range; they do not (only `LMHD`, see `meqos.f`). Fix: state it, and ask instead whether `MHDPX1` should signal the failure.

Revised: question 1 rewritten.

## mhdpx1.f

1. **Wrong (question 2).** Elements 21–25 of rows 1–3 are not "left from earlier calls to centre tables": the centre tables fill rows 4–8, and `MHDPX2` copies only 20 variables into rows 1–3, so those elements are never written (undefined). Fix.
2. **Missing question (apparent bug).** Tables are chosen with `TL.LT.TLIM2` (mhdpx1.f:45) but interpolated with `TL.LE.TLIM2` (line 60): at $\log T$ = `TLIM2` exactly, the centre tables are read and the quadratic interpolation uses stale rows 1–3. Fix: add question 4.
3. **Unclear.** Step 2 does not say where the tables' values go. Fix: "filled by `MHDPX2`, one row of `VAROUT` each".

Revised: items 1–3 applied.

## mhdpx2.f

1. **Unclear.** Purpose: "stores the result in row `ITBL` of `VAROUT`"; for `ITBL` < 0 the row is −`ITBL`. Fix: rows 1–3 for the ZAMS tables, 4–8 for the centre tables.

Checked otherwise: the nine branches, the 20 and 25 variables, `XCOMP`, and question 1 (`INTPT` returns early when `PL` is above the table, intpt.f:34–35).

Revised: the purpose line corrected.

## meval.f

Checked: the sorting check (`ERR` = 2), the walk through points and intervals, the extrapolation at both ends (`ERR` = 1), the first question (the comment contradicts the code).
1. **Missing.** `OSPLIN` is also called by `EQ2MOD` and `GETGRID`, not only by `HPOINT`. Fix: name them.
2. **Unclear (question 2).** "Does `OSPLIN` check `ERR`?" It does not (osplin.f:41 is the last use). Fix: state it and ask what should happen.

Revised: both applied.

## mhdst.f

1. **Missing.** A unit ≤ 0 skips a table, but `MHDTBL` always opens all eight files (`STATUS='OLD'`), and `MHDPX1` always uses all three ZAMS tables and all five centre tables. Fix: say so.
2. **Unclear.** The limits: with centre tables, the ZAMS upper part is used only up to the centre tables' first temperature. Fix: one sentence.

Revised: both applied.

## mhdst1.f

Checked: the headers and their checks, the composition test (the signs of $\delta X$ for $X$ and $Y$, 5 % tolerance, metals from element 3), the identical temperature grids, the centred differences into variables 21–24 and the placeholder 25. The smaller dimensions passed for the centre tables (`NTXM`, `NRXM` in place of `NT2M`, `NR2M`) are consistent within the routine. Nothing to fix.

No change.
