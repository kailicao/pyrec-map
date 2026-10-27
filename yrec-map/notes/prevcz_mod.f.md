## Explanation

**Purpose.** `PREVCZ_MOD` carries the state of the surface convection zone and of light-element burning from one step to the next, for [[liburn.f#LIBURN|`LIBURN`]] and [[liburn2.f#LIBURN2|`LIBURN2`]]. Shared by 3 routines. It replaces `COMMON/PREVCZ/` (MHP via Claude, 10/14/26).

**What its variables hold, who sets them, who reads them.**
- `RBASE0`: the radius of the base of the convection zone at the start of the step (with overshoot). `LIBURN`, `LIBURN2` compute it from the starting model when it is 0, and store the step's ending base in it for the next step; the [[main.f#(file level)|main program]] resets it to 0 when `LEXCOM` is set.
- `JENVOS`: the shell of the envelope's base at the end of the step, stored by `LIBURN`, `LIBURN2` and used as the next step's starting `JENV0` when `RBASE0` is already known.
- `BLI6OLD`, `BLI7OLD`, `BBE9OLD`: the mass-averaged burning rates of ⁶Li, ⁷Li and ⁹Be in the convection zone at the end of the step, stored by `LIBURN`, `LIBURN2` for the start of the next; `LIBURN`, `LIBURN2` recompute the starting rates when `BLI6OLD` ≤ 0, and the main program sets all three to 0 when `LEXCOM` is set.

**Design.** A blanket `USE PREVCZ_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/PREVCZ/` as a module.
