## Explanation

**Purpose.** `INTPT` interpolates the MHD equation-of-state table in pressure and temperature: for a given $\log P$ and $\log T$ it returns the `IVAR` tabulated quantities by 4×4-point cubic interpolation.

**How it fits.** Called only by [[mhdpx2.f#MHDPX2|`MHDPX2`]], which passes one of the MHD tables (`TDVAR(NTM,NRM,IVAR)`, with `TDVAR(…,2)` the pressure variable on each row) and its temperature grid `TLOG`. It calls [[lir.f#LIR|`LIR`]] five times. COMMON: `CCOUT2` (debug flags), declared but not used.

**The method.**
1. Find `IT(1)`, the last grid temperature below `TL` (`TLOG` ascending), step back by one and clamp it to at most `NT`−3, so that four rows `IT(1..4)` are available.
2. On each of those rows, find the four density points whose pressure brackets `PL` the same way.
3. On each row, interpolate all `IVAR` quantities in pressure with `LIR` (4-point Lagrange in `TDVAR(…,2)`).
4. Interpolate the four row results in $\log T$ with `LIR`, giving `VAROUT`.

**KC's changes.** 2025-05-30: DO loops with shared or non-`CONTINUE` terminations rewritten (no change in behaviour intended).

## Questions for the experts

1. **`IT(1)` may be undefined.** The loop sets `IT(1)` only for rows with `TLOG(N)` < `TL`. If `TL` ≤ `TLOG(1)`, the loop exits at once and `IT(1)` keeps whatever value the previous call left (it is `SAVE`d) or is undefined on the first call. Should it start at 1?
2. **Silent return above the table.** If `PL` exceeds a row's largest pressure, the routine returns without setting `VAROUT`. Does `MHDPX2` detect this?
3. **Unused.** `PMINI` and the COMMON block `CCOUT2` are unused.

### INTPT

Bicubic (Lagrange, via `LIR`) interpolation of the MHD table in $(\log P, \log T)$ (above).
