## Explanation

**Purpose.** `EQBOUND` decides whether a point $(T, \rho)$ lies inside the OPAL 1995 equation-of-state table, and whether it lies in the border zone where OPAL results are blended ("ramped") with the Yale/SCV equation of state. It returns the blending weight. The header says "MHP 8/98".

**How it fits.**
- **Who calls it:** only [[eqstat2.f#EQSTAT2|EQSTAT2]], right after [[oeqos.f#OEQOS|OEQOS]] has returned the OPAL 1995 result, when `LOPALE` is set and $T \ge 5000$ K, $\log T \le 8$ and $\log\rho \le 5$ (EQSTAT2's own density).
- **Inputs:** $T$ (`T`, in K) and $\log_{10}\rho$ (`DL`) from OPAL.
- **Outputs:** `LTAB` (in the table), `LRAMP` (blending needed) and `FAC`, the weight of the OPAL result. `EQSTAT2` then sets each quantity to $q = q_\mathrm{Yale} + f\,(q_\mathrm{OPAL} - q_\mathrm{Yale})$.
- **COMMON blocks:** `/A/` holds the OPAL 1995 table (`T6A`, `RHO`, …), shared with [[esac.f#ESAC|ESAC]], `READCO`, `RHOOFP`, `T6RINTERP` and `BLOCK_DATA`. `/RMPOPEOS/` holds `RMX` (the highest density at each temperature), `KRA` (the index of the highest table density at each temperature, set by a DATA statement; the ramp begins one element lower) and `KT` (the last temperature index found); `READCO` fills it.

**The method.** With $T_6 = T/10^6$ and the table temperatures $T_{6,k}$ decreasing with $k$:
1. Outside $-14 \le \log\rho \le 5$: out of table.
2. Find `KT` with $T_{6,KT+1} \le T_6 \le T_{6,KT}$, searching from the previous `KT`. If none is found, the run stops ("SR CALL SHOULD HAVE BEEN STOPPED OUTSIDE TABLE BOUNDS").
3. The density edge is $\log\rho_\mathrm{lim} = \log_{10}$ `RMX(KT+1)`, and the ramp starts one table element lower, $\log\rho_2 = \log_{10}$ `RHO(KRA(KT+1)-1)`. Above $\rho_\mathrm{lim}$: out of table.
4. Ramps, checked in this order: near the lowest temperature, $f = (T_6 - T_{6,N})/(T_{6,N-1} - T_{6,N})$; near the highest, $f = (T_{6,1} - T_6)/(T_{6,1} - T_{6,2})$; near the density edge, $f = (\log\rho_\mathrm{lim} - \log\rho)/(\log\rho_\mathrm{lim} - \log\rho_2)$. Otherwise no ramp.
5. Out of table: `LTAB` false, `LRAMP` true, $f = 0$.

**KC's changes.** The unused argument `DL0` was removed (2025-05-31).

## Questions for the experts

1. **Edges not interpolated.** The comments say the density edge and the ramp start are found "by linear interpolation" in $T$, but those lines are commented out: the edge is taken at `KT+1` alone, and the interpolation weight `FT` is computed but never used. Which is meant?
2. **One ramp at a time.** Only one ramp factor is used, even at a corner where both a temperature and a density ramp apply. [[eqbound06.f#EQBOUND06|EQBOUND06]] multiplies the two factors instead. Should the 1995 version do the same?
3. **No low-density ramp.** There is no ramp at the low-density edge, only the hard cut at $\log\rho = -14$. Is that safe, given that `EQSTAT2` calls OPAL only for $\log\rho \le 5$?

### EQBOUND

Returns whether $(T,\rho)$ is in the OPAL 1995 table and the blending weight $f$ (method above). Keeps the last temperature index in `/RMPOPEOS/` to speed up the next search.
