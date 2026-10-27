## Explanation

**Purpose.** `ENVPRT_MOD` holds the state at the current point of the envelope integration, passed from [[qenv.f#QENV|`QENV`]] (the right-hand side) to [[envint.f#ENVINT|`ENVINT`]] (the integrator), which stores it. It replaces `COMMON/ENVPRT/` (MHP via Claude, 10/14/26). All members are `REAL*8`.

**What its variables hold, who sets them, who reads them.** `QENV` sets them at each call ("07/02 always store the basic structure variables"):
- `EP`, `ET`, `ED`, `ER`: $\log P$, $\log T$, $\log\rho$, $\log r$; `ES`: $\log(m/M_*)$ (`SL - STOTAL`).
- `EO`: the opacity; `EBETA`: $\beta$; `EVEL`: the convective velocity; `EDEL(3)`: the radiative and adiabatic gradients and the actual one (`DELR`, `DELA`, `DEL`); `EFXION(3)`: the ionization fractions.
- `ENVINT` reads them to print the point and to store the envelope's run in [[envstruct_mod.f#ENVSTRUCT_MOD|`ENVSTRUCT_MOD`]].

**Design.** A blanket `USE ENVPRT_MOD`. QENV is called by the ODE solver through a fixed argument list, so its extra outputs go through the module. At `rp_1`, [[getnewenv.f#GETNEWENV|`GETNEWENV`]] and [[starin.f#STARIN|`STARIN`]] also declared the block without using it.

**Changed since `rp_1`.** New file: `COMMON/ENVPRT/` as a module (two unused declarations dropped).
