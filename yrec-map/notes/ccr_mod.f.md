## Explanation

**Purpose.** `CCR_MOD` holds the table of the electron (Fermi–Dirac) equation of state used for partial degeneracy. It replaces `COMMON/CCR/` (MHP via Claude, 10/14/26).

**What its variables hold, who sets them, who reads them.** [[setups.f#SETUPS|`SETUPS`]] reads from the Fermi-table file (unit `IFERMI`) the 43 abscissae in density `DVAL`, the degeneracies `ETAT8` and the table `DTABLE(5,43,20)`, and builds `IDEN(261)`, which maps a density bin of width 0.05 to the table row; [[eqrelv.f#EQRELV|`EQRELV`]] reads them all.

**Changed since `rp_1`.** New file: `COMMON/CCR/` as a module.
