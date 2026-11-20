## Explanation

**Purpose.** `PULSE2_MOD` holds the physics at the current point of the envelope or atmosphere integration, saved by [`QENV`](https://github.com/yreclab/yrec/blob/7be4133/src/qenv.f#L6-L136) and [`QATM`](https://github.com/yreclab/yrec/blob/7be4133/src/qatm.f#L6-L125) (the derivative routines of the integration) for [`ENVINT`](envint.f.md#envint) to write in the envelope's pulsation output. Shared by 4 routines. It replaces `COMMON/PULSE2/` (MHP via Claude, 10/14/26).

**What its variables hold, who sets them, who reads them.** `QENV` and `QATM` set them when `LSAVE` or `LPUMOD` (`PULSE1_MOD`) is on (`QENV` sets `QQDP`, `QQDT`, `QQCP` always); `ENVINT` reads them.
- `QTL`, `QT`, `QPL`, `QP`, `QDL`, `QD`: $`\log T`$, $`T`$, $`\log P`$, $`P`$, $`\log\rho`$, $`\rho`$.
- `QO`, `QOL`: the opacity and its log (`QOL` is read nowhere: unused?); `QQOD`, `QQOT`: its logarithmic derivatives in $`\rho`$ and $`T`$.
- `QQDP`, `QQDT`, `QQCP`, `QRMU`, `QEMU`: the equation of state's $`\partial\ln\rho/\partial\ln P`$, $`\partial\ln\rho/\partial\ln T`$, $`c_P`$, `RMU`, `EMU`.
- `QDEL`, `QDELA`: $`\nabla`$ and $`\nabla_\mathrm{ad}`$.
- `QQED`, `QQET`: energy generation's derivatives, set to 0 by `QENV`, `QATM`, and `ENVINT` (which also sets `QQET`); `QFS`: set to 1 by `ENVINT` at the first point and for the atmosphere, and by `QENV` to the mass fraction $`m/M`$ (`10**(SL-STOTAL)`, [qenv.f, line 119](https://github.com/yreclab/yrec/blob/7be4133/src/qenv.f#L119)).

**Design.** A blanket `USE PULSE2_MOD` in each routine. [`COEFFT`](coefft.f.md#coefft) also uses the module and has working variables of its own named `QP`, `QT`, and `QTL` (the Henyey coefficients), which are therefore the module's: COEFFT overwrites them (so at `rp_1` too, where COEFFT declared `/PULSE2/`). ENVINT does not read `QP`; it reads `QT` and `QTL` in its pulsation blocks, each just after a call of QATM or QENV that passes ENVINT's `LPRT` as `LSAVE` ([lines 400–475](https://github.com/yreclab/yrec/blob/7be4133/src/envint.f#L400-L475), [lines 569–595](https://github.com/yreclab/yrec/blob/7be4133/src/envint.f#L569-L595), [lines 700–725](https://github.com/yreclab/yrec/blob/7be4133/src/envint.f#L700-L725)). The two envelope blocks run only with `LPRT` on, so they read the values QENV has just saved. The atmosphere block also runs when `LCLCD` or `LSTCH` is on ([line 433](https://github.com/yreclab/yrec/blob/7be4133/src/envint.f#L433)); with `LPRT` off, QATM saves nothing in that step (`LPUMOD` is off too), and the block reads the values stored last, by QATM, QENV, or COEFFT.

**Changed since `rp_1`.** New file: `COMMON/PULSE2/` as a module.
