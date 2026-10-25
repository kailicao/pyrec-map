## Explanation

**Purpose.** `WTIME` limits the time step of a rotating model by the change of the angular velocity since the previous model: if $\Omega$ changed by more than the user's fraction `DTWIND` somewhere (default 0.08, by the comment), the step shrinks; if less, it grows.

**How it fits.**
- **Inputs:** the previous step `DELTS`, `M`, the current `OMEGA`; through COMMON blocks, the previous model's rates `WOLD` (`OLDROT`, saved by [[starin.f#STARIN|STARIN]] and the rotation routines), `DTWIND` (`CT2`, from [[parmin.f#PARMIN|PARMIN]]) and the step-change limit `ATIME(13)` (`CTLIM`).
- **Who calls it:** only [[htimer.f#HTIMER|HTIMER]], which takes the smallest of its candidate steps.
- **Outputs:** `DELTSW`, the rotation-based step, and `DWMAX`, the largest relative change.

**The method.** The largest relative change over all shells,
$$\delta_\mathrm{max} = \max_i \frac{2\,|\Omega_i - \Omega_i^\mathrm{old}|}{\Omega_i + \Omega_i^\mathrm{old}},$$
gives $f = \delta_\mathrm{max}/$`DTWIND`, limited to $1/a \le f \le a$ with $a$ = `ATIME(13)` (MHP 10/14), and $\Delta t_\Omega = \Delta t/f$. If nothing changed ($f = 0$), $\Delta t_\Omega = 10^{20}$, so that rotation does not limit the step.

## Questions for the experts

1. **A non-rotating shell.** If $\Omega_i = \Omega_i^\mathrm{old} = 0$ in any shell, the ratio is 0/0.
2. **The comment and the limiter.** The comment says the change is restricted to "a factor of ATIME(14)%", while the code uses `ATIME(13)` as a factor (MHP 10/14).
3. **`IWMAX`** (the shell of the largest change) is found but not returned or used.

### WTIME

Rotation-based time step: $\Delta t/f$ with $f$ the largest relative change of $\Omega$ over `DTWIND`, limited by `ATIME(13)`.
