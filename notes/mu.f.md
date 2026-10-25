## Explanation

**Purpose.** Computes the gas's mean molecular weight terms for the equation-of-state routines: the ions' contribution `AMU`, the free electrons' contribution `EMU`, and `RMU` $= \mathcal{R}\,(\mathrm{AMU}+\mathrm{EMU})$.

**How it fits.**
- **Inputs:** $T$, $P$, $\rho$ (`D`), $X$, $Z$, and `BETA` (probably the ratio of gas to total pressure, as the name suggests); the envelope composition and its `AMUENV` from `/COMP/`; the gas constant `CGAS` from `/CONST2/`.
- **Who calls it:** the equation-of-state routines [[meqos.f#MEQOS|MEQOS]], [[oeqos.f#OEQOS|OEQOS]], [[oeqos01.f#OEQOS01|OEQOS01]] and [[oeqos06.f#OEQOS06|OEQOS06]].
- **Outputs:** `AMU`, `EMU`, `RMU`.
- **COMMON blocks:** `/COMP/`, `/CONST2/`; `/CTLIM/`, `/CONST1/` and `/CCOUT2/` are declared but not used.

**The method.**
1. **Ions.** If $X$ and $Z$ differ from the envelope's by less than $10^{-5}$ in total, `AMU = AMUENV`. Otherwise the change is added species by species, with "excess Z (metals) … in the form of carbon(12)":
$$\mathrm{AMU} = \mathrm{AMU_{env}} + \frac{\Delta X}{1.008} + \frac{\Delta Y}{4.004} + \frac{\Delta Z}{12.016},\qquad \Delta Y = -(\Delta X + \Delta Z),$$
(the weights `ATOMWT` are 0.9921, 0.24975 and 0.08322, i.e. $1/A$). So `AMU` is the number of ions per unit mass in units of $1/m_u$, the inverse of the ions' mean molecular weight.
2. **Electrons.** From the gas pressure, $\beta P = \rho\,\mathcal{R}\,T\,(\mathrm{AMU}+\mathrm{EMU})$, so
$$\mathrm{EMU} = \mathrm{AMU}\left(\frac{\beta P}{\rho\,T\,\mathcal{R}\,\mathrm{AMU}} - 1\right),\qquad \mathrm{RMU} = \mathcal{R}\,(\mathrm{AMU}+\mathrm{EMU}) = \frac{\beta P}{\rho T}.$$

## Questions for the experts

1. **An unused weight.** `ATOMWT(4)` $= 0.4995$ ($2/4.004$, probably for ³He or for He's electrons) is never used. A leftover?
2. **Carbon for the metals.** The comment says excess metals are carbon, which suits helium-burning regions. Is this still the intended approximation for metal changes from settling?
