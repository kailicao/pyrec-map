## Explanation

**Purpose.** `SOLID` makes a range of shells, `JSTART` to `JEND`, rotate as a solid body while conserving their total angular momentum. Given each shell's angular momentum per unit mass, it returns the common rotation rate $\Omega$ and the shells' moments of inertia. Its comment adds that it also gives $r_0$ and $\eta_2$ (`R0`, `ETA2`), which [[fpft.f#FPFT|FPFT]] needs.

**How it fits.**
- **Inputs:** arguments only: the shells' masses (`HS2`, probably in grams, since the angular momentum is the sum of `HS2*HJM`), specific angular momenta `HJM`, the previous rates `OMEGA`, and the structure (`HD`, `HR`, `HS`), passed on to the shape routines.
- **Who calls it:** the rotation routines that impose solid-body rotation on a zone: [[checkj.f#CHECKJ|CHECKJ]], [[getrot.f#GETROT|GETROT]], [[midmod.f#MIDMOD|MIDMOD]], [[seculr.f#SECULR|SECULR]] and [[wczimp.f#WCZIMP|WCZIMP]] (for convection zones, by its name; WCZ, removed since `rp_1`, was another).
- **What it calls:** [[shape.f#SHAPE|SHAPE]] (the distortion of the shells, `ETA2` and `R0`) and [[momi.f#MOMI|MOMI]] (each shell's moment of inertia `HI` and $dI/d\Omega$, `QIW`).
- **Outputs:** `OMEGA`, `HI`, `QIW`, `ETA2`, `R0` and an updated `HJM`, all through the arguments.
- **Modules:** `ERRMOM_MOD` (the tolerance `TOLERI`, used only here and in [[checkj.f#CHECKJ|CHECKJ]]; no routine or initializer gives it a value: CHECKJ saves it (`TOLER0 = TOLERI`), relaxes it to `MAX(DJOK*1.0D-2,TOLER0)` around its call to GETROT, and restores it); `DISK_MOD` (the age `SAGE`, shared with [[getw.f#GETW|GETW]], [[seculr.f#SECULR|SECULR]], [[mdot.f#MDOT|MDOT]] and others); `NMLPAR_MOD` (the disk-locking parameters: the locking time `TDISK`, the locked rate `PDISK` and the switch `LDISK`, namelist parameters read by [[parmin.f#PARMIN|PARMIN]]); `DIMENSIONS_MOD` (`JSON`).

**The method.** Let $m_j$ be `HS2(J)` and $j_j$ be `HJM(J)`. The target is the zone's total angular momentum,

$$J = \sum_{j=J_\mathrm{start}}^{J_\mathrm{end}} m_j\, j_j .$$

The first guess for $\Omega$ is the mean of the previous rates. With every shell at $\Omega$, `SHAPE` and `MOMI` give the moments of inertia $I_j(\Omega)$ and $I'_j = dI_j/d\Omega$. With $I = \sum I_j$ (`CZI`) and $I' = \sum I'_j$ (`CZQIW`), a Newton step solves $\Omega\, I(\Omega) = J$:

$$\Delta\Omega = \frac{J - \Omega I}{I + \Omega I'} ,$$

repeated until $|J - \Omega I|/J \le$ `TOLERI`, or 20 times. Finally each shell's specific angular momentum is reset to $j_j = I_j\,\Omega / m_j$.

**Disk locking.** For the surface convection zone (`JEND = M`, more than one shell), when `LDISK` is set and the age `SAGE` is at most `TDISK`, $\Omega$ is fixed to `PDISK` with no iteration, and the angular momentum follows from it ("MHP 9/94").

**KC's changes.** The call to `MOMI` drops the arguments `HD` and `M` (2025-05-31), matching `MOMI`'s new argument list.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/ERRMOM/` to `ERRMOM_MOD`; `/DISK/` split between `DISK_MOD` (`SAGE`) and `NMLPAR_MOD` (`TDISK`, `PDISK`, `LDISK`); the unused `/LUOUT/` dropped), the array size `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`. One caller, WCZ, was removed with its file.

## Questions for the experts

1. **The tolerance `TOLERI`.** Nothing initializes it: [[checkj.f#CHECKJ|CHECKJ]] only relaxes it around its call to GETROT and then restores the old value. Outside those calls `TOLERI` is zero (where the compiler zero-initializes module variables; `ERRMOM_MOD` gives it no initial value), so the test `DABS(DELJ/CZJ).GT.TOLERI` always holds and the Newton loop always runs its 20 steps. Is a tolerance missing from the setup?
2. **No warning after 20 steps.** When the Newton iteration has not converged after 20 steps, `SOLID` keeps the last guess silently. Should it report this?
3. **`PDISK` as a rate.** Under disk locking, `WGUESS = PDISK`, which is used as $\Omega$. `NMLPAR_MOD` gives `PDISK` the initial value `7.2722D-6`, which is $2\pi/(10\ \mathrm{d})$ in rad/s: an angular rate, for a period of 10 days. The comment calls it the "period at which locking is set". Should the comment say "rate", and do users who set it in the namelist know it is a rate?
4. **A zone of zero angular momentum.** The test `DABS(DELJ/CZJ)` divides by the total angular momentum, which is zero for a non-rotating zone.

### SOLID

Solid-body rotation of shells `JSTART`–`JEND` at fixed total angular momentum, by Newton iteration on $\Omega I(\Omega) = J$; or, under disk locking, at the fixed rate `PDISK`.
