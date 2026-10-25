# Pages eq2mod.f to getyrec7.f

Round 1, Oct 25, 2026, by Claude, against the code at YREC `rp_1`. Each finding gives its kind (wrong, missing, unclear, format), the text and the proposed fix; "Revised" says what was applied.

## eq2mod.f

1. **Unclear (question 1 rests on a false premise).** "Is a uniform fractional change in $j$ what solid-body rotation in the zone requires, or should $\Omega$ be uniform instead?" Multiplying every shell's $j$ by the same factor multiplies every shell's $\Omega$ by that factor too, so a zone already in solid-body rotation stays so. Fix: rewrite the question to ask whether the extended shells are assumed to be in solid-body rotation already (the code does not check it).
2. **Missing.** `CHI` is described only as "the model points' coordinate". GETGRID's comment defines it, $\chi = \log M/\Delta M + L/(L_\mathrm{tot}\Delta L) - \log P/\Delta P$. Fix: add a short phrase. Also note that `XVAL(I) = CHI(I)` for `I = 1..NMOD`, so `CHI` holds only the region's points, starting at `IBEG`.

Revised: question 1 rewritten; `CHI` described.

## eqbound.f

1. **Wrong.** "`KRA` (the index where the density ramp begins)". `READCO` sets `RMX(I) = RHO(KRA(I))`: `KRA` is the index of the highest table density at each temperature; the ramp begins one element lower, at `KRA-1`. Fix: reword.
2. **Missing.** EQSTAT2 calls OPAL 1995 only when $T \ge 5000$ K, $\log T \le 8$ and $\log\rho \le 5$ (its own density). Fix: add to "Who calls it"; question 3 then reads more clearly.
3. **Missing.** `KT` is set to 1 by `READCO` after it reads the table; `FT` is computed but used only in the commented-out lines (question 1 covers that). Fix: mention `FT` in question 1.

Revised: `KRA` corrected; EQSTAT2's conditions added; `FT` named in question 1.

## eqbound01.f

1. **Missing.** EQSTAT2's conditions for the 2001 table differ: $2000 \le T \le 10^8$ K and $\log\rho \le 7$. Question 2 says the 1995 questions "apply here too", but question 3 of `EQBOUND` quotes the 1995 cut ($\log\rho \le 5$). Fix: add the conditions to "Who calls it".
2. **Missing.** `/AEOS/` lists its last members as `M, MF, XA` where `/A/` has `XA, M, MF`; all users of `/AEOS/` declare it the same way, so there is no mismatch. No fix needed; noted for the reviewer.

Revised: EQSTAT2's conditions added.

## eqbound06.f

1. **Missing.** EQSTAT2 calls OPAL 2006 only when $1870 \le T \le 2\times10^8$ K and $\log\rho \le 7$. Fix: add.
2. **Missing (design note).** `KC 2025-05-30` reordered `/BEOS06/` in every routine that declares it (`ESAC06`, `RADSUB06`, `READCOEOS06`, `RHOOFP06`, this file): checked, consistent. No fix.
3. Otherwise correct: the ramps, signs and search match the code.

Revised: EQSTAT2's conditions added.

## eqburn.f

1. **Wrong.** "the reaction-rate arrays `HR1`…`HR12` (… computed elsewhere, probably in ENGEB or KEMCOM …)". Both callers compute them by calling [[rates.f#RATES|RATES]] just before `EQBURN` (mix.f line 166, xtime.f line 71). Fix: say so.
2. **Wrong / question 4 answerable.** The units: KEMCOM's header comment says `HR1`–`HR13` are rates "PER GIGAYEAR PER AMU", to be multiplied by the reactants' mass fractions and the product's atomic weight. XTIME's use, `CSECYR*1.0D9*ATIME(7)/DXDT`, is consistent with `DXDT` per Gyr. Fix: state the units in the explanation and drop question 4.
3. **Unclear.** "compared with `HT`, so probably $\log T$". XTIME passes `TL = HT(IEND)` to RATES as $\log T$, and PARMIN's defaults for `TCUT` are 6.5, 6.5, 6.82, 7.7, 7.5. Fix: state that `HT` is $\log T$ and `TCUT` are $\log T$ cutoffs, without "probably".
4. **Missing.** The helium-burning step uses `XC12`, which step 4 has replaced by its CN-equilibrium value when $T >$ `TCUT(3)`; when $X \le 10^{-10}$ the code jumps past the CN step and uses the actual abundance. Fix: add to question 1.

Revised: rates from RATES; step 4 runs only after step 3 (added); units stated, question 4 dropped; `HT` as $\log T$; question 1 extended.

## eqrelv.f

1. **Wrong.** Question 1: "`DL`, `D` and all derivatives then keep the values of the previous call (the routine has `SAVE`)". They are dummy arguments, not saved locals: on failure the routine returns before `DL = DL8`, so `DL` and `D` keep the caller's starting guess and the derivatives whatever the caller's variables held. Fix: say so.
2. **Wrong.** "solves … for $\ln\rho$" while the update is in $\log_{10}$ (`DML`, the limit of $\pm4$ is a factor $10^4$). Fix: "$\log\rho$".
3. **Unclear.** "Newton (equal spacing) in $y$, with step 0.2 starting at $\log T = 5$". The code places column $j$ at $\log T = 5 + 0.2j$ (`TTUD`), so the 20 columns span $\log T = 5.2$ to 9.0. Fix: state that.
4. **Missing.** The Debye–Hückel composition factors: $c_0 = 2X + \tfrac32 Y + \tfrac12(Z + \alpha)$ (`CMFDH0`), $c_1 = X + Y + \tfrac12\alpha$ (`CMFDH1`), with $\alpha = \sum_i \nu_i Z_i$ over the metal mixture (`DHNUE`, `ZDH`). Fix: add to step 3.
5. **Wrong.** "`/CCR/` … shared only with SETUPS, which presumably fills it." SETUPS reads it from the Fermi-table file (unit `IFERMI`): `DVAL`, `ETAT8`, `DTABLE` read, `IDEN` built. Fix: state it.
6. **Wrong / unclear.** "[[getnewenv.f#GETNEWENV|GETNEWENV]] and others set its composition"; question 2 suggests the composition may be stale. In fact each caller of the equation of state sets `XXDH`, `YYDH`, `ZZDH` (and `ZDH`) from the shell's `HCOMP` before the call (PHYSIC, COEFFT, CRRECT, SCONVEC, HSUBP, GETNEWENV, STARIN, WRTMOD, WRTOUT). Fix: say so in the COMMON blocks and reduce question 2 to the naming difference.

Revised: all six applied.

## eqsaha.f

1. **Wrong.** "Species with $K_i$ below $e^{-40}$ are treated as neutral; above $e^{40}$, as fully ionized." The test is on the exponent, and the loop stops at the first species below the limit (`GO TO 12`): that species and all later ones in the list are treated as neutral (the list is in order of increasing `SAHAT`). A species above the limit gets $K_i = 10^{16}$ and is left out of the derivative sums (`NZ1`). Fix: state both.
2. **Unclear.** "the ionized fraction of a metal is $x_i = K_i/(K_i+\epsilon)$": the same holds for hydrogen, which is one of the eleven species in the loop. Fix: "of species $i$ (the ten metals and hydrogen)".
3. **Wrong premise (question 4).** "`FXION(1)` … is 0 even if hydrogen is slightly ionized." Since the loop stops at the first species below $e^{-40}$, and the species before hydrogen have lower ionization temperatures, `NZ0 < 7` means hydrogen's own $K$ is below the limit too (up to the small differences in `SAHAU`). Fix: drop the question and explain in step 1.
4. **Missing.** `KSAHA` is not reset here; it adds this call's iterations to the caller's counter (callers such as CRRECT, GETNEWENV, GETTAU, HSUBP set it to 0). Fix: reword the output line.

5. **Missing (a clear bug, not yet asked).** For $X < 10^{-6}$, ESAC sets `MH=1` twice (lines 134–135) where ESAC01 and ESAC06 set `MF=1` and `MH=1`. So `MF` keeps the value from the bisection, `IHI-2` = 0, and the code reads `XZ(0,…)`, `EPL(0,…)`, `ZZ(0)` and copies `ESK = EPL(MF,…)` from outside the arrays. Fix: add a question.

Revised: all five applied (5 as question 6).

## eqscve.f

1. **Missing.** Step 1 lists the out-of-table tests on $\log T$ and $\log P_\mathrm{gas} < 4$, but the pressure search also returns `LCALC = .FALSE.` when $\log P_\mathrm{gas}$ is above the last pressure of row `IDT` (line 109). Fix: add.
2. **Unclear.** Step 5 says "from the hydrogen and helium tables": these are the pure-hydrogen `TABLEX` and pure-helium `TABLEY` (columns 2 and 3), read at the envelope's $T$ and $P_\mathrm{gas}$ with the stencil and the pressure abscissae of `TABLENV`. Fix: name the arrays, and extend question 3, since the same-grid assumption now covers three tables.
3. Otherwise correct: the radiation corrections, the smoothing weights and the particle-conservation formulas match the code.

Revised: both applied.

## eqscvg.f

1. **Unclear (question 3).** "Stale stencil search. The temperature search starts from `IDT`, which `EQSCVE` may have set for another point". The searches go down or up from any starting `IDT` until they bracket the point, so a starting value left by another point only costs time; it does not give a wrong stencil. The real point is the second half (the pressure stencil found on row `IDT` only). Fix: rewrite the question around the shared pressure grid.
2. Otherwise correct: the additive-volume density, the volume-weighted derivatives, the entropy-based $c_P$ (with `FTD` derivative weights on $\log_{10}$ `SMIX`) and the radiation terms match the code; the $c_P$ formula here equals `EQSCVE`'s, since $Q_{\rho T}\chi_T = -Q_{\rho T}^2/Q_{\rho P}$.

Revised: question 3 rewritten.

## eqstat.f

1. **Unclear (question 1).** "`KSAHA` is only an iteration counter, so the effect is probably small." `KSAHAx` is a saved local that only the four derivative calls increment and nothing reads, so the typo has no effect on any result; the caller's `KSAHA` simply does not count those iterations. Fix: say so.
2. **Unsupported (question 2).** "the OPAL 2006 table, whose spacing differs from the older tables" is not shown by the code. What the code does show: EQSTAT2's own comment gives the SCV tables' spacing as 0.20 in $\log P$ and 0.08 in $\log T$, not the 0.15 and 0.03 assumed here. Fix: base the question on that.
3. Otherwise correct; the central differences and the dummy outputs of the last call match the code.

Revised: questions 1 and 2 rewritten.

## eqstat2.f

1. **Missing (a clear bug, not yet asked).** In the transition band, the code forms the differences Saha − relativistic for `DL0`, `QDT0`, `QDP0`, `QCP0`, `DELA0`, `QCPT0`, `QCPP0`, `QAT0`, `QAP0` (lines 249–257), but not for `QDTT0` and `QDTP0`. The blend `QDTT = QDTT + WT0*QDTT0` then adds $W$ times the full Saha value to the relativistic one instead of $W$ times the difference; the same for `QDTP`. Fix: say in step 5 that the blend holds for all but these two, and add a question.
2. **Missing.** The blend uses the weight $W(\log T)$ but the derivatives ignore $dW/d\log T$ (the line computing it, `WT1`, is commented out), so the blended $Q_{\rho T}$ etc. are not the derivatives of the blended $\log\rho$. Fix: add to the new question.
3. **Wrong.** "`/DEBHU/` and `/CTLIM/` are shared with about twenty routines each." `/DEBHU/` is declared here but not used; `/CTLIM/` is used for `TSCUT` only (shared by 28 units, `/DEBHU/` by 17). Fix: say `/DEBHU/` is declared but unused here.
4. Checked and correct: `BETA14` $= 4\min(1, 1-\beta)/\beta$; PARMIN does keep only one OPAL flag (lines 869–877); the smooth step and $\mu_e^{-1}$; the OPAL ranges and blends; questions 1–6 are real (question 3: the message is written and the run continues).

Revised: step 5 and a new question 7 on the blend; the COMMON sentence corrected.

## equal_to_model.f

Checked against the code: the interpolation, the limits on each side (as the comment says), the metal scaling, the unit conversions, the callers and the COMMON blocks are right, and the four questions are real. Nothing to fix.

No change.

## esac.f

1. **Wrong.** Question 5 lists `IS` among the unused locals. `IS` is passed as `QUAD`'s first argument: with `IS = 0`, `QUAD` recomputes its saved abscissa factors, with `IS = 1` it reuses them. Fix: drop `IS` from the list, and mention this caching in step 5.
2. **Wrong.** "`/A/`, `/AA/`, `/B/`, `/BB/`, `/E/`, `/EE/` … all shared with `READCO`, `T6RINTERP`, `RADSUB`, `RHOOFP` and `BLOCK_DATA`." The callgraph gives: `/A/` with READCO, RHOOFP, T6RINTERP, BLOCK_DATA, EQBOUND; `/AA/` with READCO, T6RINTERP, BLOCK_DATA; `/B/` with READCO, RADSUB, RHOOFP, BLOCK_DATA; `/BB/` with T6RINTERP only; `/E/` with OEQOS, RADSUB, READCO, RHOOFP, T6RINTERP; `/EE/` with READCO, T6RINTERP. Fix: list them per block.
3. **Missing.** Step 1: if $X + Z > 1$ the run stops (label 61), and later, if the tables' $Z$ values differ from each other or from `ZZ(1)`, it stops too (labels 66 and the "Z DOES NOT MATCH" check); only the table-range and empty-region cases use the alternate return. Fix: add.
4. **Unclear.** Step 4: "if even 3×3 fails, shift the stencil once". The code: if the 3×3 sum is in the empty region but the 2×2 one is not, it moves the stencil back by one in both $T_6$ and $\rho$ (to `K3-3`, `L3-3`) and uses 3×3 without checking the shifted stencil; otherwise "empty region". Fix: reword.

Revised: all four applied.

## esac01.f

1. **Wrong.** "`/AEOS/`, `/AAEOS/`, `/BEOS/`, `/BBEOS/`, `/EEOS/`, `/EEEOS/` … shared with `READCOEOS01`, `T6RINTEOS01`, `RADSUB01`, `RHOOFP01` and EQBOUND01" reads as if every block were shared with all five. The callgraph: `/AEOS/` with READCOEOS01, T6RINTEOS01, RHOOFP01, EQBOUND01; `/AAEOS/` and `/EEEOS/` with READCOEOS01, T6RINTEOS01; `/BEOS/` with READCOEOS01, RADSUB01, RHOOFP01; `/BBEOS/` with T6RINTEOS01 only; `/EEOS/` with OEQOS01, RADSUB01, READCOEOS01, RHOOFP01, T6RINTEOS01. Fix: list per block.
2. **Missing.** For $X < 10^{-6}$ this routine sets `MF = 1` correctly, unlike `ESAC` (its new question 6); worth a word, since the question list says the ESAC questions "apply here too". Fix: say which ones do.
3. Checked: the guards (`IPU`, `IQU`, and `IP = IQ = 2` at the last row or column), `APROP`, the message without values, the `ESK`/`ESK2` slip (line 437) and the swapped `IP,IQ` (line 489).

Revised: COMMON blocks listed per block; question 3 made precise.

## esac06.f

1. **Unclear.** "shared with the 2006 routines above and EQBOUND06": per block, `/AEOS06/` with READCOEOS06, T6RINTEOS06, RHOOFP06, EQBOUND06; `/AAEOS06/`, `/EEEOS06/` with READCOEOS06, T6RINTEOS06; `/BEOS06/` with READCOEOS06, RADSUB06, RHOOFP06, EQBOUND06; `/BBEOS06/` with T6RINTEOS06, EQBOUND06; `/EEOS06/` also with CALCAD and OEQOS06. Fix: list per block.
2. **Missing.** The check `iorder .gt. 9` writes "iorder cannot exceed 9", copied from ESAC01, although this table has ten quantities (EOS(10) = $\Gamma_3 - 1$); the routine continues anyway. Fix: add to a question.
3. **Unclear.** "CALCAD … calls it directly for every point of the model and envelope": right (`I = 1..M+NUMENV-1`); its call for the atmosphere points is commented out. Fix: add that.
4. Checked: `NTA`, `NRA`, `RADSUB06(irad,…)` called only when `irad = 1` (question 1 is real), the `MF = 1` case is right here.

Revised: all three applied.

## findex.f

1. **Wrong (question 2).** "The header lists `INTPOL` and `YSPLIN`, which live elsewhere or no longer exist." Both exist, in `intpol.f` and `ysplin.f`; the header is the package's table of contents. Fix: say where they are, and turn the question into a lighter note (or drop it).
2. **Unclear (question 1).** "Do all seven callers do so?" can be answered from the code: LL4TH, YLLO2D, YLLO2D2, YLLO3D and YLLO3D2 test for a negative `M`; KURUCZ and KURUCZ2 do not. They clamp `ITS = M2-2` to 1, so below the table they still work, but above it ($M_2 = -$`NUMTM`) `ITF = M2+3` is below `ITS` and the temperature loop does nothing. Fix: make the question about KURUCZ and KURUCZ2 only.
3. **Missing.** `X` equal to the last table value counts as above the table (`M = -NX`); YLLO3D and YLLO3D2 catch this case explicitly. Fix: add to the method.

Revised: all three applied.

## findsh.f

Checked against the code: the shell counts, the end tests, the core and envelope searches and the fully convective case are right; the three questions are real (question 2 says itself that the case is safe as written). Nothing to fix.

No change.

## fpft.f

Checked against the code: $f_P$, $f_T$ and $\langle g\rangle$ from `F0`, the amplitude $a$, the Romberg step (`JMAX` = 2, `H(J+1) = H(J)/4`), the potentials in `/QUADD/`, the callers and the COMMON blocks. Nothing to fix.

No change.

## func.f

Checked against the code: $P_2$, both derivatives of $\Phi$ (with `CONST` $= 4\pi/(3r^4)$), $\partial r_0/\partial r$, $\partial r_0/\partial\theta$, $g$ and $S$ match; the three questions are real. Nothing to fix.

No change.

## get_imp_diffco.f

1. **Question 1 answerable.** Both callers pass the change of one iteration: GRSETT sets `EX_H(I) = 0.5*(EX(I)+EX(I-1)-EX_P(I)-EX_P(I-1))` and then `EX_P = EX`; MICRODIFF_RUN does the same for `ED_H`. So the corrections add up correctly. Fix: state it and drop the question.
2. **Missing.** MICRODIFF_RUN sets `EQCOD2X_H` to zero before each call ("only used in GRSETT … retained for legacy"), so there the coefficients do not change and only the matrix is rebuilt. Fix: add.
3. **Missing (an apparent bug, new question).** Here `ECOD2_H(I)` is the coefficient between points `I` and `I+1` (`B(1)` uses `ECOD2_H(1)`), and MODEL_TO_EQUAL and LAX_WENDROF1 use the same convention for `EX_H(1..NPT-1)`. But GRSETT's loop sets `EX_H(I)` for `I = 2..NPT` from points `I-1` and `I`, which is the midpoint one lower; `EX_H(1)` keeps the value LAX_WENDROF1 left in it. So `ECOD2_H(I)` is probably corrected with the change at the neighbouring midpoint. Fix: add the question; report to the group that has grsett.f.

Revised: question 1 replaced by the answer; MICRODIFF_RUN's zeroing added; new question on the index.

## getalex06.f

Checked against the code: the rebuild test, $\log R = \log\rho - 3(\log T - 6)$, the index searches, the four-point Lagrange weights (INTERP), the linear extrapolation above the largest $\log R$ (`QOD` kept at the edge, `QOT` taken from the extrapolated values), the conversion to fixed $\rho$, the caller and the COMMON blocks. The three questions are real. No findings.

No change

## getfc.f

1. **Question 4 answerable.** "is `IMIN` ≥ 2 always?" MIDMOD sets `IMIN = MAX(2,I-1)` or `IMIN = 2` (midmod.f lines 329, 331), so `IMIN-1` is at least 1. Fix: state it and drop the question.
2. **Unclear.** "`DM` (density at zone edges, probably)". SETUPV sets `DM(I)` by four-point interpolation of $\log\rho$ to the zone edges (setupv.f line 207) and `RM(I)` as the mean of the neighbouring centre radii (line 68). Fix: drop "probably", name SETUPV.
3. **Unclear.** Step 3 writes $\alpha U$, but $\alpha$ was defined with the comment's ½, while the code uses `ALPHA` (no ½); the code also takes the absolute value, which the comment's formula does not. Fix: write `ALPHA` in step 3 and mention the absolute value.

Revised: question 4 answered in "The method" and dropped; `DM`, `RM` sourced to SETUPV; step 3 written with `ALPHA` and the absolute value noted.

## getgrid.f

1. **Unclear.** "the same combination of $\log m$, $L$ and $\log P$ that the model uses to place its points." HPOINT scales $\Delta_L$ by the largest $L$ in the model (`HPMAX(2) = HPTTOL(9)*HLMAX`, hpoint.f line 285); GETGRID by the surface value `HL(M)`. Fix: name HPOINT and the difference.

Otherwise checked: $\chi$, `NTOT`, `DCHI`, `ECHI`, the OSPLIN call in $\log m$, the callers and the readers of `/EGRID/`; both questions are real.

Revised: HPOINT named, with the difference in $\Delta_L$; $L_\mathrm{surf}$ = `HL(M)` stated.

## getmodel2.f

1. **Question 2 answerable.** "What does −1 mean for the fit, and who reads `FTRI`?" `FTRI` is the orientation of the envelope triangle: SURFBC sets it to +1 when it starts a triangle and flips its sign each time it reflects a corner (surfbc.f lines 102–119), using it in its test of whether ($T_\mathrm{eff}$, $L$) lies inside. PUTMODEL2 (called by WRTLST) and PUTYREC7 write the record numbers as negative when `FTRI` < 0 (putmodel2.f line 87), so that the sign survives a restart. Fix: state it under "Outputs" and drop the question.
2. **Missing (question 3).** The header record reads `HS(M)` in the same statement that reads `M`, so a model with `M` > `JSON` writes out of bounds before any shell is read. Fix: add to the question.

Otherwise checked: the formats, the unit test on `TLUMX` (with $|L_\nu|$), the 15 abundances, the caller (`MOD2 ` in STARIN) and `/CONST/`.

Revised: `FTRI` explained, question 2 dropped; question 3 (now 2) extended.

## getnewenv.f

1. **Wrong.** "moves the outer fitting point … outward when the star loses mass." The main program calls it only when MASSLOSS has set `LNEWFIT`, that is, when `DMDT` > 0 (massloss.f line 85), whether `DMDT` is the constant `DMDT0` or the Reimers rate `CREIM`$\,L/(gR)$; MDOT applies a positive `DMDT` as a mass gain (`DELM` > 0 added to `SMASS` and `HSTOT`, mdot.f lines 88, 175–183), and main.f's comment says "restore prior fitting point if mass accretion is being included". The defaults of both rates are negative (`DMDT0` = −1e-14, `CREIM` = −4e-13, parmin.f lines 578–581), so with them the routine does not run. The header comment ("total mass is being decreased") disagrees. Fix: describe the trigger by the sign of `DMDT`, both rates included, and ask about the header (new question 6).
2. **Wrong.** `OMEGA` is listed among the outputs, but it is a local array (question 2 says so). Fix: drop it from the outputs; extend question 2: the new points' $j$ comes from the stale `OMEGA(MM)` in two of the three cases, and the main program then calls FPFT with its own `OMEGA`, which has no values for the new points.
3. **Missing (apparent bug).** The general case sets $\Omega \propto r^{-\alpha}$ (lines 258, 260), while WCZ uses $\Omega \propto r^{\alpha}$, for which the end cases $\alpha = -2$ (constant $j$) and $\alpha = 0$ (solid body) used here hold; with $r^{-\alpha}$ the intermediate laws rise outward. MDOT line 145 uses the same sign as this routine. Fix: new question 7.
4. **Missing.** `/ENVPRT/` is declared but not used. Fix: one phrase.

Otherwise checked: the surface quantities, the spot temperature, the matching shift and the $10^{-10}$ test, the new points, the interpolation (question 1's sign error is real, line 185–186), the shell masses, $J$ and $E_\mathrm{rot}$.

Revised: "When it runs" added (trigger by the sign of `DMDT`, defaults, the header's disagreement); `OMEGA` dropped from the outputs and question 2 extended; step 6 rewritten; questions 6 and 7 added; `/ENVPRT/` noted; FPFT named under "Who calls it".

## getopac.f

1. **Missing.** The stop for $Z$ far from `ZENV` applies only without `L2Z` and without OPAL 1995 (`.AND..NOT.L2Z .AND. .NOT.LOPAL95`, getopac.f line 98 of the source): OPAL 1995 interpolates in $Z$ itself. The page says "with a single-$Z$ table". Fix: name both exceptions.
2. **Missing.** `KURUCZ` and `KURUCZ2` have an alternate return (`*100`): if either fails, `LGOTATM` stays false and the interior tables are used alone, even below `TMOLMIN`. Fix: add to step 1.

Otherwise checked: the table order, the helium-burning interpolation to $Z = 1$, the ramp, the Hubbard–Lampe fit and its derivatives, the combination $1/\kappa = 1/\kappa_\mathrm{rad} + 1/\kappa_c$ with its derivatives, the callers and the COMMON blocks; the four questions are real.

Revised: both added.

## getopal95.f

1. **Unclear.** Step 5: "the $X = 0.95$ table (and for $Z \ge 0.1$ also the next) is absent; the stencil skips it, and the last $X$ node is set to $1 - Z$." The node is set to $1 - Z$ only for $0.04 \le Z < 0.1$, where the stencil is 0.7, 0.8, 0.9, $1 - Z$; for $Z \ge 0.1$ the stencil is 0.5, 0.7, 0.8, 0.9 (source lines 252–286, 355–389). Fix: give the nodes and both stencils.

Otherwise checked: $\log R$, the range stop, `LEXTL`, the stencil searches, the empty-corner logic (`LSHIFT`, `LEXH`, `RLH`), the 2D/3D/4D choice and the forced 4D path, the callers and the COMMON blocks. All five questions are real; question 1 (`CAPPA2(IXX,ITT,J)` with an $X$ index, line 168) is an apparent bug, and `LCHK` is indeed never read anywhere.

Revised: step 5 rewritten.

## getqua.f

1. **Format.** Question 3 repeats its own text after "matches neither.)" (a stray `\rho g$, the comment's term …`), which breaks the math rendering. Fix: remove the repeated half.
2. **Unclear (question 1).** "roughly half the one-sided forward difference": the expression as written reduces exactly to $\tfrac12(\rho_{i+1}-\rho_i)/\Delta r_+$. Fix: say "exactly half". The apparent bug itself is real (getqua.f lines 55–56: `-FMI*EXP(CLN*HD(I))`, presumably `HD(I-1)`).
3. **Missing.** The central row divides $\rho_2 - \rho_1$ by $\Delta r = \min(r_1, r_2 - r_1)$ rather than $r_2 - r_1$, and its right-hand side uses $\Omega_1^2\,d\rho/dr$, not $d(\rho\Omega^2)/dr$ (lines 41, 45). Fix: new question 5.

Otherwise checked: the discretized equation (the `DRI` terms give $(2/r)\phi'$), the surface row, the solver, `/QUADRU/`, `/TRIDI/` and the caller.

Revised: question 3 repaired; question 1 sharpened; question 5 added.

## getrot.f

1. **Missing.** `HJM` is also an output: SOLID and WCZIMP rewrite it as `HI*OMEGA/HS2` (solid.f line 69; wczimp.f lines 42, 73, 82, 102, 126), so $j$ is redistributed within convection zones. Fix: add to "Outputs".
2. **Missing (apparent bug).** A convective last shell under a radiative one (`LCZ(M)`, not `LCZ(M-1)`) only sets `LCONVZ` and `JSTART = M`; the loop then ends, and neither WCZIMP nor SOLID is called for shell `M` (getrot.f lines 25–29, 43–50 of the source). Fix: new question 2.

Otherwise checked: the scan, the calls and the callers.

Revised: `HJM` added to the outputs; question 2 added and pointed to from "The method".

## gettau.f

1. **Wrong premise (question 1).** "`SDEL(3,I)` for the interior points but `EDELS(2,·)` for the envelope points … one of them is wrong." The two arrays store the gradients in different orders: PHYSIC sets `SDEL(1..3)` = $\nabla_\mathrm{rad}$, $\nabla$, $\nabla_\mathrm{ad}$ (physic.f lines 80–82), QENV sets `EDEL(1..3)` = $\nabla_\mathrm{rad}$, $\nabla_\mathrm{ad}$, $\nabla$ (qenv.f lines 64–66), copied into `EDELS`. Both give $\nabla_\mathrm{ad}$. Fix: state it in step 4 and drop the question.
2. **Unclear.** "`RBCZ` … presumably set by `TAUINTNEW`". TAUINTNEW sets it (tauintnew.f lines 136–144, in solar radii at line 247, 0 at line 250); TAUINT does not. Fix: say so.
3. **Unclear.** Step 4 "if needed, append the envelope points": only with the new method and `LCALCENV`, points 2 to `NUMENV`. Fix: say so.

Otherwise checked: the base search, the threshold, the ENVINT call with the spot correction, the early exit on `TAUCZ` ≠ 0, the reset of `LCALCENV`, the callers and the COMMON blocks; questions 2–5 are real.

Revised: question 1 answered in step 4 and dropped (the others renumbered); `RBCZ` and the appending stated.

## getw.f

1. **Question 2 answerable.** "`DWMAX` as a time … What is its unit and meaning?" `DWMAX` is the largest fractional change of $\Omega$ in the last step, $2|\Omega-\Omega_\mathrm{old}|/(\Omega+\Omega_\mathrm{old})$ (wtime.f lines 31–36, via HTIMER); `DTWIND` is the largest $\Delta\Omega/\Omega$ allowed per model step (WTIME's comment, line 22) and `DTDIF` the largest per substep (REMAP sets them from `TIME_DW_GLOBAL` and `TIME_DW_MIX`, remap.f lines 253, 256). All dimensionless; the `DT` prefixes are misleading. Fix: state it in step 3 and drop the question.
2. **Question 3 answerable.** CHECKJ and CHECKC halve `DT` before they set `LREDO` (checkj.f line 103, checkc.f line 90), so $2\,$`DT` is the old substep and `SUMDT` returns exactly to the substep's start. Fix: state it and drop the question.
3. **Wrong.** "the wind removes angular momentum over the substep". In the substep loop GETW calls `MWIND` and `WCZIMP` only for a fully convective star (`LALLCZ .OR. .NOT.LINSTB`, the second always false on this path); otherwise it passes the wind's quantities to SECULR, which calls MWIND (seculr.f line 192). Likewise `MIXCZ` and `SECULR` run only when the star is not fully convective. Fix: say so.

Otherwise checked: the header, the callees, the no-instability path with `FRACSTEP` = 0.5, the $\theta$ update, the light-element block, the final GETROT, the printed quadrupole term, and questions 1, 4, 5, 6 (now 1–4). (`LSKIP` at source line 170 is always false on the path that reaches it; not worth a question.) No remark on the false `QUAD` link remains (a settled point).

Revised: step 3 gives the meaning of `DWMAX`, `DTWIND`, `DTDIF`, the redo with the halved `DT`, and where the wind is applied; questions 2 and 3 dropped, the rest renumbered.

## getyrec7.f

1. **Wrong (question 2).** "`LDIFY = .FALSE.` appears twice". It appears once (getyrec7.f line 60), followed by `LDIFZ = .FALSE.` (line 61). Fix: drop the question.
2. **Unclear.** "Who writes the format: probably PUTYREC7". Its formats match GETYREC7's (putyrec7.f lines 44–125), and nothing calls it. Fix: drop "probably".
3. **Missing (apparent mismatch).** PUTYREC7 writes the flags record with `'F F '` (four characters) before `JCORE` (putyrec7.f line 52), GETYREC7 reads it with `5X` (getyrec7.f line 90): every field is read one column late, harmless with blanks ignored unless `JENV` (or `JCORE`) has four digits, when a digit of `JENV` lands in `JCORE`. Fix: new question.

Otherwise checked: the defaults, the header, `TLUMX`, `FTRI`, the shell records and the range check, the compressed composition (including the odd-count read of rows 12–15, which relies on the DO variable's value after the loop and is right), $\Omega$, the rewinds and the caller.

Revised: question 2 dropped, the others renumbered; PUTYREC7 stated as the writer; the offset question added.

## For other groups (from the pages above)

- **massloss.f.md**, "Output: `LNEWFIT` (true when mass changes)": it is set only when `DMDT` > 0 (massloss.f line 85), and false at line 41 only when `LMDOT` is off; with `DMDT` < 0 it keeps the value the caller set (main.f line 588 sets it false before the call). A positive `DMDT`, from `DMDT0` or from the Reimers formula, is applied by MDOT as a mass gain (mdot.f lines 88, 175); the defaults of both rates are negative (`DMDT0` = −1e-14, `CREIM` = −4e-13, parmin.f lines 578–581). Settled: the page says so (Outputs, steps 1 and 5).
- **mdot.f.md**: MDOT line 145 sets $\Omega_\mathrm{surf} \propto r^{-\alpha}$ with $\alpha$ = `WALPCZ`, the opposite sign to WCZ's $\Omega = C r^{\alpha}$ (wcz.f line 58); see getnewenv.f question 7. Settled: added to the page as question 7.
- **checkj.f.md**: CHECKJ stops at the first negative $j$ (`IF(IREDO.GT.0)`, checkj.f line 93), although its message says three attempts at cutting the step failed. Settled: the page says so (question 1).
