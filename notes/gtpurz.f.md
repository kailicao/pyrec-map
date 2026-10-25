## Explanation

**Purpose.** `GTPURZ` returns the opacity from the Livermore table for pure metals ($Z = 1$), with its derivatives, at a given density and temperature.

**How it fits.** Called only by [[getopac.f#GETOPAC|`GETOPAC`]], when $Z > 0.1$ and $\log T > 7.7$ (its comment: "Z > 0.10, T > 5 × 10⁷ K"; it stops if no pure-$Z$ table was read, `LPUREZ`): `GETOPAC` then interpolates $\log\kappa$ and its derivatives linearly in $Z$ between a normal table (at `ZIT`) and this pure-$Z$ table ($Z = 1$). The table is in COMMON `ZLAOL` (read by [[rdzlaol.f#RDZLAOL|`RDZLAOL`]]) and `ZSLAOL` (its density splines, from [[zsulaol.f#ZSULAOL|`ZSULAOL`]]); it also takes `TOLLAOL` from `NWLAOL`. Calls `LOCATE`, `XRNG4`, `CSPLINE`, `SPLINT`.

**The method.** As in [[gtlaol.f#GTLAOL|`GTLAOL`]] but without the composition step: a spline in $\log\rho$ at each of four temperatures (with linear extrapolation within the margin $\ln$ `TOLLAOL`), then a natural spline in $\log T$; chord slopes for the derivatives; $\log\kappa$ capped at 35.

## Questions for the experts

1. **Unused block.** `SLAOL` is declared but not used.
2. **Same margin question as `GTLAOL`** (`LOG(TOLLAOL)` is a natural log).

### GTPURZ

Opacity of a pure-metal mixture: spline in $\rho$, then in $T$.
