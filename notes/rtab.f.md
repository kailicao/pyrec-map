## Explanation

**Purpose.** Reads one block of an MHD equation-of-state table: for each of `NT` temperatures, the temperature and a row of `IVAR` quantities at each of `NR` densities.

**How it fits.** Called by [[mhdst1.f#MHDST1|`MHDST1`]], which reads the MHD tables (several calls, for the main table and the difference tables of each composition). Input: unformatted records on unit `IR`, opened by the caller. Outputs: `NR` (the number of densities, from the first temperature), `TL` (the temperatures, $\log T$ by the caller's names `TLOG1`, `TLOG2`) and `TDVAR(NT, NR, IVAR)`. It declares `/CCOUT2/` but does not use it.

**The method.** For each temperature, one record with the number of densities and $\log T$, then `NR` records of `IVAR` values. The run stops, with no message, if the sizes exceed the arrays (`NTM`, `NRM`) or if a temperature has a different number of densities.

**KC's changes.** Two `DO` loops that shared one termination label were given their own (KC 2025-05-30).

## Questions for the experts

1. **Silent stops.** Both checks end with `STOP` and no message; the messages (formats 9001, 9011) are commented out. Restore them?
2. **Check after use.** The size check on `NR` comes after `TL(N)` is read but before the data, which is fine; the check on `NT` (`NT.GT.NTM`) could be made once, before the loop, since `NT` is an input.
