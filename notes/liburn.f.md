## Explanation

**Purpose.** `LIBURN` burns the light elements ⁶Li, ⁷Li and ⁹Be (`HCOMP(13)`, `HCOMP(14)`, `HCOMP(15)`) over one time step: in the radiative interior shell by shell, and in the surface convection zone as one mixed reservoir, with the rates changing during the step. Its accuracy is controlled by Richardson-type extrapolation over ever finer substeps. Its comment: "lithium and beryllium burning in a non-rotating model".

**How it fits.**
- **Who calls it:** the main program, [[main.f#(file level)|main.f]], at the end of each step when light elements are followed (`LEXCOM`) and the model is not rotating with rotational mixing; and [[getw.f#GETW|`GETW`]] for rotating models. The cheaper variant [[liburn2.f#LIBURN2|`LIBURN2`]] (one step, no extrapolation) is used by `GETW` and [[bursmix.f#BURSMIX|`BURSMIX`]].
- **Inputs:** `DELTS` (the step; main.f passes it in seconds), `HCOMP`, `HR`, `HS1`, `HS2`, `HT`, `M`; `JNENV0` and `JNENV`, the index of the base of the surface convection zone at the start and at the end of the step. The rates at the start (`OLDRAT`) and end (`NEWRAT`) of the step, from [[lirate88.f#LIRATE88|`LIRATE88`]].
- **Output:** the new `HCOMP(13..15)`.
- **Calls:** [[ratext.f#RATEXT|`RATEXT`]] (rational extrapolation) and `SAFEDIVEXP` (below).
- **COMMON blocks:** `NEWRAT`, `OLDRAT` (the rates; with `LIRATE88`, `LIBURN2`, `GETW`, `BURSMIX`); `SCRTCH` (`SDEL`, the gradients $\nabla_\mathrm{rad}$, $\nabla$, $\nabla_\mathrm{ad}$ from `PHYSIC`); `MDPHY` (the same for rotating models); `OLDMOD` (`HRO`, the old radii); `DPMIX` (`LOVSTE`, envelope overshoot); `LIOV` (`PSCAL0`, `PSCAL1`, the overshoot distances at the start and end of the step, set in main.f); `PREVCZ` (`RBASE0`, the end-of-step rates `BLI6OLD`… and `JENVOS`, kept for the next step); `MASSCHG` and `DEUTER` (mass accretion: `LMDOT`, `DMDT0`, `COMPACC`, `FMASSACC`); `ROT`, `CONST1`, `LUOUT`.

**The method.**
1. **Base of the convection zone.** Locate the base between the last convective point and the one below by linear interpolation of $\nabla_\mathrm{ad} - \nabla_\mathrm{rad}$: an offset $f_x \in [-\tfrac12, \tfrac12]$ of a zone. With envelope overshoot, move the base down by the overshoot distance (`PSCAL0`, `PSCAL1`) at the start and end of the step.
2. **Radiative interior** (points below both bases, from the centre out, stopping at the first point where the ⁹Be rate, at the start or at the end, is at most $10^{-32}$; points where all three abundances are below $10^{-24}$ are skipped). Above $\log T = 7$ the elements are destroyed outright. Elsewhere, for $n$ = 2, 4, 6, 8, 12, … , 96 substeps of $h = \Delta t/n$: the rate at substep $k$ is interpolated linearly in its log between start and end,
$$\ln\lambda_k = \ln\lambda_0 + \tfrac{k - 1/2}{n}\,(\ln\lambda_1 - \ln\lambda_0),$$
and the abundance decays as $x \leftarrow x\,e^{-\lambda_k h}$ (set to 0 when $\lambda_k h \ge 30$). The results for successive $n$ are extrapolated to $h \to 0$ in $h^2$ by `RATEXT`; it stops when the relative error estimates are below $10^{-6}$. Values below $10^{-24}$ are set to 0.
3. **Convection zone.** The zone's starting abundance is the mass-weighted mean over the zone at the start (or at the end, if the zone deepened). Its rate is the mass-weighted mean $\bar\lambda = \sum\lambda_i\Delta m_i/\sum\Delta m_i$ at the start (or the previous step's end value) and at the end, the bottom point's mass and rate adjusted for the offset $f_x$. The same substepping and extrapolation as in step 2 follow. With accretion (`LMDOT`, `DMDT0` > 0), accreted material of composition `COMPACC` is added at each substep, assumed to burn for half a substep on arrival, and mixed in by mass with the factor `FMASSACC`. All points from the shallower of the two bases (`MAXJ`) to the surface get the result. The adjusted rates of the bottom point stay in `NEWRAT` (only its mass is restored).
4. **Region left by a retreating zone** (points `JENV0`..`JENV`−1, between the old and the new base): each is burned once with a rate weighted geometrically between its own end-of-step rate and the zone's start rate,
$$x \leftarrow x\,\exp\!\left(-\Delta t\,\lambda_\mathrm{rad}^{\,f}\,\bar\lambda_0^{\,1-f}\right),\qquad f = \frac{m - m_\mathrm{beg}}{m_\mathrm{beg} - m_\mathrm{end}},$$
with $m$ = `HS1` (the mass inside the point, in g), and $m_\mathrm{beg}$, $m_\mathrm{end}$ the masses at the old and the new base (`HSBEG`, `HSEND`; midpoints between the base point and the one below). The comment says that a point a fraction $f$ of the way (in mass) from the old base to the new one spent the fraction $f$ of the step in the zone, so $f$ should lie between 0 and 1; as written, $f$ is negative (question 7).

**Design.** With accretion it prints a line to the terminal (`WRITE(*,913)`) at every level of the extrapolation.

**KC's changes.**
- 2025-05-31: the unused argument `HD` removed.
- 2025-05-31: `SAFEDIVEXP` added and used in step 4 for ⁶Li and ⁷Li, to prevent a floating-point exception when the exponent is very large.

## Questions for the experts

1. **Units of the step.** The comments call `DELT` "the fractional timestep in years", but main.f passes `DELTS` in seconds, and the rates from `LIRATE88` are probably per second ($\rho X N_A\langle\sigma v\rangle$). Which comment is stale?
2. **A radius from the old model.** In the overshoot branch, `DR = EXP(CLN*HRO(J+1)) - R` mixes the old model's radius `HRO` with the new model's `R`; every other line uses `HR`. A typo for `HR(J+1)`?
3. **Points newly in the convection zone.** When the zone deepens (`JENV` < `JENV0`), the result of step 3 is written only from `MAXJ` = `JENV0` outward, and the radiative loop stops below `JENV`. So the points between the new and the old base keep their old abundances, although the zone's starting abundance includes them. Is the mixing of those points left to a later routine?
4. **⁹Be is not protected.** `SAFEDIVEXP` guards ⁶Li and ⁷Li in step 4 but not ⁹Be, whose line is unchanged (`HCOMP(15,I)/EXP(DBE9)`), and the comment "remember to add failsafes for large depletion" remains. Should ⁹Be get the same guard, and `LIBURN2` too?
5. **The radiative loop's exit.** It leaves the loop at the first point (from the centre) where the ⁹Be rate is at most $10^{-32}$, assuming the rates only fall outward; `LIBURN2` skips such points instead. Which is meant?
6. **Hard-coded values.** The destruction temperature $\log T = 7$, the cut $\lambda h \ge 30$, the floor $10^{-24}$ and the tolerances $10^{-6}$.

7. **The sign of `FRAD` (apparent bug).** In step 4, `DMASS = HSBEG - HSEND` is negative when the zone retreats (`JENV` > `JENV0`, and `HS1` grows outward), while `HS1(I) - HSBEG` is positive, so `FRAD` lies between −1 and 0. The rate $\lambda_\mathrm{rad}^{f}\bar\lambda_0^{1-f}$ then extrapolates beyond the zone's rate instead of interpolating between the two. Should it be `DMASS = HSEND - HSBEG`? And with that fixed, the code gives the radiative rate the weight $f$, while the comment says the point spent the fraction $f$ of the step in the zone; is the weighting the right way round? `LIBURN2` has the same lines.
8. **The bottom point's rates.** The adjustment of `RLI6`, `RLI7`, `RBE9` at `JENV` for the offset $f_x$ is not undone (unlike `HS2(JENV)`), so `NEWRAT` keeps the adjusted values, which `GETW` and `BURSMIX` copy into the start rates `OLDRAT` for the next substep. Intended?

### LIBURN

Light-element burning with substeps and extrapolation, radiative and convective parts (above).

### SAFEDIVEXP

KC's guard (2025-05-31): replaces $x$ by $x/e^{a}$ when $a < 709.78$ (the largest argument for which $e^a$ fits in double precision), and by 0 otherwise.
