## Explanation

**Purpose.** Limits the time step by how much the structure changed from the previous model to this one. Its comment: the changes "in T, P, R, and L [must] be less than the user parameters ATIME(8)–ATIME(11) at any model point"; this criterion "dominates in the pre-main sequence, and this SR must be used (LPTIME=T) to perform pre-main sequence evolution."

**How it fits.**
- **Inputs:** the last step `DELTS`; the current model (`HL`, `HP`, `HR`, `HT`, `M`) and the previous one (`HLO`, `HPO`, `HRO`, `HTO` in `OLDMOD_MOD`); the limits `ATIME` in `NMLPAR_MOD` (set by [[parmin.f#PARMIN|PARMIN]], possibly through [[remap.f#REMAP|REMAP]]).
- **Who calls it:** [[htimer.f#HTIMER|HTIMER]], when `LPTIME`; otherwise HTIMER uses $10^{20}$.
- **Output:** `PDELT`, the proposed step; HTIMER takes the smallest of its candidates.

**The method.** Over all shells, the largest changes $\Delta\log P$, $\Delta\log T$, $\Delta\log r$, and the relative luminosity change $\Delta L / \bar L$ (with $\bar L$ the mean of the shell and its inner neighbour). Then
$$f = \max\left(\frac{\Delta\log P}{a_9},\ \frac{\Delta\log T}{a_8},\ \frac{\Delta\log r}{a_{10}},\ \frac{\Delta L/\bar L}{a_{11}\ln 10}\right),\qquad \frac{1}{a_{13}} \le f \le a_{13},\qquad \texttt{PDELT} = \frac{\Delta t}{f},$$
with $a_k$ = `ATIME(k)`, and $f = 1$ if nothing changed. The shells where the maxima occur are recorded in `NHMAX`, which nothing reads (unused?). The header still calls `ATIME(12)` the "maximum percentage change in the timestep"; since MHP 10/14 the code uses `ATIME(13)` as the factor, and REMAP now sets `ATIME(12)` from `TIME_DY_SHELL`, the helium-shell limit that [[ytime.f#YTIME|YTIME]] reads, and `ATIME(13)` from `TIME_MAX_DT_FRAC`: The header's line is older wording (settled from the code, Nov 9, 2026: [[#L68]]; [[#L128-L135]]; [[remap.f#L274-L275]]; [[remap.f#L291-L294]]).

> **Question** ([[#L67]]; [[#L107-L108]]; [[#L122-L124]]). **The luminosity criterion.** $\Delta L/\bar L$ is compared with `ATIME(11)` $\times\ln 10$, which makes `ATIME(11)` a limit on $\Delta\log L$, whereas the header calls it "delta L/L" (and the documentation of `TIME_DL`, "max local ΔL"). Which is meant?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/OLDMOD/` to `OLDMOD_MOD`, `ATIME` of `/CTLIM/` to `NMLPAR_MOD`; the unused `/CONST/`–`/CONST3/` dropped), `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

> **Question** ([[#L107-L108]]). **The luminosity's relative change.** `TESTL` divides the change of the shell's luminosity, `HLO(I)-HL(I)`, by the mean of `HL(I)` and `HL(I-1)`, the new value of the shell below, not by the mean of its old and new values as a relative change in time would. Is the mean over two shells intended (a point-centered value), or a slip for `HLO(I)`? Noticed while sorting the questions (Nov 10, 2026); not checked by running YREC.

