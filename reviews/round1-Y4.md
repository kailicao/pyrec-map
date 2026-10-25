# Pages mhdtbl.f to quadeos06.f

Round 1, Oct 25, 2026, by Claude, against the code at YREC `rp_1`. Each finding gives its kind (wrong, missing, unclear, format), the text and the proposed fix; "Revised" says what was applied.

Following the review brief; checked also against `callgraph.json` and with `grep`. No earlier round to check (this is the only one). Part of the list was reviewed on Oct 25 in a second pass.

## mhdtbl.f

Checked: the eight `OPEN`s, the call from SETUPS under `LMHD`, the unit numbers 40–47 in PARMIN, the users of `/MHD/`. Nothing to fix.

Revised: no change.

## microdiff.f

1. **Wrong (small).** "The temperature gradient … comes through `/SCRTCH/` (`SDEL(2,·)`)": MICRODIFF itself does not declare `/SCRTCH/`; its header says so, but [[microdiff_mte.f]] reads it. Fix: say that MICRODIFF_MTE reads it from `/SCRTCH/`.
2. **Unclear.** "probably ⁶Li, ⁷Li and ⁹Be, from these values": STARIN fills rows 13–15 from `XLI6_INI`, `XLI7_INI`, `XBE9_INI`, so it is a fact from the code. Fix: drop "probably", cite STARIN.
3. **Missing.** The units of `STOT` (g) and what the four calls convert. Fix: one line; `STOT` in grams, converted in place by SETUP and back by ETM.

Revised: the line on `/SCRTCH/` moved to MICRODIFF_MTE; units of `STOT` added; the light elements stated from STARIN.

## microdiff_setup.f

1. **Wrong.** "It reads `/GRAVS2/`, `/GRAVST/`, `/GRAVS3/` and `/SCRTCH/`": only `/GRAVS2/` (`XMIN`, `YMIN`) and `/CONST1/` (`CLN`) are used; `/GRAVST/`, `/GRAVS3/`, `/SCRTCH/` (only a commented-out line uses `SDEL`), `/GSCOF/`, `/CMIXING/`, `/CONST/` and `/CONST3/` are declared and unused. Fix: list them so.
2. **Unclear.** "`IEND` is the first convective point of the envelope; it then moves in to the last point with $Y >$ `YMIN`": the code sets `IEND` to the innermost point of the surface convection zone, then searches inward for the outermost point with $Y >$ `YMIN`. Fix: say "innermost" and "outermost".
3. **Missing question.** Nothing checks that `IEND > IBEGIN` after the two searches. If the radiative region shrinks to nothing, `MICRODIFF_MTE` divides `DRTOT` (zero or negative) by itself and builds a grid with $\Delta r \le 0$. Fix: add a question.

Revised: COMMON blocks corrected; `IEND` wording fixed; question 4 added.

## microdiff_mte.f

1. **Missing question.** The comment says `NPT` is chosen "such that DR <= DRMIN", but with $N = \lceil \Delta r_\mathrm{tot}/\Delta r_\mathrm{min}\rceil$ points there are $N-1$ intervals, so $\Delta r = \Delta r_\mathrm{tot}/(N-1) > \Delta r_\mathrm{min}$. An off-by-one? Fix: add a question.
2. **Missing.** The grid values of $\rho$ and $T$ (`EDEN`, `ETEM`) are in cgs units (from `ODEN`, `OTEM`), while $r$, $m$ and $d\ln P/dr$ are in Bahcall–Loeb units. Fix: say so in Outputs.

Revised: units added to Outputs; question 6 added.

## microdiff_etm.f

1. **Wrong.** Method step 1: "and likewise for $Z$ and the light elements". In the centre $Z$ is *capped* at $1 - X - X_4$, not floored; only $X$ and the light elements are floored at zero. Fix: say so.
2. **Unclear.** Question 1 ("kept non-negative (the centre) or added without a limit (the envelope); in the interior … no floor either") is tangled. Fix: "Light elements are floored at zero only in the centre; in the interior and the envelope the change is added with no floor."
3. **Unclear.** "probably ³He": STARIN fills row 4 from `XHE3_INI`, and rows 5–11 are C12…O18. Fix: state them as facts.
4. **Missing question.** For `NPT = 2` (allowed by MICRODIFF_MTE), `K0 = MIN(MAX(J-2,1), NPT-3) = -1`, which the "JVS fix" (`IF (K0 .EQ. 0) K0=1`) does not catch, and the interpolation reads `EDELX(-1)`; for `NPT = 3`, `K0 = 1` and it reads `EDELX(4)`, beyond the grid. These cases arise only when the radiative region spans two or three model points. Fix: add a question.

Revised: step 1 corrected; question 1 rewritten; ³He and rows 5–11 stated as facts; question 5 added.

## microdiff_run.f

1. **Wrong (small).** "with $m_1 = 0$ in the first cell": in `LAX_WENDROF1` the first cell also takes $C_{1,1} = 0$ (`DT2*ECOD1(2)/EM(2)`), and the last cell $C_{1,N} = 0$ with $m_N =$ `STOT`. In `LAX_WENDROF2` the same holds at $i = 1$ and $i = N$. Fix: state the boundary values for both steps.

Revised: the boundary values of both Lax–Wendroff steps stated.

## microdiff_cod.f

Checked every equation (concentrations, $n_e$, $a_0$, $\lambda_D$, the Coulomb logarithms, $C_1$, $C_2$) and the COMMON blocks. Nothing to fix.

Revised: no change.

## midmod.f

1. **Missing.** On the first diffusion step (`LFIRST`), MIDMOD resets `HCOMP` (rows 1–11, or 1–15 with `LEXCOM`) to the old model's composition `HCOMPP` and `AMUM` to `AMUO`, so mixing and burning start from the start of the model step. The note does not say so. Fix: add a step 0.
2. **Wrong.** "`IMIN` is the first shell above a central convection zone": the code sets `IMIN = MAX(2, I-1)`, where `I` is the first non-convective shell, so `IMIN` is the outermost shell of the convection zone; the comment says "first zone above". Fix: state what the code does, and add a question.
3. **Unclear.** The deuterium test uses `HCOMPP(12,M)`, the surface deuterium *at the start of the step*. Fix: say so.

Revised: step 0 added; `IMIN` corrected; the deuterium test explained; question 7 added.

## mix.f

1. **Wrong.** The settling time's outer boundary is "the deepest shell of the surface region with $Y >$ `YMIN`": the code starts at `JENV` (the base of the surface convection zone) and searches inward for the first shell with $Y >$ `YMIN`. Fix: say so.
2. **Wrong.** The COMMON blocks: `/COMP/`, `/OLDMOD/`, `/THEAGE/` and `/NEWENG/` are all declared but not used (each name occurs only in its declaration); the note lists them as shared and asks only about `/NEWENG/`. Fix: list the four as unused; widen question 6.
3. **Unclear.** Question 1's case "when `DTMAX` is an exact multiple of `DELTS`" holds only for multiples of two or more (`INT(DELTS/DTMAX) = 0`, `MOD = 0`). Fix: say so.

Revised: the outer boundary corrected; COMMON blocks and question 6 corrected; question 1 made precise.

## mixcom.f

1. **Wrong.** "$\mathcal{D}$ = `ECOD2` (a coefficient that includes $4\pi\rho r^2\, d\chi/dr$)": MIXGRID multiplies `COD2` by $\rho r^2\, d\chi/dr$, without $4\pi$. Fix: correct.
2. **Wrong.** Question 3 says that on the final call "heavier species (including $Z$) are mixed". The callers pass `JBEG = 5` on SECULR's final call (rows 5–11 or 5–15, not $Z$, row 3) and `JBEG = 4` in BURSMIX. Fix: rewrite the question: on SECULR's final call $X$, $Z$ and ³He do not change, so closure holds; in BURSMIX ³He (row 4) is mixed, and $Y$ is recomputed only if `LOK` is false.
3. **Missing.** Question 1: `I1` is also not set when `IEND = M`. Fix: add.

Revised: `ECOD2` corrected; questions 1 and 3 rewritten.

## mixcz.f

Checked the zones, the mixing, the clean-up, the callers (main, GETW twice, SECULR), the COMMON blocks and KC's change. Nothing to fix.

Revised: no change.

## mixgrid.f

1. **Wrong (question settled by the code).** Question 3 asks whether GETGRID uses the same $\Delta_L$. It does: GETGRID uses `HPTTOL(9)*HL(M)` with `HL` in solar units (FINDSH's header), and MIXGRID the same times `CLSUN`, in erg s⁻¹, as $d L/dr$ needs. Fix: state it in the method and drop the question.
2. **Missing.** Where the coefficient sits: `ECOD2(I)` is at the edge between grid points `I-1` and `I` (`XVAL(I) = ECHI(I) - DCHI/2`), as [[ccoeft.f]] expects. Fix: one sentence.

Revised: $\Delta_L$ and the position of `ECOD2` stated; question 3 dropped.

## ndifcom.f

1. **Missing question.** The header says the grid of the last region "is used initially, and then the program checks for additional unstable regions interior to that", but with `LOK = F` only that one region is mixed; other unstable regions are not mixed until the final call. Fix: add a question.
2. **Unclear.** Question 1 can be partly answered from the callers: SECULR passes rows 1–4 before the final iteration and rows 5–11 (or 5–15) on it, as the comments say; BURSMIX passes rows 4 to 11 (or 15). Fix: say so and narrow the question to BURSMIX.
3. **Unclear.** The header speaks of "an equally spaced grid in radius"; the grid is in $\chi$ (GETGRID). Fix: say so.

Revised: the grid's coordinate stated; question 1 narrowed; question 3 added.

## mmid.f

Checked the scheme against the code (including `YOUT` used for the derivatives) and the caller. Nothing to fix.

Revised: no change.

## model_to_equal.f

Checked: the grid (minimum spacing over the whole region), the interpolation, the row-8 metals (row 3 is $Z$ in SETUP_GRSETT and EQUAL_TO_MODEL), the overwritten midpoint radii, `/GRAVSZ/` and `/GRAVEZ/`. Nothing to fix.

Revised: no change.

## momi.f

1. **Unclear (question settled in part by the code).** Question 2 asks what `WALPCZ` is. GETNEWENV's comment gives it: the exponent in $\Omega r^{\mathrm{WALPCZ}} =$ constant in the surface convection zone, which PARMIN keeps in $[-2, 0]$. Fix: say so in the method and narrow the question to why that law switches off distortion for every shell.
2. **Missing.** `H0` is also computed and unused. Fix: add to question 1.

Revised: `WALPCZ` explained; questions 1 and 2 revised.

## mu.f

Checked the weights ($1/1.008$, $1/4.004$, $1/12.016$), the equations and the callers. Nothing to fix.

Revised: no change.

## mwind.f

1. **Wrong.** "`/DEUTER/` and `/ROT/` are declared but not used": the first element of `/ROT/` is `WNEW`, the input rotation rate that STARIN uses with `LWNEW`, and MWIND uses the same name for its new angular velocity, so it overwrites the input value at every call (WIND does the same). STARIN runs again for each run in main's `NUMRUN` loop. Fix: correct the COMMON line and add a question.
2. **Unclear.** "the convective turnover time and the photospheric pressure from `/OVRTRN/`": MWIND reads only `TAUCZ0`, `TAUCZ`, `FRACSTEP`; the pressures are read by AMCALC. Fix: say so.

Revised: COMMON line corrected; `/OVRTRN/` made precise; question 5 added.

## neutrino.f

Checked the four nuclei, the call from ENGEB (above `TCUT(5)`, with `LNULOS1`; `ZC`, `ZO`; the logarithmic derivatives) and the question on $\bar A$, $\bar Z$. Nothing to fix.

Revised: no change.

## nulosses.f

Checked AZBAR's equations and the call to SNEUT. Nothing to fix.

Revised: no change.

## For other groups

- **wind.f:** WIND uses the local name `WNEW`, which is the first element of `/ROT/` (the input rotation rate STARIN uses with `LWNEW`), so it overwrites the input at every call, as MWIND does. Worth the same question on wind.f's page. Settled: the page asks it (question 1).

- **ll95tbl.f (apparent bug):** tables are stored at `NZ(IZ)+IX`; at $Z = 0.06$, $0.08$ (no table 9) table 10 lands in slots 110 and 119, the $X = 0$ tables of $Z = 0.08$ and $0.1$, which are read earlier and so overwritten (slots 109, 118 stay empty). Asked on op954d.f's page. Also, LL95TBL's `/NEWOPAC/` has an older layout (with `ZOPAL952`, `ZALEX2`) than the other 17 routines; only `ZOPAL951`, at the same offset, is used, so it is harmless but misleading. Settled: op954d.f's page asks the first (question 1), ll95tbl.f's the second (question 1).
- **mdot.f:** `/MASSCHG3/` (`LSOLWIND` and the scaled solar wind's constants) is declared only in MDOT now that PARMIN's is commented out, so it is never set. Asked on parmin.f's page (question 6). Settled: mdot.f's page asks it too (question 2).
- **getopal95.f / op95ztab.f:** OP95ZTAB stops the run for $Z > 0.08$, so GETOPAL95's 3D branch for `ZTAB` $\ge 0.1$ ("no table 9 or table 10") is unreachable; the 4D branch can still meet the grid value $Z = 0.1$. Settled: added to getopal95.f's page (step 5).

## oeqos.f

1. **Format (broken math).** Question 3: "the table is used at its own $. Is the table chosen for the run's $ elsewhere?" The two stray dollar signs break MathJax (the "$Z$" was lost). Fix: restore "$Z$" and say that `ZTAB = Z` is set but not passed on.
2. **Missing.** Which `EOS` entries are used, as ESAC's header documents them, and that `EOS(1)` is the pressure in $10^{12}$ dyn cm⁻² (used in the pressure check). Fix: one paragraph.

Revised: question 3 repaired; the `EOS` entries listed.

## oeqos01.f

1. **Unclear (question settled in part by the code).** Question 1 asks whether the shifted indices come from ESAC01 storing its results differently: ESAC01's header lists them in that order (no $dE/d\rho$ entry). Fix: state it, and narrow the question.

Revised: the Indices paragraph cites ESAC01's header; question 1 narrowed.

## oeqos06.f

Checked against the code (the entries, the range, `NT = 197`, the commented-out pressure check). Nothing to fix.

Revised: no change.

## op952d.f

1. **Wrong (small).** "when the point's $Z$ and $X$ match the surface table's (within $10^{-4}$)": GETOPAL95 compares $Z$ with `ZTAB` to a *relative* $10^{-4}$ and $X$ with `XTAB` to an absolute $10^{-4}$, and skips this path when the acoustic depth is computed (`LADON .AND. LACOUT`). Fix: say so.

Revised: the call condition stated exactly.

## op953d.f

1. **Unclear.** The call condition omits the acoustic-depth bypass and the relative test on $Z$. Fix: as in OP952D.

Revised: the call condition stated exactly.

## op954d.f

1. **Unclear.** "as its comment says (JVS 04/11)": the comment is in GETOPAL95, not here. Fix: name GETOPAL95 and the flags `LADON`, `LACOUT`; add the general condition ($Z \ne$ `ZTAB`).
2. **Missing question (apparent bug, in LL95TBL).** LL95TBL stores each table at `NZ(IZ)+IX`, with `NZ` = 0, 10, …, 100, 109, 118. At $Z = 0.06$ and $0.08$ (no table 9), table 10 goes to `NZ(IZ)+10`, which is the first slot of the next $Z$: slots 110 and 119, the $X = 0$ tables of $Z = 0.08$ and $0.1$. These are read earlier (the file runs with $X$ outer, as LL95TBL's header check enforces) and so are overwritten; slots 109 and 118 stay empty. OP954D reads with the same indexing, so $X = 0$ at $Z = 0.08$, $0.1$ is wrong in every 4D interpolation that reaches it. Fix: add a question; report to the LL95TBL page's group.

Revised: the call condition rewritten; the `NZ` offsets explained; question 1 added.

## op95xtab.f

1. **Wrong.** Question 1 treats $Z \ge 0.1$ as a live case, but OP95ZTAB stops the run for any $Z > 0.08$ (its search loop ends at `NUMZ-1`), so `ZTAB` never exceeds 0.08 and the branch "use tables 6–9" is unreachable. The live problem is $Z = 0.04$ exactly with surface $X > 0.8$. Fix: split into two questions, the live one first.
2. **Unclear.** SURFOPAC "when the surface composition changes, probably": SURFOPAC is called by HPOINT (with `XNEW`) and STARIN (with `XENV`) and rebuilds the surface tables. Fix: drop "probably".

Revised: questions 1–2 rewritten from the old question 1; the SURFOPAC line fixed.

## op95ztab.f

1. **Wrong.** "A $Z$ above the grid stops the run": the loop `DO I = 3,NUMZ-1` accepts a fourth value only up to $Z = 0.08$, so any $Z > 0.08$ stops the run, though the comment says "Z > 0.1". Fix: say so; add a question.
2. **Wrong (consequence).** Question 1 (label 30 before the table-10 loop) is real but unreachable now, since $Z \ge 0.1$ never gets that far. Fix: say so.
3. **Unclear.** "four $Z$ values all below 0.04": the shift gives 0.01–0.04, so "no larger than 0.04"; table 10's shift gives 0.03–0.08. Fix: state the ranges.

Revised: the stop at $Z > 0.08$ stated, new question 1; the label-30 question qualified; table 9's mismatch at $Z = 0.04$ tied to OP95XTAB; the shifted ranges given.

## osplin.f

1. **Unclear.** `EPS` is described as MEVAL's tolerance; the code's comment says it is a relative error tolerance for `CHOOSE`. Fix: say so; give the meaning of `ERR` (1, 2) in the question.

Revised: both applied.

## ovrot.f

1. **Wrong.** Question 1 says KC's check "means `MRZONE` can hold zeros (… probably when there is no radiative region)": CONVEC sets every counted zone with a lower edge $\ge 1$, and with no radiative region `NRZONE = 0`, so the loop does not run. The check's cause is unknown. Missing: CONVEC's index error (`MRZONE(1,2) = M`, convec.f line 172) makes OVROT's top radiative region run to a stale bound, possibly past `M`. Fix: rewrite the question.

Revised: question 1 rewritten.

## pdist.f

1. **Wrong.** "The pulsation files are written by WRTMOD, QATM and QENV": QATM and QENV only declare `/PULSE/`; WRTMOD writes `IOPMOD` and passes `LPULPT` to ENVINT, which writes `IOPATM` and `IOPENV`. Fix: say so.
2. **Unclear.** `NK` "probably the run number": it is the main program's loop index over runs (`DO 200 NK = 1, NUMRUN`). Fix: say so.

Revised: both applied.

## pindex.f

No findings (both questions checked against the code).

Revised: no change.

## polint.f

No findings (the recurrence checked against the code: $D_i = h_P W/(h_O - h_P)$, $C_i = h_O W/(h_O-h_P)$).

Revised: no change.

## ptime.f

No findings (the factor $\ln 10 \approx 2.3026$, the clamp by `ATIME(13)` and the three questions checked).

Revised: no change.

## oversh.f

1. **Unclear.** "`IOV1`, `IOV2` … read elsewhere for the overshoot region's temperature gradient": the reader is TPGRAD, which with `LADOV` gives radiative points with `IOV1` $\le$ `IOVIM` $\le$ `IOV2` the adiabatic gradient; `IOV1` is the new lower edge, `IOV2` the formal one; `IOVIM` is set by COEFFT and PHYSIC. Fix: say so.
2. **Missing.** $H_P$ and its units (HSUBP: $H_P = P r^2/(\rho G m)$, cm), and the exact rule for the new edge (downward: innermost point with $r \ge r_\mathrm{edge} - d$; upward: outermost with $r \le r_\mathrm{edge} + d$). That CONVEC merges overlapping zones afterwards. Fix: add.
3. **Missing (question 1).** Upward overshoot (core, intermediate zones) never sets `IOV1`, `IOV2`, so `LADOV` never applies above a core. Fix: add to question 1.

Revised: the outputs line rewritten with TPGRAD's use; $H_P$, units and the edge rule added; question 1 extended.

## parmin.f

Checked: the unit numbers, the `DATA` values quoted ($L_\odot$, $R_\odot$, `CMIXL`, `ACFPFT`), the namelist dump at line 799 against the `OPEN` at 924, line 1458 (`ZENV`), line 1270 (`TRIDL`), the EOS and opacity priorities, `TENV`, `WALPCZ`, `IMPJMOD`, the settling switches, both wind laws' exponents against lines 1000–1086.

1. **Wrong.** Question 6 lists `LSOLWIND` among locals "used nowhere else": MDOT reads `LSOLWIND` from `/MASSCHG3/`, which PARMIN no longer declares (commented out on 2025-05-30) and nothing else sets, so MDOT's scaled solar wind can no longer be switched on and its constants `DMSUN`, `DMWSUN`, `DMWMAX` are never set. Fix: say so in question 6; point to it from KC's changes.
2. **Missing question.** The comment derives $\dot J \propto R^{2+5m+4mbc}$; the code (JvS 09/25) uses $a_R = 2 + 5m - 4mc$. For K97 the code reproduces the old law's $2 - \alpha$, so the comment looks stale. Fix: add question 9.
3. **Unclear (small).** KC's reordering "probably for alignment": a guess, not in the code. Fix: drop it.

Revised: question 6 corrected; question 9 added; "probably for alignment" dropped.

## physic.f

Checked: the $\mu$ formulas, the shear criterion (`DEXP(CLN*(DMID-PMID))*(DELAMD-DELMID)*GMID**2`), the stencil `K`, the COMMON outputs, the callers.

1. **Wrong (small).** "[[microdiff.f]] uses `SDEL(2,·)`": the reader is MICRODIFF_MTE (round 1, microdiff.f finding 1). Fix: link MICRODIFF_MTE.
2. **Unclear.** "0 otherwise (and in convective regions)": `QWRMAX(IM)` belongs to the interface `IM-1`/`IM`, is 0 only where both shells are convective, and `QWRMAX(1)` is never set; $\rho$, $P$ are interpolated in logs, $g$ and the gradients directly. Fix: say so.
3. **Missing (question 2).** `KSAHA`, an in/out counter of EQSTAT, is never initialized here. Fix: add to question 2.

Revised: all three applied.

## putmodel2.f

1. **Missing (question 2 answered).** `TLUMX(8)` is the $\alpha$-capture luminosity (COEFFT adds `ECA = EALPCA`; CRRECT counts `TLUMX(5) + TLUMX(8)` as helium burning); it is not written, so a model read back lacks it. Fix: rewrite question 2.
2. **Missing.** What the seven luminosities are (GETYREC7's comment: PP 1–3, CNO, He, ν, gravitational). Fix: add.

Revised: both applied.

## putstore.f

No findings (checked: the labels, the line with `SCV+O6`, the `PINDEX` call with undefined `JXBEG`, `JXEND`, `LSHELL`, `LMILNE` undeclared, $A$ and $R_p/R_e$ against lines 271–274, the callers WRTOUT and the main program).

Revised: no change.

## putyrec7.f

1. **Missing question (known bug).** The flags record: this routine writes `2(L1,1X),'F F ',2I4,F7.3` (line 52), GETYREC7 reads `2(L1,1X),5X,2I4,F7.3` (line 90), so `JCORE`, `JENV`, `CMIXL` are read one column off. Fix: add a question.
2. **Settled (question 3).** GETYREC7 reads two composition lines in the fully convective case too, so only the comment is wrong. Fix: say so.
3. **Missing.** Stale comments ("Last two lines are MODEL2 add-ons", "error messages go to LU ISHORT") after KC's change. Fix: add a question.
4. **Unclear.** "it is kept, probably, for writing models in the old format": a guess. Fix: drop.

Revised: questions 3–6 rewritten and renumbered; "probably" dropped.

## qatm.f

1. **Missing (small).** `HRAS` is HRA(2/3), set once by SETUPS (`HRAS = HRA(CC23)`). Fix: add.

Revised: applied.

## qenv.f

No findings (the three derivatives checked against lines 52–54, including $f_P$ in each; the `/ENVPRT/` readers).

Revised: no change.

## qgauss.f

1. **Unclear.** "the local effective gravity `G` and the surface element `S` (probably; …)": FUNC sets `G = DSQRT(QPHIR**2 + QPHITH**2)` and `S = C4PI*R*DSIN(X)*…`. Fix: state it.

Revised: applied.

## quad.f

No findings (the coefficients checked; the remark on false links already removed, as settled).

Revised: no change.

## quadeos01.f

No findings.

Revised: no change.

## quadeos06.f

No findings (identical to QUADEOS01 except the name and `(xx1pxx2(i))`).

Revised: no change.
