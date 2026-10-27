## Explanation

**Purpose.** `ATMPRT_MOD` holds the state at the last point of the atmosphere integration (or the fitting point of a tabulated atmosphere), for the envelope integration and the output. It replaces `COMMON/ATMPRT/` (MHP via Claude, 10/14/26), where the optical depth was named `TAU`; it is now `TAUL`.

**What its variables hold, who sets them, who reads them.**
- `TAUL` ($\log\tau$), `AP` ($\log P$), `AT` ($\log T$): set by [[qatm.f#QATM|`QATM`]] at each point of the atmosphere integration; `AP` and `AT` also by the table routines [[surfp.f#SURFP|`SURFP`]] and [[kcsurfp.f#KCSURFP|`KCSURFP`]], and `AT` by [[alsurfp.f#ALSURFP|`ALSURFP`]].
- `AD` ($\log\rho$), `AO` (the opacity), `AFXION(3)` (the ionization fractions): set by `QATM` only when the model is stored or written for pulsation (`LSAVE`, `LPUMOD`).
- Read by [[envint.f#ENVINT|`ENVINT`]], which writes them with the stored model, and by [[massloss.f#MASSLOSS|`MASSLOSS`]] (`AP`, `AT`) and the table routines.

**Changed since `rp_1`.** New file: `COMMON/ATMPRT/` as a module, `TAU` renamed `TAUL`.
