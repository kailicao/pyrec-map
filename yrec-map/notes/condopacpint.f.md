## Explanation

**Purpose.** This file computes the conductive opacity for a mixture of hydrogen, helium and metals from Potekhin's conductivity tables ("based on Chris Burke's conductive opacity code", LLP 5/31/04). [[getopac.f#GETOPAC|GETOPAC]] then adds it to the radiative opacity in harmonic sum.

**How it fits.**
- **Inputs:** the arguments `DL` ($\log\rho$), `TL` ($\log T$), `X`, `Z`, and `FXION`, the ionization fractions (of H; of He singly and doubly).
- **Who calls it:** [[getopac.f#GETOPAC|GETOPAC]], when the Potekhin option (`LcondOpacP`) is on.
- **What it calls:** [[condopacp.f#CONDOPACP|CONDOPACP]], for $Z_\mathrm{ion}$ = 1, 2 and 8.
- **Outputs:** `OC` and `OCL` (the conductive opacity and its log), `QODC`, `QOTC` (its derivatives in $\log\rho$ and $\log T$), and `LCONDO` (true if computed). If `LCONDO` is false, GETOPAC falls back to the Hubbard–Lampe formula or uses no conductive opacity.

**The method.**
1. Number fractions of H, He and metals (taken as oxygen, $A = 16$), $w_k = (X_k/A_k)/\sum_j(X_j/A_j)$, then weighted by ionization: $w_\mathrm{H} f_\mathrm{H^+}$, $w_\mathrm{He}(f_\mathrm{He^+} + 2f_\mathrm{He^{2+}})/2$; metals are taken as fully ionized.
2. Inside $3 \le \log T \le 9$, $-6 \le \log\rho \le 9.75$: the conductivity $K_k$ of each pure composition from CONDOPACP, combined as
$$\frac{1}{K} = \sum_k \frac{w_k}{K_k},$$
and the conductive opacity
$$\kappa_\mathrm{cond} = \frac{16\,\sigma\,T^3}{3\,\rho\,K}, \qquad \log\kappa_\mathrm{cond} = -3.5194 + 3\log T - \log\rho - \log K,$$
with $\log(16\sigma/3) = -3.5194$ in cgs. Its derivatives are $\partial\log\kappa/\partial\log\rho = -1 - \partial\log K/\partial\log\rho$ and $\partial\log\kappa/\partial\log T = 3 - \partial\log K/\partial\log T$.
   These limits are the table's edges (see [[condopacp.f#CONDOPACP|CONDOPACP]], question 1, for the upper ones).
3. Below $\log\rho = -6$, where $\log R = \log\rho - 3(\log T - 6) \ge 0$ (so only for $\log T < 4$): evaluate at $\log\rho = -6$ and extrapolate linearly in $\log\rho$ with the hydrogen table's slope; $\partial\log\kappa/\partial\log T$ is hydrogen's alone, at $\log\rho = -6$.
4. Elsewhere, `LCONDO` stays false, and `OC` is left at $10^{9.9998}$ with `QODC = QOTC = OC`; GETOPAC then either returns before using them ($\log T < 4.2$, or low density) or replaces them with the Hubbard–Lampe formula.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

## Questions for the experts

1. **A sign in the extrapolation.** In step 3, `CONDL = LOG10(…)`, while in step 2 `CONDL = -LOG10(…)`, with the same sum inside. Since $\sum w_k/K_k = 1/K$, step 2 gives $\log K$ but step 3 gives $-\log K$, so the extrapolated opacity has the conductivity's sign reversed. Probably a missing minus sign. The step of the extrapolation also looks reversed: `OCL = OCL + QODC*(-6.0D0-DL)` adds slope × $(-6 - \log\rho)$, where a linear extrapolation from $\log\rho = -6$ adds slope × $(\log\rho + 6)$.
2. **The derivatives of the mixture.** `QODC = CONDL * (WtH1*QODCX + …)` multiplies the weighted derivatives by $\log K$ itself. The derivative of the harmonic sum is $\partial\log K/\partial\log\rho = \sum_k (w_k K/K_k)\,\partial\log K_k/\partial\log\rho$; the factor $\log K$ looks wrong (the commented-out older lines have a different, also unusual, form).
3. **A copy error.** `QOTC` is computed from the density derivatives `QODCX`, `QODCY`, `QODCZ`, not from `QOTCX`, `QOTCY`, `QOTCZ`, so $\partial\log\kappa/\partial\log T$ is wrong.
4. **The metals.** All metals are represented by $Z_\mathrm{ion} = 8$ with $A = 16$ and full ionization; the comment justifies this by their low abundance. Fine for the Sun; for metal-rich or evolved cores (C/O), is it adequate?
5. **Weights by number of ions.** The comment says the weights count only charged atoms; for helium the weight $(f_1 + 2f_2)/2$ mixes ion number and charge. Is this what Chris Burke's code did?

### CONDOPACPINT

Conductive opacity for an H/He/metal mixture: harmonic sum of Potekhin's conductivities for $Z_\mathrm{ion}$ = 1, 2, 8 weighted by ionized number fractions, then $\kappa_\mathrm{cond} = 16\sigma T^3/(3\rho K)$; linear extrapolation below $\log\rho = -6$.
