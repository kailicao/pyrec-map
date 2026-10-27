# Pages quint.f to sneut.f

Round 1, Oct 25, 2026, by Claude, against the code at YREC `rp_1`. Each finding gives its kind (wrong, missing, unclear, format), the text and the proposed fix; "Revised" says what was applied.

## quint.f

- **Wrong.** "the caller is the one that warns about extrapolation": `MHDPX1`'s extrapolation warnings (formats 5001, 5011) and the range test are commented out; it only checks that the three `XC` are equidistant. Fix: say the caller checks equal spacing, and that its extrapolation warning is commented out.

Revised: the sentence on extrapolation corrected.

## rabu.f

No findings: the claims, the call from `MHDST1`'s loop over `IIDX` and the question hold.

No change.

## radsub.f

- **Missing.** `ESAC` calls `RADSUB` only when `IRAD = 1`; otherwise `ESAC` itself multiplies $c_V$ (`EOS(IRI(5))`) by `MOLES*APROP/TMASS`. Fix: add to "Who calls it".
- **Unclear.** Question 2 asks "or is this routine no longer used?". The routine is reached from `EQSTAT2` → `OEQOS` → `ESAC` when the old OPAL tables are chosen (`LOPALE`). Fix: drop that clause, name the path.

Revised: both applied.

## radsub01.f

- **Missing.** As for `RADSUB`: called only when `irad = 1`; otherwise `ESAC01` scales $c_V$ (`eos(iri(4))`) itself. Fix: add.
- **Missing question.** The `DATA` statement gives `sigmacc` and `aprop` single-precision literals (`1.8914785e-3`, `83.14510`, no `D` exponent) though both are REAL*8 by the `IMPLICIT`, so they carry only about 7 significant digits; `RADSUB` and `RADSUB06` use `D` constants. Fix: add a question.

Revised: both applied.

## radsub06.f

- **Wrong.** Question 3 says the `save` stands after the `DATA` statement "unlike the other versions"; in `RADSUB` and `RADSUB01` the `SAVE` also follows the `DATA` statement, and the placement is legal and harmless. Not a real question. Fix: cut it.

Revised: question 3 cut.

## rates.f

- **Missing.** Outputs say only that "`MIX` stores `HF2` in `HCOMPM(15,·)`". `MIX` copies all fifteen arrays (`HR1`…`HR13`, `HF1`, `HF2`) into `/BURN/ HCOMPM(1..15,·)`, and `ROTMIX` reads them back; `KEMCOM` gets all but `HR9`, `HR13`, `HF2`. Fix: say so.
- **Mathematics, missing.** The strong-screening form `USTR` is named but not written. Fix: add its equation.
- **Unclear question.** Question 3 ("swapped names … is `HF2` used anywhere") can be settled from the code: `HF2` is copied to `/BURN/` and back by `ROTMIX`, never used in a computation. Fix: state that and ask whether the Be7 branching should enter the abundance update.
- **Missing question.** When `TL ≤ TCUT(1)` the routine jumps to label 200 without setting `F1`, `F3`, so `HF1(IU)`, `HF2(IU)` get the values saved from the previous call (another shell). Fix: add a question.

Revised: all four applied.

## ratext.f

- **Unclear question, answerable from the code.** Question 1 asks what `BSSTEP` passes: `NV` = 1 or 3 from `ENVINT`, and `NUSE`, `IMAX` from `/INTPAR/` (namelist, defaults 7 and 11 in `PARMIN`). Fix: say so, and ask whether a namelist value above the array sizes should be checked.
- **Wrong question.** Question 2 (interleaving of `BSSTEP`'s and `LIBURN`'s sequences): each caller runs its whole sequence inside one call, and `IEST` = 1 restarts the tableau, so they cannot interleave. Fix: move to Design as a statement, cut the question.

Revised: both applied.

## rdlaol.f

- **Wrong question.** Question 3 says `ZDH` is overwritten later in `COEFFT` and `HSUBP` and asks whether the table's mix is used. Only `ZDH(1..3)` (C, N, O) are overwritten (also in `CRRECT`, `GETNEWENV`, `PHYSIC`, `SCONVEC`, `STARIN`, `WRTOUT`, `WRTMOD`); `ZDH(4..18)` keep the table's values and are used by `EQRELV`. Fix: rewrite the question (the mixed source of `ZDH`, not rescaled to the model's Z) and say in Outputs who uses `ZDH`.

Revised: applied.

## rdzlaol.f

No findings: the layout, the stop condition and the COMMON use hold.

No change.

## readalex06.f

No findings: the grids, the storage index (143 compositions), the checks and the questions hold (the exact comparisons of question 3 do pass for the current grid values, but the question stands for other tables).

No change.

## readco.f

No findings: the call from `ESAC` (guarded by `ITIME`), the unit 49 opened in `PARMIN`, the read layout, the inverse spacings and the questions hold.

No change.

## readcoeos01.f

- **Wrong (KC's changes).** "a `DO` loop … was rewritten": two loops were (labels 12 and 13). Fix.
- **Question answerable from the code.** Question 2 asks whether anything reads the tenth slot: `ESAC01` stops when `iorder` exceeds 9, so no. Fix: state it under The method, cut the question.

Revised: both applied.

## readcoeos06.f

- **Wrong (KC's changes).** Same as `READCOEOS01`: two `DO` loops (labels 12 and 13), not one. Fix.

Revised: applied.

## reduce.f

- **Wrong.** "The linearized system for the corrections has the coefficients $-\delta_{jk} \pm \tfrac{\Delta s}{2}\ln 10\,\partial f/\partial y$": the code has $-1 - \tfrac{\Delta s}{2}\ln10\,\partial f/\partial y$ at shell $i-1$ and $+1 - \tfrac{\Delta s}{2}\ln10\,\partial f/\partial y$ at shell $i$ (the sign of the identity changes, not of the derivative). Fix: write the linearized equation in full.
- **Wrong.** "What remains … expresses the corrections at shell $i$ in terms of two remaining unknowns, probably $\delta P$ and $\delta T$ of shell $i-1$": it is the reverse. From the algebra (and `HSOLVE`, which back-substitutes `PSTORE = HHB(1,IM) - QQQP*HHA(1,1,IM) - …` to get $\delta P_{i-1}$), `HHA(k,·,I)`, `HHB(k,I)` give $\delta P_{i-1}$, $\delta T_{i-1}$, $\delta R_i$, $\delta L_i$ in terms of $\delta P_i$, $\delta T_i$. Fix: give the column map and the final relation as an equation.
- **Unclear.** `HSOLVE` "probably the back-substitution": confirmed by its code. Fix: drop "probably".
- **Question answerable.** Question 3 (sign of the luminosity elimination): the plus sign follows because the coefficient of $\delta L_{i-1}$ in the $L$ row is $-1$ (no $\partial f_L/\partial L$ term), so `PIVOT` $=-1$. Fix: explain in the method, cut the question. Question 1 (meaning of the columns) reworded to ask for confirmation of the map now given.

Revised: all applied; Kronecker delta written $\epsilon_{yk}$ to avoid a clash with the corrections $\delta y$.

## remap.f

- **Wrong (KC's changes).** "`LSTRUCT_TIME` moved to the end": it now stands just before `LNEWVARS`. Fix.
- Checked and confirmed: question 1's bug (the denominators of `QS0E(2..7)`, `QQS0EE(4,5,7)` use `S0_1_1_A98` = 4.00e-22, giving factors of order $10^{-25}$).

Revised: the KC's-changes line corrected.

## rhoofp.f

- **Question answerable.** Question 3 asks whether `OEQOS` tests for $-999$ in every path: it does (`IF(R.LE.-998.0D0) RETURN 1`), and so do `OEQOS01`, `OEQOS06`. Fix: state it under Output, cut the question.

Revised: applied.

## rhoofp01.f

No findings: the call chain, the `NRA`/`KRA` disagreement (`6*115,8*113` against `9*115,5*113`) and the tolerance hold.

No change.

## rhoofp06.f

- **Format.** The author's tag is "MR 2025-10-10" in the code, "mr" in the note. Fix.
- **Missing question (minor).** `data sigmacc/1.8914785e-3/` is a single-precision literal (also in `RHOOFP01`); `RHOOFP` uses `D`. Fix: add a question.

Revised: both applied.

## rotgrid.f

No findings: the zone sums, the end zones, the Jacobian $d\chi/dr$ (checked term by term against `QCHIR`), the factors on `ECOD`, `ECOD2`, `ECOD3`, `ECOD4` and the four questions hold.

No change.

## rotmix.f

- **Unclear (units).** The settling time is written in years, but the code's `TSCALE` includes `CSECYR` and is in seconds, the unit of `DELTS`. Fix: say so.
- Checked and confirmed: the `MOD(DTMAX,DELTS)` question (one extra substep is always added), the unit-69 output, the stale message.

Revised: the units sentence added.

## rscale.f

- **Wrong (detail).** "a negative or zero value means 'no change'": for $Z$ the test is `RESCAL(3,NK).GE.0`, so zero is a valid target. Fix: say so.
- Checked and confirmed: the two horizontal-branch methods and their fixed points, the core rescaling, and the `ZFACT` bug of question 1.

Revised: applied.

## rtab.f

No findings: the read layout, the silent stops and the calls from `MHDST1` hold.

No change.

## sconvec.f

- **Missing question.** In the merger, the merged zone takes zone $j+1$'s top; if zone $j$'s top was extended past it, the merged zone shrinks. Fix: add a question (use the larger top).
- Checked and confirmed: $R_\mathrm{max}$ (with $L$ = `HL*CLSUN`, $P$, $r$ at `JMC`), the walk and its two stops, the unchanged `RL`, the write-back of `HD`.

Revised: question 6 added.

## search.f

No findings: the binary search, `FND`, `LCN`, the caller chain `OSPLIN` → `MEVAL` → `SEARCH` and KC's change hold.

No change.

## seculr.f

- **Missing.** Step 5 does not say that a region flagged by `ROTGRID` (`LDUM2`) is skipped, nor that for solid-body models (`LSOLID`, `IMPJMOD` = 1) the $\Omega$ solution is skipped while `NDIFCOM` still diffuses species 1–4. Fix: add both.
- Checked and confirmed: the centered shear formula (it reduces to $\Delta\Omega/\Delta\ln r$ at the geometric mean), the iteration, the wind branches, questions 1–5 (`LCODM`, `CODM` are local, undeclared; the final `NDIFCOM` uses the last region's `IBEG`, `IEND`, `ECOD2`, `EM`).

Revised: applied.

## setcal.f

No findings: the 48 runs, the copies, the hard-wired ages and the call from the main program with `FACAGE` hold.

No change.

## setkrz.f

- **Missing (detail).** The stop "KURUCZ INPUT ERROR" when a table has more than 60 temperatures is not mentioned. Fix: add a sentence.

Revised: applied.

## setllo.f

- **Wrong.** "A table with fewer rows ends the composition early (`END=93`)": `END=` fires only at the end of the file, so only the last composition may be short; a short composition in the middle would have its successor's header read as a data row. Fix: say so.

Revised: applied.

## setscal.f

- **Not a real question.** Question 3 (`ALRI = 0`, an integer literal for a REAL*8, "harmless") asks nothing. Fix: cut it.

Revised: question 3 cut.

## setscv.f

- **Unclear (mathematics).** In $S_\mathrm{mix}$, $n$, $n_{e,H}$, $n_{e,He}$ and the last term's $1/\delta$ are not defined. Fix: define them from `TNUM`, `HNUME`, `HENUME`, `DEI`.
- **Missing.** `QCPP` ($\partial\ln c_P/\partial\ln P$) is computed in the derivative loop but never stored. Fix: add to question 5.
- Checked and confirmed: the $dU/dT$ formula, the volume-additive density and derivatives, the stored columns 1–12, questions 1–4.

Revised: both applied.

## setup_grsett.f

- **Wrong.** "ends below a convective envelope, at the last shell with $Y >$ `YMIN`": the helium loop (labels 45–47) only checks that some shell at or below `IEND` has $Y >$ `YMIN`; unlike the hydrogen check (`IBEGIN = I`), it never resets `IEND`. Fix: say so, and ask whether `IEND = I` is missing after label 47.
- **Missing.** The coefficient loop (label 60) runs over all shells 1 to `M`, not only `IBEGIN`–`IEND`. Fix: add a sentence.
- **Missing.** With `ILAMBDA = 4`, $\ln\Lambda_{ij}$ goes only to `THDIFF` (helium, `LTHOUL` true, `LTHOULFIT` false); `FAC` and the metals' factor still divide by the default 2.2. With `ILAMBDA = 2`, `QCOD1X` gets an extra term from $d\ln\Lambda/dX$. Fix: add both.
- **Unclear.** "mass in $10^{-2}R_\odot^{-3}$ g units": the code multiplies masses by `CON_MASS` $=10^{-2}/R_\odot^3$ ($R_\odot$ in cm). Fix: say that.
- **Unclear.** Question 6 says the check "prints" the comment's words; the comment is not printed (the message is "Y BELOW … IN WHOLE MODEL-NO SETTLING"). Fix: reword.
- Checked and confirmed: the call from `GRSETT`, the COMMON blocks, the unit factors, the Noerdlinger and Loeb formulas, $D_1$, $D_2$ (`5X²+8X+3` = $(X+1)(5X+3)$), the Thoul fits, questions 1–5.

Revised: the range (the helium check does not move `IEND`; question 7 added), the loop over all shells, options 2 and 4 of $\ln\Lambda$, the mass unit and question 6 reworded.

## setupopac.f

- **Wrong (detail).** "by the switches in `/NEWOPAC/`": `LPUREZ` is in `/NWLAOL/`, not `/NEWOPAC/`. Fix: say so.
- Checked and confirmed: the calls and their order, `L2Z`, the low-temperature `ELSE IF` chain, the call from `SETUPS`, the question.

Revised: `LPUREZ` placed in `/NWLAOL/`.

## setups.f

No findings: the constants and their combinations (`CMKH`, `CDELRL`, `CDH`, `CMIXL3`), the Fermi, atmosphere and SCV reads, the users of `/CCR/`, `/ATMOS2C/`, `/SCVEOS/`, and questions 1–4 (`IMIN2(J) = NG` at line 306) hold.

No change.

## setupv.f

- **Unclear (mathematics).** In `FACT5`, $\beta_r = aT^4/(3P)$ is the ratio of radiation to total pressure, while the code's comment calls $1 -$ that ratio "BETA" (the usual gas-pressure fraction). Fix: name it $p_r$, the radiation-pressure fraction, and say that $1-p_r$ is the comment's $\beta$.
- Checked and confirmed: the call from `SECULR` (before its iterations), the interpolated interface values ($\nabla$ from $\nabla_\mathrm{rad}$, capped at $\nabla_\mathrm{ad}$), `DMIN`, `FACT1`–`FACT4`, `QWRMAX`, $\eta$, `THM`, `FES1`–`FES3`, and questions 1–4.

Revised: the radiation-pressure fraction in `FACT5` renamed $p_r$ and explained.

## shape.f

- **Missing.** When `JSTART` > 1, the integration starts from the caller's `ETA2(JSTART-1)` and, in the second pass, `R0(JSTART-1)`: both arrays are inputs as well as outputs. Fix: say so under Inputs.
- **Missing (question).** Neither the Newton loop (`ITFP2`) nor the outer loop (`ITFP1`) warns when it ends without converging; the last values are kept. Fix: add a question.
- Checked and confirmed: the callers, Radau's equation and the Runge–Kutta steps, the central value, the Newton step (its derivative $1 + \tfrac95A^2 - \tfrac{8}{35}A^3$ is right), and questions 1–3.

Revised: the inputs `ETA2(JSTART-1)`, `R0(JSTART-1)` noted; question 4 added.

## simeqc.f

No findings: the pivoting, the row swap and scaling, the elimination below the pivot, the back substitution (columns `N`+1 to `M`), the stop code 29, the call `SIMEQC(A,8,7)` from `KEMCOM` (line 316) and both questions hold.

No change.

## slopes.f

- **Unclear.** At the end nodes, "or $2m$ if the last two chords have opposite signs": $m$ is not defined. It is the end chord's slope (`M2` at the last node, `M1S`, the first chord, at the first). Fix: say so, and say that "the line" is the line through the neighbor node with that node's derivative.
- Checked and confirmed: the interior formula (both cases), the zero-slope test, the call from `OSPLIN`, the two `SAFEDIVIDE` calls, and questions 1–3.

Revised: the end-node rule reworded, with $m$ and "the line" defined.

## sneut.f

No findings: the `cap-cap` typo (line 125) and its reach (`tfac3` in the pair and photoneutrino terms, `tfac5` in bremsstrahlung; plasmon and recombination untouched) hold; so do the cut below $10^7$ K, $\lambda$, $\xi$, the pair formula, the photoneutrino ranges and zero floor, $T_F$ and the 0.01 test, the recombination range, the division by $\rho$ (with its derivative), the callers and questions 1–4.

No change.
