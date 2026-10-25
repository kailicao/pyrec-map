## Explanation

**Purpose.** `LIBURN2` is a cheaper version of [[liburn.f#LIBURN|`LIBURN`]]: it burns ⁶Li, ⁷Li and ⁹Be over a step in one go, with the rate taken at the geometric mean of its start and end values, without substeps, extrapolation or accretion.

**How it fits.** Called by [[getw.f#GETW|`GETW`]] (rotating models, as an alternative to `LIBURN`) and [[bursmix.f#BURSMIX|`BURSMIX`]]. Same arguments (except none for accretion), same COMMON blocks as `LIBURN` without `MASSCHG` and `DEUTER`: `NEWRAT`, `OLDRAT` (rates from [[lirate88.f#LIRATE88|`LIRATE88`]]), `SCRTCH`, `MDPHY`, `OLDMOD`, `DPMIX`, `LIOV`, `PREVCZ`, `ROT`, `CONST1`, `LUOUT`. No calls.

**The method.** The base of the convection zone is found as in `LIBURN`. Then, in each radiative point below both bases (skipping points where the ⁹Be rate, at the start or the end, is at most $10^{-32}$; destroying everything above $\log T = 7$), and in the convection zone as a whole,

$$x \leftarrow x\,\exp\!\left(-\Delta t\,\sqrt{\lambda_0\lambda_1}\right),$$

with $\lambda_0$, $\lambda_1$ the rates (mass-weighted means in the zone) at the start and end of the step; set to 0 when the exponent is 30 or more, or the result below $10^{-24}$. Points left by a retreating zone get the weighted rate of `LIBURN`'s step 4.

**KC's changes.** 2025-05-31: the unused argument `HD` removed.

## Questions for the experts

1. **No overflow guard.** The last loop divides by `EXP(DLI6)`, `EXP(DLI7)`, `EXP(DBE9)` without the 30 cut or KC's `SAFEDIVEXP`, which `LIBURN` now uses. Should it get the same guard?
2. **Exit from the last loop.** A point below the ⁹Be rate threshold ends the routine (`GOTO 200`) rather than skipping that point (`LIBURN` does the same), while the radiative loop skips such points.
3. **Same questions as `LIBURN`** on the `HRO` radius in the overshoot branch, the points newly in the zone, the units of the step, the sign of `FRAD` in the last loop (`LIBURN`, question 7) and the bottom point's adjusted rates left in `NEWRAT` (question 8).
4. **Header.** The banner comment still says "LIBURN".

### LIBURN2

One-step burning with the geometric-mean rate (above).
