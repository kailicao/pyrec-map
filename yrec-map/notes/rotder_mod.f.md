## Explanation

**Purpose.** `ROTDER_MOD` passes three quantities at each shell from the structure equations to the setup of rotational mixing. Shared by 2 routines. It replaces `COMMON/ROTDER/` (MHP via Claude, 10/14/26), less its arrays `SQOD` and `SQED`, which [[coefft.f#COEFFT|`COEFFT`]] stored and no routine read; `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.** All three are stored by `COEFFT` at each shell when `LROT` is set, and read by [[setupv.f#SETUPV|`SETUPV`]] for the circulation's coefficients.
- `SQOT(JSON)`: the opacity's $\partial\ln\kappa/\partial\ln T$ (`QOT`); SETUPV forms $\partial\ln\chi/\partial\ln T = 3 - \partial\ln\kappa/\partial\ln T$ and its radial derivative.
- `SQET(JSON)`: the energy generation's $\partial\ln\epsilon/\partial\ln T$ (`QET`).
- `FRACNUC(JSON)`: the share of the energy generation that is nuclear, $(\epsilon_\mathrm{tot} - \epsilon_\nu)/\epsilon_\mathrm{tot}$ from `SESUM` and `SEG(6)`, `SEG(7)` (`SCRTCH_MOD`), or 0 when $\epsilon_\mathrm{tot} \le 0$.

**Design.** A blanket `USE ROTDER_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/ROTDER/` as a module, without the unused `SQOD`, `SQED`.
