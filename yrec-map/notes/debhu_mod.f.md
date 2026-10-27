## Explanation

**Purpose.** `DEBHU_MOD` holds the inputs of the Debye–Hückel correction to the equation of state: the constant `CDH`, the charges of the 18 heavy elements and the local composition, shared by 11 routines. It replaces `COMMON/DEBHU/` (MHP via Claude, 10/14/26), less the switch `LDH` and `ETADH0`, `ETADH1` (now in [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]]).

**What its variables hold, who sets them, who reads them.**
- `CDH`: $-\sqrt{\pi/(k\,m_H^3)}\,e^3/3$, set in [[setups.f#SETUPS|`SETUPS`]].
- `DHNUE(18)`: the charges of C, N, O, Ne, Na, Mg, Al, Si, P, S, Cl, Ar, Ca, Ti, Cr, Mn, Fe, Ni (SETUPS's comment), set in `SETUPS`.
- `XXDH`, `YYDH`, `ZZDH`, `ZDH(18)`: the local $X$, $Y$ (He3 + He4), $Z$ and the heavy-element abundances (C12 + C13, N14 + N15, O16 + O18 from `HCOMP`), copied from the shell's composition just before the equation of state is called, by nine routines: [[coefft.f#COEFFT|`COEFFT`]], [[crrect.f#CRRECT|`CRRECT`]], [[getnewenv.f#GETNEWENV|`GETNEWENV`]], [[hsubp.f#HSUBP|`HSUBP`]], [[physic.f#PHYSIC|`PHYSIC`]], [[sconvec.f#SCONVEC|`SCONVEC`]], [[starin.f#STARIN|`STARIN`]], [[wrtmod.f#WRTMOD|`WRTMOD`]] and [[wrtout.f#WRTOUT|`WRTOUT`]].
- All are read only by [[eqrelv.f#EQRELV|`EQRELV`]], which, with `LDH`, forms $\sum_i$ `DHNUE(i)` `ZDH(i)` and the Debye–Hückel pressure $P_\mathrm{DH} = $ `CDH` × (charge factor) × $\sqrt{\rho/T}\,\rho$.

**Design.** A blanket `USE DEBHU_MOD`. The composition reaches `EQRELV` through the module rather than as arguments, so each caller of the equation of state must copy it first; the copies are the same few lines in nine files. At `rp_1`, two files (EQSTAT, EQSTAT2) named the second member `XXDY`, harmless with COMMON's storage association.

**Changed since `rp_1`.** New file: `COMMON/DEBHU/` as a module, with `LDH`, `ETADH0`, `ETADH1` moved to `NMLPAR_MOD`.
