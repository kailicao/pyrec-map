## Explanation

**Purpose.** This file computes the diffusion coefficients for rotational mixing: one for angular-momentum transport (`COD`) and one for composition transport (`COD2`), from the characteristic velocities of the rotational instabilities, at each interface between shells.

**How it fits.**
- **Inputs:** the arguments `HRU` (the radius of each shell's midpoint, not logged) and `M`; the velocities `VES` (meridional circulation), `VGSF` (Goldreich–Schubert–Fricke instability) and `VSS` (secular shear) in [[temp2_mod.f#TEMP2_MOD|`TEMP2_MOD`]], computed by [[vcirc.f#VCIRC|VCIRC]]; the variable $f_c$, the argument `VFC` (SECULR's array, filled by [[getfc.f#GETFC|GETFC]]); in [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]], the multipliers `FW`, `FC`, `FESC`, `FGSFC`, `FSSC`, the switch `LVFC`, the constant background coefficient `CODM`, `LCODM`, and `LNOJ`. All options are set in [[parmin.f#PARMIN|PARMIN]].
- **Who calls it:** [[seculr.f#SECULR|SECULR]].
- **Outputs:** `COD`, `COD2` and `RMID` (arguments); `HLE` in `TEMP2_MOD`, set to zero.
- **Unused:** the local arrays `FADV`, `FADV0` (formerly `/ADVEC/`, declared only here).

**The method.** Element $i$ refers to the interface between shells $i-1$ and $i$, at $r_{\mathrm{mid},i} = \tfrac12(r_i + r_{i-1})$. With $v = v_\mathrm{ES} + v_\mathrm{GSF} + v_\mathrm{SS}$:
$$D_J = 4\pi f_w\, v\, r_\mathrm{mid}, \qquad D_X = 4\pi f_w f_c \left(f_{c,\mathrm{ES}}\,v_\mathrm{ES} + f_{c,\mathrm{GSF}}\,v_\mathrm{GSF} + f_{c,\mathrm{SS}}\,v_\mathrm{SS}\right) r_\mathrm{mid},$$
with $f_{c,\mathrm{ES}}$, $f_{c,\mathrm{GSF}}$, $f_{c,\mathrm{SS}}$ = `FESC`, `FGSFC`, `FSSC`, as on VCIRC's page; or, with a variable $f_c$ (`LVFC`), $D_X = D_J\,f_c(r)$. The two sets of factors differ: `FES`, `FGSF`, `FSS` scale the velocities in VCIRC; `FESC`, `FGSFC`, `FSSC` weight each mechanism's share of composition mixing only. With `LCODM`, a constant `CODM` is added to $D_J$ ($4\pi f_w\,\mathrm{CODM}$; "MHP 9/14", "MHP 8/13"). With `LNOJ`, $D_J = 0$: composition is mixed but angular momentum is not transported (MHP 9/93). So the coefficient is a velocity times a length, the radius: $v\,r$ is in cm$^2$ s$^{-1}$, and the factor $4\pi$ belongs to the form in which the equation is solved: [[rotgrid.f#ROTGRID|ROTGRID]] multiplies the coefficients by $\rho r^4\,d\chi/dr$ and $I/(mr^2)$ (its comment: "a factor of 4PI has already been included in CODIFF"), giving the $D$ of [[dcoeft.f#DCOEFT|DCOEFT]]'s equation.

**KC's changes.** 2025-05-30: the elements of `/MAG/` reordered. 2025-05-31: the unused arguments `DELTS`, `HV`, `IMIN`, `IMAX`, `LC`, `LCZ` removed.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) (Angular momentum transport): `LCODM` adds a magnetic diffusion term `CODM` to angular-momentum transport (0 is pure hydrodynamics; 9e4 matches the constraints on the solar core's rotation; the code's default is 2.5e4); `FW` scales all angular-momentum diffusion coefficients, and `FC` the mixing coefficients relative to them, usually calibrated on lithium depletion (in clusters or the Sun). `LVFC`, experimental, is the variable-`FC` model of Zahn (1991).

**Changed since `rp_1`.** `VFC` is now an argument (`/VARFC/` retired); COMMON blocks to modules (the unused `/INTVAR/` and `/MDPHY/` dropped, `/ADVEC/` made local), `IMPLICIT NONE`.

## Questions for the experts

1. **The background coefficient and composition.** `CODM` is added to $D_J$ only, never to $D_X$, in both branches. Is a constant background mixing of angular momentum without mixing of composition intended?
2. **The length scale.** The coefficient uses the radius $r$ as the length scale; the header says the routine "determines the run of characteristic velocity length scales", but `HLE` is set to zero (the line `HLE(I)=RMID(I)` is commented out). The only reader is [[checkj.f#CHECKJ|CHECKJ]]'s print (column "LENGTH"), which is switched off. Should `HLE` and that column be removed, or the length scale restored?
3. **The $\mu$-gradient.** `VMU` and `FMU` act in [[vcirc.f#VCIRC|VCIRC]] (with `IMU = 3`, restored MHP 4/26), which subtracts the $\mu$ currents from `VES` and `VGSF` before they reach CODIFF; so the $\mu$ terms enter here only through those velocities, and `VMU` itself is not read. Is that the intended route?
4. **`COD(1)`.** No routine sets `COD(1)` or `COD2(1)`; the readers start at element 2 (MIXGRID from `COD2(IBEG+1)`). Worth a check that no reader ever reaches element 1.

### CODIFF

Diffusion coefficients for angular momentum, $D_J = 4\pi f_w (v_\mathrm{ES} + v_\mathrm{GSF} + v_\mathrm{SS})\,r$, and for composition, $D_X$ (with the extra factors $f_c$ and per-mechanism weights), at the interfaces; options for a constant background and for no angular-momentum transport.
