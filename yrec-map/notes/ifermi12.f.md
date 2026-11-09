## Explanation

**Purpose.** `IFERMI12` returns the inverse of the Fermi–Dirac integral of order 1/2: given $f = F_{1/2}(\eta)$ it returns $\eta$. It uses the rational-function expansions of Antia (1993, ApJS 84, 101), with a stated maximum error of $4.19\times10^{-9}$.

**How it fits.** Called only by [[sneut.f#SNEUT|`SNEUT`]] (the neutrino energy losses), probably to get the electron degeneracy parameter. No COMMON blocks, no calls. `SNEUT` passes $f$ in Antia's normalization, without the factor $1/\Gamma(3/2)$: Its argument $1.1052\times10^8\,\rho Y_e/T^{3/2}$ is $n_e h^3/[4\pi(2m_e kT)^{3/2}]$ in that normalization, and it takes $dF_{1/2}/d\eta = \tfrac12 F_{-1/2}$, as [[zfermim12.f#ZFERMIM12|`ZFERMIM12`]]'s page shows (settled from the code, Nov 9, 2026: [[sneut.f#L1188-L1200]]).

**The method.** For $f < 4$,

$$\eta = \ln\!\left( f\,\frac{\sum_{i=0}^{4} a_i f^i}{\sum_{i=0}^{3} b_i f^i}\right)$$

(a degree-4 numerator `A1`, with leading coefficient 1, over a degree-3 denominator `B1`, both evaluated by Horner's scheme). For $f \ge 4$, with $u = f^{-1/(1+1/2)} = f^{-2/3}$,

$$\eta = \frac{\sum_{i=0}^{6} a'_i u^i}{u\sum_{i=0}^{5} b'_i u^i}.$$

(numerator of degree 6 with leading coefficient 1, denominator of degree 5). The degrees `M1, K1, M2, K2` = 4, 3, 6, 5 are set in a `DATA` statement; `AN` = 1/2 is the order.

**Changed since `rp_1`.** None: the file is the same as at `rp_1`.

### IFERMI12

The inverse Fermi–Dirac integral of order 1/2, two rational expansions split at $f = 4$ (above).
