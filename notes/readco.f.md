## Explanation

**Purpose.** Reads the OPAL equation-of-state tables (the original 1990s version, "YCK 2/95 OPAL EOS"), for five hydrogen abundances, into memory. The versions for the 2001 and 2006 tables are [[readcoeos01.f#READCOEOS01|`READCOEOS01`]] and [[readcoeos06.f#READCOEOS06|`READCOEOS06`]].

**How it fits.**
- **Who calls it:** [[esac.f#ESAC|`ESAC`]], once, on its first call (guarded by `ITIME` in `/LREADCO/`), after setting `XX` and the index map.
- **Input:** the table file, already opened on unit `IOPALE` (49) by [[parmin.f#PARMIN|`PARMIN`]] ("MHP 8/25 Moved opening of file to parmin"). `READCO` closes it at the end.
- **Outputs, through COMMON:**
  - `/A/`: the tables `XZ(MX, MV, NT, NR)` (5 compositions × 10 quantities × 56 temperatures × 77 densities), the grids `T6LIST`, `T6A`, `RHO`, and the inverse spacings `DFS`, `DFSR`, `DFSX` used by the interpolation; shared with `ESAC`, [[rhoofp.f#RHOOFP|`RHOOFP`]], [[t6rinterp.f#T6RINTERP|`T6RINTERP`]], [[eqbound.f#EQBOUND|`EQBOUND`]] and `BLOCK_DATA`.
  - `/B/`: `ZZ` (the table's $Z$, read here), and `IRI`, `INDEX`, `NTA` (set elsewhere, in `BLOCK_DATA`, used here to place each column and to know how many temperatures each density row has).
  - `/EEE/`: per composition, `MOLES`, `XIN`, `TMASS`, `FRAC`, `RHOGR`, `ALOGR`, `ICYCUSE`; only `READCO` declares it.
  - `/RMPOPEOS/`: `RMX(T)`, the highest table density at each temperature, for the ramp between OPAL and the other equations of state in [[eqbound.f#EQBOUND|`EQBOUND`]] ("MHP 8/98").
- **Other COMMON:** `/OPALEOS/` (the unit `IOPALE`), `/E/`, `/EE/` (`XX`, the hydrogen abundances), `/AA/`, `/LUOUT/`.

**The method.** On the first call, all of `XZ` is set to $10^{35}$ (a marker for "no data"). Then for each of the five compositions: a header ($X$, $Z$, `MOLES`, `TMASS`, six fractions `FRAC`), and for each of the 77 densities a header (checked against the density's number), followed by `ICYCUSE` temperature rows, of which the first `NTA(JCS)` are kept: $T_6$, $\log R$ and ten quantities, stored as `XZ(M, INDEX(IV), I, JCS)`. Afterwards the grids are taken from the first composition, and the inverse spacings computed:

$$\texttt{DFS}(i) = \frac{1}{T_{6,i} - T_{6,i-1}},\qquad \texttt{DFSR}(i) = \frac{1}{\rho_i - \rho_{i-1}},\qquad \texttt{DFSX}(i) = \frac{1}{X_i - X_{i-1}} .$$

Here `RHO` holds the table's density variable read as `RHOGR`, which by the header names is probably $\rho$ in g cm$^{-3}$; the code does not say.

**Design.** The temperature list stops at the first zero (`NTUSE`), but `NTUSE` is not used afterwards, and `DFS` is computed over all `NT` points. The ramp's edge `KRA` is a hard-coded `DATA` list of 56 density indices.

**KC's changes.** Three `DO` loops that ended on an assignment were rewritten to end on `CONTINUE` (KC 2025-05-30); the members of `/OPALEOS/` were reordered (KC 2025-05-30, with the file names then removed by MHP 8/25).

## Questions for the experts

1. **A zero temperature leaves `DFS` undefined.** If `T6LIST(1,I)` is zero for some `I`, the loop jumps out, leaving `T6A` from `I` onward unset (zero), and then `DFS` divides by $T_{6,i} - T_{6,i-1}$ over all `NT` points, which can be zero or negative. In [[readcoeos01.f#READCOEOS01|`READCOEOS01`]] a zero stops the run instead. Can the original tables have fewer than 56 temperatures?
2. **`ITIMECO` uninitialized.** The local first-call flag `ITIMECO` is never initialized; it relies on the memory not happening to hold 12345678. Harmless in practice, since `ESAC` calls `READCO` once; is the flag still needed?
3. **`ZZ` per composition.** `ZZ(M)` is read for each of the five tables, but nothing checks that the five agree or that they match the run's $Z$. Is that checked elsewhere?
