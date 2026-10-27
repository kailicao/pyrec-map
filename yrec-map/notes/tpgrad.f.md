## Explanation

**Purpose.** `TPGRAD` decides whether a point is convective and gives its temperature gradient $\nabla = d\ln T/d\ln P$. It computes the radiative gradient, compares it with the adiabatic one (the Schwarzschild criterion), and in convective regions solves the mixing-length theory's cubic for the actual gradient and the convective velocity; on request it also gives the gradient's derivatives for the Henyey solution. Its comments assume that the equation of state and the opacity have been computed already.

**How it fits.**
- **Inputs:** arguments: $\log T$, $T$, $\log P$, $P$, $\rho$ (`D`), $\log r$, $\log m$ (`SL`), $L/L_\odot$ (`B`), the opacity $\kappa$ (`O`) and its derivatives, the equation-of-state quantities ($\delta = -$`QDT`, $c_P$ = `QCP`, $\nabla_\mathrm{ad}$ = `DELA`, and derivatives), the rotation factors `FPL`, `FTL`, $\log T_\mathrm{eff}$, and the mixing length `CMIXL` (set for each run by the main program, `CMIXL = CMIXLA(NK)`, and passed down by the callers). Through modules: the constants `CDELRL`, `CMIXL2`, `CMIXL3`, set by [[setups.f#SETUPS|SETUPS]], and `CC13` ([[constants_mod.f|`CONSTANTS_MOD`]]); the temperature above which MLT is skipped, `TGCUT`, the overshoot switch `LADOV` and the spot parameters `SPOTF`, `SPOTX`, `LSDEPTH` ([[nmlpar_mod.f|`NMLPAR_MOD`]]); the overshoot shells `IOV1`, `IOV2`, `IOVIM` ([[dpmix_mod.f|`DPMIX_MOD`]]); `ISHORT` ([[iounits_mod.f|`IOUNITS_MOD`]]).
- **Who calls it:** the routines that evaluate the physics at a point: [[physic.f#PHYSIC|PHYSIC]], [[coefft.f#COEFFT|COEFFT]], [[qenv.f#QENV|QENV]], [[sconvec.f#SCONVEC|SCONVEC]] and [[starin.f#STARIN|STARIN]].
- **Outputs:** `LCONV`, `DELR` ($\nabla_\mathrm{rad}$), `DEL` ($\nabla$), `VEL` (the convective velocity, cm/s), and with `LDERIV` the logarithmic derivatives of $\nabla$ (`QACT`, `QACP`, `QACR`). It sets `ALFMLT`, `PHMLT`, `CMXMLT` in [[pualpha_mod.f|`PUALPHA_MOD`]] to zero, for the pulsation output of [[coefft.f#COEFFT|COEFFT]], [[envint.f#ENVINT|ENVINT]] and [[wrtmod.f#WRTMOD|WRTMOD]].

**The method.**
1. **Radiative gradient.** With `CDELRL` = $-\log(4\pi/3) - \log\sigma - \log 16$ (from `SETUPS`),
   $$\nabla_\mathrm{rad} = \frac{3\,\kappa\,L\,P}{64\pi\,\sigma\,G\,m\,T^4}\;\frac{f_T}{f_P},$$
   with $L = $ `B`$\,L_\odot$, and $f_P$, $f_T$ the rotational distortion factors.
2. **Radiative** if $\nabla_\mathrm{rad} - \nabla_\mathrm{ad} \le 10^{-6}$: $\nabla = \nabla_\mathrm{rad}$, $v = 0$; but inside an adiabatic overshoot region (`LADOV`, shell `IOVIM` between `IOV1` and `IOV2`) $\nabla = \nabla_\mathrm{ad}$.
3. **Convective:** above `TGCUT` (cores), $\nabla = \nabla_\mathrm{ad}$ and $v = 10^{-11}$, without MLT.
4. **Spots** (G. Somers 9/14): the radiative flux in convective regions is reduced, $\nabla_\mathrm{rad} \to \nabla_\mathrm{rad}/(f x^4 + 1 - f)$, with $f$ = `SPOTF`; the contrast $x$ is `SPOTX`, or with `LSDEPTH` varies with depth as the comment derives, $x(T) = 1 - (1 - x_\mathrm{surf})\,T_\mathrm{amb}/T$.
5. **Mixing-length theory.** With $g = Gm/r^2$, $H_P = P/(\rho g)$, the mixing length $\ell$ in units of $H_P$ (`CMIXL`), $\phi = \ell\,\kappa\rho H_P$ (the optical thickness of an element), `CMIXL2` = 1/3 and `CMIXL3` = $16\sqrt2\,\sigma$:
   $$A_1 = \frac{16\sqrt2\,\sigma\,T^3\kappa}{c_P\,(1 + \phi^2/3)\,\sqrt{(\nabla_\mathrm{rad} - \nabla_\mathrm{ad})\,g\,\delta/H_P}},\qquad A_3 = \frac{3\phi^2}{4\,(1 + \phi^2/3)\,A_1},$$
   and the cubic
   $$A_3 V^3 + V^2 + A_1 V - 1 = 0$$
   is solved for $V$ by a Newton iteration with a second-order correction (at most 25 steps, tolerance $10^{-10}$), starting from $V = 1/A_1$, or $V = A_3^{-1/3}$ when $A_3 > 10^3$. Then
   $$\nabla = \nabla_\mathrm{ad} + (\nabla_\mathrm{rad} - \nabla_\mathrm{ad})\,V(V + A_1),\qquad v = V\,\sqrt{\frac{g\,\delta\,\ell^2 H_P\,(\nabla_\mathrm{rad} - \nabla_\mathrm{ad})}{8}} .$$
   If the cubic does not converge, the point is taken as adiabatic, with a message. If $A_1$'s square root would be of a negative number, the run stops (`STOP 912`, "RUN ENDED").
6. **Derivatives** (`LDERIV`): of $A_1$, $A_3$ and $V$ with respect to $\ln T$, $\ln P$, $\ln r$, combined into those of $\nabla$.

**Changed since `rp_1`.** COMMON blocks to modules, `IMPLICIT NONE` (the unused `CTLIM` dropped); `CMIXL` is now an argument instead of a COMMON variable; the cubic's starting value uses `CC13` instead of the literal 0.333333333; the negative-square-root message now says "RUN ENDED" instead of "assumed adiabatic convection", which settles former question 2 (stopping is intended), so former questions 3–5 are now 2–4.

## Questions for the experts

1. **A typo in the velocity.** When `G*(-QDT)*PRESHT*DELDEL` is not positive, `VEL = 1.0D0-11`, which is $1 - 11 = -10$, not $10^{-11}$ as elsewhere in the routine.
2. **Spots and the criterion.** The radiative/convective decision uses $\nabla_\mathrm{rad}$ without the spot correction; the correction is applied only after the point is found convective, and the returned `DELR` and the derivatives (`QDDELT`, `QDDELP`) are uncorrected. And `DELDEL` is recomputed with the correction after the point is found convective; if the correction makes it negative, `TEST` is negative and the run stops (`STOP 912`).
3. **`PUALPHA` is always zero.** `ALFMLT`, `PHMLT` and `CMXMLT` are set to zero on entry and never computed, but `COEFFT`, `ENVINT` and `WRTMOD` store and write them. Is the pulsation output's MLT data lost?
4. **Unused values.** `DELPM` and `RRR` are computed but not used.

### TPGRAD

The Schwarzschild test and the temperature gradient: radiative, adiabatic (cores, overshoot), or from the mixing-length cubic, with the convective velocity and, on request, the gradient's derivatives.
