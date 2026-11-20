## Explanation

**Purpose.** `ZFERMIM12` evaluates the complete Fermi–Dirac integral of order $`-\tfrac12`$,
```math
F_{-1/2}(x) = \int_0^\infty \frac{t^{-1/2}}{e^{t - x} + 1}\,dt,
```
by the rational-function approximations of Antia ([1993](https://ui.adsabs.harvard.edu/abs/1993ApJS...84..101A), ApJS 84, 101); its comment gives a maximum error of $`1.23\times10^{-12}`$.

**How it fits.** Called by [SNEUT](https://github.com/yreclab/yrec/blob/7be4133/src/sneut.f#L2-L1355) (neutrino losses, by its name). No COMMON blocks.

**The method.** For $`x \lt{} 2`$, with $`z = e^x`$,
```math
F_{-1/2}(x) = z\,\frac{P_7(z)}{Q_7(z)},
```
and for $`x \ge 2`$, with $`z = 1/x^2`$,
```math
F_{-1/2}(x) = \sqrt{x}\,\frac{P_{11}(z)}{Q_{11}(z)},
```
where the polynomials' coefficients are `a1`, `b1` (degree 7) and `a2`, `b2` (degree 11). Both numerators have leading coefficient 1: the loops start from `xx + a1(m1)` and `xx + a2(m2)`, so `a1(8)` and `a2(12)`, both 1, are not read.

**The convention.** The integral is Antia's, without the factor $`1/\Gamma(k+1)`$: the coefficients give $`F_{-1/2} \to \Gamma(\tfrac12)\,e^x`$ for small $`x`$ and $`2\sqrt x`$ for large $`x`$. [`SNEUT`](https://github.com/yreclab/yrec/blob/7be4133/src/sneut.f#L2-L1355) uses it in the same convention: there $`d\nu/dF_{1/2} = 1/\bigl(\tfrac12F_{-1/2}(\nu)\bigr)`$, and the argument it passes to [`IFERMI12`](ifermi12.f.md#ifermi12), $`1.1052\times10^8\,\rho Y_e/T^{3/2}`$, equals $`n_e h^3/[4\pi(2m_e kT)^{3/2}]`$ in it.

**Changed since `rp_1`.** None: the file is the same as at `rp_1`.

### ZFERMIM12

Fermi–Dirac integral of order $`-1/2`$ by Antia's (1993) rational approximations.
