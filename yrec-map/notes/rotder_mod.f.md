## Explanation

**Purpose.** `ROTDER_MOD` passes three quantities at each shell from the structure equations to the setup of rotational mixing. Shared by 2 routines. It replaces `COMMON/ROTDER/` (MHP via Claude, 10/14/26), less its arrays `SQOD` and `SQED`, which [`COEFFT`](coefft.f.md#coefft) stored and no routine read; `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.** All three are stored by `COEFFT` at each shell when `LROT` is set, and read by [`SETUPV`](https://github.com/yreclab/yrec/blob/7be4133/src/setupv.f#L3-L467) for the circulation's coefficients.
- `SQOT(JSON)`: the opacity's $`\partial\ln\kappa/\partial\ln T`$ (`QOT`); SETUPV forms $`\partial\ln\chi/\partial\ln T = 3 - \partial\ln\kappa/\partial\ln T`$ and its radial derivative.
- `SQET(JSON)`: the energy generation's $`\partial\ln\epsilon/\partial\ln T`$ (`QET`).
- `FRACNUC(JSON)`: the nuclear energy generation less the neutrino term and the gravitational term, as a fraction of the nuclear, (`SESUM` − `SEG(6)` − `SEG(7)`)/`SESUM` from `SCRTCH_MOD`, or 0 when `SESUM` $`\le 0`$.

**Design.** A blanket `USE ROTDER_MOD` in each routine.

**Changed since `rp_1`.** New file: `COMMON/ROTDER/` as a module, without the unused `SQOD`, `SQED`.
