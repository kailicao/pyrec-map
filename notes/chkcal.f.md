## Explanation

**Purpose.** This file drives the solar calibration: after each solar model, it checks whether the model has the solar luminosity and radius (and, optionally, the solar surface $Z/X$) at the solar age; if not, it computes new guesses for the hydrogen abundance $X$ and the mixing length $\alpha$ (and $Z$) for the next model, by a Newton step.

**How it fits.**
- **Inputs:** the arguments `BL` ($\log L/L_\odot$ of the model), `RL` ($\log R/R_\odot$, computed by the caller from $L$ and $T_\mathrm{eff}$), `N` (the current kind card) and `SOLZX` (the model's surface $Z/X$); the tolerances `TOLL`, `TOLR`, `TOLZ`, the switch `LCALSOLZX` and the target `CALSOLZX` in `/CALS2/`, set in [[parmin.f#PARMIN|PARMIN]] and [[setcal.f#SETCAL|SETCAL]].
- **Who calls it:** the main program ([[main.f#(file level)|main.f]]), when solar calibration is on (`LCALS`), at every third kind card (`MOD(NK,3).EQ.0`): "solar models in 3 kind cards" (MHP 5/96).
- **Outputs:** `LSOL` and the stored derivatives in `/CALSUN/` (also used by [[wrtmonte.f#WRTMONTE|WRTMONTE]]); the new $X$ (`RESCAL(2,N+1)`, and `XENV0A` for cards $N+1$ to $N+3$), $\alpha$ (`CMIXLA`, cards $N+1$ to $N+3$) and $Z$ (`RESCAL(3,N+1)`, `ZENV0A`) in `/CKIND/` and `/NEWXYM/`; lines to unit `IOWR`.

**The method.**
1. **Converged** if $|\log L/L_\odot| <$ `TOLL` and $|\log R/R_\odot| <$ `TOLR` and, with the $Z/X$ option, $|\log_{10}(Z/X) - \log_{10}(Z/X)_\odot| <$ `TOLZ`: set `LSOL` and return. The target is thus exactly $L_\odot$ and $R_\odot$.
2. **Newton step** with fixed partial derivatives ("empirical", LLP 6/28/09): $\partial\log L/\partial X = -3.78$, $\partial\log R/\partial X = -0.89$, $\partial\log L/\partial\alpha = 0.0139$, $\partial\log R/\partial\alpha = -0.050$. It solves
$$\log L + L_X\,\Delta X + L_\alpha\,\Delta\alpha = 0, \qquad \log R + R_X\,\Delta X + R_\alpha\,\Delta\alpha = 0,$$
that is
$$\Delta\alpha = \frac{\log L\,R_X/L_X - \log R}{R_\alpha - L_\alpha R_X/L_X}, \qquad \Delta X = -\frac{\log L + L_\alpha\,\Delta\alpha}{L_X}.$$
3. The new values go to kind cards $N+1$ to $N+3$, starting from those of card $N-2$ (the start of the current cycle). With the $Z/X$ option, $Z$ is scaled: $Z_\mathrm{new} = Z_\mathrm{old}\,(Z/X)_\odot / (Z/X)_\mathrm{model}$.

**Design.** An older method, which measured the derivatives with extra runs at kind cards 3, 6 and 9, is still in the file but skipped by `GOTO 1234`.

## Questions for the experts

1. **A derivative off by ten?** `DLDA = 0.0139D0` carries the comment "empirical result: +0.139". Which is right? With a value ten times too small, the Newton step in $\alpha$ is too large, though the iteration may still converge.
2. **The header.** It says "only called for even NK", but main.f calls it when `NK` is a multiple of 3, which matches the use of `N-2` and `N+1..N+3`.
3. **$Z/X$ not converged.** If $L$ and $R$ are within tolerance but $Z/X$ is not, the routine falls through to the Newton step and also changes $X$ and $\alpha$ slightly. Intended? Also, the convergence test uses $Z/X$ only when `CALSOLZX > 0`, but the update of $Z$ tests only `LCALSOLZX`, so a target of 0 would set $Z = 0$ (the default target is 0.02292).
4. **Dead code.** The skipped derivative runs (with `DX`, `DA` never set on that path) and the unused `ZLP`: can they go?

### CHKCAL

Checks a solar model against $L_\odot$, $R_\odot$ (and $Z/X$); if not calibrated, sets new $X$, $\alpha$ (and $Z$) for the next three kind cards by a Newton step with fixed derivatives.
