## Explanation

**Purpose.** `MHDPX1` interpolates the MHD equation-of-state tables in $\log P$, $\log T$ and $X$ (at fixed $Z$): it picks the set of tables for the temperature, interpolates each in $(\log P, \log T)$ through [[mhdpx2.f#MHDPX2|`MHDPX2`]], then interpolates the results in $X$. The result goes to COMMON `MHDOUT`.

**How it fits.** Called only by [[mhdpx.f#MHDPX|`MHDPX`]]. Calls [[mhdpx2.f#MHDPX2|`MHDPX2`]], [[quint.f#QUINT|`QUINT`]] (quadratic interpolation) and [[lir.f#LIR|`LIR`]] (cubic). COMMON: `TTTT` (the temperature limits `TLIM1`, `TLIM2`, `TMINI`, `TMAXI`, set by [[mhdst.f#MHDST|`MHDST`]]), `MHDOUT` (output, with `MEQOS`, `MHDPX`), `LUOUT`, `CCOUT2`.

**The method.**
1. If $\log T$ is outside [`TMINI`, `TMAXI`], return at once.
2. Choose the tables (filled by `MHDPX2`, one row of `VAROUT` each): for $\log T$ < `TLIM1` the lower parts of the three "ZAMS" tables (A, B, C, different $X$); for `TLIM1` ≤ $\log T$ < `TLIM2` their upper parts; above, the five "centre" tables (variable $X$, for the core).
3. For the ZAMS tables, whose $X$ values must be equally spaced (else stop), interpolate each of the 25 variables quadratically in $X$ (Newton form, `QUINT`):
$$y(X) = y_0 + \frac{\Delta y_0}{h}(X - X_0) + \frac{\Delta^2 y_0}{2h^2}(X-X_0)(X-X_0-h).$$
For the centre tables, take four of the five (the four highest $X$ when possible) and interpolate cubically with `LIR`.

**KC's changes.** 2025-05-30: DO loops rewritten to end on `CONTINUE` (no change in behaviour intended).

## Questions for the experts

1. **Silent return out of range.** Outside the tables' temperature range it returns without touching `MHDOUT`, so the caller gets the previous point's values. The warning formats (extrapolation in $X$, $T$ out of range) are all commented out.
2. **Variables 21–25 from the ZAMS tables.** The ZAMS tables have 20 variables (`IVARC`), but the $X$ interpolation runs over 25; elements 21–25 of rows 1–3 of `VAROUT` are never written ([[mhdpx2.f#MHDPX2|`MHDPX2`]] copies 20 for these rows, and the centre tables fill rows 4–8), so `VARMHD(21..25)` come from undefined values. `MEQOS` uses only variables up to 20, so this may be harmless.
3. **Extrapolation in X.** The test whether $X$ lies inside the ZAMS tables' range is commented out.
4. **Mismatch at exactly `TLIM2` (apparent bug).** The tables are chosen with `TL.LT.TLIM2` (line 45), but the interpolation uses `TL.LE.TLIM2` (line 60). At $\log T$ = `TLIM2` exactly, the centre tables are read into rows 4–8 while the quadratic interpolation uses rows 1–3, left from an earlier call. Should line 60 read `TL.LT.TLIM2`?

### MHDPX1

Selects the MHD tables by temperature and interpolates in $X$ (above).
