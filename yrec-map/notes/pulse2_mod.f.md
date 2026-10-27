## Explanation

**Purpose.** `PULSE2_MOD` holds the physics at the current point of the envelope or atmosphere integration, saved by [[qenv.f#QENV|`QENV`]] and [[qatm.f#QATM|`QATM`]] (the derivative routines of the integration) for [[envint.f#ENVINT|`ENVINT`]] to write in the envelope's pulsation output. Shared by 4 routines. It replaces `COMMON/PULSE2/` (MHP via Claude, 10/14/26).

**What its variables hold, who sets them, who reads them.** `QENV` and `QATM` set them when `LSAVE` or `LPUMOD` (`PULSE1_MOD`) is on (`QENV` sets `QQDP`, `QQDT`, `QQCP` always); `ENVINT` reads them.
- `QTL`, `QT`, `QPL`, `QP`, `QDL`, `QD`: $\log T$, $T$, $\log P$, $P$, $\log\rho$, $\rho$.
- `QO`, `QOL`: the opacity and its log (`QOL` is read nowhere); `QQOD`, `QQOT`: its logarithmic derivatives in $\rho$ and $T$.
- `QQDP`, `QQDT`, `QQCP`, `QRMU`, `QEMU`: the equation of state's $\partial\ln\rho/\partial\ln P$, $\partial\ln\rho/\partial\ln T$, $c_P$, `RMU`, `EMU`.
- `QDEL`, `QDELA`: $\nabla$ and $\nabla_\mathrm{ad}$.
- `QQED`, `QQET`: energy generation's derivatives, set to 0 by `QENV`, `QATM` and by `ENVINT` (which also sets `QQET`); `QFS`: set to 1 by `ENVINT` at the first point and by `QENV`.

**Design.** A blanket `USE PULSE2_MOD` in each routine. [[coefft.f#COEFFT|`COEFFT`]] also uses the module and has working variables of its own named `QP`, `QT` and `QTL` (the Henyey coefficients), which are therefore the module's: COEFFT overwrites them (so at `rp_1` too, where COEFFT declared `/PULSE2/`). Probably harmless, since `ENVINT` reads them only after `QENV` or `QATM` has set them.

**Changed since `rp_1`.** New file: `COMMON/PULSE2/` as a module.
