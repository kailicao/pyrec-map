## Explanation

**Purpose.** `LIOV_MOD` holds the overshoot distance below the surface convection zone at the start and end of the step, used for light-element burning with overshoot ("11/91 changed for lithium burning with overshoot"), shared by 5 routines. It replaces `COMMON/LIOV/` (MHP via Claude, 10/14/26).

**What its variables hold, who sets them, who reads them.**
- `PSCAL1` (`REAL*8`): the overshoot distance at the end of the step, `ALPHAE` times the pressure scale height at the base of the convection zone, $\alpha_e\,P r^2/(\rho\,G m)$ (cm), with `LOVSTE` and a convective surface; 0 otherwise. Set by [[getw.f#GETW|`GETW`]] and by the [[main.f#(file level)|main program]].
- `PSCAL0`: the same at the start of the step. The main program sets it at the start of a run; `GETW` and [[bursmix.f#BURSMIX|`BURSMIX`]] copy `PSCAL1` into it after burning, for the next step.
- Read by [[liburn.f#LIBURN|`LIBURN`]] and [[liburn2.f#LIBURN2|`LIBURN2`]], which extend the mixed region below the base of the convection zone by them.

**Design.** A blanket `USE LIOV_MOD`.

**Changed since `rp_1`.** New file: `COMMON/LIOV/` as a module.
