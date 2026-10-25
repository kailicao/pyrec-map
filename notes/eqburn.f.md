## Explanation

**Purpose.** `EQBURN` gives explicit hydrogen and helium burning rates for one shell or one convection zone, assuming that $^3$He and the CN cycle are in equilibrium. Its comment says the result is "an initial guess at the burning rates at the start of the time step", which a fully implicit non-equilibrium calculation can supplement later.

**How it fits.**
- **Who calls it:** [[mix.f#MIX|MIX]] (twice, to use the explicit hydrogen burning rate) and [[xtime.f#XTIME|XTIME]], which turns `DXDT` into a nuclear time step limit.
- **Inputs:** the reaction-rate arrays `HR1`…`HR12`, which both callers compute with [[rates.f#RATES|RATES]] just before the call. [[kemcom.f#KEMCOM|KEMCOM]]'s header gives their units: rates "per gigayear per amu", to be multiplied by the reactants' mass fractions and the product's atomic weight; so `DXDT` and the other outputs are changes of mass fraction per Gyr, the shell masses `HS2`, the temperatures `HT` ($\log T$), and the range `IBEGIN..IEND`. The abundances come from the previous model, `HCOMPP` in `/OLDMOD/`.
- **Outputs:** the rates `DXDT`, `DYDT`, `DCDT`, `DODT` (hydrogen, helium, $^{12}$C, $^{16}$O) and the zone's mean `X`, `Z`, `XC12`, `XO16`.
- **COMMON blocks:** `/CTLIM/` gives the temperature cutoffs `TCUT(1..4)` (cutoffs in $\log T$, set in [[parmin.f#PARMIN|PARMIN]]; the defaults are 6.5, 6.5, 6.82, 7.7), shared with 27 routines; `/OLDMOD/` holds the previous model, written by the main program and read by 18 routines.

**The method.**
1. Below `TCUT(1)` at the zone's first shell, all rates are zero.
2. For a convection zone (`IBEGIN` ≠ `IEND`), abundances $X_j$ and rates $R_k$ are mass-weighted means over the zone, $\bar q = \sum_i q_i m_i / \sum_i m_i$ with $m_i$ = `HS2`.
3. **pp chains** (above `TCUT(2)`, if $X > 10^{-10}$). The equilibrium $^3$He abundance solves $2R_{33}x^2 + R_{34}Y x - R_{11}X^2 = 0$:
$$x_{3,\mathrm{eq}} = \frac{\sqrt{(R_{34}Y)^2 + 8R_{33}R_{11}X^2} - R_{34}Y}{4R_{33}},$$
with $R_{11}$ = `GR1`, $R_{33}$ = `GR2`, $R_{34}$ = `GR3`. The code takes $x_3 = \min(x_3, x_{3,\mathrm{eq}})$ "to avoid spuriously high burning rates in outer layers", and
$$\dot X = -3R_{11}X^2 + 2R_{33}x_3^2 - R_{34}Y x_3 .$$
4. **CN cycle** (above `TCUT(3)`, and only if step 3 ran). In equilibrium, $X_{12} = X_{14}R_{14}/R_{12}$ and $X_{13} = X_{14}R_{14}/R_{13}$, with $R_{12}, R_{13}, R_{14}$ = `GR4`, `GR5`, `GR6`, and the number of CN nuclei $S = X_{12}/12 + X_{13}/13 + X_{14}/14$ is conserved, so
$$X_{14} = \frac{S}{R_{14}/(12R_{12}) + R_{14}/(13R_{13}) + 1/14}.$$
Then $\dot X \mathrel{-}= X\,(R_{12}X_{12} + R_{13}X_{13} + 2R_{14}X_{14} + 2R_{16}X_{16})$, with $R_{16}$ = `GR7` ($^{16}$O + p).
5. **Helium burning** (above `TCUT(4)`, if $Y > 10^{-10}$): with $r_{3\alpha} = R_{3\alpha}Y^3$ (`GR12`) and $r_{12\alpha} = R_{12\alpha}YX_{12}$ (`GR10`),
$$\dot Y = -4(r_{12\alpha} + 3r_{3\alpha}),\quad \dot X_{12} = 12(r_{3\alpha} - r_{12\alpha}),\quad \dot X_{16} = 16\,r_{12\alpha}.$$

**KC's changes.** Unused arguments removed (2025-05-31): `HF1`, `HR8`, `HR9`, `HR11`; their uses were already commented out.

## Questions for the experts

1. **Equilibrium CN abundances returned.** `XC12` is overwritten by its CN-equilibrium value in step 4 and returned to the caller. Do `MIX` and `XTIME` expect the actual abundance or the equilibrium one? The helium-burning step also uses this equilibrium `XC12` for $^{12}$C + $\alpha$, except when $X \le 10^{-10}$, where the code jumps past the CN step and uses the actual abundance.
2. **Division by a rate.** Step 3 divides by `GR2`, and step 4 by `GR4` and `GR5`. Are these rates guaranteed nonzero above the cutoffs?
3. **Factor 2 for $^{16}$O.** The $^{16}$O + p term counts two protons per reaction, like $^{14}$N + p. Is that the intended accounting for the ON branch?

### EQBURN

Explicit burning rates for a shell or a convection zone, with $^3$He and CN in equilibrium (equations above).
