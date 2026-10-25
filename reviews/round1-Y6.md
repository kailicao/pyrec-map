# Pages solid.f to zsulaol.f

Round 1, Oct 25, 2026, by Claude, against the code at YREC `rp_1`. Each finding gives its kind (wrong, missing, unclear, format), the text and the proposed fix; "Revised" says what was applied.

Checked against the code in `src/` and `callgraph.json`.

## solid.f

1. **Wrong.** "`ERRMOM` (the tolerance `TOLERI`, shared only with CHECKJ, which sets it)". CHECKJ never gives `TOLERI` a value of its own: it saves it (`TOLER0 = TOLERI`), relaxes it to `MAX(DJOK*1.0D-2,TOLER0)` around its call to GETROT, and restores it. No routine, `DATA` or `BLOCK DATA` initializes it. **Fix:** say so, and rewrite question 1: outside CHECKJ's relaxed calls `TOLERI` is zero (where the compiler zero-initializes COMMON), so the Newton loop always runs its 20 steps.
2. **Missing.** Question 3 (`PDISK` as a rate): PARMIN's `DATA` gives `PDISK = 7.2722D-6`, which is $2\pi/(10\ \mathrm{d})$ in rad/s, so it is an angular rate, and the comment's "period" is the misleading part. **Fix:** reword the question with this fact.

Revised: `TOLERI` never initialized (CHECKJ only relaxes and restores it), question 1 rewritten; question 3 gives `PDISK` = 2π/(10 d) in rad/s.

## splinc.f

No findings.

No change.

## spline.f

1. **Unclear.** The notation uses $y_0, y_1$ for the table values and $y_1$ (`Y1`) for the first knot of case 4, then $y_1^\mathrm{tab}$. **Fix:** call the table values $f_0, f_1$ (`YTABS`, `YTABS1`) and the knots $\xi_1$ (`Y1`), $z_1$ (`Z1`).
2. **Unclear.** Question 1 is longer than it needs to be: every fallback branch is reached only when `XVALS` lies outside `[XTABS, XTABS1]`. **Fix:** say that plainly.

Revised: notation $f_0, f_1$, $\xi_1$, $z_1$; question 1 shortened.

## splinj.f

No findings.

No change.

## splinnr.f

1. **Missing.** The double-precision Numerical Recipes `spline` that the code does use is [[cspline.f#CSPLINE|CSPLINE]]. **Fix:** name it in question 1.

Revised: CSPLINE named in question 1.

## splint.f

1. **Wrong (incomplete).** "the second derivatives computed beforehand (by SPLINJ)": the opacity routines GTLAOL, GTLAOL2 and GTPURZ use second derivatives from [[cspline.f#CSPLINE|CSPLINE]] (computed there, or tabulated by SULAOL and ZSULAOL). **Fix:** name both.
2. **Wrong.** Question 1 says the comment's "SPLINE ABOVE" is SPLINJ in this code base; the comment is Numerical Recipes' text, and its `spline` (with end slopes) is CSPLINE here. **Fix:** reword.

Revised: second derivatives from SPLINJ or CSPLINE; question 1 reworded.

## splintd2.f

No findings.

No change.

## splnr.f

No findings.

No change.

## starin.f

1. **Wrong.** "38 of them" (COMMON blocks): STARIN declares 36. **Fix:** 36.
2. **Unclear.** Step 6 calls `SENV0` "the log envelope mass". It is $\log_{10}(m_\mathrm{fit}/M_\star)$ (`SENV = HS(M) - HSTOT`), a small negative number; `-1.0D-12` is a fitting point a fraction $\approx 2\times10^{-12}$ of the mass below the surface. **Fix:** say so.
3. **Missing.** Step 9: `AMUENV` is $\sum_k X_k/A_k$ over all 12 elements, H and He included (the inverse mean atomic weight per ion, as CHECKC's comment says), while STARIN's comment calls it "mean atomic weight of surface Z". **Fix:** write the equation, and add a question on the comment.
4. **Missing (apparent bug).** Core extension with `MCORE = 1` (for example the default `FCORE = 1.0`, which gives `INT(0)+1 = 1`): after the shift, `HT(2) = HT(1)` and `HP(2) = HP(1)`, so `DEL = (HT(2)-HT(1))/(HP(2)-HP(1))` is 0/0. **Fix:** new question.
5. **Missing.** Question 3 (`HD` not shifted) understates it: every density above the new core stays at its old index, and PHYSIC then reads `HD`. **Fix:** say that the whole density profile is misaligned by `MCORE` shells.
6. **Missing.** `FCORE` is overwritten with `MCORE*HPTTOL(2)` (a log offset, no longer a factor) in COMMON `CORE`. Minor; mention in step 4.

Revised: 36 COMMON blocks; `SENV0` explained; `AMUENV` equation and question 10; 0/0 with `MCORE = 1` (question 11); question 3 extended; `FCORE` overwrite in step 4.

## stitch.f

1. **Missing.** Question 1: besides STARIN, [[wrtmod.f#WRTMOD|WRTMOD]] and [[getnewenv.f#GETNEWENV|GETNEWENV]] also restore the integration steps they change; only CALCAD and STITCH do not. **Fix:** add.
2. **Missing.** Question 5: with `LSTATM` but not `LSTENV`, the atmosphere's luminosity column writes `B`, which is set only in the envelope branch (a value from an earlier call, or undefined). **Fix:** add to question 5.

Revised: questions 1 and 5 extended.

## sulaol.f

No findings.

No change.

## surfbc.f

1. **Missing.** `LRESET` (from CRRECT): all three envelopes are recomputed without starting a new triangle; the note mentions only `LNEW`. **Fix:** add to step 2.
2. **Missing (question).** When the code switches back from the gray atmosphere to Kurucz or Allard tables (`LTTAU`), it does not set `LNEW`, so the triangle's envelopes computed with the gray atmosphere are kept, while switching to gray starts a new triangle. **Fix:** new question.

Revised: `LRESET` in step 2; new question 5.

## surfopac.f

1. **Unclear.** "HPOINT (probably when the surface composition changes)": the code says when: HPOINT calls it when the surface $X$ has changed by more than $10^{-8}$. **Fix:** state it.

Revised: HPOINT's condition stated.

## surfp.f

1. **Missing (question).** G. Somers limited the general case's search to `IMINMAX(J)` "to prevent using -999", but the top-four branch (`GL ≥ ATMGL(NG-1)`) and the hot branches use the gravities `NG-3`…`NG` without checking `IMINMAX(J)`. **Fix:** new question.

Revised: new question 4.

## t6rinteos01.f

No findings.

No change.

## t6rinteos06.f

No findings.

No change.

## t6rinterp.f

1. **Unclear (overstated).** Question 1, "an undefined weight": when `IP` ≠ 3, the `ESACTQ` computed with the undefined `DIX` is not used, since the final blend needs `IP = 3`; the result is not affected. **Fix:** say so; the question becomes one of tidiness.

Revised: question 1 notes the result is not affected.

## taucal.f

1. **Wrong.** Step 5, "With no convective zone … $\tau_\mathrm{cz} = 0$": with no convective zone the code sets `IMAX = M` and, unless `LALLCZ`, computes $\tau_\mathrm{cz}$ at the surface anyway; `TAUCZ = 0` only when `LALLCZ`, which depends on a stale `IMAX < 1`. **Fix:** correct step 5 and add a question.
2. **Unclear.** Step 3, "the point $r_b + H_P$ lies in the upper half of the zone": the test is $\left|1 - \frac{r_b + H_P - r_\mathrm{IMAX}}{r_\mathrm{top} - r_\mathrm{IMAX}}\right| < 0.5$, so the point lies between the zone's middle and half a width above its top. **Fix:** write the test.
3. **Wrong.** `DEL1`, `DEL2` "probably the radiative and adiabatic gradients": ENVINT passes `EDELS(1,·)` and `EDELS(2,·)`, which STITCH's column list names the radiative and the actual gradient. **Fix:** say so.

Revised: step 3's test written out; step 5 corrected, new question 6; `DEL1`, `DEL2` named.

## tauint.f

1. **Wrong.** "the profile built by GETTAU (interior shells followed by the envelope's points)": GETTAU stitches the envelope onto the profile only when `LCALCENV` and `LNEWTCZ` are set, so TAUINT (called when `LNEWTCZ` is false) gets the interior only; that is why it searches `ENVSTRUCT` itself. GETTAU calls it only when `TAUCZ` is still 0 after its ENVINT call. **Fix:** correct, and rewrite question 1 (its premise was wrong).
2. **Missing.** `DEL1`, `DEL2`: for interior shells GETTAU passes `SDEL(1,·)` and `SDEL(3,·)`, the radiative and adiabatic gradients. **Fix:** say so.

Revised: interior-only profile and the calling condition; `DEL1`, `DEL2`; question 1 rewritten.

## tauintnew.f

1. **Missing (apparent bug).** A fully convective star: the code reaches "fully convective" only when every point from `IBEG` to `M` is convective, and then sets `IMAX = 1`, `JCORE = 1`; when the envelope is stitched (`M ≠ MINT`), the near-core test `HP(1) - HP(1) < 1` always holds, so `IBEG = 2` and the search restarts, ending in the same state: an endless loop. And if the outermost points are radiative, the whole convective interior is taken as a "convective core", and $\tau_\mathrm{cz} = 0$. **Fix:** new question.
2. **Missing.** `DEL1`, `DEL2` from GETTAU: radiative and adiabatic gradients for interior shells, but radiative and actual gradients for the stitched envelope points. **Fix:** add to the inputs, and a question.
3. **Missing.** In the interior-only case with two zones (`IJMAX ≠ 0`, `M = MINT`), `IMAX` is set to `JMAX`. **Fix:** add to step 2.

Revised: `DEL1`, `DEL2` in the inputs; `IMAX = JMAX` in step 2; new questions 6 (endless loop) and 7 (gradients).

## thdiff.f

1. **Unclear.** Step 4, "multiplied by $K_0\,\rho\,C$": the code multiplies by `KO*AC*CC` $= K_0 \sum_s A_s C_s \sum_s C_s$; $\sum_s A_s C_s$ is only proportional to $\rho$. **Fix:** write the factor as the code has it.

Revised: the factor written as the code has it.

## tpgrad.f

1. **Wrong.** "the mixing length `CMIXL` … (`CONST3`, set by SETUPS)": SETUPS sets `CDELRL`, `CMIXL2` and `CMIXL3`; `CMIXL` is set for each run by the main program (`CMIXL = CMIXLA(NK)`). **Fix:** correct.
2. **Missing (question 3).** With spots, `DELDEL` is recomputed after the point is found convective; if the spot correction makes it negative, `TEST` is negative and the run stops (`STOP 912`). **Fix:** add to question 3.

Revised: `CMIXL` set by the main program; `STOP 912` in question 3.

## trapzd.f

No findings.

No change.

## tridia.f

No findings.

No change.

## tridiag_gs.f

1. **Unclear.** Question 1 is titled "The same algorithm three times" but names four routines. **Fix:** "four times".

Revised: "four times".

## vcirc.f

1. **Format / settled.** The paragraph "A note on the site's call graph" (the false `QUAD` link) is obsolete: `codemap.py` no longer makes the link (settled). **Fix:** drop it.
2. **Wrong.** "with `LDIFAD`, the advective and diffusive parts `VESA`, `VESD`, `VESD2`, `VESD3`, `DSS`, `DGSF` (`DIFAD2`, `DIFAD3`), read by DADCOEFT": `VESA`, `VESD` are in `DIFAD2`, shared with CHECKJ and ROTGRID; `VESD2`, `VESD3`, `DSS`, `DGSF`, `FV0` are in `DIFAD3`, shared with DADCOEFT and SETUPV. `RAT` (`QUADD`) is read by CHECKJ, FPFT and WRTMOD. **Fix:** correct.
3. **Wrong.** Question 3: `VES` is made positive by `ABS(FES*VES)` for every interface before `HV` is formed, so `HV` never sees a negative `VES`; only `VESA` (the advective part) keeps its sign. **Fix:** rewrite the question: with `LDIFAD`, `HV` takes $|v_\mathrm{ES}|$ of a signed circulation; intended?
4. **Missing (apparent bug).** The $\mu$ loop multiplies `FESTIME` and `FV0` (COMMON, set once by SETUPV before SECULR's iterations) by the factor at every call of VCIRC, so the factor compounds over SECULR's iterations. **Fix:** new question.
5. **Unclear.** Step 3 calls the $\mu$ factor $q$, while steps 4 and 5 use $q$ for the shear `QWLNR`. **Fix:** call the factor $f_\mu$.

Revised: call-graph paragraph already gone; COMMON sharing corrected; question 3 rewritten; new question 7 (compounding); factor renamed $f_\mu$.

## viscos.f

No findings.

No change.

## wcz.f

No findings.

No change.

## wczimp.f

No findings.

No change.

## wind.f

No findings.

No change.

## wrthead.f

1. **Unclear.** Design: "1, a description in comment lines": two lines of format 1505 (" Neutrinos …" and '    "        " cont: …') and the rotation line of format 1510 (`ITRVER = 2`) do not start with `#`. **Fix:** say so, and add it to question 2.

Revised: non-`#` lines of formats 1505 and 1510 in the design and question 2.

## wrtlst.f

No findings.

No change.

## wrtmil.f

1. **Missing.** "when `LMILNE` is set": the calls are inside other conditions too. PUTSTORE calls it only when `LSTATM` or `LSTENV` is set, and WRTOUT only in its pulsation branch (`LPULSE` on a model that is not stored). So `LMILNE` alone writes nothing. **Fix:** say so, and add a question.

Revised: calling conditions; new question 4.

## wrtmod.f

1. **Wrong (sign).** "$A = V/\Gamma_1 - V(\ldots)$": the code has `XXX` $= -V$, `XX2` $= V/\Gamma_1$, `XX4 = -XX2 - XXX*(PQDP + SDEL(2)*PQDT)` $= -V/\Gamma_1 + V(\ldots)$. **Fix:** reverse the sign.
2. **Missing.** The pulsation model's shell lines are written only when both `LPULSE` and `LSTORE` are set; the header needs `LPULSE` alone. **Fix:** add to step 3.

Revised: sign of $A$; `LPULSE` and `LSTORE` in step 3.

## wrtmonte.f

No findings.

No change.

## wrtout.f

No findings.

No change.

## wtime.f

No findings.

No change.

## xrng4.f

No findings.

No change.

## xtime.f

No findings.

No change.

## ytime.f

No findings.

No change.

## zero.f

No findings.

No change.

## yalo3d.f

No findings.

No change.

## ykoeff.f

No findings.

No change.

## ylloc.f

No findings.

No change.

## ysplin.f

1. **Missing.** "Called by YKOEFF and YLLOC": also by [[intpol.f#INTPOL|INTPOL]] and [[ll4th.f#LL4TH|LL4TH]]. **Fix:** add them.

Revised: INTPOL and LL4TH added.

## yllo2d.f

- **Missing (detail).** For the surface table (`M1` = 4), the coefficients come from `CFORD4`, but the density range (`NDS`, `NDD`) is that of composition `KIPM1` (`/LLOT4/`, set by `LL4TH` to its `M1`). Fix: say so.
- **Missing (detail).** Outside the density grid, `FINDEX` returns a negative index and the extrapolation uses the first or last knot's $c_1 + c_2\delta$. Fix: name `FINDEX`'s signal.
- Checked and confirmed: the callers, the COMMON blocks, the cubic and its derivative, the two `INTPOL` calls, the stops, and questions 1–2.

Revised: both details added.

## yllo2d2.f

- **Missing (detail).** Besides the COMMON blocks, the stop message differs ("OPAL95 2D2 CHECK NDSS"), with the same mislabel as `YLLO2D`'s question 1. Fix: add it to the question.
- Checked and confirmed (by a line-by-line `diff` with `yllo2d.f`): the same code with `/GLLOT2/`, `/LLOT2/`, `/LLOT42/`, `/LINTPL2/`; the callers and the writers of `CFORD2` (`YLLOC`) and `CFORD42` (`LL4TH`).

Revised: the stop message added to question 1.

## yllo3d.f

- **Unclear.** "forced to tables 2–3 (for $X$ above the second grid value, or below it at $\log R > -1$)": "below it" reads as "below the second value", which at $\log R \le -1$ keeps tables 1–2. Fix: say that tables 2–3 are used for $X$ above the second grid value, and for $X$ below it only when $\log R > -1$; otherwise tables 1–2.
- Checked and confirmed: the call from `GETOPAC`, the COMMON blocks (`/KIPMLL/` is used here only; `YLLO3D2` has `/KIPMLL2/`), $\log R$, the interpolation in $X$, the derivative at fixed $\rho$, the stops, and questions 1–3.

Revised: the choice of tables reworded.

## yllo3d2.f

- **Wrong.** Question 1: "`M32` … is only an output there". In `YLLO2D2`, `M3` goes to `FINDEX` as its starting guess, so it is an input too (as are `M12`, `M22`); `FINDEX` resets a guess outside $1 \dots$`NX` to 1, which is why the missing `DATA` is harmless. Fix: say so.
- **Unclear.** "probably to interpolate between the two $Z$ tables": `GETOPAC` does exactly that when `L2Z` is true (with `LOPAL92`), linearly in $Z$ between `ZOPAL1` and `ZOPAL2`, for $\log\kappa$ and both derivatives. Fix: state it as fact.
- Checked and confirmed (by a `diff` with `yllo3d.f`): the same code with the second-$Z$ COMMON blocks and `YLLO2D2`.

Revised: the call from `GETOPAC` stated; question 1 corrected.

## zfermim12.f

- **Not a real question (settled from the code).** Question 1 asks whether the normalisation matches `SNEUT`'s use. The coefficients give $F_{-1/2} \to \Gamma(\tfrac12)\,e^x$ for small $x$ ($a_1/b_1 = 1.7725$) and $2\sqrt x$ for large $x$ ($a_1/b_1 = 2.000$ in the second set): Antia's convention, without $1/\Gamma(k+1)$. `SNEUT` uses $d\nu/d F_{1/2} = 1/(\tfrac12F_{-1/2}(\nu))$, which is right in that convention, and its argument of `IFERMI12`, $1.1052\times10^8\,\rho Y_e/T^{3/2}$, is $n_e h^3/[4\pi(2m_ekT)^{3/2}]$, the same convention. Fix: state this in the explanation and drop the question.
- **Missing (detail).** Both numerators have leading coefficient 1 (`a2(12)` = 1 too, and neither `a1(8)` nor `a2(12)` is read: the loops start from `xx + a(m)`). Fix: say so.
- Checked and confirmed: the two ranges, $z = e^x$ and $z = 1/x^2$, the degrees, the caller.

Revised: the convention stated and question 1 dropped; the numerators' leading coefficient noted.

## zsulaol.f

- **Missing (detail).** A temperature with fewer than four nonzero entries gets `NUMRSZ` = 0, and `GTPURZ` skips it. Fix: add.
- **Settled from the code.** Question 1 (called once per job?): `ZSULAOL` is called only from `SETUPOPAC`, which only `SETUPS` calls, once, from the main program (before the model loop). Fix: answer it in the text and keep only the design point (a logarithm taken in place is fragile).
- Checked and confirmed: the COMMON blocks, the natural spline (`CSPLINE` treats end slopes above $0.99\times10^{30}$ as natural), the reader `GTPURZ`.

Revised: `NUMRSZ` = 0 added; question 1 answered in the text and narrowed to the design point.
