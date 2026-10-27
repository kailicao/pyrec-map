## Explanation

**Purpose.** `GTPURZ` returns the opacity from the LAOL89 table for pure metals ($Z = 1$), with its derivatives, at a given density and temperature.

**How it fits.** Called only by [[getopac.f#GETOPAC|`GETOPAC`]], when $Z > 0.1$ and $\log T > 7.7$ (its comment: "Z > 0.10, T > 5 × 10⁷ K"; it stops if no pure-$Z$ table was read, `LPUREZ`): `GETOPAC` then interpolates $\log\kappa$ and its derivatives linearly in $Z$ between a normal table (at `ZIT`) and this pure-$Z$ table ($Z = 1$). The table is in the modules `ZLAOL_MOD` (read by [[rdzlaol.f#RDZLAOL|`RDZLAOL`]]) and `ZSLAOL_MOD` (its density splines, from [[zsulaol.f#ZSULAOL|`ZSULAOL`]]), COMMON blocks until `rp_1`; it takes `TOLLAOL` from `NMLPAR_MOD` (formerly `/NWLAOL/`) and the output unit from `IOUNITS_MOD`. Calls `LOCATE`, `XRNG4`, `CSPLINE`, `SPLINT`.

**The method.** As in `GTLAOL` (removed since `rp_1`) but without the composition step: a spline in $\log\rho$ at each of four temperatures (with linear extrapolation within the margin $\ln$ `TOLLAOL`), then a natural spline in $\log T$; chord slopes for the derivatives; $\log\kappa$ capped at 35.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`, the local `TOLL` renamed `TOLLOG`, and the unused `/SLAOL/` no longer declared (question 1 of `rp_1`, now settled and removed).

## Questions for the experts

1. **Natural log for the margin.** `LOG(TOLLAOL)` is a natural log; is that intended? (The same question was raised for `GTLAOL`, removed since `rp_1`.)

### GTPURZ

Opacity of a pure-metal mixture: spline in $\rho$, then in $T$.
