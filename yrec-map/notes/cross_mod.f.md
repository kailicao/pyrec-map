## Explanation

**Purpose.** `CROSS_MOD` holds the factors by which the nuclear reaction rates are adjusted for user-changed cross sections: the S-factor derivative factors and the N15+p branching factors, shared by 3 routines. It replaces `COMMON/CROSS/` (MHP via Claude, 10/14/26), less `SSTANDARD` (now in [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]]) and `LNEWNUC` (now in [[nmlbypass_mod.f#NMLBYPASS_MOD|`NMLBYPASS_MOD`]]).

**What its variables hold, who sets them, who reads them.**
- `QS0E(8)`, `QQS0EE(8)`: factors on the first-derivative ($Q_2$, $Q_3$) and second-derivative ($Q_4$, $Q_5$) terms of the eight pp and CNO rates, proportional to $S'/S$ and $S''/S$ relative to the reference values (REMAP's comments). [[remap.f#REMAP|`REMAP`]] sets them to 1, or, with `LNEWNUC`, from the user's S-factors and their derivatives.
- `FC12`, `FO16`: the factors on the N15+p → C12+α and → O16+γ branches, 1 or, with `LNEWNUC`, the ratio of the user's S-factor to the reference; set in `REMAP`.
- All four are read by [[engeb.f#ENGEB|`ENGEB`]] and [[rates.f#RATES|`RATES`]], which multiply the rate brackets and the branching ratio by them.

**Design.** A blanket `USE CROSS_MOD` in each of the three routines.

**Changed since `rp_1`.** New file: `COMMON/CROSS/` as a module, with `SSTANDARD` and `LNEWNUC` moved to the namelist modules.
