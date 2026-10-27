## Explanation

**Purpose.** `GRAB_MOD` holds the energy generation of the He3+He3 reaction and of the two He3-burning reactions together, and their luminosities shell by shell ("JVS 10/11 need to grab He3 energy generation"), shared by [[engeb.f#ENGEB|`ENGEB`]] and [[coefft.f#COEFFT|`COEFFT`]]. It replaces `COMMON/GRAB/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]].

**What its variables hold, who sets them, who reads them.**
- `ENGHE3`, `HE3ALL`: the energy generation rate (per gram) of He3+He3 (`DG(2)`) and of He3+He3 plus He3+He4 (`DG(2)+DG(3)`) at the current shell, set by `ENGEB`; read by `COEFFT`.
- `UMHE33(JSON)`, `UMHEAL(JSON)`: the same times the shell's mass, in solar luminosities, set by `COEFFT`; read nowhere.

**Design.** A blanket `USE GRAB_MOD`. At `rp_1`, the [[main.f#(file level)|main program]] and [[wrtout.f#WRTOUT|`WRTOUT`]] also declared the block, without using it; probably the output that would have used these was never written.

**Changed since `rp_1`.** New file: `COMMON/GRAB/` as a module (two unused declarations dropped).

## Questions for the experts

1. **Luminosities no one reads.** `UMHE33` and `UMHEAL` are computed at every shell and read nowhere (so also at `rp_1`). Should they be written out, or removed with `ENGHE3`, `HE3ALL`?
