## Explanation

**Purpose.** Prepares, once per call of the rotational-mixing step, the structural factors that the stability criteria and circulation velocities need at each interface between shells. Its comment explains the scheme: stability is computed for the interface $i/i-1$ and stored in element $i$; each criterion is "a combination of variables stored at each shell multiplied by a gradient between the shells", which must stay below a critical number. `SETUPV` computes the parts that "do not change during a diffusion timestep"; [[vcirc.f#VCIRC|`VCIRC`]] multiplies them by the current $\Omega$ gradients.

**How it fits.**
- **Who calls it:** [[seculr.f#SECULR|`SECULR`]], once per time step, before the iterations.
- **Inputs:** the model's $\log\rho$, $g$ (`HG`), $L$ (solar units), $\log P$, $\log r$, enclosed mass (g), $\log T$, and the range `IMIN`–`IMAX`; from `MDPHY_MOD` the shell values of $\mu$ (`AMUM`), $c_P$ (`CPM`), $\nabla$, $\nabla_\mathrm{ad}$, $\nabla_\mathrm{rad}$ (`DELM`, `DELAM`, `DELRM`), $\varepsilon$ (`ESUMM`), $\kappa$ (`OM`), $\partial\ln\rho/\partial\ln T$ (`QDTM`); from `ROTDER_MOD` the derivatives of $\kappa$ and $\varepsilon$ (`SQOT`, `SQET`) and the nuclear fraction `FRACNUC`, set in [[coefft.f#COEFFT|`COEFFT`]]; the namelist switch `LDIFAD` from `NMLPAR_MOD`.
- **Outputs:** `HRU` (radii), `QWRMAX` (the largest stable $d\Omega/d\ln r$ for the dynamical shear), the interpolation weights `FACI` (an argument owned by `SECULR`, which passes it on to `VCIRC`), and, through modules, read by `VCIRC`, [[codiff.f#CODIFF|`CODIFF`]], [[getfc.f#GETFC|`GETFC`]] and [[dadcoeft.f#DADCOEFT|`DADCOEFT`]]: the interface values in `INTVAR_MOD` (`RM`, `PM`, `TM`, `DM`, `DELMI`, `DELAMI`, `QDTMI`, `HS3`, `EPSILM`, `ALM`, `HGM`), the velocity factors `FACT1`…`FACT5`, `FACT7`, `FACT8` (`VFACT_MOD`), `FACT6`, `FES1`–`FES3`, `FGSFJ`, `FGSFK` (`TAUKH_MOD`), `DDELM`, `FESTIME`, `THM` (`OLDROT2_MOD`), and with `LDIFAD` the higher-order terms in `DIFAD3_MOD` and `EGRIDDER_MOD`.

**The method.**
1. **Interface values.** At the midpoint $r_{m,i} = \tfrac12(r_i + r_{i-1})$, each quantity is found by 4-point Lagrange interpolation in $r$ over shells $i-2 \dots i+1$ (the first and last interfaces use the first or last four shells); $P$, $T$, $\rho$ are interpolated in the log. The actual gradient is $\nabla = \min(\nabla_\mathrm{rad}, \nabla_\mathrm{ad})$.
2. **Scales.** With $G$, $m$ the mass inside the interface, $H_P = P r^2/(\rho G m)$, $H_T = H_P/\nabla$, $\eta = \tfrac43\,r^3/(G m)$, and $\Delta\nabla = \max(\nabla_\mathrm{ad} - \nabla,\ \nabla_\mathrm{min})$ with a floor of $10^{-3}$ (larger at the ends of the range, including a $\mu$-gradient term).
3. **Eddington–Sweet circulation** (Endal and Sofia, paper II, as cited): $v_\mathrm{ES} = $ `FACT1`·`FACT2`·$\Omega^2$, with
   $$\texttt{FACT1} = \frac{1}{(\partial\ln\rho/\partial\ln T)\,\max(\nabla_\mathrm{ad}-\nabla,\,10^{-3})},\qquad \texttt{FACT2} = \frac{\nabla_\mathrm{ad}}{g}\,\eta\,\Bigl(\varepsilon - \frac{L}{m}\Bigr).$$
4. **GSF and $\mu$ currents.** `FACT3` $= |H_T r|$ for the Goldreich–Schubert–Fricke velocity; `FACT4` $= \frac{r^2}{G m\rho}\,(P - aT^4/3)/\sqrt g$ for the "fictitious $\mu$ currents" (Kippenhahn, IAU 66).
5. **Dynamical shear.** Stable when the Richardson number $\frac{\rho}{P}(\nabla_\mathrm{ad}-\nabla)\,g^2/(d\Omega/d\ln r)^2 > \tfrac14$, that is when
   $$\left|\frac{d\Omega}{d\ln r}\right| < \texttt{QWRMAX} = 2g\sqrt{\frac{\rho}{P}\max(\nabla_\mathrm{ad}-\nabla,\,10^{-3})}.$$
6. **Secular shear with $\mu$ gradients:** `FACT5` $= \frac{\rho g^2}{P\,\Delta\ln P}\cdot\frac{p_r - 1}{1 + 3p_r}$, where $p_r = aT^4/(3P)$ is the radiation-pressure fraction ($1 - p_r$ is the comment's "BETA") and the last factor is the comment's $-d\ln T/d\ln\mu$.
7. **Zahn-type terms** (`FES1`, `FES2`, `FES3`, `FV*`, and, with `LDIFAD`, `FACT7`, `FACD2`, `FACD3`, following Zahn and Maeder 1998 as the comments say), built from $F = P/(g\,\Delta\nabla\,c_P\,\rho\,T)$, $L/m$ and $\varepsilon$; and `THM` $= r^4/(\sqrt{m}\,G)$ for the $d\theta/dt$ term.

**KC's changes.** The unused argument `LCZ` was removed (KC 2025-05-31). (Also, "JvS 09/25" renamed the local `CPM` to `CPMI` to avoid a clash with `/MDPHY/`, now `MDPHY_MOD`.)

**Changed since `rp_1`.** `FACI`, formerly COMMON `/INTFAC/`, is a new last argument, owned by `SECULR`; `LDIFAD` comes from `NMLPAR_MOD` (COMMON `/VARFC/` is gone); otherwise declarations only: COMMON blocks to modules, `IMPLICIT NONE`. The statements are unchanged; no question is settled.

## Questions for the experts

1. **Index 0 with `LDIFAD`.** The `LDIFAD` block starts with `HTM` computed at shell `IMIN-1`; if `IMIN` can be 1, this reads `HP(0)`, `HR(0)`, `HS1(0)`. Can `IMIN` be 1 when `LDIFAD` is true?
2. **Many computed, unused values.** In the `LDIFAD` block, `V0`, `QC1R`, `QQC1RR`, `QQCHITR`, `HTP2`, `QHTR` are computed but used only in commented-out alternatives for `FACT7` and `FACT8`; `FACT8` is always 0. Which formulation is the current one, and can the rest go?
3. **Two floors for $\nabla_\mathrm{ad} - \nabla$.** `FACT1` and `QWRMAX` use a floor of $10^{-3}$; `FESTIME` and `FGSFK` use `DDEL` with the end-dependent floor `DMIN`; `DDELM` adds the $\mu$ gradient. The comment says 1/(∇ad − ∇) "is set to a maximum of 10^6", but the floor $10^{-3}$ gives a maximum of $10^3$. Which is intended?
4. **The definition of `ETA`.** `ETA = 2·(2/3)·r³/(G m)`. Is the factor 2 part of the physics or a leftover (the comment block gives no formula)?
