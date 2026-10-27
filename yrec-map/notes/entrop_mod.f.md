## Explanation

**Purpose.** `ENTROP_MOD` holds the rates of change of the structure variables in the last model, used for a better first guess of the next one (`LNEWS`), shared by the [[main.f#(file level)|main program]] and [[hpoint.f#HPOINT|`HPOINT`]]. It replaces `COMMON/ENTROP/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]].

**What its variables hold, who sets them, who reads them.**
- `HTT0`, `HPP0` (`JSON` each): the changes of $\log T$ and $\log P$ over the last step, divided by the step `DELTS`; `HLL0`: the relative change of $L$, $2(L - L_\mathrm{old})/(L + L_\mathrm{old})$, per unit time; `HRR0`: the change of $\log r$ per unit time.
- The main program zeroes them at the start of a run and when `LNEWS` is off or the step is not positive, sets them after each converged model ("7/91 store changes in the structure"), and reads them to estimate the next model's structure: $\Delta T = $ `HTT0*DELTS`, and so on.
- `HPOINT` interpolates them onto the new mass grid when points are added or removed ("7/91 add entropy term interpolation").

**Design.** A blanket `USE ENTROP_MOD`. The comments call them "entropy terms", but they hold time derivatives of the structure.

**Changed since `rp_1`.** New file: `COMMON/ENTROP/` as a module.
