## Explanation

**Purpose.** `GRSETT` computes the gravitational settling of helium (and, with `LDIFZ`, of the metals) over one time step, "using the formalism of Bahcall and Loeb 1989" (its comment). The diffusion equation has two terms: one in $d\ln P/dr \cdot dX/dr$ (settling) and one in $d^2X/dr^2$ (diffusion). `GRSETT` treats the first explicitly with a two-step Lax–Wendroff scheme and the second implicitly, iterating on the coefficients.

**How it fits.**
- **Who calls it:** [[mix.f#MIX|`MIX`]] and [[rotmix.f#ROTMIX|`ROTMIX`]], the mixing drivers of the evolution step.
- **Inputs:** `DT` (time step, s), `HCOMP` (mass fractions; `HCOMP(1)` = $X$, `HCOMP(2)` = $Y$, `HCOMP(3)` = $Z$), `HQPR` = $d\ln P/dr$, `HR` = $\log r$, `HD` = $\log\rho$, `HS1` = $m$ (g, not logged), `HT` = $\log T$, `LC` (convective or not), `M`, `STOT`.
- **Output:** the new `HCOMP(1)` and `HCOMP(2)` (via [[equal_to_model.f#EQUAL_TO_MODEL|`EQUAL_TO_MODEL`]], which uses $X+Y+Z=1$).
- **Calls, in order:** [[setup_grsett.f#SETUP_GRSETT|`SETUP_GRSETT`]] (the coefficients `COD1`, `COD2` and their $X$-derivatives, the convection-zone edges, and whether the model is fully convective), [[model_to_equal.f#MODEL_TO_EQUAL|`MODEL_TO_EQUAL`]] (to an equally spaced grid in radius), [[lax_wendrof1.f#LAX_WENDROF1|`LAX_WENDROF1`]] and [[lax_wendrof2.f#LAX_WENDROF2|`LAX_WENDROF2`]], then in each iteration [[get_imp_diffco.f#GET_IMP_DIFFCO|`GET_IMP_DIFFCO`]] and [[tridiag_gs.f#TRIDIAG_GS|`TRIDIAG_GS`]], and at the end `EQUAL_TO_MODEL`.
- **COMMON blocks:** `GRAVST` (`GRTOL`, `NITER_GS`; set by [[parmin.f#PARMIN|`PARMIN`]], shared with the microdiffusion routines, `MIX`, `ROTMIX`, `PUTSTORE`, the output writers), `GRAVS3` (`LDIFZ`), `GRAVEZ` (the metals on the equal grid, with the Lax–Wendroff pair and the regridding routines), `CONST1`, `LUOUT`.

**The method.**
1. Set up the coefficients; return at once for a fully convective model.
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

## Questions for the experts

1. **The convergence test ignores negative changes.** `DXMAX` is the largest signed $X_i - X^p_i$, not its absolute value, so an iteration whose changes are all negative is taken as converged at once. Should it be `ABS(DX)`?
2. **Stale comment.** "Settling of metals will be added later": metal settling was added in 3/94 (`LDIFZ`), for the explicit term only. Should the metals also get the implicit term?
3. **Unused.** `ZZ1` and `ZZ2` (the metals' changes at the two ends) are computed and not used; the argument `HD` is passed on but `GRSETT` itself does not use it.
4. **The coefficient correction is one midpoint off.** In the iteration, `EX_H(I)` (`I` = 2..`NPT`) is the change at the midpoint between points `I-1` and `I`, but [[get_imp_diffco.f#GET_IMP_DIFFCO|`GET_IMP_DIFFCO`]] adds `EQCOD2X_H(I)*EX_H(I)` to `ECOD2_H(I)`, the coefficient between points `I` and `I+1` (its matrix uses `ECOD2_H(I-1)` on the left of point `I` and `ECOD2_H(I)` on the right). `ECOD2_H(1)` also gets the stale `EX_H(1)` left by `LAX_WENDROF1`. Should the loop set `EX_H(I-1)` instead?
5. **Failure is only reported.** When the iteration does not converge, `GRSETT` writes a message and carries on with the last iterate.

### GRSETT

Settling of He (and metals) in one step: regrid to equal radii, explicit Lax–Wendroff for the settling term, implicit iterated tridiagonal solve for the diffusion term, regrid the change back (above).
