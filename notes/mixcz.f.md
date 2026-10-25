## Explanation

**Purpose.** Homogenizes the composition of every convection zone (mass-weighted mean over the zone), then applies light clean-ups to the composition.

**How it fits.**
- **Inputs:** `HCOMP`, the shell masses `HS2`, the convection flags `LCZ` and `M`; `ZENVM` from `/COMP/`; `LEXCOM` from `/FLAG/`.
- **Who calls it:** the main program in [[main.f|main.f]], [[getw.f#GETW|GETW]] (twice) and [[seculr.f#SECULR|SECULR]].
- **Output:** `HCOMP` in place. It also writes `LCZ(M+1) = .FALSE.` as a sentinel.
- **COMMON blocks:** only `/FLAG/` and `/COMP/` are used. `/DEUTER/`, `/SCRTCH/`, `/CONST1/`, `/CONST2/`, `/ROT/`, `/MDPHY/` and `/OVRTRN/` are declared for a convective turnover time calculation that is now commented out ("it is now passed in in the OVRTRN common block", G. Somers 3/17).

**The method.**
1. **Zones.** Runs of convective shells give up to 12 zones (`MXZONE`, pairs of first and last shell).
2. **Mixing.** In each zone (one shell is enough at the centre), every species $k$ (11, or 15 with `LEXCOM`) becomes
$$\bar X_k = \frac{\sum_j X_{k,j}\,\Delta m_j}{\sum_j \Delta m_j}.$$
3. **Clean-up,** at every shell: $X \ge 0$; $Z \le 1 - X$; and ¹⁶O (row 9) at least $0.99\times10^{-3}\,(Z - Z_\mathrm{env,m})$, where $Z_\mathrm{env,m}$ = `ZENVM`.

**KC's changes.** 2025-05-31: the arguments `HS1`, `HR`, `HP`, `HD`, `HG` and `IFSTCL` removed, used only by the commented-out turnover time.

## Questions for the experts

1. **Helium after the clean-up.** $X$ is floored and $Z$ capped, but $Y$ is not recomputed, so $X+Y+Z+X_{^3\mathrm{He}}$ may differ from 1 afterwards. Is this restored elsewhere?
2. **The oxygen floor.** `HCOMP(9,I) = MAX(HCOMP(9,I), 0.99D-3*(HCOMP(3,I)-ZENVM))`: what is this floor for, and where does $0.99\times10^{-3}$ come from? (Probably a guard for helium-burning regions, where $Z$ exceeds the envelope's; this is a guess.)
3. **The sentinel.** `LCZ(M+1) = .FALSE.` writes past the model into the caller's array; it is safe only while `M < JSON`.
4. **Twelve zones.** More than 12 convection zones are silently ignored (the loop stops at `J = 24`).
