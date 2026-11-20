## Explanation

**Purpose.** `LIOV_MOD` holds the overshoot distance below the surface convection zone at the start and end of the step, used for light-element burning with overshoot ("11/91 CHANGED FOR LITHIUM BURNING WITH OVERSHOOT"), shared by 5 routines. It replaces `COMMON/LIOV/` (MHP via Claude, 10/14/26).

**What its variables hold, who sets them, who reads them.**
- `PSCAL1` (`REAL*8`): the overshoot distance at the end of the step, `ALPHAE` times the pressure scale height at the base of the convection zone, $`\alpha_e\,P r^2/(\rho\,G m)`$ (cm), with `LOVSTE` (in GETW also only with a convective surface); 0 otherwise. Set by [`GETW`](getw.f.md#getw) and by the [main program](main.f.md#file-level).
- `PSCAL0`: the same at the start of the step. The main program sets it at the start of each step, with `LEXCOM` ("store starting depth of C.Z. for light element burning," [main.f, lines 797–807](https://github.com/yreclab/yrec/blob/7be4133/src/main.f#L797-L807)); `GETW` and [`BURSMIX`](bursmix.f.md#bursmix) copy `PSCAL1` into it after burning, for the next step.
- Read by [`LIBURN`](liburn.f.md#liburn) and [`LIBURN2`](liburn2.f.md#liburn2), which extend the mixed region below the base of the convection zone by them.

**Design.** A blanket `USE LIOV_MOD`.

**Changed since `rp_1`.** New file: `COMMON/LIOV/` as a module.
