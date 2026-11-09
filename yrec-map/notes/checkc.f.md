## Explanation

**Purpose.** This file checks the composition after a step of rotational mixing for anomalous abundances (below 0 or above 1), cuts the diffusion time step if it finds any, and recomputes the mean molecular weight, which the mixing changes.

**How it fits.**
- **Inputs:** the arguments `HCOMP` (mass fractions), `IT` (the iteration on the diffusion coefficients), `LPRT`, `M`; `ITDIF2` (the last iteration, for the print) and `LEXCOM` from [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]]; the envelope abundances `XENV`, `ZENV`, `AMUENV` from [[comp_mod.f#COMP_MOD|`COMP_MOD`]] and `YENV`, `Y3ENV` from [[comp2_mod.f#COMP2_MOD|`COMP2_MOD`]]; the start-of-step composition `HCOMPP` from [[oldmod_mod.f#OLDMOD_MOD|`OLDMOD_MOD`]].
- **Who calls it:** [[seculr.f#SECULR|SECULR]], the secular (rotational) mixing step.
- **Outputs:** `DT` (halved on an error), `IREDO`, `LOK`, `LREDO`; small anomalies in `HCOMP` are repaired in place; the mean molecular weight `AMUM` in [[mdphy_mod.f#MDPHY_MOD|`MDPHY_MOD`]], read by [[vcirc.f#VCIRC|VCIRC]], [[setupv.f#SETUPV|SETUPV]] (the $\mu$ gradient), [[getw.f#GETW|GETW]] and [[midmod.f#MIDMOD|MIDMOD]].

**The method.**
1. Species checked: on every iteration only $X$, $Y$ and $^3$He (1, 2, 4); species 5 to 11 (5 to 15 with `LEXCOM`) are mixed by [[seculr.f#SECULR|SECULR]] once, after its iteration loop, and the code's comment names the clip to $[0,1]$ at the start of the next step in [[mix.f#MIX|MIX]] and [[rotmix.f#ROTMIX|ROTMIX]] as their safeguard. $Z$ (3) is skipped, since it "is not diffused as a unit". Only interior points $2..M-1$ are checked.
2. A value outside $[0, 1]$ that is tiny in size, $|X_{j,i}| < 10^{-5} X_{j,M}$ (relative to the surface value), is replaced by $\max(0, \tfrac12(X_{j,i+1} + X_{j,i-1}))$ ([[#L109-L117]]): the comment explains that mixing into a burning region can give small negative abundances. The branch inside it that sets the centre or surface value to 0 (`I.EQ.1.OR.I.EQ.M`, [[#L110-L111]]) is never taken, since the loop runs over $2..M-1$ ([[#L103]]): unused? Otherwise the time step is halved (`LREDO`), up to 3 times; then the run stops with exit status 1. On the first anomaly that is not repaired, the routine jumps to its end, so $\mu$ is not recomputed in that call.

    > **Question** ([[#L109]]). **The repair threshold.** The threshold is relative to the surface abundance $X_{j,M}$. Of the species checked ($X$, $Y$, $^3$He), $^3$He is the one that could be absent at the surface, and then every negative value, however small, cuts the step. Should the threshold have an absolute floor, as `CMINCHK` has in the print below ([[#L150]])?

3. At the last iteration, with `LPRT`, print the largest fractional change of an abundance over the step, and the surface lithium if `LEXCOM`.
4. For `IT > 1`, the mean molecular weight of a fully ionized gas: per ion, from the surface value and the local differences; per electron, directly:
$$\frac{1}{\mu_\mathrm{ion}} = \frac{1}{\mu_\mathrm{ion,env}} + \sum_k \frac{X_k - X_{k,\mathrm{env}}}{A_k}, \qquad \frac{1}{\mu_e} = \frac{X}{A_\mathrm{H}} + 2\left(\frac{Y}{A_4} + \frac{X_3}{A_3}\right) + \frac{Z}{2},$$
for $k$ = H, $^4$He, $Z$ (with $A = 12$), $^3$He; then $\mu = \mu_\mathrm{ion}\mu_e/(\mu_\mathrm{ion} + \mu_e)$, that is $1/\mu = 1/\mu_\mathrm{ion} + 1/\mu_e$. The comment notes that partial ionization would need a correction in massive stars.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`; the local `CMIN` renamed `CMINCHK`.

**Changed since `a8a5950`.** Species 1, 2, and 4 are checked on every iteration, as before; the last iteration's check of species 5 to 11, which ran before SECULR mixed them, is commented out (settles former question 2); the stop after 3 cuts is `STOP 1` (`KNOWN_ISSUES.md`, issue 38).

### CHECKC

Checks abundances after rotational mixing (repairs tiny negatives, halves the step otherwise, stops after 3 cuts) and recomputes the mean molecular weight $\mu$ for a fully ionized gas.
