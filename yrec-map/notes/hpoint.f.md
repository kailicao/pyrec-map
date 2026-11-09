## Explanation

**Purpose.** `HPOINT` rezones the model: at the start of each step it chooses a new set of mass points so that the jumps between neighbours in mass, luminosity, pressure, $X$ and $Z$ stay below user limits, keeps real discontinuities (convection-zone edges, composition jumps) as fixed points, and interpolates every model variable to the new points. It also adds or removes outer points when the outermost point drifts out of the allowed envelope temperature range, and recomputes the shell masses and, for rotating models, the rotation quantities.

**How it fits.**
- **Who calls it:** the main program, [[main.f#(file level)|main.f]], once per evolutionary step.
- **Inputs (arguments, changed in place):** the model (`HS` = $\log m$, `HP`, `HT`, `HR`, `HL`, `HD`, `HCOMP`, `LC`, `M`), `HSTOT` ($\log M_*$), the envelope-fitting values `PS`, `RS`, `ESTORE`, `ISTORE`, the indices `JCORE`, `JENV` (edges of the convective core and envelope), `JXBEG` (H-shell base), `LSHELL`, the model number `MODEL`, the rotation arrays (`OMEGA`, `ETA2`, `R0`, `HI`, `HJM`, `HKEROT`, `FP`, `FT`, `HG`, `QIW`), the totals `SJTOT`, `SKEROT`, `TEFFL`, and `CMIXL` (the run's mixing-length parameter, which main.f sets from `CMIXLA(NK)`; passed on to `PHYSIC`).
- **Outputs:** the rezoned model; `HS1` (mass at each point) and `HS2` (mass of each shell); `LRESET` (true when outer points were added or removed); and in modules, the previous model on the new grid for the next step.
- **Calls:** [[splinc.f#SPLINC|`SPLINC`]] and [[splintd2.f#SPLINTD2|`SPLINTD2`]] (splines to place the points), [[osplin.f#OSPLIN|`OSPLIN`]] (an "oscillatory" spline for interpolating the variables); for rotation [[ovrot.f#OVROT|`OVROT`]], [[momi.f#MOMI|`MOMI`]], [[getrot.f#GETROT|`GETROT`]], [[fpft.f#FPFT|`FPFT`]]; [[physic.f#PHYSIC|`PHYSIC`]] (the physics at the new points); [[surfopac.f#SURFOPAC|`SURFOPAC`]] (a new surface opacity table when surface $X$ changed).
- **Modules, the main ones:** [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] (the namelist parameters: `HPTTOL(1..12)`, the zoning limits, from [[parmin.f#PARMIN|`PARMIN`]]; `TENV0`, `TENV1`; `LEXCOM`, whether light elements 12–15 are followed; `LROT`; the overshoot settings `LOVSTE`, `ALPHAE`; the debug output `LDEBUG`, `NPOINT`); [[oldmod_mod.f#OLDMOD_MOD|`OLDMOD_MOD`]] (after the rezoning, `HSS`, `HPO`, `HTO`, `HRO`, `HLO`, `HDO` and `HCOMPP` hold the start-of-step model on the new grid, and `TEFFLO`, `HLSURO` the start-of-step $T_\mathrm{eff}$ and surface luminosity, saved before the rezoning; read by [[kemcom.f#KEMCOM|`KEMCOM`]], [[liburn.f#LIBURN|`LIBURN`]], [[lirate88.f#LIRATE88|`LIRATE88`]], [[crrect.f#CRRECT|`CRRECT`]] and others); [[entrop_mod.f#ENTROP_MOD|`ENTROP_MOD`]] (the previous step's rates of change of $\log T$, $\log P$, $\ln L$, $\log r$, which main.f uses for its first guess of the new structure; shared with main.f only); [[deuter_mod.f#DEUTER_MOD|`DEUTER_MOD`]] (`DRATE0`); [[oldrot_mod.f#OLDROT_MOD|`OLDROT_MOD`]], [[oldrot2_mod.f#OLDROT2_MOD|`OLDROT2_MOD`]], [[oldphy_mod.f#OLDPHY_MOD|`OLDPHY_MOD`]], [[dwmax_mod.f#DWMAX_MOD|`DWMAX_MOD`]] (rotation and the physics at the start of the step, for the angular-momentum transport in [[getw.f#GETW|`GETW`]] and [[midmod.f#MIDMOD|`MIDMOD`]]); [[scrtch_mod.f#SCRTCH_MOD|`SCRTCH_MOD`]], [[temp_mod.f#TEMP_MOD|`TEMP_MOD`]] (the physics just computed by `PHYSIC`); [[comp_mod.f#COMP_MOD|`COMP_MOD`]] (`XNEW`, `ZNEW`, `SENV`); [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]]; [[iounits_mod.f#IOUNITS_MOD|`IOUNITS_MOD`]] (`ISHORT`, `IOWR`, `IDEBUG`); `JSON` from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]]; 14 modules in all.

**The method.**
1. **Outer boundary.** If $\log T$ at the outermost point is below `TENV0`, drop the outer points down to the first one hotter than `TENV0` (and put the dropped mass into the envelope, `SENV`). If it is above `TENV1`, add one point from the stored envelope integration: $\Delta\log P$ from `ESTORE`, $\Delta\log T = 0.25\,\Delta\log P$, $\Delta\log r$ from `ESTORE`, the same $L$ and composition, and $\log\rho = \log P - \log T - 8$.

    > **Question** ([[#L169-L180]]; [[envint.f#L806-L813]]). **The added outer point.** $\Delta\log T = 0.25\,\Delta\log P$ and $\log\rho = \log P - \log T - 8$ are rough, hard-coded guesses, while `ESTORE(2)` holds $\log T$ at the stored envelope point. Are they only starting values for the next Henyey iteration, and would `ESTORE(2)` give a better one?

    > **Question** ([[#L148-L186]]; [[nmlpar_mod.f#L184-L185]]). **`TENV0`, `TENV1`: stop or adjust?** The documentation says the code stops when the envelope's temperature is outside $[$`TENV0`, `TENV1`$]$; `HPOINT` instead drops the outer points cooler than `TENV0` (stopping only if the whole model is cooler) and adds one point from the stored envelope when the outermost point is hotter than `TENV1`. With the default `TENV1` = 9.0, a point is added only if the outermost point is hotter than $10^9$ K. Is the documentation describing an older behavior?

2. **Fixed points.** Flag the edge of the convective core, the base of the convective envelope, the base of the H shell, every point where $|\Delta X|$ > `HPTTOL(3)`, $|\Delta Z|$ > `HPTTOL(4)`, or (rotating models) $|\Delta\log\Omega|$ > `HPTTOL(12)`, the base of envelope overshoot and the base of a finely zoned region around the envelope's base (`HPTTOL(7)` in $\log P$). At most 100 flags; sort them and remove duplicates.

    > **Question** ([[#L190-L228]]; [[#L247-L293]]). **Flags beyond 100.** The convection-zone edges and the H-shell base are flagged first, but when the composition and $\Omega$ tests reach 100 flags, the code jumps (`GOTO 130`) past the flags for the base of envelope overshoot and the base of the finely zoned region. Should those two be flagged before the gradient tests? (When the tests stop just short of 100, the two can run past the array: bug 2.)

3. **New mass points.** Build a cumulative "distance" along the star,
$$\chi_j = \chi_{j-1} + \frac{\Delta\log m}{\delta_m} + \frac{\Delta L}{\delta_L} - \frac{\Delta\log P}{\delta_P},$$
with $\delta_m$ = `HPTTOL(2)`, $\delta_L$ = `HPTTOL(9)` times the largest $L$, and $\delta_P$ = `HPTTOL(10)` in the finely zoned region, `HPTTOL(11)` below it, `HPTTOL(8)` in the convective envelope (the $L$ term only where $L$ increases outward). Between consecutive flagged points, place points evenly in $\chi$, one per unit, and find their masses from a spline of $\log m$ against $\chi$. The idea: $\chi$ adds up the changes of $\log m$, $L$ and $\log P$ along the star, each in units of its tolerance, so that between neighbouring new points their sum is one tolerance; points crowd where any of the three changes fast. The code also sets `PMAX1`–`PMAX5` (by their comment, the largest $\Delta\log P$ in each region), `HPMAX(1)`, `IIFLG`, `I0`, and, for rotating models, $\log\Omega$ in `OMEGAL`, and declares `ID(7)` with its `DATA`; nothing reads them (unused?), and the placement uses `HPTTOL` directly ([[#L229-L239]]; [[#L325-L333]]; [[#L353]]; [[#L359-L361]]; [[#L128]]; [[#L137]]).
4. **Refinement in X and Z.** Where $X$ increases outward between new points by more than `HPTTOL(5)`, or $Z$ decreases outward by more than `HPTTOL(6)`, insert evenly spaced points, stopping the run (`STOP 1`) if they would take the model past `JSON` points. Then drop points closer than `HPTTOL(1)` in $\log m$.
5. **Convection flags.** Relocate `JCORE` and `JENV` on the new grid and reset `LC`.
6. **Interpolation.** With `OSPLIN`, interpolate to the new points: the entropy-term variables (`ENTROP`), the composition `HCOMP` and the starting composition `HCOMPP`, the deuterium burning rate `DRATE0`, then $\log P$, $\log r$, $L$, $\log T$, $\log\rho$, and for rotating models $\Omega$, $j$, $f_P$, $f_T$, $r_0$, $\eta_2$; and the energy generation at the start of the step when needed (see bug 1).

    > **Question** ([[#L648-L665]]). **Is rezoning conservative?** Step 6 interpolates $X$, $Z$ and the isotopes with `OSPLIN` to the new mass points; spline interpolation does not conserve $\int X\,dm$, and over thousands of steps the error could accumulate (in the total helium, say, or in lithium). Is the total mass of each species checked after `HPOINT`, and how large is the drift over a main-sequence run?

7. **Masses.** With $m_i = 10^{\log m_i}$:
$$\texttt{HS1}_i = m_i,\qquad \texttt{HS2}_i = \tfrac12\,(m_{i+1} - m_{i-1}),\qquad \texttt{HS2}_1 = \tfrac12(m_2 + m_1),\qquad \texttt{HS2}_M = M_* - \tfrac12(m_{M-1}+m_M).$$
8. **Rotation.** First guess of the moment of inertia $I_i = \tfrac23\,\Delta m_i\,r_i^2$; overshoot zones (`OVROT`); moment of inertia (`MOMI`); $\Omega$ from the conserved specific angular momentum (`GETROT`); the distortion terms (`FPFT`); `MOMI` again; then the totals $J = \sum j_i\Delta m_i$ and $K = \sum \tfrac12\Omega_i j_i \Delta m_i$, printed against the previous ones; and the old rotation state saved in `OLDROT`.

    > **Question** ([[#L782-L787]]). **The JNT comment.** JNT (2025-09-03) added the first call to `MOMI`, before `GETROT`, with the comment "WALPCZ does run in this version but I don't think it can hurt". Is the extra `MOMI` call still needed?

9. **Physics at the start of the step** (rotating models, or light elements with envelope overshoot): `PHYSIC` at the new points; the results stored in `OLDPHY`, `DWMAX`, and the shear term
$$\theta_i = \frac{\bar r^{\,4}}{G\,\bar m}\,\bar\Omega\,\frac{\Delta\Omega}{\Delta r}$$
(`THO`, with geometric means of $r$ and $m$ over the two points) and $d\Omega/dr$ (`QWRST`) in `OLDROT2`.
10. A new surface opacity table (`SURFOPAC`) if surface $X$ changed by more than $10^{-8}$.

**Design.** It prints the flag points and the old and new numbers of points to the short output every step, and a full table of old and new points to the debug unit every `NPOINT` models when `LDEBUG` is on. Several module arrays of the old model (`HPO`, `HTO`, `HDO`) serve as scratch space before receiving their final contents.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) (Rarely used options) gives `TENV0` and `TENV1` (defaults 3.0 and 9.0, in $\log T$) as the minimum and maximum temperature of the envelope integration, and says "Code stops below this" and "Code stops above this". The mesh tolerances `HPTTOL` that `HPOINT` applies are documented under their newer names on [[remap.f#REMAP|REMAP's page]].

**Changed since `rp_1`.** `CMIXL` is a new argument, passed on to `PHYSIC` (it was in `/CONST3/`); COMMON blocks to modules, `IMPLICIT NONE`; the namelist parameters it reads (from `/CTOL/`, `/CTLIM/`, `/DPMIX/`, `/FLAG/`, `/ROT/`, `/CCOUT1/`, `/CCOUT2/` before) now come from `NMLPAR_MOD`, and unused declarations are gone. No question is settled.

**Changed since `a8a5950`.** The $X$ and $Z$ insertions of step 4 stop (`STOP 1`) before running past `JSON` (settles former question 1); the previous model's surface luminosity is saved as `HLSURO` in place of the point count `MO`, for [[entime.f#ENTIME|`ENTIME`]] (settles former question 6); `DRATE0` is moved onto the new mesh unconditionally, since the old gate (`LEXCOM` and surface deuterium $\ge 10^{-14}$) read `HCOMP(12,M)` on the new mesh with the old `M` and, when it failed, left `DRATE0` in old-mesh order; the regrid of `HCOMPM`, which nothing read, is gone with `BURN_MOD` (removed since `a8a5950`); the store of `DDELM`, which [[setupv.f#SETUPV|`SETUPV`]] overwrites before use, is dropped; and the stop when the whole model is cooler than `TENV0` is `STOP 1` (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(a)** **The start-of-step energy generation is interpolated against the new mass points.** ([[#L602]]; [[#L733-L740]]; [[#L751-L758]]) The block "MHP 6/00 interpolated in energy generation at start of timestep" runs after loop 1000 has copied the new points `HSS` into `HS`, so `OSPLIN` fits `SESUM` and `SESUM + SEG(6,·) + SEG(7,·)`, which are on the old points, against `HS(1..MNEW)` (the new points) and, when the old model had more points, the old `HS(MNEW+1..M)` after them, whose masses are then not increasing. `ESUMO` and `EPSO` thus hold roughly the old values copied index by index, shifted wherever points were added or removed. What follows: MIDMOD interpolates `ESUMM` and `EPSM` from them ([[midmod.f#L159]]; [[midmod.f#L166-L168]]), which SETUPV ([[setupv.f#L155-L156]]) and the rotational mixing grids ([[mixgrid.f#L156]]; [[rotgrid.f#L251]]) use, in rotating runs (`LROT`, off by default) and with `LEXCOM` and `LOVSTE`. Read from the code, not run. **A possible fix** (the block moved before loop 1000):

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to interpolate the energy generation at the start of the
    C timestep before HS takes the new points, so that SESUM is fitted
    C against its own (old) mass points.
    C MHP 6/00 INTERPOLATED IN ENERGY GENERATION AT START OF TIMESTEP
          IF(LROT .OR. (LEXCOM .AND. LOVSTE))THEN
             CALL OSPLIN(HSS,ESUMO,HS,SESUM,NTAB,NTOT)
             DO IM = 1,M
                YTAB(IM) = SESUM(IM)+SEG(6,IM)+SEG(7,IM)
             END DO
             CALL OSPLIN(HSS,EPSO,HS,YTAB,NTAB,NTOT)
          ENDIF
    C TRANSFER NEW POINTS.
          DO 1000 J = 1,MNEW
    ...
     1000 CONTINUE
    ...
          WRITE(ISHORT,1020) M,MNEW
    ```

2. **(b)** **The flag array can overflow.** ([[#L73]]; [[#L223-L227]]; [[#L264-L267]]; [[#L287-L290]]; [[#L294]]) `NFLAG` has 100 elements, and the gradient tests stop at `IFLAG` = 100; but when they end with `IFLAG` = 99, the base of the overshoot region and the base of the finely zoned region are flagged after them, and label 130 writes `NFLAG(101)` = `M`, past the array, which the sort then reads. This needs `LOVSTE` and a nonzero `HPTTOL(7)` (both off by default), a convective envelope, and exactly 98 flags set before them. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to add the overshoot and fine-zoning flags only while
    C NFLAG has room for them and for M.
    ...
                IF(JOS.GT.1 .AND. IFLAG.LT.100)THEN
                   NFLAG(IFLAG) = JOS
                   IFLAG = IFLAG + 1
                ENDIF
    ...
                IF(JFINE.GT.1 .AND. IFLAG.LT.100)THEN
                   NFLAG(IFLAG) = JFINE
                   IFLAG = IFLAG + 1
                ENDIF
    ```

3. **(c)** **`ALPHAE` taken as a depth in $\log_{10}P$.** ([[#L252-L255]]; [[main.f#L803-L804]]) The base of envelope overshoot is the first point where $\log_{10}P - \log_{10}P(\texttt{JENV}) >$ `ALPHAE`. The documentation gives `ALPHAE` as the "envelope overshoot in pressure scale heights", and main.f uses it so (`PSCAL0` = `ALPHAE` $\cdot H_p$); an overshoot of $\alpha H_p$ is about $\Delta\ln P = \alpha$, that is $\Delta\log_{10}P \approx 0.43\,\alpha$. The point flagged as the base of the overshoot region is thus about 2.3 times deeper in $\log P$ than the overshoot, which changes only where the mesh keeps a fixed point (`PMAX3`, computed from it, is unused). With `LOVSTE` (off by default). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to measure the overshoot depth ALPHAE in pressure scale
    C heights, as a change of ln P, not of log P.
              DO 191 JOS = JENV-1,1,-1
                 IF(HP(JOS)-HP(JENV).GT.ALPHAE/CLN)GOTO 193
      191       CONTINUE
    ```

4. **(c)** **The debug table prints new values under "old points".** ([[#L436-L441]]; [[#L493-L499]]; [[#L648-L655]]; [[#L713-L720]]) Under the heading "OLD POINTS", the columns X, Z, and O16 print `HKO`, `HFO`, and `HCOMP(9,·)`: `HKO` and `HFO` hold $X$ and $Z$ interpolated at the new points (before the $X$ and $Z$ insertions of step 4), and `HCOMP` has already been moved to the new points (loop 850). The comments also say these values go into `HIO` and `HGO`. Only with `LDEBUG` (off by default). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to keep the old X, Z and O16 for the debug table, which
    C printed values at the new points under OLD POINTS.
          DO J = 1,M
             HKO(J) = HCOMP(1,J)
             HFO(J) = HCOMP(3,J)
             YTAB(J) = HCOMP(9,J)
          END DO
          DO 850 I = 1,IEND
    ...
             WRITE(IDEBUG,920) (I,HS(I),HP(I),HT(I),HR(I),HL(I),
         *   HKO(I),HFO(I),YTAB(I),I,HSS(I),HPO(I),HTO(I),
         *   HRO(I),HLO(I),HCOMP(1,I),HCOMP(3,I),HCOMP(9,I), I = 1,MINMIN)
    ...
                WRITE(IDEBUG,930) (I,HS(I),HP(I),HT(I),HR(I),HL(I),
         *      HKO(I),HFO(I),YTAB(I),I=MINMIN,M)
    ```

5. **(d)** **A third equal flag survives.** ([[#L309-L320]]) After removing a duplicate, the loop still advances `I`, so the entry moved into place is not compared with the one before it, and of three equal flags in a row two remain. The duplicate makes the placement add a point at almost the same $\chi$, hence the same mass ([[#L398-L419]]), which the removal of points closer than `HPTTOL(1)` ($10^{-8}$ in $\log m$ by default) then deletes ([[#L542-L556]]); so this is correct today, but a zero `HPTTOL(1)` would leave two points at the same mass. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to compare the entry moved into place with the one
    C before it, so that no flag is kept twice.
          I = 2
      160 CONTINUE
          IF(NFLAG(I).EQ.NFLAG(I-1))THEN
           IF(I.LT.IFLAG) THEN
              DO 170 J = I,IFLAG-1
                 NFLAG(J) = NFLAG(J+1)
      170       CONTINUE
           ENDIF
           IFLAG = IFLAG - 1
          ELSE
           I = I + 1
          ENDIF
          IF(I.LE.IFLAG) GOTO 160
    ```

### HPOINT

Rezoning: fixed points, even spacing in the cumulative variable $\chi$, refinement in $X$ and $Z$, interpolation of all variables, new shell masses, and the rotation and start-of-step physics on the new grid (above).
