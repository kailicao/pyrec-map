## Explanation

**Purpose.** Limits the time step by how much the structure changed from the previous model to this one. Its comment: the changes "in T, P, R, and L [must] be less than the user parameters ATIME(8)–ATIME(11) at any model point"; this criterion "dominates in the pre-main sequence, and this SR must be used (LPTIME=T) to perform pre-main sequence evolution."

**How it fits.**
- **Inputs:** the last step `DELTS`; the current model (`HL`, `HP`, `HR`, `HT`, `M`) and the previous one (`HLO`, `HPO`, `HRO`, `HTO` in `/OLDMOD/`); the limits `ATIME` in `/CTLIM/` (set by [[parmin.f#PARMIN|PARMIN]], possibly through [[remap.f#REMAP|REMAP]]).
- **Who calls it:** [[htimer.f#HTIMER|HTIMER]], when `LPTIME`; otherwise HTIMER uses $10^{20}$.
- **Output:** `PDELT`, the proposed step; HTIMER takes the smallest of its candidates.

**The method.** Over all shells, the largest changes $\Delta\log P$, $\Delta\log T$, $\Delta\log r$, and the relative luminosity change $\Delta L / \bar L$ (with $\bar L$ the mean of the shell and its inner neighbour). Then
$$f = \max\left(\frac{\Delta\log P}{a_9},\ \frac{\Delta\log T}{a_8},\ \frac{\Delta\log r}{a_{10}},\ \frac{\Delta L/\bar L}{a_{11}\ln 10}\right),\qquad \frac{1}{a_{13}} \le f \le a_{13},\qquad \texttt{PDELT} = \frac{\Delta t}{f},$$
with $a_k$ = `ATIME(k)`, and $f = 1$ if nothing changed.

## Questions for the experts

1. **`ATIME(12)` or `ATIME(13)`.** The header says `ATIME(12)` is the "maximum percentage change in the timestep"; since MHP 10/14 the code uses `ATIME(13)` as a factor. Update the header?
2. **The luminosity criterion.** $\Delta L/\bar L$ is compared with `ATIME(11)` $\times\ln 10$, which makes `ATIME(11)` a limit on $\Delta\log L$, whereas the header calls it "delta L/L". Which is meant?
3. **Unused.** `NHMAX` (where each maximum occurs) is filled but not used, and is undefined when the maximum is at the first shell.
