## Explanation

**Purpose.** `GRSETT` computes the gravitational settling of helium (and, with `LDIFZ`, of the metals) over one time step, "using the formalism of Bahcall and Loeb 1989" (its comment). The code solves for the divergence of a flux, in mass (as [[lax_wendrof1.f#LAX_WENDROF1|`LAX_WENDROF1`]] differences it),
$$\frac{\partial X}{\partial t} = 4\pi\,\frac{\partial}{\partial m}\Bigl[D_1 + D_2\,\frac{\partial X}{\partial r}\Bigr],\qquad D_1 = f\,\frac{r^2T^{5/2}}{\ln\Lambda}\,X\,(A_P + A_T\nabla)\,\frac{d\ln P}{dr},\qquad D_2 = f\,\frac{r^2T^{5/2}}{\ln\Lambda}\,A_C,$$
where $r$ is in $R_\odot$ and $T$ in $10^7$ K (Bahcall and Loeb's units), $A_P$, $A_T$, $A_C$ are the coefficients of the pressure, temperature and concentration gradients (`AP`, `AT`/$\nabla$, `AC`, from Thoul et al. with `LTHOUL`; without it, Bahcall and Loeb's fits in $X$), $f$ the user's factor (below), and $D_1$, $D_2$ are `COD1`, `COD2` from `SETUP_GRSETT`. The first term is advective (settling at a velocity proportional to $d\ln P/dr$), the second diffusive; the code's comment, a first term "that depends on DLNP/DR*DX/DR" and a second "on D^2X/DR^2," describes them only loosely. The factor $f$ is `FGRY` for helium and `FGRZ` for the metals (namelist settings, default 1), and with `LTHOUL` also `CSTMIXING` (and `CSTDIFFMIX` on the metals' settling term), factors added in 10/09 to "mimic mixing to reduce settling" (their $X$-derivatives are not scaled: [[setup_grsett.f#b1]]). `GRSETT` treats the first term explicitly with a two-step Lax–Wendroff scheme and the second implicitly, iterating on the coefficients.

**How it fits.**
- **Who calls it:** [[mix.f#MIX|`MIX`]] and [[rotmix.f#ROTMIX|`ROTMIX`]], the mixing drivers of the evolution step.
- **Inputs:** `DT0` (time step, s), `HCOMP` (mass fractions; `HCOMP(1)` = $X$, `HCOMP(2)` = $Y$, `HCOMP(3)` = $Z$), `HQPR0` = $d\ln P/dr$, `HR` = $\log r$, `HD` = $\log\rho$ (passed on to `SETUP_GRSETT`, which needs it for the Coulomb logarithm), `HS10` = $m$ (g, not logged), `HT` = $\log T$, `LC` (convective or not), `M`, `STOT0`. `GRSETT` copies `DT0`, `STOT0`, `HS10` and `HQPR0` into its own `DT`, `STOT`, `HS1`, and `HQPR`, which `SETUP_GRSETT` converts to Bahcall and Loeb's units in place and `EQUAL_TO_MODEL` converts back, so the caller's values are not changed.
- **Output:** the new `HCOMP(1)` and `HCOMP(2)`, and with `LDIFZ` `HCOMP(3)` ($Z$, the CNO rows scaled with it) (via [[equal_to_model.f#EQUAL_TO_MODEL|`EQUAL_TO_MODEL`]], which uses $X+Y+Z=1$).
- **Calls, in order:** [[setup_grsett.f#SETUP_GRSETT|`SETUP_GRSETT`]] (the coefficients `COD1`, `COD2` and their $X$-derivatives, the convection-zone edges, and whether the model is fully convective), [[model_to_equal.f#MODEL_TO_EQUAL|`MODEL_TO_EQUAL`]] (to an equally spaced grid in radius), [[lax_wendrof1.f#LAX_WENDROF1|`LAX_WENDROF1`]] and [[lax_wendrof2.f#LAX_WENDROF2|`LAX_WENDROF2`]], then in each iteration [[get_imp_diffco.f#GET_IMP_DIFFCO|`GET_IMP_DIFFCO`]] and [[tridiag_gs.f#TRIDIAG_GS|`TRIDIAG_GS`]], and at the end `EQUAL_TO_MODEL`.
- **Modules** (COMMON blocks until `rp_1`): `NMLPAR_MOD` for the settings `GRTOL`, `NITER_GS` (formerly `/GRAVST/`, set by [[parmin.f#PARMIN|`PARMIN`]]) and `LDIFZ` (formerly `/GRAVS3/`); `GRAVEZ_MOD` (the metals on the equal grid, with the Lax–Wendroff pair and the regridding routines); `CONSTANTS_MOD`; `IOUNITS_MOD` (the output units). The metals' coefficients `COD1Z`, `COD2Z`, `QCOD1Z`, `QCOD2Z` (formerly `/GRAVSZ/`) are now `GRSETT`'s own arrays, filled by `SETUP_GRSETT` and passed to `MODEL_TO_EQUAL`.

**The method.**
1. Set up the coefficients; return at once for a fully convective model. Settling is computed only between the edge of a convective core (or the centre, or the first shell with $X >$ `XMIN`) and the base of the surface convection zone (or, if helium is too scarce there, the first shell below it with $Y >$ `YMIN`): `IBEGIN` and `IEND`. What lies beyond them is not on the grid; each side acts as one reservoir at the grid's end (the boundary cells of `LAX_WENDROF1` hold all the mass beyond the grid), and every shell below `IBEGIN` (a convective core, or a hydrogen-exhausted region, which may be radiative) and above `IEND` gets the change found at the grid's end point (step 5); for a convective zone this keeps it homogeneous.
2. Move to $N$ (`NPT`) equally spaced radii $r_i$ (step $\Delta r$), with values at the points (`E…`) and at the midpoints (`E…_H`). Keep the starting $X_i^0$ (`EX_ORIG`).
3. **Explicit term.** `LAX_WENDROF1` gives the half-step changes $\Delta X_{i+1/2}$; the midpoint coefficients are linearized in them,
$$F_{i+1/2} \leftarrow F_{i+1/2} + \Delta X_{i+1/2}\,\frac{\partial F}{\partial X}\Big|_{i+1/2},$$
and `LAX_WENDROF2` applies the full step, giving $X'_i$ (`EX_PRIME`).
4. **Implicit term.** With $\alpha_i = 4\pi\Delta t/(\Delta r\,\Delta m_i)$ (`ALPHA`; $\Delta m_i$ the mass between midpoints, $m_{1/2}$ at the centre and $M - m_{N-1/2}$ at the surface), iterate up to `NITER_GS` times: take the change at the midpoints $\tfrac12(X_i + X_{i-1} - X^p_i - X^p_{i-1})$ since the previous iterate $X^p$; let `GET_IMP_DIFFCO` build the tridiagonal coefficients $a_i, b_i, c_i$ from `ECOD2_H` corrected by that change; solve
$$a_i X_{i-1} + b_i X_i + c_i X_{i+1} = X'_i$$
with `TRIDIAG_GS`. With $D_{i+1/2}$ = `ECOD2_H(I)` (the coefficient between points $i$ and $i+1$), the rows are those of an implicit (backward Euler) step:
$$\bigl(1+\alpha_i(D_{i-1/2}+D_{i+1/2})\bigr)X_i - \alpha_i D_{i-1/2}X_{i-1} - \alpha_i D_{i+1/2}X_{i+1} = X'_i,$$
with $D_{1/2} = D_{N+1/2} = 0$ (no flux through the centre or the surface). Stop when $\max_i (X_i - X^p_i) <$ `GRTOL`, the largest signed change ([[#b2]]); print each iteration's largest change. The change at the midpoints is stored one index off from the coefficients it corrects ([[#b1]]).

    > **Question** ([[#L247-L253]]). **Failure is only reported.** When the iteration does not converge in `NITER_GS` steps, `GRSETT` writes a message and carries on with the last iterate. Should it stop the run, or shorten the settling step and retry? How often the message appears in the `.short` files of settling runs would show whether it matters.
5. Return the change $X_i - X_i^0$ (and $Z_i - Z_i^0$), which `EQUAL_TO_MODEL` interpolates back to the model's points (the change rather than the abundance, "to minimize errors from the interpolation"). `ZZ1` and `ZZ2`, the metals' changes at the two ends ([[#L260-L261]]), are computed and never read (unused?).

**Design.** Each iteration writes a line to the short output (`ISHORT`). The metals get the explicit term only; the implicit iteration is for $X$ alone.

> **Question** ([[#L80-L82]]; [[#L178-L185]]; [[model_to_equal.f#L180-L181]]). **The metals' diffusion term.** The header still says "settling of metals will be added later," though metal settling came in 3/94 (`LDIFZ`), for the explicit term only: `SETUP_GRSETT` computes the metals' $D_2$ (`COD2Z`) and `MODEL_TO_EQUAL` interpolates it to the midpoints (`ECOD2Z_H`), but nothing reads it. Should the metals also get the implicit term? Comparing the surface $Z$ of a solar model with and without it would show whether it matters.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html): `GRTOL` (default 1.0D-8) is the numerical tolerance on the abundance changes from diffusion, and `NITER_GS` (10) the largest number of iterations of the solver.

**Changed since `rp_1`.** The metals' coefficient arrays (formerly `/GRAVSZ/`) are local and passed to `SETUP_GRSETT` and `MODEL_TO_EQUAL` as new arguments; otherwise declarations only: COMMON blocks to modules, `IMPLICIT NONE`. No question settled.

**Changed since `a8a5950`.** The arguments `DT`, `HQPR`, `HS1`, and `STOT` are now `DT0`, `HQPR0`, `HS10`, and `STOT0`, copied on entry, so that the unit conversion and its inverse (which need not restore a value to the last bit) no longer change the structure's mass coordinate or [[mix.f#MIX|`MIX`]]'s sub-step.

## Bugs, by priority

1. **(not reached)** **The coefficient correction is one midpoint off.** ([[#L213-L215]]; [[get_imp_diffco.f#L19-L21]]) In the iteration, loop 30 sets `EX_H(I)`, for `I` = 2..`NPT`, to the change at the midpoint between points `I-1` and `I`; but [[get_imp_diffco.f#GET_IMP_DIFFCO|`GET_IMP_DIFFCO`]] adds `EQCOD2X_H(I)*EX_H(I)` to `ECOD2_H(I)`, the coefficient between points `I` and `I+1` (its matrix uses `ECOD2_H(I-1)` on the left of point `I` and `ECOD2_H(I)` on the right, and `MODEL_TO_EQUAL` puts `ECOD2_H(1)` at `ER(1)` + $\Delta r/2$: [[model_to_equal.f#L76]]). `ECOD2_H(1)` also gets `EX_H(1)`, which loop 30 never sets: it keeps the half-step change from `LAX_WENDROF1` ([[lax_wendrof1.f#L45-L47]]), and is added again at every iteration. What follows: Each diffusion coefficient is corrected with its neighbour's change in $X$, and the first one drifts by the same amount per iteration; the size of the effect was not estimated. Only with `LDIFY` (off by default; set by `LDIFZ` and `LDIFLI`) and `LNEWDIF` false (the default, but `LDIFLI` sets it true).

    **A possible fix:**

    ```diff
    --- a/src/grsett.f
    +++ b/src/grsett.f
    @@ -210,8 +210,12 @@
           DO 100 ITER=1,NITER_GS
     C  FIND CHANGE IN X AT THE ZONE MIDPOINTS, GIVEN CHANGE IN X AT
     C  THE ZONE CENTERS.
    +C 11/09/26 KC via Claude
    +C code changed to store the change at the midpoint between points I-1
    +C and I in EX_H(I-1), the index of that midpoint's coefficient
    +C ECOD2_H(I-1) in GET_IMP_DIFFCO.
              DO 30 I = 2,NPT
    -            EX_H(I) = 0.5D0*(EX(I)+EX(I-1)-EX_P(I)-EX_P(I-1))
    +            EX_H(I-1) = 0.5D0*(EX(I)+EX(I-1)-EX_P(I)-EX_P(I-1))
      30      CONTINUE
     C  STORE CURRENT RUN OF HYDROGEN ABUNDANCES IN VECTOR EX_P. THE ITERATION
     C  LOOP IS COMPLETED ONCE EX - EX_P IS EVERYWHERE LESS THAN THE TOLERANCE
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): not reached in any of 34 runs (26 of YREC's cases, from 0.04 to 9 $M_\odot$, with rotation, settling, and helium burning, and 8 made-up ones). These lines belong to the old settling routines (`LNEWDIF` false), which no case uses: Every case with settling sets `LNEWDIF` and `LDIFLI`, and the documentation lists `LNEWDIF` among the legacy options (`docs/source/namelist_physics.md`, line 285). Reaching them takes `LDIFY` or `LDIFZ` with `LNEWDIF` false and `LDIFLI` off, since `LDIFLI` forces `LNEWDIF` on ([[parmin.f#L1239-L1251]]); the size of the effect is still to be measured in such a run. Intent: none found.

2. **(not reached)** **The convergence test ignores negative changes.** ([[#L233-L246]]) `DXMAX` is the largest signed change $X_i - X^p_i$, starting from 0, not the largest $|X_i - X^p_i|$; so an iteration whose changes are all negative, or whose positive changes are below `GRTOL`, is taken as converged however large its negative changes are, and the message prints the largest positive change. What follows: The iteration can stop before it has converged. Same path as [[#b1]]: the old settling routines, with `LDIFY` (set by `LDIFZ` and `LDIFLI`) and `LNEWDIF` false.

    **A possible fix:**

    ```diff
    --- a/src/grsett.f
    +++ b/src/grsett.f
    @@ -232,8 +232,10 @@
     C  ENOUGH TO EXIT.
              DXMAX = 0.0D0
              IMAX = 0
    +C 11/09/26 KC via Claude
    +C code changed to test the size of the change, not its sign.
              DO 50 I = 1,NPT
    -            DX = EX(I)-EX_P(I)
    +            DX = ABS(EX(I)-EX_P(I))
                 IF(DX.GT.DXMAX)THEN
                    DXMAX = DX
                    IMAX = I
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): not reached in any of the 34 runs, for the reason given in [[#b1]]: No case uses the old settling routines (`LNEWDIF` false), and `LDIFY` or `LDIFZ` with `LNEWDIF` false and `LDIFLI` off would reach it. Intent: none found.

### GRSETT

Settling of He (and metals) in one step: regrid to equal radii, explicit Lax–Wendroff for the settling term, implicit iterated tridiagonal solve for the diffusion term, regrid the change back (above).
