## Explanation

**Purpose.** This file checks the composition after a step of rotational mixing for anomalous abundances (below 0 or above 1), cuts the diffusion time step if it finds any, and recomputes the mean molecular weight, which the mixing changes.

**How it fits.**
- **Inputs:** the arguments `HCOMP` (mass fractions), `IT` (the iteration on the diffusion coefficients), `LPRT`, `M`; `ITDIF2` (the last iteration, for the print) and `LEXCOM` from [`NMLPAR_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/nmlpar_mod.f#L32-L279); the envelope abundances `XENV`, `ZENV`, `AMUENV` from [`COMP_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/comp_mod.f#L19-L34) and `YENV`, `Y3ENV` from [`COMP2_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/comp2_mod.f#L19-L27); the start-of-step composition `HCOMPP` from [`OLDMOD_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/oldmod_mod.f#L19-L43).
- **Who calls it:** [SECULR](https://github.com/yreclab/yrec/blob/7be4133/src/seculr.f#L6-L532), the secular (rotational) mixing step.
- **Outputs:** `DT` (halved on an error), `IREDO`, `LOK`, `LREDO`; small anomalies in `HCOMP` are repaired in place; the mean molecular weight `AMUM` in [`MDPHY_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/mdphy_mod.f#L19-L41), read by [VCIRC](vcirc.f.md#vcirc), [SETUPV](https://github.com/yreclab/yrec/blob/7be4133/src/setupv.f#L3-L467) (the $`\mu`$ gradient), [GETW](getw.f.md#getw) and [MIDMOD](https://github.com/yreclab/yrec/blob/7be4133/src/midmod.f#L2-L523).

**The method.**
1. Species checked: on every iteration only $`X`$, $`Y`$ and $`^3\mathrm{He}`$ (1, 2, 4); species 5 to 11 (5 to 15 with `LEXCOM`) are mixed by [SECULR](https://github.com/yreclab/yrec/blob/7be4133/src/seculr.f#L6-L532) once, after its iteration loop, and the code's comment names the clip to $`[0,1]`$ at the start of the next step in [MIX](https://github.com/yreclab/yrec/blob/7be4133/src/mix.f#L26-L507) and [ROTMIX](https://github.com/yreclab/yrec/blob/7be4133/src/rotmix.f#L5-L251) as their safeguard. $`Z`$ (3) is skipped, since it "is not diffused as a unit." Only interior points $`2..M-1`$ are checked.
2. A value outside $`[0, 1]`$ that is tiny in size, $`|X_{j,i}| \lt{} 10^{-5} X_{j,M}`$ (relative to the surface value), is replaced by $`\max(0, \tfrac12(X_{j,i+1} + X_{j,i-1}))`$ ([lines 109–117](https://github.com/yreclab/yrec/blob/7be4133/src/checkc.f#L109-L117)): the comment explains that mixing into a burning region can give small negative abundances. The branch inside it that sets the centre or surface value to 0 (`I.EQ.1.OR.I.EQ.M`, [lines 110–111](https://github.com/yreclab/yrec/blob/7be4133/src/checkc.f#L110-L111)) is never taken, since the loop runs over $`2..M-1`$ ([line 103](https://github.com/yreclab/yrec/blob/7be4133/src/checkc.f#L103)): unused? Otherwise the time step is halved (`LREDO`), up to 3 times; then the run stops with exit status 1. On the first anomaly that is not repaired, the routine jumps to its end, so $`\mu`$ is not recomputed in that call.

    > **Question** ([line 109](https://github.com/yreclab/yrec/blob/7be4133/src/checkc.f#L109)). **The repair threshold.** The threshold is relative to the surface abundance $`X_{j,M}`$. Of the species checked ($`X`$, $`Y`$, $`^3\mathrm{He}`$), $`^3\mathrm{He}`$ is the one that could be absent at the surface, and then every negative value, however small, cuts the step. Should the threshold have an absolute floor, as `CMINCHK` has in the print below ([line 150](https://github.com/yreclab/yrec/blob/7be4133/src/checkc.f#L150))?

3. At the last iteration, with `LPRT`, print the largest fractional change of an abundance over the step, and the surface lithium if `LEXCOM`.
4. For `IT > 1`, the mean molecular weight of a fully ionized gas: per ion, from the surface value and the local differences; per electron, directly:
   
   $$\displaystyle \frac{1}{\mu\_\mathrm{ion}} = \frac{1}{\mu\_\mathrm{ion,env}} + \sum\_k \frac{X\_k - X\_{k,\mathrm{env}}}{A\_k}, \qquad \frac{1}{\mu\_e} = \frac{X}{A\_\mathrm{H}} + 2\left(\frac{Y}{A\_4} + \frac{X\_3}{A\_3}\right) + \frac{Z}{2},$$
   
   for $`k`$ = H, $`^4\mathrm{He}`$, $`Z`$ (with $`A = 12`$), $`^3\mathrm{He}`$; then $`\mu = \mu_\mathrm{ion}\mu_e/(\mu_\mathrm{ion} + \mu_e)`$, that is $`1/\mu = 1/\mu_\mathrm{ion} + 1/\mu_e`$. The comment notes that partial ionization would need a correction in massive stars.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`; the local `CMIN` renamed `CMINCHK`.

**Changed since `a8a5950`.** Species 1, 2, and 4 are checked on every iteration, as before; the last iteration's check of species 5 to 11, which ran before SECULR mixed them, is commented out (settles former question 2); the stop after 3 cuts is `STOP 1` (`KNOWN_ISSUES.md`, issue 38).

### CHECKC

Checks abundances after rotational mixing (repairs tiny negatives, halves the step otherwise, stops after 3 cuts) and recomputes the mean molecular weight $`\mu`$ for a fully ionized gas.
