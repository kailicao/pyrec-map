## Explanation

**Purpose.** `DEBHU_MOD` holds the inputs of the Debye–Hückel correction to the equation of state: the constant `CDH`, the charges of the 18 heavy elements, and the local composition, shared by 11 routines. It replaces `COMMON/DEBHU/` (MHP via Claude, 10/14/26), less the switch `LDH` and `ETADH0`, `ETADH1` (now in [`NMLPAR_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/nmlpar_mod.f#L32-L279)).

**What its variables hold, who sets them, who reads them.**
- `CDH`: $`-\sqrt{\pi/(k\,m_H^3)}\,e^3/3`$, set in [`SETUPS`](https://github.com/yreclab/yrec/blob/7be4133/src/setups.f#L16-L396).
- `DHNUE(18)`: the charges of C, N, O, Ne, Na, Mg, Al, Si, P, S, Cl, Ar, Ca, Ti, Cr, Mn, Fe, Ni (SETUPS's comment), set in `SETUPS`.
- `XXDH`, `YYDH`, `ZZDH`, `ZDH(18)`: the local $`X`$, $`Y`$ (He3 + He4), $`Z`$, and the heavy-element abundances (C12 + C13, N14 + N15, O16 + O17 + O18 from `HCOMP`), copied from the shell's composition just before the equation of state is called, by nine routines: [`COEFFT`](coefft.f.md#coefft), [`CRRECT`](crrect.f.md#crrect), [`GETNEWENV`](getnewenv.f.md#getnewenv), [`HSUBP`](hsubp.f.md#hsubp), [`PHYSIC`](https://github.com/yreclab/yrec/blob/7be4133/src/physic.f#L3-L191), [`SCONVEC`](https://github.com/yreclab/yrec/blob/7be4133/src/sconvec.f#L4-L302), [`STARIN`](starin.f.md#starin), [`WRTMOD`](wrtmod.f.md#wrtmod), and [`WRTOUT`](wrtout.f.md#wrtout).
- All are read only by [`EQRELV`](eqrelv.f.md#eqrelv), which, with `LDH`, forms $`\sum_i`$ `DHNUE(i)` `ZDH(i)` and the Debye–Hückel pressure $`P_\mathrm{DH} =`$ `CDH` $`\times`$ (charge factor) $`\times \sqrt{\rho/T}\,\rho`$.

**Design.** A blanket `USE DEBHU_MOD`. The composition reaches `EQRELV` through the module rather than as arguments, so each caller of the equation of state must copy it first; the copies are the same few lines in nine files. At `rp_1`, two files (EQSTAT, EQSTAT2) named the member `XXDH` `XXDY`, harmless with COMMON's storage association.

**Changed since `rp_1`.** New file: `COMMON/DEBHU/` as a module, with `LDH`, `ETADH0`, `ETADH1` moved to `NMLPAR_MOD`.
