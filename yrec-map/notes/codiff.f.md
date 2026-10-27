## Explanation

**Purpose.** This file computes the diffusion coefficients for rotational mixing: one for angular-momentum transport (`COD`) and one for composition transport (`COD2`), from the characteristic velocities of the rotational instabilities, at each interface between shells.

**How it fits.**
- **Inputs:** the arguments `HRU` (the radius of each shell's midpoint, not logged) and `M`; the velocities `VES` (Eddington–Sweet circulation, probably), `VGSF` (Goldreich–Schubert–Fricke instability) and `VSS` (secular shear) in [[temp2_mod.f#TEMP2_MOD|`TEMP2_MOD`]], computed by [[vcirc.f#VCIRC|VCIRC]]; the variable $f_c$, the argument `VFC` (SECULR's array, filled by [[getfc.f#GETFC|GETFC]]); in [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]], the multipliers `FW`, `FC`, `FESC`, `FGSFC`, `FSSC`, the switch `LVFC`, the constant background coefficient `CODM`, `LCODM`, and `LNOJ`. All options are set in [[parmin.f#PARMIN|PARMIN]].
- **Who calls it:** [[seculr.f#SECULR|SECULR]].
- **Outputs:** `COD`, `COD2` and `RMID` (arguments); `HLE` in `TEMP2_MOD`, set to zero.
- **Unused:** the local arrays `FADV`, `FADV0` (formerly `/ADVEC/`, declared only here).

**The method.** Element $i$ refers to the interface between shells $i-1$ and $i$, at $r_{\mathrm{mid},i} = \tfrac12(r_i + r_{i-1})$. With $v = v_\mathrm{ES} + v_\mathrm{GSF} + v_\mathrm{SS}$:
$$D_J = 4\pi f_w\, v\, r_\mathrm{mid}, \qquad D_X = 4\pi f_w f_c \left(f_{ES}\,v_\mathrm{ES} + f_{GSF}\,v_\mathrm{GSF} + f_{SS}\,v_\mathrm{SS}\right) r_\mathrm{mid},$$
or, with a variable $f_c$ (`LVFC`), $D_X = D_J\,f_c(r)$. With `LCODM`, a constant `CODM` is added to $D_J$ ($4\pi f_w\,\mathrm{CODM}$; "MHP 9/14", "MHP 8/13"). With `LNOJ`, $D_J = 0$: composition is mixed but angular momentum is not transported (MHP 9/93). So the coefficient is a velocity times a length, the radius, probably in cm$^2$ s$^{-1}$ before the factor $4\pi$.

**KC's changes.** 2025-05-30: the elements of `/MAG/` reordered. 2025-05-31: the unused arguments `DELTS`, `HV`, `IMIN`, `IMAX`, `LC`, `LCZ` removed.

**Changed since `rp_1`.** `VFC` is now an argument (`/VARFC/` retired); COMMON blocks to modules (the unused `/INTVAR/` and `/MDPHY/` dropped, `/ADVEC/` made local), `IMPLICIT NONE`.

## Questions for the experts

1. **The background coefficient and composition.** `CODM` is added to $D_J$ only, never to $D_X$, in both branches. Is a constant background mixing of angular momentum without mixing of composition intended?
2. **The length scale.** The coefficient uses the radius $r$ as the length scale; the header says the routine "determines the run of characteristic velocity length scales", but `HLE` is set to zero (the line `HLE(I)=RMID(I)` is commented out). The only reader is [[checkj.f#CHECKJ|CHECKJ]]'s print (column "LENGTH"), which is switched off. Should `HLE` and that column be removed, or the length scale restored?
3. **The $\mu$-gradient.** `NMLPAR_MOD` holds `FMU` and `IMU`, and `TEMP2_MOD` `VMU`, but they do not enter here. [[vcirc.f#VCIRC|VCIRC]] sets `VMU = 0`; its comment says the $\mu$ terms were replaced by $(\nabla + \nabla_\mu - \nabla_\mathrm{ad})$, and `IMU` is kept "for later use". `FMU` and `IMU` are still namelist inputs, unused. Should they be removed?
4. **`COD(1)`.** No routine sets `COD(1)` or `COD2(1)`; the readers start at element 2 (MIXGRID from `COD2(IBEG+1)`). Worth a check that no reader ever reaches element 1.

### CODIFF

Diffusion coefficients for angular momentum, $D_J = 4\pi f_w (v_\mathrm{ES} + v_\mathrm{GSF} + v_\mathrm{SS})\,r$, and for composition, $D_X$ (with the extra factors $f_c$ and per-mechanism weights), at the interfaces; options for a constant background and for no angular-momentum transport.
