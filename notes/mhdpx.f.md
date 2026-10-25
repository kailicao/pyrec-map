## Explanation

**Purpose.** `MHDPX` is the entry point of the MHD equation-of-state interpolation package ("pressure as argument, interpolation in X, Z fixed"): for $\log P_\mathrm{gas}$, $\log T$ and $X$ it returns $\log\rho$, with all other table variables in COMMON `MHDOUT`.

**How it fits.** Called only by [[meqos.f#MEQOS|`MEQOS`]]. It calls [[mhdpx1.f#MHDPX1|`MHDPX1`]], which does the work. COMMON: `MHDOUT` (`VARMHD`, with `MEQOS` and `MHDPX1`), `LUOUT`, `CCOUT2` (unused). The tables must have been read first by [[mhdst.f#MHDST|`MHDST`]] (through [[mhdtbl.f#MHDTBL|`MHDTBL`]] at set-up); the comment calls it "MHDSTX" and says it "must be called in main".

**The method.** `MHDPX1(PL, TL, XC)`, then `RL = VARMHD(1)`.

## Questions for the experts

1. **No error signal.** The header promises `IERR = 1` outside the tables, but there is no `IERR`, and the error lines after `RETURN` are unreachable. Outside the temperature range `MHDPX1` returns silently, leaving `VARMHD` from the previous call, so `MEQOS` would use stale values. The callers of `MEQOS` test only the switch `LMHD`, not the range, so a point outside the tables gets stale values (and perhaps `MEQOS`'s stop on $\mu$). Should `MHDPX1` signal the failure, so that the caller can switch to another EOS?

### MHDPX

Thin wrapper: calls `MHDPX1` and returns $\log\rho$.
