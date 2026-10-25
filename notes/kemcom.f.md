## Explanation

**Purpose.** `KEMCOM` solves the nuclear burning network for one shell, or one convection zone, over a time step: it finds the new mass fractions of H, ³He, ⁴He, ¹²C, ¹³C, ¹⁴N and ¹⁶O simultaneously and implicitly, by Newton iteration, from the reaction rates computed in [[engeb.f#ENGEB|`ENGEB`]] (its comment: "Don VandenBerg's notes explain what the SR is doing"). ¹⁸O is updated explicitly afterwards.

**How it fits.**
- **Who calls it:** [[mix.f#MIX|`MIX`]] and [[rotmix.f#ROTMIX|`ROTMIX`]], for each radiative shell (`IBEGIN` = `IEND`) and each convection zone (`IBEGIN` < `IEND`).
- **Inputs:** `HT` ($\log T$), the rates `HR1`–`HR8`, `HR10`–`HR12` and the branching ratio `HF1` (per Gyr per amu, without the composition factors, as its comment says), `HS2` (shell masses), `DDAGE` (the step in years); the abundances at the start of the step `HCOMPP` from COMMON `OLDMOD`.
- **Output:** the new `HCOMP` (elements 1–7, 9 and 11; element 3, $Z$, is either reset or set to its zone mean, see step 4) for shells `IBEGIN`..`IEND`.
- **Calls:** [[simeqc.f#SIMEQC|`SIMEQC`]], the linear solver for the 7×8 Newton system.
- **COMMON blocks:** `BURTOL` (`CMIN`, `ABSTOL`, `RELTOL`, `KEMMAX`; set by [[parmin.f#PARMIN|`PARMIN`]]), `CTLIM` (`TCUT(1)`, the lowest burning temperature), `OLDMOD` (the previous model: `HCOMPP`; written by [[hpoint.f#HPOINT|`HPOINT`]] and others), `LUOUT`.

**The method.**
1. **Mixing.** For a convection zone, the starting abundances are the mass-weighted means $\bar x_j = \sum_i x_{j,i}\,\Delta m_i / \sum_i \Delta m_i$ over the zone (elements 1–11), and so are the rates. If the zone's (or shell's) first point is below `TCUT(1)`, it only homogenizes and returns.
2. **Equations.** With $\Delta t$ in Gyr and $A_k$ the species' mass numbers (1, 3, 4, 12, 13, 14, 16), the residuals are
$$G_k(w) = w_k - w_k^0 - A_k\,\Delta t\,R_k(w),$$
where $w = (X, {}^3\mathrm{He}, Y, {}^{12}\mathrm{C}, {}^{13}\mathrm{C}, {}^{14}\mathrm{N}, {}^{16}\mathrm{O})$ are the end-of-step abundances (so the scheme is implicit) and, with $r_n$ the rate `GRn` and $f_3$ = `HF1`, $f_4 = 1-f_3$ (the branching of ¹⁵N + p to ¹²C + α or to ¹⁶O):
$$R_X = -3r_1X^2 + 2r_2\,{}^3\mathrm{He}^2 - r_3\,{}^3\mathrm{He}\,Y - r_4X\,{}^{12}\mathrm{C} - r_5X\,{}^{13}\mathrm{C} - 2X\,(r_6\,{}^{14}\mathrm{N} + r_7\,{}^{16}\mathrm{O}),$$
$$R_{^3\mathrm{He}} = r_1X^2 - 2r_2\,{}^3\mathrm{He}^2 - r_3\,{}^3\mathrm{He}\,Y,$$
$$R_Y = r_2\,{}^3\mathrm{He}^2 + r_3\,{}^3\mathrm{He}\,Y + f_3r_6X\,{}^{14}\mathrm{N} + r_7X\,{}^{16}\mathrm{O} - r_{10}Y\,{}^{12}\mathrm{C} - r_8Y\,{}^{13}\mathrm{C} - r_{11}Y\,{}^{14}\mathrm{N} - 3r_{12}Y^3,$$
$$R_{^{12}\mathrm{C}} = r_{12}Y^3 - r_4X\,{}^{12}\mathrm{C} - r_{10}Y\,{}^{12}\mathrm{C} + f_3r_6X\,{}^{14}\mathrm{N},\qquad R_{^{13}\mathrm{C}} = r_4X\,{}^{12}\mathrm{C} - r_5X\,{}^{13}\mathrm{C} - r_8Y\,{}^{13}\mathrm{C},$$
$$R_{^{14}\mathrm{N}} = r_5X\,{}^{13}\mathrm{C} + r_7X\,{}^{16}\mathrm{O} - r_6X\,{}^{14}\mathrm{N} - r_{11}Y\,{}^{14}\mathrm{N},\qquad R_{^{16}\mathrm{O}} = f_4r_6X\,{}^{14}\mathrm{N} + r_{10}Y\,{}^{12}\mathrm{C} - r_7X\,{}^{16}\mathrm{O} + r_8Y\,{}^{13}\mathrm{C}.$$
The reactions by the comments: $r_1$ pp, $r_2$ ³He+³He, $r_3$ ³He+⁴He, $r_4$ ¹²C+p, $r_5$ ¹³C+p, $r_6$ ¹⁴N+p (with ¹⁵N+p), $r_7$ ¹⁶O+p (with ¹⁷O+p), $r_8$ ¹³C+α, $r_{10}$ ¹²C+α, $r_{11}$ ¹⁴N+α, $r_{12}$ triple α; $r_9$ (¹⁶O+α) and $r_{13}$ (¹²C+¹²C) are zeroed.
3. **Newton iteration.** The Jacobian $\partial G_k/\partial w_l$ fills `A(1..49)` column by column and the residuals $G_k$ fill `A(50..56)` (= `B`, by `EQUIVALENCE`); entries below $10^{-8}$ off the diagonal are zeroed, and `SIMEQC` (which solves $J\,\delta = G$, leaving $\delta$ in `B`) is skipped when the matrix is diagonal. Then $w \leftarrow w - \delta$; abundances below `CMIN` are set to 0. It stops when $\max|B_k| <$ `ABSTOL` and $\max|B_k/w_k| <$ `RELTOL`, or stops the run after `KEMMAX` iterations. The first guess is the result for the shell below (or the shell's current `HCOMP` for the first shell).
4. **After convergence.** ¹⁸O explicitly: $x_{18} = x_{18}^0 + 18\,\Delta t\,r_{11}\,Y\,{}^{14}\mathrm{N}$. If the previous model's $X$ at the zone's top (`HCOMPP(1,IEND)`) is below $5\times10^{-7}$, $Z$ is reset to $1 - X - {}^3\mathrm{He} - Y$ from the new values; otherwise $Z$ is the zone's mean at the start of the step. All shells of the zone get the same new values.

**KC's changes.** 2025-05-31: the unused arguments `HR9`, `HR13` and `ITLVL` removed from the interface.

## Questions for the experts

1. **¹⁸O is only produced.** The explicit update adds ¹⁴N(α,γ) production but no destruction. Intended?
2. **¹⁵N and ¹⁷O are not mixed in burning zones.** When a convection zone burns, elements 8 and 10 of `HCOMP` are left unchanged (only the non-burning branch homogenizes all 11). Do they matter anywhere?
3. **Comments that no longer hold.** The comment on the first guess speaks of calls from `CRRECT` with `ITLVL` > 1, an argument now removed; the error message says "run stopped after 50 attempts", while the limit is `KEMMAX`.
4. **Hard-coded thresholds.** $10^{-8}$ for zeroing matrix entries and $5\times10^{-7}$ for resetting $Z$.
5. **The diagonal shortcut.** When all off-diagonal entries are below $10^{-8}$, `SIMEQC` is skipped and the correction is the residual $G_k$ itself, not $G_k/J_{kk}$. The diagonal entries are $1 + A_k\Delta t\,(\dots)$, close to 1 only for small rates; is the undivided step intended?

### KEMCOM

Implicit Newton solution of the 7-species network over one step (equations above), with explicit ¹⁸O.
