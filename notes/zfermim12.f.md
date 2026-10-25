## Explanation

**Purpose.** `ZFERMIM12` evaluates the complete Fermi–Dirac integral of order $-\tfrac12$,
$$F_{-1/2}(x) = \int_0^\infty \frac{t^{-1/2}}{e^{t - x} + 1}\,dt,$$
by the rational-function approximations of Antia (1993, ApJS 84, 101); its comment gives a maximum error of $1.23\times10^{-12}$.

**How it fits.** Called by [[sneut.f#SNEUT|SNEUT]] (neutrino losses, by its name). No COMMON blocks.

**The method.** For $x < 2$, with $z = e^x$,
$$F_{-1/2}(x) = z\,\frac{P_7(z)}{Q_7(z)},$$
and for $x \ge 2$, with $z = 1/x^2$,
$$F_{-1/2}(x) = \sqrt{x}\,\frac{P_{11}(z)}{Q_{11}(z)},$$
where the polynomials' coefficients are `a1`, `b1` (degree 7) and `a2`, `b2` (degree 11). Both numerators have leading coefficient 1: the loops start from `xx + a1(m1)` and `xx + a2(m2)`, so `a1(8)` and `a2(12)`, both 1, are not read.

**The convention.** The integral is Antia's, without the factor $1/\Gamma(k+1)$: the coefficients give $F_{-1/2} \to \Gamma(\tfrac12)\,e^x$ for small $x$ and $2\sqrt x$ for large $x$. [[sneut.f#SNEUT|`SNEUT`]] uses it in the same convention: there $d\nu/dF_{1/2} = 1/\bigl(\tfrac12F_{-1/2}(\nu)\bigr)$, and the argument it passes to [[ifermi12.f#IFERMI12|`IFERMI12`]], $1.1052\times10^8\,\rho Y_e/T^{3/2}$, equals $n_e h^3/[4\pi(2m_e kT)^{3/2}]$ in it.

**KC's changes.** Removed the unused variable `an` (the order, $-0.5$) from the declarations and the `DATA` statement (2025-05-31).

## Questions for the experts

None open: the normalisation, once asked here, is settled above (The convention).

### ZFERMIM12

Fermi–Dirac integral of order $-1/2$ by Antia's (1993) rational approximations.
