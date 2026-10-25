## Explanation

**Purpose.** This file computes, at one point, the rate of deuterium burning by $^2$H(p,$\gamma$)$^3$He out of equilibrium ("MHP 5/02"), for the burning done in [[dburn.f#DBURN|DBURN]] and [[dburnm.f#DBURNM|DBURNM]]. Screening is left out, "reasonable given the low temperatures involved".

**How it fits.**
- **Inputs:** the arguments `DL` ($\log\rho$), `TL` ($\log T$), `X` (hydrogen), `I` (the point), `ITLVL` (the level of iteration); `JCZ` (the base of the surface convection zone) in `/DEUTER/`; `TAUCZ` (convective overturn time) in `/OVRTRN/`.
- **Who calls it:** [[mix.f#MIX|MIX]], for every point from the centre out until $T$ falls below `TCUT(1)`, when the surface deuterium (`HCOMP(12,M)`, or the accreted `COMPACC(12)` if larger, during accretion) exceeds $10^{-11}$.
- **Outputs:** `DRATE(I)` in `/DEUTER/`, and at the first level of iteration also `DRATE0(I)` (the rate at the start of the step). DBURN reads both; [[midmod.f#MIDMOD|MIDMOD]] interpolates between them for DBURNM.

**The method.** With $T_9 = T/10^9$ K, the reaction rate per mole (the fit of Caughlan and Fowler type, by its form):
$$N_A\langle\sigma v\rangle = 2.240\times10^{3}\;T_9^{\,2/3}\;e^{-3.72\,T_9^{-1/3}}\left(1 + 0.112\,T_9^{1/3} + 3.38\,T_9^{2/3} + 2.65\,T_9\right)\ \text{(as coded)},$$
then
$$\mathtt{DRATE} = X\,\rho\,N_A\langle\sigma v\rangle \cdot \frac{N_A}{2}\cdot C_{21}, \qquad C_{21} = 5.240358\times10^{-8} \approx \frac{3.156\times10^{16}\ \mathrm{s\,Gyr^{-1}}}{N_A},$$
so `DRATE` $= \tfrac12 X\rho N_A\langle\sigma v\rangle$ per Gyr (the value of $C_{21}$ is read as seconds per Gyr over $N_A$; this is an inference). The burning routines then use $X_D \propto e^{-2\,\mathtt{DRATE}\,t}$, so the destruction rate per deuteron is $\lambda = X\rho N_A\langle\sigma v\rangle$. The comment calls $3.0115\times10^{23}$ "Avogadro's number divided by the mass of the deuteron in amu".

**The convection-zone cap.** In the surface convection zone ($I \ge$ `JCZ`, with $\tau_\mathrm{CZ} > 1$), $X\cdot$`RDEUT` is capped at $3.0115\times10^{23}/\tau_\mathrm{CZ}$, so that deuterium burns "on a time scale no shorter than the convective overturn timescale".

**KC's changes.** 2025-05-31: the unused argument `XH2` removed.

## Questions for the experts

1. **A wrong power of $T_9$?** The usual fit for $^2$H(p,$\gamma$)$^3$He (Caughlan and Fowler 1988) is $2.24\times10^{3}\,T_9^{-2/3}\exp(-3.720\,T_9^{-1/3})(1 + \dots)$. The code multiplies by `T9P23` ($T_9^{+2/3}$), while `T9M23` ($T_9^{-2/3}$) is computed and never used. If this is a typo, the rate is too low by $T_9^{4/3}$: about $10^{-4}$ at $10^6$ K. Is it? [[engeb.f#ENGEB|ENGEB]] has the same power (its question 4).
2. **The cap's units.** The cap makes $2\,\mathtt{DRATE} = 1/\tau_\mathrm{CZ}$ in units of Gyr$^{-1}$ only if $\tau_\mathrm{CZ}$ is in seconds. [[taucal.f#TAUCAL|TAUCAL]] forms `TAUCZ` as a length over a convective velocity (`CZWIDE/CVEAVG` or `PSCA/CVEL`), so it is in seconds, probably, and the cap is consistent; the test `TAUCZ > 1` (one second) then excludes almost nothing. Can the experts confirm?
3. **Single precision.** `C21` is set by `DATA` with a single-precision constant (`5.240358E-8`), so it carries about 7 digits.

### DEUTRATE

The rate of $^2$H(p,$\gamma$)$^3$He at one point, without screening, in units the burning routines expect (per Gyr), capped in the surface convection zone by the overturn time; sets `DRATE` (and `DRATE0` at the first level).
