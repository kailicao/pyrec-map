## Explanation

**Purpose.** Computes the nuclear reaction rates at one shell, for the abundance updates. Its header calls it "a stripped-down version of ENGEB": the same reactions, screening and constants as [[engeb.f#ENGEB|`ENGEB`]], but without the energy generation. The rates are those of Bahcall's *Neutrino Astrophysics* (1989), with the alpha captures from Caughlan and Fowler (1988), as the comments say.

**How it fits.**
- **Who calls it:** [[mix.f#MIX|`MIX`]] (for each shell, before the composition is mixed and burned) and [[xtime.f#XTIME|`XTIME`]] (at the shell `IEND`, for the time step).
- **Inputs:** $\log_{10}\rho$ (`DL`), $\log_{10}T$ (`TL`), the mass fractions `X`, `Y`, `XHE3`, `XC12`, `XC13`, `XN14`, `XO16`, `XO18`, and the shell index `IU`.
- **Outputs:** the arrays `HR1`…`HR13` (the rates of the 13 reactions) and `HF1`, `HF2` (two branching fractions) at element `IU`. [[kemcom.f#KEMCOM|`KEMCOM`]] reads them (all but `HR9`, `HR13` and `HF2`) to update the abundances. `MIX` also copies all fifteen arrays into `HCOMPM(1..15,·)` of `/BURN/`, and [[rotmix.f#ROTMIX|`ROTMIX`]] reads them back from there.
- **COMMON:** `/CROSS/` (the cross-section factors `SSTANDARD(17)`, the derivative scalings `QS0E`, `QQS0EE`, the N15+p branching factors `FO16`, `FC12`, and `LNEWNUC`; set in [[parmin.f#PARMIN|`PARMIN`]], normalized in [[remap.f#REMAP|`REMAP`]], shared with `ENGEB`); `/WEAK/` (`WEAKSCREENING`, 0.03 by default in `PARMIN`; shared with `ENGEB`); `/CTLIM/` (the temperature cuts `TCUT`); `/CONST1/` (`CLN` $=\ln 10$, `CC13` $=1/3$).

**The method.**

1. **Composition sums.** Over the 13 isotopes (n, H1, D, H3, He3, He4, C12, C13, N14, O16, O18, Ne20, Mg24; those of n, D, H3, Ne20, Mg24 set to zero) with mass fractions $X_i$, bare nuclear masses $A_i$ (`ANUC`) and charges $Z_i$:
   $$\mu_I^{-1} = \sum_i \frac{X_i}{A_i}\ (\texttt{AMU}),\quad \mu_e^{-1} = \sum_i \frac{Z_iX_i}{A_i}\ (\texttt{EMU}),\quad \texttt{ZET} = \sum_i\frac{Z_i^2X_i}{A_i},\quad \texttt{XTR} = \sum_i\frac{Z_i^{1.58}X_i}{A_i}.$$
2. **Below the temperature cut** $\log T \le$ `TCUT(1)`, all rates are zero.
3. **Electron degeneracy** (for Salpeter's screening): with $\rho/\mu_e$ (`RWE`), $p_F^2/(m_ec)^2 = 1.017677\times10^{-4}(\rho/\mu_e)^{2/3}$ and $E_F/kT = 5.92986\,T_9^{-1}\bigl(\sqrt{1+p_F^2/m_e^2c^2}-1\bigr)$. The factor $f'/f$ (`FPRF`) is 1 for $E_F/kT \le 0.01$, 0 for $\log_{10}(E_F/kT) \ge 1.5$, and a sixth-order polynomial in $\log_{10}(E_F/kT)$ between.
4. **Screening.** $\Lambda_0 = 5.9426\times10^{-6}\,T_9^{-3/2}\sqrt{\rho/\mu_I}$ (`XXL`), $\tilde\zeta = \sqrt{(\texttt{ZET} + f'/f\cdot\mu_e^{-1})\,\mu_I}$ (`ZCURL`), $\bar Z = \mu_I/\mu_e$ (`ZBAR`). For reaction $j$ with charge product $Z_1Z_2$ (`ZPRD`):
   $$U_\mathrm{wk} = Z_1Z_2\,\Lambda_0\,\tilde\zeta .$$
   If $U_\mathrm{wk} \le$ `WEAKSCREENING`, weak screening is used, $U = U_\mathrm{wk}$. Otherwise the intermediate form
   $$U_\mathrm{int} = 0.38\,\Lambda_0^{0.86}\,\frac{\texttt{XTR}\;\zeta_{86,j}}{\mu_I^{-1}\,\tilde\zeta^{0.58}\,\bar Z^{0.28}}$$
   (Graboske et al. 1973, with their coefficients `Z86`), or, for $U_\mathrm{wk} > 2$, the strong form
   $$U_\mathrm{str} = 0.624\,\bar Z^{1/3}\Lambda_0^{2/3}\Bigl[\zeta_{53,j} + 0.316\,\bar Z^{1/3}\zeta_{43,j} + \frac{0.737\,\zeta_{23,j}}{\bar Z\,\Lambda_0^{2/3}}\Bigr]$$
   (`USTR`, with the coefficients `Z53`, `Z43`, `Z23`) when it is smaller than $U_\mathrm{int}$ or when $U_\mathrm{wk} \ge 5$. The rate is multiplied by $e^{U}$.
5. **Reactions 1–7** (pp, He3+He3, He3+He4, p+C12, p+C13, p+N14, p+O16), with $T_9 = T/10^9$ K:
   $$r_j = \rho\,\Bigl[T_9^{-2/3} + q_{1}T_9^{-1/3} + s'_j\,(q_{2} + q_{3}T_9^{1/3}) + s''_j\,(q_{4}T_9^{2/3} + q_{5}T_9)\Bigr]\exp\bigl(q_{6}T_9^{-1/3} + q_{7} + (q_{8}T_9)^2 + U_j\bigr)\;S_j,$$
   with $q_{k} =$ `Qk(j)` (the terms of eq. 3.14 of *Neutrino Astrophysics*, as the comments explain), $s'_j$, $s''_j$ = `QS0E(j)`, `QQS0EE(j)` (user scalings of the S-factor's first and second derivatives) and $S_j$ = `SSTANDARD(j)`. Rates below $10^{-30}$ are set to zero. All are skipped when $X = 0$.
6. **Be7.** Electron capture: $\lambda_e = 1.752\times10^{-10}\,T_9^{-1/2}\,[1 + 0.004(1000\,T_9 - 16)]\,\mu_e^{-1}\,S_{15}$. Proton capture: $\lambda_p = 3.128813\times10^5\,X\,S_{16}\,e^{-10.2625\,T_9^{-1/3}}$ times the bracket of step 5 with `Q(8)`, and its own weak or intermediate screening. Both are multiplied by $\rho\cdot 8.584981\times10^{22}$, and $F_1 = \lambda_e/(\lambda_e+\lambda_p)$ is the fraction of Be7 that captures an electron.
7. **N15+p branching.** The $(p,\alpha)$ and $(p,\gamma)$ channels have their own brackets, times $67500\,f_{C12}$ and $64\,f_{O16}$ (`FC12`, `FO16`); $F_3 = \mathrm{C12ALPHA}/(\mathrm{C12ALPHA}+\mathrm{O16GAMMA})$.
8. **Alpha captures** (only when $\log T \ge$ `TCUT(4)`): C13$(\alpha,n)$O16 (`RATE(8)`), C12$(\alpha,\gamma)$O16 (`RATE(10)`), N14$(\alpha,\gamma)$F18 (`RATE(11)`) and the triple-alpha (`RATE(12)`, $\propto\rho^2 T_9^{-3} e^{-4.4027/T_9}$), as fits of the Caughlan and Fowler form. `RATE(9)` and `RATE(13)` are always zero, and every rate at or below $10^{-5}$ is set to zero.
9. **Output units.** Each rate (per second per gram, mass fractions left out) is multiplied by `C21` $= 5.240358\times10^{-8}$, "(10^9 years/1 second)·(1 atomic mass unit/1 gram)", which gives `HRj(IU)`. `HF1(IU)` $= F_3$ and `HF2(IU)` $= F_1$.

**Design.** All constants are `DATA` statements, with earlier sets kept as comments (BP00, 7/21/03). The routine duplicates much of `ENGEB`, so a change to one must be copied to the other.

**KC's changes.** The arguments `Z`, `XN15`, `XO17`, `XH2`, `XLI6`, `XLI7` and `XBE9`, which were not used, were removed from the signature (KC 2025-05-31), and the calls in `MIX` and `XTIME` changed to match.

## Questions for the experts

1. **The N15(p,α) S-factor.** The comment says S0 "has been changed from 78000. to 675000. on 9/25/97", but the code multiplies `C12ALPHA` by 67500, ten times smaller. [[remap.f#REMAP|`REMAP`]]'s reference value `S0_1_15_C12ALP_REF` is also 6.75D4, so the comment is probably the typo. Can this be confirmed?
2. **Two thresholds for zero.** Reactions 1–7 are zeroed below $10^{-30}$, but at the end every rate at or below $10^{-5}$ (per second per gram, before `C21`) is set to zero. Is the second cut intended? At low density or temperature it could switch off slow but relevant rates.
3. **`HF2` is never used.** `HF1` holds $F_3$ (N15 branching) and `HF2` holds $F_1$ (Be7 branching). `KEMCOM` uses `HF1` as `F3`. `HF2` is only copied by `MIX` into `HCOMPM(15,·)` and copied back by `ROTMIX`; no routine computes with it. Is the Be7 branching meant to enter the abundance update (for example of Be7 or Li7), or can it be dropped?
4. **Comments that disagree with the code.** "F3 IS THE FRACTION OF THE N14 THAT IS BURNED BY P, ALPHA" should read N15; the comment above the screening loop says `WEAKSCREENING` is passed "in the FLUX COMMON block", but it comes from `/WEAK/`; "DL AND DT" are `DL` and `TL`.
5. **Hard-coded Be7 constants.** The Be7 screening uses its own `ZPRDBE7P = 4.0` and `Z86BE7P = 5.7790`, and no strong-screening branch. Fine for the Sun, but is this routine used for denser cores, where strong screening would matter?
6. **Duplication with ENGEB.** Are the constants here guaranteed to match those in `ENGEB`? A check by script, or one shared routine, would remove the risk.
7. **Stale branching fractions below `TCUT(1)`.** When $\log T \le$ `TCUT(1)`, the routine jumps straight to label 200, so `F1` and `F3` are not set in this call, and `HF1(IU)`, `HF2(IU)` receive the values kept (by `SAVE`) from the previous call, for another shell. `KEMCOM`'s loop in `MIX` stops at that cut for radiative shells, but is a stale `HF1` ever used, for example in a convective zone whose first shell lies below the cut? Setting `F1 = F3 = 0` before the jump would remove the doubt.
