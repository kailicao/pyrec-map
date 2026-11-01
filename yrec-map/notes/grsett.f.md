## Explanation

**Purpose.** `GRSETT` computes the gravitational settling of helium (and, with `LDIFZ`, of the metals) over one time step, "using the formalism of Bahcall and Loeb 1989" (its comment). The code solves for the divergence of a flux, in mass (as [[lax_wendrof1.f#LAX_WENDROF1|`LAX_WENDROF1`]] differences it),
$$\frac{\partial X}{\partial t} = 4\pi\,\frac{\partial}{\partial m}\Bigl[D_1 + D_2\,\frac{\partial X}{\partial r}\Bigr],\qquad D_1 = f\,\frac{r^2T^{5/2}}{\ln\Lambda}\,X\,(A_P + A_T\nabla)\,\frac{d\ln P}{dr},\qquad D_2 = f\,\frac{r^2T^{5/2}}{\ln\Lambda}\,A_C,$$
where $r$ is in $R_\odot$ and $T$ in $10^7$ K (Bahcall and Loeb's units), $A_P$, $A_T$, $A_C$ are the coefficients of the pressure, temperature and concentration gradients (`AP`, `AT`/$\nabla$, `AC`, from Thoul et al. with `LTHOUL`; without it, Bahcall and Loeb's fits in $X$), $f$ the user's factor (below), and $D_1$, $D_2$ are `COD1`, `COD2` from `SETUP_GRSETT`. The first term is advective (settling at a velocity proportional to $d\ln P/dr$), the second diffusive; the code's comment, a first term "that depends on DLNP/DR*DX/DR" and a second "on D^2X/DR^2", describes them only loosely. The factor $f$ is `FGRY` for helium and `FGRZ` for the metals (namelist settings, default 1), and with `LTHOUL` also `CSTMIXING` (and `CSTDIFFMIX` on the metals' settling term), factors added in 10/09 to "mimic mixing to reduce settling". `GRSETT` treats the first term explicitly with a two-step Lax–Wendroff scheme and the second implicitly, iterating on the coefficients.

**How it fits.**
- **Who calls it:** [[mix.f#MIX|`MIX`]] and [[rotmix.f#ROTMIX|`ROTMIX`]], the mixing drivers of the evolution step.
- **Inputs:** `DT` (time step, s), `HCOMP` (mass fractions; `HCOMP(1)` = $X$, `HCOMP(2)` = $Y$, `HCOMP(3)` = $Z$), `HQPR` = $d\ln P/dr$, `HR` = $\log r$, `HD` = $\log\rho$, `HS1` = $m$ (g, not logged), `HT` = $\log T$, `LC` (convective or not), `M`, `STOT`.
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
with $D_{1/2} = D_{N+1/2} = 0$ (no flux through the centre or the surface). Stop when $\max_i (X_i - X^p_i) <$ `GRTOL`; print each iteration's largest change.
5. Return the change $X_i - X_i^0$ (and $Z_i - Z_i^0$), which `EQUAL_TO_MODEL` interpolates back to the model's points (the change rather than the abundance, "to minimize errors from the interpolation").

**Design.** Each iteration writes a line to the short output (`ISHORT`). The metals get the explicit term only; the implicit iteration is for $X$ alone.

**KC's changes.** 2025-05-31: the call to `MODEL_TO_EQUAL` no longer passes `HQPR` and `HTU`.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html): `GRTOL` (default 1.0D-8) is the numerical tolerance on the abundance changes from diffusion, and `NITER_GS` (10) the largest number of iterations of the solver.

**Changed since `rp_1`.** The metals' coefficient arrays (formerly `/GRAVSZ/`) are local and passed to `SETUP_GRSETT` and `MODEL_TO_EQUAL` as new arguments; otherwise declarations only: COMMON blocks to modules, `IMPLICIT NONE`. No question settled.

## Questions for the experts

1. **The convergence test ignores negative changes.** `DXMAX` is the largest signed $X_i - X^p_i$, not its absolute value, so an iteration whose changes are all negative is taken as converged at once. Should it be `ABS(DX)`?
2. **Stale comment.** "Settling of metals will be added later": metal settling was added in 3/94 (`LDIFZ`), for the explicit term only. Should the metals also get the implicit term?
3. **Unused.** `ZZ1` and `ZZ2` (the metals' changes at the two ends) are computed and not used; the argument `HD` is passed on but `GRSETT` itself does not use it.
4. **The coefficient correction is one midpoint off.** In the iteration, `EX_H(I)` (`I` = 2..`NPT`) is the change at the midpoint between points `I-1` and `I`, but [[get_imp_diffco.f#GET_IMP_DIFFCO|`GET_IMP_DIFFCO`]] adds `EQCOD2X_H(I)*EX_H(I)` to `ECOD2_H(I)`, the coefficient between points `I` and `I+1` (its matrix uses `ECOD2_H(I-1)` on the left of point `I` and `ECOD2_H(I)` on the right). `ECOD2_H(1)` also gets the stale `EX_H(1)` left by `LAX_WENDROF1`. Should the loop set `EX_H(I-1)` instead?
5. **Failure is only reported.** When the iteration does not converge, `GRSETT` writes a message and carries on with the last iterate.
6. **`CSTMIXING` in the derivatives.** With `LTHOUL`, [[setup_grsett.f#SETUP_GRSETT|`SETUP_GRSETT`]] multiplies `COD1` and `COD2` by `CSTMIXING`, but not their $X$-derivatives `QCOD1X`, `QCOD2X`, which linearize them in steps 3 and 4. With `CSTMIXING` $\ne 1$ the linearization is then inconsistent with the coefficients. Intended?

### GRSETT

Settling of He (and metals) in one step: regrid to equal radii, explicit Lax–Wendroff for the settling term, implicit iterated tridiagonal solve for the diffusion term, regrid the change back (above).
