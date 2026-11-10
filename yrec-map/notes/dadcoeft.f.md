## Explanation

**Purpose.** This file solves the transport of angular momentum by rotational instabilities over one time step when advection by meridional circulation is included (the option `LDIFAD`, "combined diffusion/advection equation," MHP 06/02). Since the circulation velocity depends on $\Omega$ and its first three radial derivatives, it writes the problem as four first-order equations per shell and solves the resulting band system with [[bandw.f#BANDW|BANDW]]. It also returns the coefficient of composition mixing that results.

**How it fits.**
- **Inputs:** the arguments `DR` (the even grid's spacing), `DT` (time step), `EI` (moment of inertia of each grid point), `EW` ($\Omega$ at the start), `NTOT`, `WIND1`, `WIND2` (the wind's change of $\Omega$ at the start and end of the step, from [[cowind.f#COWIND|COWIND]] or [[mwind.f#MWIND|MWIND]] via the caller), `LFIX` (hold the surface $\Omega$ fixed). From modules: the velocity coefficients of the circulation and instabilities (`EV0`, `EV1A`, `EV1B`, `EV2A`, `EV2B`, `ECOD5`, `ECOD6`, `FGEOM`, `ESS`, `EGSF` in [[difad3_mod.f#DIFAD3_MOD|`DIFAD3_MOD`]]; `EQQCOD`, `EQQQCOD` in [[egridder_mod.f#EGRIDDER_MOD|`EGRIDDER_MOD`]]), of which only `EQQCOD` is set by another routine ([[vcirc.f#VCIRC|VCIRC]], [[vcirc.f#L272]]); the others are set nowhere (Bugs, by priority, 1); from [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]], the multipliers `FW`, `FC`, `FESC`, `FSSC`, `FGSFC` (formerly `/VMULT/`, `/VMULT2/`), `DJOK`, `ITDIF2` (formerly `/DIFUS/`), `WMAX`, `EXW` (formerly `/CWIND/`) and `LROSSBY`, `PMMSOLTAU` (the Rossby scaling of the saturation); `TAUCZ` in [[ovrtrn_mod.f#OVRTRN_MOD|`OVRTRN_MOD`]]. `QCHIRE` (formerly `/EGRIDCHI/`), `EWST`, `EQWRST` (formerly `/DIFADDT/`), `REQ` and `FGEOMIX` (formerly `/DIFAD4/`) are now local saved arrays, since those COMMON blocks were declared in no other file; none of them is ever set (Bugs, by priority, 1).
- **Who calls it:** [[seculr.f#SECULR|SECULR]], for each unstable region when `LDIFAD` is on (otherwise [[dcoeft.f#DCOEFT|DCOEFT]] sets up a tridiagonal diffusion system).
- **What it calls:** [[bandw.f#BANDW|BANDW]].
- **Outputs:** `DJ` (the change of angular momentum of each point), `SUMDJ` (their sum), `LOKAD` (converged), `ECOD2` (the composition diffusion coefficient); `ECOD3`, `ECOD4` in [[difad_mod.f#DIFAD_MOD|`DIFAD_MOD`]] (read by [[checkj.f#CHECKJ|CHECKJ]] for printing); `VESN`, now a local array (`/DIFAD4/` was read nowhere else). Many lines to the screen.

**The equation.** In the comment's words, the diffusion part is
$$\frac{\partial\Omega}{\partial t} = \frac{1}{4\pi\rho r^2}\,\frac{1}{I/M}\,\frac{\partial}{\partial r}\left(D\,\frac{\partial\Omega}{\partial r}\right),$$
and `LDIFAD` adds an advective term $\partial_r(\rho r^4 V\Omega)$, with $V$ a function of $\Omega$, $\Omega'$, $\Omega''$ and $\Omega'''$.

**The method.**
1. **Unknowns.** Four per shell, stored in order $\Omega$, $\Omega''$, $\Omega'$, $\Omega'''$; $NM = 4N - 2$ unknowns in all (the surface has two). Each row couples to unknowns up to 4 places before and 5 after, a band that BANDW handles.
2. **Rows.** For shell $i$: the $\Omega$ equation, implicit in time, with advective terms ($\tfrac12\Delta t/(I_i\,\Delta r)$ times `ECOD3`, `ECOD5`) and diffusive terms ($\Delta t/(I_i\Delta r)$ times `ECOD4`, `ECOD6`); then three rows that define the derivatives by finite differences (for example $\Omega'_i = (\Omega_{i+1} - \Omega_i)/\Delta r$). At the centre, no flux; at the surface, the same unless `LFIX`, which holds $\Omega$ fixed.
3. **Coefficients.** From the current $\Omega$ (`EWPREV`), with $\bar\Omega$ the interface mean (corrected by a second difference): $V_1 = f_w E_0\bar\Omega^2(E_{1a} + \bar\Omega^2E_{1b})$, $V_2 = f_w E_0\bar\Omega^2(E_{2a} + E_{2b})$; `ECOD3` $= 0.2\,V_1\,f_\mathrm{geom}$ and `ECOD4` $= (0.2\,V_2 + E_{SS} + E_{GSF})\,f_\mathrm{geom}$, not below zero. The shear and GSF terms are rescaled by $(\partial\Omega/\partial r)^2$ relative to the start.
4. **The wind.** The surface row's right-hand side is reduced by $\Delta J = -\tfrac12(W_1 + W_2)\,I_N\,(\Delta t_\mathrm{sub}/\Delta t)$. From the second outer iteration, `WIND2` is rescaled to the current surface $\Omega$ with the saturation law, $W_2 = W_{2,0}\,(\Omega_n^\mathrm{sat}/\Omega_p^\mathrm{sat})^{n-1}\,\Omega_n/\Omega_p$.
5. **Iterations.** Three nested loops: substeps (`NSTEP`), an outer iteration (`NNN`, meant for the $d\theta/dt$ term, now zero) and an inner iteration (`NN`) on the coefficients. Inner convergence: $\max|\Delta\Omega/\Omega| <$ `DJOK`. Each inner solution is rescaled so that total angular momentum is conserved exactly: $\Omega \leftarrow \Omega\,(J_0 + \Delta J)/J$.
6. **Step cutting.** If a correction exceeds 10% ($|\Delta\Omega/\Omega| > 0.1$) or the iterations fail, double the number of substeps and restart; after 5 cuts, `STOP 111`.
7. **Composition mixing.** From the final solution, the circulation velocity $V_\mathrm{tot}$ (`VTOT2`: the sum of the advective and diffusive terms, with the `ECOD4` term replaced by its circulation part alone, `V1E`, so that shear and GSF are not counted twice) and
$$D_\mathrm{mix} = \left(5\,|f_c f_{ES}\,V_\mathrm{tot}\,r_\mathrm{eq}| + f_c f_{SS}E_{SS} + f_c f_{GSF}E_{GSF}\right) f_\mathrm{geom,mix}.$$

**Design.** The header comments are those of [[dcoeft.f#DCOEFT|DCOEFT]] ("DCOEFT sets up…," "a tridiagonal matrix"), not updated for the band system. A residual check of the band solution (`C = AA·B`, [[#L428-L463]]) is computed but never compared with `D` (unused?). `WMINIT` and `QWRINIT` ([[#L215-L225]]) are read only in commented-out lines (unused?), and so are `EWST` and `EQWRST`, from which they are set. The damping factor `FX` is always 1 (the alternative is commented out). The time-derivative terms of $\theta$ (`VTHN`, `VTHP`) are all set to zero.

> **Question** ([[#L177-L179]], [[#L245-L264]]). **The $d\theta/dt$ term.** The outer iteration exists for it, but every version of the term is commented out or zero; the loop still rescales the wind and averages the iterates. Can the loop go, or is the term meant to come back?

> **Question** ([[#L268-L269]], [[#L604]]; [[rotgrid.f#L214]]). **Hard-coded factors.** The factors 0.2 in `ECOD3`/`ECOD4` (and in ROTGRID's `FAC`) and 5 in `VESN`, and the 10% limit on corrections ([[#L500]]). Where do the 0.2 and 5 come from (they are reciprocal)?

> **Question** ([[#L501-L502]], [[#L522]], [[#L529]], [[#L543-L546]], [[#L586]], [[#L600-L603]], [[#L613]]). **Screen output.** Several unconditional `WRITE(*,*)` per iteration (sums of $J$, iteration counters, the first and last 10 points). Debug leftovers, or should they go to a unit under a switch?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules or local arrays, `IMPLICIT NONE`, and the unused `/DEUTER/` gone. `LROSSBY` and `PMMSOLTAU` now come from `NMLPAR_MOD`, so the Rossby scaling of $\Omega_\mathrm{sat}$ applies here as in the wind routines; this settles the former question 1 (they were undeclared locals).

## Bugs, by priority

1. **(cannot be reached)** **The coefficients on the even grid are never set.** ([[#L244]]; [[#L265-L269]]; [[#L592-L606]]) DADCOEFT reads `EV0`, `EV1A`, `EV1B`, `EV2A`, `EV2B`, `ECOD5`, `ECOD6`, `FGEOM`, `ESS`, `EGSF` ([[difad3_mod.f#DIFAD3_MOD|`DIFAD3_MOD`]]), `EQQQCOD` ([[egridder_mod.f#EGRIDDER_MOD|`EGRIDDER_MOD`]]) and its local `QCHIRE`, `REQ`, `FGEOMIX`, and no routine at 7be4133 assigns any of them (a search of `src/` for assignments), so they are zero. Then `ECOD3` = `ECOD4` = 0 and every coupling through `QCHIRE` vanishes: the band system transports no angular momentum, and $\Omega$ changes only by the wind at the surface. After the solve, `V0 = ECOD3(I)/FGEOM(I)` is 0/0 ([[#L592]]): NaN in a release build, a floating-point trap in the developers' build (`-ffpe-trap=invalid`, `src/Makefile` line 61). The NaN passes to `VESN`, `DCMIX` and `ECOD2` (NaN times 0 is NaN), which SECULR passes to [[ndifcom.f#NDIFCOM|NDIFCOM]]; before the last iteration NDIFCOM gives it to MIXCOM to mix the composition ([[ndifcom.f#L64-L66]]). Only with `LDIFAD` (off by default; "experimental" in the Physics namelist page; no test case sets it, `KNOWN_ISSUES.md` issue 3).

    **A possible fix** (a choice for the developers): the arrays look like the even-grid versions of `FV0`…`FV2B`, `QQQCOD` (set by [[setupv.f#SETUPV|SETUPV]], [[setupv.f#L350-L354]], [[setupv.f#L435]]) and `DSS`, `DGSF` (set by VCIRC, [[vcirc.f#L631-L632]]) on the model's grid; either add the step that maps them onto the even grid, as [[rotgrid.f#ROTGRID|ROTGRID]] does for `COD`, or keep the stop that PARMIN now makes when `LDIFAD` is set with rotation ([[parmin.f#L999-L1006]]) until it exists.

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Cannot be reached at 7be4133. SECULR calls DADCOEFT only with `LDIFAD` ([[seculr.f#L390-L404]]), SECULR runs only with rotation, and PARMIN stops any run that sets `LDIFAD` with rotation ([[parmin.f#L999-L1006]]), with the message that DADCOEFT reads coefficients that no routine sets. No counting line fired in any case run, the five rotating test cases run (`testsuite/Test_3Msolar_GS_rot_gray_OPALSCV_SF2_GS98_OP_CF10_RGp2diffrotI3cz2`, `testsuite/Test_solarGS98_difrotmixper18p4d1p0`, `testsuite/Test_m0p8feh+0p0GS98_rotp8p0d0p1mag1e4std_TAMS`, `testsuite/Test_m2p0_feh+0p0_vzams150_IES1_TAMS`, and `testsuite/Test_m2p0_feh+0p0_vzams150_IES2_TAMS`) among them. The stop (added on Oct 29, 2026) is the developers' own diagnosis of this bug. What remains is code that no run takes; it matters again only when the mapping onto the even grid is written and the stop lifted.

2. **(cannot be reached)** **With `ITDIF2` = 1, the default, DADCOEFT always stops the run.** ([[#L179]]; [[#L558-L562]]; [[#L575-L585]]) The outer iteration accepts convergence only at `NNN.GE.2`; with `ITDIF2` = 1 there is no second iteration, so `LOKAD` is set false at the end of every substep, the step is cut five times, and the run ends with `STOP 111`. `ITDIF2` = 1 is the namelist default ([[nmlpar_mod.f#L72]]; "1=none" in the Physics namelist page); all 965 namelists in the repository set 10. Only with `LDIFAD` (off by default).

    **A possible fix:**

    ```diff
    --- a/src/dadcoeft.f
    +++ b/src/dadcoeft.f
    @@ -555,7 +555,12 @@
                 EWIT2(K) = 0.5D0*EWIT(K)+0.5D0*EWPREV(K)
              END DO
           ENDIF
    -      IF(ABS(DWI).LE.DJOK .AND. NNN.GE.2)THEN
    +C 11/09/26 KC via Claude
    +C code changed to accept the inner iteration's convergence when
    +C ITDIF2 = 1, since there is then no second outer iteration.
    +      IF(ITDIF2.EQ.1)THEN
    +         GOTO 9999
    +      ELSE IF(ABS(DWI).LE.DJOK .AND. NNN.GE.2)THEN
              GOTO 9999
           ELSE
              LOKAD = .FALSE.
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Cannot be reached at 7be4133: SECULR calls DADCOEFT only with `LDIFAD` ([[seculr.f#L390-L404]]) and runs only with rotation, and PARMIN stops any run that sets `LDIFAD` with rotation ([[parmin.f#L999-L1006]]), as for [[#b1]]; no counting line fired in any case run. What remains is code that no run takes. Even once these are set, `EQQCOD` is read on the even grid (index `II`, [[#L363-L365]]) while [[vcirc.f#VCIRC|VCIRC]] fills it shell by shell ([[vcirc.f#L272]]); the two indexings would have to be matched.

3. **(cannot be reached)** **Array bounds not checked.** ([[#L39]]; [[#L92]]; [[#L155]]; [[#L534-L535]]) The band system has `NM = 4*NTOT-2` rows in arrays of `NMAX` = 8000 (here and in [[bandw.f#BANDW|BANDW]]), so a region of more than 2000 even-grid points (`NTOT`, as many as the model has in the region, up to `JSON` = 5000) writes past them. The history `DWIT`, `IWIT` has 50 entries and is written at `NN` up to `ITDIF2`, so `ITDIF2` > 50 writes past it (CHECKJ's history is now sized from `ITDIF2`, [[checkj.f#L132-L135]]). Only with `LDIFAD` (off by default).

    **A possible fix:**

    ```diff
    --- a/src/dadcoeft.f
    +++ b/src/dadcoeft.f
    @@ -152,7 +152,14 @@
              QWR(I) = QCHIRE(I)*(EW(I)-EW(I-1))/DR
              WM0(I) = 0.5D0*(EW(I)+EW(I-1))
           END DO
    +C 11/09/26 KC via Claude
    +C code changed to stop when the band system or the iteration history
    +C would not fit in their arrays.
           NM = 4*NTOT-2
    +      IF(NM.GT.NMAX .OR. ITDIF2.GT.50)THEN
    +         WRITE(*,*)'DADCOEFT: NTOT OR ITDIF2 TOO LARGE ',NTOT,ITDIF2
    +         STOP 112
    +      ENDIF
     C LOOP FOR TIMESTEP CUTTING
      5    CONTINUE
           SUMDT = 0.0D0
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Cannot be reached at 7be4133: SECULR calls DADCOEFT only with `LDIFAD` ([[seculr.f#L390-L404]]) and runs only with rotation, and PARMIN stops any run that sets `LDIFAD` with rotation ([[parmin.f#L999-L1006]]), as for [[#b1]]; no counting line fired in any case run. What remains is code that no run takes.

4. **(cannot be reached)** **A failed substep is not cut.** ([[#L183]]; [[#L558-L564]]; [[#L575]]) When a substep ends without convergence (its last inner iteration did not converge, or the outer iteration ran out), it goes on to label 9999 with `LOKAD` false; the next substep sets `LOKAD = .FALSE.` again and may end with it true. Only the last substep's `LOKAD` decides the cut at label 950, so an unconverged substep is kept without a message. Only with `LDIFAD` (off by default).

    **A possible fix:**

    ```diff
    --- a/src/dadcoeft.f
    +++ b/src/dadcoeft.f
    @@ -562,6 +562,10 @@
           ENDIF
           END DO
      9999 CONTINUE
    +C 11/09/26 KC via Claude
    +C code changed to cut the step when any substep fails, not only the
    +C last one.
    +      IF(.NOT.LOKAD) GOTO 950
           DO K = 1,NTOT
              EWT(K) = EWPREV(K)
           END DO
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Cannot be reached at 7be4133: SECULR calls DADCOEFT only with `LDIFAD` ([[seculr.f#L390-L404]]) and runs only with rotation, and PARMIN stops any run that sets `LDIFAD` with rotation ([[parmin.f#L999-L1006]]), as for [[#b1]]; no counting line fired in any case run. What remains is code that no run takes.

5. **(cannot be reached)** **An unset entry in the printed history.** ([[#L212]]; [[#L534]]; [[#L544]]) When the inner loop runs out without converging, `NN` is `ITDIF2+1` at label 900, so `WRITE(*,100)` prints `DWIT(ITDIF2+1)`, which this pass never set (a value from an earlier call, or zero). Output only.

    **A possible fix:**

    ```diff
    --- a/src/dadcoeft.f
    +++ b/src/dadcoeft.f
    @@ -541,7 +541,9 @@
           END DO
      900  CONTINUE
           WRITE(*,*)NNNN,NNN,NN
    -      WRITE(*,100)DWW,IWW,(DWIT(J),IWIT(J),J=1,NN)
    +C 11/09/26 KC via Claude
    +C code changed to print only the iterations done in this pass.
    +      WRITE(*,100)DWW,IWW,(DWIT(J),IWIT(J),J=1,MIN(NN,ITDIF2))
      100  FORMAT(' MAX D(OMEGA)/OMEGA',1PE12.3,' AT PT.',I5,
          *   ' BY ITERATION'/5(1X,E11.3,I4))
           IF(NNN.LE.2)THEN
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): Cannot be reached at 7be4133: SECULR calls DADCOEFT only with `LDIFAD` ([[seculr.f#L390-L404]]) and runs only with rotation, and PARMIN stops any run that sets `LDIFAD` with rotation ([[parmin.f#L999-L1006]]), as for [[#b1]]; no counting line fired in any case run. What remains is code that no run takes.

### DADCOEFT

Implicit advection–diffusion of angular momentum on the even grid: four unknowns per shell ($\Omega$ and three derivatives) in a band system solved by [[bandw.f#BANDW|BANDW]]; iterates on $\Omega$-dependent coefficients, enforces angular-momentum conservation with the wind, cuts the substep on failure, and returns `DJ`, `SUMDJ`, `LOKAD` and the composition coefficient `ECOD2`.
