## Explanation

**Purpose.** This file takes one adaptive step of the Bulirsch–Stoer method for the envelope and atmosphere integration: the modified midpoint method for an increasing number of substeps, extrapolated to zero substep size. It is the Numerical Recipes routine `BSSTEP` (first edition, with rational extrapolation), extended with the physical arguments that the derivative routine needs.

**How it fits.**
- **Inputs:** `Y(3)`, `DYDX(3)` at `X0` (the independent variable), the trial step `HTRY`, the tolerance `EPS`, the scales `YSCAL`, the derivative routine `DERIV` (passed as an argument by ENVINT: [[qatm.f#QATM|QATM]] for the atmosphere, [[qenv.f#QENV|QENV]] for the envelope) and the stellar quantities it needs (`B`, `FPL`, `FTL`, `GL`, `RL`, `TEFFL`, `X`, `Z`, …); `IMAX` and `NUSE` from the module [[intpar_mod.f|INTPAR_MOD]] (initialized there to 11 and 7; both are also in the `PHYSICS` namelist, read by [[parmin.f#PARMIN|PARMIN]], so a run can change them).
- **Who calls it:** [[envint.f#ENVINT|ENVINT]].
- **What it calls:** [[mmid.f#MMID|MMID]] (modified midpoint) and [[ratext.f#RATEXT|RATEXT]] (rational extrapolation).
- **Outputs:** `Y` and `X0` advanced, `HDID` (the step taken), `HNEXT` (the suggested next step), `ERR` (the scaled error of each variable).

**The method.** For $i = 1, \dots, I_\mathrm{max}$, integrate across $H$ with $n_i$ = 2, 4, 6, 8, 12, 16, … midpoint substeps, and extrapolate the results in $(H/n_i)^2$ to zero. Accept the step when
$$\max_j \frac{|\epsilon_j|}{y_{\mathrm{scal},j}} < \mathrm{EPS}.$$
The next step is $0.95H$ if it took `NUSE` sequences, $1.2H$ if one fewer, otherwise $H\,n_{\mathrm{NUSE}-1}/n_i$. If all $I_\mathrm{max}$ sequences fail, retry with
$$H \leftarrow \frac{H/4}{2^{\lfloor (I_\mathrm{max} - N_\mathrm{use})/2 \rfloor}}.$$

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/INTPAR/` to `INTPAR_MOD`), `IMPLICIT NONE`.

## Questions for the experts

1. **The step-size underflow check.** `IF(X+H.EQ.X)` tests `X`, which here is the hydrogen abundance passed through to `DERIV`, not the independent variable `X0` (Numerical Recipes tests the independent variable). The check thus fires only if $H$ is negligible next to $X$, not next to the position. Should it be `X0+H.EQ.X0`? Since `X` is about 0.7, the check fires only once $H$ falls below about $10^{-16}X$; until then a failing step keeps shrinking $H$, and the run may stop with "ERROR IN BSSTEP" only late.

### BSSTEP

One Bulirsch–Stoer step (modified midpoint plus rational extrapolation) of the 3 envelope variables, with step-size control.
