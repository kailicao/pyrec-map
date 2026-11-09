## Explanation

**Purpose.** This file computes the conductive opacity for a mixture of hydrogen, helium and metals from Potekhin's conductivity tables ("based on Chris Burke's conductive opacity code", LLP 5/31/04). [[getopac.f#GETOPAC|GETOPAC]] then adds it to the radiative opacity in harmonic sum.

**How it fits.**
- **Inputs:** the arguments `DL` ($\log\rho$), `TL` ($\log T$), `X`, `Z`, and `FXION`, the ionization fractions (of H; of He singly and doubly).
- **Who calls it:** [[getopac.f#GETOPAC|GETOPAC]], when the Potekhin option (`LcondOpacP`) is on.
- **What it calls:** [[condopacp.f#CONDOPACP|CONDOPACP]], for $Z_\mathrm{ion}$ = 1, 2 and 8.
- **Outputs:** `OC` and `OCL` (the conductive opacity and its log), `QODC`, `QOTC` (its derivatives in $\log\rho$ and $\log T$), and `LCONDO` (true if computed). If `LCONDO` is false, GETOPAC falls back to the Hubbard–Lampe formula or uses no conductive opacity.

**The method.**
1. Number fractions of H, He and metals (taken as oxygen, $A = 16$), $w_k = (X_k/A_k)/\sum_j(X_j/A_j)$, then weighted by ionization: $w_\mathrm{H} f_\mathrm{H^+}$, $w_\mathrm{He}(f_\mathrm{He^+} + 2f_\mathrm{He^{2+}})/2$; metals are taken as fully ionized.

    > **Question** ([[#L30-L40]]). **Weights by number of ions.** The comment says the weights count only charged atoms; for helium the weight $(f_1 + 2f_2)/2$ mixes ion number and charge. Is this what Chris Burke's code did?

2. Inside $3 \le \log T \le 9$, $-6 \le \log\rho \le 9.75$: the conductivity $K_k$ of each pure composition from CONDOPACP, combined as
$$\frac{1}{K} = \sum_k \frac{w_k}{K_k},$$
and the conductive opacity
$$\kappa_\mathrm{cond} = \frac{16\,\sigma\,T^3}{3\,\rho\,K}, \qquad \log\kappa_\mathrm{cond} = -3.5194 + 3\log T - \log\rho - \log K,$$
with $\log(16\sigma/3) = -3.5194$ in cgs. Its derivatives are $\partial\log\kappa/\partial\log\rho = -1 - \partial\log K/\partial\log\rho$ and $\partial\log\kappa/\partial\log T = 3 - \partial\log K/\partial\log T$.
   These limits are the table's edges (see the suspected bug 1 of [[condopacp.f#CONDOPACP|CONDOPACP]], [[condopacp.f#L99-L109]], for the upper ones).

    > **Question** ([[#L21]]; [[#L41]]; [[#L58]]). **The metals.** All metals are represented by $Z_\mathrm{ion} = 8$ with $A = 16$ and full ionization; the comment justifies this by their low abundance. Fine for the Sun; for metal-rich or evolved cores (C/O), is it adequate?

3. Below $\log\rho = -6$, where $\log R = \log\rho - 3(\log T - 6) \ge 0$ (so only for $\log T < 4$): evaluate at $\log\rho = -6$ and extrapolate linearly in $\log\rho$ with the hydrogen table's slope; $\partial\log\kappa/\partial\log T$ is hydrogen's alone, at $\log\rho = -6$.
4. Elsewhere, `LCONDO` stays false, and `OC` is left at $10^{9.9998}$ with `QODC = QOTC = OC`; GETOPAC then either returns before using them ($\log T < 4.2$, or low density) or replaces them with the Hubbard–Lampe formula.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

## Bugs, by priority

1. **(a)** **The mixture's derivatives are multiplied by $\log K$.** ([[#L68]]; [[#L72]]) `QODC = CONDL * (WtH1*QODCX + …)` multiplies the weighted derivatives by `CONDL` = $\log K$ itself. The derivative of the harmonic sum $1/K = \sum_k w_k/K_k$ is $\partial\log K/\partial\log\rho = \sum_k (w_k K/K_k)\,\partial\log K_k/\partial\log\rho$, with no factor $\log K$: For pure hydrogen ($w_\mathrm{H} = 1$) the code gives $\log K$ times the right value. The commented-out older lines ([[#L69-L70]], [[#L73-L74]]) weight each derivative by its `CONDX`, as the fix below does, but also multiply by `CONDL`. What follows: `QODC` and `QOTC` are wrong wherever Potekhin's opacity is computed ($\log\rho \ge -6$), and `GETOPAC` folds them into the opacity's derivatives `QOD` and `QOT` with the weight $\kappa_\mathrm{rad}/(\kappa_\mathrm{rad} + \kappa_\mathrm{cond})$ ([[getopac.f#L219-L222]]), so the error counts where conduction matters (degenerate cores). Only with `LcondOpacP` (off by default, set in all 51 decks of the test suite and recommended by the user guide). Read from the code, not run; how `QOD` and `QOT` are used further (the solver's derivatives, or the model itself) was not traced. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to take the derivative of the harmonic sum: each
    C composition weighted by its share of 1/K, WT*CONDX*K, K = 10**CONDL.
               QODC = 10.0D0**CONDL*(WtH1*CONDX*QODCX + WtHe4*CONDY*QODCY
         *            + WtOx*CONDZ*QODCZ)
    ```

2. **(a)** **The temperature derivative is taken from the density derivatives.** ([[#L72]]) `QOTC` is computed from `QODCX`, `QODCY`, `QODCZ`, not from `QOTCX`, `QOTCY`, `QOTCZ` (which the calls at [[#L56-L58]] return and nothing reads), so $\partial\log\kappa/\partial\log T$ is $3 - \partial\log K/\partial\log\rho$ (times $\log K$, bug 1). The commented-out older lines [[#L73-L74]] used `QOTCX`, `QOTCY`, `QOTCZ`. Same path as bug 1. Read from the code, not run. **A possible fix** (in the form of bug 1's):

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to take the temperature derivatives QOTCX, QOTCY and
    C QOTCZ, weighted as the density derivatives are.
                QOTC = 10.0D0**CONDL*(WtH1*CONDX*QOTCX + WtHe4*CONDY*QOTCY
         *             + WtOx*CONDZ*QOTCZ)
    ```

3. **(a)** **A sign in the extrapolation below $\log\rho = -6$.** ([[#L92]]; [[#L64]]) In step 3, `CONDL = LOG10(…)`, while in step 2 `CONDL = -LOG10(…)`, with the same sum inside. Since $\sum_k w_k/K_k = 1/K$, step 2 gives $\log K$ but step 3 gives $-\log K$, so the extrapolated $\log\kappa_\mathrm{cond}$ ([[#L96]]) is off by $2\log K$. Probably a missing minus sign. The path: `LcondOpacP`, $\log\rho < -6$ and $\log R \ge 0$, so only for $\log T < 4$ (cool surface layers); `GETOPAC` uses the result whenever `LCONDO` is true ([[getopac.f#L197]]). How much the total opacity changes there was not traced. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to give CONDL the sign it has above, log K.
               CONDL = -LOG10(WtH1*CONDX + WtHe4*CONDY + WtOx*CONDZ)
    ```

4. **(a)** **The step of the extrapolation is reversed.** ([[#L99]]) `OCL = OCL + QODC*(-6.0D0-DL)` adds the slope times $(-6 - \log\rho)$, where a linear extrapolation from $\log\rho = -6$ adds the slope times $(\log\rho + 6)$; the extrapolated opacity moves the wrong way as the density falls. Same path as bug 3. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to extrapolate from log rho = -6 down to DL.
               OCL = OCL + QODC*(DL+6.0D0)
    ```

### CONDOPACPINT

Conductive opacity for an H/He/metal mixture: harmonic sum of Potekhin's conductivities for $Z_\mathrm{ion}$ = 1, 2, 8 weighted by ionized number fractions, then $\kappa_\mathrm{cond} = 16\sigma T^3/(3\rho K)$; linear extrapolation below $\log\rho = -6$.
