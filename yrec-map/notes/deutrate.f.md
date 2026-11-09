## Explanation

**Purpose.** This file computes, at one point, the rate of deuterium burning by $^2$H(p,$\gamma$)$^3$He out of equilibrium ("MHP 5/02"), for the burning done in [[dburn.f#DBURN|DBURN]] and [[dburnm.f#DBURNM|DBURNM]]. Screening is left out, "reasonable given the low temperatures involved".

**How it fits.**
- **Inputs:** the arguments `DL` ($\log\rho$), `TL` ($\log T$), `X` (hydrogen), `I` (the point), `ITLVL` (the level of iteration); `JCZ` (the base of the surface convection zone) from [[deuter_mod.f#DEUTER_MOD|`DEUTER_MOD`]]; `TAUCZ` (convective overturn time) from [[ovrtrn_mod.f#OVRTRN_MOD|`OVRTRN_MOD`]]; `CLN`, `CC13` and `CAVOG` (Avogadro's number, $N_A = 1/m_u$) from [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]]; the deuteron mass in amu, `AMDEUT` $= 2.013553$, set here (the same value as `ANUC(3)` in [[engeb.f#ENGEB|ENGEB]]; the comment asks to keep the two in step).
- **Who calls it:** [[mix.f#MIX|MIX]], for every point from the centre out until $T$ falls below `TCUT(1)`, when the surface deuterium (`HCOMP(12,M)`, or the accreted `COMPACC(12)` if larger, during accretion) exceeds $10^{-11}$.
- **Outputs:** `DRATE(I)` in `DEUTER_MOD`, and at the first level of iteration also `DRATE0(I)` (the rate at the start of the step). DBURN reads both; [[midmod.f#MIDMOD|MIDMOD]] interpolates between them for DBURNM.

**The method.** With $T_9 = T/10^9$ K, the reaction rate per mole (the fit of Caughlan and Fowler type, by its form):
$$N_A\langle\sigma v\rangle = 2.240\times10^{3}\;T_9^{-2/3}\;e^{-3.72\,T_9^{-1/3}}\left(1 + 0.112\,T_9^{1/3} + 3.38\,T_9^{2/3} + 2.65\,T_9\right),$$
then, with $A_D$ = `AMDEUT` $= 2.013553$,
$$\mathtt{DRATE} = X\,\rho\,N_A\langle\sigma v\rangle \cdot \frac{N_A}{A_D}\cdot C_{21}, \qquad C_{21} = 5.240358\times10^{-8} \approx \frac{3.156\times10^{16}\ \mathrm{s\,Gyr^{-1}}}{N_A},$$
so `DRATE` $\approx X\rho N_A\langle\sigma v\rangle/A_D$ per Gyr (the value of $C_{21}$ is read as seconds per Gyr over $N_A$; this is an inference). The burning routines then use $X_D \propto e^{-2\,\mathtt{DRATE}\,t}$, so the destruction rate per deuteron is $\lambda = 2\,\mathtt{DRATE} = (2/A_D)\,X\rho N_A\langle\sigma v\rangle \approx 0.993\,X\rho N_A\langle\sigma v\rangle$ per Gyr. The comment calls `CAVOG/AMDEUT` "Avogadro's number divided by the mass of the deuteron in amu".

**The convection-zone cap.** In the surface convection zone ($I \ge$ `JCZ`, with $\tau_\mathrm{cz} > 1$), $X\cdot$`RDEUT` is capped at $(N_A/A_D)/\tau_\mathrm{cz}$ (`CAVOG/AMDEUT/TAUCZ`), so that deuterium burns "on a time scale no shorter than the convective overturn timescale". [[taucal.f#TAUCAL|TAUCAL]] forms `TAUCZ` as a length in cm over a convective velocity (`CZWIDE/CVEAVG` or `PSCA/CVEL`, [[taucal.f#L159-L165]], [[taucal.f#L179]]), so in seconds, with YREC's cgs velocities; then `DRATE` $= C_{21}\,(N_A/A_D)/\tau_\mathrm{cz}$ is $1/(A_D\,\tau_\mathrm{cz})$ in Gyr$^{-1}$, and the destruction rate per deuteron, $2\,$`DRATE`, is $0.993/\tau_\mathrm{cz}$: the cap is consistent with the comment (settled from the code, Nov 9, 2026: [[#L65-L66]], [[#L81]]).

> **Question** ([[#L65]]). **The test `TAUCZ > 1`.** With `TAUCZ` in seconds, the test excludes only overturn times below one second, which a convection zone does not have. Is it meant as a guard against an unset or zero `TAUCZ` (no surface convection zone), and would `TAUCZ > 0` say so more plainly?

**Changed since `rp_1`.** `C21` is now set in double precision (`5.240358D-8`), which settles the former question on its single-precision constant; COMMON blocks to modules, `IMPLICIT NONE`.

**Changed since `09c3b9b`.** The rate's leading power of $T_9$ is now $T_9^{-2/3}$ (`T9M23`), as in the usual fit, not $T_9^{+2/3}$, which settles former question 1 (the rate rises by $T_9^{-4/3}$, about $10^{4}$ at $10^6$ K); the factor $3.0115\times10^{23}$ ($6.023\times10^{23}/2$) is now `CAVOG/AMDEUT`, Avogadro's number from `CONSTANTS_MOD` over the deuteron's mass in amu (a new `DATA` value), in the rate and in the cap (both 0.7% smaller); former question 2 is now 1.

### DEUTRATE

The rate of $^2$H(p,$\gamma$)$^3$He at one point, without screening, in units the burning routines expect (per Gyr), capped in the surface convection zone by the overturn time; sets `DRATE` (and `DRATE0` at the first level).
