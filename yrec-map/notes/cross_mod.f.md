## Explanation

**Purpose.** `CROSS_MOD` holds the factors by which the nuclear reaction rates are adjusted for user-changed cross sections: the S-factor derivative factors and the N15+p branching factors, shared by 3 routines. It replaces `COMMON/CROSS/` (MHP via Claude, 10/14/26), less `SSTANDARD` (now in [`NMLPAR_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/nmlpar_mod.f#L32-L279)) and `LNEWNUC` (now in [`NMLBYPASS_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/nmlbypass_mod.f#L29-L118)).

**What its variables hold, who sets them, who reads them.**
- `QS0E(8)`, `QQS0EE(8)`: factors on the first-derivative ($`Q_2`$, $`Q_3`$) and second-derivative ($`Q_4`$, $`Q_5`$) terms of the eight pp and CNO rates, proportional to $`S'/S`$ and $`S''/S`$ relative to the reference values (REMAP's comments). [`REMAP`](https://github.com/yreclab/yrec/blob/7be4133/src/remap.f#L7-L297) sets them to 1, or, with `LNEWNUC`, from the user's S-factors and their derivatives.
- `FC12`, `FO16`: the factors on the $`^{15}\mathrm{N}+p \to {}^{12}\mathrm{C}+\alpha`$ and $`\to {}^{16}\mathrm{O}+\gamma`$ branches, 1 or, with `LNEWNUC`, the ratio of the user's S-factor to the reference; set in `REMAP`.
- All four are read by [`ENGEB`](engeb.f.md#engeb) and [`RATES`](https://github.com/yreclab/yrec/blob/7be4133/src/rates.f#L6-L677), which multiply the rate brackets and the branching ratio by them.

**Design.** A blanket `USE CROSS_MOD` in each of the three routines.

**Changed since `rp_1`.** New file: `COMMON/CROSS/` as a module, with `SSTANDARD` and `LNEWNUC` moved to the namelist modules.
