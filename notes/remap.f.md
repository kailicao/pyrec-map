## Explanation

**Purpose.** Translates newer, "more intuitively named" namelist parameters (MHP 6/2014) into the arrays the rest of the code uses: the nuclear cross sections and their energy derivatives, and the tolerances for the mesh and the time step.

**How it fits.**
- **Who calls it:** [[parmin.f#PARMIN|`PARMIN`]], after reading the namelists.
- **Inputs, through COMMON:** `/NEWCROSS/` (the new cross-section parameters, such as `S0_1_1` for p+p and `S0P_1_12` for the first derivative of p+C12) and `/NEWPARAM/` (the new tolerance names, such as `TOL_DM_MAX` and `TIME_DX_SHELL`, and the switches `LNEWVARS`, `LSTRUCT_TIME`); both shared only with `PARMIN`.
- **Outputs, through COMMON:**
  - `/CROSS/`: `SSTANDARD(17)`, `QS0E(8)`, `QQS0EE(8)`, `FC12`, `FO16`, read by [[rates.f#RATES|`RATES`]] and [[engeb.f#ENGEB|`ENGEB`]];
  - `/CTOL/`: `HPTTOL(12)`, the mesh tolerances, used by [[hpoint.f#HPOINT|`HPOINT`]] and others;
  - `/CTLIM/`: `ATIME(14)`, the time-step limits, used by [[htimer.f#HTIMER|`HTIMER`]] and others;
  - `/CT2/` (`DTWIND`), `/DIFUS/` (`DTDIF`), `/CT3/` (`LPTIME`).

**The method.**
1. **Defaults.** `QS0E`, `QQS0EE`, `FC12`, `FO16` are set to 1.
2. **Cross sections, when `LNEWNUC` is true.** `SSTANDARD` becomes the ratio of each new zero-energy S-factor to the reference value hard-coded here (`…_REF`, the values that `RATES` and `ENGEB` assume):
   $$\texttt{SSTANDARD}(j) = \frac{S_{0,j}}{S_{0,j}^{\mathrm{ref}}},\qquad f_{C12} = \frac{S_{0}^{\,15(p,\alpha)}}{6.75\times10^4},\qquad f_{O16} = \frac{S_0^{\,15(p,\gamma)}}{64}.$$
   The resonant helium-burning reactions (8, 10, 11, 12) and the unused ones (9, 13) are left at 1. The derivative factors are ratios of $S'/S$ (and $S''/S$) to those of Solar Fusion I (Adelberger et al. 1998), whose values are hard-coded (`QS0E_…_A98`, `QQS0EE_…_A98`, in b):
   $$\texttt{QS0E}(j) = \frac{S'_j/S_{0,j}}{\bigl(S'/S_0\bigr)_j^{\mathrm{A98}}},\qquad \texttt{QQS0EE}(j) = \frac{S''_j/S_{0,j}}{\bigl(S''/S_0\bigr)_j^{\mathrm{A98}}},$$
   set to 0 when $S_{0,j} \le 0$. `RATES` multiplies its $Q_2, Q_3$ terms by `QS0E` and its $Q_4, Q_5$ terms by `QQS0EE`.
3. **Tolerances, when `LNEWVARS` is true.** A one-to-one copy, with a comment on each: for example `HPTTOL(1)` = `TOL_DM_MIN` (minimum log mass spacing), `HPTTOL(11)` = `TOL_DP_CORE_MAX`, `ATIME(7)` = `TIME_DX_SHELL` (maximum fraction of X burned in a shell in a step), `ATIME(13)` = `TIME_MAX_DT_FRAC`.

**KC's changes.** The unused `DATA` values of the Adelberger reference S-factors were commented out, keeping only `S0_1_1_A98` and `S0_1_BE7P_A98` (KC 2025-05-31); the members of `/NEWPARAM/` were reordered, `LSTRUCT_TIME` moved to just before `LNEWVARS` (KC 2025-05-30).

## Questions for the experts

1. **A wrong reference in six derivative factors (apparent bug).** `QS0E(2)` to `QS0E(7)` and `QQS0EE(4)`, `QQS0EE(5)`, `QQS0EE(7)` divide by `S0_1_1_A98` (the p+p value, $4.00\times10^{-22}$) instead of each reaction's own `S0_x_A98`. For example, `QS0E(2) = (S0P_3_3/S0_3_3)/(QS0E_3_3_A98/S0_1_1_A98)`, where the commented-out lines for `QQS0EE(1..3)` use the matching `S0_3_3_A98`. With p+p's tiny $S_0$ in the denominator, these factors come out of order $10^{-22}$ instead of near 1, which switches off the derivative terms of reactions 2–7 whenever `LNEWNUC` is true. The `DATA` values needed to fix it were commented out as unused in KC 2025-05-31, so restoring them is part of the fix. (The comment "MHP 4/25 FIXED TYPOS" suggests the lines were already reviewed once.)
2. **Units of the derivatives.** The comments give the reference S-factors in keV b and the first derivatives in b; is the user expected to give `S0P_…` in b as well, and `S0PP_…` in b keV$^{-1}$? The namelist documentation should say.
3. **"NRATES".** A comment says the derivatives are used "in ENGEB AND NRATES"; the routine is `RATES`.
4. **Both switches change other inputs silently.** With `LNEWNUC`, any `SSTANDARD` given in the namelist is overwritten; with `LNEWVARS`, `HPTTOL` and `ATIME` are. Is a message printed anywhere to warn a user who sets both?
