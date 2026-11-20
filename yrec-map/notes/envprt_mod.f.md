## Explanation

**Purpose.** `ENVPRT_MOD` holds the state at the current point of the envelope integration, passed from [`QENV`](https://github.com/yreclab/yrec/blob/7be4133/src/qenv.f#L6-L136) (the right-hand side) to [`ENVINT`](envint.f.md#envint) (the integrator), which stores it. It replaces `COMMON/ENVPRT/` (MHP via Claude, 10/14/26). All members are `REAL*8`.

**What its variables hold, who sets them, who reads them.** `QENV` sets them at each call ("07/02 ALWAYS STORE THE BASIC STRUCTURE VARIABLES."), except `EO`, which it sets only with `LSAVE` or `LPUMOD` ([qenv.f, lines 96–102](https://github.com/yreclab/yrec/blob/7be4133/src/qenv.f#L96-L102)):
- `EP`, `ET`, `ED`, `ER`: $`\log P`$, $`\log T`$, $`\log\rho`$, $`\log r`$; `ES`: $`\log(m/M_*)`$ (`SL - STOTAL`).
- `EO`: the opacity; `EBETA`: $`\beta`$; `EVEL`: the convective velocity; `EDEL(3)`: the radiative and adiabatic gradients and the actual one (`DELR`, `DELA`, `DEL`); `EFXION(3)`: the ionization fractions.
- `ENVINT` reads them to print the point and to store the envelope's run in [`ENVSTRUCT_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/envstruct_mod.f#L19-L47).

**Design.** A blanket `USE ENVPRT_MOD`. QENV is called by the ODE solver through a fixed argument list, so its extra outputs go through the module. At `rp_1`, [`GETNEWENV`](getnewenv.f.md#getnewenv) and [`STARIN`](starin.f.md#starin) also declared the block without using it.

**Changed since `rp_1`.** New file: `COMMON/ENVPRT/` as a module (two unused declarations dropped).
