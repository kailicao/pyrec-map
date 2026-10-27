## Explanation

**Purpose.** Computes the moment of inertia `HI` of each shell of a rotating, distorted model, and its derivative with respect to the angular velocity, `QIW` $= dI/d\Omega$. The comment: "Moment of inertia is calculated by the method used in Wai-Yuen Law's thesis (Yale, 1980) p.61", and "MOMI assumes that SHAPE has already been called".

**How it fits.**
- **Inputs:** the shape parameters `ETA2` and `R0` per shell (from [[shape.f#SHAPE|SHAPE]], probably the distortion parameter and the radius of the equivalent sphere, as the names suggest); $\log r$ (`HR`), $\log m$ (`HS`), the shell masses `HS2`, the angular velocities `OMEGA`, and the shell range `JSTART..JEND`.
- **Who calls it:** [[hpoint.f#HPOINT|HPOINT]], [[solid.f#SOLID|SOLID]] and [[starin.f#STARIN|STARIN]].
- **What it calls:** [[intmom.f#INTMOM|INTMOM]], which evaluates the integral at each shell.
- **Outputs:** `HI` and `QIW` per shell.
- **Modules:** `NMLPAR_MOD` (`WALPCZ`), `CONSTANTS_MOD` (`CLN`, `CC13`, `CC23`, and $\log G$, `CGL`), `DIMENSIONS_MOD` (`JSON`). The unused `/CCOUT/` and `/LUOUT/` of `rp_1` are no longer declared.

**The method.**
- **Spherical shortcut.** If `WALPCZ` $\ne 0$ (`WALPCZ` is the exponent of the rotation law $\Omega\, r^{\mathrm{WALPCZ}} =$ constant in the surface convection zone, as [[getnewenv.f#GETNEWENV|GETNEWENV]]'s comment says; [[parmin.f#PARMIN|PARMIN]] keeps it between −2 and 0, so 0 is solid-body rotation), each shell is a thin spherical shell, $I = \tfrac23\,\Delta m\, r^2$, with $dI/d\Omega = 0$; the central shell is a sphere, $I = 0.4\,\Delta m\, r^2$, at the mean of the first two $\log r$.
- **Distorted shells.** Otherwise, for each shell, with $r_0$ = `R0`, the parameter
$$A = \frac{5}{3}\,\frac{\Omega^2\, r_0^3}{G\,m\,(2 + \eta_2)}$$
(`CON` $=5/(3G)$), the ratio `R0R` $= r_0^5/r^3$, and `QR0R` $= d\ln r_0/d\ln r$ set to 1, go to `INTMOM`, which returns $I$ and $dI/d\Omega$ per unit mass; these are multiplied by `HS2`.

**KC's changes.** 2025-05-31: the unused arguments `HD` and `M` removed.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **Unused values.** `R0P` and `RPHIP` (the previous shell's $\ln r_0$ and $\ln r$) and `H0` (the thin-shell moment of inertia) are computed in each pass but never used, and `QR0R` is fixed at 1. Were they meant for a derivative $d\ln r_0/d\ln r$ between shells?
2. **`WALPCZ` as a switch.** The spherical shortcut is taken for every shell in `JSTART..JEND`, not only those in the convection zone, whenever the convection zone's rotation law is not solid-body (`WALPCZ` $\ne 0$). Why should that law switch off the distortion of all shells?
